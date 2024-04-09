from django.shortcuts import render
from django.views.generic.base import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from guardian.shortcuts import get_objects_for_user
from rest_framework import permissions

from station.models import Station


class HomePageView(TemplateView):
    """
    View for displaying the home page and map dash app.
    """

    def get(self, request, *args, **kwargs):
        from .dash_apps.finished_apps import stations_map

        stations = get_objects_for_user(request.user, "view_station", klass=Station)
        station_codes = list(stations.values_list("station_code", flat=True))
        context = {"django_context": {"stations_list": {"children": station_codes}}}
        return render(request, "home.html", context)


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
