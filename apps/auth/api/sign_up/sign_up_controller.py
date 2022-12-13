from fastapi import HTTPException, status

from apps.auth.api.security_settings import get_password_hash
from apps.db import async_session
from apps.projconf import app

from ...db_auth_func import db_add_user, db_get_user
from ...db_models import User
from .sign_up_request import SignUpRequest


@app.post("/signup")
async def sign_up_controller(user: SignUpRequest):
    user.password = get_password_hash(user.password)
    async with async_session() as session, session.begin():
        exist_user = await db_get_user(session, User, user.username)
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="This username is noy unique",
            )
        else:
            created_user = await db_add_user(session, User, user)
            return {user.username: "Created", "id": created_user.id}
