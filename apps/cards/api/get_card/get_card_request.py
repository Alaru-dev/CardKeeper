from pydantic import BaseModel


class GetCardRequest(BaseModel):
    user_id: int
    card_name: str

