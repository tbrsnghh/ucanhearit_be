from pydantic import BaseModel
from typing import Any, Optional, List


class BaseResponse(BaseModel):
    status: str
    message: str
    data: Any


# Request schema for creating an audio file
class AudioCreate(BaseModel):
    name: str
    description: Optional[str]


# Response schema for a single audio file
class AudioData(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True


# Paginated response for multiple audio files
class AudioListData(BaseModel):
    total: int
    items: List[AudioData]
