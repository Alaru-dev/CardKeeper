from pydantic import BaseModel


class UserUpdateRequest(BaseModel):
    username: str
    password: str
    new_username: str | None = None
    new_password: str | None = None

