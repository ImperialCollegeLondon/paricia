FROM python:3.11-bookworm as python

FROM python

COPY requirements-dev.txt .
RUN apt-get update && apt-get install -y --no-install-recommends libmagic1 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN mkdir log
RUN python manage.py collectstatic --no-input

EXPOSE 8000
