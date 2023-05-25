from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Mapping
from typing import Sequence
from typing import TypeVar

__all__ = ['ISearchPersonsQuery']

T = TypeVar("T")


class ISearchPersonsQuery(ABC):
    __slots__ = ()

    @abstractmethod
    async def __call__(
        self,
        query: str,
        page_number: int | None,
        page_size: int | None,
    ) -> Sequence[Mapping[str, Any] | None]:
        pass
