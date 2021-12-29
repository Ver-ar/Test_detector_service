'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///./my_database.db', echo=True)

SQLALCHEMY_DATABASE_URL = "sqlite:///./my_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )


Base = declarative_base()

Base.metadata.create_all(bind=engine)
'''