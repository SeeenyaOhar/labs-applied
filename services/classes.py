from models.models import Class
from sqlalchemy.orm import Session
from typing import List
from typing import Callable
from typing import Optional

def get_cls(session: Session, filter: dict = None) -> Class:
    return session.query(Class).filter_by(**filter).first()

def delete_cls(session: Session, classes: List[Class]):
    session.delete(classes)

def get_classes(session: Session) -> List[Class]:
        return session.query(Class).all()

def save_class(session: Session, cls: Class):
    session.add(cls)
