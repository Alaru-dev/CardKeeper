import os
import shutil

from fastapi import HTTPException, Depends, status

from apps.db.card_storage_settings import StoragePath
from ...db_auth_func import db_get_user, db_delete_user
from apps.auth.api.security_settings import verify_password, AuthJWT
from apps.db import async_session
from apps.projconf import app
from .user_delete_request import UserDeleteRequest
from ...db_models import User


@app.delete('/{user_id}/user_delete')
async def user_delete_controller(user_id, user: UserDeleteRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    async with async_session() as session, session.begin():
        deleted_user = await db_delete_user(session, User, user)
        shutil.rmtree(os.path.join(StoragePath, str(user_id)))
        return {"Info": "Deleted", "name": user.username}
