from models.movie import Movie as MovieModel

class Movie():

    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        movies = self.db.query(MovieModel).all()
        return movies
    
    def get_movie(self, id: int):
        movie = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return movie