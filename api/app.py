from flask import Flask, jsonify
from api.User_API import user_api, Session
from api.Teacher_API import teacher_api
from api.Class_API import class_api
from api.Student_API import student_api
from flask_jwt_extended import JWTManager

from configuration.config import configure
from errors.auth_errors import InvalidCredentials, InsufficientRights
from models.models import User

app = Flask(__name__)

app.register_blueprint(user_api)

app.register_blueprint(teacher_api)

app.register_blueprint(class_api)

app.register_blueprint(student_api)
configure(app)

jwt = JWTManager(app)


@app.route("/api/v1/hello-world-19")
def hello_world():
    return "Hello, World 19"


@app.errorhandler(InvalidCredentials)
def invalid_credentials_handler(e):
    return jsonify({'msg': str(e)}), 401


@app.errorhandler(InsufficientRights)
def invalid_credentials_handler(e):
    return jsonify({'msg': str(e)}), 403


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    username = jwt_data["sub"]
    with Session.begin() as session:
        user = session.query(User).filter(User.username == username).first()
        session.expunge_all()

        if user is None:
            raise InvalidCredentials("sub is invalid")

        return user
