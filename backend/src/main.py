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

from src.agents.antagonists import AntagonistEngine
from src.agents.factory import AgentFactory
from src.agents.orchestrator import OrchestratorAgent
from src.agents.persona_registry import get_all_personas, get_personas_by_culture
from src.agents.sme_spawner import DynamicSMESpawner
from src.agents.topologies import OrchestrationTopologies
from src.config.settings import get_settings
from src.governance.cyber_governance import CyberGovernanceService
from src.models.department import CinemaGenreTrack, DepartmentEnum, DepartmentPersona, StudioCulture
from src.models.evaluation import (
    CinematicIndices,
    DirectorsPostMortem,
    LLMJudgeScore,
    SceneCriticalReport,
    UniverseBulletin,
)
from src.models.governance import (
    ContentProtectionRequest,
    ContentProtectionResult,
    CyberThreatAuditRequest,
    CyberThreatAuditResult,
    ScreenplaySceneRequest,
    ScreenplaySceneResult,
    ScriptPlagiarismCheckRequest,
    ScriptPlagiarismCheckResult,
    StoryPremiseRequest,
    StoryPremiseResult,
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
from src.personas.loader import load_registry
from src.services.multimodal_cinema_service import (
    CinematicReelAssembly,
    LyriaScoreGenerationRequest,
    LyriaScoreGenerationResult,
    MultimodalCinemaService,
    MultimodalSceneAsset,
    VeoVideoGenerationRequest,
    VeoVideoGenerationResult,
)
from src.services.screenplay_service import ScreenplayService
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

# Singleton Orchestrator, Translation, Voice, Cinema, Cyber & Screenplay Instances
orchestrator = OrchestratorAgent()
translation_service = CinemaTranslationService()
voice_service = CinemaVoiceService()
cinema_service = MultimodalCinemaService()
cyber_service = CyberGovernanceService()
screenplay_service = ScreenplayService()

# Persona Registry & Topology Engine Instances (Phase 5)
persona_registry = load_registry()
agent_factory = AgentFactory(persona_registry)
topologies = OrchestrationTopologies(agent_factory)
sme_spawner = DynamicSMESpawner(persona_registry)
antagonist_engine = AntagonistEngine()

# In-Memory Sample Incident Store (Replaced by Firestore/BigQuery in Production)
MOCK_INCIDENTS: dict[str, StudioIncident] = {
    "INC-2026-OTT-504": StudioIncident(
        id="INC-2026-OTT-504",
        project_title="Chronicles of Surya: The Solar Gate",
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
            promql_metric="sum(rate(cdn_504_errors_total[1m])) > 0.08",
            tempo_trace_id="tempo-trace-b8a91c7",
            severity="CRITICAL",
        ),
        cinematic_narrative=(
            "OTT regional origin transcoding buffer saturated. 40,000 live streaming "
            "subscribers experiencing sequence stalling on mobile client edge nodes."
        ),
        box_office_at_risk_usd=45000.0,
        director_directive=(
            "Switch transcoder origin to secondary cluster and invalidate edge cache."
        ),
    )
}

# In-Memory Film Projects Catalog
MOCK_PROJECTS: dict[str, StudioProject] = {
    "surya-chronicles": StudioProject(
        id="surya-chronicles",
        title="Chronicles of Surya: The Solar Gate",
        culture=StudioCulture.MYTHIC_EPIC,
        genre_track=CinemaGenreTrack.EPIC_HISTORICAL,
        release_date="2026-10-24",
        status="post_production",
        cri_score=94.5,
    ),
    "abyssal-frontier": StudioProject(
        id="abyssal-frontier",
        title="Abyssal Frontier: Deep Recon",
        culture=StudioCulture.HOLLYWOOD_TENTPOLE,
        genre_track=CinemaGenreTrack.ACTION_STUNTS,
        release_date="2026-12-18",
        status="vfx_rendering",
        cri_score=91.0,
    ),
    "whisper-crane": StudioProject(
        id="whisper-crane",
        title="Whisper of the Crane: Wuxia Chronicles",
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


@app.post("/api/cinema/multimodal/analyze")
def analyze_multimodal_scene(asset: MultimodalSceneAsset) -> dict[str, Any]:
    """Analyzes screenplay, video frames, and audio stems for cinematic continuity."""
    return cinema_service.analyze_multimodal_assets(asset)


@app.post("/api/cinema/veo/generate-scene")
def generate_veo_scene(request: VeoVideoGenerationRequest) -> VeoVideoGenerationResult:
    """Synthesizes high-fidelity cinematic video sequence via Google DeepMind Veo 2."""
    return cinema_service.generate_veo_video_scene(request)


@app.post("/api/cinema/lyria/generate-score")
def generate_lyria_music_score(
    request: LyriaScoreGenerationRequest,
) -> LyriaScoreGenerationResult:
    """Synthesizes original cinematic orchestral score and Dolby Atmos foley via Lyria."""
    return cinema_service.generate_lyria_score(request)


@app.post("/api/cinema/assemble-reel")
def assemble_cinema_reel(payload: dict[str, Any]) -> CinematicReelAssembly:
    """Assembles generated Veo shots and Lyria audio into a unified cinematic film master."""
    title = payload.get("movie_title", "Untitled Cinema Master")
    raw_shots = payload.get("veo_shots", [])
    shots = [VeoVideoGenerationResult(**s) if isinstance(s, dict) else s for s in raw_shots]
    raw_score = payload.get("lyria_score")
    score = LyriaScoreGenerationResult(**raw_score) if isinstance(raw_score, dict) else None
    return cinema_service.assemble_movie_reel(title, shots, score)


@app.post("/api/governance/cyber/audit")
def audit_cyber_security(request: CyberThreatAuditRequest) -> CyberThreatAuditResult:
    """Audits telemetry payload, command, or prompt via Gemini 3.8 Flash Cyber."""
    return cyber_service.audit_cyber_threat(request)


@app.post("/api/governance/content/protect")
def protect_media_content(request: ContentProtectionRequest) -> ContentProtectionResult:
    """Audits media assets for AI provenance, SynthID watermarking, piracy, and illicit content."""
    return cyber_service.protect_content(request)


@app.post("/api/governance/copyright/plagiarism-check")
def check_copyright_plagiarism(
    request: ScriptPlagiarismCheckRequest,
) -> ScriptPlagiarismCheckResult:
    """Audits screenplay text for copyright similarity, prior art, and patent infringement."""
    return cyber_service.check_script_plagiarism(request)


@app.post("/api/cinema/story/generate-premise")
def generate_cinematic_story_premise(request: StoryPremiseRequest) -> StoryPremiseResult:
    """Generates three-act story premise and character archetypes via StoryWriterOps."""
    return screenplay_service.generate_story_premise(request)


@app.post("/api/cinema/screenplay/format-scene")
def format_cinematic_scene(request: ScreenplaySceneRequest) -> ScreenplaySceneResult:
    """Formats industry-standard screenplay scene with localized dialogue via ScreenplayOps."""
    return screenplay_service.format_screenplay_scene(request)


@app.get("/api/cinema/screenplay/shot-list/{scene_id}")
def get_scene_shot_list(scene_id: str) -> list[dict[str, Any]]:
    """Generates director's cut shot list with camera moves and focal lengths."""
    return screenplay_service.generate_shot_list(scene_id)


# =========================================================================
# Phase 5: Complete Persona Registry, SME Spawner & Antagonist Endpoints
# =========================================================================


@app.get("/api/v1/personas")
def list_registry_personas(
    band: str | None = None,
    model_tier: str | None = None,
    budget_line: str | None = None,
    search: str | None = None,
) -> dict[str, Any]:
    """Lists and filters personas across 17 bands conforming to Phase 5B catalog."""
    if search:
        results = persona_registry.search(search)
    elif band:
        results = persona_registry.list_by_band(band.upper())
    else:
        results = persona_registry.all_personas()

    if model_tier:
        results = [p for p in results if p.model_tier == model_tier.lower()]
    if budget_line:
        results = [p for p in results if p.budget_line == budget_line.upper()]

    return {
        "total": len(results),
        "personas": [p.model_dump() for p in results],
    }


@app.get("/api/v1/personas/{persona_id}")
def get_persona_detail(persona_id: str) -> dict[str, Any]:
    """Retrieves full specification of a single cinematic persona."""
    persona = persona_registry.get(persona_id.upper())
    if not persona:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Persona '{persona_id}' not found in registry.",
        )
    return persona.model_dump()


@app.post("/api/v1/personas/sme/spawn")
def spawn_dynamic_sme(payload: dict[str, str]) -> dict[str, Any]:
    """Extracts domain entities from screenplay text and spawns custom SME advisors dynamically."""
    screenplay_text = payload.get("screenplay_text", "")
    if not screenplay_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'screenplay_text' cannot be empty.",
        )
    return sme_spawner.analyze_script_and_spawn(screenplay_text)


@app.post("/api/v1/personas/debate")
def run_persona_debate(payload: dict[str, Any]) -> dict[str, Any]:
    """Executes arbitration loop between opposing crew personas with defined tie-breaker rules."""
    p_a = payload.get("persona_a_id", "B01")
    p_b = payload.get("persona_b_id", "C04")
    topic = payload.get("topic", "Production set piece budget overrun vs artistic vision")
    version = payload.get("script_version", "1.0")

    try:
        return topologies.run_debate(p_a, p_b, topic, script_version=version)
    except KeyError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err


@app.post("/api/v1/personas/antagonist/simulate")
def simulate_antagonist_attack(payload: dict[str, Any]) -> dict[str, Any]:
    """Runs adversarial red-team stress test against production plans."""
    antag_id = payload.get("antagonist_id", "ANTG01")
    proj = payload.get("project_title", "Chronicles of Surya: The Solar Gate")
    scene = payload.get("scene_description", "Seq 14 - Waterfall Royal Gate Climax")
    loc = payload.get("shoot_location", "Outdoor Jungle Canyon Set")

    return antagonist_engine.simulate_attack(
        antagonist_id=antag_id,
        project_title=proj,
        scene_description=scene,
        shoot_location=loc,
    )


@app.post("/api/v1/multimodal/analyze")
def analyze_multimodal_sample(payload: dict[str, Any]) -> dict[str, Any]:
    """Analyzes image scans, audio WAVs, or video clips with simulated Gemini multimodal."""
    sample_id = payload.get("sample_id", "sample_01")
    media_type = payload.get("media_type", "image")
    title = payload.get("title", "Cinematic Scene Asset")

    # Generate rich multimodal telemetry and director assessment
    analysis = {
        "sample_id": sample_id,
        "media_type": media_type,
        "title": title,
        "model_used": "gemini-2.5-flash-vision",
        "multimodal_confidence": 0.965,
        "scene_beats_detected": [
            {
                "beat_index": 1,
                "description": "High tension framing with low-key shadow contrast",
                "timecode": "00:00:12",
            },
            {
                "beat_index": 2,
                "description": "Character arrival with spatial audio pan",
                "timecode": "00:00:45",
            },
        ],
        "audio_foley_telemetry": {
            "peak_dbr": -1.2,
            "snr_db": 28.4,
            "speech_clarity_score": 98.2,
            "transcription": "Director calling: Silence on set! Roll camera, speed, action!",
        }
        if media_type == "audio"
        else None,
        "visual_continuity_flags": [
            "Costume grime level consistent with Sequence 12 continuity bible.",
            "Lighting color temperature verified at 3200K tungsten profile.",
        ],
        "director_verdict": "Asset approved for master timeline conform. Zero artifacts detected.",
        "grafana_annotation_id": f"ANN-MM-{sample_id[-6:]}",
    }
    return analysis


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
