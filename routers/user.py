from fastapi import APIRouter
from fastapi import Body
from fastapi.responses import JSONResponse

from utils.jwt_manager import create_token

from schemas.user import User as UserSchema

user_router = APIRouter(prefix='/login', tags=['Auth'])

@user_router.post('', response_model=dict, status_code=200)
def login(user: UserSchema = Body(...)):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token = create_token(user.dict())
        return JSONResponse(content={'message': 'Login success', 'token': token}, status_code=200)