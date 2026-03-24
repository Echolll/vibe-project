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

#Error 500: When initializing mapper Mapper[Users(users)], expression 'Review.from_user_id' failed to locate a name ("name 'Review' is not defined")
#If this is a class name, consider adding this relationship() to the <class 'backend.app.database.user.Users'> class after both dependent classes have been defined.

