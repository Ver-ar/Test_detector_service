from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Column, Integer, DateTime, MetaData, Sequence
import datetime
from sqlalchemy.sql.schema import Table


meta = MetaData()

image_table = Table(
    "image_table",
    meta,
    Column("id", Integer, Sequence("user_id_seq"), primary_key=True),
    Column("faces", Integer, autoincrement=False),
    Column("datetime", DateTime, default=datetime.datetime.utcnow),
)


bot_table = Table(
    "bot_users",
    meta,
    Column("id", Integer, Sequence("user_id_seq"), primary_key=True),
    Column("user_id", Integer, autoincrement=False),
    Column("face_from_user", Integer, autoincrement=False),
)

engine = create_async_engine("sqlite+aiosqlite:///./my_database.db", pool_pre_ping=True)
