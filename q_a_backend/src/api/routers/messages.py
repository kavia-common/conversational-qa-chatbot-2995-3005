from datetime import datetime
from typing import List, Literal
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from src.services.session_store import SessionStore
from src.services.qa_service import QAService

router = APIRouter(prefix="/messages", tags=["messages"])
store = SessionStore.get_instance()
qa_service = QAService.get_instance()


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"] = Field(..., description="Message author role")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="UTC timestamp")


class SendMessageRequest(BaseModel):
    session_id: str = Field(..., description="Target session ID")
    message: str = Field(..., min_length=1, description="User message content")


class SendMessageResponse(BaseModel):
    session_id: str = Field(..., description="Target session ID")
    user_message: ChatMessage = Field(..., description="Echo of the user's message")
    assistant_message: ChatMessage = Field(..., description="Assistant reply")
    total_messages: int = Field(..., description="Total messages after send")


class ListMessagesResponse(BaseModel):
    session_id: str = Field(..., description="Target session ID")
    messages: List[ChatMessage] = Field(..., description="Chronological messages")


# PUBLIC_INTERFACE
@router.post(
    "",
    summary="Send Message",
    description="Send a user message and receive assistant reply within a session.",
    response_model=SendMessageResponse,
    operation_id="send_message",
)
def send_message(payload: SendMessageRequest):
    """Send a user message, generate assistant response, and store both.

    Args:
        payload: session_id, message

    Returns:
        SendMessageResponse: user and assistant messages with counts
    """
    if not store.get_session(payload.session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    # Store user message
    user_msg = store.add_message(payload.session_id, role="user", content=payload.message)

    # Generate assistant reply based on conversation state
    history = store.get_messages(payload.session_id)
    assistant_text = qa_service.answer(question=payload.message, history=history)
    assistant_msg = store.add_message(payload.session_id, role="assistant", content=assistant_text)

    total = store.get_message_count(payload.session_id)
    return SendMessageResponse(
        session_id=payload.session_id,
        user_message=ChatMessage(**user_msg),
        assistant_message=ChatMessage(**assistant_msg),
        total_messages=total,
    )


# PUBLIC_INTERFACE
@router.get(
    "",
    summary="List Messages",
    description="List messages for a given session.",
    response_model=ListMessagesResponse,
    operation_id="list_messages",
)
def list_messages(
    session_id: str = Query(..., description="Session ID to fetch messages for"),
):
    """List messages belonging to a session."""
    if not store.get_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")

    msgs = store.get_messages(session_id)
    return ListMessagesResponse(session_id=session_id, messages=[ChatMessage(**m) for m in msgs])
