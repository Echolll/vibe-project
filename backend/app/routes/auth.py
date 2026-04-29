from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.utils.security import hash_password, verify_password, create_token
from backend.app.database import get_db, Users
from backend.app.schemas.users import *

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",
            response_model=UserOut,
            summary="Создать аккаунт",
            description="Создаётся аккаунт на основе имени, почты и хэшируемого пароля")
def register(user_in: UserCreate,
             db: Session = Depends(get_db)):

    existing_username = db.query(Users).filter(Users.username == user_in.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    existing_email = db.query(Users).filter(Users.email == user_in.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с такой почтой уже существует" )


    user = Users(
        username=user_in.username,
        email=user_in.email,
        password_hash=hash_password(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login",
            summary="Вход",
            description= "На выход идёт токен и тип токена"
             )
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == form_data.username).first()

    if not user:
        raise HTTPException(status_code=401,detail="Пользователь с таким логином не найден")
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401,detail="Неверный пароль")

    token = create_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}