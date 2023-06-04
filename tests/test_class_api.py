from api.app import app as flask_app
from models.models import Class
from flask.testing import FlaskClient
import pytest
from pytest_mock import MockerFixture
import flask_jwt_extended

@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield flask_app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


# (GET) /api/v1/class/<class_id>
get_class_url = '/api/v1/class'

mock_class = Class(id=1, title='Hello', description='Hello world', teacher_id=2)
def test_when_getting_class_return_proper_one(client: FlaskClient, mocker: MockerFixture):
    mocker.patch('services.classes.get_cls', return_value=mock_class)
    mocker.patch('models.models.Class.to_dict', return_value={'title': mock_class.title})

    response = client.get(f'{get_class_url}/1')
    print(response.json)
    assert 200 == response.status_code
    assert 'title' in response.json
    assert 'id' not in response.json
    assert mock_class.title == response.json['title']


def test_when_class_doesnt_exists_return_404(client: FlaskClient, mocker):
    mocker.patch('services.classes.get_cls', return_value=None)

    response = client.get(f'{get_class_url}/1')
    print(response.json)
    assert 404 == response.status_code


# (DELETE) /api/v1/class
delete_class_url = '/api/v1/class'


def test_when_deleting_class_return_200(client: FlaskClient, mocker: MockerFixture):
    mocker.patch('services.classes.get_cls', return_value=mock_class)
    mocker.patch('services.classes.delete_cls')
    mocker.patch.object(flask_jwt_extended, 'jwt_required')
    mocker.patch('services.jwt.teacher_required')

    response = client.delete(f'{get_class_url}/1')
    assert 200 == response.status_code