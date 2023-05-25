from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Mapping
from typing import TypeVar

__all__ = ['IEntityByIdQuery']

T = TypeVar("T")


class IEntityByIdQuery(ABC):
    __slots__ = ()

    @abstractmethod
    async def __call__(self, index: str, id_: str) -> Mapping[str, Any] | None:
        pass
