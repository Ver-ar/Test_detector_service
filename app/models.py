from sqlalchemy import Column, Integer, DateTime, MetaData, Sequence, create_engine
import datetime
from sqlalchemy.sql.schema import Table



engine = create_engine('sqlite:///./my_database.db', pool_pre_ping=True, echo=True)

meta = MetaData()

image_table = Table ('image_table', meta,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('faces', Integer, autoincrement=False),
    Column('datetime', DateTime, default=datetime.datetime.utcnow) 
    )


bot_table = Table ('bot_users', meta,
    Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
    Column('user_id', Integer, autoincrement=False),
    Column('face_from_user', Integer, autoincrement=False)
    )



meta.create_all(engine)
