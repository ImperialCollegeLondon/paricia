import itertools
import os
import random
import sys
import time
import zoneinfo
from datetime import datetime
from decimal import Decimal

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

variables = list(Variable.objects.all())[:10]
years = list(range(2000, 2023))

station = Station.objects.first()
station.timezone = "UTC"
station.save()
tz = zoneinfo.ZoneInfo(station.timezone)

progress = tqdm(
    itertools.product(years, variables),
    total=len(years) * len(variables),
    desc="Creating synthetic data",
)
nrecords = 0
execution = []
for year, variable in progress:
    start = datetime(year, 1, 1, tzinfo=tz)
    end = datetime(year + 1, 1, 1, tzinfo=tz)
    minimum: int = random.randint(-5, 5)
    maximum: int = random.randint(20, 30)

    tstart = time.time()
    records = [
        Measurement(
            station=station,
            variable=variable,
            time=t,
            value=Decimal(random.randint(minimum, maximum)),
            minimum=Decimal(minimum),
            maximum=Decimal(maximum),
        )
        for t in pd.date_range(start, end, freq="5min", inclusive="left")
    ]

    [r.clean() for r in records]  # type: ignore
    Measurement.objects.bulk_create(records)
    tend = time.time()
    nrecords += len(records)
    execution.append((nrecords, tend - tstart))

os.makedirs("scratch", exist_ok=True)
pd.DataFrame(execution, columns=["nrecords", "time"]).to_csv(
    "scratch/execution_scenario1.csv"
)
