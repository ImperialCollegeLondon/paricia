from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import numpy as np
from django.test import TestCase

from djangomain.dash_apps import geotiff_layers


class _BadPathFile:
    @property
    def path(self):
        raise ValueError("invalid path")


class GeoTiffLayerUtilityTests(TestCase):
    def setUp(self):
        geotiff_layers.load_geotiff_payload.cache_clear()

    @patch("djangomain.dash_apps.geotiff_layers.get_objects_for_user")
    def test_available_map_layers_by_id_returns_empty_for_none_user(self, mock_get):
        result = geotiff_layers.available_map_layers_by_id(None)

        self.assertEqual(result, {})
        mock_get.assert_not_called()

    @patch("djangomain.dash_apps.geotiff_layers.get_objects_for_user")
    def test_available_map_layers_by_id_handles_permission_lookup_errors(
        self, mock_get
    ):
        mock_get.side_effect = Exception("boom")

        result = geotiff_layers.available_map_layers_by_id(user=object())

        self.assertEqual(result, {})

    @patch("djangomain.dash_apps.geotiff_layers.get_objects_for_user")
    def test_available_map_layers_by_id_filters_invalid_layers(self, mock_get):
        valid_layer = SimpleNamespace(
            pk=7,
            name="Visible GeoTIFF",
            file=SimpleNamespace(path="/tmp/visible.tif"),
        )
        invalid_extension = SimpleNamespace(
            pk=8,
            name="Not a GeoTIFF",
            file=SimpleNamespace(path="/tmp/not-geotiff.png"),
        )
        bad_path = SimpleNamespace(
            pk=9,
            name="Bad Path",
            file=_BadPathFile(),
        )

        queryset = MagicMock()
        queryset.order_by.return_value = [invalid_extension, bad_path, valid_layer]
        mock_get.return_value = queryset

        user = object()
        result = geotiff_layers.available_map_layers_by_id(user)

        self.assertEqual(
            result,
            {
                "maplayer-7": {
                    "id": "maplayer-7",
                    "name": "Visible GeoTIFF",
                    "file_path": "/tmp/visible.tif",
                }
            },
        )
        mock_get.assert_called_once_with(
            user,
            "importing.view_maplayerimport",
            klass=geotiff_layers.MapLayerImport,
        )

    def test_normalise_spatial_layers_filters_duplicates_and_sorts(self):
        layers_raw = [
            {
                "id": "layer-a",
                "source_kind": "geotiff",
                "name": "A",
                "visible": True,
                "order": 3,
            },
            {
                "id": "layer-a",
                "source_kind": "geotiff",
                "name": "duplicate",
                "visible": True,
                "order": 1,
            },
            {
                "id": "layer-b",
                "source_kind": "wms",
                "name": "Not GeoTIFF",
                "visible": True,
                "order": 1,
            },
            {
                "id": "layer-c",
                "source_kind": "GeoTiff",
                "name": "C",
                "order": 1.9,
            },
            {
                "id": "layer-d",
                "source_kind": "geotiff",
                "name": "",
                "order": "bad-value",
            },
        ]

        result = geotiff_layers.normalise_spatial_layers(layers_raw)

        self.assertEqual(
            [layer["id"] for layer in result], ["layer-c", "layer-a", "layer-d"]
        )
        self.assertEqual(result[0]["order"], 1)
        self.assertEqual(result[1]["order"], 3)
        self.assertEqual(result[2]["order"], 5)
        self.assertEqual(result[2]["name"], "Layer 5")
        self.assertTrue(result[2]["visible"])

    def test_extract_coordinates_requires_georeferencing(self):
        dataset = SimpleNamespace(
            crs=None,
            transform=SimpleNamespace(is_identity=True),
            bounds=(0.0, 0.0, 1.0, 1.0),
        )

        with self.assertRaisesRegex(ValueError, "missing georeferencing"):
            geotiff_layers._extract_geotiff_coordinates_from_dataset(
                dataset,
                transform_bounds_fn=lambda *args, **kwargs: (0.0, 0.0, 1.0, 1.0),
            )

    def test_extract_coordinates_transforms_to_wgs84(self):
        dataset = SimpleNamespace(
            crs="EPSG:3857",
            transform=SimpleNamespace(is_identity=False),
            bounds=(100.0, 200.0, 300.0, 400.0),
        )

        transformed = (-10.5, -5.25, 10.5, 5.25)
        result = geotiff_layers._extract_geotiff_coordinates_from_dataset(
            dataset,
            transform_bounds_fn=lambda *args, **kwargs: transformed,
        )

        self.assertEqual(
            result,
            [[-10.5, 5.25], [10.5, 5.25], [10.5, -5.25], [-10.5, -5.25]],
        )

    def test_extract_coordinates_rejects_out_of_bounds_lon_lat(self):
        dataset = SimpleNamespace(
            crs=None,
            transform=SimpleNamespace(is_identity=False),
            bounds=(-200.0, -100.0, 200.0, 100.0),
        )

        with self.assertRaisesRegex(ValueError, "valid lon/lat"):
            geotiff_layers._extract_geotiff_coordinates_from_dataset(
                dataset,
                transform_bounds_fn=lambda *args, **kwargs: (-1.0, -1.0, 1.0, 1.0),
            )

    def test_array_to_png_data_uri_handles_single_band(self):
        raster = np.array([[1.0, np.nan], [2.0, 3.0]])

        result = geotiff_layers._array_to_png_data_uri(raster)

        self.assertTrue(result.startswith("data:image/png;base64,"))
        encoded = result.split(",", maxsplit=1)[1]
        self.assertGreater(len(encoded), 0)

    def test_array_to_png_data_uri_handles_channel_first_rgb(self):
        raster = np.array(
            [
                [[10.0, 20.0], [30.0, 40.0]],
                [[20.0, 30.0], [40.0, 50.0]],
                [[30.0, 40.0], [50.0, 60.0]],
            ]
        )

        result = geotiff_layers._array_to_png_data_uri(raster)

        self.assertTrue(result.startswith("data:image/png;base64,"))

    def test_array_to_png_data_uri_rejects_invalid_dimensions(self):
        with self.assertRaisesRegex(ValueError, "displayable PNG"):
            geotiff_layers._array_to_png_data_uri(np.array([1.0, 2.0, 3.0]))

    @patch("djangomain.dash_apps.geotiff_layers._array_to_png_data_uri")
    @patch(
        "djangomain.dash_apps.geotiff_layers._extract_geotiff_coordinates_from_dataset"
    )
    @patch("djangomain.dash_apps.geotiff_layers.rasterio.open")
    def test_load_geotiff_payload_returns_image_and_coordinates(
        self,
        mock_open,
        mock_extract_coordinates,
        mock_array_to_png,
    ):
        dataset = MagicMock()
        dataset.count = 1
        dataset.read.return_value = np.ma.array(
            [[[1.0, 2.0], [3.0, np.nan]]],
            mask=[[[False, False], [False, True]]],
        )

        open_ctx = MagicMock()
        open_ctx.__enter__.return_value = dataset
        open_ctx.__exit__.return_value = False
        mock_open.return_value = open_ctx

        mock_extract_coordinates.return_value = [
            [0.0, 1.0],
            [1.0, 1.0],
            [1.0, 0.0],
            [0.0, 0.0],
        ]
        mock_array_to_png.return_value = "data:image/png;base64,abc"

        payload = geotiff_layers.load_geotiff_payload("/tmp/layer.tif", 100.0)

        self.assertEqual(
            payload,
            {
                "image": "data:image/png;base64,abc",
                "coordinates": [[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]],
            },
        )
        dataset.read.assert_called_once_with(masked=True)
        converted_raster = mock_array_to_png.call_args[0][0]
        self.assertEqual(converted_raster.shape, (2, 2))

    @patch("djangomain.dash_apps.geotiff_layers.rasterio.open")
    def test_load_geotiff_payload_raises_for_empty_raster(self, mock_open):
        dataset = MagicMock()
        dataset.count = 0

        open_ctx = MagicMock()
        open_ctx.__enter__.return_value = dataset
        open_ctx.__exit__.return_value = False
        mock_open.return_value = open_ctx

        with self.assertRaisesRegex(ValueError, "no bands"):
            geotiff_layers.load_geotiff_payload("/tmp/layer.tif", 100.0)

    @patch("djangomain.dash_apps.geotiff_layers.rasterio.open")
    def test_load_geotiff_payload_wraps_unexpected_errors(self, mock_open):
        mock_open.side_effect = RuntimeError("unexpected")

        with self.assertRaisesRegex(ValueError, "valid georeferenced GeoTIFF"):
            geotiff_layers.load_geotiff_payload("/tmp/layer.tif", 100.0)

    @patch("djangomain.dash_apps.geotiff_layers.load_geotiff_payload")
    @patch("djangomain.dash_apps.geotiff_layers.os.path.getmtime")
    @patch("djangomain.dash_apps.geotiff_layers.available_map_layers_by_id")
    @patch("djangomain.dash_apps.geotiff_layers.normalise_spatial_layers")
    def test_build_mapbox_layers_builds_entries_for_resolved_visible_layers(
        self,
        mock_normalise,
        mock_available,
        mock_getmtime,
        mock_load_payload,
    ):
        mock_normalise.return_value = [
            {"id": "maplayer-1", "visible": True},
            {"id": "maplayer-2", "visible": True},
            {"id": "maplayer-3", "visible": False},
        ]
        mock_available.return_value = {
            "maplayer-1": {
                "file_path": "/tmp/a.tif",
                "name": "A",
                "id": "maplayer-1",
            }
        }
        mock_getmtime.return_value = 123.0
        mock_load_payload.return_value = {
            "image": "data:image/png;base64,abc",
            "coordinates": [[0.0, 1.0], [1.0, 1.0], [1.0, 0.0], [0.0, 0.0]],
        }

        result = geotiff_layers.build_mapbox_layers(
            layers_raw=[{"id": "ignored"}], user=object()
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "raster")
        self.assertEqual(result[0]["source"], "data:image/png;base64,abc")
        self.assertEqual(result[0]["opacity"], 0.75)

    @patch("djangomain.dash_apps.geotiff_layers.load_geotiff_payload")
    @patch("djangomain.dash_apps.geotiff_layers.os.path.getmtime")
    @patch("djangomain.dash_apps.geotiff_layers.available_map_layers_by_id")
    @patch("djangomain.dash_apps.geotiff_layers.normalise_spatial_layers")
    def test_build_mapbox_layers_skips_layers_on_payload_errors(
        self,
        mock_normalise,
        mock_available,
        mock_getmtime,
        mock_load_payload,
    ):
        mock_normalise.return_value = [{"id": "maplayer-1", "visible": True}]
        mock_available.return_value = {
            "maplayer-1": {
                "file_path": "/tmp/a.tif",
                "name": "A",
                "id": "maplayer-1",
            }
        }
        mock_getmtime.return_value = 123.0
        mock_load_payload.side_effect = ValueError("bad geotiff")

        result = geotiff_layers.build_mapbox_layers(layers_raw=[], user=object())

        self.assertEqual(result, [])
