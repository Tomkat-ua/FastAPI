from fastapi import FastAPI
from typing import List, Dict, Any
import db

app = FastAPI()


@app.get("/endpoints")
def read_root():
    # Повертає JSON-відповідь
    try:
        sql = 'select  q.num, q.endpoint,q.api_ver,q.description  from querys q'
        data = db.get_data(sql)
        return data
    except Exception as e:
        print("Помилка отримання endpoint:", e)


@app.get("/data", response_model=List[Dict[str, Any]])
async def get_data(endpoint: str):
    print(f"Отримане значення параметра endpoint: {endpoint}")
    sql = db.get_sql(endpoint)
    print(sql)
    raw_data = db.get_data(sql)
    return raw_data



