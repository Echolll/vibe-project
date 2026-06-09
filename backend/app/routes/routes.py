from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from backend.app.database import get_db
from backend.app.routes import events,auth, reviews
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database.admin import create_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    create_admin()
    yield
    print("Приложение останавливается...")

app = FastAPI(title="Vibe-project",
              description="Веб-сервис для поиска компании",
              lifespan=lifespan)
app.include_router(events.router)
app.include_router(auth.router)
app.include_router(reviews.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/",summary="Главная страница")
def main_page():
    return {"message":"Главная страница"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("routes:app")

