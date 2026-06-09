from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

EXAMPLE_USER = {
    "id": 1,
    "username": "ivan_ivanov",
    "email": "ivan@example.com",
    "full_name": "Иван Иванов",
    "avatar": "https://example.com/avatars/ivan.png",
    "bio": "Люблю активный отдых, спорт и новые знакомства!",
    "rating": 4.5,
    "is_active": True,
    "created_at": "2026-05-21T12:00:00",
    "password_hash": "$2b$12$eI7L71XLY4aUt823XZFiHeOMPS5A9FzS..."
}

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "ivan_ivanov",
                "email": "ivan@example.com",
                "password": "secure_password123"
            }
        }
    )

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr


    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {k: EXAMPLE_USER[k] for k in ["id", "username", "email"]}
        }
    )

class UserShort(BaseModel):
    id: int
    username: str
    full_name: str | None = Field(None)
    avatar: str | None = Field(None, description="Ссылка на аватар профиля")
    is_active: bool
    rating: float = Field(0.0)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {k: EXAMPLE_USER[k] for k in ["id", "username", "avatar", "is_active", "rating"]}
        }
    )

class UserFull(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password_hash: str
    full_name: str | None = Field(None, max_length=100)
    avatar: str | None = Field(None)
    bio: str | None = Field(None, max_length=1000)
    rating: float = Field(0.0)
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": EXAMPLE_USER}
    )

class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = Field(None)
    full_name: str | None = Field(None, max_length=100)
    avatar: str | None = Field(None)
    bio: str | None = Field(None, max_length=1000)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "Иван Новый-Иванов",
                "bio": "Немного изменил информацию о себе."
            }
        }
    )

class UserUpdatePassword(BaseModel):
    password: str = Field(..., min_length=6)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "password": "new_secure_password123"
            }
        }
    )

class UserDeleteRequest(BaseModel):
    password: str = Field(..., description="Пароль пользователя для подтверждения удаления")
