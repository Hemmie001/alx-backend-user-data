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
