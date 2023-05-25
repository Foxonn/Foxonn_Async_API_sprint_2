from http import HTTPStatus
from typing import Annotated
from typing import Any
from typing import Mapping
from typing import Sequence

import elasticsearch
from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from redis.asyncio.client import Redis

from api.models.movies_model import FilmModel
from api.models.movies_model import GenreModel
from api.models.movies_model import MoviesModel
from api.models.movies_model import PersonModel
from api.utils.ioc import ioc
from api.utils.plugins_manager import IPlugin
from ...functions_plugin.interfaces.query import IFilmByIdQuery
from ...functions_plugin.interfaces.query import IFilmsPersonByIdQuery
from ...functions_plugin.interfaces.query import IGenreByIdQuery
from ...functions_plugin.interfaces.query import IGenresQuery
from ...functions_plugin.interfaces.query import IPersonByIdQuery
from ...functions_plugin.interfaces.query import IPersonsQuery
from ...functions_plugin.interfaces.query import ISearchFilmsQuery
from ...functions_plugin.interfaces.query import ISearchPersonsQuery
from ...functions_plugin.interfaces.query import IFilmsQuery

__all__ = ['ApiV1Plugin']


class ApiV1Plugin(IPlugin):
    __slots__ = (
        '__route',
    )

    def __init__(self) -> None:
        self.__route = APIRouter(prefix="/v1")

    @property
    def name(self) -> str:
        return 'api_v1'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        redis = await ioc.get(Redis)
        app = await ioc.get(FastAPI)

        async def film_details(film_id: str) -> MoviesModel:
            query = await ioc.get(IFilmByIdQuery)
            try:
                result = await query(id_=film_id)
            except elasticsearch.exceptions.NotFoundError:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item not found')

            if not result:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
            else:
                return MoviesModel(**result)

        async def genres_details(genre_id: str) -> GenreModel:
            query = await ioc.get(IGenreByIdQuery)
            try:
                result = await query(id_=genre_id)
            except elasticsearch.exceptions.NotFoundError:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item not found')

            if not result:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item not found')
            return GenreModel(**result)

        async def persons_details(person_id: str) -> PersonModel:
            query = await ioc.get(IPersonByIdQuery)
            try:
                result = await query(id_=person_id)
            except elasticsearch.exceptions.NotFoundError:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item not found')

            if not result:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item not found')
            return PersonModel(**result)

        async def films_person(person_id: str) -> Sequence[FilmModel]:
            query = await ioc.get(IFilmsPersonByIdQuery)
            result = await query(id_=person_id)
            if not result:
                raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item not found')
            return [FilmModel(**item) for item in result] if result else []

        async def films(
            sort: str | None = None,
            genre: str | None = None,
            page_number: Annotated[int | None, Query(gt=0)] = 1,
            page_size: Annotated[int | None, Query(gt=0, lt=75)] = 25,
        ) -> Sequence[FilmModel | None]:
            query = await ioc.get(IFilmsQuery)
            result = await query(sort=sort, page_number=page_number, page_size=page_size, genre=genre)
            return [FilmModel(**item) for item in result] if result else []

        async def persons(
            page_number: Annotated[int | None, Query(gt=0)] = 1,
            page_size: Annotated[int | None, Query(gt=0, lt=75)] = 25,
        ) -> Sequence[PersonModel | None]:
            query = await ioc.get(IPersonsQuery)
            result = await query(page_number=page_number, page_size=page_size)
            return [PersonModel(**item) for item in result] if result else []

        async def genres(
            page_number: Annotated[int | None, Query(gt=0)] = 1,
            page_size: Annotated[int | None, Query(gt=0, lt=75)] = 25,
        ) -> Sequence[GenreModel | None]:
            query = await ioc.get(IGenresQuery)
            result = await query(page_number=page_number, page_size=page_size)
            return [GenreModel(**item) for item in result] if result else []

        async def films_search(
            query: str,
            page_number: Annotated[int | None, Query(gt=0)] = 1,
            page_size: Annotated[int | None, Query(gt=0, lt=75)] = 25,
        ) -> Sequence[FilmModel | None]:
            query_ = await ioc.get(ISearchFilmsQuery)
            result = await query_(query=query, page_number=page_number, page_size=page_size)
            return [FilmModel(**item) for item in result] if result else []

        async def persons_search(
            query: str,
            page_number: Annotated[int | None, Query(gt=0)] = 1,
            page_size: Annotated[int | None, Query(gt=0, lt=75)] = 25,
        ) -> Sequence[PersonModel | None]:
            query_ = await ioc.get(ISearchPersonsQuery)
            result = await query_(query=query, page_number=page_number, page_size=page_size)
            return [PersonModel(**item) for item in result] if result else []

        self.__route.add_api_route(
            path='/films/search',
            endpoint=films_search,
            response_model=Sequence[FilmModel],
            description='Поиск среди фильмов по названию.'
        )
        self.__route.add_api_route(
            path='/films/{film_id}',
            endpoint=film_details,
            response_model=MoviesModel,
            description='Получить фильм по идентификатору.'
        )
        self.__route.add_api_route(
            path='/films',
            endpoint=films,
            response_model=Sequence[FilmModel],
            description='Получить список фильмов.'
        )

        self.__route.add_api_route(
            path='/genres',
            endpoint=genres,
            response_model=Sequence[GenreModel],
            description='Поличить список жанров.'
        )
        self.__route.add_api_route(
            path='/genres/{genre_id}',
            endpoint=genres_details,
            response_model=GenreModel,
            description='Поиск среди жанров по названию.'
        )

        self.__route.add_api_route(
            path='/persons',
            endpoint=persons,
            response_model=Sequence[PersonModel],
            description='Поличить список персон.'
        )
        self.__route.add_api_route(
            path='/persons/search',
            endpoint=persons_search,
            response_model=Sequence[PersonModel],
            description='Поиск среди участников по имени.'
        )
        self.__route.add_api_route(
            path='/persons/{person_id}',
            endpoint=persons_details,
            response_model=PersonModel,
            description='Получить информацию о человеке.'
        )
        self.__route.add_api_route(
            path='/persons/{person_id}/film',
            endpoint=films_person,
            response_model=Sequence[FilmModel],
            description='Получить фильмы в которых человек принимал участие.',
        )

        app.include_router(self.__route)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        pass
