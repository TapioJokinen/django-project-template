from myapp.common.utils.converters import obj_to_camel_case
from rest_framework.response import Response


class CamelCaseResponse(Response):
    """Converts response body to camel case."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "data" not in kwargs:
            raise KeyError("Missing required 'data' keyword argument.")
        self.data = obj_to_camel_case(kwargs["data"])
