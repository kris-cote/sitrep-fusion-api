from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime

class SensorEventIn(BaseModel):
    tenant_id: str = "demo"
    source: str
    sensor_type: str
    object_type: str
    object_id: Optional[str] = None
    lat: float
    lon: float
    altitude_m: Optional[float] = None
    speed_mps: Optional[float] = None
    heading_deg: Optional[float] = None
    confidence: float = Field(default=0.5, ge=0, le=1)
    raw_payload: dict[str, Any] = {}

class SensorEventOut(SensorEventIn):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class TrackOut(BaseModel):
    id: str
    tenant_id: str
    label: str
    object_type: str
    lat: float
    lon: float
    altitude_m: Optional[float] = None
    speed_mps: Optional[float] = None
    heading_deg: Optional[float] = None
    confidence: float
    threat_score: int
    threat_level: str
    sources: list[str]
    explanation: str

class AnalystRequest(BaseModel):
    track_id: str
