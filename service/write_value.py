from sqlalchemy import func, select
from models import *



def create_image(faces: int):    
    with engine.begin() as conn:            
        result = conn.execute(image_table.insert(),{"faces": faces}).inserted_primary_key 
        print(f'В базу добавлено фото c id: {result[0]}')
    return result[0]

def get_image (id: int):
    select_image = select(image_table).where(image_table.c.id == id)
    with engine.begin() as conn: 
        for row in conn.execute(select_image):
            print(f'Выбрано фото c id: {row[0]}')
            return row

def del_image(id: int):
    
    result_del = image_table.delete().where(image_table.c.id == id)
    with engine.begin() as conn:
        conn.execute(result_del)
        print(f'Удалено фото c id: {id}')
        return id
   
def count_image_id(id: int):
    count_table = [func.count('*').label('count'), image_table.c.id]
    select_count = select(count_table).where(image_table.c.id == id)
    with engine.begin() as conn:
        result = conn.execute(select_count)
        result_count = result.fetchall()                
    return result_count[0][0] 

def count_image_faces(faces: int):
    count_table = [func.count('*').label('count'), image_table.c.faces]
    select_count = select(count_table).where(image_table.c.faces == faces)
    with engine.begin() as conn:
        result = conn.execute(select_count)
        result_count = result.fetchall()                
    return result_count[0][0]