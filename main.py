from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
from database import load_data_in_database, get_news_by_date_range
from models import News
import psycopg2
from datetime import date
from config import host, db_name, user, password, port

app = FastAPI()

@app.post("/news/")
async def update_news():
    """Эндпоинт для автоматической загрузки новостей."""
    try:
        result = await load_data_in_database()
        return result
    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    

@app.get("/news/archive/")
async def get_news(start_date: date, end_date: date):
    """Получает новости за указанный период."""
    result = await get_news_by_date_range(start_date, end_date)
    if "error" in result:
        return JSONResponse(result, status_code=result["status_code"])
    return result