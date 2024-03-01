#!/usr/bin/env python3
"""
Module that contains views for Session
authentication routes
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def get_user_for_session_auth():
    """
    Get's user based on request data
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email == "" or email is None:
        return jsonify({"error": "email missing"}), 400
    if password == "" or password is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            cookie = os.getenv('SESSION_NAME')
            session = auth.create_session(user.id)
            resp = jsonify(user.to_json())
            resp.set_cookie(cookie, session)
            return resp
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def delete_user_session():
    """
    Deletes user session
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
