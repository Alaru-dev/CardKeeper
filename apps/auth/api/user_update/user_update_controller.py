from fastapi import Depends, HTTPException, status

from apps.db_models import User
from apps.utils.db_specify import async_session
from apps.utils.http_errors import ErrorResponse
from projconf import app

from ..req_res_models import UserUpdateRequest, UserUpdateResponse

from ...db_auth_func import (  # isort:skip
    db_get_user_by_id,
    db_get_user_by_name,
    db_update_user,
)

from apps.auth.api.security_settings import (  # isort:skip
    AuthJWT,
    get_password_hash,
)


@app.put("/api/v1/user_update", response_model=UserUpdateResponse)
async def user_update_controller(
    user: UserUpdateRequest, Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    if not user.new_username and not user.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorResponse.NOTHING_TO_CHANGE.detail,
        )
    async with async_session() as session, session.begin():
        not_uniq_new_name = await db_get_user_by_name(
            session, User, user.new_username
        )
        if not not_uniq_new_name:
            exist_user = await db_get_user_by_id(
                session, User, current_user_id
            )
            if user.new_username:
                exist_user.username = user.new_username
            if user.new_password:
                exist_user.password = get_password_hash(user.new_password)
            updated_user = await db_update_user(session, User, exist_user)
            return UserUpdateResponse(
                id=updated_user.id, username=updated_user.username
            )
        else:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE,
                detail=ErrorResponse.BAD_PASSWORD.detail,
            )
