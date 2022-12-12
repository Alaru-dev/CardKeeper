import json
import os
import shutil

from fastapi import HTTPException, Depends, status, UploadFile, Form, File
from apps.db import async_session
from apps.auth.api.security_settings import AuthJWT
from apps.projconf import app
from .create_card_request import CreateCardRequest
from ...db_models import Card
from ...db_card_func import db_get_card, db_add_card, StoragePath


@app.post('/{user_id}/create_card')
async def create_card_controller(user_id, image: UploadFile = File(),  data = Form(description='required json str, example: {"user_id": int, "card_name": str, "group": str, "favorites": bool}'),  Authorize: AuthJWT = Depends()):
    data = json.loads(data)
    card_name, group, favorites = data.get("card_name"), data.get("group"), data.get("favorites")
    Authorize.jwt_required()
    card = CreateCardRequest(user_id=user_id, card_name=card_name, group=group, favorites=None)
    async with async_session() as session, session.begin():
        not_uniq_card_name = await db_get_card(session, Card, f"{card.user_id}{card.card_name}")
        if not not_uniq_card_name:
            user_storage_dir = get_or_create_user_directory(StoragePath, user_id)

            card_storage_absolute_path = os.path.join(user_storage_dir, add_new_file_name(image.filename, card_name))
            with open(card_storage_absolute_path, "wb+") as file_object:
                file_object.write(image.file.read())
                # shutil.copyfileobj(image.file, file_object)
            created_card = await db_add_card(session, Card, card)

            return {"Info": "Created", "card_name": card.card_name}
        else:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="This card_name is not unique")


def add_new_file_name(file_name, card_name):
    last_point_position = file_name.rfind('.')
    return card_name+file_name[last_point_position:]


def get_or_create_user_directory(storage_path, user_id):
    user_directory = os.path.join(StoragePath, user_id)
    if not os.path.isdir(user_directory):
        os.mkdir(user_directory)
    return user_directory
