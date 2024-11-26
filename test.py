import psycopg2
from config import host, db_name, user, password, port
from psycopg2.errors import UniqueViolation
from bs4 import BeautifulSoup
import requests
import lxml
import logging


logger = logging.getLogger(__name__)

def main():

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
            try:
                date = article.find('div', class_='new-moex-news-list__date').text.strip()
                title = article.find('a').text.strip()
                link = 'https://www.moex.com' + article.find('a')['href']
        
                connection.autocommit = True

                logging.basicConfig(filename='myapp.log', level=logging.INFO)
                logging.info(f'News added:{date},{title},{link}')

                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO news (date, title, link) VALUES (to_date(%s, 'DD.MM.YYYY'),%s,%s)",(date , title , link))
            
            except Exception as e:
                logger.exception(f"Error processing article: {e}") #Логирование ошибок с traceback
                connection.rollback() #Откат транзакции, чтобы не потерять данные при ошибке
        print("[INFO] Данные успешно добавлены")
        return {"message": "Загрузка данных завершена", "added_count":cursor.rowcount} 
    
    except UniqueViolation as e:
        return {"error": f"Duplicate entry: {e}", "status_code": 409} #Возвращаем данные об ошибке
    except Exception as e:
        return {"error": str(e), "status_code": 500} #Возвращаем данные об ошибке
    finally:
        connection.close()

if __name__ == '__main__':
    main()