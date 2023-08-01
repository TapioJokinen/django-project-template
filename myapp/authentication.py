from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_KEY_ACCESS"]) or None

        # We allow authentication with raw token in debug mode.
        if header and settings.DEBUG:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
