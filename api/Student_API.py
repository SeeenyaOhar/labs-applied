from flask import make_response, Response, abort, request, Blueprint
from flask_jwt_extended import jwt_required, current_user

from Encoder import AlchemyEncoder
from errors.auth_errors import InsufficientRights
from models.models import Request, ClassUser, Class, Role
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

engine = create_engine("postgresql://postgres:admin@localhost:5432/Online-Classes-Service")
Session = sessionmaker(bind=engine)
session = Session()

student_api = Blueprint('student_api', __name__)


@student_api.route("/api/v1/<user_id>/request/<class_id>", methods=['POST'])
def send_request(user_id, class_id):
    try:
        requests = Request(user_id=user_id, class_id=class_id)
        session.add(requests)
        session.commit()
    except IntegrityError:
        return Response("Bad request", status=402)
    return Response("the request has been sent", status=200)


@student_api.route("/api/v1/<user_id>/classes", methods=['GET'])
@jwt_required()
def get_classes(user_id):
    if user_id != current_user.id and current_user.role != Role.teacher:
        raise InsufficientRights("Role should be teacher or you should be the owner of the resource")
    current = session.query(ClassUser).filter(ClassUser.user_id == user_id).all()
    dictclass = [elem.to_dict() for elem in current]

    current_Class = [session.query(Class).filter_by(id=i['class_id']).first().to_dict() for i in dictclass]

    if current_Class is None:
        return Response("class doesn't exist", status=404)
    return Response(
        response=json.dumps(current_Class, cls=AlchemyEncoder),
        status=200,
        mimetype='application/json'
    )
