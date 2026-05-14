from sqlalchemy import Column, Integer, String, Float
from database import Base

# ==========================================
# 🌟 ЗАДАНИЕ 9.1: Модель данных Product
# ==========================================
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    count = Column(Integer)
    

    description = Column(String, nullable=False)