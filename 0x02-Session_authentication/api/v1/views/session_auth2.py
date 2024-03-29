#!/usr/bin/env python3
""" Module of Session authentication views
"""


import os
from typing import Tuple
from flask import abort, jsonify, request
from api.v1.app import auth
from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login.

    Returns:
        - JSON representation of a User object.
    """
    # Get the email and password values from the form data
    email = request.form.get('email')
    password = request.form.get('password')
    # Return an error if the email is missing or empty
    if not email:
        return jsonify({"error": "email missing"}), 400
    # Return an error if the password is missing or empty
    if not password:
        return jsonify({"error": "password missing"}), 400
    # Retrieve the User instance based on the email
    user = User.search({'email': email})
    # Return an error if no User was found
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    # Return an error if the password is incorrect
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    # Otherwise, create a Session ID for the User ID
    # You must use auth.create_session(..) for creating a Session ID
    session_id = auth.create_session(getattr(user[0], 'id'))
    # Return the User in JSON format
    response = jsonify(user[0].to_json())
    # Set the cookie in the response
    response.set_cookie(os.getenv("SESSION_NAME"), session_id)
    # Return the response with the User and the cookie
    return response
