import psycopg2
from config import host, db_name, user, password, port
from psycopg2.errors import UniqueViolation
from bs4 import BeautifulSoup
import requests
import lxml
from datetime import date
import logging


def create_unique_index():
    try:
        conn = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host,
                port=port
            )
        with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS news(
                    news_id serial PRIMARY KEY,
                    date DATE,
                    title text,
                    link varchar)"""
                )

        print("[INFO] Table created successfully")

        with conn.cursor() as cur:
            cur.execute("CREATE UNIQUE INDEX idx_news_title_link ON news (title, link)")
            conn.commit()
        print("Уникальный индекс создан")
    except psycopg2.Error as e:
        print(f"Ошибка при создании индекса: {e}")
    finally:
        if conn:
            conn.close()

def load_data_in_database():

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }

    url = "https://www.moex.com/ru/news/"
        
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')

    connection = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host,
                port=port
            )
        

    try:
        for article in soup.find_all('div', class_='new-moex-news-list__record'):
            date = article.find('div', class_='new-moex-news-list__date').text.strip()
            title = article.find('a').text.strip()
            link = 'https://www.moex.com' + article.find('a')['href']
        
            connection.autocommit = True

            logging.info(f'News added:{title}')

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO news (date, title, link) VALUES (to_date(%s, 'DD.MM.YYYY'),%s,%s)",(date , title , link))
            
            print("[INFO] Данные успешно добавлены")
            return {"message": "Загрузка данных завершена", "added_count":cursor.rowcount} 
    
    except UniqueViolation as e:
        return {"error": f"Duplicate entry: {e}", "status_code": 409} #Возвращаем данные об ошибке
    except Exception as e:
        return {"error": str(e), "status_code": 500} #Возвращаем данные об ошибке
    finally:
        connection.close()

def creat_table():
     
    try:
        conn = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host,
                port=port
            )
        
        conn.autocommit = True


        with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    surname VARCHAR(255) NOT NULL,  
                    email VARCHAR(255) NOT NULL
                    )"""
                ) 

                print("[INFO] Table created successfully")

                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS news(
                    news_id serial PRIMARY KEY,
                    date DATE,
                    title text,
                    link varchar)"""
                )

                print("[INFO] Table created successfully")

                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS personal_data (
                    data_id SERIAL PRIMARY KEY,
                    login VARCHAR(255) UNIQUE NOT NULL,
                    hash_password VARCHAR(255) NOT NULL,
                    user_id INTEGER REFERENCES users(user_id)
                    )"""
                )

                print("[INFO] Table created successfully")

                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS favorites (
                    favorite_id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(user_id),
                    news_id INTEGER REFERENCES news(news_id)
                    )"""
                )

                print("[INFO] Table created successfully")

    except Exception as ex:
        print(f"An error occurred: {ex}")
    finally:
        conn.close()

def get_news_by_date_range(start_date: date, end_date: date):
    """Получает новости из базы данных за указанный период."""
    try:
        conn = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host,
                port=port
            )
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM news WHERE date BETWEEN %s AND %s",
                (start_date, end_date),
            )
            rows = cur.fetchall()
            return rows
    except psycopg2.Error as ex:
        print(f"An error occurred: {ex}")
    finally:
        conn.close()

def delete_item(news_id: int):
    """Удалим-ка мы запись из бд"""
    try:
        conn = psycopg2.connect(
                dbname=db_name, 
                user=user, 
                password=password, 
                host=host,
                port=port
            )
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM news WHERE news_id = %s",
                (news_id),
            )
            rows = cur.fetchall()
            return rows
    except psycopg2.Error as ex:
        print(f"An error occurred: {ex}")
    finally:
        conn.close