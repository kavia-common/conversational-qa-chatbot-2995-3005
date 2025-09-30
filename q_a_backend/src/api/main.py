from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import health, sessions, messages
from src.core.openapi import get_openapi_schema
from src.core.settings import settings

app = FastAPI(
    title="Q&A Chatbot API",
    description="Backend REST API for the Q&A chatbot with session management and conversational Q&A.",
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Service health and status"},
        {"name": "sessions", "description": "Chat session lifecycle and listing"},
        {"name": "messages", "description": "Send/receive chat messages inside a session"},
    ],
)

# Configure CORS for Angular frontend consumption
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(sessions.router)
app.include_router(messages.router)


# PUBLIC_INTERFACE
@app.get("/openapi.json", include_in_schema=False)
def custom_openapi():
    """Return custom OpenAPI schema with app-level metadata."""
    return get_openapi_schema(app)
