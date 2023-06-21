from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user

from errors.auth_errors import InsufficientRights
from errors.general_errors import InvalidRequest
from errors.general_errors import ResourceNotFound

from models.models import Class, ClassUser, Request, User, Role
from models.models import Thumbnail
from services.db import Session
from services.jwt import teacher_required
from services.image import thumbnail_exists
from services.image import update_thumbnail
import base64

class_api = Blueprint('class_api', __name__)


@class_api.route("/api/v1/class/<class_id>", methods=['GET'])
def get_class(class_id):
    with Session(expire_on_commit=False) as session:
        classes = session.query(Class).get(class_id)
        if classes is None:
            return jsonify({"msg": "Class doesn't exist"}), 404

        return jsonify(classes.to_dict()), 200


@class_api.route("/api/v1/class/<class_id>", methods=['DELETE'])
@jwt_required()
@teacher_required()
def delete_class(class_id):
    with Session.begin() as session:
        classes = session.query(Class)
        currentClass = classes.get(int(class_id))
        if currentClass is None:
            return jsonify({"msg": "Class doesn't exist"}), 404

        session.delete(currentClass)

    return jsonify({"msg": "Class was deleted"}), 200


@class_api.route("/api/v1/class", methods=['GET'])
def get_all_classes():
    with Session.begin() as session:
        classes = session.query(Class).all()
        classes = [element.to_dict() for element in classes]
        if classes is None:
            return jsonify({"msg": "Class doesn't exist"}), 404
        return jsonify(classes), 200


@class_api.route("/api/v1/class", methods=['POST'])
@jwt_required()
def create_class():
    with Session(expire_on_commit=False) as session:
        if current_user.role != Role.teacher:
            raise InsufficientRights("You should be teacher to do this")
        class_data = request.get_json()
        if class_data is None:
            return jsonify({"msg": "Class data is empty, no json provided"}), 400

        classes = Class(**class_data)
        class_exist = session.query(Class).filter_by(title=classes.title, description=classes.description).first()
        if class_exist is not None:
            return jsonify({"msg": "Such class already exists"}), 400

        session.add(classes)
        session.commit()

    return jsonify({"msg": "Class was created", "id": classes.id}), 200


@class_api.route("/api/v1/class", methods=['PATCH'])
@jwt_required()
@teacher_required()
def update_class():
    with Session.begin() as session:
        class_data = request.get_json()
        if (class_data is None) and ("id" not in class_data):
            return jsonify({"msg": "Bad request"}), 400

        classes = Class(**class_data)
        session.query(Class).filter(Class.id == classes.id) \
            .update(class_data, synchronize_session="fetch")
    return jsonify({"msg": "Class was updated"}), 200


@class_api.route("/api/v1/class/student", methods=['POST'])
@jwt_required()
def add_student_to_class():
    with Session.begin() as session:
        if current_user.role != Role.teacher:
            raise InsufficientRights("Role should be teacher")
        student_data = request.get_json()
        class_user = ClassUser(**student_data)
        students_in_class = session.query(ClassUser).filter(ClassUser.class_id == class_user.class_id).all()
        if len(students_in_class) > 5:
            raise InvalidRequest("There are already more than 5 people in this class")
        requests = session.query(Request).filter(
            Request.user_id == class_user.user_id and Request.class_id == class_user.class_id).first()
        session.add(class_user)

        if requests is not None:
            session.delete(requests)
    return jsonify({"msg": "Student has been added"}), 200


@class_api.route("/api/v1/class/student", methods=['DELETE'])
@jwt_required()
@teacher_required()
def delete_student_from_class():
    with Session.begin() as session:
        class_user_json = request.get_json()
        if current_user.role != Role.teacher:
            raise InsufficientRights("You should be a teacher to remove a student from a class")

        student_id = class_user_json.get('user')
        class_id = class_user_json.get('class')
        if student_id is None or class_id is None:
            return jsonify({"msg": "Invalid JSON, student_id or class_id is missing."}), 400
        current_class = session.query(ClassUser).filter(
            ClassUser.user_id == student_id, ClassUser.class_id == class_id).first()
        if current_class is None:
            return jsonify({"msg": "student or class doesn't exist"}), 404

        session.delete(current_class)
    return jsonify({"msg": "Class was deleted"}), 200


@class_api.route("/api/v1/class/requests/<class_id>", methods=['GET'])
@jwt_required()
@teacher_required()
def get_all_requests(class_id):
    with Session.begin() as session:
        current_request = session.query(Request).filter(Request.class_id == class_id).all()
        if current_request is None:
            return jsonify({"msg": "class doesn't exist"}), 404

        requests = [elem.to_dict() for elem in current_request]

        return jsonify(requests), 200


@class_api.route("/api/v1/<class_id>/student", methods=['GET'])
@jwt_required()
def get_all_students_in_class(class_id):
    with Session.begin() as session:
        if current_user.role != Role.teacher and \
                session.query(ClassUser).filter(ClassUser.class_id == class_id and
                                                ClassUser.user_id == current_user.id).first() is not None:
            raise InsufficientRights("You have to be in this class to get the list of students")
        current_student = session.query(ClassUser).filter(ClassUser.class_id == class_id).all()
        dictclass = [elem.to_dict() for elem in current_student]

        current_stud = [session.query(User).filter_by(id=i['user_id']).first().to_dict() for i in dictclass]

        if current_student is None:
            return jsonify({"msg": "class doesn't exist"}), 404
        return jsonify(current_stud), 200

@class_api.route("/api/v1/class/img/<class_id>", methods=['GET'])
def get_image(class_id):
    class_id = int(class_id)
    with Session.begin() as session:
        if session.query(Class).filter(Class.id == class_id).first() is None:
            raise ResourceNotFound("There is no class with such id.")
        thumbnail = session.query(Thumbnail).filter(Thumbnail.class_id == class_id).first()

        return jsonify(thumbnail=base64.b64encode(thumbnail.image).decode("utf-8") if thumbnail is not None else None), 200


@class_api.route("/api/v1/class/img", methods=['PUT'])
@jwt_required()
def upload_image():
    data = request.json
    if current_user.role != Role.teacher:
            raise InsufficientRights("You should be a teacher to do this")
    if data is None or data.get('image') is None or data.get('id') is None:
        raise InvalidRequest('To upload an image you have to pass JSON object with base64 encrypted "image" and "id" field.')
    with Session(expire_on_commit=False) as session:
        # check if the class provided exists
        # if not throw 400
        class_id = data.get('id')
        request_image = data.get('image')
        encode_image = lambda image: base64.b64decode(image.encode())

        images = thumbnail_exists(session, class_id)
        image = images.first()
        if image:
            update_thumbnail(images, encode_image(request_image))
            return jsonify(msg='Found an existant thumbnail and replaced it successfully.'), 200
        thumbnail = Thumbnail(class_id=class_id, image=encode_image(request_image))

        session.add(thumbnail)
        session.commit()

    return jsonify(msg='Thumbnail has been uploaded successfully'), 200


@class_api.route("/api/v1/classes/<user_id>", methods=['GET'])
@jwt_required()
def get_classes(user_id):
    with Session(expire_on_commit=False) as session:
        def get_joined_classes():
            class_users = session.query(ClassUser)\
            .filter(ClassUser.user_id == int(user_id))\
                .all()
            class_users_dicts = [elem.to_dict() for elem in class_users]

            classes = [session.query(Class)\
                            .filter_by(id=class_user['class_id'])\
                                .first().to_dict() for class_user in class_users_dicts]
            
            return classes

        def get_teacher_classes():
            classes = session.query(Class)\
                .filter(Class.teacher_id == int(user_id))\
                .all()
            return [cls.to_dict() for cls in classes]

        if int(user_id) != current_user.id and current_user.role != Role.teacher:
            raise InsufficientRights("Role should be teacher or you should be the owner of the resource")
        joined_classes = get_joined_classes()
        teacher_classes = get_teacher_classes()
        all_user_classes = joined_classes + teacher_classes

        if all_user_classes is None:
            return jsonify({"msg": "Classes don't exist"}), 404
        return jsonify(all_user_classes), 200