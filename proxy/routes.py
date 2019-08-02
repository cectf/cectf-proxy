
import requests
from flask import Blueprint, current_app, request, Response
from flask_jwt import jwt_required, current_identity


def _proxy(new_url):
    new_url = request.url.replace(request.host_url, new_url + "/")
    print("Proxying", request.url, "to", new_url)
    resp = requests.request(
        method=request.method,
        url=new_url,
        headers={key: value for (key, value)
                 in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


static_bp = Blueprint("static_routes", __name__, url_prefix="/")


@static_bp.route('/login')
@static_bp.route('/login/')
@static_bp.route('/login/<path:path>')
@static_bp.route('/app')
@static_bp.route('/app/')
@static_bp.route('/app/<path:path>')
@static_bp.route('/admin')
@static_bp.route('/admin/')
@static_bp.route('/admin/<path:path>')
def frontend(path=None):
    return _proxy(current_app.config.get('TOPKEK_FRONTEND_URL'))


api_bp = Blueprint("api_routes", __name__, url_prefix="/api")


@api_bp.route('/login/<path:path>')
def api_login(path):
    return _proxy(current_app.config.get('TOPKEK_SERVER_URL'))


@api_bp.route('/app/<path:path>')
@jwt_required()
def api_app(path):
    return _proxy(current_app.config.get('TOPKEK_SERVER_URL'))


@api_bp.route('/admin/<path:path>')
@jwt_required()
def api_admin(path):
    return _proxy(current_app.config.get('TOPKEK_SERVER_URL'))


def init_app(app):
    app.register_blueprint(static_bp)
    app.register_blueprint(api_bp)
