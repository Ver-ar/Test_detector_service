from sqlalchemy import func, select
from database_process.models import bot_table, image_table, engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, AsyncEngine

async def create_image(faces: int):    
    async with engine.begin() as conn:            
        result = (await conn.execute(image_table.insert(),{"faces": faces})).inserted_primary_key
        print(f'В базу добавлено фото c id: {result[0]}')
    return result[0]

async def get_image (id: int):
    select_image = select(image_table).where(image_table.c.id == id)
    async with engine.begin() as conn: 
        result = await conn.execute(select_image)
        result_image = result.fetchone() 
        print(f'Выбрано фото c id: {result_image}')
        return result_image

async def del_image(id: int):    
    result_del = image_table.delete().where(image_table.c.id == id)
    async with engine.begin() as conn:
        result = await conn.execute(result_del)
        if result.rowcount == 1:
            print(f'Удалено фото c id: {id}')
            return result
        else:
            return
   
async def count_image_faces(faces: int):
    count_table = [func.count('*').label('count'), image_table.c.faces]
    select_count = select(count_table).where(image_table.c.faces == faces)
    async with engine.begin() as conn:
        result = await conn.execute(select_count)
        result_count = result.fetchone()                             
    return result_count[1]

async def get_image_from_faces (faces: int):
    select_image = select(image_table).where(image_table.c.faces == faces)
    async with engine.begin() as conn: 
        result = await conn.execute(select_image)
        result_image = result.fetchall() 
        print(f'Выбрано фото c количеством лиц: {result_image}')
        return result_image

async def get_db():
    select_image = select([image_table])
    async with engine.begin() as conn: 
        result = (await conn.execute(select_image)).fetchall()
        return result

async def get_notify_users(faces: int):
    select_image = select(bot_table).where(bot_table.c.face_from_user == faces)
    async with engine.begin() as conn:
        result = await conn.execute(select_image)
        result_id = result.fetchall()
        list_users_id = []
        for a in result_id:
            list_users_id.append(a[1])
        return list_users_id

async def create_users(faces, user_id):
    exist = select(bot_table).where(bot_table.c.face_from_user == faces, bot_table.c.user_id == user_id)
    async with engine.begin() as conn:
        result = await conn.execute(exist)
        result_ex = result.fetchone()
        if result_ex == None:
            await conn.execute(bot_table.insert(),{'face_from_user': faces,'user_id': user_id})     
            return (f'В базу бота внесены новые данные:user_id: {user_id} и количество отслеживаемых лиц: {faces}')            
        else:
            return (f'В базе уже есть это значение, попробуй ввести другое с командой /faces')