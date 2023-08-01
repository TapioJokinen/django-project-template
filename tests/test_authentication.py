from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from myapp.authentication import CookieAuthentication
from rest_framework.test import APIRequestFactory


def mock_get_validated_token(self, token):
    return "foobar"


def mock_get_user(self, token):
    return "Bob"


def mock_get_raw_token(self, header):
    return "foobar"


def mock_get_raw_token_none(self, header):
    return None


class CookieAuthenticationTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_header_is_none(self):
        request = self.factory.post("/", {}, format="json")
        request.COOKIES[settings.SIMPLE_JWT["AUTH_COOKIE_KEY_ACCESS"]] = "foobar"

        with patch.object(CookieAuthentication, "get_validated_token", mock_get_validated_token):
            with patch.object(CookieAuthentication, "get_user", mock_get_user):
                result = CookieAuthentication().authenticate(request)

        self.assertEqual(result, ("Bob", "foobar"))

    def test_header_is_not_none(self):
        settings.DEBUG = True
        request = self.factory.post("/", {}, format="json", HTTP_AUTHORIZATION={"Authorization": "bar"})

        with patch.object(CookieAuthentication, "get_raw_token", mock_get_raw_token):
            with patch.object(CookieAuthentication, "get_validated_token", mock_get_validated_token):
                with patch.object(CookieAuthentication, "get_user", mock_get_user):
                    result = CookieAuthentication().authenticate(request)

        self.assertEqual(result, ("Bob", "foobar"))

    def test_header_is_not_none_and_raw_token_is_none(self):
        settings.DEBUG = True
        request = self.factory.post("/", {}, format="json", HTTP_AUTHORIZATION={"Authorization": "bar"})

        with patch.object(CookieAuthentication, "get_raw_token", mock_get_raw_token_none):
            with patch.object(CookieAuthentication, "get_validated_token", mock_get_validated_token):
                with patch.object(CookieAuthentication, "get_user", mock_get_user):
                    result = CookieAuthentication().authenticate(request)

        self.assertEqual(result, None)
