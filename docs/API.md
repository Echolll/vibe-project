# Документация API Vibe

Базовый URL: `http://localhost:8000` (локально)

Все защищенные эндпоинты требуют заголовок: `Authorization: Bearer <token>`

---

## Авторизация (Auth)

### 1. `POST /auth/register`
Регистрация нового пользователя.
- **Body (JSON):**
  ```json
  {
    "username": "user123",
    "email": "user@test.com",
    "password": "securepassword",
    "full_name": "Иван Иванов"
  }
  ```
- **Response (200 OK):** Возвращает объект созданного пользователя (без пароля).

### 2. `POST /auth/login`
Авторизация пользователя и получение токена.
- **Body (Form Data):** `username` и `password`.
- **Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbG...",
    "token_type": "bearer"
  }
  ```

---

## Пользователи (Users)

### 1. `GET /users/me`
Получение профиля текущего (авторизованного) пользователя.
- **Response (200 OK):** Данные пользователя.

### 2. `GET /users/{user_id}`
Получение профиля любого пользователя по ID.
- **Response (200 OK):** Данные пользователя + рассчитанный `rating`.

### 3. `PATCH /users/{user_id}`
Редактирование своего профиля (био, имя, аватар).
- **Body (JSON):** Поля для обновления (опционально).

### 4. `DELETE /users/{user_id}`
Безопасное удаление своего аккаунта. Требует подтверждения паролем!
- **Body (JSON):** `{"password": "mycurrentpassword"}`
- **Response (204 No Content)**: Аккаунт и все связанные с ним события, заявки и отзывы удалены каскадно.

---

## События (Events)

### 1. `GET /events/`
Получение списка всех активных событий.
- **Query Params:** `skip` (int), `limit` (int).

### 2. `POST /events/`
Создание нового события (только для авторизованных).
- **Body (JSON):** `title`, `description`, `date`, `location`, `max_participants`.

### 3. `GET /events/{event_id}`
Получение деталей конкретного события (включая информацию об организаторе и участниках).

### 4. `DELETE /events/{event_id}`
Удаление события. Доступно только создателю события.
- **Response (204 No Content):** Событие удалено, все участники и отзывы отвязаны.

### 5. `POST /events/{event_id}/join`
Подать заявку на участие в событии.
- **Response (200 OK):** Статус заявки `pending`.

### 6. `DELETE /events/{event_id}/leave`
Отменить свою заявку или покинуть событие.

---

## Управление участниками (Participants)

Эндпоинты доступны только создателю (организатору) события.

### 1. `GET /events/{event_id}/participants`
Получить список всех заявок (pending, accepted, rejected) на событие.

### 2. `PATCH /participants/{participant_id}/status`
Одобрить или отклонить заявку пользователя.
- **Query Param:** `status` (`accepted` или `rejected`).

---

## Отзывы (Reviews)

### 1. `POST /reviews/`
Оставить отзыв организатору после события.
- **Body (JSON):**
  ```json
  {
    "to_user_id": 2,
    "event_id": 5,
    "rating": 5,
    "comment": "Всё было супер!"
  }
  ```

### 2. `GET /users/{user_id}/reviews`
Получить все отзывы, оставленные указанному пользователю.
