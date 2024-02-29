#!/usr/bin/env python3
"""Module for session authentication."""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session Authentication Class"""
    # Class attribute initialized by an empty dictionary
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id."""
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a Session ID using uuid4()
        session_id = str(uuid4())

        # Store the Session ID and user ID in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID."""
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the user ID associated with the session ID
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a User instance based on a cookie value."""
        if request is None:
            return None

        # Get the session ID from the cookie
        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        # Retrieve the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        # Retrieve the User instance from the database using the user ID
        return User.get(user_id)
