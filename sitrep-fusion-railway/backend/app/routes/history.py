import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import SensorEvent

router = APIRouter(prefix="/api/v1/history", tags=["history"])

@router.get("/track/{label}")
def get_track_history(label: str, db: Session = Depends(get_db), tenant_id: str = "demo"):
    events = db.query(SensorEvent).filter(
        SensorEvent.tenant_id == tenant_id,
        SensorEvent.object_id == label
    ).order_by(SensorEvent.created_at.asc()).all()

    return [
        {
            "id": e.id,
            "time": e.created_at,
            "source": e.source,
            "sensor_type": e.sensor_type,
            "object_type": e.object_type,
            "object_id": e.object_id,
            "lat": e.lat,
            "lon": e.lon,
            "altitude_m": e.altitude_m,
            "speed_mps": e.speed_mps,
            "heading_deg": e.heading_deg,
            "confidence": e.confidence,
            "raw_payload": json.loads(e.raw_payload or "{}"),
        }
        for e in events
    ]
