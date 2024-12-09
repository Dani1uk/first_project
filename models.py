from sqlalchemy.orm import  DeclarativeBase
from sqlalchemy import Column, Integer, String, Date

class Base(DeclarativeBase):
    pass

class News(Base):
    __tablename__ = "news"
    news_id = Column(Integer, primary_key=True)
    date = Column(Date)
    title = Column(String)
    link = Column(String)
  




