"""Run a benchmark on the queries to the database.

This script will run a series of queries to the database and measure the time it takes.
The queries are random and the number of records returned is also random. The idea is
to measure the performance of the database when querying for different time ranges and
different variables.
"""

import os
import random
import sys
import time
from datetime import datetime, timedelta

import django
import pandas as pd
from tqdm import tqdm

# This needs to be done before importing any model
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangomain.settings")
django.setup()

from measurement.models import Measurement  # noqa: E402

# Now we can import the models
from station.models import Station  # noqa: E402
from variable.models import Variable  # noqa: E402

# These query the WHOLE database, and they are pretty fast, so things look good.
stations = [
    Station.objects.get(pk=v)
    for v in set(Measurement.objects.values_list("station", flat=True))
]
variables = [
    Variable.objects.get(pk=v)
    for v in set(Measurement.objects.values_list("variable", flat=True))
]
start = Measurement.objects.earliest("time").time
end = Measurement.objects.latest("time").time
years = (end - start).days // 365


def random_date(start_: datetime, end_: datetime) -> datetime:
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end_ - start_
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start_ + timedelta(seconds=random_second)


queries = 500

execution = []
for _ in tqdm(range(queries), desc="Querying database"):
    start_date = random_date(start, end)
    end_date = random_date(start_date, end)
    station = random.choice(stations)
    variable = random.choice(variables)
    days = (end_date - start_date) / timedelta(days=1)

    tstart = time.time()
    records = Measurement.objects.filter(
        station=station, variable=variable, time__range=(start_date, end_date)
    )
    records_df = pd.DataFrame.from_records(records.values())
    tend = time.time()
    execution.append((len(records_df), days, tend - tstart))

os.makedirs("scratch", exist_ok=True)
pd.DataFrame(execution, columns=["records", "days", "time"]).to_csv(
    f"scratch/queries_{queries}_v{len(variables)}_s{len(stations)}_y{years}.csv"
)
