from pydantic import BaseModel


class UserDeleteRequest(BaseModel):
    username: str
    password: str
