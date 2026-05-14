import pytest
from httpx import AsyncClient, ASGITransport
from main import app, db_users
from faker import Faker

fake = Faker()

# ==========================================
# 🌟 ЗАДАНИЯ 11.1 и 11.2: Модульные асинхронные тесты
# ==========================================

@pytest.fixture(autouse=True)
def clean_db():
    """Изоляция состояния: очищаем in-memory БД перед каждым тестом"""
    db_users.clear()

@pytest.mark.asyncio
async def test_create_user():
    """Тест: успешное создание пользователя (201)"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        payload = {
            "username": fake.user_name(),
            "age": fake.random_int(min=19, max=60), # Валидация age > 18
            "email": fake.email(),
            "password": fake.password(length=12)
        }
        response = await ac.post("/users", json=payload)
    
    assert response.status_code == 201
    assert response.json()["username"] == payload["username"]

@pytest.mark.asyncio
async def test_get_existing_user():
    """Тест: получение существующего пользователя (200)"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Сначала создаем
        payload = {"username": "testuser", "age": 25, "email": "test@test.com", "password": "password123"}
        post_response = await ac.post("/users", json=payload)
        user_id = post_response.json()["id"]
        
        # Затем получаем
        get_response = await ac.get(f"/users/{user_id}")
        
    assert get_response.status_code == 200
    assert get_response.json()["id"] == user_id

@pytest.mark.asyncio
async def test_get_non_existent_user():
    """Тест: попытка получить несуществующего пользователя (404 / CustomExceptionB)"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/users/999")
        
    assert response.status_code == 404
    assert "error_type" in response.json() # Проверяем, что сработал кастомный хендлер

@pytest.mark.asyncio
async def test_delete_user():
    """Тест: удаление пользователя (204) и повторное удаление (404)"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Создаем
        payload = {"username": "deluser", "age": 30, "email": "del@test.com", "password": "password123"}
        post_res = await ac.post("/users", json=payload)
        user_id = post_res.json()["id"]
        
        # Удаляем (Успех)
        del_res = await ac.delete(f"/users/{user_id}")
        assert del_res.status_code == 204
        
        # Удаляем повторно (Ошибка)
        del_res_again = await ac.delete(f"/users/{user_id}")
        assert del_res_again.status_code == 404