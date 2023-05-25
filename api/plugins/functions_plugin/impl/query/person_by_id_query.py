from typing import Any
from typing import Mapping

from elasticsearch import AsyncElasticsearch

from .entity_by_id_query import EntityByIdQuery
from ...interfaces.query import IPersonByIdQuery

__all__ = ['PersonByIdQuery']


class PersonByIdQuery(IPersonByIdQuery):
    __slots__ = (
        '__elastic',
    )

    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.__elastic = elastic

    async def __call__(self, id_: str) -> Mapping[str, Any] | None:
        query = EntityByIdQuery(elastic=self.__elastic)
        return await query(index='persons', id_=id_)
