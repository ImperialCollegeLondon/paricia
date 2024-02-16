import os

from .settings import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = ["172.31.14.31"]
SECRET_KEY = os.environ["SECRET_KEY"]
DATABASES["default"]["PASSWORD"] = os.environ["POSTGRES_PASSWORD"]  # noqa: F405
