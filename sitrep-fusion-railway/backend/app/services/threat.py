RESTRICTED_ZONES = [
    {"name": "Airport Restricted Zone", "lat": 49.05497, "lon": -123.86986, "radius_m": 1800},
    {"name": "Power Facility", "lat": 49.07500, "lon": -123.89000, "radius_m": 1200},
]

from app.services.geo import haversine_m

def score_event(event, sources: list[str]) -> tuple[int, str, str]:
    score = 0
    reasons = []

    if event.object_type.lower() in ["drone", "uas", "unknown_uas"]:
        score += 25
        reasons.append("non-cooperative drone/UAS object")

    if event.sensor_type.lower() in ["rf", "passive_rf"]:
        score += 15
        reasons.append("RF anomaly correlated with track")

    if event.sensor_type.lower() in ["camera", "eo", "infrared"]:
        score += 10
        reasons.append("visual/EO confirmation available")

    if len(set(sources)) >= 2:
        score += 20
        reasons.append("multiple independent sensor sources")

    for zone in RESTRICTED_ZONES:
        d = haversine_m(event.lat, event.lon, zone["lat"], zone["lon"])
        if d <= zone["radius_m"]:
            score += 35
            reasons.append(f"entered {zone['name']}")

    if event.speed_mps and event.speed_mps > 25 and event.object_type.lower() in ["drone", "uas", "unknown_uas"]:
        score += 10
        reasons.append("high speed for local drone activity")

    score = min(score, 100)
    if score >= 75:
        level = "urgent"
    elif score >= 50:
        level = "high-risk"
    elif score >= 25:
        level = "suspicious"
    else:
        level = "normal"

    explanation = " ; ".join(reasons) if reasons else "No significant risk indicators."
    return score, level, explanation
