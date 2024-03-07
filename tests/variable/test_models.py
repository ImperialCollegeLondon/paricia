from django.test import TestCase


class TestInitialData(TestCase):
    fixtures = ["variable_unit", "variable_variable"]

    def test_units(self):
        from variable.models import Unit

        self.assertEqual(len(Unit.objects.get_queryset()), 22)

        unit = Unit.objects.get(unit_id=1)
        self.assertEqual(unit.name, "Kil\u00f3metros por Hora")
        self.assertEqual(unit.initials, "km/h")

    def test_variables(self):
        from variable.models import Variable

        self.assertEqual(len(Variable.objects.get_queryset()), 30)
        variable = Variable.objects.get(name="Temperatura ambiente")
        self.assertEqual(variable.variable_code, "airtemperature")
        self.assertEqual(variable.unit.name, "Grados Cent\u00edgrados")
