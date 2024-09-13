from logging import getLogger

from huey.contrib.djhuey import on_commit_task

from .functions import save_temp_data_to_permanent
from .models import DataImport


@on_commit_task()
def ingest_data(data_import_pk: int) -> None:
    """Initiate the ingestion of data into the DB.

    If the status of the data import is "not queued", the request is processed. The data
    loaded and saved to the database. The status is updated to completed or failed
    depending on the outcome.
    """
    data_import = DataImport.objects.get(pk=data_import_pk)
    if data_import.status != "N":
        return

    data_import.status = "Q"
    data_import.save()

    try:
        getLogger("huey").info("Ingesting data for %s", data_import)
        data_import.start_date, data_import.end_date, data_import.records = (
            save_temp_data_to_permanent(
                data_import.station, data_import.format, data_import.rawfile
            )
        )
        data_import.status = "C"
        data_import.log = "Data ingestion completed successfully"
        getLogger("huey").info("Data ingestion for %s completed", data_import)
    except Exception as e:
        data_import.status = "F"
        data_import.log = str(e)
        getLogger("huey").exception("Error ingesting data for %s", data_import)
    finally:
        data_import.save()
