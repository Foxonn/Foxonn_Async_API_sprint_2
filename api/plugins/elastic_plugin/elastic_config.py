from pydantic import BaseModel

__all__ = ['ElasticConfig']


class ElasticConfig(BaseModel):
    host: str
    port: int
