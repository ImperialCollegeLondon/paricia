# -*- coding: utf-8 -*-
from django import forms

from station.models import Station
from variable.models import Variable


class DailyValidationForm(forms.Form):
    station = forms.ModelChoiceField(
        queryset=Station.objects.order_by("station_code"),
        empty_label="Station",
        initial=1,
    )
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by("variable_code"), empty_label="Variable"
    )
    start_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        label="Start date",
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        initial="2023-03-01",
    )
    end_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        label="End date",
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        initial="2023-03-31",
    )
    minimum = forms.DecimalField(required=False)
    maximum = forms.DecimalField(required=False)

    def __init__(self, *args, **kwargs):
        super(DailyValidationForm, self).__init__(*args, **kwargs)
        self.fields["station"].widget.attrs["placeholder"] = self.fields[
            "station"
        ].label


class DataReportForm(forms.Form):
    temporality = forms.ChoiceField(
        choices=[
            ("measurement", "Raw measurement"),
            ("validated", "Validated measurement"),
            ("hourly", "Hourly"),
            ("daily", "Daily"),
            ("monthly", "Monthly"),
        ],
        label="Temporality",
        initial=1,
    )
    station = forms.ModelChoiceField(
        queryset=Station.objects.order_by("station_code"),
        empty_label="Station",
        initial=1,
    )
    variable = forms.ModelChoiceField(
        queryset=Variable.objects.order_by("variable_code"), empty_label="Variable"
    )
    start_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        label="Start date",
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        initial="2023-03-01",
    )
    end_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        label="End date",
        required=True,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        initial="2023-03-31",
    )
    request_type = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(DataReportForm, self).__init__(*args, **kwargs)
        self.fields["station"].widget.attrs["placeholder"] = self.fields[
            "station"
        ].label