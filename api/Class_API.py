from flask import make_response, Response, abort, request, Blueprint

from Encoder import AlchemyEncoder
import json
from models.models import Class, Teacher, ClassUser, Request, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine("postgresql://postgres:admin@localhost:5432/Online-Classes-Service")
Session = sessionmaker(bind=engine)
session = Session()

class_api = Blueprint('class_api', __name__)


@class_api.route("/api/v1/class", methods=['POST'])
def create():
    Class_data = request.get_json()
    if Class_data is None:
        return Response(status=400)

    try:
        classes = Class(**Class_data)
        class_exist = session.query(Class).filter_by(title=classes.title, description=classes.description).first()
        if (class_exist is not None):
            return Response("Class is already existed", status=402)
        session.add(classes)
        session.commit()
    except IntegrityError:
        return Response("Create failed", status=402)
    return Response("Class was created", status=200)


@class_api.route("/api/v1/class/student", methods=['POST'])
def create_student():
    Student_data = request.get_json()
    try:
        student = ClassUser(**Student_data)
        requests = session.query(Request).filter(
            Request.user_id == student.user_id and Request.class_id == student.class_id).first()
        session.add(student)
        session.delete(requests)
        session.commit()
    except IntegrityError:
        return Response("Create failed", status=402)
    return Response("student added", status=200)


@class_api.route("/api/v1/class/<class_id>", methods=['GET'])
def get_id(class_id):
    classes = session.query(Class).get(class_id)
    if classes is None:
        return Response("Class doesn't exist", status=404)
    return Response(
        response=json.dumps(classes.to_dict(), cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )


@class_api.route("/api/v1/class/<class_id>", methods=['DELETE'])
def delete_class(class_id):
    classes = session.query(Class)
    currentClass = classes.get(int(class_id))
    if currentClass is None:
        return Response("Class doesn't exist", status=404)

    try:
        session.delete(currentClass)
        session.commit()
    except IntegrityError:
        return Response("Delete failed", status=402)
    return Response("Class was deleted", status=200)


@class_api.route("/api/v1/class", methods=['GET'])
def get():
    clas = session.query(Class).all()
    classes = [element.to_dict() for element in clas]
    if classes is None:
        return Response("class doesn't exist", status=404)
    return Response(
        response=json.dumps(classes, cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )


@class_api.route("/api/v1/class", methods=['PUT'])
def put():
    Class_data = request.get_json()
    if (Class_data is None) and ("id" not in Class_data):
        return Response("Bad request", status=400)
    try:
        classes = Class(**Class_data)
        session.query(Class).filter(Class.id == classes.id).update(Class_data, synchronize_session="fetch")
        session.commit()
    except IntegrityError:
        return Response("Update failed", status=402)
    return Response("Class was updated", status=200)


@class_api.route("/api/v1/class/<student_id>/<class_id>", methods=['DELETE'])
def delete_student(student_id, class_id):
    currentClass = session.query(ClassUser).filter(
        ClassUser.user_id == student_id, ClassUser.class_id == class_id).first()
    if currentClass is None:
        return Response("student or class doesn't exist", status=404)
    try:
        session.delete(currentClass)
        session.commit()
    except IntegrityError:
        return Response("Delete failed", status=402)
    return Response("class was deleted", status=200)


@class_api.route("/api/v1/class/requests/<class_id>", methods=['GET'])
def get_request(class_id):
    current_request = session.query(Request).filter(Request.class_id == class_id).all()
    dictrequest = [elem.to_dict() for elem in current_request]
    if current_request is None:
        return Response("class doesn't exist", status=404)
    return Response(
        response=json.dumps(dictrequest, cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )


@class_api.route("/api/v1/<class_id>/student", methods=['GET'])
def get_student(class_id):
    current_student = session.query(ClassUser).filter(ClassUser.class_id == class_id).all()
    dictclass = [elem.to_dict() for elem in current_student]

    current_stud = [session.query(User).filter_by(id=i['user_id']).first().to_dict() for i in dictclass]

    if current_student is None:
        return Response("class doesn't exist", status=404)
    return Response(
        response=json.dumps(current_stud, cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )
