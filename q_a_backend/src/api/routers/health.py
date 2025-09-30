from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")


# PUBLIC_INTERFACE
@router.get(
    "/",
    summary="Health Check",
    description="Returns the service health status.",
    response_model=HealthResponse,
    operation_id="health_check",
)
def health_check():
    """Root endpoint to verify the service is running.

    Returns:
        HealthResponse: status, service, and version information.
    """
    return HealthResponse(status="ok", service="q_a_backend", version="1.0.0")
