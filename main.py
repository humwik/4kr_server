from fastapi import FastAPI, HTTPException, Response
from schemas import UserCreate
from exceptions import register_custom_exceptions, CustomExceptionA, CustomExceptionB
from itertools import count

# Инициализация приложения
app = FastAPI(title="Контрольная работа №4")

# 🌟 ЗАДАНИЕ 10.1: Регистрация обработчиков кастомных исключений
register_custom_exceptions(app)

# Имитация базы данных в оперативной памяти (для заданий 11.1 и 11.2)
db_users = {}
_id_seq = count(start=1)

# ==========================================
# ЭНДПОИНТЫ (Задания 10.2, 11.1, 11.2)
# ==========================================

@app.post("/users", status_code=201)
async def create_user(user: UserCreate):
    """
    Создание пользователя. 
    Здесь автоматически срабатывает валидация Pydantic из Задания 10.2
    """
    user_id = next(_id_seq)
    user_data = user.model_dump()
    db_users[user_id] = user_data
    return {"id": user_id, **user_data}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    Получение пользователя.
    Вызывает CustomExceptionB (404), если ID не найден (Задание 10.1)
    """
    if user_id not in db_users:
        raise CustomExceptionB(message=f"Пользователь с ID {user_id} не найден")
    return {"id": user_id, **db_users[user_id]}

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    """Удаление пользователя (Задание 11.1)"""
    if db_users.pop(user_id, None) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)

# ==========================================
# ТЕСТОВАЯ РУЧКА (Задание 10.1)
# ==========================================
@app.get("/trigger-error")
async def trigger_error_a():
    """Эндпоинт для проверки CustomExceptionA"""
    raise CustomExceptionA(message="Тестовая ошибка типа А")