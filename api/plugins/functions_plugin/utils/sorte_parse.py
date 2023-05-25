from typing import Any
from typing import Mapping

__all__ = ['sort_parse']


def sort_parse(sort_field: str) -> Mapping[str, Any]:
    field = sort_field[1:] if sort_field[0] == '-' else sort_field

    query = {
        field: {
            'order': 'asc' if sort_field[0] == '-' else 'desc'
        }
    }
    return query
