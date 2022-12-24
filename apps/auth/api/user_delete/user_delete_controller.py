import os
import shutil

from fastapi import Depends

from apps.auth.api.security_settings import AuthJWT
from apps.db_models import User
from apps.utils.db_specify import async_session
from projconf import StoragePath, app
from projconf.end_points import UsersEndPoints

from ...db_auth_func import db_delete_user
from ..req_res_models import UserDeleteResponse


@app.delete(UsersEndPoints.Delete, response_model=UserDeleteResponse)
async def user_delete_controller(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    async with async_session() as session, session.begin():
        deleted_user = await db_delete_user(session, User, current_user_id)
        if os.path.isdir(os.path.join(StoragePath, str(current_user_id))):
            shutil.rmtree(os.path.join(StoragePath, str(current_user_id)))
        return UserDeleteResponse(
            id=deleted_user.id, username=deleted_user.username
        )
