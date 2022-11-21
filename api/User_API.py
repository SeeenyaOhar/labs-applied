import bcrypt
from flask import make_response, Response, request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, current_user, create_access_token

from Encoder import AlchemyEncoder
from errors.auth_errors import InsufficientRights
from models.models import User, Role
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine("postgresql://postgres:admin@localhost:5432/Online-Classes-Service")
Session = sessionmaker(bind=engine)
session = Session()

user_api = Blueprint('user_api', __name__)


@user_api.route("/api/v1/user", methods=['POST'])
def create_user():
    user_data = request.get_json()

    if user_data is None:
        return Response("Bad request", status=400)

    new_user = User(**user_data)
    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        return Response("Create failed", status=402)
    return Response("user was created", status=200)


@user_api.route("/api/v1/user/<userId>", methods=['GET'])
@jwt_required()
def get_user(userId):
    user = session.query(User)
    currentUser = user.get(int(userId))
    if currentUser is None:
        return Response("User doesn't exist", status=404)
    if current_user.id != userId and current_user.role != Role.teacher:
        raise InsufficientRights("Role should be teacher or you should be the owner of the resource")
    return Response(
        response=json.dumps(currentUser.to_dict(), cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )


@user_api.route("/api/v1/user/<userId>", methods=['DELETE'])
@jwt_required()
def delete_user(userId):
    if current_user.role != Role.teacher:
        raise InsufficientRights("Role should be teacher")
    user = session.query(User)
    currentUser = user.get(int(userId))
    if currentUser is None:
        return Response("User doesn't exist", status=404)

    try:
        session.delete(currentUser)
        session.commit()
    except IntegrityError:
        return Response("Delete failed", status=402)
    return Response("User was deleted", status=200)


@user_api.route("/api/v1/user/login", methods=['GET'])
def login_user():
    data = request.get_json()
    if data is None:
        return Response("No JSON data has been specified!", status=400)
    try:
        if 'password' in data and 'username' in data:
            with Session.begin() as session:
                user = session.query(User).filter_by(username=data['username']).first()
                if not bcrypt.checkpw(data['password'].encode("utf-8"), user.password.encode("utf-8")):
                    return Response("Invalid password or username specified", status=404)
                access_token = create_access_token(identity=data['username'])
                return jsonify(access_token=access_token), 200
    except IntegrityError:
        return Response("Invalid username or password specified", status=400)

    return Response("Invalid request body, specify password and username, please!", status=400)


@user_api.route("/api/v1/user", methods=['PUT'])
@jwt_required()
def update_user():
    user_data = request.get_json()
    if ('id' in user_data and current_user.id != user_data['id']):
        raise InsufficientRights("User not found")
    if user_data is None:
        return Response("Bad request", status=400)
    user = User(**user_data)
    if 'id' in user_data:
        try:
            session.query(User).filter(User.id == user.id).update(user.to_dict(), synchronize_session="fetch")
            session.commit()
        except IntegrityError:
            return Response("Update failed", status=402)
        return Response("User was updated", status=200)
    return Response("Bad request", status=400)
