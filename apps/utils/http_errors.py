import enum


class ErrorResponse(enum.Enum):
    """Enum for HTTP Errors"""

    BAD_REQUEST = (400, "Bad Request")
    BAD_USERNAME = (401, "Bad username")
    BAD_PASSWORD = (401, "Bad password")

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
