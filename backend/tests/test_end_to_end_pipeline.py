"""
End-to-End Vertical Slice Integration Test.
Verifies the complete pipeline:
User Login -> Register Participant -> Create Visit -> Ingest Image ->
Quality Check -> Calibrate -> Segment & Measure -> Clinician Review ->
Longitudinal Trajectory -> Research CSV Export.
"""

import os
from backend.app.models.participant import Participant
from backend.app.models.visit import Visit

def test_full_clinical_pipeline_vertical_slice(client, auth_headers):
    # 1. Clinician Authentication & Profile Verification
    me_resp = client.get("/api/v1/auth/me", headers=auth_headers["clinician"])
    assert me_resp.status_code == 200
    assert me_resp.json()["role"] == "clinician"

    # 2. Register Coded Research Participant (PART-500)
    p_resp = client.post(
        "/api/v1/participants",
        headers=auth_headers["clinician"],
        json={
            "study_id": "PART-500",
            "biological_sex": "male",
            "age_at_enrollment": 66,
            "enrollment_status": "active",
        },
    )
    assert p_resp.status_code == 201
    part_id = p_resp.json()["id"]

    # 3. Create Baseline Visit (V01, Day 0)
    v1_resp = client.post(
        f"/api/v1/participants/{part_id}/visits",
        headers=auth_headers["clinician"],
        json={
            "visit_code": "V01",
            "follow_up_day": 0,
            "wound_side": "left",
            "anatomical_location": "plantar_forefoot",
            "notes": "Baseline presentation. 10mm circular marker applied.",
        },
    )
    assert v1_resp.status_code == 201
    visit1_id = v1_resp.json()["id"]

    # 4. Ingest Baseline Synthetic Image with EXIF scrub
    baseline_img_path = "data/sample_synthetic/demo_wound_baseline.jpg"
    assert os.path.exists(baseline_img_path)
    
    with open(baseline_img_path, "rb") as f:
        upload_resp = client.post(
            f"/api/v1/visits/{visit1_id}/images",
            headers=auth_headers["clinician"],
            files={"file": ("demo_wound_baseline.jpg", f, "image/jpeg")},
            data={"view_label": "dorsal_aspect", "is_synthetic": True},
        )
    assert upload_resp.status_code == 201
    img1_id = upload_resp.json()["id"]
    assert upload_resp.json()["quality_passed"] is True
    assert upload_resp.json()["is_synthetic"] is True

    # 5. Ingest Degraded Blurry Image to Verify Rejection / Warning Flag
    blurry_img_path = "data/sample_synthetic/demo_wound_blurry.jpg"
    with open(blurry_img_path, "rb") as f:
        blurry_upload = client.post(
            f"/api/v1/visits/{visit1_id}/images",
            headers=auth_headers["clinician"],
            files={"file": ("demo_wound_blurry.jpg", f, "image/jpeg")},
            data={"view_label": "dorsal_aspect", "is_synthetic": True},
        )
    assert blurry_upload.status_code == 201
    assert blurry_upload.json()["quality_passed"] is False  # Flagged!

    # 6. Geometric Calibration on Baseline Image
    calib_resp = client.post(
        f"/api/v1/images/{img1_id}/calibrate",
        headers=auth_headers["clinician"],
        json={
            "marker_type": "circle_10mm",
            "known_dimension_mm": 10.0,
            "manual_points": [[120.0, 75.0], [120.0, 165.0]],  # 90px diameter
        },
    )
    assert calib_resp.status_code == 201
    mm_per_px = calib_resp.json()["mm_per_pixel"]
    assert abs(mm_per_px - (10.0 / 90.0)) < 0.01

    # 7. AI Segmentation & Measurement Assessment
    seg_resp = client.post(
        f"/api/v1/images/{img1_id}/segment",
        headers=auth_headers["clinician"],
        json={"model_name": "segformer-b0", "compute_uncertainty": True},
    )
    assert seg_resp.status_code == 201
    pred1 = seg_resp.json()
    pred1_id = pred1["id"]
    assert pred1["calibrated_area_cm2"] is not None
    assert pred1["calibrated_area_cm2"] > 0
    assert pred1["granulation_percentage"] > 0
    assert "uncertainty_score" in pred1

    # 8. Clinician Review & Sign-Off
    review_resp = client.post(
        f"/api/v1/predictions/{pred1_id}/clinician-review",
        headers=auth_headers["clinician"],
        json={
            "approved": True,
            "override_area_cm2": pred1["calibrated_area_cm2"],
            "notes": "Automated boundary verified. Agrees with clinical presentation.",
        },
    )
    assert review_resp.status_code == 201
    assert review_resp.json()["approved"] is True

    # 9. Create Follow-up Visit (V02, Day 14) and Assessment
    v2_resp = client.post(
        f"/api/v1/participants/{part_id}/visits",
        headers=auth_headers["clinician"],
        json={
            "visit_code": "V02",
            "follow_up_day": 14,
            "wound_side": "left",
            "anatomical_location": "plantar_forefoot",
            "notes": "Week 2 follow-up.",
        },
    )
    visit2_id = v2_resp.json()["id"]

    followup_img_path = "data/sample_synthetic/demo_wound_followup_v02.jpg"
    with open(followup_img_path, "rb") as f:
        up2 = client.post(
            f"/api/v1/visits/{visit2_id}/images",
            headers=auth_headers["clinician"],
            files={"file": ("followup.jpg", f, "image/jpeg")},
            data={"view_label": "dorsal_aspect", "is_synthetic": True},
        )
    img2_id = up2.json()["id"]

    client.post(
        f"/api/v1/images/{img2_id}/calibrate",
        headers=auth_headers["clinician"],
        json={"marker_type": "circle_10mm", "known_dimension_mm": 10.0},
    )
    client.post(
        f"/api/v1/images/{img2_id}/segment",
        headers=auth_headers["clinician"],
        json={"model_name": "segformer-b0"},
    )

    # 10. Longitudinal Progression Analysis
    prog_resp = client.get(
        f"/api/v1/participants/{part_id}/progression",
        headers=auth_headers["clinician"],
    )
    assert prog_resp.status_code == 200
    prog_data = prog_resp.json()
    assert prog_data["study_id"] == "PART-500"
    assert len(prog_data["points"]) == 2
    assert "Decreasing wound area alone does not prove complete tissue healing" in prog_data["clinical_notice"]

    # 11. De-identified Research CSV Export
    csv_resp = client.post(
        "/api/v1/research/exports/csv",
        headers=auth_headers["researcher"],
    )
    assert csv_resp.status_code == 200
    assert "PART-500" in csv_resp.text
    assert "study_id,biological_sex,age_at_enrollment" in csv_resp.text
