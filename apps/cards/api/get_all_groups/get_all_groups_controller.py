from fastapi import Depends, HTTPException

from apps.auth.api.security_settings import AuthJWT
from apps.db_models import Card
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import app
from projconf.end_points import CardsEndPoints

from ...db_card_func import db_get_all_card


@app.get(CardsEndPoints.GetAllGroup)
async def get_all_groups_controller(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    async with async_session() as session, session.begin():
        group_massive = await db_get_all_card(session, Card, current_user_id)
        if group_massive:
            groups = set()
            for el in group_massive.all():
                if el.group:
                    groups.add(el.group)
            return groups
        else:
            raise HTTPException(
                ErrorResponse.USER_HAVE_NOT_CARDS.status_code,
                ErrorResponse.USER_HAVE_NOT_CARDS.detail,
            )
