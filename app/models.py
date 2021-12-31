from sqlalchemy import Column, Integer, DateTime, MetaData, Sequence, create_engine, TEXT
import datetime
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///./my_database.db')

meta = MetaData()

image_table = Table ('image_table', meta,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('faces', Integer, autoincrement=False),
    Column('datetime', DateTime, default=datetime.datetime.utcnow) 
    )


bot_table = Table ('bot_users', meta,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('user_id', Integer, autoincrement=False),
    Column('user_name', TEXT, autoincrement=False)
    )



meta.create_all(engine)