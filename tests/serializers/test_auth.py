from django.test import TestCase
from myapp.serializers.auth import (
    AuthLogoutSerializer,
    AuthRefreshSerializer,
    AuthVerifySerializer,
)
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class AuthSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()

    def test_refresh_serializer_refresh_token_invalid(self):
        self.assertEqual(AuthRefreshSerializer.refresh, None)

        request = self.factory.post("/", {}, format="json")
        request.COOKIES = {"refresh_token": "foobar"}
        context = {"request": request}

        serializer = AuthRefreshSerializer(context=context)

        with self.assertRaises(TokenError):
            serializer.validate({})

    def test_refresh_serializer_no_token(self):
        request = self.factory.post("/", {}, format="json")
        request.COOKIES = {}
        context = {"request": request}

        serializer = AuthRefreshSerializer(context=context)

        with self.assertRaises(InvalidToken):
            serializer.validate({})

    def test_verify_serializer_token_invalid(self):
        self.assertEqual(AuthVerifySerializer.token, None)

        request = self.factory.post("/", {}, format="json")
        request.COOKIES = {"refresh_token": "foobar"}
        context = {"request": request}

        serializer = AuthVerifySerializer(context=context)

        with self.assertRaises(TokenError):
            serializer.validate({})

    def test_verify_serializer_no_token(self):
        request = self.factory.post("/", {}, format="json")
        request.COOKIES = {}
        context = {"request": request}

        serializer = AuthVerifySerializer(context=context)

        with self.assertRaises(InvalidToken):
            serializer.validate({})

    def test_blacklist_serializer_token_invalid(self):
        self.assertEqual(AuthLogoutSerializer.refresh, None)

        request = self.factory.post("/", {}, format="json")
        request.COOKIES = {"refresh_token": "foobar"}
        context = {"request": request}

        serializer = AuthLogoutSerializer(context=context)

        with self.assertRaises(TokenError):
            serializer.validate({})

    def test_blacklist_serializer_no_token(self):
        request = self.factory.post("/", {}, format="json")
        request.COOKIES = {}
        context = {"request": request}

        serializer = AuthLogoutSerializer(context=context)

        with self.assertRaises(InvalidToken):
            serializer.validate({})
