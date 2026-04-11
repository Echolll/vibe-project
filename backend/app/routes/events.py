from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import List,Annotated
from sqlalchemy.orm import Session

from backend.app.database import get_db, Events, Users
from backend.app.schemas.events import *
from backend.app.utils.security import get_current_user

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

DbSession = Annotated[Session, Depends(get_db)]

@router.get("/", response_model = List[EventShort],
            summary="Получить список всех событий",
            description="Возвращает краткую информацию о всех мероприятиях."
            )
def get_events(db: DbSession):
    events = db.query(Events).all()
    return events

@router.get("/{event_id}", response_model =  EventFull,
            summary="Получить полную информацию о событии",
            description="Возвращает детальные данные конкретного события по его ID, включая описание и дополнительные поля."
            )
def get_event(db: DbSession,
              event_id: Annotated[int, Path(..., title="ID события", gt=0)],
              ):
    event = db.query(Events).filter(Events.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Событие с id {event_id} не найдено"
        )
    return event

@router.post("/", response_model=EventFull,
             summary="Создать новое событие",
             description="Регистрирует новое событие в системе. На вход ожидается объект `EventCreate`."
             )
def create_event(
    db: DbSession,
    event_in: EventCreate,
    current_user: Users = Depends(get_current_user)
):
    new_event = Events(**event_in.model_dump(), creator_id = current_user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.patch("/{event_id}", response_model=EventFull,
              summary="Частичное обновление события",
              description="Позволяет изменить только выбранные поля события. Если поле не передано в теле запроса, оно останется неизменным."
              )
def update_event(
        db: DbSession,
        event_id: Annotated[int, Path(..., gt=0)],
        event_in: EventUpdate,
        current_user: Users = Depends(get_current_user)

):
    db_event = db.query(Events).filter(Events.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Событие не найдено")

    if db_event.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для редактирования этого события"
        )
    update_data = event_in.model_dump(exclude_unset=True) # Извлекаем только присланные данные
    for key, value in update_data.items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)

    return db_event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить событие",
               description="Безвозвратно удаляет событие из базы данных по его идентификатору."
               )
def delete_event(
    event_id: Annotated[int, Path(..., gt=0)],
    db: DbSession,
    current_user: Users = Depends(get_current_user)
):
    event = db.query(Events).filter(Events.id == event_id).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Событие с id {event_id} не найдено"
        )

    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для удаления этого события"
        )

    db.delete(event)
    db.commit()

    return None
