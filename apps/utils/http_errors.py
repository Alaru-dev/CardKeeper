import enum


class ErrorResponse(enum.Enum):
    """Enum for HTTP Errors"""

    BAD_REQUEST = (400, "Bad Request")
    BAD_USERNAME = (401, "Bad username")
    BAD_PASSWORD = (401, "Bad password")
    USERNAME_NOT_UNIQ = (406, "This username is not unique")
    NOTHING_TO_CHANGE = (400, "Nothing to change")
    CARD_NAME_NOT_UNIQ = (406, "This card_name is not unique")
    CARD_NOT_EXIST = (404, "Card don`t exist")
    USER_HAVE_NOT_CARDS = (404, "User haven`t cards")

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
