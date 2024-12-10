from datetime import date
from fastapi import FastAPI, HTTPException, Response, Depends
from database import get_db
from models import News
from test import archive_news, delete_news_item, load_data
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.responses import JSONResponse


app = FastAPI()

@app.post("/update_news/")
async def update_news(db: AsyncSession = Depends(get_db)):
    result = await load_data(db=db)
    return result

@app.get("/news/")
async def get_news(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(News))
    item = result.scalars().all()
    return item

@app.delete("/delete_news/")
async def delete(news_id: int, db: AsyncSession = Depends(get_db)):
    result = await delete_news_item(db=db, id=news_id)


@app.get("/news/archive/")
async def get_news(start_date: date, end_date: date, db: AsyncSession = Depends(get_db)):
    result = await archive_news(db=db, start_date=start_date, end_date=end_date)
    return result
    # return JSONResponse(result, status_code=result["status_code"])     












# @app.delete("/delete/news")
# def delete_news(news_id: int):
#     """Удаляет запись из бд"""
#     result = delete_item(news_id)
#     return JSONResponse(result, status_code=result["status_code"])

# @app.get("/export_csv")
# def get_csv():
#     try:
#         conn = psycopg2.connect(
#                 dbname=db_name, 
#                 user=user, 
#                 password=password, 
#                 host=host,
#                 port=port
#             )
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM news")
#         query_results = cursor.fetchall()

#         # Преобразует данные в формат CSV
#         csv_content = ""
#         for row in query_results:
#             csv_content += ','.join(map(str, row)) + '\n'

#         # Ответ отображается в браузере
#         response = Response(content=csv_content,media_type="text/csv")
#         response.headers["Content-Disposition"] = "attachment; filename=news.csv" # inline для отображения в браузере,для загрузки файла attachment
        
#         return response
#     except psycopg2.Error as e:
#         return Response(content=f"Database error: {e}", status_code=500)
#     except Exception as e:
#         return Response(content=f"An unexpected error occurred: {e}", status_code=500)
#     finally:
#         if conn:
#             cursor.close()
#             conn.close()


# @app.get("/export_txt")
# def get_txt():
#     try:
#         conn = psycopg2.connect(
#                 dbname=db_name, 
#                 user=user, 
#                 password=password, 
#                 host=host,
#                 port=port
#             )
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM news")
#         query_results = cursor.fetchall()
        
#         txt_content = ""
#         for row in query_results:
#             txt_content += "\t".join(map(str, row)) + "\n"

#         response = Response(content=txt_content, media_type="text/plain; charset=utf-8")
#         response.headers["Content-Disposition"] = "attachment; filename=news.txt"
#         return response
    
#     except psycopg2.Error as e:
#         return Response(content=f"Database error: {e}", status_code=500)
#     except Exception as e:
#         return Response(content=f"An unexpected error occurred: {e}", status_code=500)
#     finally:
#         if conn:
#             cursor.close()
#             conn.close()

# @app.get("/export_json")
# def get_json():
#     try:
#         conn = psycopg2.connect(
#                 dbname=db_name, 
#                 user=user, 
#                 password=password, 
#                 host=host,
#                 port=port
#             )
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM news")
#         query_results = cursor.fetchall()
        
#         # в json объект
#         columns = [desc[0] for desc in cursor.description]
#         json_data = [dict(zip(columns, row)) for row in query_results]
#         json_str = json.dumps(json_data, indent=4, default=str)
        
#         response = Response(content=json_str, media_type='application/json')
#         response.headers["Content-Disposition"] = "attachment; filename=news.json"
#         return response

#     except psycopg2.Error as e:
#         return Response(content=f"Database error: {e}", status_code=500)
#     except Exception as e:
#         return Response(content=f"An unexpected error occurred: {e}", status_code=500)
#     finally:
#         if conn:
#             cursor.close()
#             conn.close()