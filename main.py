from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
from database import load_data_in_database

app = FastAPI()

class NewsItem(BaseModel):
    date: str
    title: str
    link: str

@app.get("/update_news")
async def update_news():
    """Эндпоинт для автоматической загрузки новостей."""
    try:
        result = load_data_in_database()
        return result
    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)