from functools import wraps

from flask_jwt_extended import verify_jwt_in_request, get_jwt

from errors.auth_errors import InsufficientRights
from models.models import Role


def teacher_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            if 'role' in claims and claims['role'] == Role.teacher.name:
                return fn(*args, **kwargs)
            else:
                raise InsufficientRights("Not enough permission set to access this endpoint!")

        return decorator

    return wrapper
