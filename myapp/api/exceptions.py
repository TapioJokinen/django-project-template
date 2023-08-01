import logging
import traceback

from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import set_rollback

from myapp.api.response import CamelCaseResponse
from myapp.common.exceptions import MyAppException

logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    """Returns the response that should be used for any given exception.

    By default we handle Django's built-in `Http404`, `PermissionDenied` and `ObjectDoesNotExist` exceptions.
    Also rest_framework's `APIException`'s are handled, since we use rest_framework for authentication.
    """

    if isinstance(exc, Http404):
        # Built-in Http404.
        exc = URLNotFound()
    elif isinstance(exc, PermissionDenied):
        # Built-in PermissionDenied.
        exc = Forbidden()
    elif isinstance(exc, MyAppAPIException):
        # Skip if our own exception is raised.
        pass
    elif isinstance(exc, ObjectDoesNotExist):
        # Handle Django model's DoesNotExist exception.
        exc = ObjectNotFound(message=str(exc))
    elif isinstance(exc, APIException):
        # Handle rest framework exceptions.
        exc = MyAppAPIException(message=exc.default_detail, code=exc.default_code, status_code=exc.status_code)
    elif isinstance(exc, MyAppException) or issubclass(type(exc), MyAppException):
        # Handle our own myappExceptions.
        exc = MyAppAPIException(
            message=exc.data["error"]["message"],
            code=exc.data["error"]["code"],
            status_code=exc.status_code if exc.status_code else status.HTTP_400_BAD_REQUEST,
        )
    else:
        # Handle everything else.
        exc = MyAppAPIException(message=str(exc), traceback=traceback.format_exc())

    set_rollback()
    logger.error(traceback.format_exc())

    return CamelCaseResponse(data=exc.data, status=exc.status_code)


class MyAppAPIException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "unhandled-exception"
    message = "No error message supplied."

    def __init__(self, message=None, code=None, status_code=None, **kwargs):
        error = {
            "code": code if code else self.code,
            "message": message if message else self.message,
            "extra": kwargs,
        }
        self.data = {"error": error}
        self.status_code = status_code if status_code else self.status_code


class URLNotFound(MyAppAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "url-not-found"
    message = "URL not found."


class Forbidden(MyAppAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    code = "forbidden-action"
    message = "You are forbidden to do this action."


class ObjectNotFound(MyAppAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not-found"
    message = "Not found."


class APINotImplemented(MyAppAPIException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    code = "not-implemented"
    message = "Not implemented."
