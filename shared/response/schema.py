from typing import TypeVar, Optional

from pydantic import BaseModel

T = TypeVar('T')


class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None
