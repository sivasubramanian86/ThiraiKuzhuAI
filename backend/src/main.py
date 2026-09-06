"""FastAPI entrypoint for Thirai Kuzhu AI.

Follows APAC 2026 strict layer separation: Endpoints validate input and delegate
directly to the OrchestratorAgent. Zero business calculations inside routes.
Follows PEP 257 Google-style docstrings.
"""

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from src.agents.orchestrator import OrchestratorAgent
from src.agents.persona_registry import get_all_personas, get_personas_by_culture
from src.config.settings import get_settings
from src.models.department import CinemaGenreTrack, DepartmentEnum, DepartmentPersona, StudioCulture
from src.models.evaluation import (
    CinematicIndices,
    DirectorsPostMortem,
    LLMJudgeScore,
    SceneCriticalReport,
    UniverseBulletin,
)
from src.models.incident import (
    CRIEvaluationReport,
    InvestigationRequest,
    InvestigationResponse,
    MitigationApplyRequest,
    MitigationApplyResponse,
    SeverityLevel,
    StudioIncident,
    StudioProject,
    TechnicalTelemetry,
)
from src.tools.cinema_eval_tools import (
    compute_all_cinematic_indices,
    evaluate_agent_response_rubric,
    generate_directors_post_mortem,
    generate_scene_critical_report,
    generate_universe_bulletin,
)
from src.tools.translation_service import CinemaTranslationService
from src.tools.voice_service import CinemaVoiceService

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description=(
        "Autonomous Screen Crew AI for Cinematic Observability (Grafana Labs Hackathon Track)"
    ),
)

# CORS Configuration for local Next.js frontend and Cloud Run
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Singleton Orchestrator, Translation, and Voice Instances
orchestrator = OrchestratorAgent()
translation_service = CinemaTranslationService()
voice_service = CinemaVoiceService()

# In-Memory Sample Incident Store (Replaced by Firestore/BigQuery in Production)
MOCK_INCIDENTS: dict[str, StudioIncident] = {
    "INC-2026-OTT-504": StudioIncident(
        id="INC-2026-OTT-504",
        project_title="Baahubali III: The Eternal Realm",
        sequence_affected="Seq 14 - Royal Coronation Climax",
        culture=StudioCulture.MYTHIC_EPIC,
        genre_track=CinemaGenreTrack.EPIC_HISTORICAL,
        severity=SeverityLevel.CRITICAL,
        departments_impacted=[
            DepartmentEnum.DIRECTING,
            DepartmentEnum.OTT_DISTRIBUTION,
            DepartmentEnum.PRODUCING,
        ],
        telemetry=TechnicalTelemetry(
            grafana_alert_uid="Alert-OTT-504-AsiaSouth",
            promql_metric="sum(rate(cdn_requests_total{status=~'5..'}[2m])) by (region) > 8.4%",
            loki_log_pattern="{app='origin-transcoder'} |= 'deadlock on AV1 4K master'",
            tempo_trace_id="7b8f9e1204cba31d",
            raw_telemetry_payload={"cache_hit_ratio": 0.32, "stall_rate": 0.042},
        ),
        cinematic_narrative=(
            "At minute 142 of the royal coronation sequence, video playback stalled "
            "for 42,000 viewers across South Asia. Emotional climax interrupted."
        ),
        box_office_at_risk_usd=38500.00,
        director_directive=(
            "Re-route Chennai POP to Mumbai fallback. Transcode master fallback "
            "to H.264 high-tier while origin pool restarts."
        ),
    )
}

# In-Memory Film Projects Catalog
MOCK_PROJECTS: dict[str, StudioProject] = {
    "baahubali-3": StudioProject(
        id="baahubali-3",
        title="Baahubali III: The Eternal Realm",
        culture=StudioCulture.MYTHIC_EPIC,
        genre_track=CinemaGenreTrack.EPIC_HISTORICAL,
        release_date="2026-10-24",
        status="post_production",
        cri_score=94.5,
    ),
    "avatar-trench": StudioProject(
        id="avatar-trench",
        title="Avatar: The Deep Trenches",
        culture=StudioCulture.HOLLYWOOD_TENTPOLE,
        genre_track=CinemaGenreTrack.ACTION_STUNTS,
        release_date="2026-12-18",
        status="vfx_rendering",
        cri_score=91.0,
    ),
    "crane-shadow": StudioProject(
        id="crane-shadow",
        title="Shadow of the Crane",
        culture=StudioCulture.EAST_ASIAN_ANIME,
        genre_track=CinemaGenreTrack.MARTIAL_ARTS_WUXIA,
        release_date="2026-11-05",
        status="sound_conforming",
        cri_score=95.2,
    ),
}


@app.get("/api/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, Any]:
    """Liveness probe for Cloud Run and automated health monitoring.

    Returns:
        dict: Health and runtime status.
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENV,
        "primary_model": settings.PRIMARY_MODEL,
        "grafana_mcp_endpoint": settings.GRAFANA_MCP_ENDPOINT,
    }


@app.get("/api/incidents", response_model=list[StudioIncident])
async def list_incidents() -> list[StudioIncident]:
    """Lists all active and monitored film production incidents.

    Returns:
        list[StudioIncident]: Collection of current incidents.
    """
    return list(MOCK_INCIDENTS.values())


@app.get("/api/incidents/{incident_id}", response_model=StudioIncident)
async def get_incident(incident_id: str) -> StudioIncident:
    """Retrieves detailed technical and cinematic incident record.

    Args:
        incident_id: Target incident identifier.

    Returns:
        StudioIncident: Incident details.

    Raises:
        HTTPException: If incident ID is not found.
    """
    incident = MOCK_INCIDENTS.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return incident


@app.post("/api/missions/investigate", response_model=InvestigationResponse)
async def investigate_incident(request: InvestigationRequest) -> InvestigationResponse:
    """Dispatches Thirai Kuzhu multi-agent mesh to investigate an incident.

    Strict layer separation: Delegates reasoning to OrchestratorAgent.route().

    Args:
        request: Validated investigation request payload.

    Returns:
        InvestigationResponse: Complete synthesized investigation findings.

    Raises:
        HTTPException: If target incident is not found.
    """
    incident = MOCK_INCIDENTS.get(request.incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{request.incident_id}' not found.")
    return await orchestrator.route(request, incident)


@app.get("/api/missions/{incident_id}/stream")
async def stream_mission(incident_id: str) -> EventSourceResponse:
    """Streams live multi-agent Walkie-Talkie thought steps as Server-Sent Events (SSE).

    Args:
        incident_id: Target incident identifier.

    Returns:
        EventSourceResponse: SSE stream of agent thought steps.

    Raises:
        HTTPException: If target incident is not found.
    """
    incident = MOCK_INCIDENTS.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    req = InvestigationRequest(incident_id=incident_id)
    return EventSourceResponse(orchestrator.stream_investigation(req, incident))


@app.get("/api/projects", response_model=list[StudioProject])
async def list_projects() -> list[StudioProject]:
    """Lists all active film productions tracked by Thirai Kuzhu AI.

    Returns:
        list[StudioProject]: List of studio productions.
    """
    return list(MOCK_PROJECTS.values())


@app.get("/api/evaluation/cri/{project_id}", response_model=CRIEvaluationReport)
async def get_project_cri(project_id: str) -> CRIEvaluationReport:
    """Returns Cinematic Readiness Index (CRI) and radar metrics for a production.

    Strict layer separation: Delegates calculation to OrchestratorAgent.

    Args:
        project_id: Target film project identifier.

    Returns:
        CRIEvaluationReport: CRI scores across technical and narrative dimensions.

    Raises:
        HTTPException: If project is not found.
    """
    project = MOCK_PROJECTS.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found.")
    return await orchestrator.get_cri_evaluation(project_id)


@app.post("/api/mitigations/apply", response_model=MitigationApplyResponse)
async def apply_mitigation(request: MitigationApplyRequest) -> MitigationApplyResponse:
    """Executes automated director mitigation and annotates Grafana dashboard.

    Strict layer separation: Delegates action to OrchestratorAgent.

    Args:
        request: Mitigation action and annotation details.

    Returns:
        MitigationApplyResponse: Result of applied mitigation.

    Raises:
        HTTPException: If target incident is not found.
    """
    incident = MOCK_INCIDENTS.get(request.incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{request.incident_id}' not found.")
    return await orchestrator.apply_mitigation(request)


@app.get("/api/personas", response_model=list[DepartmentPersona])
async def list_personas() -> list[DepartmentPersona]:
    """Lists all registered international cinema department personas.

    Returns:
        list[DepartmentPersona]: Collection of all available personas.
    """
    return get_all_personas()


@app.get("/api/personas/{culture}", response_model=list[DepartmentPersona])
async def list_personas_for_culture(culture: StudioCulture) -> list[DepartmentPersona]:
    """Filters cinema department personas by cultural archetype.

    Args:
        culture: Studio culture identifier.

    Returns:
        list[DepartmentPersona]: Filtered list of matching personas.
    """
    return get_personas_by_culture(culture)


@app.get("/api/evaluation/indices", response_model=CinematicIndices)
async def get_cinematic_indices() -> CinematicIndices:
    """Returns the four core quantitative cinematic indices for studio operations.

    Calculates CRI, AER, UCS, and CWV based on current studio telemetry.

    Returns:
        CinematicIndices: Consolidated cinematic indices with release readiness.
    """
    return compute_all_cinematic_indices()


@app.get(
    "/api/evaluation/reports/scene-critical/{incident_id}",
    response_model=SceneCriticalReport,
)
async def get_scene_critical_report(incident_id: str) -> SceneCriticalReport:
    """Generates an executive scene-critical incident report for studio leadership.

    Args:
        incident_id: Target incident identifier.

    Returns:
        SceneCriticalReport: Formatted narrative scene impact report.

    Raises:
        HTTPException: If target incident is not found.
    """
    incident = MOCK_INCIDENTS.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return generate_scene_critical_report(incident)


@app.get("/api/evaluation/bulletin/{franchise}", response_model=UniverseBulletin)
async def get_universe_bulletin(franchise: str) -> UniverseBulletin:
    """Generates a franchise-level universe continuity and asset drift bulletin.

    Args:
        franchise: Target franchise name.

    Returns:
        UniverseBulletin: Franchise continuity status and recommendations.
    """
    active_films = [
        p.title
        for p in MOCK_PROJECTS.values()
        if franchise.lower() in p.title.lower() or franchise.lower() in p.culture.value
    ] or [f"{franchise.capitalize()} Universe Master"]
    return generate_universe_bulletin(franchise_name=franchise, active_productions=active_films)


@app.get(
    "/api/evaluation/retrospective/{incident_id}",
    response_model=DirectorsPostMortem,
)
async def get_directors_retrospective(incident_id: str) -> DirectorsPostMortem:
    """Generates a comprehensive post-incident retrospective for producers and SREs.

    Args:
        incident_id: Target incident identifier.

    Returns:
        DirectorsPostMortem: Chronological timeline and permanent mitigations.

    Raises:
        HTTPException: If target incident is not found.
    """
    incident = MOCK_INCIDENTS.get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident '{incident_id}' not found.")
    return generate_directors_post_mortem(incident)


@app.post("/api/evaluation/judge", response_model=LLMJudgeScore)
async def evaluate_agent_mission(response: InvestigationResponse) -> LLMJudgeScore:
    """Automated LLM-as-a-Judge grading harness evaluating agent mission reports.

    Grades on a 1.0-5.0 rubric across Technical Accuracy, Cinematic Relevance,
    and Actionability, verifying the >= 4.5/5.0 benchmark.

    Args:
        response: InvestigationResponse payload to grade.

    Returns:
        LLMJudgeScore: Multi-dimensional score and pass/fail benchmark result.
    """
    return evaluate_agent_response_rubric(response)


@app.post("/api/translation/translate")
async def translate_text(payload: dict[str, Any]) -> dict[str, Any]:
    """Translates narrative text to target cinema language.

    Args:
        payload: Dict containing 'text' and 'target_language'.

    Returns:
        dict[str, Any]: Translation result with preserved invariant tokens.
    """
    text = payload.get("text", "")
    target = payload.get("target_language", "en")
    return await translation_service.translate_narrative(text, target)


@app.post("/api/voice/synthesize")
async def synthesize_speech(payload: dict[str, Any]) -> dict[str, Any]:
    """Synthesizes on-set walkie-talkie radio audio for agent bulletins.

    Args:
        payload: Dict with 'script_text', 'language_code', and 'speaker_name'.

    Returns:
        dict[str, Any]: Audio metadata and base64 audio payload.
    """
    script = payload.get("script_text", "")
    lang = payload.get("language_code", "en")
    speaker = payload.get("speaker_name", "DirectorOps")
    return await voice_service.synthesize_walkie_talkie_alert(script, lang, speaker)


# Mount static frontend assets for web browser visualization and judge evaluation

_FRONTEND_CANDIDATES = [
    Path(__file__).resolve().parent.parent.parent / "frontend" / "dist",
    Path(__file__).resolve().parent.parent.parent / "frontend",
    Path(__file__).resolve().parent.parent / "frontend" / "dist",
    Path(__file__).resolve().parent.parent / "frontend",
    Path("/app/frontend/dist"),
    Path("/app/frontend"),
]
for _candidate in _FRONTEND_CANDIDATES:
    if _candidate.exists() and (_candidate / "index.html").exists():
        app.mount("/", StaticFiles(directory=str(_candidate), html=True), name="static_frontend")
        break
