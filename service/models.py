from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
import datetime

from create_database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True) #generated by itself; send value to my_database
    faces = Column(Integer, autoincrement=False) #get faces with func. create_image from create_writing < main; send value to my_database
    datetime = Column(DateTime, default=datetime.datetime.utcnow) #generated by itself; send value to my_database
