import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from guardian.shortcuts import assign_perm
from rasterio.errors import RasterioIOError
from rasterio.io import MemoryFile
from rasterio.transform import from_origin

from djangomain.dash_apps import map_layers
from importing.models import MapLayerImport


class MapLayerUtilityTests(TestCase):
    def setUp(self):
        map_layers.load_payload.cache_clear()

        Group.objects.get_or_create(name="Standard")

        self._temp_media = tempfile.TemporaryDirectory()
        self._media_override = self.settings(MEDIA_ROOT=self._temp_media.name)
        self._media_override.enable()

        self.addCleanup(self._media_override.disable)
        self.addCleanup(self._temp_media.cleanup)

    def _create_user(self, username):
        return get_user_model().objects.create_user(
            username=username,
            password="testpass123",
        )

    def _build_geotiff_bytes(self, data):
        array = np.asarray(data, dtype="float32")
        with MemoryFile() as memfile:
            with memfile.open(
                driver="GTiff",
                height=array.shape[0],
                width=array.shape[1],
                count=1,
                dtype="float32",
                crs="EPSG:4326",
                transform=from_origin(-60.0, 10.0, 0.01, 0.01),
            ) as dataset:
                dataset.write(array, 1)
            return memfile.read()

    def _create_layer(
        self,
        *,
        owner,
        name,
        filename,
        visibility="private",
        data=None,
        raw_content=None,
        grant_view_to=None,
    ):
        if raw_content is None:
            if data is None:
                data = np.array([[1.0, 2.0], [3.0, 4.0]], dtype="float32")
            raw_content = self._build_geotiff_bytes(data)

        upload = SimpleUploadedFile(
            filename,
            raw_content,
            content_type="image/tiff",
        )

        layer = MapLayerImport.objects.create(
            owner=owner,
            visibility=visibility,
            name=name,
            file=upload,
        )

        if grant_view_to is not None:
            assign_perm("view_maplayerimport", grant_view_to, layer)

        return layer

    def test_available_map_layers_by_id_returns_empty_for_none_user(self):
        self.assertEqual(map_layers.available_map_layers_by_id(None), {})

    def test_available_map_layers_by_id_returns_empty_for_anonymous_user(self):
        self.assertEqual(map_layers.available_map_layers_by_id(AnonymousUser()), {})

    def test_available_map_layers_by_id_filters_by_permissions_only(self):
        owner = self._create_user("owner")
        viewer = self._create_user("viewer")

        visible_tif = self._create_layer(
            owner=owner,
            name="Visible GeoTIFF",
            filename="visible.tif",
            grant_view_to=viewer,
        )
        self._create_layer(
            owner=owner,
            name="Hidden GeoTIFF",
            filename="hidden.tif",
        )

        result = map_layers.available_map_layers_by_id(viewer)

        self.assertEqual(
            result,
            {
                f"maplayer-{visible_tif.pk}": {
                    "id": f"maplayer-{visible_tif.pk}",
                    "name": "Visible GeoTIFF",
                    "mtime": visible_tif.updated_at.timestamp(),
                    "file_name": visible_tif.file.name,
                    "file_type": "geotiff",
                },
            },
        )

    def test_bounds_to_lonlat_coordinates_returns_expected_order(self):
        result = map_layers._bounds_to_lonlat_coordinates(
            bounds=(-10.5, -5.25, 10.5, 5.25),
            src_crs=map_layers._TARGET_MAPBOX_COORDS_CRS,
        )

        self.assertEqual(
            result,
            [[-10.5, 5.25], [10.5, 5.25], [10.5, -5.25], [-10.5, -5.25]],
        )

    def test_bounds_to_lonlat_coordinates_transforms_non_wgs84_bounds(self):
        result = map_layers._bounds_to_lonlat_coordinates(
            bounds=(-1_000_000.0, -1_000_000.0, 1_000_000.0, 1_000_000.0),
            src_crs="EPSG:3857",
        )

        self.assertEqual(len(result), 4)
        self.assertLess(result[0][0], 0.0)
        self.assertGreater(result[1][0], 0.0)
        self.assertGreater(result[0][1], 0.0)
        self.assertLess(result[2][1], 0.0)

    def test_bounds_to_lonlat_coordinates_rejects_invalid_lon_lat(self):
        with self.assertRaisesRegex(ValueError, "valid lon/lat"):
            map_layers._bounds_to_lonlat_coordinates(
                bounds=(-181.0, -5.0, 10.0, 5.0),
                src_crs=map_layers._TARGET_MAPBOX_COORDS_CRS,
            )

    def test_build_geotiff_image_payload_happy_path(self):
        owner = self._create_user("payload-owner")
        layer = self._create_layer(
            owner=owner,
            name="Payload Layer",
            filename="payload.tif",
            data=np.array([[1.0, 2.0], [3.0, 4.0]], dtype="float32"),
        )

        payload = map_layers._build_geotiff_image_payload(layer.file.path)

        self.assertIn("image", payload)
        self.assertIn("coordinates", payload)
        self.assertTrue(payload["image"].startswith("data:image/png;base64,"))
        self.assertEqual(len(payload["coordinates"]), 4)

    def test_build_geotiff_image_payload_handles_flat_data(self):
        owner = self._create_user("flat-owner")
        layer = self._create_layer(
            owner=owner,
            name="Flat Layer",
            filename="flat.tif",
            data=np.full((2, 2), 5.0, dtype="float32"),
        )

        payload = map_layers._build_geotiff_image_payload(layer.file.path)

        self.assertTrue(payload["image"].startswith("data:image/png;base64,"))
        self.assertEqual(len(payload["coordinates"]), 4)

    def test_load_payload_uses_mtime_in_cache_key(self):
        owner = self._create_user("cache-owner")
        layer = self._create_layer(
            owner=owner,
            name="Cache Layer",
            filename="cache.tif",
        )

        mtime = layer.updated_at.timestamp()

        map_layers.load_payload.cache_clear()
        map_layers.load_payload(layer.file.name, mtime, "geotiff")
        first_info = map_layers.load_payload.cache_info()

        map_layers.load_payload(layer.file.name, mtime, "geotiff")
        second_info = map_layers.load_payload.cache_info()

        map_layers.load_payload(layer.file.name, mtime + 1, "geotiff")
        third_info = map_layers.load_payload.cache_info()

        self.assertEqual(second_info.hits, first_info.hits + 1)
        self.assertEqual(third_info.misses, second_info.misses + 1)

    def test_build_geotiff_image_payload_raises_rasterio_error_for_invalid_geotiff(
        self,
    ):
        broken_path = Path(self._temp_media.name) / "broken.tif"
        broken_path.write_bytes(b"this is not a geotiff")

        with self.assertRaises(RasterioIOError):
            map_layers._build_geotiff_image_payload(str(broken_path))

    def test_build_mapbox_layers_builds_entries_for_resolved_visible_layers(self):
        owner = self._create_user("map-owner")
        viewer = self._create_user("map-viewer")

        layer = self._create_layer(
            owner=owner,
            name="Visible map layer",
            filename="visible-map.tif",
            grant_view_to=viewer,
        )

        result = map_layers.build_mapbox_layers(
            layers_raw=[
                {
                    "id": f"maplayer-{layer.pk}",
                    "visible": True,
                }
            ],
            user=viewer,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "raster")
        self.assertEqual(result[0]["sourcetype"], "image")
        self.assertTrue(result[0]["source"].startswith("data:image/png;base64,"))
        self.assertEqual(result[0]["opacity"], 0.75)

    def test_build_mapbox_layers_skips_layers_on_payload_errors(self):
        owner = self._create_user("error-owner")
        viewer = self._create_user("error-viewer")

        broken = self._create_layer(
            owner=owner,
            name="Broken layer",
            filename="broken-layer.tif",
            raw_content=b"this is not a geotiff",
            grant_view_to=viewer,
        )

        result = map_layers.build_mapbox_layers(
            layers_raw=[
                {
                    "id": f"maplayer-{broken.pk}",
                    "visible": True,
                }
            ],
            user=viewer,
        )

        self.assertEqual(result, [])

    def test_available_map_layers_by_id_returns_empty_when_lookup_raises(self):
        user = self._create_user("lookup-exception-user")
        with patch(
            "djangomain.dash_apps.map_layers.get_objects_for_user",
            side_effect=Exception("db error"),
        ):
            result = map_layers.available_map_layers_by_id(user)
        self.assertEqual(result, {})

    def test_bounds_to_lonlat_coordinates_rejects_invalid_lat(self):
        with self.assertRaisesRegex(ValueError, "valid lon/lat"):
            map_layers._bounds_to_lonlat_coordinates(
                bounds=(-10.0, -91.0, 10.0, 5.0),
                src_crs=map_layers._TARGET_MAPBOX_COORDS_CRS,
            )

    def test_bounds_to_lonlat_coordinates_raises_on_transform_failure(self):
        with patch(
            "djangomain.dash_apps.map_layers.transform_bounds",
            side_effect=Exception("bad CRS"),
        ):
            with self.assertRaisesRegex(ValueError, "could not be transformed"):
                map_layers._bounds_to_lonlat_coordinates(
                    bounds=(-10.0, -5.0, 10.0, 5.0),
                    src_crs=map_layers._TARGET_MAPBOX_COORDS_CRS,
                )

    def test_build_mapbox_layers_skips_invisible_layers(self):
        owner = self._create_user("invisible-owner")
        viewer = self._create_user("invisible-viewer")

        layer = self._create_layer(
            owner=owner,
            name="Invisible layer",
            filename="invisible.tif",
            grant_view_to=viewer,
        )

        result = map_layers.build_mapbox_layers(
            layers_raw=[{"id": f"maplayer-{layer.pk}", "visible": False}],
            user=viewer,
        )

        self.assertEqual(result, [])

    def test_build_mapbox_layers_skips_unauthorised_layers(self):
        owner = self._create_user("unauth-owner")
        viewer = self._create_user("unauth-viewer")

        layer = self._create_layer(
            owner=owner,
            name="Unauthorised layer",
            filename="unauth.tif",
        )

        result = map_layers.build_mapbox_layers(
            layers_raw=[{"id": f"maplayer-{layer.pk}", "visible": True}],
            user=viewer,
        )

        self.assertEqual(result, [])

    def test_build_mapbox_layers_returns_empty_for_empty_input(self):
        user = self._create_user("empty-input-user")
        result = map_layers.build_mapbox_layers(layers_raw=[], user=user)
        self.assertEqual(result, [])

    def test_build_netcdf_image_payload(self):
        test_netcdf_file = Path(__file__).parent.parent / "test_data/test_layer.nc"
        content = test_netcdf_file.read_bytes()
        owner = self._create_user("owner")

        layer = MapLayerImport.objects.create(
            owner=owner,
            name="Test Layer",
            variable="value",
            file=SimpleUploadedFile(
                "layer.nc", content, content_type="application/netcdf"
            ),
        )

        payload = map_layers._build_netcdf_image_payload(layer.file.path, "value", 0)

        self.assertIsInstance(payload, dict)
        self.assertIn("image", payload)
        self.assertIn("coordinates", payload)
        self.assertTrue(payload["image"].startswith("data:image/png;base64,"))
        self.assertEqual(len(payload["coordinates"]), 4)

    def test_build_netcdf_image_payload_orders_retrieve_different_timestamps(self):
        test_netcdf_file = Path(__file__).parent.parent / "test_data/test_layer.nc"
        content = test_netcdf_file.read_bytes()
        owner = self._create_user("owner")

        layer = MapLayerImport.objects.create(
            owner=owner,
            name="Test Layer",
            variable="value",
            file=SimpleUploadedFile(
                "layer.nc", content, content_type="application/netcdf"
            ),
        )

        payload_0 = map_layers._build_netcdf_image_payload(layer.file.path, "value", 0)
        payload_1 = map_layers._build_netcdf_image_payload(layer.file.path, "value", 1)

        self.assertIsInstance(payload_0, dict)
        self.assertIsInstance(payload_1, dict)
        self.assertIn("image", payload_0)
        self.assertIn("image", payload_1)
        self.assertNotEqual(payload_0["image"], payload_1["image"])

    def test_load_payload_raises_on_unsupported_file_type(self):
        with self.assertRaisesRegex(ValueError, "Unsupported file type"):
            map_layers.load_payload("dummy.xyz", 0.0, "xyz", "value", 0)

    def test_load_payload_raises_on_netcdf_without_variable(self):
        with self.assertRaisesRegex(ValueError, "Variable must be specified"):
            map_layers.load_payload("dummy.nc", 0.0, "netcdf", None, 0)
