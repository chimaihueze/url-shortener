from pydantic import BaseModel, Field, AnyUrl
from datetime import datetime


class Request(BaseModel):
    url: AnyUrl


class Response(BaseModel):
    id: str = Field(max_length=36)
    url: AnyUrl
    short_code: str = Field(min_length=4, max_length=10)
    created_at: datetime
    updated_at: datetime
