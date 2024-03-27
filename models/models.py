from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Enum 
from sqlalchemy import ARRAY
from sqlalchemy import DateTime
from sqlalchemy import LargeBinary

from sqlalchemy.orm import declarative_base, relationship, validates
import enum
import re
import bcrypt

Base = declarative_base()


class Class(Base):
    __tablename__ = "class"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    teacher_id = Column(Integer, ForeignKey("teacher.user_id"))

    class_users = relationship("ClassUser", cascade="all, delete")
    requests = relationship("Request", cascade="all, delete")
    messages = relationship("Message", cascade="all, delete")
    thumbnail = relationship("Thumbnail", cascade="all, delete")
    teacher = relationship("Teacher")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'teacher_id': self.teacher_id,
            'teacher_first_name': self.teacher.user.firstName,
            'teacher_last_name': self.teacher.user.lastName
        }


class Role(enum.Enum):
    teacher = 1
    student = 2


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String, unique=True)
    role = Column(Enum(Role))

    teacher = relationship("Teacher", cascade="all, delete")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'username': self.username,
            'password': self.password,
            'phone': self.phone,
            'email': self.email,
            'role': str(self.role)
        }

    # These fields are used for validation
    __email_r = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[""" +
                           """\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")""" +
                           """@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|""" +
                           """2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:""" +
                           """(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
    __password_r = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
    __phone_r = re.compile("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")

    @staticmethod
    def validate_name(name):
        length = len(name)
        if length <= 3 or length > 40:
            raise ValueError("Length of username should be less than 40 and more than 4 characters long")
        return name

    @validates("firstName")
    def validate_first_name(self, key, firstName):
        return self.validate_name(firstName)

    @validates("lastName")
    def validate_last_name(self, key, lastName):
        return self.validate_name(lastName)

    @validates("email")
    def validate_email(self, key, email):
        if User.__email_r.match(email) is None:
            raise ValueError("Invalid email")

        return email

    @validates("password")
    def validate_password(self, key, password: str):
        if User.__password_r.match(password) is None:
            raise ValueError("This is not password(8 characters long+, one letter and number")
        password = bytes(password, 'utf-8')
        password = bcrypt.hashpw(password, bcrypt.gensalt(15))
        return password.decode("utf-8")

    @validates("phone")
    def validate_phone(self, key, phone):
        match = User.__phone_r.match(phone)
        if match is None:
            raise ValueError("This is not a phone number")

        return phone

    @validates("role")
    def validate_role(self, key, role):
        if role not in [r.name for r in Role] and \
                role not in [r for r in Role]:
            raise ValueError("This is not a role")

        return role


class Teacher(Base):
    __tablename__ = "teacher"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    user = relationship("User", cascade="all, delete")
    diplomas = Column(ARRAY(String))
    employment = Column(ARRAY(String))

    def to_dict(self) -> dict:
        return {
            'diplomas': self.diplomas,
            'employment': self.employment
        }


class ClassUser(Base):
    __tablename__ = "class_user"

    class_id = Column('class', Integer, ForeignKey("class.id"), primary_key=True)
    user_id = Column('user', Integer, ForeignKey("user.id"), primary_key=True)

    class_obj = relationship("Class")
    user_obj = relationship("User")

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'class_id': self.class_id
        }


class Request(Base):
    __tablename__ = "request"

    class_id = Column('class', Integer, ForeignKey("class.id"), primary_key=True)
    user_id = Column('user', Integer, ForeignKey("user.id"), primary_key=True)

    class_obj = relationship("Class")
    user_obj = relationship("User")

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'class_id': self.class_id
        }


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    user = Column(Integer, ForeignKey("user.id"))
    class_ = Column(Integer, ForeignKey("class.id"))

    cls = relationship('Class')
    usr: User = relationship('User')

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'date': str(self.date),
            'user': self.user,
            'cls': self.class_,
            'fullname': f'{self.usr.firstName} {self.usr.lastName}',
            'username': self.usr.username
        }


class Thumbnail(Base):
    __tablename__ = "class_thumbnail"

    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey("class.id"))
    image = Column(LargeBinary())