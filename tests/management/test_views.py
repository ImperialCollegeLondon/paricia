from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm

from management.models import ThingsboardCredentials


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


class TestCustomDetailView(TestCase):
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

    def test_get_object(self):
        from management.views import CustomDetailView
        from sensor.models import Sensor

        request = self.factory.get("/fake-url")
        request.user = self.user
        view = CustomDetailView()
        view.request = request
        view.kwargs = {"pk": self.sensor.pk}
        view.model = Sensor
        obj = view.get_object()
        self.assertEqual(obj, self.sensor)

    def test_get_object_permission_denied(self):
        from management.views import CustomDetailView
        from sensor.models import Sensor

        request = self.factory.get("/fake-url")
        request.user = self.user
        view = CustomDetailView()
        view.request = request
        view.kwargs = {"pk": self.sensor_private.pk}
        view.model = Sensor
        with self.assertRaises(PermissionDenied):
            view.get_object()

    def test_get_context_data(self):
        from management.views import CustomDetailView
        from sensor.models import Sensor

        request = self.factory.get("/fake-url")
        request.user = self.user
        view = CustomDetailView()
        view.request = request
        view.kwargs = {"pk": self.sensor.pk}
        view.model = Sensor
        view.object = view.get_object()
        context = view.get_context_data()
        self.assertIn("form", context)
        self.assertEqual(context["title"], "Sensor")
        self.assertIsNone(context["delete_url"])
        self.assertIsNone(context["edit_url"])
        self.assertIsNone(context["list_url"])

    def test_properties(self):
        from management.views import CustomDetailView
        from sensor.models import Sensor

        view = CustomDetailView()
        view.model = Sensor
        self.assertEqual(view.app_label, "sensor")
        self.assertEqual(view.model_name, "sensor")
        self.assertEqual(view.permission_required, "sensor.view_sensor")
        self.assertEqual(view.list_url, "sensor:sensor_list")
        self.assertEqual(view.delete_url, "sensor:sensor_delete")
        self.assertEqual(view.edit_url, "sensor:sensor_edit")
        self.assertEqual(view.model_description, "Sensor")


class TestUserProfileView(TestCase):
    fixtures = ["management_user.json"]

    def setUp(self) -> None:
        self.user = get_user_model().objects.first()
        self.client.force_login(self.user)

    def test_get_profile_context_forms(self):
        response = self.client.get(reverse("user_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("profile_form", response.context)
        self.assertIn("thingsboard_form", response.context)

    def test_post_updates_profile_and_thingsboard(self):
        payload = {
            "first_name": "New",
            "last_name": "User",
            "email": "new@example.com",
            "thingsboard_username": "tb_user",
            "thingsboard_password": "tb_pass",
            "thingsboard_access_token": "tb_token",
        }
        response = self.client.post(reverse("user_profile"), data=payload)
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.email, "new@example.com")

        creds = ThingsboardCredentials.objects.get(user=self.user)
        self.assertEqual(creds.thingsboard_username, "tb_user")
        self.assertEqual(creds.thingsboard_password, "tb_pass")
        self.assertEqual(creds.thingsboard_access_token, "tb_token")
