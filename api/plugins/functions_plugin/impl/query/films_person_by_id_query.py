from abc import abstractmethod
from typing import Any
from typing import Mapping
from typing import Sequence

from elasticsearch import AsyncElasticsearch

from api.plugins.functions_plugin.impl.query import PersonByIdQuery
from api.plugins.functions_plugin.interfaces.query import IFilmsPersonByIdQuery

__all__ = ['FilmsPersonByIdQuery']


class FilmsPersonByIdQuery(IFilmsPersonByIdQuery):
    __slots__ = (
        '__elastic',
    )

    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.__elastic = elastic

    @abstractmethod
    async def __call__(self, id_: str) -> Sequence[Mapping[str, Any] | None]:
        query = PersonByIdQuery(elastic=self.__elastic)
        result = await query(id_=id_)
        films_ids = [film['id'] for film in result['films']]
        body = {"query": {"terms": {"_id": films_ids}}}
        result = await self.__elastic.search(index='movies', body=body)
        records = result['hits']['hits']
        return [record['_source'] for record in records] if records else []
