# To-Do FastAPI

Менеджер задач на FastAPI

## Стек

- **Backend**: FastAPI, SQLAlchemy, Alembic
- **БД**: PostgreSQL 16
- **Кэш**: Redis 7
- **Аутентификация**: JWT (cookies)
- **Контейнеризация**: Docker Compose

## API эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/registration/register/` | Регистрация |
| POST | `/registration/login/` | Авторизация |
| POST | `/registration/logout/` | Выход |
| GET | `/users/` | Список пользователей |
| GET | `/users/{id}` | Пользователь по ID |
| POST | `/users/add/` | Добавить пользователя |
| GET | `/tasks/` | Задачи текущего пользователя |
| POST | `/tasks/add/` | Добавить задачу |
| PUT | `/tasks/update/{id}` | Обновить задачу |
| DELETE | `/tasks/delete/{id}` | Удалить задачу |

## Запуск

```bash
docker compose up --build
```

- Backend: `http://0.0.0.0:8000`
- Swagger UI: `http://0.0.0.0:8000/docs`


## Тесты

```bash
cd to_do/backend
pytest
```