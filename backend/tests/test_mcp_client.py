"""Unit tests for Grafana Cloud MCP Client in Thirai Kuzhu AI.

Follows PEP 257 Google-style docstrings and rigorous assertions.
"""

from typing import Any

import pytest

from src.tools.grafana_mcp_client import (
    GrafanaMcpClient,
    LogsResult,
    MetricsResult,
    TracesResult,
)


@pytest.mark.asyncio
async def test_mcp_query_prometheus_synthetic() -> None:
    """Tests Prometheus query execution and fallback model parsing."""
    client = GrafanaMcpClient()
    result: MetricsResult = await client.query_prometheus("sum(rate(cdn_requests_total[2m]))")

    assert result.status == "success"
    assert result.result_type == "vector"
    assert len(result.series) >= 1
    assert "Evaluated PromQL" in result.summary


@pytest.mark.asyncio
async def test_mcp_query_loki_pattern_detection() -> None:
    """Tests Loki logs query and automated error taxonomy tagging."""
    client = GrafanaMcpClient()
    result: LogsResult = await client.query_loki(logql="{app='vfx'} |= 'oom'", limit=10)

    assert result.total_lines >= 1
    assert len(result.entries) >= 1
    assert any(
        p in result.error_patterns_detected
        for p in ["GPU_OUT_OF_MEMORY", "GATEWAY_TIMEOUT", "AUDIO_PHASE_DESYNC"]
    )


@pytest.mark.asyncio
async def test_mcp_query_tempo_spans() -> None:
    """Tests Tempo distributed trace retrieval and bottleneck isolation."""
    client = GrafanaMcpClient()
    result: TracesResult = await client.query_tempo(trace_id="7b8f9e1204cba31d")

    assert result.trace_id == "7b8f9e1204cba31d"
    assert result.duration_ms > 0
    assert len(result.spans) >= 2
    assert len(result.bottlenecks) >= 1


@pytest.mark.asyncio
async def test_mcp_create_annotation() -> None:
    """Tests publishing a Director's Cut operational note to Grafana dashboard."""
    client = GrafanaMcpClient()
    success = await client.create_annotation(
        time_ms=1725667200000,
        director_note="Re-routed Chennai CDN origin to Mumbai cluster.",
        tags=["hotfix", "ott"],
    )
    assert success is True


@pytest.mark.asyncio
async def test_mcp_client_auth_header() -> None:
    """Tests GrafanaMcpClient correctly formats Bearer token in headers."""
    client = GrafanaMcpClient(token="glsa_secret_token_123")
    assert client.headers["Authorization"] == "Bearer glsa_secret_token_123"


@pytest.mark.asyncio
async def test_mcp_incident_detail_model() -> None:
    """Tests IncidentDetail schema serialization."""
    from src.tools.grafana_mcp_client import IncidentDetail

    detail = IncidentDetail(
        id="INC-100",
        title="CDN Outage",
        status="firing",
        severity="critical",
        created_at="2026-09-06T12:00:00Z",
        labels={"region": "ap-south-1"},
    )
    assert detail.id == "INC-100"
    assert detail.labels["region"] == "ap-south-1"


@pytest.mark.asyncio
async def test_mcp_client_live_http_200(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests live HTTP execution path returning 200 JSON-RPC response."""
    import httpx

    class MockResponse:
        status_code = 200

        def json(self) -> dict[str, Any]:
            return {
                "result": {
                    "data": {
                        "resultType": "vector",
                        "result": [{"metric": {"job": "live-stream"}, "value": [123, "0.45"]}],
                    }
                }
            }

    async def mock_post(self: Any, *args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    client = GrafanaMcpClient(
        grafana_url="https://live-cinema.grafana.net",
        token="glsa_live_token",
    )
    res = await client.query_prometheus("up{job='live-stream'}")
    assert len(res.series) == 1
    assert res.series[0]["metric"]["job"] == "live-stream"


@pytest.mark.asyncio
async def test_mcp_client_live_http_429_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests live HTTP retry loop upon encountering 429 Too Many Requests."""
    import httpx

    call_count = 0

    class MockResponse:
        def __init__(self, code: int) -> None:
            self.status_code = code

        def json(self) -> dict[str, Any]:
            return {"result": {"data": {"result": []}}}

    async def mock_post_retry(self: Any, *args: Any, **kwargs: Any) -> MockResponse:
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            return MockResponse(429)
        return MockResponse(200)

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post_retry)

    client = GrafanaMcpClient(
        grafana_url="https://live-cinema.grafana.net",
        token="glsa_live_token",
    )
    res = await client.query_prometheus("up")
    assert call_count >= 2
    assert res.status == "success"


@pytest.mark.asyncio
async def test_mcp_client_live_http_error_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests live HTTP failure falls back gracefully to synthetic mock data."""
    import httpx

    async def mock_post_fail(self: Any, *args: Any, **kwargs: Any) -> None:
        raise httpx.ConnectError("Connection refused to hosted endpoint")

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post_fail)

    client = GrafanaMcpClient(
        grafana_url="https://live-cinema.grafana.net",
        token="glsa_live_token",
    )
    # Falls back to synthetic response on error
    res = await client.query_prometheus("up")
    assert res.status == "success"
    assert len(res.series) >= 1


@pytest.mark.asyncio
async def test_mcp_client_live_http_raise_for_status(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests live HTTP 400 client error raises and triggers fallback."""
    import httpx

    class MockErrorResponse:
        status_code = 400

        def raise_for_status(self) -> None:
            raise httpx.HTTPStatusError("Bad request", request=None, response=None)  # type: ignore[arg-type]

    async def mock_post_bad(self: Any, *args: Any, **kwargs: Any) -> MockErrorResponse:
        return MockErrorResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post_bad)

    client = GrafanaMcpClient(
        grafana_url="https://live-cinema.grafana.net",
        token="glsa_live_token",
    )
    res = await client.query_prometheus("invalid_syntax")
    assert res.status == "success"


@pytest.mark.asyncio
async def test_mcp_client_retries_zero() -> None:
    """Tests client handles zero retries by returning fallback directly."""
    client = GrafanaMcpClient(
        grafana_url="https://live-cinema.grafana.net",
        token="glsa_live_token",
    )
    res = await client._post_mcp("tools/call", {"name": "query_prometheus"}, retries=0)
    assert res["result"]["status"] == "success"


@pytest.mark.asyncio
async def test_mcp_client_offline_mode() -> None:
    """Tests client in explicit offline mode returns mock response directly."""
    client = GrafanaMcpClient(
        token="",
        grafana_url="https://thiraikuzhu.grafana.net",
    )
    res = await client._post_mcp("tools/call", {"name": "query_prometheus"})
    assert res["result"]["status"] == "success"

