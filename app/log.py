import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('uvicorn').setLevel('ERROR')
logging.getLogger('aiogram').setLevel('ERROR')
logging.getLogger('sqlalchemy').setLevel('ERROR')
logging.getLogger('aiosqlite').setLevel('ERROR')

fh = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)