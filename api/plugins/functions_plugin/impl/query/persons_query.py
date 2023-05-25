from typing import Any
from typing import Mapping
from typing import Sequence

from elasticsearch import AsyncElasticsearch

from api.plugins.functions_plugin.interfaces.query import IPersonsQuery

__all__ = ['PersonsQuery']


class PersonsQuery(IPersonsQuery):
    __slots__ = (
        '__elastic',
    )

    def __init__(self, elastic: AsyncElasticsearch):
        self.__elastic = elastic

    async def __call__(
        self,
        page_number: int,
        page_size: int,
    ) -> Sequence[Mapping[str, Any] | None]:
        from_ = page_size * page_number
        body = {"query": {"match_all": {}}}

        result = await self.__elastic.search(
            index='persons',
            body=body,
            from_=from_,
            size=page_size,
        )
        records = result['hits']['hits']
        return [record['_source'] for record in records] if records else []
