from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid


@dataclass
class _Session:
    session_id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[Dict] = field(default_factory=list)


class SessionStore:
    """Simple in-memory session storage. Replaceable with persistent DB."""

    _instance: Optional["SessionStore"] = None

    def __init__(self):
        self._sessions: Dict[str, _Session] = {}

    # PUBLIC_INTERFACE
    @classmethod
    def get_instance(cls) -> "SessionStore":
        """Return singleton instance of SessionStore."""
        if cls._instance is None:
            cls._instance = SessionStore()
        return cls._instance

    # PUBLIC_INTERFACE
    def create_session(self, title: Optional[str] = None) -> Dict:
        """Create and store a new session."""
        now = datetime.now(timezone.utc)
        sid = str(uuid.uuid4())
        session = _Session(
            session_id=sid,
            title=title or "New Chat",
            created_at=now,
            updated_at=now,
        )
        self._sessions[sid] = session
        return self._to_public(session)

    # PUBLIC_INTERFACE
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get a session by ID, or None if not found."""
        s = self._sessions.get(session_id)
        return self._to_public(s) if s else None

    # PUBLIC_INTERFACE
    def list_sessions(self, skip: int = 0, limit: int = 50) -> List[Dict]:
        """Return a list of sessions with pagination."""
        all_sessions = list(self._sessions.values())
        sliced = all_sessions[skip : skip + limit]
        return [self._to_public(s) for s in sliced]

    # PUBLIC_INTERFACE
    def delete_session(self, session_id: str) -> bool:
        """Delete a session by ID. Returns True if deleted."""
        return self._sessions.pop(session_id, None) is not None

    # PUBLIC_INTERFACE
    def add_message(self, session_id: str, role: str, content: str) -> Dict:
        """Append a message to a session and update timestamps."""
        s = self._sessions.get(session_id)
        if not s:
            raise KeyError("Session not found")
        now = datetime.now(timezone.utc)
        msg = {
            "role": role,
            "content": content,
            "timestamp": now,
        }
        s.messages.append(msg)
        s.updated_at = now
        return msg

    # PUBLIC_INTERFACE
    def get_messages(self, session_id: str) -> List[Dict]:
        """Get messages for a session, or empty list if none."""
        s = self._sessions.get(session_id)
        return list(s.messages) if s else []

    # PUBLIC_INTERFACE
    def get_message_count(self, session_id: str) -> int:
        """Get message count for a session."""
        s = self._sessions.get(session_id)
        return len(s.messages) if s else 0

    def _to_public(self, s: _Session) -> Dict:
        return {
            "session_id": s.session_id,
            "title": s.title,
            "created_at": s.created_at,
            "updated_at": s.updated_at,
            "message_count": len(s.messages),
        }
