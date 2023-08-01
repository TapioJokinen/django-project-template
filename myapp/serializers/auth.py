from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import (
    TokenBlacklistSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)


class AuthRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        raise InvalidToken("No valid token found in cookie 'refresh_token'")


class AuthVerifySerializer(TokenVerifySerializer):
    token = None

    def validate(self, attrs):
        attrs["token"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["token"]:
            return super().validate(attrs)
        raise InvalidToken("No valid token found in cookie 'refresh_token'")


class AuthLogoutSerializer(TokenBlacklistSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        raise InvalidToken("No valid token found in cookie 'refresh_token'")
