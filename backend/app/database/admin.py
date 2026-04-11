from backend.app.database import Users, SessionLocal
from backend.app.utils.security import hash_password

def create_admin():
    db = SessionLocal()
    try:
        admin = db.query(Users).filter(Users.email == "admin@example.com").first()
        if not admin:
            admin = Users(
                username="admin", #в реальном проекте должен быть скрыт
                email="admin@example.com",
                password_hash=hash_password("123456") #в реальном проекте должен быть скрыт
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()