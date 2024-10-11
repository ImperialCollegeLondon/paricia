from django_filters import FilterSet, filters

from management.filters import FilterVisible
from variable.models import Variable

from .models import Classification, Date, Delimiter, Extension, Format, Time


class FormatFilter(FilterSet):
    extension = filters.ModelChoiceFilter(queryset=FilterVisible(Format, Extension))
    delimiter = filters.ModelChoiceFilter(queryset=FilterVisible(Format, Delimiter))
    date = filters.ModelChoiceFilter(queryset=FilterVisible(Format, Date))
    time = filters.ModelChoiceFilter(queryset=FilterVisible(Format, Time))

    class Meta:
        model = Format
        fields = ["visibility", "extension", "delimiter", "date", "time"]


class ClassificationFilter(FilterSet):
    format = filters.ModelChoiceFilter(queryset=FilterVisible(Classification, Format))
    variable = filters.ModelChoiceFilter(
        queryset=FilterVisible(Classification, Variable)
    )

    class Meta:
        model = Classification
        fields = ["visibility", "format", "variable"]
