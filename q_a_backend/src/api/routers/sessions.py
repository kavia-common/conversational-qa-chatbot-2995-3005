from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from src.services.session_store import SessionStore

router = APIRouter(prefix="/sessions", tags=["sessions"])
store = SessionStore.get_instance()


class SessionCreateRequest(BaseModel):
    title: Optional[str] = Field(None, description="Optional title for the chat session")


class SessionResponse(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    title: str = Field(..., description="Session title")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")
    message_count: int = Field(..., description="Number of messages in the session")


# PUBLIC_INTERFACE
@router.post(
    "",
    summary="Create Session",
    description="Create a new chat session and return its details.",
    response_model=SessionResponse,
    operation_id="create_session",
)
def create_session(payload: SessionCreateRequest):
    """Create a new chat session.

    Args:
        payload: optional title

    Returns:
        SessionResponse: the created session metadata.
    """
    session = store.create_session(title=payload.title)
    return SessionResponse(**session)


# PUBLIC_INTERFACE
@router.get(
    "/{session_id}",
    summary="Get Session",
    description="Get a chat session by its ID.",
    response_model=SessionResponse,
    operation_id="get_session",
)
def get_session(session_id: str):
    """Get a session by ID.

    Args:
        session_id: ID of the session

    Returns:
        SessionResponse: session metadata

    Raises:
        HTTPException: 404 if not found
    """
    session = store.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionResponse(**session)


# PUBLIC_INTERFACE
@router.get(
    "",
    summary="List Sessions",
    description="List chat sessions with optional pagination.",
    response_model=List[SessionResponse],
    operation_id="list_sessions",
)
def list_sessions(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(50, gt=0, le=200, description="Maximum number of items to return"),
):
    """List sessions.

    Args:
        skip: skip count
        limit: page size

    Returns:
        List[SessionResponse]: sessions
    """
    sessions = store.list_sessions(skip=skip, limit=limit)
    return [SessionResponse(**s) for s in sessions]


# PUBLIC_INTERFACE
@router.delete(
    "/{session_id}",
    summary="Delete Session",
    description="Delete a chat session by its ID.",
    operation_id="delete_session",
)
def delete_session(session_id: str):
    """Delete a session by ID."""
    deleted = store.delete_session(session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"deleted": True, "session_id": session_id}
