"""
Audit logging and regulatory compliance tests.
"""

def test_audit_log_tracking_and_admin_view(client, auth_headers):
    # Perform an action that logs an audit event
    client.post(
        "/api/v1/participants",
        headers=auth_headers["clinician"],
        json={"study_id": "PART-202"},
    )

    # Admin inspects audit trail
    audit_resp = client.get("/api/v1/audit/logs", headers=auth_headers["admin"])
    assert audit_resp.status_code == 200
    data = audit_resp.json()
    assert data["total"] >= 1
    actions = [item["action"] for item in data["items"]]
    assert "PARTICIPANT_REGISTERED" in actions

def test_non_admin_cannot_view_audit_logs(client, auth_headers):
    # Clinician trying to inspect audit trail
    resp = client.get("/api/v1/audit/logs", headers=auth_headers["clinician"])
    assert resp.status_code == 403
