from abc import abstractmethod
from typing import Any
from typing import Mapping

__all__ = ['IPersonByIdQuery']


class IPersonByIdQuery:
    __slots__ = ()

    @abstractmethod
    async def __call__(self, id_: str) -> Mapping[str, Any] | None:
        pass
