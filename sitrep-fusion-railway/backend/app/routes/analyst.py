import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Track
from app.schemas import AnalystRequest

router = APIRouter(prefix="/api/v1/analyst", tags=["ai-analyst"])

@router.post("/explain")
def explain_track(payload: AnalystRequest, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == payload.track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    sources = json.loads(track.sources or "[]")
    recommendation = "Monitor only."
    if track.threat_score >= 75:
        recommendation = "Escalate to operations lead, cue secondary sensors, and notify relevant authority."
    elif track.threat_score >= 50:
        recommendation = "Increase monitoring, verify with independent source, and prepare response options."
    elif track.threat_score >= 25:
        recommendation = "Keep on watchlist and continue correlation."

    return {
        "track_id": track.id,
        "summary": f"{track.label} is assessed as {track.threat_level} with score {track.threat_score}/100.",
        "why": track.explanation,
        "sources": sources,
        "recommendation": recommendation,
    }
