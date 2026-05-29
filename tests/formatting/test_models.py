from django.core.exceptions import ValidationError
from django.test import TestCase


class TestInitialData(TestCase):
    fixtures = [
        "management_user",
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

        self.assertEqual(len(Format.objects.get_queryset()), 3)
        form = Format.objects.get(format_id=45)
        self.assertEqual(form.first_row, 1)
        self.assertEqual(form.extension.value, "csv")
        self.assertEqual(form.delimiter.name, "Coma")
        self.assertEqual(form.date.date_format, "DD/MM/YYYY")

    def test_classification(self):
        from formatting.models import Classification

        self.assertEqual(len(Classification.objects.get_queryset()), 3)
        classification = Classification.objects.get(cls_id=176)
        self.assertEqual(classification.format.name, "iMHEA nivel y flujo periódico")
        self.assertEqual(classification.format.delimiter.name, "Coma")
        self.assertEqual(classification.variable.name, "Caudal")


class TestClassification(TestCase):
    fixtures = [
        "management_user",
        "variable_unit",
        "variable_variable",
        "formatting_delimiter",
        "formatting_extension",
        "formatting_date",
        "formatting_time",
        "formatting_format",
        "formatting_classification",
    ]

    def setUp(self):
        from formatting.models import Format
        from variable.models import Variable

        self.variable = Variable.objects.get(variable_id=1)
        self.format = Format.objects.get(format_id=46)

    def test_clean_resolution(self):
        """Test the clean method checks the resolution is set."""
        from formatting.models import Classification

        classification = Classification.objects.create(
            owner=self.variable.owner,
            visibility="Public",
            variable=self.variable,
            accumulate=3,
        )
        with self.assertRaises(ValidationError) as ctx:
            classification.clean()
        self.assertEqual(
            {"resolution": ["The resolution must be set if the data is accumulated."]},
            ctx.exception.message_dict,
        )

        classification.resolution = 2.0
        classification.clean()

    def test_clean_different_columns(self):
        """Test the clean method checks that columns provided are different."""
        from formatting.models import Classification

        classification = Classification.objects.create(
            owner=self.variable.owner,
            visibility="Public",
            format=self.format,
            variable=self.variable,
            value=0,
            maximum=1,
            minimum=1,
        )
        with self.assertRaises(ValidationError) as ctx:
            classification.clean()
        self.assertEqual(
            {
                "maximum": ["The columns must be different."],
                "minimum": ["The columns must be different."],
            },
            ctx.exception.message_dict,
        )

        classification.minimum = 2
        classification.clean()

    def test_clean_value(self):
        """Test the clean method checks value is provided if there is a Format."""
        from formatting.models import Classification

        classification = Classification.objects.create(
            owner=self.variable.owner,
            visibility="Public",
            format=self.format,
            variable=self.variable,
        )
        with self.assertRaises(ValidationError) as ctx:
            classification.clean()
        self.assertEqual(
            {
                "value": ["A value column must be specified if a format is provided."],
            },
            ctx.exception.message_dict,
        )

        classification.value = 0
        classification.clean()

        # No format provided (only for Thingsboard)
        classification = Classification.objects.create(
            owner=self.variable.owner,
            visibility="Public",
            variable=self.variable,
        )
        classification.clean()
