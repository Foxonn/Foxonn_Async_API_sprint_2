from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import TypeVar

__all__ = ['IGenresQuery']

T = TypeVar("T")


class IGenresQuery(ABC):
    __slots__ = ()

    @abstractmethod
    async def __call__(
        self,
        page_number: int,
        page_size: int,
    ) -> Sequence[Mapping[str, Any] | None]:
        pass
