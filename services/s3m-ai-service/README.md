# S3M AI Service

Hosted analysis-only AI service for GhostEye v0.4.

The service exposes a stable HTTP contract for GhostEye Cloud API. It optionally
loads S3M-Core when available through `S3M_CORE_PATH` or importable Python
modules. If S3M-Core is unavailable, deterministic fallback analysis remains
fully functional.

## Run locally

```bash
cd services/s3m-ai-service
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8100
```

## Run with Docker

```bash
cd services/s3m-ai-service
docker build -t s3m-ai-service .
docker run --rm -p 8100:8100 \
  -e GHOSTEYE_ENV=development \
  -e CORS_ALLOWED_ORIGINS='*' \
  s3m-ai-service
```

To enable an external S3M-Core checkout inside the container, mount it and set:

```bash
-v /path/to/s3m-core:/opt/s3m-core -e S3M_CORE_PATH=/opt/s3m-core
```

## Endpoints

- `GET /health`
- `GET /ai/status`
- `POST /ai/analyze-scan`
- `POST /ai/analyze-session`
- `POST /ai/recommend-calibration`

Responses always use `mode: analysis_only_no_autonomy` and include summary,
confidence explanation, false-positive risks, calibration recommendations,
operator notes, recommended next action, and provider.
