
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
from typing import List
from sqlalchemy import exists

from errors.auth_errors import InsufficientRights
from errors.general_errors import InvalidRequest
from models.models import Request, ClassUser, Class, Role
from services.db import Session

student_api = Blueprint('student_api', __name__)


@student_api.route("/api/v1/student/request/<class_id>", methods=['POST'])
@jwt_required()
def send_request(class_id):
    with Session.begin() as session:
        if session.query(ClassUser).filter_by(user_id = current_user.id, class_id = int(class_id)).first():
            raise InvalidRequest("User has already been assigned to this class.")
        if session.query(Request).filter_by(user_id = current_user.id, class_id = int(class_id)).first() is not None:
            raise InvalidRequest("You have already sent a request to this class.")

        requests = Request(user_id=current_user.id, class_id=class_id)

        session.add(requests)
        session.commit()

        return jsonify({"msg": "The request has been sent"}), 200



    
@student_api.route("/api/v1/student/requests", methods=['GET'])
@jwt_required()
def get_student_requests():
    with Session(expire_on_commit=False) as session:
        user_id = current_user.id
        requests: List[Request] = session.query(Request).filter(Request.user_id == user_id)
        requests = [i.to_dict() for i in requests]
        
        return jsonify(requests), 200
