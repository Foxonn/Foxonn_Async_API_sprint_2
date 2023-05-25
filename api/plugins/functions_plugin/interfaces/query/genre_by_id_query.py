from abc import abstractmethod
from typing import Any
from typing import Mapping

__all__ = ['IGenreByIdQuery']


class IGenreByIdQuery:
    __slots__ = ()

    @abstractmethod
    async def __call__(self, id_: str) -> Mapping[str, Any] | None:
        pass
