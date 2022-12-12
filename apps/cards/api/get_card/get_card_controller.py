import os

from fastapi import HTTPException, Depends, status, UploadFile, Form, File
from apps.db import async_session
from apps.auth.api.security_settings import AuthJWT
from apps.projconf import app
from ...db_models import Card
from ...db_card_func import db_get_card, db_add_card, StoragePath
from .get_card_request import GetCardRequest


@app.get('/{user_id}/get_card/{card_name}')
async def get_card_controller(user_id, card_name,  Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    async with async_session() as session, session.begin():
        current_card: Card = await db_get_card(session, Card, f"{user_id}{card_name}")
        if current_card:
            files_list = os.listdir(current_card.card_path)
            card_path_without_ext = os.path.join(current_card.card_path, current_card.card_name[1:])
            full_file_name = [file for file in files_list if current_card.card_name[1:] in file][0]
            card_absolute_path = os.path.join(current_card.card_path, full_file_name)
            with open(card_absolute_path, "rb") as file_object:
                return file_object
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Card don`t exist")
