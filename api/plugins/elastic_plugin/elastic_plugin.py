from typing import Any
from typing import Mapping

from elasticsearch import AsyncElasticsearch

from api.plugins.elastic_plugin.elastic_config import ElasticConfig
from api.utils.ioc import ioc
from api.utils.plugins_manager import IPlugin

__all__ = ['ElasticPlugin']


class ElasticPlugin(IPlugin):
    __slots__ = (
        '__driver',
    )

    def __init__(self) -> None:
        self.__driver: AsyncElasticsearch | None = None

    @property
    def name(self) -> str:
        return 'elastic'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        settings = ElasticConfig(**plugins_settings)
        self.__driver = AsyncElasticsearch(hosts=f'{settings.host}:{settings.port}')
        ioc.set(AsyncElasticsearch, self.__driver)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        await self.__driver.close()
