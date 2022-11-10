from flask import make_response,Response, abort, request, Blueprint

from Encoder import AlchemyEncoder
from models.models import  User,Teacher
import  json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
engine = create_engine("postgresql://postgres:admin@localhost:5432/Online-Classes-Service")
Session = sessionmaker(bind=engine)
session = Session()

teacher_api = Blueprint('teacher_api', __name__)


@teacher_api.route("/api/v1/teacher",methods=['POST'])
def create():
    All_data = request.get_json()
    User_data = All_data.get('User')
    Teacher_Data = All_data.get('Teacher')
    if User_data is None:
        return Response(status=402)
    if('username' in User_data
    and 'firstName' in User_data
    and 'lastName' in User_data
            and 'email' in User_data
    and 'password' in User_data
    and 'phone' in User_data
    and 'role' in User_data):

        username = User_data['username']
        firstName = User_data['firstName']
        lastName = User_data['lastName']
        email = User_data['email']
        password = User_data['password']
        phone = User_data['phone']
        role = User_data['role']

        new_user=User(username=username, firstName=firstName, lastName=lastName, email=email, password=password, phone=phone, role=role)
        session.add(new_user)
        try:
            session.commit()
        except IntegrityError:
            return Response(status=402)
        user = session.query(User)
        currentUser = new_user

        if ('diplomas' in Teacher_Data
                and 'employment' in Teacher_Data):
            diplomas=Teacher_Data['diplomas']
            employment=Teacher_Data['employment']
            new_ticher=Teacher(user_id=new_user.id,diplomas=diplomas,employment=employment)
            session.add(new_ticher)
            try:
                session.commit()
            except IntegrityError:
                return Response(status=402)
            return Response(status=200)

    else:
        return Response(status=402)


@teacher_api.route("/api/v1/teacher/<user_Id>", methods=['GET'])
def get_user(user_Id):
    user = session.query(User)
    teacher = session.query(Teacher)
    currentTeacher= teacher.get(int(user_Id))
    currentUser = user.get(int(user_Id))
    if currentUser is None:
        return Response("User doesn't exist", status=404)
    if currentTeacher is None:
        return Response("Teacher doesn't exist", status=404)
    return Response(
        response=json.dumps(currentUser.to_dict(),cls=AlchemyEncoder)+json.dumps(currentTeacher.to_dict(), cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )


@teacher_api.route("/api/v1/teacher/<user_Id>", methods=['DELETE'])
def delete_user(user_Id):
    user = session.query(User)
    teacher = session.query(Teacher)
    sam = teacher.get(int(user_Id))
    currentUser = user.get(int(user_Id))
    if currentUser is None:
        return Response("User doesn't exist", status=404)
    session.delete(sam)
    session.delete(currentUser)
    try:
        session.commit()
    except IntegrityError:
        return Response("Delete failed", status=402)
    return Response("User was deleted", status=200)
