from django import forms
from django.utils import timezone
from guardian.shortcuts import get_objects_for_user

from formatting.models import Format

from .models import ThingsboardImportMap


class ThingsboardDataRetrievalForm(forms.Form):
    """Form to select ThingsboardImportMap and date range for data retrieval."""

    thingsboard_map = forms.ModelChoiceField(
        queryset=ThingsboardImportMap.objects.none(),
        label="Select Device/Variable Mapping",
        help_text="Choose which ThingsBoard device and variable to fetch. If you dont see your desired mapping, create one using the button above.",  # noqa: E501
    )
    format = forms.ModelChoiceField(
        queryset=Format.objects.none(),
        label="Format",
    )
    start_date = forms.DateTimeField(
        label="Start Date & Time",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        initial=timezone.now() - timezone.timedelta(days=7),
    )

    end_date = forms.DateTimeField(
        label="End Date & Time",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        initial=timezone.now(),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["thingsboard_map"].queryset = get_objects_for_user(
                user,
                "importing.view_thingsboardimportmap",
                klass=ThingsboardImportMap,
            )
            self.fields["format"].queryset = get_objects_for_user(
                user,
                "formatting.view_format",
                klass=Format,
            ).order_by("name")
