from django.test import TestCase


class TestInitialData(TestCase):
    fixtures = [
        "sensor_type",
        "sensor_brand",
    ]

    def test_sensor_type(self):
        from sensor.models import SensorType

        self.assertEqual(len(SensorType.objects.get_queryset()), 10)
        sensor_type = SensorType.objects.get(type_id=7)
        self.assertEqual(sensor_type.name, "Radiaci\u00f3n Solar")

    def test_sensor_brand(self):
        from sensor.models import SensorBrand

        self.assertEqual(len(SensorBrand.objects.get_queryset()), 16)
        sensor_brand = SensorBrand.objects.get(brand_id=3)
        self.assertEqual(sensor_brand.name, "Davis")
