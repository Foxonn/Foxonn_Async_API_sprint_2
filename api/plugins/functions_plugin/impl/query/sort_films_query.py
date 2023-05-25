from typing import Any
from typing import Mapping
from typing import Sequence

from elasticsearch import AsyncElasticsearch

from api.plugins.functions_plugin.impl.query import GenreByIdQuery
from api.plugins.functions_plugin.interfaces.query import IFilmsQuery
from api.plugins.functions_plugin.utils import sort_parse

__all__ = ['FilmsQuery']


class FilmsQuery(IFilmsQuery):
    __slots__ = (
        '__elastic',
    )

    def __init__(self, elastic: AsyncElasticsearch):
        self.__elastic = elastic

    async def __call__(
        self,
        page_number: int,
        page_size: int,
        sort: str | None = None,
        genre: str | None = None,
    ) -> Sequence[Mapping[str, Any] | None]:
        from_ = page_size * page_number
        body = {}

        if genre:
            get_genre = GenreByIdQuery(elastic=self.__elastic)
            if result := await get_genre(id_=genre):
                body.update({"query": {"bool": {"must": [{"match": {"genre": result['name']}}]}}})
        else:
            body.update({"query": {"match_all": {}}})

        if sort:
            body.update({"sort": [sort_parse(sort)]})

        result = await self.__elastic.search(
            index='movies',
            body=body,
            from_=from_,
            size=page_size,
        )
        records = result['hits']['hits']
        return [record['_source'] for record in records] if records else []
