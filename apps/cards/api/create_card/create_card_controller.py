import json
import os
import shutil

from fastapi import Depends, File, Form, HTTPException, UploadFile, status

from apps.auth.api.security_settings import AuthJWT
from apps.db import async_session
from apps.db.card_storage_settings import StoragePath
from apps.projconf import app

from ...db_card_func import db_add_card, db_get_all_card, db_get_card
from ...db_models import Card
from .create_card_request import CreateCardRequest


@app.post("/{user_id}/create_card")
async def create_card_controller(
    image: UploadFile = File(),
    data=Form(
        description='required json str, example: {"user_id": int, "card_name": str, "group": str, "favorites": bool}'
    ),
    Authorize: AuthJWT = Depends(),
):
    Authorize.jwt_required()

    new_card = CreateCardRequest(**json.loads(data))
    new_card.favorites = None
    async with async_session() as session, session.begin():
        check_is_card_exist = await db_get_card(
            session, Card, new_card.user_id, new_card.card_name
        )
        if check_is_card_exist:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                detail="This card_name is not unique",
            )
        user_storage_dir = get_or_create_user_directory(
            StoragePath, new_card.user_id
        )
        card_storage_absolute_path = os.path.join(
            user_storage_dir,
            add_new_file_name(image.filename, new_card.card_name),
        )
        with open(card_storage_absolute_path, "wb+") as file_object:
            file_object.write(image.file.read())
        created_card = await db_add_card(
            session, Card, new_card, card_storage_absolute_path
        )

        return {"Info": "Created", "card_name": created_card.card_name}


def add_new_file_name(file_name, card_name):
    last_point_position = file_name.rfind(".")
    return card_name + file_name[last_point_position:]


def get_or_create_user_directory(storage_path, user_id):
    user_directory = os.path.join(StoragePath, str(user_id))
    if not os.path.isdir(user_directory):
        os.mkdir(user_directory)
    return user_directory
