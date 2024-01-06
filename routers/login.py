from fastapi import APIRouter
from fastapi import Body
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from utils.jwt_manager import create_token

class User(BaseModel):
    email: str
    password: str

login_router = APIRouter(prefix='/login', tags=['Auth'])

@login_router.post('', response_model=dict, status_code=200)
def login(user: User = Body(...)):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token = create_token(user.dict())
        return JSONResponse(content={'message': 'Login success', 'token': token}, status_code=200)