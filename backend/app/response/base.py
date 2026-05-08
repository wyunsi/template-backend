from typing import Any

from pydantic import BaseModel


class SuccessResponse[DataT](BaseModel):
    success: bool = True
    data: DataT


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Any = None
