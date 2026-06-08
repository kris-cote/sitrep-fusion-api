# SitRep Fusion — Railway-ready TRL 4 Prototype

SitRep Fusion is a separate API service that can run independently on Railway, while still acting as a module/capability pack for the larger SitRep platform.

## What it does

- Ingests multi-domain sensor events
- Normalizes events into a common data model
- Fuses related detections into tracks
- Scores risk/threat level
- Exposes a Common Operational Picture API
- Serves a lightweight live dashboard
- Includes simulators for drone, aircraft, RF, camera, and cyber events

## Architecture

SitRep Core
  -> Auth / users / tenants / subscriptions / main product shell

SitRep Fusion API
  -> Sensor ingestion / fusion / threat scoring / COP / AI analyst

For Railway, deploy this as its own service first. Later, connect it to SitRep Core using API keys or JWT.

## Local quick start

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000
http://localhost:8000/dashboard
http://localhost:8000/docs
```

Start simulated events in another terminal:

```bash
cd simulators
python run_all.py http://localhost:8000
```

## Railway deployment

1. Create a new Railway project.
2. Add a PostgreSQL database.
3. Add a new service from this repo.
4. Set the service root directory to `backend`.
5. Add environment variables:
   - `DATABASE_URL` from Railway Postgres
   - `SITREP_API_KEY` any long random string
   - `OPENAI_API_KEY` optional for AI analyst
6. Deploy.

Railway will use `backend/Procfile`.

## Demo scenario

The simulators create an airport + power facility scenario with aircraft, drone tracks, RF anomalies, EO/camera detections, and cyber alerts. The API correlates events and exposes a COP feed.
