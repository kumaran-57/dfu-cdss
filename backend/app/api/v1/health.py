"""
System Healthcheck API.
"""

from fastapi import APIRouter
from backend.app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def healthcheck():
    """Health status and clinical safety notice."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "clinical_disclaimer": settings.CLINICAL_DISCLAIMER,
    }
