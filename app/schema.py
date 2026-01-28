from typing import Generic, TypeVar
from pydantic import BaseModel, Field, AnyUrl
from datetime import datetime


class RequestDTO(BaseModel):
    url: AnyUrl


class ResponseDTO(BaseModel):
    id: str = Field(max_length=36)
    url: AnyUrl
    short_code: str = Field(min_length=4, max_length=10)
    created_at: datetime
    updated_at: datetime

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    message: str
    data: T

class SuccessMessage(BaseModel):
    message: str