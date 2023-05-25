import functools
import hashlib
import json
from typing import Awaitable
from typing import Callable

from pydantic import BaseModel
from redis.asyncio.client import Redis

__all__ = ['redis_model_cache']


@functools.lru_cache(maxsize=999)
def to_hash_string(value: str) -> str:
    return hashlib.md5(value.encode()).hexdigest()


def redis_model_cache(redis: Redis, expiration_time: int) -> Callable:
    def inner_func(func: Callable[[str], Awaitable[BaseModel]]) -> Callable:
        @functools.wraps(func)
        async def wrapper_redis_cache(*args, **kwargs):
            key = to_hash_string(value=json.dumps(kwargs))
            if data := await redis.get(name=key):
                return json.loads(data)
            else:
                result = await func(*args, **kwargs)
                await redis.set(name=key, value=json.dumps(result), ex=expiration_time)
                return result

        return wrapper_redis_cache

    return inner_func
