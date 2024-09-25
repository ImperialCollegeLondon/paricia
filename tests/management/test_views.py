from django.test import RequestFactory, TestCase
from guardian.shortcuts import assign_perm, get_user_model


class TestModelToDict(TestCase):
    def setUp(self) -> None:
        from sensor.models import Sensor, SensorType

        self.sensor_type = SensorType.objects.create(name="Temperature")
        self.sensor = Sensor.objects.create(
            code="Temperature Sensor",
            sensor_type=self.sensor_type,
            model="12345",
        )

    def test_model_to_dict(self):
        from management.views import model_to_dict

        data = model_to_dict(self.sensor)
        self.assertEqual(data["code"], "Temperature Sensor")
        self.assertEqual(data["sensor_type"], str(self.sensor_type))
        self.assertIsNone(data["sensor_brand"])
        self.assertEqual(data["model"], "12345")


class TestCustomTableView(TestCase):
    def setUp(self) -> None:
        from sensor.models import Sensor, SensorType

        User = get_user_model()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.sensor_type = SensorType.objects.create(name="Temperature")
        self.sensor = Sensor.objects.create(
            code="Temperature Sensor",
            sensor_type=self.sensor_type,
            model="12345",
        )
        assign_perm("view_sensor", self.user, self.sensor)
        self.sensor_private = Sensor.objects.create(
            code="Another Sensor",
            sensor_type=self.sensor_type,
            model="12345",
        )

    def test_get_queryset(self):
        from management.views import CustomTableView
        from sensor.models import Sensor

        request = self.factory.get("/fake-url")
        request.user = self.user
        view = CustomTableView()
        view.request = request
        view.model = Sensor
        queryset = view.get_queryset()
        self.assertIn(self.sensor, queryset)
        self.assertNotIn(self.sensor_private, queryset)

    def test_get_context_data(self):
        from management.views import CustomTableView
        from sensor.models import Sensor

        request = self.factory.get("/fake-url")
        request.user = self.user
        view = CustomTableView()
        view.request = request
        view.kwargs = {}
        view.model = Sensor
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        self.assertIn("table", context)
        self.assertEqual(context["title"], "Sensors")
        self.assertIsNone(context["refresh"])
        self.assertIsNone(context["new_url"])

    def test_properties(self):
        from management.views import CustomTableView
        from sensor.models import Sensor

        view = CustomTableView()
        view.model = Sensor
        self.assertEqual(view.app_label, "sensor")
        self.assertEqual(view.model_name, "sensor")
        self.assertEqual(view.permission_required, "sensor.view_sensor")
        self.assertEqual(view.list_url, "sensor:sensor_list")
        self.assertEqual(view.create_url, "sensor:sensor_create")
        self.assertEqual(view.title, "Sensors")
