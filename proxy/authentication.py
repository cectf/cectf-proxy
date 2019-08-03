
from flask import jsonify, session
from werkzeug.security import safe_str_cmp
from flask_jwt import JWT
from proxy import user_client


def authenticate(username, password):
    user = user_client.get_user_by_username(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return user_client.get_user_by_id(user_id)


def auth_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'admin': identity.admin
    })


def init_app(app):
    jwt = JWT(app, authenticate, identity)
    jwt.auth_response_callback = auth_response_handler
