"""
Role-Based Access Control (RBAC) and Privilege Escalation prevention tests.
"""

def test_admin_can_create_user(client, auth_headers):
    response = client.post(
        "/api/v1/users",
        headers=auth_headers["admin"],
        json={
            "email": "newclinician@test.org",
            "password": "Password123!",
            "full_name": "New Clinician",
            "role": "clinician",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "newclinician@test.org"
    assert response.json()["role"] == "clinician"

def test_clinician_cannot_create_user(client, auth_headers):
    """Verifies that clinicians cannot escalate privilege to create users."""
    response = client.post(
        "/api/v1/users",
        headers=auth_headers["clinician"],
        json={
            "email": "hacked@test.org",
            "password": "Password123!",
            "role": "admin",
        },
    )
    assert response.status_code == 403
    assert "Access forbidden" in response.json()["detail"]

def test_viewer_cannot_register_participant(client, auth_headers):
    """Verifies that viewers cannot write or modify participant records."""
    response = client.post(
        "/api/v1/participants",
        headers=auth_headers["viewer"],
        json={
            "study_id": "PART-099",
            "biological_sex": "female",
            "age_at_enrollment": 55,
        },
    )
    assert response.status_code == 403

def test_clinician_can_register_participant(client, auth_headers):
    response = client.post(
        "/api/v1/participants",
        headers=auth_headers["clinician"],
        json={
            "study_id": "PART-001",
            "biological_sex": "male",
            "age_at_enrollment": 62,
        },
    )
    assert response.status_code == 201
    assert response.json()["study_id"] == "PART-001"
