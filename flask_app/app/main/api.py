from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)


@api_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')


    if password != 'strong_password':
        return jsonify({"message": "Invalid username or password"}), 401

    token_exp = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode({'username': username, 'exp': token_exp}, 'SECRET_KEY', algorithm='HS256')

    return jsonify({"token": token})

from flask import Blueprint, request, abort
from functools import wraps
import jwt

api_bp = Blueprint('api', __name__)


def check_token(token):
    try:
        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
        if payload['username'] in ['admin', 'user', 'root']:
            return True
        return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


def authorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401)
        token = token.split(' ')[1] if token.startswith('Bearer ') else None
        if not token or not check_token(token):
            abort(401)
        return func(*args, **kwargs)
    return wrapper


@api_bp.route('/protected')
@authorize
def protected_route():
    return 'Access granted'

