from fastapi import Depends, File, HTTPException, status
from fastapi.responses import FileResponse

from apps.auth.api.security_settings import AuthJWT
from apps.db import async_session
from apps.projconf import app

from ...db_card_func import db_get_card
from ...db_models import Card
from .get_card_request import GetCardRequest


@app.get("/{user_id}/get_card/{card_name}")
async def get_card_controller(
    user_id: int, card_name: str, Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    async with async_session() as session, session.begin():
        current_card: Card = await db_get_card(
            session,
            Card,
            user_id,
            card_name,
        )
        card_full_name = get_file_name(current_card.card_path)
        if current_card:
            # with open(current_card.card_path, "rb") as file_object:
            return FileResponse(
                current_card.card_path, filename=card_full_name
            )
        else:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, detail="Card don`t exist"
            )


def get_file_name(card_path):
    position = card_path.rfind("/") + 1
    return card_path[position:]
