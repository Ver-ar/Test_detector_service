from sqlalchemy.orm import Session
import models

def create_image(db: Session, faces: int):
    db_image = models.Image(faces=faces)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image.id
