from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.app.database import get_db
from backend.app.routes import events,auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(events.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main_page():
    return {"message":"Главная страница"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("routes:app")

