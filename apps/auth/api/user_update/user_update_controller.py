from fastapi import HTTPException, Depends, status
from apps.db import async_session
from apps.auth.api.security_settings import get_password_hash, verify_password, AuthJWT
from apps.projconf import app
from .user_update_request import UserUpdateRequest
from ...db_models import User
from ...db_auth_func import db_get_user, db_update_user


@app.put('/{user_id}/user_update')
async def user_update_controller(user: UserUpdateRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    if (not user.new_username and not user.new_password) or (user.new_username == user.username and user.new_password == user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nothing to change")
    async with async_session() as session, session.begin():
        not_uniq_new_name = await db_get_user(session, User, user.new_username)
        if not not_uniq_new_name:
            exist_user = await db_get_user(session, User, user.username)
            if user.new_username:
                exist_user.username = user.new_username
            if user.new_password:
                exist_user.password = get_password_hash(user.new_password)
                updated_user = await db_update_user(session, User, exist_user)
                return {"Info": "Updated", "user_id": exist_user.id, "updated_username": exist_user.username}
        else:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="This username is noy unique")
