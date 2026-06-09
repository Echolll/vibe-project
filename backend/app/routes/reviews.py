from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List

from backend.app.utils.security import get_current_user
from backend.app.database import get_db, Reviews
from backend.app.schemas.reviews import ReviewCreate, ReviewResponse, UserRatingResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post(
    "/",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать отзыв и оценку",
    description=(
        "Позволяет текущему авторизованному пользователю оставить отзыв и оценку другому участнику в контексте конкретного мероприятия. "
        "Бизнес-правило: пользователь не может оценить сам себя."
    )
)
def create_review(
        review_data: ReviewCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    if current_user.id == review_data.to_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы не можете поставить оценку самому себе."
        )
        
    existing_review = db.query(Reviews).filter(
        Reviews.from_user_id == current_user.id,
        Reviews.to_user_id == review_data.to_user_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Вы уже оставляли отзыв этому пользователю."
        )

    db_review = Reviews(
        from_user_id=current_user.id,  # Берем из токена авторизации
        to_user_id=review_data.to_user_id,
        event_id=review_data.event_id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get(
    "/user/{user_id}",
    response_model=List[ReviewResponse],
    summary="Получить список отзывов о пользователе",
    description="Возвращает массив всех когда-либо оставленных текстовых отзывов и оценок НА конкретного пользователя."
)
def get_user_reviews(user_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Reviews).options(joinedload(Reviews.from_user)).filter(Reviews.to_user_id == user_id).all()
    return reviews


@router.get(
    "/user/{user_id}/rating",
    response_model=UserRatingResponse,
    summary="Получить агрегированный рейтинг пользователя",
    description=(
        "Рассчитывает в реальном времени среднее арифметическое всех оценок пользователя и считает общее количество отзывов. Используется для вывода счётчика в профиле."
    )
)
def get_user_profile_rating(user_id: int, db: Session = Depends(get_db)):
    # Делаем один запрос в БД, который сразу считает среднее и сумму
    result = db.query(
        func.avg(Reviews.rating).label("avg_rating"),
        func.count(Reviews.id).label("count_reviews")
    ).filter(Reviews.to_user_id == user_id).first()

    # Если отзывов нет, func.avg вернет None. Заменяем его на 0.0
    avg_rating = round(result.avg_rating, 2) if result.avg_rating else 0.0
    reviews_count = result.count_reviews or 0

    return UserRatingResponse(
        user_id=user_id,
        average_rating=avg_rating,
        reviews_count=reviews_count
    )