from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


EXAMPLE_EVENT = {
    "id": 101,
    "title": "Пример: Каток",
    "description": "Хотим сходить в Парк Горького. Уровень катания любой!",
    "date": "2026-04-12T15:00:00",
    "location": "Парк Горького, главный вход",
    "max_participants": 6,
    "creator_id": 77,
    "created_at": "2026-04-04T10:30:00",
    "status": "active",
    "confirmed_participants_count": 5
}

class EventShort(BaseModel):
    id: int
    title: str
    date: datetime
    status: str
    location: str | None = None
    description: str | None = None
    creator_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {k: EXAMPLE_EVENT[k] for k in ["id", "title", "date", "status", "location", "description", "creator_id"]}
        }
    )

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
    confirmed_participants_count: int = 0

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": EXAMPLE_EVENT}
    )

class EventCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    date: datetime
    location: str = Field(..., min_length=2, max_length=200)
    max_participants: int = Field(10, gt=0)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {k: EXAMPLE_EVENT[k] for k in ["title", "description", "date", "location", "max_participants", "creator_id"]}
        }
    )
class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    date: Optional[datetime] = Field(None)
    location: Optional[str] = Field(None, min_length=2, max_length=200)
    max_participants: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(None)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Test: Обновленное название (Каток)",
                "status": "active"
            }
        }
    )