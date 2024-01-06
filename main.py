from fastapi import FastAPI, Depends, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer

from pydantic import BaseModel, Field
from typing import Optional, List

from starlette.requests import Request
from jwt_manager import create_token, validate_token

from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
app.title = "Curso de FastAPI"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Invalid user")
        

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=5, max_length=50)
    year: int = Field(ge=1900, le=2024)
    rating: float = Field(ge=0, le=10)
    category: str = Field(min_length=3, max_length=15)

    model_config = {
      "json_schema_extra": {
          "examples": [
              {   "id": 1,
                  "title": "The Shawshank Redemption",
                  "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                  "year": 1994,
                  "rating": 9.3,
                  "category": "Drama"
              }
          ]
      }
    }
    
@app.get('/', tags=['Home'])
def message():
    return HTMLResponse(content='<h1>Curso de FastAPI</h1>', status_code=200)

@app.post('/login', tags=['Auth'], response_model=dict, status_code=200)
def login(user: User = Body(...)):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token = create_token(user.dict())
        return JSONResponse(content={'message': 'Login success', 'token': token}, status_code=200)

@app.get('/movies', tags=['Movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())] )
def get_movies() -> List[Movie]:
    db = Session()
    movies = db.query(MovieModel).all()
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie,   status_code=200)
def get_movie(id: int = Path(ge=1, le=100)) -> Movie:
    db = Session()
    movie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if movie:
      return JSONResponse(content=jsonable_encoder(movie), status_code=200)
    return JSONResponse(content={'error': 'Movie not found'}, status_code=404)

@app.get('/movies/', tags=['Movies'], response_model=List[Movie], status_code=200)
def get_movie_by_category(category: str = Query(min_length=3, max_length=15)) -> List[Movie]:
    db = Session()
    movies = db.query(MovieModel).filter(MovieModel.category.lower() == category.lower()).all()
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@app.post('/movies', tags=['Movies'], response_model=dict, status_code=201)
def create_movie(movie: Movie = Body()) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created"}, status_code=201)

@app.put('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie = Body()) -> dict:
    db = Session()
    foundedMovie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if foundedMovie:
        foundedMovie.title = movie.title
        foundedMovie.overview = movie.overview
        foundedMovie.year = movie.year
        foundedMovie.rating = movie.rating
        foundedMovie.category = movie.category
        db.commit()
        return JSONResponse(content={'message': 'Movie updated'}, status_code=200)
    return JSONResponse(content={'error': 'Movie not found'}, status_code=404)

@app.delete('/movies/{id}', tags=['Movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    foundedMovie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if foundedMovie:
        db.delete(foundedMovie)
        db.commit()
        return JSONResponse(content={'message': 'Movie deleted'}, status_code=200)
    return JSONResponse(content={'error': 'Movie not found'}, status_code=404)