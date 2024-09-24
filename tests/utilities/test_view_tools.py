from django.test import TestCase


class ModelToDictTests(TestCase):
    def setUp(self):
        from sensor.models import Sensor, SensorType

        self.sensor_type = SensorType.objects.create(name="Temperature")
        self.sensor = Sensor.objects.create(
            code="Sensor1",
            sensor_type=self.sensor_type,
            model="12345",
        )

    def test_model_to_dict(self):
        from utilities.view_tools import model_to_dict

        sensor_dict = model_to_dict(self.sensor)
        self.assertEqual(sensor_dict["code"], "Sensor1")
        self.assertEqual(sensor_dict["sensor_type"], str(self.sensor_type))
        self.assertIsNone(sensor_dict["sensor_brand"])
        self.assertEqual(sensor_dict["model"], "12345")
