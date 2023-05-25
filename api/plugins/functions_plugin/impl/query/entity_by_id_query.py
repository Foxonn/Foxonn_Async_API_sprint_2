from typing import Any
from typing import Mapping
from typing import TypeVar

from elasticsearch import AsyncElasticsearch

from api.plugins.functions_plugin.interfaces.query import IEntityByIdQuery

__all__ = ['EntityByIdQuery']

T = TypeVar("T")


class EntityByIdQuery(IEntityByIdQuery):
    __slots__ = (
        '__elastic',
    )

    def __init__(self, elastic: AsyncElasticsearch) -> None:
        self.__elastic = elastic

    async def __call__(self, index: str, id_: str) -> Mapping[str, Any] | None:
        doc = await self.__elastic.get(index=index, id=id_)
        return doc['_source']
