from fastapi import Depends, HTTPException

from apps.auth.api.security_settings import AuthJWT
from apps.db_models import Card
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import app

from ...db_card_func import db_get_all_card
from ..req_res_models import CardOut, CardsOut


@app.get("/api/v1/get_all_groups")
async def get_all_groups_controller(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    async with async_session() as session, session.begin():
        group_massive = await db_get_all_card(session, Card, current_user_id)
        if group_massive:
            groups = {}
            for el in group_massive.all():
                groups.update({el.group: el.card_name})
            return groups
        else:
            raise HTTPException(
                ErrorResponse.USER_HAVE_NOT_CARDS.status_code,
                detail=ErrorResponse.USER_HAVE_NOT_CARDS.detail,
            )
