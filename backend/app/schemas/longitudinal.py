"""
Pydantic schemas for Longitudinal Wound Trajectory Analysis.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class VisitTrajectoryPoint(BaseModel):
    visit_id: str
    visit_code: str
    visit_date: datetime
    follow_up_day: int
    calibrated_area_cm2: Optional[float]
    percentage_area_change: Optional[float]  # % relative to baseline
    granulation_percentage: Optional[float]
    slough_percentage: Optional[float]
    necrotic_percentage: Optional[float]
    uncertainty_score: Optional[float]
    review_status: str

class LongitudinalTrajectoryResponse(BaseModel):
    participant_id: str
    study_id: str
    baseline_area_cm2: Optional[float]
    latest_area_cm2: Optional[float]
    total_area_change_percentage: Optional[float]
    healing_trajectory_trend: str  # improving, stalled, deteriorating, uncalibrated
    healing_rate_cm2_per_week: Optional[float]
    points: List[VisitTrajectoryPoint]
    clinical_notice: str
