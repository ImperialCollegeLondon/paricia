from django.test import TestCase


class TestInitialData(TestCase):
    fixtures = [
        "station_country",
        "station_region",
        "station_ecosystem",
        "station_institution",
        "station_type",
        "station_place",
        "station_basin",
        "station_placebasin",
        "station_station",
    ]

    def test_country(self):
        from station.models import Country

        self.assertEqual(len(Country.objects.get_queryset()), 5)
        country = Country.objects.get(id=2)
        self.assertEqual(country.name, "Ecuador")

    def test_region(self):
        from station.models import Region

        self.assertEqual(len(Region.objects.get_queryset()), 11)
        region = Region.objects.get(id=11)
        self.assertEqual(region.name, "Cochabamba")
        self.assertEqual(region.country.name, "Bolivia")

    def test_ecosystem(self):
        from station.models import Ecosystem

        self.assertEqual(len(Ecosystem.objects.get_queryset()), 10)
        ecosystem = Ecosystem.objects.get(id=9)
        self.assertEqual(ecosystem.name, "Bosque tropical")

    def test_institution(self):
        from station.models import Institution

        self.assertEqual(len(Institution.objects.get_queryset()), 23)
        institution = Institution.objects.get(id=12)
        self.assertEqual(institution.name, "JUASVI")

    def test_station_type(self):
        from station.models import StationType

        self.assertEqual(len(StationType.objects.get_queryset()), 5)
        stationtype = StationType.objects.get(id=4)
        self.assertEqual(stationtype.name, "Aforo")

    def test_place(self):
        from station.models import Place

        self.assertEqual(len(Place.objects.get_queryset()), 18)
        place = Place.objects.get(id=5)
        self.assertEqual(place.name, "Alto Pita")

    def test_basin(self):
        from station.models import Basin

        self.assertEqual(len(Basin.objects.get_queryset()), 44)
        basin = Basin.objects.get(id=9)
        self.assertEqual(basin.name, "Huagrahuma")

    def test_placebasin(self):
        from station.models import PlaceBasin

        self.assertEqual(len(PlaceBasin.objects.get_queryset()), 41)
        placebasin = PlaceBasin.objects.get(id=9)
        self.assertEqual(placebasin.place.name, "Boyac\u00e1")
        self.assertEqual(placebasin.basin.name, "Ci\u00e9naga")

    def test_station(self):
        from station.models import Station

        self.assertEqual(len(Station.objects.get_queryset()), 104)
        station = Station.objects.get(station_id=11)
        self.assertEqual(station.station_code, "HMT_02_HI_01")
        self.assertEqual(station.country.name, "Per\u00fa")
