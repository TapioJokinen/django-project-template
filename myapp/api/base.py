import json

from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from myapp.api.exceptions import APINotImplemented
from myapp.common.exceptions import MyAppValidationError
from myapp.common.utils.converters import to_snake_case


class BaseAPIView(APIView):
    """Base class for all endpoints with default permissions."""

    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        raise APINotImplemented  # pragma: no cover

    def post(self, request):
        raise APINotImplemented  # pragma: no cover

    def put(self, request):
        raise APINotImplemented  # pragma: no cover

    def patch(self, request):
        raise APINotImplemented  # pragma: no cover

    def delete(self, request):
        raise APINotImplemented  # pragma: no cover

    def load_json_body(self, request: Request, input_serializer_cls: serializers.Serializer = None):
        """
        Attempts to load the request body when it's JSON.

        The end result is ``request.json_body`` having a value. When it can't
        load the body as JSON, for any reason, ``request.json_body`` is None.

        The request flow is unaffected and no exceptions are ever raised.
        """

        request.json_body = None

        if not request.META.get("CONTENT_TYPE", "").startswith("application/json"):
            return

        if not len(request.body):
            return

        try:
            request.json_body = json.loads(request.body)
            request.dict_body = {to_snake_case(k): v for k, v in request.json_body.items()}

            if input_serializer_cls:
                input_serializer_cls(data=request.dict_body).is_valid(raise_exception=True)
        except json.JSONDecodeError:
            raise


class BaseInputSerializer(serializers.Serializer):
    def validate(self, data):
        """Raise an error if unknown field is given in request body."""

        if hasattr(self, "initial_data"):  # pragma: no cover
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
            if unknown_keys:
                raise MyAppValidationError(f"Got unknown fields: {unknown_keys}.")

        return data
