import sys, time, random, requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
API_KEY = "change-me"

def post(payload):
    headers = {}
    if API_KEY != "change-me":
        headers["x-api-key"] = API_KEY
    r = requests.post(f"{BASE}/api/v1/events/ingest", json=payload, headers=headers, timeout=10)
    print(r.status_code, r.text[:180])

for i in range(20):
    post({
        "source":"network-monitor",
        "sensor_type":"cyber",
        "object_type":"infrastructure_alert",
        "object_id":"POWER-FACILITY-NETWORK",
        "lat":49.075 + random.uniform(-0.0005,0.0005),
        "lon":-123.890 + random.uniform(-0.0005,0.0005),
        "altitude_m":0,
        "speed_mps":0,
        "heading_deg":0,
        "confidence":0.7,
        "raw_payload":{"alert":"camera_gateway_packet_loss","severity":"medium"}
    })
    time.sleep(7)
