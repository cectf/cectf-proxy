import os
import requests

from flask import Flask, request, redirect, Response
from flask_jwt import JWT, jwt_required, current_identity
from proxy import auth


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


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    auth.init_app(app)

    @app.route('/login')
    @app.route('/login/')
    @app.route('/login/<path:path>')
    def frontend_login(path=None):
        return _proxy(app.config.get('TOPKEK_FRONTEND_URL'))

    @app.route('/app')
    @app.route('/app/')
    @app.route('/app/<path:path>')
    def frontend_app(path=None):
        return _proxy(app.config.get('TOPKEK_FRONTEND_URL'))

    @app.route('/admin')
    @app.route('/admin/')
    @app.route('/admin/<path:path>')
    def frontend_admin(path=None):
        return _proxy(app.config.get('TOPKEK_FRONTEND_URL'))

    @app.route('/api/login/<path:path>')
    def api_login(path):
        return _proxy(app.config.get('TOPKEK_SERVER_URL'))

    @app.route('/api/app/<path:path>')
    @jwt_required()
    def api_app(path):
        return _proxy(app.config.get('TOPKEK_SERVER_URL'))

    @app.route('/api/admin/<path:path>')
    @jwt_required()
    def api_admin(path):
        return _proxy(app.config.get('TOPKEK_SERVER_URL'))

    return app
