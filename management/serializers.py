from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    # TODO this needs thinking about - how do we want to handle
    # serialization of users

    class Meta:
        model = User
        fields = ["id", "username"]
