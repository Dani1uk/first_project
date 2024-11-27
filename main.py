from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from database import delete_item, load_data_in_database, get_news_by_date_range
from models import News
from datetime import date
import psycopg2
from io import StringIO
from config import host, db_name, user, password, port
import csv
import json

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

@app.get("/export_csv")
def get_csv():
    try:
        conn = psycopg2.connect(
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
        # output = StringIO()
        # writer = csv.writer(output)
        # writer.writerows([[str(x) for x in row] for row in query_results]) # Декодируем данные в строки
        # csv_content = output.getvalue()

        # Ответ отображается в браузере
        response = Response(content=csv_content,media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=news.csv" # inline для отображения в браузере,для загрузки файла attachment
        
        return response
    except psycopg2.Error as e:
        return Response(content=f"Database error: {e}", status_code=500)
    except Exception as e:
        return Response(content=f"An unexpected error occurred: {e}", status_code=500)
    finally:
        if conn:
            cursor.close()
            conn.close()


@app.get("/export_txt")
def get_txt():
    try:
        conn = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host,
                port=port
            )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news")
        query_results = cursor.fetchall()
        
        txt_content = ""
        for row in query_results:
            txt_content += "\t".join(map(str, row)) + "\n"

        response = Response(content=txt_content, media_type="text/plain; charset=utf-8")
        response.headers["Content-Disposition"] = "attachment; filename=news.txt"
        return response
    
    except psycopg2.Error as e:
        return Response(content=f"Database error: {e}", status_code=500)
    except Exception as e:
        return Response(content=f"An unexpected error occurred: {e}", status_code=500)
    finally:
        if conn:
            cursor.close()
            conn.close()

@app.get("/export_json")
def get_json():
    try:
        conn = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host,
                port=port
            )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM news")
        query_results = cursor.fetchall()
        
        # в json объект
        columns = [desc[0] for desc in cursor.description]
        json_data = [dict(zip(columns, row)) for row in query_results]
        json_str = json.dumps(json_data, indent=4, default=str)
        
        response = Response(content=json_str, media_type='application/json')
        response.headers["Content-Disposition"] = "attachment; filename=news.json"
        return response

    except psycopg2.Error as e:
        return Response(content=f"Database error: {e}", status_code=500)
    except Exception as e:
        return Response(content=f"An unexpected error occurred: {e}", status_code=500)
    finally:
        if conn:
            cursor.close()
            conn.close()