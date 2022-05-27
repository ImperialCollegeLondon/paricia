from django.test import TestCase


class TestUnit(TestCase):
    fixtures = ["variable_unit.json"]

    def test_unit(self):
        from variable.models import Unit

        self.assertEqual(len(Unit.objects.get_queryset()), 22)

        unit = Unit.objects.get(unit_id=1)
        self.assertEqual(unit.name, "Kil\u00f3metros por Hora")
        self.assertEqual(unit.initials, "km/h")


class TestVariable(TestCase):
    fixtures = ["variable_unit.json", "variable_variable.json"]

    def test_variable(self):
        from variable.models import Variable

        self.assertEqual(len(Variable.objects.get_queryset()), 30)
        variable = Variable.objects.get(name="Temperatura ambiente")
        self.assertEqual(variable.variable_code, "tai")
        self.assertEqual(variable.unit.name, "Grados Cent\u00edgrados")
