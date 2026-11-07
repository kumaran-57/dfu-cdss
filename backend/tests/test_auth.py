"""
Authentication and credential verification tests.
"""

def test_login_success(client, seed_users):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "clinician@test.org", "password": "ClinicianPass123!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "clinician"
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, seed_users):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "clinician@test.org", "password": "WrongPassword!"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_login_nonexistent_user(client, seed_users):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "unknown@test.org", "password": "SomePassword123!"},
    )
    assert response.status_code == 401

def test_get_current_user_profile(client, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers["clinician"])
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "clinician@test.org"
    assert data["role"] == "clinician"

def test_get_profile_unauthorized(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401 or response.status_code == 403
