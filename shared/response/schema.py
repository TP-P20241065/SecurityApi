from typing import TypeVar, Optional, Generic

from pydantic import BaseModel

T = TypeVar('T')


class ResponseSchema(BaseModel, Generic[T]):
    detail: str
    result: Optional[T] = None
