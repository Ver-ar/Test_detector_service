from sqlalchemy import delete, insert, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from models import *
from fastapi import HTTPException
from detect_faces import detect
#from create_database import engine
from sqlalchemy.sql import select



def create_image(Session, faces: int):    
    try:
        with engine.begin() as conn:            
            #ins = image_table.insert().values(faces='faces')
            #ins = conn.execute(image_table.select())
            result = conn.execute(image_table.insert(),{"faces": faces}).inserted_primary_key 
                               
            print(f'В базу добавлено фото c id: {result[0]}')
    except:
        Session.rollback()
        print('ralled back')
        raise
    finally:
        Session.close()
    return result[0]


def get_image (Session, id: int):
    try:
        s = select(image_table).where(image_table.c.id == id)
        with engine.begin() as conn: 
            for row in conn.execute(s):
                print(f'Выбрано фото c id: {row[0]}')
                return row
                
    finally:
        Session.close()
    #2 with engine.begin() as conn:
        
        #result = conn.execute(s)
        #row = result.fetchone()
        #return ("id:", row._mapping['id'], "; faces:", row._mapping['faces'], "; datetime:", row._mapping['datetime'])
    #1  return Session.query(image_table).filter(image_table.id == id).first()
        
    

def del_image(Session, id: int):
    db_image = Session.query(image_table).filter(image_table.id == id).first()
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    Session.delete(db_image)
    Session.commit()
    return db_image.id

    

def count_image(Session, id: int, faces: int, time: str):
    #images = db.query(Image).filter(Image.id == id, Image.faces == faces, Image.datetime == time).count()
    #return images
    try:
        count_fn = func.count(image_table.c.id == id, image_table.c.faces == faces, image_table.c.datetime == time)
        return count_fn
    finally:
        Session.close()