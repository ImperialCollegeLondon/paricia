from django.test import TestCase


class TestInitialData(TestCase):
    fixtures = [
        "variable_unit",
        "variable_variable",
        "formatting_delimiter",
        "formatting_extension",
        "formatting_date",
        "formatting_time",
        "formatting_format",
        "formatting_classification",
    ]

    def test_delimiter(self):
        from formatting.models import Delimiter

        self.assertEqual(len(Delimiter.objects.get_queryset()), 9)
        delim = Delimiter.objects.get(name="Coma")
        self.assertEqual(delim.character, ",")

    def test_extension(self):
        from formatting.models import Extension

        self.assertEqual(len(Extension.objects.get_queryset()), 5)
        extension = Extension.objects.get(extension_id=2)
        self.assertEqual(extension.value, "csv")

    def test_date(self):
        from formatting.models import Date

        self.assertEqual(len(Date.objects.get_queryset()), 12)
        date = Date.objects.get(date_id=5)
        self.assertEqual(date.date_format, "MM/DD/YYYY")
        self.assertEqual(date.code, "%m/%d/%Y")

    def test_time(self):
        from formatting.models import Time

        self.assertEqual(len(Time.objects.get_queryset()), 3)
        time = Time.objects.get(time_id=3)
        self.assertEqual(time.time_format, "HH:MM 24H")
        self.assertEqual(time.code, "%H:%M")

    def test_format(self):
        from formatting.models import Format

        self.assertEqual(len(Format.objects.get_queryset()), 39)
        form = Format.objects.get(format_id=21)
        self.assertEqual(form.first_row, 3)
        self.assertEqual(form.extension.value, "csv")
        self.assertEqual(form.delimiter.name, "Coma")
        self.assertEqual(form.date.date_format, "MM/DD/YY")

    def test_classification(self):
        from formatting.models import Classification

        self.assertEqual(len(Classification.objects.get_queryset()), 123)
        classification = Classification.objects.get(cls_id=101)
        self.assertEqual(classification.format.name, "Vaisala (relleno)")
        self.assertEqual(classification.format.delimiter.name, "Punto y Com")
        self.assertEqual(classification.variable.name, "Velocidad de viento")
