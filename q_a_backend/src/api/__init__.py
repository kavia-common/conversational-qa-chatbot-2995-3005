"""
API package for Q&A backend.

Exposes submodules for routers to keep imports clean.
"""
from .routers import health, sessions, messages  # noqa: F401
