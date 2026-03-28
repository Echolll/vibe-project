from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db, Events

app = FastAPI()


@app.get("/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Events.title,
                      Events.date,
                      Events.status).all()
    return events



