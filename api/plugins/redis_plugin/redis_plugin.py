from typing import Any
from typing import Mapping

from redis.asyncio.client import Redis

from .redis_config import RedisConfig
from api.utils.ioc import ioc
from api.utils.plugins_manager import IPlugin

__all__ = ['RedisPlugin']


class RedisPlugin(IPlugin):
    __slots__ = (
        '__driver',
    )

    def __init__(self) -> None:
        self.__driver: Redis | None = None

    @property
    def name(self) -> str:
        return 'redis'

    async def load(self, plugins_settings: Mapping[str, Any] | None = None) -> None:
        settings = RedisConfig(**plugins_settings)
        self.__driver = Redis(host=settings.host, port=settings.port)
        ioc.set(Redis, self.__driver)

    async def reload(self) -> None:
        pass

    async def unload(self) -> None:
        await self.__driver.close()
