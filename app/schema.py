
from pydantic import BaseModel


class Request(BaseModel):
    url: str


class Response(BaseModel):
    id: str
    url: str
    short_code: str
    created_at: str
    updated_at: str