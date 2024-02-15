import os

from .settings import *  # noqa: F401, F403

DEBUG = False
ALLOWED_HOSTS = ["172.31.1431"]
SECRET_KEY = os.environ["SECRET_KEY"]
DATABASES["default"]["PASSWORD"] = os.environ["POSTGRESS_KEY"]  # noqa: F405
