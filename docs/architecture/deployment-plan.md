# GhostEye Cloud Deployment Plan v0.4

## Deployable units

1. `services/ghosteye-cloud-api`
2. `services/s3m-ai-service`

Each service has its own `requirements.txt`, `Dockerfile`, FastAPI app, health
endpoint, and README.

## Required hosted capabilities

- HTTPS for REST APIs.
- WSS support for `/ws/session/{session_id}`.
- Environment variable management.
- Structured logs.
- Health checks.
- Mobile-friendly CORS with explicit allowed origins.
- Horizontal scaling compatibility once storage moves from JSON files to a
  managed database/object store.

## Environment variables

Cloud API:

- `GHOSTEYE_ENV`
- `GHOSTEYE_API_SECRET`
- `SUPABASE_URL`
- `SUPABASE_JWT_SECRET`
- `S3M_AI_SERVICE_URL`
- `CORS_ALLOWED_ORIGINS`
- `GHOSTEYE_STORAGE_DIR`

S3M AI Service:

- `GHOSTEYE_ENV`
- `CORS_ALLOWED_ORIGINS`
- `S3M_CORE_PATH` optional

## Render

- Create two Web Services from Dockerfiles.
- Set health checks:
  - Cloud API: `/health`
  - S3M AI Service: `/health`
- Configure `S3M_AI_SERVICE_URL` in Cloud API to the private/internal S3M URL if
  available, otherwise the HTTPS service URL.
- Set explicit `CORS_ALLOWED_ORIGINS` for Expo/mobile web callback origins.
- Enable log drains if production observability is required.

## Fly.io

- Create two Fly apps.
- Deploy each service using its Dockerfile.
- Use Fly secrets for all environment variables.
- Enable TLS at Fly edge.
- Use private networking for Cloud API -> S3M service if both apps are in the
  same organization.
- Confirm WebSocket idle timeout behavior for mobile WSS sessions.

## Railway

- Create two services from the repository subdirectories.
- Use Dockerfile builds.
- Configure variables per service.
- Set health check paths.
- Use Railway private networking for `S3M_AI_SERVICE_URL` when available.

## AWS

Recommended baseline: ECS Fargate or App Runner for both services.

- Terminate HTTPS at ALB/App Runner.
- Configure health checks to `/health`.
- Store secrets in AWS Secrets Manager or SSM Parameter Store.
- Send logs to CloudWatch.
- Use VPC/private service discovery for Cloud API -> S3M service.
- Move storage adapters to RDS/Postgres, DynamoDB, or S3 before scaling beyond a
  single instance.

## GCP Cloud Run

- Build and deploy each Dockerfile as a separate Cloud Run service.
- Require HTTPS with Cloud Run managed TLS.
- Set `S3M_AI_SERVICE_URL` to the S3M Cloud Run service URL.
- Use Secret Manager for `GHOSTEYE_API_SECRET` and future Supabase secrets.
- Enable request logs and error reporting.
- Configure min instances if cold start latency affects mobile sessions.
- Verify WebSocket support and timeout behavior for expected session streams.

## Production hardening checklist

- Replace placeholder JWT with Supabase/OIDC verification.
- Move JSON-compatible storage to managed persistence.
- Use explicit CORS origins; avoid `*` in production.
- Add rate limits for device registration and telemetry ingestion.
- Add request IDs and structured security audit logs.
- Ensure telemetry logs do not include raw secrets or unnecessary identifiers.
- Keep AI analysis bounded to advisory `analysis_only_no_autonomy` responses.
