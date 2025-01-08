from pydantic import BaseModel
from typing import Any

class BaseResponse(BaseModel):
    status: str
    message: str
    data: Any
