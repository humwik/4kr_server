from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ==========================================
# 🌟 ЗАДАНИЕ 10.2: Модель Pydantic
# ==========================================
class UserCreate(BaseModel):
    username: str
    age: int = Field(gt=18)  # Валидация: возраст строго больше 18
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"