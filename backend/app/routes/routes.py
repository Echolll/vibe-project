from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.routes import events

app = FastAPI()
app.include_router(events.router)

@app.get("/")
def main_page():
    return {"message":"Главная страница"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("routes:app")

