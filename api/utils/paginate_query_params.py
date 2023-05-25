from fastapi.params import Query

__all__ = ['PaginateQueryParams']


class PaginateQueryParams:
    def __init__(
            self,
            page_number: int = Query(
                1,
                title="Page number.",
                description="Page number to return",
                ge=1,
            ),
            page_size: int = Query(
                25,
                title="Size of page.",
                description="The number of records returned per page",
                ge=1,
                le=75,
            ),
    ):
        self.page_number = page_number
        self.page_size = page_size
