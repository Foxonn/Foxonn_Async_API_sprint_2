from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Mapping
from typing import Sequence
from typing import TypeVar

__all__ = ['IFilmsQuery']

T = TypeVar("T")


class IFilmsQuery(ABC):
    __slots__ = ()

    @abstractmethod
    async def __call__(
        self,
        page_number: int,
        page_size: int,
        sort: str | None = None,
        genre: str | None = None,
    ) -> Sequence[Mapping[str, Any] | None]:
        pass
