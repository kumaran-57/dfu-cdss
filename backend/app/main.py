"""
DFU-XAI FastAPI Main Application Entrypoint.
"""

import sys
from contextlib import asynccontextmanager

# Python-multipart bridge for Debian/Kali environments
try:
    if "multipart" not in sys.modules:
        import python_multipart
        sys.modules["multipart"] = python_multipart
except ImportError:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import init_db, SessionLocal
from backend.app.models.user import User, UserRole
from backend.app.security.password import get_password_hash
from backend.app.api.v1 import api_router

def seed_initial_users():
    """Seeds standard role accounts if database is empty."""
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            demo_accounts = [
                ("admin@dfuxai.local", "AdminPass123!", "System Administrator", UserRole.ADMIN.value),
                ("clinician@dfuxai.local", "ClinicianPass123!", "Dr. Jane Smith, MD", UserRole.CLINICIAN.value),
                ("researcher@dfuxai.local", "ResearcherPass123!", "Alex Vance, MSc", UserRole.RESEARCHER.value),
                ("viewer@dfuxai.local", "ViewerPass123!", "Guest Auditor", UserRole.VIEWER.value),
            ]
            for email, password, name, role in demo_accounts:
                u = User(
                    email=email,
                    hashed_password=get_password_hash(password),
                    full_name=name,
                    role=role,
                    is_active=True,
                )
                db.add(u)
            db.commit()
            print("[Bootstrap] Default research accounts initialized.")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed default accounts
    init_db()
    seed_initial_users()
    yield
    # Shutdown

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Research decision-support API for standardized smartphone diabetic foot ulcer "
        "assessment, geometric scale calibration, segmentation, and longitudinal monitoring."
    ),
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "docs_url": "/docs",
        "clinical_disclaimer": settings.CLINICAL_DISCLAIMER,
    }

@app.get("/health")
def root_health():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "clinical_disclaimer": settings.CLINICAL_DISCLAIMER,
    }
