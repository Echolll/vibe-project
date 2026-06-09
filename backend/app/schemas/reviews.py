from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ReviewCreate(BaseModel):
    to_user_id: int = Field(..., description="ID получателя отзыва")
    event_id: int = Field(..., description="ID мероприятия")
    rating: int = Field(..., ge=1, le=5, description="Оценка от 1 до 5")
    comment: str | None = Field(None, max_length=1000, description="Опциональный комментарий")


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Для работы с объектами SQLAlchemy

    id: int
    from_user_id: int
    to_user_id: int
    event_id: int
    rating: int
    comment: str | None = Field(None)
    created_at: datetime

class UserRatingResponse(BaseModel):
    user_id: int
    average_rating: float = Field(0.0, description="Средний рейтинг")
    reviews_count: int = Field(0, description="Количество полученных оценок")