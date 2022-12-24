from fastapi import Depends, HTTPException

from apps.auth.api.security_settings import AuthJWT
from apps.db_models import Card
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import app
from projconf.end_points import CardsEndPoints

from ...db_card_func import db_get_card_by_id
from ..req_res_models import CardOut


@app.get(CardsEndPoints.GetCardInfo, response_model=CardOut)
async def get_card_info_controller(
    card_id: int, Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    dict_1 = Authorize.get_raw_jwt()
    print(dict_1)
    async with async_session() as session, session.begin():
        current_card: Card = await db_get_card_by_id(
            session,
            Card,
            current_user_id,
            card_id,
        )
        if current_card:
            return CardOut(
                id=current_card.id,
                card_name=current_card.card_name,
                group=current_card.group,
                favorites=current_card.favorites,
            )
        else:
            raise HTTPException(
                ErrorResponse.CARD_NOT_EXIST.status_code,
                ErrorResponse.CARD_NOT_EXIST.detail,
            )
