#!/usr/bin/env python3
"""
This module contains views for Session
authentication routes
"""

from flask import request, jsonify, abort
from api.v1.app import app
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from models.user import User

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Handles user login/session creation &gets email/password from request form
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Find user by email
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Check password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(auth.SESSION_NAME, session_id)

    return response
