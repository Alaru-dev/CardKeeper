from fastapi import HTTPException

from apps.auth.api.security_settings import get_password_hash
from apps.db_models import User
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf.application import app
from projconf.end_points import UsersEndPoints

from ...db_auth_func import db_add_user, db_get_user_by_name
from ..req_res_models import SignUpRequest, UserOut


@app.post(UsersEndPoints.SignUp, response_model=UserOut)
async def sign_up_controller(user: SignUpRequest):
    user.password = get_password_hash(user.password)
    async with async_session() as session, session.begin():
        exist_user = await db_get_user_by_name(session, User, user.username)
        if exist_user:
            raise HTTPException(
                ErrorResponse.USERNAME_NOT_UNIQ.status_code,
                ErrorResponse.USERNAME_NOT_UNIQ.detail,
            )
        else:
            created_user = await db_add_user(session, User, user)
            return UserOut(id=created_user.id, username=created_user.username)
