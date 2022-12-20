from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class SignUpRequest(UserIn):
    pass


class LoginRequest(UserIn):
    pass


class UserDeleteRequest(UserIn):
    username: str = None
    pass


class UserUpdateRequest(BaseModel):
    new_username: str | None = None
    new_password: str | None = None


class UserOut(BaseModel):
    id: int
    username: str


class LoginResponse(UserOut):
    token: str


class UserUpdateResponse(UserOut):
    pass


class UserDeleteResponse(UserOut):
    pass
