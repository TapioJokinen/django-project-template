from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from myapp.api.views.auth import AuthLoginView, AuthLogoutView, AuthRefreshView
from rest_framework import status
from rest_framework.test import APIRequestFactory


class AuthViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.AUTH_COOKIE_REFRESH_MAX_AGE = settings.SIMPLE_JWT["AUTH_COOKIE_REFRESH_MAX_AGE"]
        cls.AUTH_COOKIE_ACCESS_MAX_AGE = settings.SIMPLE_JWT["AUTH_COOKIE_ACCESS_MAX_AGE"]
        cls.AUTH_COOKIE_SAME_SITE = settings.SIMPLE_JWT["AUTH_COOKIE_SAME_SITE"]
        cls.AUTH_COOKIE_HTTP_ONLY = settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"]

        cls.User = get_user_model()
        cls.EMAIL = "foo@bar.com"
        cls.PASSWORD = "foobarz"
        cls.FIRST_NAME = "foo"
        cls.LAST_NAME = "bar"

        cls.user = cls.User.objects.create_superuser(
            email=cls.EMAIL,
            password=cls.PASSWORD,
            first_name=cls.FIRST_NAME,
            last_name=cls.LAST_NAME,
        )

    def setUp(self) -> None:
        self.api_factory = APIRequestFactory()

    def _login_response(self):
        path = reverse("auth_login")

        request = self.api_factory.post(
            path,
            {"email": self.EMAIL, "password": self.PASSWORD},
            headers={"Accept": "application/json; version=1.0"},
            format="json",
        )

        view = AuthLoginView.as_view()

        return view(request)

    def _login_refresh_response(self, login_response):
        path = reverse("auth_refresh")

        request = self.api_factory.post(path, {}, headers={"Accept": "application/json; version=1.0"}, format="json")

        request.COOKIES["refresh_token"] = login_response.cookies["refresh_token"].value

        view = AuthRefreshView.as_view()

        return view(request)

    def test_auth_login(self):
        response = self._login_response()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.cookies["refresh_token"]["max-age"],
            self.AUTH_COOKIE_REFRESH_MAX_AGE,
        )
        self.assertEqual(response.cookies["access_token"]["max-age"], self.AUTH_COOKIE_ACCESS_MAX_AGE)
        self.assertEqual(response.cookies["refresh_token"]["samesite"], self.AUTH_COOKIE_SAME_SITE)
        self.assertEqual(response.cookies["refresh_token"]["httponly"], self.AUTH_COOKIE_HTTP_ONLY)

        correct_keys = [
            "id",
            "dateAdded",
            "dateUpdated",
            "email",
            "firstName",
            "lastName",
            "isActive",
            "lastActive",
            "groups",
            "userPermissions",
        ]

        to_be_removed = []
        for key in response.data["user"].keys():
            if key in correct_keys:
                to_be_removed.append(key)

        for key in to_be_removed:
            response.data["user"].pop(key)

        self.assertEqual(len(response.data["user"].keys()), 0)

    def test_auth_refresh(self):
        login_response = self._login_response()

        refresh_response = self._login_refresh_response(login_response)

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            refresh_response.cookies["access_token"]["max-age"],
            self.AUTH_COOKIE_ACCESS_MAX_AGE,
        )

    def test_auth_logout_cookie_exists(self):
        login_response = self._login_response()

        path = reverse("auth_logout")

        request = self.api_factory.post(path, {}, headers={"Accept": "application/json; version=1.0"}, format="json")

        request.COOKIES["refresh_token"] = login_response.cookies["refresh_token"].value

        view = AuthLogoutView.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        refresh_response = self._login_refresh_response(login_response)

        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_logout_cookie_does_not_exist(self):
        path = reverse("auth_logout")

        request = self.api_factory.post(path, {}, headers={"Accept": "application/json; version=1.0"}, format="json")

        view = AuthLogoutView.as_view()

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.cookies["refresh_token"].value, "")
        self.assertEqual(response.cookies["access_token"].value, "")
