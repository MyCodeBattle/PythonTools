import sqlite3
from sqlalchemy import Column, Integer, String, VARCHAR, create_engine
import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('jdbc:sqlite:song.sqlite')
Session = sessionmaker(engine)

class Song(Base):
    __tablename__ = 'Songs'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    singer = Column(String(50))
    lyrics = Column(VARCHAR(1000))
    album = Column(String(30))

if __name__ == '__main__':
    Base.