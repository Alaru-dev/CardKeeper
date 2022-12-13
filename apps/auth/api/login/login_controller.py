from fastapi import Depends, HTTPException, status

from apps.auth.api.security_settings import AuthJWT, verify_password
from apps.db import async_session
from apps.projconf import app

from ...db_auth_func import db_get_user
from ...db_models import User
from .login_request import LoginRequest


@app.post("/login", operation_id="authorize")
async def login_controller(user: LoginRequest, Authorize: AuthJWT = Depends()):
    async with async_session() as session, session.begin():
        exist_user = await db_get_user(session, User, user.username)
        if exist_user:
            if verify_password(user.password, exist_user.password):
                access_token = Authorize.create_access_token(
                    subject=user.username
                )
                return {"access_token": access_token, "id": exist_user.id}
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad password"
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad username"
        )
