from django.views.generic.base import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class HomePageView(TemplateView):
    template_name = "home.html"


schema_view = get_schema_view(
    openapi.Info(
        title="Paricia API",
        default_version="v1",
        description="API for the Paricia project",
        terms_of_service="https://github.com/ImperialCollegeLondon/paricia",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
