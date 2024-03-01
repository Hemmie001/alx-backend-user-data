#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
# Import the necessary authentication classes
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth

# Import SessionAuth if AUTH_TYPE is set to session_auth
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize auth variable based on AUTH_TYPE
if auth_type == 'auth':
    auth = Auth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = SessionAuth()
elif auth_type == 'session_exp_auth':  # Add this condition
    auth = SessionExpAuth()
elif auth_type == 'session_db_auth':  # Add this condition
    auth = SessionDBAuth()


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden handler.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def authenticate_user():
    """Authenticates a user before processing a request.
    """
    if auth:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
        ]
        if auth.require_auth(request.path, excluded_paths):
            auth_header = auth.authorization_header(request)
            session_cookie = auth.session_cookie(request)
            if auth_header is None and session_cookie is None:
                abort(401)
            user = auth.current_user(request)
            if user is None:
                abort(403)
            request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
