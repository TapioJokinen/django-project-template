class MyAppException(Exception):
    status_code = None
    code = "unhandled_exception"
    message = "No error message supplied."

    def __init__(self, message=None, code=None, status_code=None, **kwargs):
        error = {
            "code": code if code else self.code,
            "message": message if message else self.message,
            "extra": kwargs,
        }
        self.data = {"error": error}
        self.status_code = status_code if status_code else self.status_code


class MyAppValidationError(MyAppException):
    """Raised when validation failed on one or more fields."""

    code = "validation-error"
    message = "Validation failed on one or more fields."

    def __init__(self, message=None, code=None, **kwargs):
        super().__init__(message, code, **kwargs)
