"""Grafana Cloud MCP Client for Thirai Kuzhu AI.

Connects to hosted Grafana Cloud MCP Server (https://mcp.grafana.com/mcp)
via Streamable HTTP with X-Grafana-URL routing and service account authentication.
Includes resilient fallback to synthetic telemetry for offline studio development.
Follows PEP 257 Google-style docstrings and strict typing.
"""

import asyncio
import logging
from typing import Any

import httpx
from pydantic import BaseModel, Field

from src.config.settings import get_settings

logger = logging.getLogger("thiraikuzhu.mcp")


class MetricsResult(BaseModel):
    """Normalized metrics result from Grafana Mimir/Prometheus."""

    query: str
    status: str = "success"
    result_type: str = "vector"
    series: list[dict[str, Any]] = Field(default_factory=list)
    summary: str = ""


class LogsResult(BaseModel):
    """Normalized logs result from Grafana Loki."""

    logql: str
    total_lines: int = 0
    entries: list[dict[str, Any]] = Field(default_factory=list)
    error_patterns_detected: list[str] = Field(default_factory=list)


class TracesResult(BaseModel):
    """Normalized trace result from Grafana Tempo."""

    service_name: str
    trace_id: str
    duration_ms: float = 0.0
    spans: list[dict[str, Any]] = Field(default_factory=list)
    bottlenecks: list[str] = Field(default_factory=list)


class IncidentDetail(BaseModel):
    """Grafana IRM Incident representation."""

    id: str
    title: str
    status: str
    severity: str
    created_at: str
    labels: dict[str, str] = Field(default_factory=dict)


class GrafanaMcpClient:
    """Async client interfacing with the Grafana Cloud MCP Server."""

    def __init__(
        self,
        mcp_endpoint: str | None = None,
        grafana_url: str | None = None,
        token: str | None = None,
    ) -> None:
        """Initializes client with Grafana stack URL and credentials."""
        settings = get_settings()
        self.mcp_endpoint = mcp_endpoint or settings.GRAFANA_MCP_ENDPOINT
        self.grafana_url = grafana_url or settings.GRAFANA_URL
        self.token = token or settings.GRAFANA_TOKEN
        self.headers = {
            "Content-Type": "application/json",
            "X-Grafana-URL": self.grafana_url,
            "User-Agent": "ThiraiKuzhuAI-ADK/1.0",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    async def _post_mcp(
        self, method: str, params: dict[str, Any], retries: int = 3
    ) -> dict[str, Any]:
        """Executes JSON-RPC call to Grafana MCP with exponential backoff."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        # If running in offline test mode (no token or default URL), return mock
        if not self.token or "thiraikuzhu.grafana.net" in self.grafana_url:
            return self._mock_mcp_response(method, params)

        delay = 0.5
        async with httpx.AsyncClient(timeout=10.0) as client:
            for attempt in range(retries):
                try:
                    response = await client.post(
                        self.mcp_endpoint,
                        headers=self.headers,
                        json=payload,
                    )
                    if response.status_code == 200:
                        return response.json()
                    if response.status_code in (429, 502, 503):
                        await asyncio.sleep(delay)
                        delay *= 2
                        continue
                    response.raise_for_status()
                except httpx.HTTPError as exc:
                    logger.warning("Grafana MCP attempt %d failed: %s", attempt + 1, exc)
                    if attempt == retries - 1:
                        logger.error("MCP call exhausted retries; falling back to synthetic data.")
                        return self._mock_mcp_response(method, params)
                    await asyncio.sleep(delay)
                    delay *= 2

        return self._mock_mcp_response(method, params)

    def _mock_mcp_response(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        """Provides high-fidelity synthetic fallback responses for studio testing."""
        tool_name = str(params.get("name", "")).lower()
        method_lower = method.lower()

        if "prometheus" in tool_name or "metric" in tool_name or "metric" in method_lower:
            return {
                "result": {
                    "status": "success",
                    "data": {
                        "resultType": "vector",
                        "result": [
                            {
                                "metric": {"region": "ap-south-1", "service": "cdn-edge"},
                                "value": [1725667200, "0.084"],
                            },
                            {
                                "metric": {"region": "ap-south-1", "service": "vfx-render-pool"},
                                "value": [1725667200, "0.982"],
                            },
                        ],
                    },
                }
            }
        if "loki" in tool_name or "log" in tool_name or "log" in method_lower:
            return {
                "result": {
                    "lines": [
                        "[vfx-node-14] CUDA OOM: failed allocating 16384MB texture in frame 1420",
                        "[origin-transcoder] 504 Gateway Timeout fetching master stream 4K-AV1",
                        "[audio-muxer-02] Atmos stem 7.1.4 phase offset exceeds 12ms threshold",
                    ]
                }
            }
        if "trace" in tool_name or "tempo" in tool_name or "trace" in method_lower:
            args = params.get("arguments", {})
            trace_id = args.get("trace_id", params.get("trace_id", "7b8f9e1204cba31d"))
            return {
                "result": {
                    "traceID": trace_id,
                    "durationMs": 2450.5,
                    "spans": [
                        {"name": "cdn_edge_fetch", "duration_ms": 12.4},
                        {"name": "drm_license_validator", "duration_ms": 2380.0},
                        {"name": "storage_chunk_read", "duration_ms": 58.1},
                    ],
                }
            }
        return {"result": {"status": "ok", "message": "Synthetic MCP action executed"}}

    async def query_prometheus(self, query: str) -> MetricsResult:
        """Queries Prometheus/Mimir through Grafana MCP."""
        res = await self._post_mcp(
            "tools/call",
            {"name": "query_prometheus", "arguments": {"query": query}},
        )
        data = res.get("result", {}).get("data", {})
        series = data.get("result", [])
        summary = f"Evaluated PromQL '{query}': Returned {len(series)} time series."
        return MetricsResult(
            query=query,
            status=data.get("status", "success"),
            result_type=data.get("resultType", "vector"),
            series=series,
            summary=summary,
        )

    async def query_loki(self, logql: str, limit: int = 50) -> LogsResult:
        """Queries Loki logs through Grafana MCP."""
        res = await self._post_mcp(
            "tools/call",
            {"name": "query_loki", "arguments": {"query": logql, "limit": limit}},
        )
        lines = res.get("result", {}).get("lines", [])
        detected_patterns = []
        for line in lines:
            line_str = str(line).lower()
            if "oom" in line_str or "memory" in line_str:
                detected_patterns.append("GPU_OUT_OF_MEMORY")
            elif "504" in line_str or "timeout" in line_str:
                detected_patterns.append("GATEWAY_TIMEOUT")
            elif "desync" in line_str or "phase" in line_str:
                detected_patterns.append("AUDIO_PHASE_DESYNC")

        return LogsResult(
            logql=logql,
            total_lines=len(lines),
            entries=[{"raw": line} for line in lines],
            error_patterns_detected=list(set(detected_patterns)),
        )

    async def query_tempo(self, trace_id: str) -> TracesResult:
        """Queries Tempo distributed traces through Grafana MCP."""
        res = await self._post_mcp(
            "tools/call",
            {"name": "get_trace", "arguments": {"trace_id": trace_id}},
        )
        data = res.get("result", {})
        spans = data.get("spans", [])
        duration_ms = float(data.get("durationMs", 0.0))
        bottlenecks = [
            f"Span '{s.get('name')}' consumed {s.get('duration_ms')}ms"
            for s in spans
            if float(s.get("duration_ms", 0)) > 500.0
        ]
        return TracesResult(
            service_name="cinema-pipeline",
            trace_id=trace_id,
            duration_ms=duration_ms,
            spans=spans,
            bottlenecks=bottlenecks,
        )

    async def create_annotation(
        self,
        time_ms: int,
        director_note: str,
        tags: list[str],
        dashboard_uid: str = "cinema-ops-main",
    ) -> bool:
        """Annotates a Grafana dashboard panel with director operations mitigation note."""
        params = {
            "name": "create_annotation",
            "arguments": {
                "dashboardUID": dashboard_uid,
                "time": time_ms,
                "text": f"[Director's Cut] {director_note}",
                "tags": ["thirai-kuzhu", *tags],
            },
        }
        res = await self._post_mcp("tools/call", params)
        return res.get("result", {}).get("status") == "ok"
