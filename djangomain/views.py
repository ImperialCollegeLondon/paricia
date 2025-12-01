from django.shortcuts import render
from django.views.generic.base import TemplateView
from guardian.shortcuts import get_objects_for_user

from station.models import Station


class HomePageView(TemplateView):
    """View for displaying the home page and map dash app."""

    def get(self, request, *args, **kwargs):
        from .dash_apps import stations_map  # noqa: F401

        stations = get_objects_for_user(request.user, "view_station", klass=Station)
        station_codes = list(stations.values_list("station_code", flat=True))
        context = {"django_context": {"stations_list": {"children": station_codes}}}
        return render(request, "home.html", context)
