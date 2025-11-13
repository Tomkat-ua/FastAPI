from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Створюємо екземпляр FastAPI
app = FastAPI()

# 2. Визначаємо модель даних для товару (Item) за допомогою Pydantic
# Це забезпечує автоматичну валідацію вхідних JSON-даних
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

# 3. Визначаємо маршрут (Route) за допомогою декоратора
@app.get("/")
def read_root():
    # Повертає JSON-відповідь
    return {"Hello": "World"}

# 4. Маршрут з POST-методом, що приймає Pydantic-модель
@app.post("/items/")
def create_item(item: Item):
    # FastAPI автоматично валідує вхідний JSON на відповідність моделі Item
    return item

# Приклад: Параметр Шляху (Path Parameter)
@app.get("/items/{item_id}")
def read_item(item_id: int):
    # FastAPI автоматично перетворює item_id на ціле число (int)
    return {"item_id": item_id}

# Приклад: Параметр Запиту (Query Parameter)
@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10):
    # skip та limit мають значення за замовчуванням
    return {"skip": skip, "limit": limit}

