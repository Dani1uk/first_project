from datetime import datetime
from fastapi import HTTPException, status
from bs4 import BeautifulSoup
from fastapi import Depends
import requests
from models import News
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database import get_db
from sqlalchemy import insert, select, delete

async def load_data(db: AsyncSession = Depends(get_db)):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    }
    url = "https://www.moex.com/ru/news/"
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'lxml')
    count = 0
    try:
        for article in soup.find_all('div', class_='new-moex-news-list__record'):
            date_str = article.find('div', class_='new-moex-news-list__date').text.strip()
            title = article.find('a').text.strip()
            link = 'https://www.moex.com' + article.find('a')['href']
            try:
                date = datetime.strptime(date_str, '%d.%m.%Y').date()
                stmt = insert(News).values(date=date, title=title, link=link)
                result = await db.execute(stmt)
                await db.commit()
                count += result.rowcount
            except IntegrityError as e:
                db.rollback() 
                print(f"Duplicate entry: {e}")
                continue 

        return {"message": "Загрузка данных завершена", "added_count": count}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
    
async def archive_news(start_date, end_date, db: AsyncSession = Depends(get_db)):
    stmt = select(News).where(News.date.between(start_date, end_date))
    result = await db.execute(stmt)
    await db.commit()
    news_items = result.scalars().all()
    return news_items

async def delete_news_item(id: int, db: AsyncSession = Depends(get_db)):
    stmt = delete(News).filter_by(news_id=id)
    result = await db.execute(stmt)
    await db.commit()
    if result.rowcount == 1:
        return {"message": "Запись успешно удалена"}
    else:
        return {"message": "Запись не найдена", "status_code": 404}