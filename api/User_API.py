import bcrypt
from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user, create_access_token
from sqlalchemy.exc import IntegrityError

from errors.auth_errors import InsufficientRights
from models.models import User, Role
from services.db import Session
from services.jwt import teacher_required

user_api = Blueprint('user_api', __name__)


@user_api.route("/api/v1/user", methods=['POST'])
def create_user():
    session = Session()
    user_data = request.get_json()

    if user_data is None:
        return jsonify({"msg": "Bad request"}), 400

    user_data['role'] = Role.student

    new_user = User(**user_data)
    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        return jsonify({"msg": "Create failed"}), 400

    return jsonify({"msg": "User has been created", "id": new_user.id}), 200


@user_api.route("/api/v1/user/<user_id>", methods=['GET'])
@jwt_required()
@teacher_required()
def get_user(user_id):
    with Session() as session:
        user = session.query(User)
        currentUser = user.get(int(user_id))

        if currentUser is None:
            return jsonify({"msg": "User doesn't exist"}), 404
        if current_user.id != user_id and current_user.role != Role.teacher:
            raise InsufficientRights("Role should be teacher or you should be the owner of the resource")

        return jsonify(currentUser.to_dict()), 200


@user_api.route("/api/v1/user/<user_id>", methods=['DELETE'])
@jwt_required()
@teacher_required()
def delete_user(user_id):
    with Session.begin() as session:
        user = session.query(User)
        currentUser = user.get(int(user_id))
        if currentUser is None:
            return jsonify({"msg": "User doesn't exist"}), 404

        session.delete(currentUser)
    return jsonify({"msg": "User was deleted"}), 200


@user_api.route("/api/v1/user/login", methods=['GET'])
def login_user():
    data = request.get_json()
    if data is None:
        return jsonify({"msg": "No JSON data has been specified!"}), 400
    try:
        if 'password' in data and 'username' in data:
            with Session.begin() as session:
                user = session.query(User).filter_by(username=data['username']).first()

                if not bcrypt.checkpw(data['password'].encode("utf-8"), user.password.encode("utf-8")):
                    return jsonify({"msg": "Invalid password or username specified"}), 404

                access_token = create_access_token(identity=data['username'],
                                                   additional_claims={'role': user.role.name})
                return jsonify(access_token=access_token), 200
    except IntegrityError:
        return jsonify({"msg": "Invalid username or password specified"}), 400

    return jsonify({"msg": "Invalid request body, specify password and username}, please!"}), 400


@user_api.route("/api/v1/user", methods=['PUT'])
@jwt_required()
def update_user():
    with Session() as session:
        user_data = request.get_json()

        if 'id' in user_data and current_user.id != user_data['id']:
            raise InsufficientRights("User not found")
        if user_data is None:
            return jsonify({"msg": "Bad request"}, 400)

        user = User(**user_data)
        user_id = user_data.get('id')
        if user_id is not None:
            try:
                session.query(User).filter(User.id == user.id).\
                    update(user_data, synchronize_session="fetch")
                session.commit()
            except IntegrityError:
                return jsonify({"msg": "Update failed"}), 400
            return jsonify({"msg": "User was updated"}), 200

    return jsonify({"msg": "Update failed"}), 400
