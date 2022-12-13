import os
import shutil

from fastapi import Depends, HTTPException, status

from apps.auth.api.security_settings import AuthJWT, verify_password
from apps.db import async_session
from apps.db.card_storage_settings import StoragePath
from apps.projconf import app

from ...db_auth_func import db_delete_user, db_get_user
from ...db_models import User
from .user_delete_request import UserDeleteRequest


@app.delete("/{user_id}/user_delete")
async def user_delete_controller(
    user_id, user: UserDeleteRequest, Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    async with async_session() as session, session.begin():
        deleted_user = await db_delete_user(session, User, user)
        shutil.rmtree(os.path.join(StoragePath, str(user_id)))
        return {"Info": "Deleted", "name": user.username}
