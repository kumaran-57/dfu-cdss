"""
Longitudinal wound trajectory analysis and healing rate computation.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

def analyze_wound_trajectory(
    visit_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes longitudinal progression indicators across multiple visits.
    visit_records: list of dicts with:
      visit_id, visit_code, visit_date, follow_up_day, calibrated_area_cm2,
      granulation_percentage, slough_percentage, necrotic_percentage, uncertainty_score, review_status
    """
    if not visit_records:
        return {
            "baseline_area_cm2": None,
            "latest_area_cm2": None,
            "total_area_change_percentage": None,
            "healing_trajectory_trend": "no_data",
            "healing_rate_cm2_per_week": None,
            "points": [],
            "clinical_notice": "No visit records available.",
        }

    # Sort chronological by follow_up_day or visit_date
    sorted_visits = sorted(visit_records, key=lambda v: (v["follow_up_day"], v["visit_date"]))
    
    baseline_point = sorted_visits[0]
    baseline_area = baseline_point.get("calibrated_area_cm2")
    
    points = []
    for v in sorted_visits:
        curr_area = v.get("calibrated_area_cm2")
        pct_change = None
        if baseline_area and baseline_area > 0 and curr_area is not None:
            pct_change = round(((curr_area - baseline_area) / baseline_area) * 100.0, 1)

        points.append({
            "visit_id": v["visit_id"],
            "visit_code": v["visit_code"],
            "visit_date": v["visit_date"],
            "follow_up_day": v["follow_up_day"],
            "calibrated_area_cm2": curr_area,
            "percentage_area_change": pct_change,
            "granulation_percentage": v.get("granulation_percentage"),
            "slough_percentage": v.get("slough_percentage"),
            "necrotic_percentage": v.get("necrotic_percentage"),
            "uncertainty_score": v.get("uncertainty_score"),
            "review_status": v.get("review_status", "pending"),
        })

    latest_point = points[-1]
    latest_area = latest_point.get("calibrated_area_cm2")
    total_change = latest_point.get("percentage_area_change")

    # Healing rate (cm^2 per week)
    healing_rate = None
    trend = "uncalibrated"
    if baseline_area is not None and latest_area is not None:
        total_days = max(1, latest_point["follow_up_day"] - baseline_point["follow_up_day"])
        weeks = total_days / 7.0
        if weeks > 0:
            # Negative delta means area shrank (healing progression)
            area_delta = latest_area - baseline_area
            healing_rate = round(area_delta / weeks, 2)

        if total_change is not None:
            if total_change <= -15.0:
                trend = "improving"
            elif total_change >= 15.0:
                trend = "deteriorating"
            else:
                trend = "stalled"

    clinical_notice = (
        "Longitudinal area change is an observational proxy. Decreasing wound area alone does not "
        "prove complete tissue healing or absent deep infection. Clinician review is mandatory."
    )

    return {
        "baseline_area_cm2": baseline_area,
        "latest_area_cm2": latest_area,
        "total_area_change_percentage": total_change,
        "healing_trajectory_trend": trend,
        "healing_rate_cm2_per_week": healing_rate,
        "points": points,
        "clinical_notice": clinical_notice,
    }
