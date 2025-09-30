from __future__ import annotations
from typing import List, Dict, Optional
import re


class QAService:
    """Naive rule-based Q&A service (placeholder for LLM or retrieval)."""

    _instance: Optional["QAService"] = None

    def __init__(self):
        pass

    # PUBLIC_INTERFACE
    @classmethod
    def get_instance(cls) -> "QAService":
        """Return singleton instance of QAService."""
        if cls._instance is None:
            cls._instance = QAService()
        return cls._instance

    # PUBLIC_INTERFACE
    def answer(self, question: str, history: List[Dict]) -> str:
        """Produce an assistant reply based on the question and conversation history.

        This is a naive implementation and can be replaced with an LLM.
        """
        q = question.strip()
        if not q:
            return "Could you please provide more details about your question?"

        # Simple intents
        if re.search(r"\bhello|hi|hey\b", q, flags=re.IGNORECASE):
            return "Hello! How can I help you with your questions today?"
        if re.search(r"\bhelp\b", q, flags=re.IGNORECASE):
            return "Sure! Ask me any question. You can also create sessions to organize your topics."
        if q.endswith("?") and len(q) < 120:
            return f"Great question! While I don't have external knowledge yet, you asked: “{q}”. Could you add context so I can assist better?"

        # Use last context if available
        last_user = next((m for m in reversed(history) if m.get("role") == "user"), None)
        if last_user:
            return f"Continuing from your previous point: “{last_user.get('content', '')}”. Could you clarify what outcome you expect?"

        # Default fallback
        return "I'm here to help. Please ask a question, and I'll do my best to assist!"
