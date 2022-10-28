from sqlalchemy import Column, Integer, String, ForeignKey, Enum, ARRAY
from sqlalchemy.orm import declarative_base, relationship
import enum


Base = declarative_base()


class Class(Base):
    __tablename__ = "class"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    teacher_id = Column(Integer, ForeignKey("teacher.user_id"))

    teacher = relationship("Teacher")


class Role(enum.Enum):
    teacher = 1
    student = 2


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    role = Column(Enum(Role))


class Teacher(Base):
    __tablename__ = "teacher"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    user = relationship("User")
    diplomas = Column(ARRAY(String))
    employment = Column(ARRAY(String))


class ClassUser(Base):
    __tablename__ = "class_user"

    class_id = Column('class', Integer, ForeignKey("class.id"), primary_key=True)
    user_id = Column('user', Integer, ForeignKey("user.id"), primary_key=True)

    class_obj = relationship("Class")
    user_obj = relationship("User")


class Request(Base):
    __tablename__ = "request"

    class_id = Column('class', Integer, ForeignKey("class.id"), primary_key=True)
    user_id = Column('user', Integer, ForeignKey("user.id"), primary_key=True)

    class_obj = relationship("Class")
    user_obj = relationship("User")
