"""
API v1 Router aggregation.
"""

from fastapi import APIRouter
from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.users import router as users_router
from backend.app.api.v1.participants import router as participants_router
from backend.app.api.v1.visits import router as visits_router
from backend.app.api.v1.images import router as images_router
from backend.app.api.v1.calibration import router as calibration_router
from backend.app.api.v1.assessments import router as assessments_router
from backend.app.api.v1.longitudinal import router as longitudinal_router
from backend.app.api.v1.audit import router as audit_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(participants_router)
api_router.include_router(visits_router)
api_router.include_router(images_router)
api_router.include_router(calibration_router)
api_router.include_router(assessments_router)
api_router.include_router(longitudinal_router)
api_router.include_router(audit_router)
