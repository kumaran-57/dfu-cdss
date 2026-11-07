"""
Pytest configuration and test fixtures for DFU-XAI.
Uses an isolated in-memory SQLite database for high-speed, repeatable testing.
"""

import sys
try:
    if "multipart" not in sys.modules:
        import python_multipart
        sys.modules["multipart"] = python_multipart
except ImportError:
    pass

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from backend.app.core.database import Base, get_db
from backend.app.main import app
from backend.app.models.user import User, UserRole
from backend.app.security.password import get_password_hash
from backend.app.security.auth import create_access_token

# In-memory SQLite engine for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session():
    """Provides an isolated database session per test with rollback."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Override app dependency
    app.dependency_overrides[get_db] = lambda: session

    yield session

    session.close()
    transaction.rollback()
    connection.close()
    app.dependency_overrides.pop(get_db, None)

@pytest.fixture
def client(db_session):
    return TestClient(app)

@pytest.fixture
def seed_users(db_session):
    users = {
        "admin": User(
            email="admin@test.org",
            hashed_password=get_password_hash("AdminPass123!"),
            full_name="Test Administrator",
            role=UserRole.ADMIN.value,
            is_active=True,
        ),
        "clinician": User(
            email="clinician@test.org",
            hashed_password=get_password_hash("ClinicianPass123!"),
            full_name="Dr. Test Clinician",
            role=UserRole.CLINICIAN.value,
            is_active=True,
        ),
        "researcher": User(
            email="researcher@test.org",
            hashed_password=get_password_hash("ResearcherPass123!"),
            full_name="Test Researcher",
            role=UserRole.RESEARCHER.value,
            is_active=True,
        ),
        "viewer": User(
            email="viewer@test.org",
            hashed_password=get_password_hash("ViewerPass123!"),
            full_name="Test Viewer",
            role=UserRole.VIEWER.value,
            is_active=True,
        ),
    }
    for u in users.values():
        db_session.add(u)
    db_session.commit()
    for u in users.values():
        db_session.refresh(u)
    return users

@pytest.fixture
def auth_headers(seed_users):
    headers = {}
    for role, user in seed_users.items():
        token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )
        headers[role] = {"Authorization": f"Bearer {token}"}
    return headers
