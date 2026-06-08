import sys, time, random, requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
API_KEY = "change-me"

def post(payload):
    headers = {}
    if API_KEY != "change-me":
        headers["x-api-key"] = API_KEY
    r = requests.post(f"{BASE}/api/v1/events/ingest", json=payload, headers=headers, timeout=10)
    print(r.status_code, r.text[:180])

for i in range(40):
    post({
        "source":"rf-node-alpha",
        "sensor_type":"rf",
        "object_type":"drone",
        "object_id":"DRONE-17",
        "lat":49.063 + random.uniform(-0.004,0.004),
        "lon":-123.887 + random.uniform(-0.004,0.004),
        "altitude_m":None,
        "speed_mps":None,
        "heading_deg":None,
        "confidence":0.66,
        "raw_payload":{"band":"2.4GHz","anomaly":"unregistered_control_link"}
    })
    time.sleep(3)
