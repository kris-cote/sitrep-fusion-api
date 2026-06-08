import sys, time, random, requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
API_KEY = "change-me"

def post(payload):
    headers = {}
    if API_KEY != "change-me":
        headers["x-api-key"] = API_KEY
    r = requests.post(f"{BASE}/api/v1/events/ingest", json=payload, headers=headers, timeout=10)
    print(r.status_code, r.text[:180])

lat, lon = 49.030, -123.820
for i in range(45):
    lat += 0.001
    lon -= 0.001
    post({
        "source":"adsb-sim",
        "sensor_type":"adsb",
        "object_type":"aircraft",
        "object_id":"CIV-AIR-422",
        "lat":lat,
        "lon":lon,
        "altitude_m":random.randint(800,1800),
        "speed_mps":random.randint(80,140),
        "heading_deg":285,
        "confidence":0.92,
        "raw_payload":{"callsign":"CIV422"}
    })
    time.sleep(3)
