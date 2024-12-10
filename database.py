from bs4 import BeautifulSoup
import requests
import lxml
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from config import setting
from sqlalchemy import text, insert

engine = create_async_engine(url=setting.db_url, echo=True)
AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with AsyncSession() as session:
        yield session

                













# def create_unique_index():
#     try:
#         conn = psycopg2.connect(
#                 dbname=db_name, 
#                 user=user, 
#                 password=password, 
#                 host=host,
#                 port=port
#             )
        
#         with conn.cursor() as cur:
#             cur.execute("CREATE UNIQUE INDEX idx_news_title_link ON news (title, link)")
#             conn.commit()
#         print("Уникальный индекс создан")
#     except psycopg2.Error as e:
#         print(f"Ошибка при создании индекса: {e}")
#     finally:
#         if conn:
#             conn.close()

# def load_data():

#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
#     }

#     url = "https://www.moex.com/ru/news/"
        
#     r = requests.get(url=url, headers=headers)
#     r.encoding = 'utf-8'
#     soup = BeautifulSoup(r.text, 'lxml')

        
#     news_data = []
#     connection = None
#     try:
#         connection = psycopg2.connect(
#                     dbname=db_name, 
#                     user=user, 
#                     password=password, 
#                     host=host,
#                     port=port
#                 )
           
#         with connection.cursor() as cursor:
#             query = "INSERT INTO news (date, title, link) VALUES (to_date(%s, 'DD.MM.YYYY'),%s,%s) ON CONFLICT (title, link) DO NOTHING;"
#             try:
#                 for article in soup.find_all('div', class_='new-moex-news-list__record'):
#                     try:
#                         date = article.find('div', class_='new-moex-news-list__date').text.strip()
#                         title = article.find('a').text.strip()
#                         link = 'https://www.moex.com' + article.find('a')['href']
#                         news_data.append((date, title, link))
#                     except AttributeError as e:
#                         logger.exception(f"Error processing article: {e}")
#                     continue # Пропускаем ошибочные статьи
#                 cursor.executemany(query,news_data)
#                 connection.commit()
#                 return {"message": "Записи успешно добавлены в бд"}
#             except psycopg2.Error as e:
#                 connection.rollback()
#                 raise #Передаем исключение дальше, чтобы обработать его в основном блоке try-except
#             except Exception as e:
#                 connection.rollback()
#                 raise #Передаем исключение дальше
         
#     except psycopg2.Error as e:
#         return {"error": f"Database error: {e}", "status_code": 500}
#     except Exception as e:
#         logger.exception(f"Unexpected error: {e}")
#         return {"error": str(e), "status_code": 500}
#     finally:
#         if connection:
#             connection.close()
# def creat_table(): 
#     try:
#         conn = psycopg2.connect(
#                 dbname=db_name, 
#                 user=user, 
#                 password=password, 
#                 host=host,
#                 port=port
#             )
        
#         conn.autocommit = True


#         with conn.cursor() as cursor:
#                 # cursor.execute(
#                 #     """CREATE TABLE IF NOT EXISTS users (
#                 #     user_id SERIAL PRIMARY KEY,
#                 #     username VARCHAR(255) NOT NULL,
#                 #     surname VARCHAR(255) NOT NULL,  
#                 #     email VARCHAR(255) NOT NULL
#                 #     )"""
#                 # ) 

#                 # print("[INFO] Table created successfully")

#                 cursor.execute(
#                     """CREATE TABLE IF NOT EXISTS news(
#                     news_id SERIAL PRIMARY KEY,
#                     date DATE NOT NULL,
#                     title VARCHAR NOT NULL,
#                     link VARCHAR NOT NULL)"""
#                 )

#                 print("[INFO] Table created successfully")

#                 # cursor.execute(
#                 #     """CREATE TABLE IF NOT EXISTS personal_data (
#                 #     data_id SERIAL PRIMARY KEY,
#                 #     login VARCHAR(255) UNIQUE NOT NULL,
#                 #     hash_password VARCHAR(255) NOT NULL,
#                 #     user_id INTEGER REFERENCES users(user_id)
#                 #     )"""
#                 # )

#                 # print("[INFO] Table created successfully")

#                 # cursor.execute(
#                 #     """CREATE TABLE IF NOT EXISTS favorites (
#                 #     favorite_id SERIAL PRIMARY KEY,
#                 #     user_id INTEGER REFERENCES users(user_id),
#                 #     news_id INTEGER REFERENCES news(news_id)
#                 #     )"""
#                 # )

#                 # print("[INFO] Table created successfully")

#     except Exception as ex:
#         print(f"An error occurred: {ex}")
#     finally:
#         conn.close()

# def get_news_by_date_range(start_date: date, end_date: date):
#     """Получает новости из базы данных за указанный период."""
#     try:
#         conn = psycopg2.connect(
#                 dbname=db_name, 
#                 user=user, 
#                 password=password, 
#                 host=host,
#                 port=port
#             )
#         with conn.cursor() as cur:
#             cur.execute(
#                 "SELECT * FROM news WHERE date BETWEEN %s AND %s",
#                 (start_date, end_date),
#             )
#             conn.commit()
#             rows = cur.fetchall()
#             return rows
#     except psycopg2.Error as ex:
#         print(f"An error occurred: {ex}")
#     finally:
#         conn.close()

# def delete_item(p):
#     """Удалим-ка мы запись из бд"""
#     conn = psycopg2.connect(
#                 dbname=db_name, 
#                 user=user, 
#                 password=password, 
#                 host=host,
#                 port=port
#             )
#     try:
#         with conn.cursor() as cur:
#             query = "DELETE FROM news WHERE news_id = %s;"
#             cur.execute(query,p)
#             conn.commit()
#             return {"message": "Запись успешно удалена"}
#     except psycopg2.Error as ex:
#         print(f"An error occurred: {ex}")
#     finally:
#         if conn:
#             conn.close()
