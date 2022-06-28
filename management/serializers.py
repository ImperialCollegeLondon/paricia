from rest_framework import serializers

from importing.models import DataImportTemp

from .models import User


class UserSerializer(serializers.ModelSerializer):
    data_imports_temp = serializers.PrimaryKeyRelatedField(
        many=True, queryset=DataImportTemp.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "data_imports_temp"]
