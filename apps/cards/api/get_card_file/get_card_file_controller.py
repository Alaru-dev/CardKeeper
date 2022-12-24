from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse

from apps.auth.api.security_settings import AuthJWT
from apps.db_models import Card
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import app
from projconf.end_points import CardsEndPoints

from ...db_card_func import db_get_card_by_id


@app.get(CardsEndPoints.GetCardFile)
async def get_card_file_controller(
    card_id: int, Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    async with async_session() as session, session.begin():
        current_card: Card = await db_get_card_by_id(
            session,
            Card,
            current_user_id,
            card_id,
        )
        if current_card:
            card_full_name = get_file_name(current_card.card_path)
            return FileResponse(
                current_card.card_path, filename=card_full_name
            )
        else:
            raise HTTPException(
                ErrorResponse.CARD_NOT_EXIST.status_code,
                ErrorResponse.CARD_NOT_EXIST.detail,
            )


def get_file_name(card_path):
    position = card_path.rfind("/") + 1
    return card_path[position:]
