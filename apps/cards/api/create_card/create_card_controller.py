import json
import os

from fastapi import Depends, File, Form, HTTPException, UploadFile, status

from apps.auth.api.security_settings import AuthJWT
from apps.db_models import Card
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import StoragePath, app

from ...db_card_func import db_add_card, db_get_card_by_name
from ..req_res_models import CardOut, CreateCardRequest


@app.post("/api/v1/create_card", response_model=CardOut)
async def create_card_controller(
    image: UploadFile = File(),
    data=Form(
        description='required json str, example: {"card_name": str, "group": str, "favorites": bool}'
    ),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    new_card = CreateCardRequest(**json.loads(data))
    async with async_session() as session, session.begin():
        check_is_card_exist = await db_get_card_by_name(
            session, Card, current_user_id, new_card.card_name
        )
        if check_is_card_exist:
            raise HTTPException(
                ErrorResponse.CARD_NAME_NOT_UNIQ.status_code,
                detail=ErrorResponse.CARD_NAME_NOT_UNIQ.detail,
            )
        user_storage_dir = get_or_create_user_directory(
            StoragePath, current_user_id
        )
        card_storage_absolute_path = os.path.join(
            user_storage_dir,
            add_new_file_name(image.filename, new_card.card_name),
        )
        with open(card_storage_absolute_path, "wb+") as file_object:
            file_object.write(image.file.read())
        created_card = await db_add_card(
            session,
            Card,
            current_user_id,
            new_card,
            card_storage_absolute_path,
        )
        return CardOut(
            id=created_card.id,
            card_name=created_card.card_name,
            group=created_card.group,
            favorites=created_card.favorites,
        )


def add_new_file_name(file_name, card_name):
    last_point_position = file_name.rfind(".")
    return card_name + file_name[last_point_position:]


def get_or_create_user_directory(storage_path, current_user_id):
    user_directory = os.path.join(storage_path, str(current_user_id))
    if not os.path.isdir(user_directory):
        os.mkdir(user_directory)
    return user_directory
