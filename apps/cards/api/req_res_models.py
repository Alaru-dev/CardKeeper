from typing import List

from pydantic import BaseModel


class CardIn(BaseModel):
    card_name: str


class CreateCardRequest(CardIn):
    group: str | None = None
    favorites: bool | None = None


class UpdateCardRequest(BaseModel):
    new_card_name: str | None = None
    group: str | None = None
    favorites: bool | None = None


class GetCardRequest(CardIn):
    pass


class CardOut(BaseModel):
    id: int
    card_name: str
    group: str | None
    favorites: bool | None


class CardsOut(BaseModel):
    cards: List[CardOut]
