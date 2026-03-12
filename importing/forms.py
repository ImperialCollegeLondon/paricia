from django import forms
from django.utils import timezone

from .models import DataImport, ThingsboardImportMap


class ThingsboardDataRetrievalForm(forms.Form):
    """Form to select ThingsboardImportMap and date range for data retrieval."""

    thingsboard_map = forms.ModelChoiceField(
        queryset=ThingsboardImportMap.objects.all(),
        label="Select Device/Variable Mapping",
        help_text="Choose which ThingsBoard device and variable to fetch",
    )
    format = DataImport._meta.get_field("format").formfield(
        queryset=DataImport._meta.get_field("format")
        .remote_field.model.objects.all()
        .order_by("name")
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
