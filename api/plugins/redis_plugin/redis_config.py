from pydantic import BaseModel

__all__ = ['RedisConfig']


class RedisConfig(BaseModel):
    host: str
    port: int
