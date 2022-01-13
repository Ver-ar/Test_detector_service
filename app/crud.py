from sqlalchemy import func, select
from sqlalchemy.sql import exists
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
        result = conn.execute(result_del)
        if result.rowcount == 1:
            print(f'Удалено фото c id: {id}')
            return result
        else:
            return
   
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

def get_notify_users(faces: int):                #получаем id по кол-ву лиц, чтоб передать его в рез-т отправки сообщений ботом из таблицы фото по этому id
    select_image = select(bot_table).where(bot_table.c.face_from_user == faces)
    with engine.begin() as conn:
        result = conn.execute(select_image)
        result_id = result.fetchall()
        print(f'id по этому кол-ву лиц: {result_id}')
        return result_id


#def find_user
def create_users(faces, user_id):
    exist = bot_table.select().where(bot_table.c.face_from_user == faces, bot_table.c.user_id == user_id)
    select_row = exists(exist).select()
    
    with engine.begin() as conn:
        result = conn.execute(select_row).fetchone()
        print(result)
        if result[0] == False:            
            with engine.connect() as conn:
                ins = bot_table.insert().values(user_id = 'user_id', faces = 'faces')                
                res = conn.execute(ins)   
                print(res)
                print(result)       
                return (f'В базу бота внесены новые данные:user_id: {user_id} и количество отслеживаемых лиц: {faces}')            
        else:
            return(f'В базе уже есть это значение, попробуй ввести другое с командой /faces')
    
            
'''
def create_db_users(faces, user_id):    
    with engine.connect().execution_options(autocommit=True) as conn:
        res = conn.execute(bot_table.insert(),{'user_id': user_id}, {'faces': faces})   
        print(res)       
    return (f'В базу бота внесены новые данные:user_id: {user_id} и количество отслеживаемых лиц: {faces}')
'''


#def find_image_from_id(id: int):


'''
def compare_faces(faces: int):
    select_image = select(bot_table).where(bot_table.c.face_from_user == faces)
    with engine.begin() as conn:
        result = conn.execute(select_image)
        result_image = result.fetchall()
        print(f'Выбрано фото c количеством лиц: {result_image}')
        return result_image
'''
