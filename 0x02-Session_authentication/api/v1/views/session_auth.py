#!/usr/bin/env python3
""" Module of Session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, Blueprint
from models.user import User
from os import getenv



app_views = Blueprint('app_views', __name__)


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
@app_views.route('/auth_session/login/', methods=['POST'], strict_slashes=False)
def login():
    """Authenticate user and create session."""
    auth = SessionAuth()

    # Retrieve email and password from request form
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email is missing or empty
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check if password is missing or empty
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for user by email
    user = User.search({'email': email})

    # Return error if no user found
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Check if password is valid
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session ID
    session_id = auth.create_session(user.id)

    # Create response with user JSON and set cookie
    response = jsonify(user.to_json())
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response
