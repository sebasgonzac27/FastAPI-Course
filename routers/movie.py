from fastapi import APIRouter

from fastapi import Depends, Body, Path, Query
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field
from typing import Optional, List

from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

from middlewares.jwt_bearer import JWTBearer

from services.movie import Movie as MovieService

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


movie_router = APIRouter(prefix='/movies', tags=['Movies'])

@movie_router.get('', response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    db = Session()
    movies = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@movie_router.get('/{id}', response_model=Movie,   status_code=200)
def get_movie(id: int = Path(ge=1, le=100)) -> Movie:
    db = Session()
    movie = MovieService(db).get_movie(id)
    if movie:
      return JSONResponse(content=jsonable_encoder(movie), status_code=200)
    return JSONResponse(content={'error': 'Movie not found'}, status_code=404)

@movie_router.get('/', response_model=List[Movie], status_code=200)
def get_movie_by_category(category: str = Query(min_length=3, max_length=15)) -> List[Movie]:
    db = Session()
    movies = db.query(MovieModel).filter(MovieModel.category.lower() == category.lower()).all()
    return JSONResponse(content=jsonable_encoder(movies), status_code=200)

@movie_router.post('', response_model=dict, status_code=201, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie = Body()) -> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(content={"message": "Movie created"}, status_code=201)

@movie_router.put('/{id}', response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
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

@movie_router.delete('/{id}', response_model=dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int) -> dict:
    db = Session()
    foundedMovie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if foundedMovie:
        db.delete(foundedMovie)
        db.commit()
        return JSONResponse(content={'message': 'Movie deleted'}, status_code=200)
    return JSONResponse(content={'error': 'Movie not found'}, status_code=404)