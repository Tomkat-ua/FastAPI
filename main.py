from fastapi import FastAPI,Request
from pydantic import BaseModel, computed_field
from typing import List, Dict, Any,Optional
import db

app = FastAPI()

# 🌟 Встановіть свій базовий URL
BASE_URL = "http://127.0.0.1:8000/endpoints"

class Endpoints(BaseModel):
    NUM: int
    ENDPOINT: str
    API_VER: str
    DESCRIPTION: Optional[str]
    URL: Optional[str] = None

    # # 🌟 Використання обчислюваного поля (computed_field)
    # @computed_field(return_type=str)
    # @property
    # def URL(self) -> str:
    #     """Генерує URL, використовуючи значення поля ENDPOINT."""
    #     # Коректне форматування URL-параметра
    #     return f"{BASE_URL}?endpoint={self.ENDPOINT}"
    # Налаштування для коректного прийому даних з БД
    class Config:
        populate_by_name = True

# @app.get("/endpoints")
# def read_root():
#     # Повертає JSON-відповідь
#     try:
#         sql = 'select  q.num, q.endpoint,q.api_ver,q.description  from querys q'
#         data = db.get_data(sql)
#         return data
#     except Exception as e:
#         print("Помилка отримання endpoint:", e)


@app.get("/data", response_model=List[Dict[str, Any]])
async def get_data(endpoint: str):
    print(f"Отримане значення параметра endpoint: {endpoint}")
    sql = db.get_sql(endpoint)
    print(sql)
    raw_data = db.get_data(sql)
    return raw_data


@app.get("/endpoints", response_model=List[Endpoints])
async def read_items(request: Request):
    base_url = f"{request.url.scheme}://{request.url.netloc}/data?endpoint="

    sql = 'select  q.num, q.endpoint,q.api_ver,q.description  from querys q'
    data = db.get_data(sql)
    validated_data = []

    for row in data:
        # Створюємо об'єкт Pydantic з даних БД
        item = Endpoints(**row)
        # 🌟 Генеруємо та встановлюємо URL, використовуючи dynamic_base_url
        item.URL = f"{base_url}{item.ENDPOINT}"
        validated_data.append(item)
    # 2. Валідація та створення об'єктів Pydantic
    # validated_data = [Endpoints(**row) for row in data]

    # 3. FastAPI серіалізує об'єкти, викликаючи метод .URL
    return validated_data

