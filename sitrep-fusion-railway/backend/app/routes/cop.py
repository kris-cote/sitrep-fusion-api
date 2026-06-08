import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Track
from app.schemas import TrackOut

router = APIRouter(prefix="/api/v1/cop", tags=["common-operational-picture"])

@router.get("/tracks", response_model=list[TrackOut])
def get_tracks(db: Session = Depends(get_db), tenant_id: str = "demo"):
    tracks = db.query(Track).filter(Track.tenant_id == tenant_id, Track.is_active == True).order_by(Track.threat_score.desc()).all()
    return [
        TrackOut(
            id=t.id,
            tenant_id=t.tenant_id,
            label=t.label,
            object_type=t.object_type,
            lat=t.lat,
            lon=t.lon,
            altitude_m=t.altitude_m,
            speed_mps=t.speed_mps,
            heading_deg=t.heading_deg,
            confidence=t.confidence,
            threat_score=t.threat_score,
            threat_level=t.threat_level,
            sources=json.loads(t.sources or "[]"),
            explanation=t.explanation,
        )
        for t in tracks
    ]
