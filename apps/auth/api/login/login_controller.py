from fastapi import Depends, HTTPException, status

from apps.auth.api.security_settings import AuthJWT, verify_password
from apps.db_models import User
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf.application import app

from ...db_auth_func import db_get_user_by_name
from ..req_res_models import LoginRequest, LoginResponse


@app.post(
    "/api/v1/login", operation_id="authorize", response_model=LoginResponse
)
async def login_controller(user: LoginRequest, Authorize: AuthJWT = Depends()):
    async with async_session() as session, session.begin():
        exist_user = await db_get_user_by_name(session, User, user.username)
        if exist_user:
            if verify_password(user.password, exist_user.password):
                access_token = Authorize.create_access_token(
                    subject=exist_user.id,
                )
                return LoginResponse(
                    id=exist_user.id,
                    username=exist_user.username,
                    token=access_token,
                )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorResponse.BAD_PASSWORD.detail,
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorResponse.BAD_USERNAME.detail,
        )
