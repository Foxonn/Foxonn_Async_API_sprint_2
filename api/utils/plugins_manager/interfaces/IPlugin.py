from typing import Any
from typing import Mapping
from typing import Optional

__all__ = ['IPlugin']


class IPlugin:
    __slots__ = ()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    async def load(self, plugins_settings: Optional[Mapping[str, Any]] = None) -> None:
        raise NotImplementedError()

    async def reload(self) -> None:
        raise NotImplementedError()

    async def unload(self) -> None:
        raise NotImplementedError()
