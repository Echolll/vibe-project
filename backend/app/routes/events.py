from fastapi import APIRouter, Depends, Path, Query,HTTPException, status
from typing import List,Annotated
from sqlalchemy.orm import Session

from backend.app.database import get_db, Events, Users, Participants
from backend.app.schemas.events import *
from backend.app.schemas.participants import *
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


@router.post("/{event_id}/join", status_code=status.HTTP_201_CREATED, response_model=ParticipantRead,
             summary="Присоединиться к событию",
             description="Создаёт объект класса Participants с статусом pending")
def join_event(
        db: DbSession,
        event_id: Annotated[int, Path(..., gt=0)],
        current_user: Users = Depends(get_current_user)
):
    # Проверяем, существует ли событие
    event = db.query(Events).filter(Events.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Событие не найдено")

    # Организатор не может вступить в свое же событие
    if event.creator_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вы являетесь организатором этого события")

    # Проверяем, нет ли уже такой заявки (дубликат)
    existing = db.query(Participants).filter(
        Participants.event_id == event_id,
        Participants.user_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Вы уже подали заявку или участвуете в этом событии")

    # Проверяем лимит мест (считаем только подтвержденных участников 'accepted')
    if event.max_participants is not None:
        current_participants_count = db.query(Participants).filter(
            Participants.event_id == event_id,
            Participants.status == "accepted"
        ).count()
        if current_participants_count >= event.max_participants:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Мест больше нет")

    # Создаем заявку
    new_participant = Participants(
        user_id=current_user.id,
        event_id=event_id,
        status="pending"  # По умолчанию статус ожидания
    )
    db.add(new_participant)
    db.commit()
    db.refresh(new_participant)

    return new_participant


@router.get("/{event_id}/participants", response_model= List[ParticipantRead],
            summary="Список заявок на участие (для организатора)")
def get_join_requests(
        event_id: Annotated[int, Path(..., gt=0)],
        db: DbSession,
        current_user: Users = Depends(get_current_user)
):
    # Проверяем, что событие существует и юзер — его создатель
    event = db.query(Events).filter(Events.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Событие не найдено")

    if event.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только организатор видит заявки")

    # Получаем все заявки для этого события
    requests = db.query(Participants).filter(
        Participants.event_id == event_id
    ).order_by(Participants.joined_at.asc()).all()  # Сортируем: кто раньше пришел — тот первый в списке

    return requests

@router.patch("/{event_id}/participants/{participant_id}",
              summary="Управление заявкой на участие",
              description="Организатор либо принимает (accepted) , либо нет (rejected) ")
def manage_join_request(
        db: DbSession,
        event_id: Annotated[int, Path(..., gt=0)],
        participant_id: int,
        new_status: Annotated[str, Query(pattern="^(accepted|rejected)$")],  # Ожидается "accepted" или "rejected"
        current_user: Users = Depends(get_current_user)
):

    # Проверяем, существует ли событие (404)
    event = db.query(Events).filter(Events.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие не найдено"
        )

    # Проверяем права доступа
    if event.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав на управление этим событием"
        )

    # Ищем заявку
    participant_request = db.query(Participants).filter(
        Participants.id == participant_id,
        Participants.event_id == event_id
    ).first()

    if not participant_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена")

    # Проверка лимита при одобрении
    if new_status == "accepted" and participant_request.status != "accepted":
        if event.max_participants is not None:
            current_count = db.query(Participants).filter(
                Participants.event_id == event_id,
                Participants.status == "accepted"
            ).count()

            if current_count >= event.max_participants:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Невозможно одобрить: лимит мест исчерпан"
                )

    #Обновляем статус
    participant_request.status = new_status
    db.commit()

    return {"message": f"Статус заявки изменен на {new_status}"}

@router.delete("/{event_id}/join",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Отменить заявку или покинуть событие",
               description="Удаляет запись пользователя из списка участников события.")
def leave_event(
    event_id: Annotated[int, Path(..., gt=0)],
    db: DbSession,
    current_user: Users = Depends(get_current_user)
):
    # Проверяем, существует ли само событие
    event = db.query(Events).filter(Events.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие не найдено"
        )

    # Ищем запись о его участии
    participation = db.query(Participants).filter(
        Participants.event_id == event_id,
        Participants.user_id == current_user.id
    ).first()

    # Если записи нет — значит он и так не участвовал (404)
    if not participation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вы не являетесь участником этого события или ваша заявка не найдена"
        )

    # Удаляем запись
    db.delete(participation)
    db.commit()

    return None