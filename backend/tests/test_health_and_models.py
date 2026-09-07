"""Integration and unit tests for Thirai Kuzhu AI API and models.

Follows PEP 257 Google-style docstrings and strict assertion standards.
"""

import pytest
from httpx import AsyncClient

from src.agents.orchestrator import OrchestratorAgent
from src.models.incident import InvestigationRequest, StudioIncident


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient) -> None:
    """Tests the /api/health endpoint returns 200 and expected metadata.

    Args:
        async_client: Async HTTP client fixture.
    """
    response = await async_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Thirai Kuzhu" in data["app_name"]
    assert "gemini-3.8-flash-001" in data["primary_model"]


@pytest.mark.asyncio
async def test_list_and_get_incidents(async_client: AsyncClient) -> None:
    """Tests incident listing and retrieval by ID.

    Args:
        async_client: Async HTTP client fixture.
    """
    # 1. List incidents
    list_resp = await async_client.get("/api/incidents")
    assert list_resp.status_code == 200
    incidents = list_resp.json()
    assert len(incidents) >= 1
    target_id = incidents[0]["id"]

    # 2. Get specific incident
    get_resp = await async_client.get(f"/api/incidents/{target_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == target_id
    assert "Chronicles of Surya" in data["project_title"]

    # 3. Not found handling
    nf_resp = await async_client.get("/api/incidents/NON_EXISTENT_ID")
    assert nf_resp.status_code == 404


@pytest.mark.asyncio
async def test_investigate_incident_route(async_client: AsyncClient) -> None:
    """Tests the /api/missions/investigate endpoint delegates to the Orchestrator.

    Args:
        async_client: Async HTTP client fixture.
    """
    payload = {
        "incident_id": "INC-2026-OTT-504",
        "target_language": "en",
        "include_graph_rag": True,
    }
    resp = await async_client.post("/api/missions/investigate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["incident_id"] == "INC-2026-OTT-504"
    assert len(data["agent_timeline"]) >= 3
    assert len(data["mitigation_plan"]) >= 2
    assert data["cri_score_after_mitigation"] > 90.0


@pytest.mark.asyncio
async def test_orchestrator_agent_direct(sample_incident: StudioIncident) -> None:
    """Tests OrchestratorAgent.route() directly for isolation and typing.

    Args:
        sample_incident: Pre-configured sample incident fixture.
    """
    orchestrator = OrchestratorAgent()
    req = InvestigationRequest(incident_id=sample_incident.id, target_language="ta")
    result = await orchestrator.route(req, sample_incident)
    assert result.incident_id == sample_incident.id
    assert result.box_office_at_risk_usd == 15000.00
    assert any(step.agent_name == "DirectorOps" for step in result.agent_timeline)


@pytest.mark.asyncio
async def test_orchestrator_wuxia_and_sakuga_routes(sample_incident: StudioIncident) -> None:
    """Tests Wuxia and Anime Sakuga genre routing branches.

    Args:
        sample_incident: Pre-configured sample incident fixture.
    """
    from src.models.department import CinemaGenreTrack

    orchestrator = OrchestratorAgent()

    # 1. Test Wuxia genre branch
    sample_incident.genre_track = CinemaGenreTrack.MARTIAL_ARTS_WUXIA
    req = InvestigationRequest(incident_id=sample_incident.id, target_language="zh")
    res_wuxia = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "MartialArtsOps" for step in res_wuxia.agent_timeline)

    # 2. Test Anime Sakuga genre branch
    sample_incident.genre_track = CinemaGenreTrack.ANIMATION
    req_ja = InvestigationRequest(incident_id=sample_incident.id, target_language="ja")
    res_sakuga = await orchestrator.route(req_ja, sample_incident)
    assert any(step.agent_name == "AnimationSakugaOps" for step in res_sakuga.agent_timeline)


@pytest.mark.asyncio
async def test_orchestrator_stream_investigation(sample_incident: StudioIncident) -> None:
    """Tests SSE stream generator emitting thought steps and complete event.

    Args:
        sample_incident: Pre-configured sample incident fixture.
    """
    orchestrator = OrchestratorAgent()
    req = InvestigationRequest(incident_id=sample_incident.id, target_language="en")

    events = []
    async for event_chunk in orchestrator.stream_investigation(req, sample_incident):
        events.append(event_chunk)

    assert len(events) >= 4
    assert any("event: complete" in chunk for chunk in events)


@pytest.mark.asyncio
async def test_api_stream_endpoint(async_client: AsyncClient) -> None:
    """Tests the /api/missions/{incident_id}/stream SSE HTTP endpoint.

    Args:
        async_client: Async HTTP client fixture.
    """
    resp = await async_client.get("/api/missions/INC-2026-OTT-504/stream")
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers.get("content-type", "")


@pytest.mark.asyncio
async def test_api_missions_not_found(async_client: AsyncClient) -> None:
    """Tests 404 handling when investigating or streaming non-existent incidents.

    Args:
        async_client: Async HTTP client fixture.
    """
    # 1. Investigate non-existent incident
    post_resp = await async_client.post(
        "/api/missions/investigate",
        json={"incident_id": "INC-DOES-NOT-EXIST", "target_language": "en"},
    )
    assert post_resp.status_code == 404

    # 2. Stream non-existent incident
    stream_resp = await async_client.get("/api/missions/INC-DOES-NOT-EXIST/stream")
    assert stream_resp.status_code == 404


@pytest.mark.asyncio
async def test_list_projects_endpoint(async_client: AsyncClient) -> None:
    """Tests the /api/projects endpoint returns registered studio projects.

    Args:
        async_client: Async HTTP client fixture.
    """
    resp = await async_client.get("/api/projects")
    assert resp.status_code == 200
    projects = resp.json()
    assert len(projects) >= 3
    assert any(p["id"] == "surya-chronicles" for p in projects)
    assert any(p["id"] == "abyssal-frontier" for p in projects)


@pytest.mark.asyncio
async def test_cri_evaluation_endpoint(async_client: AsyncClient) -> None:
    """Tests the /api/evaluation/cri/{project_id} endpoint and 404 error handling.

    Args:
        async_client: Async HTTP client fixture.
    """
    # 1. Valid project evaluation
    resp = await async_client.get("/api/evaluation/cri/surya-chronicles")
    assert resp.status_code == 200
    report = resp.json()
    assert report["project_id"] == "surya-chronicles"
    assert report["cri_score"] >= 90.0
    assert "vfx_pipeline_stability" in report["radar_metrics"]
    assert "sound_stem_sync" in report["radar_metrics"]
    assert len(report["recommendations"]) >= 2
    assert report["verdict"] == "APPROVED_FOR_RELEASE"

    # 2. 404 for unknown project
    nf_resp = await async_client.get("/api/evaluation/cri/unknown-film-999")
    assert nf_resp.status_code == 404
    assert "not found" in nf_resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_apply_mitigation_endpoint(async_client: AsyncClient) -> None:
    """Tests the /api/mitigations/apply endpoint and 404 error handling.

    Args:
        async_client: Async HTTP client fixture.
    """
    # 1. Valid mitigation execution
    payload = {
        "incident_id": "INC-2026-OTT-504",
        "action_taken": "Re-routed origin transcoder pool to secondary node cluster",
        "annotation_text": "Thirai Kuzhu AI: Applied transcode failover",
        "dashboard_uid": "cinema-stream-master",
    }
    resp = await async_client.post("/api/mitigations/apply", json=payload)
    assert resp.status_code == 200
    res_data = resp.json()
    assert res_data["status"] == "applied"
    assert "INC-2026-OTT-504" in res_data["message"]
    assert res_data["grafana_annotation_id"].startswith("annot-")

    # 2. 404 for unknown incident
    payload["incident_id"] = "INC-NON-EXISTENT"
    nf_resp = await async_client.post("/api/mitigations/apply", json=payload)
    assert nf_resp.status_code == 404


@pytest.mark.asyncio
async def test_static_frontend_mount(async_client: AsyncClient) -> None:
    """Tests that the frontend static mount serves the index.html page.

    Args:
        async_client: Async HTTP client fixture.
    """
    resp = await async_client.get("/")
    assert resp.status_code == 200
    assert "Thirai Kuzhu AI" in resp.text


@pytest.mark.asyncio
async def test_orchestrator_cri_and_mitigation_direct() -> None:
    """Tests OrchestratorAgent get_cri_evaluation and apply_mitigation directly.

    Verifies the REQUIRES_MITIGATION branch and direct mitigation dispatch.
    """
    from src.models.incident import MitigationApplyRequest

    orchestrator = OrchestratorAgent()

    # 1. REQUIRES_MITIGATION branch
    risk_report = await orchestrator.get_cri_evaluation("unapproved-risk-project")
    assert risk_report.verdict == "REQUIRES_MITIGATION"
    assert risk_report.cri_score < 90.0

    # 2. Direct apply mitigation
    req = MitigationApplyRequest(
        incident_id="INC-2026-OTT-504",
        action_taken="Failover to H.264",
        annotation_text="Applied fallback transcode",
        dashboard_uid="cinema-test",
    )
    mit_res = await orchestrator.apply_mitigation(req)
    assert mit_res.status == "applied"
    assert mit_res.success is True


@pytest.mark.asyncio
async def test_orchestrator_vfx_and_audio_routes(sample_incident: StudioIncident) -> None:
    """Tests VFX and Audio routing branches in OrchestratorAgent.

    Args:
        sample_incident: Fixture incident.
    """
    from src.models.department import CinemaGenreTrack, DepartmentEnum

    orchestrator = OrchestratorAgent()

    # 1. VFX alert branch
    sample_incident.genre_track = CinemaGenreTrack.ACTION_STUNTS
    sample_incident.telemetry.grafana_alert_uid = "Alert-VFX-CUDA-OOM"
    req = InvestigationRequest(incident_id=sample_incident.id, target_language="en")
    res_vfx = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "VFXOps" for step in res_vfx.agent_timeline)

    # 2. Audio department branch
    sample_incident.telemetry.grafana_alert_uid = "Alert-Standard"
    sample_incident.departments_impacted = [DepartmentEnum.AUDIO]
    res_audio = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "AudioOps" for step in res_audio.agent_timeline)


@pytest.mark.asyncio
async def test_list_personas_endpoints(async_client: AsyncClient) -> None:
    """Tests /api/personas and /api/personas/{culture} endpoints.

    Args:
        async_client: Async HTTP client fixture.
    """
    # 1. List all personas
    resp = await async_client.get("/api/personas")
    assert resp.status_code == 200
    personas = resp.json()
    assert len(personas) >= 8
    assert any(p["id"] == "hollywood_director" for p in personas)
    assert any(p["id"] == "mythic_scene_keeper" for p in personas)

    # 2. Filter by culture
    resp_cult = await async_client.get("/api/personas/hollywood_tentpole")
    assert resp_cult.status_code == 200
    hollywood_personas = resp_cult.json()
    assert len(hollywood_personas) >= 2
    assert all(p["culture"] == "hollywood_tentpole" for p in hollywood_personas)


@pytest.mark.asyncio
async def test_persona_registry_direct() -> None:
    """Tests get_all_personas and get_personas_by_culture directly."""
    from src.agents.persona_registry import get_all_personas, get_personas_by_culture
    from src.models.department import StudioCulture

    all_personas = get_all_personas()
    assert len(all_personas) >= 8

    anime_personas = get_personas_by_culture(StudioCulture.EAST_ASIAN_ANIME)
    assert len(anime_personas) >= 2
    assert any(p.id == "anime_sakuga_director" for p in anime_personas)
