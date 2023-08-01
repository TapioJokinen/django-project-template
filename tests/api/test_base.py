import json
from unittest.mock import patch

from django.test import TestCase
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from myapp.api.base import BaseAPIView, BaseInputSerializer
from myapp.common.exceptions import MyAppValidationError


class TestInputSerializer(BaseInputSerializer):
    foo = serializers.CharField(required=True)


class BaseAPIViewTestCase(TestCase):
    def setUp(self) -> None:
        self.api_factory = APIRequestFactory()

    def test_load_json_body(self):
        request_1 = self.api_factory.post("/test", {"foo": "bar"}, format="json")
        request_2 = self.api_factory.post("/test", format="json")
        request_3 = self.api_factory.post("/test", "", content_type="application/json")

        try:
            BaseAPIView().load_json_body(request_1)
            BaseAPIView().load_json_body(request_2)
            BaseAPIView().load_json_body(request_3)
        except Exception:
            self.fail()

        with self.assertRaises(json.JSONDecodeError):
            with patch.object(json, "loads", side_effect=json.JSONDecodeError(msg="foo", doc="bar", pos=1)):
                BaseAPIView().load_json_body(request_1)

    def test_load_json_body_input_serializer(self):
        request_1 = self.api_factory.post("/test", {"baz": "bar", "foo": "bar"}, format="json")
        request_2 = self.api_factory.post("/test", {"foo": "bar"}, format="json")

        with self.assertRaises(MyAppValidationError):
            BaseAPIView().load_json_body(request_1, TestInputSerializer)

        try:
            BaseAPIView().load_json_body(request_2, TestInputSerializer)
            self.fail()
        except Exception:
            pass
