import sys, time, random, requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
API_KEY = "change-me"

def post(payload):
    headers = {}
    if API_KEY != "change-me":
        headers["x-api-key"] = API_KEY
    r = requests.post(f"{BASE}/api/v1/events/ingest", json=payload, headers=headers, timeout=10)
    print(r.status_code, r.text[:180])

for i in range(35):
    post({
        "source":"eo-camera-03",
        "sensor_type":"camera",
        "object_type":"drone",
        "object_id":"DRONE-17",
        "lat":49.066 + random.uniform(-0.003,0.003),
        "lon":-123.883 + random.uniform(-0.003,0.003),
        "altitude_m":random.randint(70,150),
        "speed_mps":random.randint(10,25),
        "heading_deg":random.randint(20,80),
        "confidence":0.58,
        "raw_payload":{"model":"yolo-demo","class":"small_uas"}
    })
    time.sleep(4)
