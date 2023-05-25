import functools
import hashlib
from typing import Callable, Optional

from redis.asyncio.client import Redis
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from api.utils.ioc import IOC

__all__ = ['RedisCacheFastApiMiddleware']


@functools.lru_cache(maxsize=999)
def to_hash_string(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest()


class RedisCacheFastApiMiddleware(BaseHTTPMiddleware):
    __slots__ = (
        '_redis',
        '_cache_expiration',
    )

    def __init__(self, app: Starlette, ioc: IOC, cache_expiration: Optional[int] = 60) -> None:
        super().__init__(app)
        self._ioc = ioc
        self._cache_expiration = cache_expiration

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        redis = await self._ioc.get(Redis)
        response = await call_next(request)
        response_body = b""
        headers = dict(response.headers)

        if cache := await redis.get(to_hash_string(str(request.url))):
            response_body = cache
            headers.update({'Cache-Control': f'max-age={self._cache_expiration}'})
        else:
            async for chunk in response.body_iterator:
                response_body += chunk
            await redis.set(
                name=to_hash_string(str(request.url)),
                value=response_body,
                ex=self._cache_expiration,
            )

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=headers,
            media_type=response.media_type,
        )
