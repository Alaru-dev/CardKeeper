from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from passlib.context import CryptContext
from apps.projconf import app


# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(user_password, hashed_password):
    return pwd_context.verify(user_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

# def read_file(filename):
#     with open(filename, 'r') as f:
#         binary = f.read()
#     return binary
#
# def save_fail(binary, file_name):
#     with open(file_name, "w") as file:
#         file.write(binary)

# if __name__=="main":
#     filename = '/send_storage/123.png'
#     binary = read_file(filename)
#     save_fail(binary, '/home/alaru/Projects/pythonProject/pythonProject/pythonProject/fast_api/api_methods/321.png')