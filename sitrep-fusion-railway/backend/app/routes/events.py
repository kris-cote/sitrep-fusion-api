import json
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.db.session import get_db
from app.db.models import SensorEvent
from app.schemas import SensorEventIn, TrackOut
from app.services.fusion import fuse_event

router = APIRouter(prefix="/api/v1/events", tags=["events"])

def check_key(x_api_key: str | None):
    if settings.sitrep_api_key != "change-me" and x_api_key != settings.sitrep_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

@router.post("/ingest", response_model=TrackOut)
def ingest_event(payload: SensorEventIn, db: Session = Depends(get_db), x_api_key: str | None = Header(default=None)):
    check_key(x_api_key)
    event = SensorEvent(
        tenant_id=payload.tenant_id,
        source=payload.source,
        sensor_type=payload.sensor_type,
        object_type=payload.object_type,
        object_id=payload.object_id,
        lat=payload.lat,
        lon=payload.lon,
        altitude_m=payload.altitude_m,
        speed_mps=payload.speed_mps,
        heading_deg=payload.heading_deg,
        confidence=payload.confidence,
        raw_payload=json.dumps(payload.raw_payload),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    track = fuse_event(db, event)
    return TrackOut(
        id=track.id,
        tenant_id=track.tenant_id,
        label=track.label,
        object_type=track.object_type,
        lat=track.lat,
        lon=track.lon,
        altitude_m=track.altitude_m,
        speed_mps=track.speed_mps,
        heading_deg=track.heading_deg,
        confidence=track.confidence,
        threat_score=track.threat_score,
        threat_level=track.threat_level,
        sources=json.loads(track.sources or "[]"),
        explanation=track.explanation,
    )
