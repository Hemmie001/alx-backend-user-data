#!/usr/bin/env python3
""" Module of Session Authentication
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication Class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a Session ID for a user_id."""
        if not isinstance(user_id, str) or user_id is None:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID."""
        if not isinstance(session_id, str) or session_id is None:
            return None

        return self.user_id_by_session_id.get(session_id)
