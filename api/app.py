from flask import Flask
from User_API import user_api
from Teacher_API import teacher_api
from Class_API import class_api
from Student_API import student_api

app = Flask(__name__)

app.register_blueprint(user_api)

app.register_blueprint(teacher_api)

app.register_blueprint(class_api)

app.register_blueprint(student_api)


@app.route("/api/v1/hello-world-19")
def hello_world():
    return "Hello, World 19"
