"""
Participant and Visit management tests.
"""

def test_participant_and_visit_lifecycle(client, auth_headers):
    # 1. Register Participant
    resp = client.post(
        "/api/v1/participants",
        headers=auth_headers["clinician"],
        json={
            "study_id": "PART-101",
            "biological_sex": "female",
            "age_at_enrollment": 58,
        },
    )
    assert resp.status_code == 201
    part_id = resp.json()["id"]

    # 2. Duplicate Study ID Rejected
    dup_resp = client.post(
        "/api/v1/participants",
        headers=auth_headers["clinician"],
        json={"study_id": "PART-101"},
    )
    assert dup_resp.status_code == 400

    # 3. Create Baseline Visit
    v_resp = client.post(
        f"/api/v1/participants/{part_id}/visits",
        headers=auth_headers["clinician"],
        json={
            "visit_code": "V01",
            "follow_up_day": 0,
            "wound_side": "right",
            "anatomical_location": "plantar_hallux",
        },
    )
    assert v_resp.status_code == 201
    visit_id = v_resp.json()["id"]

    # 4. Attach Clinical Observation
    obs_resp = client.post(
        f"/api/v1/visits/{visit_id}/observations",
        headers=auth_headers["clinician"],
        json={
            "hba1c_percentage": 8.4,
            "neuropathy_present": True,
            "abi_index": 0.82,
            "infection_status": "superficial",
            "offloading_modality": "removable_boot",
        },
    )
    assert obs_resp.status_code == 201
    assert obs_resp.json()["hba1c_percentage"] == 8.4

    # 5. List Observations
    list_obs = client.get(
        f"/api/v1/visits/{visit_id}/observations",
        headers=auth_headers["clinician"],
    )
    assert list_obs.status_code == 200
    assert len(list_obs.json()) == 1
