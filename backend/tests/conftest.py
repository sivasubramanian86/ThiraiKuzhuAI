"""Pytest configuration and shared fixtures for Thirai Kuzhu AI tests.

Follows PEP 257 Google-style docstrings and strict typing.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.models.department import CinemaGenreTrack, DepartmentEnum, StudioCulture
from src.models.incident import (
    SeverityLevel,
    StudioIncident,
    TechnicalTelemetry,
)


@pytest.fixture
def sample_incident() -> StudioIncident:
    """Fixture providing a mock high-severity OTT playback incident.

    Returns:
        StudioIncident: Pre-configured test incident.
    """
    return StudioIncident(
        id="INC-TEST-001",
        project_title="KGF: Chapter III",
        sequence_affected="Seq 08 - Mine Ambush",
        culture=StudioCulture.HOLLYWOOD_TENTPOLE,
        genre_track=CinemaGenreTrack.ACTION_STUNTS,
        severity=SeverityLevel.CRITICAL,
        departments_impacted=[DepartmentEnum.DIRECTING, DepartmentEnum.VFX],
        telemetry=TechnicalTelemetry(
            grafana_alert_uid="Alert-VFX-CUDA-OOM",
            promql_metric="vfx_gpu_memory_used_bytes > 98%",
            loki_log_pattern="CUDA out of memory allocating 16GB texture buffer",
            tempo_trace_id="a1b2c3d4e5f67890",
            raw_telemetry_payload={"gpu_temp_c": 84, "dropped_frames": 142},
        ),
        cinematic_narrative="GPU cluster runout of memory during mine ambush explosion sequence.",
        box_office_at_risk_usd=15000.00,
        director_directive="Downscale texture mipmaps and re-render frame buffer.",
    )


@pytest.fixture
async def async_client() -> AsyncClient:
    """Fixture providing an async HTTP client for FastAPI integration tests.

    Yields:
        AsyncClient: Test client bound to the FastAPI application.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
