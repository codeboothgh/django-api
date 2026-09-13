from rest_framework_simplejwt import serializers as jwt_serializers

class TokenSerializer(jwt_serializers.TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["email"] = user.email

        return token

    # def validate(self, attrs):
    #     data = super().validate(attrs)

    #     refresh = self.get_token(self.user)

    #     data["refresh"] = str(refresh)
    #     data["refresh_expires"]