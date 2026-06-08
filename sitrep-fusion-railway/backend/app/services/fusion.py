import json
from sqlalchemy.orm import Session
from app.db.models import SensorEvent, Track
from app.services.geo import haversine_m
from app.services.threat import score_event
from app.config import settings

def fuse_event(db: Session, event: SensorEvent) -> Track:
    tracks = db.query(Track).filter(
        Track.tenant_id == event.tenant_id,
        Track.object_type == event.object_type,
        Track.is_active == True
    ).all()

    best = None
    best_distance = None

    for t in tracks:
        d = haversine_m(event.lat, event.lon, t.lat, t.lon)
        if d <= settings.fusion_distance_meters and (best_distance is None or d < best_distance):
            best = t
            best_distance = d

    source = f"{event.source}:{event.sensor_type}"
    if best:
        sources = list(set(json.loads(best.sources or "[]") + [source]))
        best.lat = (best.lat + event.lat) / 2
        best.lon = (best.lon + event.lon) / 2
        best.altitude_m = event.altitude_m or best.altitude_m
        best.speed_mps = event.speed_mps or best.speed_mps
        best.heading_deg = event.heading_deg or best.heading_deg
        best.confidence = min(1.0, max(best.confidence, event.confidence) + 0.05 * len(sources))
        best.sources = json.dumps(sources)
        score, level, explanation = score_event(event, sources)
        best.threat_score = max(best.threat_score, score)
        best.threat_level = level if score >= best.threat_score else best.threat_level
        best.explanation = explanation
        db.add(best)
        db.commit()
        db.refresh(best)
        return best

    sources = [source]
    score, level, explanation = score_event(event, sources)
    track = Track(
        tenant_id=event.tenant_id,
        label=event.object_id or f"{event.object_type.upper()}-TRACK",
        object_type=event.object_type,
        lat=event.lat,
        lon=event.lon,
        altitude_m=event.altitude_m,
        speed_mps=event.speed_mps,
        heading_deg=event.heading_deg,
        confidence=event.confidence,
        threat_score=score,
        threat_level=level,
        sources=json.dumps(sources),
        explanation=explanation,
    )
    db.add(track)
    db.commit()
    db.refresh(track)
    return track
