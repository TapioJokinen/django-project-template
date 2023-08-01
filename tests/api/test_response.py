from django.test import TestCase
from myapp.api.response import CamelCaseResponse


class APIResponseTests(TestCase):
    def test_camel_case_response(self):
        with self.assertRaises(KeyError):
            CamelCaseResponse()
