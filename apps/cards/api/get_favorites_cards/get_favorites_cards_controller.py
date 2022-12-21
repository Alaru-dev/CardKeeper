from fastapi import Depends, HTTPException

from apps.auth.api.security_settings import AuthJWT
from apps.db_models import Card
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import app

from ...db_card_func import db_get_all_card
from ..req_res_models import CardOut, CardsOut


@app.get("/api/v1/get_favorites_cards")
async def get_favorites_cards_controller(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    async with async_session() as session, session.begin():
        card_massive = await db_get_all_card(session, Card, current_user_id)
        if card_massive:
            cards: CardsOut = []
            for el in card_massive.all():
                if el.favorites is True:
                    cards.append(
                        CardOut(
                            id=el.id,
                            card_name=el.card_name,
                            group=el.group,
                            favorites=el.favorites,
                        )
                    )
            return cards
        else:
            raise HTTPException(
                ErrorResponse.USER_HAVE_NOT_CARDS.status_code,
                detail=ErrorResponse.USER_HAVE_NOT_CARDS.detail,
            )
