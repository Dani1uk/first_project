# from selenium import webdriver
# from bs4 import BeautifulSoup
# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver/", options=chrome_options )

# # Переходим  на  страницу
# driver.get('https://www.moex.com/ru/news/')

# # Ждем  загрузки  скриптов  JavaScript  (например,  5  секунд)
# driver.implicitly_wait(5) 

# # Получаем  HTML-код  страницы
# html_content = driver.page_source

# soup = BeautifulSoup(html_content, 'html.parser'

# dates = soup.find_all('div', class_="new-moex-news-list__date")
# times = soup.find_all('div', class_="new-moex-news-list__time")
# headers = soup.find_all('div', class_="new-moex-news-list__body")
# #ink = 'https://www.moex.com' + header.a['href']

# for time in headers:
#     print(time.text.strip())

# # Закрываем  браузер
# driver.quit()

from bs4 import BeautifulSoup
import requests
import lxml

def get_data():

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }

    url = "https://www.moex.com/ru/news/"

    try:
        r = requests.get(url=url, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')

        for article in soup.find_all('div', class_='new-moex-news-list__record'):
            data = article.find('div', class_='new-moex-news-list__date').text.strip()
            time = article.find('div', class_='new-moex-news-list__time').text.strip()
            description = article.find('a').text.strip()
            link = article.find('a')['href']
            link = 'https://www.moex.com' + link
        
            print(data,time,description,link)
    
    except Exception as e:
        print(f'Ошибка сбора данных {e}')
