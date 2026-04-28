from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

from backend.app.database import get_db,Users
from backend.app.utils.security import oauth2_scheme, SECRET_KEY, ALGORITHM

def get_current_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Невалидный токен")
    except JWTError:
        raise HTTPException(status_code=401, detail="Токен просрочен или изменен")

    user = db.query(Users).filter(Users.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user