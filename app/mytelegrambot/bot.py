import logging
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(filename='bot.log', format='%(asctime)s-%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Track(StatesGroup):
    faces = State()

class Get(StatesGroup):
    get_faces = State()

class View(StatesGroup):
    view_faces = State()

class Del(StatesGroup):
    del_id = State()

class GetID(StatesGroup):
    get_id = State()