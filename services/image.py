from sqlalchemy.orm import Session
from sqlalchemy.orm import Query
from models.models import Thumbnail
def thumbnail_exists(session: Session, id: int):
    return session.query(Thumbnail).filter(Thumbnail.class_id == id)

def update_thumbnail(images: Query, encoded_image):
    images.update({Thumbnail.image: encoded_image})