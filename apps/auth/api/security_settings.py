from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from passlib.context import CryptContext
from pydantic import BaseModel

from apps.projconf import app


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code, content={"detail": exc.message}
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(user_password, hashed_password):
    return pwd_context.verify(user_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
