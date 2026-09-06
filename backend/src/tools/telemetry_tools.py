"""Cinematic Observability ADK Tools for Thirai Kuzhu AI.

Provides specialized film-domain telemetry tools wrapped around the Grafana Cloud MCP Server
and the Cinematic Knowledge Graph RAG service. Sub-agents invoke these tools during missions.
Follows PEP 257 Google-style docstrings and strict typing.
"""

from typing import Any

from src.services.graph_rag_service import BlastRadiusReport, CinematicGraphService
from src.tools.grafana_mcp_client import (
    GrafanaMcpClient,
    LogsResult,
    MetricsResult,
    TracesResult,
)

# Shared tool dependencies
_mcp_client = GrafanaMcpClient()
_graph_service = CinematicGraphService()


async def query_cinema_metrics(
    query_type: str,
    project_id: str = "default-production",
    time_window: str = "15m",
) -> dict[str, Any]:
    """Queries Prometheus/Mimir metrics via Grafana MCP translated for film production.

    Args:
        query_type: Telemetry metric category (e.g., 'cdn_throughput', 'transcode_fps',
            'render_gpu_util', 'drm_license_rate').
        project_id: Studio production identifier.
        time_window: Lookback evaluation interval.

    Returns:
        dict: Normalized metric evaluation dictionary with time series and summary.
    """
    query_map = {
        "cdn_throughput": "sum(rate(cdn_requests_total{status=~'5..'}[2m])) by (region)",
        "render_gpu_util": (
            "sum(vfx_gpu_memory_used_bytes) by (instance) / sum(vfx_gpu_memory_total_bytes)"
        ),
        "transcode_fps": "rate(video_frames_transcoded_total[1m])",
        "drm_license_rate": (
            "histogram_quantile(0.99, sum(rate(drm_latency_seconds_bucket[5m])) by (le))"
        ),
        "audio_stem_offset": "avg(audio_stem_sync_offset_ms) by (channel)",
    }
    promql = query_map.get(query_type, f"rate({query_type}_total[5m])")
    result: MetricsResult = await _mcp_client.query_prometheus(promql)
    return result.model_dump()


async def query_cinema_logs(
    department: str,
    error_pattern: str,
    limit: int = 50,
) -> dict[str, Any]:
    """Queries Loki logs via Grafana MCP for specific film department error patterns.

    Args:
        department: Studio department label ('vfx', 'audio', 'ott', 'stunts', 'sakuga').
        error_pattern: Substring or regex pattern to search for in log streams.
        limit: Maximum number of matching log records to return.

    Returns:
        dict: Parsed logs dictionary containing raw entries and detected error taxonomy.
    """
    logql = f"{{department='{department}'}} |= '{error_pattern}'"
    result: LogsResult = await _mcp_client.query_loki(logql=logql, limit=limit)
    return result.model_dump()


async def query_cinema_traces(
    service_name: str,
    trace_id: str = "7b8f9e1204cba31d",
    min_duration_ms: int = 1000,
) -> dict[str, Any]:
    """Queries Tempo distributed traces via Grafana MCP to pinpoint pipeline bottlenecks.

    Args:
        service_name: Service being traced ('dolby-muxer', 'transcoder-worker', 'drm-validator').
        trace_id: Distributed trace UUID or hex string.
        min_duration_ms: Latency threshold to flag as bottleneck.

    Returns:
        dict: Structured trace spans and flagged latency bottlenecks.
    """
    result: TracesResult = await _mcp_client.query_tempo(trace_id=trace_id)
    return result.model_dump()


async def query_cinematic_graph(
    fault_node_id: str,
) -> dict[str, Any]:
    """Traverses the Cinematic Knowledge Graph to evaluate narrative and financial blast radius.

    Args:
        fault_node_id: Failing hardware or service node (e.g., 'vfx-node-14',
            'cdn-origin-southasia').

    Returns:
        dict: Blast radius report with affected shots, scenes, narrative arc, and dollar risk.
    """
    report: BlastRadiusReport = await _graph_service.get_blast_radius(fault_node_id=fault_node_id)
    return report.model_dump()


async def annotate_studio_dashboard(
    director_note: str,
    tags: list[str],
    dashboard_uid: str = "cinema-ops-main",
    time_ms: int = 1725667200000,
) -> bool:
    """Writes a Director's Cut operational note directly to the live Grafana dashboard.

    Args:
        director_note: Human-readable creative and technical mitigation text.
        tags: Categorization labels for Grafana annotation markers.
        dashboard_uid: UID of target Grafana dashboard panel.
        time_ms: Epoch millisecond timestamp of the incident event.

    Returns:
        bool: True if Grafana MCP successfully registered the annotation.
    """
    return await _mcp_client.create_annotation(
        time_ms=time_ms,
        director_note=director_note,
        tags=tags,
        dashboard_uid=dashboard_uid,
    )
