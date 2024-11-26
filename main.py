from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from database import delete_item, load_data_in_database, get_news_by_date_range
from models import News
from datetime import date
import psycopg2
from config import host, db_name, user, password, port
app = FastAPI()

@app.post("/news/")
def update_news():
    """Эндпоинт для автоматической загрузки новостей."""
    try:
        result = load_data_in_database()
        return result
    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    

@app.get("/news/archive/")
def get_news(start_date: date, end_date: date):
    """Получает новости за указанный период."""
    result = get_news_by_date_range(start_date, end_date)
    if "error" in result:
        return JSONResponse(result, status_code=result["status_code"])
    return result

@app.delete("/delete/news/{news_id}")
def delete_news(news_id: int):
    """Удаляет запись из бд"""
    result = delete_item(news_id)
    if "error" in result:
        return JSONResponse(result, status_code=result["status_code"])
    return result

@app.get("/export_query_results")
async def export_csv():
    conn = conn = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host,
                port=port
            )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news")
    query_results = cursor.fetchall()

    # Преобразует данные в формат CSV
    csv_content = ""
    for row in query_results:
        csv_content += ','.join(map(str, row)) + '\n'

    # Ответ отображается в браузере
    response = Response(content=csv_content)
    response.headers["Content-Disposition"] = "inline; filename=query_results.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
