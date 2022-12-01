from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required

from models.models import User, Teacher
from services.db import Session
from services.jwt import teacher_required

teacher_api = Blueprint('teacher_api', __name__)


@teacher_api.route("/api/v1/teacher", methods=['POST'])
@jwt_required()
@teacher_required()
def create():
    session = Session()

    All_data = request.get_json()
    User_data = All_data.get('User')
    User_data['role'] = 'teacher'  # role is always teacher for this case
    Teacher_Data = All_data.get('Teacher')
    if User_data is None:
        return jsonify({"msg": "Bad request"}), 400

    new_user = User(**User_data)
    session.add(new_user)

    if ('diplomas' not in Teacher_Data
            or 'employment' not in Teacher_Data):
        return jsonify({"msg": "No diplomas or employment specified."}), 400
    diplomas = Teacher_Data['diplomas']
    employment = Teacher_Data['employment']
    new_teacher = Teacher(user=new_user, diplomas=diplomas, employment=employment)
    session.add(new_teacher)
    session.commit()
    return jsonify({"msg": "Teacher was created", "id": new_teacher.user_id}), 200


@teacher_api.route("/api/v1/teacher/<user_id>", methods=['GET'])
@jwt_required()
@teacher_required()
def get_teacher(user_id):
    session = Session()
    user = session.query(User)
    teacher = session.query(Teacher)
    currentTeacher = teacher.get(int(user_id))
    currentUser = user.get(int(user_id))

    if currentUser is None:
        return jsonify({"msg": "User doesn't exist"}), 404
    if currentTeacher is None:
        return jsonify({"msg": "Teacher doesn't exist"}), 404

    return jsonify({'user': currentUser.to_dict(),
                    'teacher': currentTeacher.to_dict()}), 200


@teacher_api.route("/api/v1/teacher/<user_id>", methods=['DELETE'])
@jwt_required()
@teacher_required()
def delete_user(user_id):
    session = Session()
    user = session.query(User)
    teacher = session.query(Teacher)
    sam = teacher.get(int(user_id))
    currentUser = user.get(int(user_id))
    if currentUser is None:
        return jsonify({"msg": "Teacher doesn't exist"}), 404
    session.delete(sam)
    session.delete(currentUser)
    session.commit()
    return jsonify({"msg": "Teacher was deleted"}), 200
