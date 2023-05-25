from orjson import orjson
from pydantic import BaseModel

__all__ = ['ExtBaseModel']


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ExtBaseModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
