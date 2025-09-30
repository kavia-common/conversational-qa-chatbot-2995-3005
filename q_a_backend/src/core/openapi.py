from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi as _get_openapi


# PUBLIC_INTERFACE
def get_openapi_schema(app: FastAPI) -> dict:
    """Generate and return the OpenAPI schema with custom metadata."""
    if app.openapi_schema:
        return app.openapi_schema

    schema = _get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["info"]["x-theme"] = {
        "name": "Ocean Professional",
        "colors": {
            "primary": "#2563EB",
            "secondary": "#F59E0B",
            "error": "#EF4444",
            "background": "#f9fafb",
            "surface": "#ffffff",
            "text": "#111827",
        },
    }
    app.openapi_schema = schema
    return app.openapi_schema
