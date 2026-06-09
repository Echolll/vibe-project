from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import List,Annotated
from sqlalchemy.orm import Session

from backend.app.database import get_db, Events, Users, Participants, Reviews
from backend.app.schemas.users import *
from backend.app.schemas.events import *
from backend.app.utils.security import get_current_user, hash_password, verify_password

router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

DbSession = Annotated[Session, Depends(get_db)]

@router.get('/me', response_model = UserFull,
            summary = 'Получение текущего пользователя',
            description = 'Возвращает полную информацию о пользователе')
def get_user_me(current_user: Users = Depends(get_current_user)):
    return current_user

@router.get("/me/events", response_model = List[EventShort],
            summary = "Получить список всех событий текущего пользователя",
            description = "Возвращает краткую информацию о всех мероприятиях, созданных текущим пользователем"
            )
def get_my_events(db: DbSession,
                  current_user: Users = Depends(get_current_user)):
    events = current_user.created_events
    # if not events:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail=f"Ваши события не найдены"
    #     )
    return events

@router.get('/{user_id}', response_model = UserShort,
            summary = 'Получение частичной информации о пользователе',
            description = 'Возвращает id, username, avatar, is_active и rating')
def get_user(db: DbSession,
             user_id: Annotated[int, Path(..., title = "ID пользователя", gt=0)]):
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь с id {user_id} не найден"
        )
    return user

@router.patch("/{user_id}", response_model = UserFull,
              summary = "Частичное обновление пользователя",
              description = "Позволяет изменить только выбранные поля пользователя. Если поле не передано в теле запроса, оно останется неизменным."
              )
def update_user(
        db: DbSession,
        user_id: Annotated[int, Path(..., gt=0)],
        user_in: UserUpdate,
        current_user: Users = Depends(get_current_user)
):
    # db_user = db.query(Users).filter(Users.id == user_id).first()
    # if not db_user:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Пользователь не найден")
    if user_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Вы не можете изменить данные другого пользователя"
        )
    update_data = user_in.model_dump(exclude_unset=True)
    if "password" in update_data:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Используйте отдельный эндпоинт для смены пароля")
    for key, value in update_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.patch("/{user_id}/password", response_model = UserFull,
              summary = "Изменение пользовательского пароля",
              description = "Позволяет изменить пароль пользователя"
              )
def update_user_password(
    db: DbSession,
    user_id: Annotated[int, Path(..., gt=0)],
    user_in: UserUpdatePassword,
    current_user: Users = Depends(get_current_user)
):
    # db_user = db.query(Users).filter(Users.id == user_id).first()
    # if not db_user:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Пользователь не найден")
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете изменить данные другого пользователя"
        )
    current_user.password_hash = hash_password(user_in.password)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary = "Удалить пользователя",
               description = "Безвозвратно удаляет пользователя из базы данных по его идентификатору."
               )
def delete_user(
    db: DbSession,
    user_id: Annotated[int, Path(..., gt=0)],
    request: UserDeleteRequest,
    current_user: Users = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "У вас нет прав для удаления этого пользователя"
        )
    
    if not verify_password(request.password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Неверный пароль"
        )

    # Каскадное удаление всех связанных данных пользователя
    user_events = db.query(Events).filter(Events.creator_id == current_user.id).all()
    for ev in user_events:
        db.query(Participants).filter(Participants.event_id == ev.id).delete(synchronize_session=False)
        db.query(Reviews).filter(Reviews.event_id == ev.id).delete(synchronize_session=False)
        db.delete(ev)
        
    db.query(Participants).filter(Participants.user_id == current_user.id).delete(synchronize_session=False)
    db.query(Reviews).filter((Reviews.from_user_id == current_user.id) | (Reviews.to_user_id == current_user.id)).delete(synchronize_session=False)

    db.delete(current_user)
    db.commit()
    return None

@router.get("/{user_id}/events", response_model = List[EventShort],
            summary = "Получить список всех событий пользователя по id",
            description = "Возвращает краткую информацию о всех мероприятиях, созданных пользователем с указанным id"
            )
def get_events_user(db: DbSession,
               user_id: Annotated[int, Path(..., gt=0)]):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Пользователь с id {user_id} не найден"
        )
    events = db.query(Events).filter(Events.creator_id == user_id).all()
    # if not events:
    #     raise HTTPException(
    #         status_code = status.HTTP_404_NOT_FOUND,
    #         detail = f"События пользователя с id {user_id} не найдены"
    #     )
    return events

