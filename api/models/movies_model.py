from typing import Any
from typing import Dict
from typing import List

from pydantic import BaseModel

from api.utils.extbasemodel import ExtBaseModel

__all__ = [
    'MoviesModel',
    'GenreModel',
    'FilmModel',
    'PersonModel',
]


class FilmModel(ExtBaseModel):
    id: str
    title: str
    imdb_rating: float


class MoviesModel(ExtBaseModel):
    id: str
    imdb_rating: float
    genre: str
    title: str
    description: str
    director: List[str] | None
    writers: List[Dict[str, Any]] | None
    actors: List[Dict[str, Any]] | None
    actors_names: List[str] | None
    writers_names: List[str] | None


class GenreModel(ExtBaseModel):
    id: str
    name: str


class PersonFilmModel(BaseModel):
    id: str
    roles: List[str]


class PersonModel(ExtBaseModel):
    id: str
    full_name: str
    films: List[PersonFilmModel]
