from fastapi import FastAPI,Request
from pydantic import BaseModel
from typing import List, Dict, Any,Optional
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import db

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class Endpoints(BaseModel):
    NUM: int
    ENDPOINT: str
    API_VER: str
    DESCRIPTION: Optional[str]
    URL: Optional[str] = None
    class Config:
        populate_by_name = True

@app.get("/data", response_model=List[Dict[str, Any]])
# async def get_data(endpoint: str):
# @app.get("/data")
async def get_data(request: Request):
    try:
        # 🌟 Доступ до всіх параметрів запиту як словника (Dict)
        query_params = dict(request.query_params)
        endpoint = query_params.get('endpoint')
        del query_params['endpoint']

        db_args = query_params

        for key, value in db_args.items():
            print(f"{key} = {value}")

        sql = db.get_sql(endpoint)
        if db_args:
            sql = sql + ' where 1=1'
            for key, value in db_args.items():
                sql = sql + ' and '+ key + ' ='+ value
        print(sql)
        raw_data = db.get_data(sql)
        return raw_data
    except Exception as e:
        display_sql = sql.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ').replace('\u003E','>')
        raise HTTPException(
            status_code=500,
            detail={
                "error": str(e),
                "executed_sql": display_sql
            }
        )

@app.get("/", response_model=List[Endpoints])
async def get_endpoints(request: Request):
    base_url = f"{request.url.scheme}://{request.url.netloc}/data?endpoint="
    sql = 'select  q.num, q.endpoint,q.api_ver,q.description  from querys q order by 1'
    data = db.get_data(sql)
    validated_data = []
    for row in data:
        item = Endpoints(**row)
        item.URL = f"{base_url}{item.ENDPOINT}"
        validated_data.append(item)
    # return validated_data
    context = {
        "request": request,
        "title": "Список Ендпоінтів",
        # 🌟 Передаємо дані у контекст під іменем 'endpoints'
        "endpoints": validated_data
    }
    return templates.TemplateResponse("index.html", context)
