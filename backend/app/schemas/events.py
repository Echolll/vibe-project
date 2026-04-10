from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class EventShort(BaseModel):
    id: int
    title: str
    date: datetime
    status: str
    model_config = ConfigDict(from_attributes=True)

class EventFull(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    date: datetime
    location: str = Field(..., min_length=2)
    max_participants: int = Field(10, gt=0)
    creator_id: int
    created_at: datetime
    status: str = Field("active")
    model_config = ConfigDict(from_attributes=True)

class EventCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    date: datetime
    location: str = Field(..., min_length=2, max_length=200)
    max_participants: int = Field(10, gt=0)

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    date: Optional[datetime] = None
    location: Optional[str] = Field(None, min_length=2, max_length=200)
    max_participants: Optional[int] = Field(None, gt=0)
    status: Optional[str] = None


