# Railway Deployment Notes

## Recommended service split

For the DIANA TRL 4 demo, deploy one Railway service:

- `sitrep-fusion-api`

Add:

- Railway PostgreSQL

Later split:

- `sitrep-core-api`
- `sitrep-fusion-api`
- `sitrep-edge-sync`
- `sitrep-dashboard`

## Environment variables

```text
DATABASE_URL=${{Postgres.DATABASE_URL}}
SITREP_API_KEY=<long random value>
OPENAI_API_KEY=<optional>
FUSION_DISTANCE_METERS=650
FUSION_TIME_WINDOW_SECONDS=90
```

## Railway start command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Health check

```text
/health
```

## Public demo URLs

```text
/
 /dashboard
 /docs
 /api/v1/cop/tracks
```
