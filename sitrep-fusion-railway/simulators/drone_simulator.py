import sys, time, random, requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
API_KEY = "change-me"

def post(payload):
    headers = {}
    if API_KEY != "change-me":
        headers["x-api-key"] = API_KEY
    r = requests.post(f"{BASE}/api/v1/events/ingest", json=payload, headers=headers, timeout=10)
    print(r.status_code, r.text[:180])

lat, lon = 49.060, -123.900
for i in range(60):
    lat += random.uniform(-0.0006, 0.0009)
    lon += random.uniform(0.0002, 0.0010)
    post({
        "source":"drone-sim-01",
        "sensor_type":"track_sim",
        "object_type":"drone",
        "object_id":"DRONE-17",
        "lat":lat,
        "lon":lon,
        "altitude_m":random.randint(60,140),
        "speed_mps":random.randint(12,32),
        "heading_deg":random.randint(20,80),
        "confidence":0.72,
        "raw_payload":{"scenario":"airport_power_facility"}
    })
    time.sleep(2)
