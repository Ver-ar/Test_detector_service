import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.WARNING)


logging.getLogger('uvicorn').setLevel('WARNING')
logging.getLogger('aiogram').setLevel('WARNING')
logging.getLogger('sqlalchemy').setLevel('WARNING')
logging.getLogger('aiosqlite').setLevel('WARNING')

sh = logging.StreamHandler(sys.stdout)
fh = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)