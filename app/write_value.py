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
        result = conn.execute(select_image)
        result_image = result.fetchone() 
        print(f'Выбрано фото c id: {result_image}')
        return result_image

def del_image(id: int):    
    result_del = image_table.delete().where(image_table.c.id == id)
    with engine.begin() as conn:
        id = conn.execute(result_del).rowcount
        print(f'Удалено фото c id: {id}')
        return id
   
def count_image_faces(faces: int):
    count_table = [func.count('*').label('count'), image_table.c.faces]
    select_count = select(count_table).where(image_table.c.faces == faces)
    with engine.begin() as conn:
        result = conn.execute(select_count)
        result_count = result.fetchone()                             
    return result_count[1]


def get_image_from_faces (faces: int):
    select_image = select(image_table).where(image_table.c.faces == faces)
    with engine.begin() as conn: 
        result = conn.execute(select_image)
        result_image = result.fetchall() 
        print(f'Выбрано фото c количеством лиц: {result_image}')
        return result_image



def get_db():
    select_image = select([image_table])
    with engine.begin() as conn: 
        result = conn.execute(select_image).fetchall()             
        return result




'''
def compare_values(face_from_user:int):
    
    compare = select (image_table).where(image_table.c.faces==bot_table.c.face_from_user)
    with engine.begin() as conn:
        result = conn.execute(compare)
        result_compare = result.fetchall()
        print(result)
        print(result_compare)
        return(result_compare)
'''
