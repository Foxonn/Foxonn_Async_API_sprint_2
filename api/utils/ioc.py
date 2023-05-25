from typing import Type
from typing import TypeVar

from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_fixed

__all__ = [
    'IOC',
    'ioc',
]

T = TypeVar("T")


class IOC:
    __slots__ = (
        '__store',
    )

    def __init__(self) -> None:
        self.__store = dict()

    def set(self, key: Type[T], value: T) -> None:
        self.__store[key] = value

    async def get(self, key: Type[T]) -> T | None:
        @retry(
            retry=retry_if_exception_type(KeyError),
            wait=wait_fixed(1),
            stop=stop_after_attempt(30)
        )
        def _() -> T | None:
            return self.__store[key]

        return _()


ioc = IOC()
