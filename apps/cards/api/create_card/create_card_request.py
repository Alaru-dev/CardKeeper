from pydantic import BaseModel


class CreateCardRequest(BaseModel):
    user_id: int
    card_name: str
    group: str | None = None
    favorites: str | None = None
