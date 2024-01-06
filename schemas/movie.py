from pydantic import BaseModel, Field
from typing import Optional

class MovieSchema(BaseModel):
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