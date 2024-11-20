import psycopg2
from config import host, db_name, user, password, port
from psycopg2.errors import UniqueViolation
from bs4 import BeautifulSoup
import requests
import lxml

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
       
            with connection.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS news(
                    news_id serial PRIMARY KEY,
                    date DATE,
                    title text,
                    link varchar)"""
                )
            print("[INFO] Table created successfully")

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO news (date, title, link) VALUES (to_date(%s, 'DD.MM.YYYY'),%s,%s)",(date , title , link))
            
            print("[INFO] Данные успешно добавлены")
            return {"message": "Данные успешно добавлены"}
    except UniqueViolation as e:
        connection.rollback()
    except Exception as ex:
        print(f"An error occurred: {ex}")
    finally:
        connection.close()


            
