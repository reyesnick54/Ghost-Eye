# Hosted S3M AI Service Contract v0.4

Base URL: value of `S3M_AI_SERVICE_URL` in GhostEye Cloud API.

The S3M AI Service is an internal hosted HTTP service. It accepts GhostEye
telemetry from the Cloud API and returns advisory analysis only.

## Health

`GET /health`

```json
{
  "status": "ok",
  "service": "s3m-ai-service",
  "timestamp": "2026-06-22T16:18:00Z",
  "mode": "analysis_only_no_autonomy"
}
```

## Status

`GET /ai/status`

```json
{
  "provider": "fallback",
  "s3m_core_available": false,
  "mode": "analysis_only_no_autonomy"
}
```

## Analyze scan

`POST /ai/analyze-scan`

Request:

```json
{
  "scan": { "...": "TelemetryScan" },
  "metadata": {}
}
```

Response:

```json
{
  "summary": "Telemetry reports possible motion with motion score 0.42 in coarse zone zone_a.",
  "confidence_explanation": "Analysis uses GhostEye scan confidence 0.45 and does not raise confidence.",
  "false_positive_risks": ["missing_zone_fingerprints"],
  "calibration_recommendations": ["Run zone calibration for coarse room zones."],
  "operator_notes": [
    "Analysis is advisory and bounded to mobile-submitted network observations."
  ],
  "recommended_next_action": "Run zone calibration for coarse room zones.",
  "provider": "s3m_service_fallback",
  "mode": "analysis_only_no_autonomy",
  "confidence": 0.45,
  "created_at": "2026-06-22T16:18:00Z",
  "metadata": {}
}
```

## Analyze session

`POST /ai/analyze-session`

Request:

```json
{
  "session": { "...": "SessionSummary" },
  "metadata": {}
}
```

Response: `AIAnalysis`.

## Recommend calibration

`POST /ai/recommend-calibration`

Request:

```json
{
  "team_id": "team_demo",
  "room_id": "living_room",
  "latest_scan": { "...": "TelemetryScan" },
  "existing_baseline": null,
  "zone_fingerprints": [],
  "metadata": {}
}
```

Response: `AIAnalysis`.

## Runtime behavior

- If S3M-Core is importable, the adapter attempts a compatible analysis method.
- If S3M-Core is unavailable or errors, deterministic fallback analysis works.
- Output confidence must not exceed GhostEye telemetry confidence.
- Responses must use `mode: analysis_only_no_autonomy`.
- The service must not claim exact object/person localization.
