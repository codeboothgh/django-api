from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group


class TokenSerializer(jwt_serializers.TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token

class UserRequestSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "groups"
        ]
        model = User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["id", "name"]
        read_only_fields = ["id"]
        model = Group


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        fields = [
            "email",
            "first_name",
            "last_name",
            "groups",
            "date_joined",
            "last_login"
        ]
        model = User