import os

from fastapi import Depends, HTTPException

from apps.auth.api.security_settings import AuthJWT
from apps.cards.api.req_res_models import CardOut
from apps.cards.db_card_func import (
    db_delete_card,
    db_get_card_by_id,
    db_get_card_by_name,
)
from apps.db_models import Card
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import app
from projconf.end_points import CardsEndPoints


@app.delete(CardsEndPoints.DeleteCard, response_model=CardOut)
async def delete_card_controller(card_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    async with async_session() as session, session.begin():
        current_card = await db_get_card_by_id(
            session, Card, current_user_id, card_id
        )
        if current_card:
            deleted_card = await db_delete_card(
                session, Card, current_user_id, card_id
            )
            if os.path.isfile(deleted_card.card_path):
                os.remove(deleted_card.card_path)
            return CardOut(
                id=deleted_card.id,
                card_name=deleted_card.card_name,
                group=deleted_card.group,
                favorites=deleted_card.favorites,
            )
        else:
            raise HTTPException(
                ErrorResponse.CARD_NOT_EXIST.status_code,
                ErrorResponse.CARD_NOT_EXIST.detail,
            )
