"""Scenario for creating synthetic data for benchmarking purposes.

This scenario creates synthetic data for a set of stations and variables for a single
year. It results in a database structure where the number of records is
spread evenly across the years and variables. As the default chunk time interval for
the TimescaleDB is 1 day, this scenario results in not that many chunks (365) and a
higher number of records per chunk that the previous scenario (~66000), althoguh the
total number of records is the same. Even per chunk, the number of records is still
pretty small, sugesting that the performance will not be that different.
"""

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

stations = list(Station.objects.all())[:23]
for s in stations:
    s.timezone = "UTC"
    s.save()
tz = zoneinfo.ZoneInfo(stations[0].timezone)

start = datetime(2023, 1, 1, tzinfo=tz)
end = datetime(2024, 1, 1, tzinfo=tz)
date_range = pd.date_range(start, end, freq="5min", inclusive="left")

progress = tqdm(
    itertools.product(stations, variables),
    total=len(stations) * len(variables),
    desc="Creating synthetic data",
)
nrecords = 0
execution = []
for station, variable in progress:
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
        for t in date_range
    ]

    [r.clean() for r in records]  # type: ignore
    Measurement.objects.bulk_create(records)
    tend = time.time()
    nrecords += len(records)
    execution.append((nrecords, tend - tstart))

os.makedirs("scratch", exist_ok=True)
pd.DataFrame(execution, columns=["nrecords", "time"]).to_csv(
    "scratch/execution_scenario2.csv"
)
