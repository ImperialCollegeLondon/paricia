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

    def test_measurement_consistency(self):
        from django.apps import apps

        from variable.models import Variable

        # Check that each variable relates to a class in measurement.models
        models = apps.get_app_config("measurement").get_models()
        model_names = [m._meta.model_name for m in models]

        for variable in Variable.objects.get_queryset():
            if variable.is_active:
                self.assertIn(variable.variable_code, model_names)
