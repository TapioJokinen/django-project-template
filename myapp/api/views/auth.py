from django.conf import settings
from django.contrib.auth import get_user_model
from myapp.common.utils.converters import obj_to_camel_case
from myapp.serializers.auth import (
    AuthLogoutSerializer,
    AuthRefreshSerializer,
    AuthVerifySerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


def set_response_cookie(response, token_type):
    key = None
    if token_type == "refresh":
        key = settings.SIMPLE_JWT["AUTH_COOKIE_KEY_REFRESH"]
        max_age = settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH_MAX_AGE"]
    if token_type == "access":
        key = settings.SIMPLE_JWT["AUTH_COOKIE_KEY_ACCESS"]
        max_age = settings.SIMPLE_JWT["AUTH_COOKIE_ACCESS_MAX_AGE"]
    value = response.data.pop(token_type, "") if response.data else ""
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        domain=settings.SIMPLE_JWT["AUTH_COOKIE_DOMAIN"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAME_SITE"],
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
    )


class AuthLoginView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):  # pragma: no cover
            set_response_cookie(response, "refresh")

        if response.data.get("access"):  # pragma: no cover
            set_response_cookie(response, "access")

        User = get_user_model()

        response = super().finalize_response(request, response, *args, **kwargs)

        if response.status_code == 200:  # pragma: no cover
            user = User.objects.get(email=request.data["email"])
            response.data["user"] = user.to_dict()
            response.data = obj_to_camel_case(response.data)

        return response


class AuthRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):  # pragma: no cover
            set_response_cookie(response, "refresh")

        if response.data.get("access"):  # pragma: no cover
            set_response_cookie(response, "access")
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = AuthRefreshSerializer


class AuthVerifyView(TokenVerifyView):
    serializer_class = AuthVerifySerializer


class AuthLogoutView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=False)
        except (InvalidToken, AttributeError):  # pylint: disable=broad-except
            # Exception might be raised if user manually deleted refresh_token cookie.
            # We still want to return response so cookies get cleaned from the browser.
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

    def finalize_response(self, request, response, *args, **kwargs):
        set_response_cookie(response, "refresh")
        set_response_cookie(response, "access")
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = AuthLogoutSerializer
