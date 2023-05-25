from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import TypeVar

__all__ = ['ISearchFilmsQuery']

T = TypeVar("T")


class ISearchFilmsQuery(ABC):
    __slots__ = ()

    @abstractmethod
    async def __call__(
        self,
        query: str,
        page_number: Optional[int],
        page_size: Optional[int],
    ) -> Sequence[Mapping[str, Any] | None]:
        pass
