from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PageResponse[DataT](BaseModel):
    items: list[DataT]
    total: int
    page: int
    page_size: int
    has_next: bool
