from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, JSONResponse

from pydantic import BaseModel

from jwt_manager import create_token

from config.database import engine, Base

from middlewares.error_handler import ErrorHandler

from routers.movie import movie_router
from routers.login import login_router

app = FastAPI()
app.title = "Curso de FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(login_router)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)
    
@app.get('/', tags=['Home'])
def message():
    return HTMLResponse(content='<h1>Curso de FastAPI</h1>', status_code=200)