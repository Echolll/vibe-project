# Документация API Vibe

Базовый URL: `http://localhost:8000` (локально)

Все защищенные эндпоинты требуют заголовок: 
`Authorization: Bearer <access_token>`

---

## Авторизация (Auth)

### 1. `POST /auth/register`
Регистрация нового пользователя.
**Входные параметры (JSON Body - UserCreate):**
- `username` (string, required): От 3 до 50 символов.
- `email` (string, required): Валидный email-адрес.
- `password` (string, required): Минимум 6 символов.

**Успешный ответ (200 OK - UserOut):**
```json
{
  "id": 1,
  "username": "ivan_ivanov",
  "email": "ivan@example.com"
}
```

### 2. `POST /auth/login`
Авторизация пользователя. Обратите внимание: данные передаются как форма, а не JSON!
**Входные параметры (Form Data):**
- `username` (string, required)
- `password` (string, required)

**Успешный ответ (200 OK):**
```json
{
  "access_token": "eyJhbG...",
  "token_type": "bearer"
}
```

---

## Пользователи (Users)

### 1. `GET /users/me`
Получение полного профиля текущего авторизованного пользователя.
**Входные параметры:** Нет (Только Bearer Token)
**Успешный ответ (200 OK - UserFull):**
```json
{
  "id": 1,
  "username": "ivan_ivanov",
  "email": "ivan@example.com",
  "full_name": "Иван Иванов",
  "avatar": "https://example.com/avatars/ivan.png",
  "bio": "Люблю активный отдых!",
  "rating": 4.5,
  "is_active": true,
  "created_at": "2026-05-21T12:00:00"
}
```

### 2. `GET /users/{user_id}`
Получение профиля любого пользователя.
**Path Parameters:**
- `user_id` (int, required): ID пользователя.

**Успешный ответ (200 OK - UserShort):** Возвращает `id`, `username`, `full_name`, `avatar`, `is_active`, `rating`.

### 3. `PATCH /users/{user_id}`
Редактирование профиля.
**Входные параметры (JSON Body - UserUpdate):**
*(Все поля опциональны)*
- `username` (string)
- `email` (string)
- `full_name` (string)
- `avatar` (string)
- `bio` (string)

### 4. `DELETE /users/{user_id}`
Удаление своего аккаунта. Требует обязательного подтверждения паролем.
**Входные параметры (JSON Body - UserDeleteRequest):**
- `password` (string, required)

**Успешный ответ (204 No Content)**

---

## События (Events)

### 1. `GET /events/`
Получение списка всех активных событий.
**Query Parameters:**
- `skip` (int, default=0): Смещение для пагинации.
- `limit` (int, default=100): Количество возвращаемых элементов.

**Успешный ответ (200 OK - List[EventShort]):**
Возвращает массив объектов с полями `id`, `title`, `date`, `status`, `location`, `description`, `creator_id`.

### 2. `POST /events/`
Создание нового события.
**Входные параметры (JSON Body - EventCreate):**
- `title` (string, required): От 3 до 100 символов.
- `description` (string, optional): До 1000 символов.
- `date` (datetime, required): ISO-8601 строка (напр. `2026-04-12T15:00:00`).
- `location` (string, required): От 2 до 200 символов.
- `max_participants` (int, default=10): Число строго больше 0.

**Успешный ответ (200 OK - EventFull):** Возвращает полную информацию о созданном событии (вкл. `id` и `created_at`).

### 3. `GET /events/{event_id}`
Получение полных деталей события.

### 4. `DELETE /events/{event_id}`
Удаление события. Выполняется только создателем `creator_id == current_user_id`.
**Успешный ответ (204 No Content)**

---

## Отзывы (Reviews)

### 1. `POST /reviews/`
Создание нового отзыва организатору.
**Входные параметры (JSON Body - ReviewCreate):**
- `to_user_id` (int, required): ID получателя отзыва.
- `event_id` (int, required): ID мероприятия, после которого оставляется отзыв.
- `rating` (int, required): Оценка строго от 1 до 5.
- `comment` (string, optional): До 1000 символов.

**Успешный ответ (200 OK - ReviewResponse):**
Возвращает созданный отзыв, включая объект `from_user` с краткой информацией о написавшем.
