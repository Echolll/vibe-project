from fastapi import APIRouter, Depends, Path, HTTPException, status
from typing import List,Annotated
from sqlalchemy.orm import Session
from backend.app.database import get_db, Events
from backend.app.schemas.events import *


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

DbSession = Annotated[Session, Depends(get_db)]

@router.get("/", response_model = List[EventShort])
def get_events(db: DbSession):
    events = db.query(Events.title,
                      Events.date,
                      Events.status).all()
    return events

@router.get("/{event_id}", response_model =  EventFull)
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

@router.post("/", response_model=EventFull)
def create_event(
    db: DbSession,
    event_in: EventCreate ):
    new_event = Events(
        title=event_in.title,
        description=event_in.description,
        date=event_in.date,
        location=event_in.location,
        max_participants=event_in.max_participants,
        creator_id=event_in.creator_id, #надо будет сделать, чтобы автоматически вводилось
        status="active"
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


@router.patch("/{event_id}", response_model=EventFull)
def update_event(
        db: DbSession,
        event_id: Annotated[int, Path(..., gt=0)],
        event_in: EventUpdate,

):
    db_event = db.query(Events).filter(Events.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    # Извлекаем только присланные данные
    update_data = event_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)

    db.commit()
    db.refresh(db_event)

    return db_event



@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: Annotated[int, Path(..., gt=0)],
    db: DbSession
):
    event = db.query(Events).filter(Events.id == event_id).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Событие с id {event_id} не найдено"
        )

    db.delete(event)
    db.commit()

    return None