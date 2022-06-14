from pathlib import Path

from django.test import TestCase


class TestPreformatMatrix(TestCase):
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

    def test_preformat_matrix(self):
        from formatting.models import Format
        from importing.functions import preformat_matrix

        file_format = Format.objects.get(format_id=45)
        data_file = str(
            Path(__file__).parent.parent / "test_data/iMHEA_HMT_01_HI_01_raw.csv"
        )

        df = preformat_matrix(data_file, file_format)
        self.assertEqual(df.shape, (263371, 5))
