# Vibe — Платформа для поиска компании

## 📋 Описание
Веб-сервис для поиска компании на совместный досуг: походы, кино, настолки, путешествия. Главная фишка — безопасность через рейтинги и отзывы.

## 🚀 Функционал
- Регистрация и авторизация
- Создание и просмотр событий
- Запись на события
- Профили с рейтингом
- Отзывы после встреч
- Чат участников

## 🛠 Стек технологий
- **Python 3.10+** / **FastAPI** / **SQLite** / **SQLAlchemy**
- **HTML** / **CSS** / **Bootstrap** / **Jinja2**
- **Git** / **Pytest** / **GitHub Actions**

## 👥 Команда
| Роль | Участник |
|------|----------|
| TeamLead / DevOps | @username |
| Backend #1 | @username |
| Backend #2 | @username |
| Frontend #1 | @username |
| Frontend #2 | @username |

## 📦 Установка и запуск

### Требования
- Python 3.10 или выше
- Git

### Инструкция
```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/vibe-project.git
cd vibe-project

# Создать виртуальное окружение
python -m venv venv
# Активировать:
# на Windows:
venv\Scripts\activate
# на Mac/Linux:
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn app.main:app --reload
