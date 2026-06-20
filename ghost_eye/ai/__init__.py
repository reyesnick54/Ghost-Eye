"""Optional AI integrations for Ghost-Eye telemetry analysis."""

from .s3m_bridge import S3MBridge, telemetry_prompt_builder

__all__ = ["S3MBridge", "telemetry_prompt_builder"]
