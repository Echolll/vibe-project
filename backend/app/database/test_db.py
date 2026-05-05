from database import SessionLocal
from backend.app.database.user import Users
from backend.app.database.event import Events
from backend.app.database.participant import Participants
from backend.app.database.review import Reviews
from passlib.context import CryptContext
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def seed_users():
    db = SessionLocal()

    try:
        users_data = [
            {
                "username": "Random",
                "email": "someemail@.gmail.com",
                "password": "2345",
                "full_name": "Smirnov Oleg",
                "avatar": "ava.png",
                "bio": "cool user",
                "rating": 4.6,
                "is_active": 1,
                "created_at": datetime(2026, 1, 12, 15, 31, 9)
            },
            {
                "username": "Wow",
                "email": "anyemail@.gmail.com",
                "password": "554",
                "full_name": "Nesterenko Alica",
                "avatar": "ava.png",
                "bio": "i like dogs",
                "rating": 3.7,
                "is_active": 1,
                "created_at": datetime(2026, 2, 16, 10, 44, 29)
            },
            {
                "username": "Arina",
                "email": "ariknefed@.gmail.com",
                "password": "532",
                "full_name": "Nefedova Arina",
                "avatar": "ava.png",
                "bio": "smile",
                "rating": 4.9,
                "is_active": 1,
                "created_at": datetime(2026, 1, 8, 20, 32, 30)
            },
            {
                "username": "UserBeaver",
                "email": "coolemail@.gmail.com",
                "password": "532",
                "full_name": "Zaharov Ivan",
                "avatar": "ava.png",
                "bio": "beavers are cool",
                "rating": 5,
                "is_active": 1,
                "created_at": datetime(2026, 1, 9, 18, 0, 5)
            },
            {
                "username": "SerSid",
                "email": "sergey@.gmail.com",
                "password": "4r2",
                "full_name": "Sidorov Sergey",
                "avatar": "ava.png",
                "bio": "no bio",
                "rating": 3.1,
                "is_active": 1,
                "created_at": datetime(2026, 1, 1, 17, 34, 56)
            }
        ]

        for user_data in users_data:
            user = Users(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=hash_password(user_data["password"]),
                full_name=user_data["full_name"],
                avatar=user_data["avatar"],
                bio=user_data["bio"],
                rating=user_data["rating"],
                is_active=user_data["is_active"],
                created_at=user_data["created_at"]
            )
            db.add(user)
            print(f" Добавлен пользователь: {user_data['username']}")

        db.commit()
        print("\n Пользователи успешно добавлены!")

    # except Exception as e:
    #     db.rollback()
    #     print(f" Ошибка при добавлении пользователей: {e}")

    finally:
        db.close()

def seed_events():
    db = SessionLocal()
    try:
        events_data = [
            {
                "title": "Walk",
                "description": "Walking through the city for fun",
                "date": datetime(2026, 2, 28, 14, 0, 0),
                "location": "Central Street",
                "max_participants": 5,
                "creator_id": 3,
                "created_at": datetime(2026, 2, 26, 14, 1, 19),
                "status": "completed"
            },
            {
                "title": "Cafe",
                "description": "Spending time in cafe",
                "date": datetime(2026, 3, 1, 16, 0, 0),
                "location": "West Street Cafe",
                "max_participants": 5,
                "creator_id": 3,
                "created_at": datetime(2026, 2, 28, 16, 13, 21),
                "status": "completed"
            },
            {
                "title": "UNO",
                "description": "Playing Uno in the park",
                "date": datetime(2026, 3, 3, 10, 0, 0),
                "location": "Central Park",
                "max_participants": 3,
                "creator_id": 3,
                "created_at": datetime(2026, 2, 11, 19, 59, 59),
                "status": "completed"
            },
            {
                "title": "Museum",
                "description": "Visiting Car Museum",
                "date": datetime(2026, 3, 12, 14, 0, 0),
                "location": "Car Museum",
                "max_participants": 5,
                "creator_id": 3,
                "created_at": datetime(2026, 3, 7, 20, 14, 59),
                "status": "completed"
            },
            {
                "title": "Math",
                "description": "Helping with math homework",
                "date": datetime(2026, 3, 1, 13, 0, 0),
                "location": "East Street 8",
                "max_participants": 2,
                "creator_id": 2,
                "created_at": datetime(2026, 2, 28, 10, 24, 35),
                "status": "completed"
            }
        ]

        for event_data in events_data:
            event = Events(
                title=event_data["title"],
                description=event_data["description"],
                date=event_data["date"],
                location=event_data["location"],
                max_participants=event_data["max_participants"],
                creator_id=event_data["creator_id"],
                created_at=event_data["created_at"],
                status=event_data["status"],
            )
            db.add(event)
            print(f"Добавлено событие: {event_data['title']}")

        db.commit()
        print("\n События успешно добавлены!")

    # except Exception as e:
    #     db.rollback()
    #     print(f" Ошибка при добавлении событий: {e}")

    finally:
        db.close()

if __name__ == "__main__":
    print(" Начинаем заполнение базы данных...")
    seed_users()
    seed_events()