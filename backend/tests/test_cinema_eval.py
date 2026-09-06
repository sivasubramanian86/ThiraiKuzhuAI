"""Unit and integration tests for Phase 6 Narrative Framing and Cinematic Evaluation.

Tests mathematical indices (CRI, AER, UCS, CWV), narrative report generation,
LLM-as-a-judge rubric evaluation, and all related FastAPI endpoints.
Enforces 100% statement coverage without cheat annotations.
"""

import pytest
from httpx import AsyncClient

from src.models.incident import AgentThoughtStep, InvestigationResponse, StudioIncident
from src.tools.cinema_eval_tools import (
    calculate_aer,
    calculate_cri,
    calculate_cwv,
    calculate_ucs,
    compute_all_cinematic_indices,
    evaluate_agent_response_rubric,
    generate_directors_post_mortem,
    generate_scene_critical_report,
    generate_universe_bulletin,
)


def test_calculate_cri_math() -> None:
    """Tests CRI formula calculations, custom weights, and clamping."""
    # 1. Normal calculation
    score = calculate_cri(vqr=0.95, asr=0.98, chr_val=0.90, eer=0.02)
    assert 90.0 <= score <= 100.0

    # 2. Clamping high
    score_high = calculate_cri(vqr=1.5, asr=1.5, chr_val=1.5, eer=0.0)
    assert score_high == 100.0

    # 3. Clamping low
    score_low = calculate_cri(vqr=0.0, asr=0.0, chr_val=0.0, eer=2.0)
    assert score_low == 0.0


def test_calculate_aer_math() -> None:
    """Tests AER formula calculations and release block thresholds."""
    # 1. Minimal risk
    aer_clean = calculate_aer(stall_rate=0.0005, drm_latency_ms=100.0, sub_sync_error_ms=5.0)
    assert aer_clean < 0.2

    # 2. High risk above 0.7 release block threshold
    aer_critical = calculate_aer(stall_rate=0.008, drm_latency_ms=2500.0, sub_sync_error_ms=400.0)
    assert aer_critical >= 0.7
    assert aer_critical <= 1.0

    # 3. Zero inputs
    assert calculate_aer(0.0, 0.0, 0.0) == 0.0


def test_calculate_ucs_and_cwv_math() -> None:
    """Tests UCS franchise continuity and CWV crew workload volatility formulas."""
    # 1. UCS tests
    ucs = calculate_ucs(asset_drift_rate=0.01, vfx_mismatch_rate=0.01, timeline_sync_drift=0.01)
    assert ucs > 95.0

    ucs_zero = calculate_ucs(asset_drift_rate=2.0, vfx_mismatch_rate=2.0, timeline_sync_drift=2.0)
    assert ucs_zero == 0.0

    # 2. CWV tests
    cwv = calculate_cwv(gpu_saturation_pct=75.0, transcode_backlog_min=5.0, pending_approvals=3)
    assert 0.0 <= cwv <= 100.0

    cwv_high = calculate_cwv(
        gpu_saturation_pct=100.0, transcode_backlog_min=200.0, pending_approvals=50
    )
    assert cwv_high == 100.0


def test_compute_all_cinematic_indices() -> None:
    """Tests consolidated cinematic indices generation and release block flag."""
    # Clean scenario: not blocked
    indices_ok = compute_all_cinematic_indices(stall_rate=0.001)
    assert indices_ok.release_blocked is False
    assert indices_ok.cri_score > 90.0

    # Severe scenario: blocked
    indices_blocked = compute_all_cinematic_indices(stall_rate=0.015, drm_latency_ms=3000.0)
    assert indices_blocked.release_blocked is True
    assert indices_blocked.aer_score >= 0.7


def test_narrative_report_generators(sample_incident: StudioIncident) -> None:
    """Tests SceneCriticalReport, UniverseBulletin, and DirectorsPostMortem generators.

    Args:
        sample_incident: Fixture incident.
    """
    # 1. SceneCriticalReport with fallback narrative
    sample_incident.cinematic_narrative = ""
    sample_incident.director_directive = ""
    report = generate_scene_critical_report(sample_incident)
    assert report.incident_id == sample_incident.id
    assert "Disruption affecting" in report.cinematic_narrative
    assert "Execute automated transcode" in report.director_mitigation_directive

    # 2. UniverseBulletin with drift detected and without drift
    bulletin_drift = generate_universe_bulletin(
        franchise_name="Baahubali",
        active_productions=["Baahubali III"],
        vfx_version_drift_detected=True,
    )
    assert bulletin_drift.vfx_version_drift_detected is True
    assert "USD schema" in bulletin_drift.recommended_action

    bulletin_clean = generate_universe_bulletin(
        franchise_name="Avatar",
        active_productions=["Avatar 3"],
        vfx_version_drift_detected=False,
    )
    assert bulletin_clean.vfx_version_drift_detected is False
    assert "verified" in bulletin_clean.recommended_action

    # 3. DirectorsPostMortem with custom timeline
    post_mortem = generate_directors_post_mortem(
        incident=sample_incident,
        incident_timeline=[{"timestamp": "T+00:01", "event": "Alert fired"}],
        permanent_mitigations=["Permanent autoscaling rule applied."],
    )
    assert len(post_mortem.incident_timeline) == 1
    assert len(post_mortem.permanent_mitigations) == 1


def test_llm_judge_rubric_evaluation() -> None:
    """Tests LLM-as-a-Judge grading rubric against passing and low-score responses."""
    # 1. High scoring response meeting benchmark >= 4.5
    high_resp = InvestigationResponse(
        incident_id="INC-2026-TEST",
        project_title="Test Movie",
        root_cause_summary="Telemetry: promql cdn_5xx_rate > 8% alert confirmed origin deadlock.",
        cinematic_impact=(
            "Audience in Chennai experienced 42s of buffering during royal coronation reveal."
        ),
        box_office_at_risk_usd=25000.0,
        mitigation_plan=["Failover to Mumbai", "Re-route edge CDN", "Scale standby worker pool"],
        agent_timeline=[
            AgentThoughtStep(
                agent_name="DirectorOps",
                department="directing",
                thought="Triaged blast radius",
                mcp_tool_invoked="query_cinematic_graph",
                tool_output_summary="Scene 14 affected",
            )
        ],
        cri_score_after_mitigation=95.0,
        grafana_annotation_status="Annotated on Grafana Dashboard successfully.",
    )
    judge_high = evaluate_agent_response_rubric(high_resp)
    assert judge_high.passed_benchmark is True
    assert judge_high.overall_grade >= 4.5
    assert "PASSED" in judge_high.feedback

    # 2. Low scoring response
    low_resp = InvestigationResponse(
        incident_id="INC-2026-LOW",
        project_title="Low Movie",
        root_cause_summary="Unknown glitch",
        cinematic_impact="Short",
        box_office_at_risk_usd=0.0,
        mitigation_plan=["Wait"],
        agent_timeline=[],
        cri_score_after_mitigation=50.0,
        grafana_annotation_status="Not posted",
    )
    judge_low = evaluate_agent_response_rubric(low_resp)
    assert judge_low.passed_benchmark is False
    assert "FAILED" in judge_low.feedback


@pytest.mark.asyncio
async def test_evaluation_endpoints(async_client: AsyncClient) -> None:
    """Tests all Phase 6 evaluation endpoints on FastAPI.

    Args:
        async_client: Async HTTP client fixture.
    """
    # 1. GET /api/evaluation/indices
    idx_resp = await async_client.get("/api/evaluation/indices")
    assert idx_resp.status_code == 200
    indices_data = idx_resp.json()
    assert "cri_score" in indices_data
    assert "aer_score" in indices_data
    assert "ucs_score" in indices_data
    assert "cwv_score" in indices_data

    # 2. GET /api/evaluation/reports/scene-critical/{incident_id}
    sc_resp = await async_client.get("/api/evaluation/reports/scene-critical/INC-2026-OTT-504")
    assert sc_resp.status_code == 200
    sc_data = sc_resp.json()
    assert sc_data["incident_id"] == "INC-2026-OTT-504"
    assert "Royal Coronation" in sc_data["sequence_affected"]

    # 404 for unknown scene report
    sc_404 = await async_client.get("/api/evaluation/reports/scene-critical/UNKNOWN-999")
    assert sc_404.status_code == 404

    # 3. GET /api/evaluation/bulletin/{franchise}
    bul_resp = await async_client.get("/api/evaluation/bulletin/baahubali")
    assert bul_resp.status_code == 200
    bul_data = bul_resp.json()
    assert bul_data["franchise_name"] == "baahubali"
    assert len(bul_data["active_productions"]) >= 1

    # 4. GET /api/evaluation/retrospective/{incident_id}
    ret_resp = await async_client.get("/api/evaluation/retrospective/INC-2026-OTT-504")
    assert ret_resp.status_code == 200
    ret_data = ret_resp.json()
    assert ret_data["incident_id"] == "INC-2026-OTT-504"
    assert len(ret_data["incident_timeline"]) >= 3
    assert len(ret_data["permanent_mitigations"]) >= 2

    # 404 for unknown retrospective
    ret_404 = await async_client.get("/api/evaluation/retrospective/UNKNOWN-999")
    assert ret_404.status_code == 404

    # 5. POST /api/evaluation/judge
    sample_resp_payload = {
        "incident_id": "INC-2026-OTT-504",
        "project_title": "Baahubali III",
        "root_cause_summary": "Telemetry: promql alert cdn_5xx_rate > 8%",
        "cinematic_impact": "Emotional climax interrupted for 42,000 viewers across Tamil Nadu.",
        "box_office_at_risk_usd": 38500.0,
        "mitigation_plan": [
            "Re-route Chennai POP to Mumbai",
            "Fallback to H.264",
            "Restart AV1 master",
        ],
        "agent_timeline": [
            {
                "agent_name": "DirectorOps",
                "department": "directing",
                "thought": "Checking scene blast radius",
                "mcp_tool_invoked": "query_cinematic_graph",
                "tool_output_summary": "Scene 14 impact",
            }
        ],
        "cri_score_after_mitigation": 94.5,
        "grafana_annotation_status": "Annotated on Grafana Dashboard successfully.",
    }
    judge_api = await async_client.post("/api/evaluation/judge", json=sample_resp_payload)
    assert judge_api.status_code == 200
    judge_data = judge_api.json()
    assert judge_data["passed_benchmark"] is True
    assert judge_data["overall_grade"] >= 4.5
