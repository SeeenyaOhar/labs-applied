from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import exists

from errors.auth_errors import InsufficientRights
from errors.general_errors import ResourceNotFound, InvalidRequest
from models.models import Message, Class, ClassUser
from services.db import Session

messages_api = Blueprint('messages_api', __name__)


def authorize_class(class_id, session):
    if class_id is None:
        raise InvalidRequest("Class id has not been specified")

    class_ = session.query(Class).filter(Class.id == class_id).first()

    if class_ is None:
        raise ResourceNotFound("Such class doesn't exist")

    if class_.teacher_id != current_user.id and \
            not session.query(exists().where(ClassUser.user_id == current_user.id)).scalar():
        raise InsufficientRights("Not enough rights to access the messages of this class")


def auth_message(message_id, session, type='private'):
    """
    Used to authorize for get, put and delete.
    :param type: Type of authorization
    :param message_id: The id of the message.
    :param session: The SQL Alchemy Session.
    """
    if message_id is None:
        raise InvalidRequest("Class id has not been specified")

    message = session.query(Message).filter(Message.id == message_id).first()

    if message is None:
        raise ResourceNotFound("Such message doesn't exist")

    if type == 'private':
        if message.user == current_user.id:
            return

    elif type == 'public':
        if message.user == current_user.id or \
                session.query(exists().where(ClassUser.user_id == current_user.id and ClassUser.class_id == message.class_)).scalar():
            return

    raise InsufficientRights("Not enough rights to access the messages of this class")


@messages_api.route("/api/v1/class/messages/<class_id>", methods=['GET'])
@jwt_required()
def get_messages(class_id):
    with Session.begin() as session:
        authorize_class(class_id, session)

        messages = session.query(Message).filter(Message.class_ == class_id).all()
        messages = [message.to_dict() for message in messages]

        return jsonify(messages), 200


@messages_api.route("/api/v1/class/message", methods=['GET'])
@jwt_required()
def get_message():
    data = request.json
    message_id = data.get('id')

    if message_id is None:
        raise InvalidRequest("Id of the message has not been specified. "
                             "Check out the documentation to learn more(hint: id should be in the JSON for this "
                             "request)")
    with Session.begin() as session:
        auth_message(message_id, session)

        message = session.query(Message).filter(Message.id == message_id).first()

        if message is None:
            raise ResourceNotFound("Message has not been found")

        return jsonify(message.to_dict()), 200


@messages_api.route("/api/v1/class/message", methods=['POST'])
@jwt_required()
def create_message():
    data = request.json

    if data is None:
        return jsonify({"msg": "JSON Data is empty!"}), 400

    with Session() as session:
        class_id = data.get('class_')
        authorize_class(class_id, session)
        if 'date' in data:
            raise InvalidRequest("Date should not be specified. \n"
                                 "We still are going to use the current date and time")

        data['date'] = datetime.now()
        data['user'] = current_user.id
        message = Message(**data)

        session.add(message)
        session.commit()

        return jsonify({"msg": "Successfully added the message to the class", "id": message.id}), 200


@messages_api.route("/api/v1/class/message", methods=['PUT'])
@jwt_required()
def update_message():
    data = request.json

    if data is None:
        return jsonify({"msg": "JSON Data is empty!"}), 400

    with Session() as session:
        auth_message(data.get('id'), session)

        message = Message(**data)
        session.query(Message) \
            .filter(Message.id == message.id) \
            .update(data, synchronize_session="fetch")

    return jsonify({"msg": "Message has been successfully updated!"}), 200


@messages_api.route("/api/v1/class/message", methods=['DELETE'])
@jwt_required()
def delete_message():
    data = request.json

    if data is None:
        return jsonify({"msg": "JSON Data is empty!"}), 400

    with Session() as session:
        auth_message(data.get('id'), session)

        message = session.query(Message) \
            .filter(Message.id == data.get('id')).first()
        session.delete(message)

    return jsonify({"msg": "Message has been successfully deleted!"}), 200
