# Q&A Backend (FastAPI)

Backend for the Q&A chatbot. Provides REST endpoints for:
- Health (`GET /`)
- Sessions (`/sessions`)
- Messages (`/messages`)

Run locally:
- uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

Generate OpenAPI:
- python -m src.api.generate_openapi

Environment variables (create .env in container root or provide via deployment):
- CORS_ALLOW_ORIGINS: Comma-separated list of origins (default: "*")
- DATABASE_URL: Optional for future persistence

Notes:
- This version uses an in-memory store; data resets on restart.
- QA logic is a simple rule-based stub in src/services/qa_service.py and can be swapped with an LLM service later.
