"""Unit tests for film-domain ADK telemetry tools.

Follows PEP 257 Google-style docstrings and rigorous assertions.
"""

import pytest

from src.tools.telemetry_tools import (
    annotate_studio_dashboard,
    query_cinema_logs,
    query_cinema_metrics,
    query_cinema_traces,
    query_cinematic_graph,
)


@pytest.mark.asyncio
async def test_tool_query_cinema_metrics() -> None:
    """Tests Prometheus query wrapper across film metric types."""
    res = await query_cinema_metrics(query_type="cdn_throughput", project_id="baahubali-3")
    assert res["status"] == "success"
    assert "series" in res
    assert len(res["series"]) >= 1


@pytest.mark.asyncio
async def test_tool_query_cinema_logs() -> None:
    """Tests Loki logs query wrapper for film department filters."""
    res = await query_cinema_logs(department="vfx", error_pattern="CUDA", limit=5)
    assert res["logql"] == "{department='vfx'} |= 'CUDA'"
    assert res["total_lines"] >= 1


@pytest.mark.asyncio
async def test_tool_query_cinema_traces() -> None:
    """Tests Tempo trace wrapper with bottleneck detection."""
    res = await query_cinema_traces(service_name="drm-validator")
    assert res["trace_id"] == "7b8f9e1204cba31d"
    assert len(res["spans"]) >= 1


@pytest.mark.asyncio
async def test_tool_query_cinematic_graph() -> None:
    """Tests Graph RAG tool wrapper for blast radius lookup."""
    res = await query_cinematic_graph(fault_node_id="vfx-node-14")
    assert res["origin_node_id"] == "vfx-node-14"
    assert res["box_office_at_risk_usd"] == 15000.00


@pytest.mark.asyncio
async def test_tool_annotate_studio_dashboard() -> None:
    """Tests Grafana dashboard annotation tool wrapper."""
    success = await annotate_studio_dashboard(
        director_note="Re-routed CDN edge to prevent buffer stalls.",
        tags=["action", "ott"],
    )
    assert success is True
