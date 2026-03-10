from django import forms
from django.utils import timezone

from .models import ThingsboardImportMap


class ThingsboardDataRetrievalForm(forms.Form):
    """Form to select ThingsboardImportMap and date range for data retrieval."""

    thingsboard_map = forms.ModelChoiceField(
        queryset=ThingsboardImportMap.objects.all(),
        label="Select Device/Variable Mapping",
        help_text="Choose which ThingsBoard device and variable to fetch",
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
