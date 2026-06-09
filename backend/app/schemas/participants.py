from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


#  Краткая информация о пользователе (чтобы организатор видел, кто подал заявку)
class UserShortInfo(BaseModel):
    id: int
    username: str
    rating: float
    email: Optional[str] = None
    full_name: Optional[str] = None
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


#  Основная схема для чтения данных о заявке
class ParticipantRead(BaseModel):
    id: int
    user_id: int
    event_id: int
    status: str = Field(..., description="Текущий статус: pending, accepted или rejected")
    joined_at: datetime

    # Вложенная информация о пользователе (связь relationship из модели)
    user: UserShortInfo

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 77,
                "event_id": 101,
                "status": "pending",
                "joined_at": "2026-04-12T15:30:00",
                "user": {
                    "id": 77,
                    "username": "ivan_ivanov",
                    "rating" : 5.0,
                    "email": "ivan@example.com"
                }
            }
        }
    )


