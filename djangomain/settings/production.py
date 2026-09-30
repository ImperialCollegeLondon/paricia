import os

from azure.identity import DefaultAzureCredential

from .settings import *  # noqa: F403

DEBUG = False
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 15552000
SECRET_KEY = os.environ["SECRET_KEY"]
DATABASES["default"] = {  # noqa: F405
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ["POSTGRES_DB"],
    "USER": os.environ["POSTGRES_USER"],
    "PASSWORD": os.environ["POSTGRES_PASSWORD"],
    "HOST": os.environ["POSTGRES_HOST"],
    "PORT": os.environ.get("POSTGRES_PORT", "5432"),
}
INSTALLED_APPS += ["storages"]  # noqa: F405
AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]
AZURE_CONTAINER_MEDIA = os.environ["AZURE_CONTAINER_MEDIA"]
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "token_credential": DefaultAzureCredential(),
            "account_name": AZURE_ACCOUNT_NAME,
            "azure_container": AZURE_CONTAINER_MEDIA,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
MEDIA_URL = (
    f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER_MEDIA}/"
)
