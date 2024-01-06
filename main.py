from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "Curso de FastAPI"
app.version = "0.0.1"

movies = [
  {
    "id": 1,
    "title": "The Shawshank Redemption",
    "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    "year": 1994,
    "rating": 9.3,
    "category": "Drama"
  },
  {
    "id": 2,
    "title": "The Godfather",
    "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
    "year": 1972,
    "rating": 9.2,
    "category": "Crime"
  },
  {
    "id": 3,
    "title": "The Dark Knight",
    "overview": "When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.",
    "year": 2008,
    "rating": 9.0,
    "category": "Action"
  },
  {
    "id": 4,
    "title": "12 Angry Men",
    "overview": "A jury holdout attempts to prevent a miscarriage of justice by forcing his colleagues to reconsider the evidence.",
    "year": 1957,
    "rating": 9.0,
    "category": "Drama"
  },
  {
    "id": 5,
    "title": "Schindler's List",
    "overview": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.",
    "year": 1993,
    "rating": 8.9,
    "category": "Biography"
  },
  {
    "id": 6,
    "title": "Pulp Fiction",
    "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
    "year": 1994,
    "rating": 8.9,
    "category": "Crime"
  },
  {
    "id": 7,
    "title": "The Lord of the Rings: The Return of the King",
    "overview": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
    "year": 2003,
    "rating": 8.9,
    "category": "Action"
  },
  {
    "id": 8,
    "title": "Fight Club",
    "overview": "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.",
    "year": 1999,
    "rating": 8.8,
    "category": "Drama"
  },
  {
    "id": 9,
    "title": "Forrest Gump",
    "overview": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
    "year": 1994,
    "rating": 8.8,
    "category": "Romance"
  },
  {
    "id": 10,
    "title": "Inception",
    "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    "year": 2010,
    "rating": 8.8,
    "category": "Action"
  }
]

@app.get('/', tags=['Home'])
def message():
    return HTMLResponse(content='<h1>Curso de FastAPI</h1>', status_code=200)

@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return {'error': 'Movie not found'}

@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str):
    return [movie for movie in movies if movie['category'].lower() == category.lower()]

@app.post('/movies', tags=['Movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movie = {
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    }
    movies.append(movie)
    return movie