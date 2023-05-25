from typing import Optional

from pydantic import BaseModel

__all__ = [
    'APISearchRequest',
]


class Pagination(BaseModel):
    page_number: int
    page_size: int


class APISearchRequest(BaseModel):
    query: str
    pagination: Optional[Pagination]
