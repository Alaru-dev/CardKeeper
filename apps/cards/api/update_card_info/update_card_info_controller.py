import os

from fastapi import Depends, HTTPException

from apps.auth.api.security_settings import AuthJWT
from apps.db_models import Card
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import app
from projconf.end_points import CardsEndPoints

from ..req_res_models import CardOut, UpdateCardRequest

from ...db_card_func import (  # isort:skip
    db_get_card_by_id,
    db_get_card_by_name,
    db_update_card,
)


@app.put(CardsEndPoints.UpdateCardInfo, response_model=CardOut)
async def update_card_controller(
    card_id: int,
    update_card: UpdateCardRequest,
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    async with async_session() as session, session.begin():
        current_card = await db_get_card_by_id(
            session, Card, current_user_id, card_id
        )
        if (
            not update_card.new_card_name
            and not update_card.group
            and not update_card.favorites
        ):
            raise HTTPException(
                ErrorResponse.NOTHING_TO_CHANGE.status_code,
                ErrorResponse.NOTHING_TO_CHANGE.detail,
            )
        if update_card.new_card_name:
            check_new_card_name_is_unique = await db_get_card_by_name(
                session, Card, current_user_id, update_card.new_card_name
            )
            if check_new_card_name_is_unique:
                raise HTTPException(
                    ErrorResponse.CARD_NAME_NOT_UNIQ.status_code,
                    ErrorResponse.CARD_NAME_NOT_UNIQ.detail,
                )
            new_card_path = add_new_file_name_to_path(
                current_card.card_path, update_card.new_card_name
            )
            os.rename(current_card.card_path, new_card_path)
            current_card.card_name, current_card.card_path = (
                update_card.new_card_name,
                new_card_path,
            )
        if update_card.group:
            current_card.group = update_card.group
        if update_card.favorites is not None:
            current_card.favorites = update_card.favorites
        updated_card = await db_update_card(
            session, Card, current_user_id, current_card
        )
        return CardOut(
            id=updated_card.id,
            card_name=updated_card.card_name,
            group=updated_card.group,
            favorites=updated_card.favorites,
        )


def add_new_file_name_to_path(card_path, new_card_name):
    extension = card_path[card_path.rfind(".") :]
    user_storage_dir = card_path[: card_path.rfind("/")]
    return os.path.join(user_storage_dir, new_card_name + extension)
