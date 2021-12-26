from sqlalchemy.orm import Session
from sqlalchemy.sql import select
import models

def count_image(db: Session, id: int, faces: int, time: str):
    db_image = models.Image(id=id, faces=faces, time=time)
    pass