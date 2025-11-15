from fastapi import FastAPI,Request
from pydantic import BaseModel, computed_field
from typing import List, Dict, Any,Optional
import db

app = FastAPI()

class Endpoints(BaseModel):
    NUM: int
    ENDPOINT: str
    API_VER: str
    DESCRIPTION: Optional[str]
    URL: Optional[str] = None
    class Config:
        populate_by_name = True

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
        item = Endpoints(**row)
        item.URL = f"{base_url}{item.ENDPOINT}"
        validated_data.append(item)
    return validated_data

