from django.test import TestCase


class TestUnit(TestCase):
    fixtures = ["variable_unit.json"]

    def test_units(self):
        from variable.models import Unit

        self.assertEqual(len(Unit.objects.get_queryset()), 22)

        unit = Unit.objects.get(unit_id=1)
        self.assertEqual(unit.name, "Kil\u00f3metros por Hora")
        self.assertEqual(unit.initials, "km/h")
