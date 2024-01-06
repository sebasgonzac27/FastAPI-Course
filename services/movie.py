from models.movie import Movie as MovieModel
from schemas.movie import Movie as MovieSchema

class Movie():

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        movies = self.db.query(MovieModel).all()
        return movies
    
    def get_movie(self, id: int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return movie
    
    def get_movie_by_category(self, category: str):
        movies = self.db.query(MovieModel).filter(MovieModel.category.lower() == category.lower()).all()
        return movies
    
    def create_movie(self, movie: MovieSchema):
        new_movie = MovieModel(**movie.dict())
        self.db.add(new_movie)
        self.db.commit()
        return
    
    def update_movie(self, id: int, movie: MovieSchema):
        foundedMovie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        foundedMovie.title = movie.title
        foundedMovie.overview =movie.overview
        foundedMovie.year = movie.year
        foundedMovie.rating = movie.rating
        foundedMovie.category =movie.category
        self.db.commit()
        return
    
    def delete_movie(self, id: int):
        foundedMovie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        self.db.delete(foundedMovie)
        self.db.commit()
        return