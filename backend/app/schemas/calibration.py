"""
Pydantic schemas for scale and color calibration.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class CalibrationRequest(BaseModel):
    marker_type: str = Field(default="circle_10mm", json_schema_extra={"example": "circle_10mm"})
    known_dimension_mm: float = Field(default=10.0, gt=0.0)
    manual_points: Optional[List[List[float]]] = None  # [[x1, y1], [x2, y2]]

class CalibrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    image_id: str
    marker_type: str
    mm_per_pixel: float
    calibration_confidence: float
    color_card_detected: bool
    status: str
    created_at: datetime
