from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from django.test import TestCase
from rest_framework.exceptions import APIException

from myapp.api.exceptions import MyAppAPIException, exception_handler
from myapp.api.response import CamelCaseResponse
from myapp.common.exceptions import MyAppException, MyAppValidationError


class APIExceptionsTestCase(TestCase):
    def test_exception_handler(self):
        response_1 = exception_handler(Http404(), None)

        self.assertIsInstance(response_1, CamelCaseResponse)
        self.assertEqual(response_1.data["error"]["code"], "url-not-found")

        response_2 = exception_handler(PermissionDenied(), None)

        self.assertIsInstance(response_2, CamelCaseResponse)
        self.assertEqual(response_2.data["error"]["code"], "forbidden-action")

        response_3 = exception_handler(MyAppAPIException(code="foobar"), None)

        self.assertIsInstance(response_3, CamelCaseResponse)
        self.assertEqual(response_3.data["error"]["code"], "foobar")

        response_4 = exception_handler(ObjectDoesNotExist(), None)

        self.assertIsInstance(response_4, CamelCaseResponse)
        self.assertEqual(response_4.data["error"]["code"], "not-found")

        response_5 = exception_handler(APIException(), None)

        self.assertIsInstance(response_5, CamelCaseResponse)
        self.assertEqual(response_5.data["error"]["code"], "error")

        response_6 = exception_handler(MyAppException(code="hello-world", status_code=123), None)

        self.assertIsInstance(response_6, CamelCaseResponse)
        self.assertEqual(response_6.data["error"]["code"], "hello-world")
        self.assertEqual(response_6.status_code, 123)

        response_7 = exception_handler(MyAppValidationError(code="you"), None)

        self.assertIsInstance(response_7, CamelCaseResponse)
        self.assertEqual(response_7.data["error"]["code"], "you")

        response_8 = exception_handler(Exception(":)"), None)

        self.assertIsInstance(response_8, CamelCaseResponse)
        self.assertEqual(response_8.data["error"]["code"], "unhandled-exception")
