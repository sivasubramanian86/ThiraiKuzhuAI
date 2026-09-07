"""Tests for extended cinema universe subagents, screenplay service, and orchestrator routing.

Validates StoryWriterOps, DialogueWriterOps, ScreenplayOps, FilmEditorOps,
CinematographerLens, and CopyrightLegalOps with 100% statement coverage.
"""

import pytest
from fastapi.testclient import TestClient

from src.agents.orchestrator import OrchestratorAgent
from src.agents.persona_registry import (
    INTERNATIONAL_PERSONAS,
    get_all_personas,
    get_personas_by_culture,
)
from src.agents.subagents import (
    CinematographerLensSubAgent,
    CopyrightLegalOpsSubAgent,
    DialogueWriterOpsSubAgent,
    FilmEditorOpsSubAgent,
    ScreenplayOpsSubAgent,
    StoryWriterOpsSubAgent,
)
from src.main import app
from src.models.department import DepartmentEnum, StudioCulture
from src.models.governance import ScreenplaySceneRequest, StoryPremiseRequest
from src.models.incident import InvestigationRequest, StudioIncident
from src.services.screenplay_service import ScreenplayService

client = TestClient(app)


@pytest.mark.asyncio
async def test_story_writer_subagent(sample_incident: StudioIncident) -> None:
    """Tests StoryWriterOpsSubAgent narrative stakes audit."""
    agent = StoryWriterOpsSubAgent()
    assert agent.department == DepartmentEnum.STORY_WRITING
    step = await agent.investigate(sample_incident)
    assert step.agent_name == "StoryWriterOps"
    assert step.department == DepartmentEnum.STORY_WRITING
    assert "narrative consequences" in step.thought
    assert step.mcp_tool_invoked == "audit_narrative_continuity"


@pytest.mark.asyncio
async def test_dialogue_writer_subagent(sample_incident: StudioIncident) -> None:
    """Tests DialogueWriterOpsSubAgent punchline and sync audit."""
    agent = DialogueWriterOpsSubAgent()
    assert agent.department == DepartmentEnum.DIALOGUE_WRITING
    step = await agent.investigate(sample_incident)
    assert step.agent_name == "DialogueWriterOps"
    assert step.department == DepartmentEnum.DIALOGUE_WRITING
    assert "spoken cadence" in step.thought
    assert step.mcp_tool_invoked == "verify_dialogue_sync"


@pytest.mark.asyncio
async def test_screenplay_subagent(sample_incident: StudioIncident) -> None:
    """Tests ScreenplayOpsSubAgent sluglines and transition audit."""
    agent = ScreenplayOpsSubAgent()
    assert agent.department == DepartmentEnum.SCREENPLAY
    step = await agent.investigate(sample_incident)
    assert step.agent_name == "ScreenplayOps"
    assert step.department == DepartmentEnum.SCREENPLAY
    assert "Auditing sluglines" in step.thought
    assert step.mcp_tool_invoked == "validate_sluglines"


@pytest.mark.asyncio
async def test_film_editor_subagent(sample_incident: StudioIncident) -> None:
    """Tests FilmEditorOpsSubAgent NLE cut and timeline audit."""
    agent = FilmEditorOpsSubAgent()
    assert agent.department == DepartmentEnum.EDITING
    step = await agent.investigate(sample_incident)
    assert step.agent_name == "FilmEditorOps"
    assert step.department == DepartmentEnum.EDITING
    assert "24.000 fps lock" in step.thought
    assert step.mcp_tool_invoked == "verify_edl_timecode"


@pytest.mark.asyncio
async def test_cinematographer_subagent(sample_incident: StudioIncident) -> None:
    """Tests CinematographerLensSubAgent lens and lighting audit."""
    agent = CinematographerLensSubAgent()
    assert agent.department == DepartmentEnum.CINEMATOGRAPHY
    step = await agent.investigate(sample_incident)
    assert step.agent_name == "CinematographerLens"
    assert step.department == DepartmentEnum.CINEMATOGRAPHY
    assert "ACEScc color gamut" in step.thought
    assert step.mcp_tool_invoked == "audit_aces_gamut"


@pytest.mark.asyncio
async def test_copyright_legal_subagent(sample_incident: StudioIncident) -> None:
    """Tests CopyrightLegalOpsSubAgent powered by Gemini 3.8 Flash Cyber."""
    agent = CopyrightLegalOpsSubAgent()
    assert agent.department == DepartmentEnum.COPYRIGHT_LEGAL
    sample_incident.cinematic_narrative = (
        "Original screenplay about a deep sea expedition uncovering acoustic frequencies."
    )
    step = await agent.investigate(sample_incident)
    assert step.agent_name == "CopyrightLegalOps"
    assert step.department == DepartmentEnum.COPYRIGHT_LEGAL
    assert "Gemini 3.8 Flash Cyber" in step.thought
    assert "Originality Score" in step.thought
    assert step.mcp_tool_invoked == "verify_ip_clearance"


def test_screenplay_service_story_premise() -> None:
    """Tests story premise generation with 3-act narrative and characters."""
    service = ScreenplayService()
    req = StoryPremiseRequest(
        core_theme="Sacrifice for Knowledge",
        target_audience="Global Film Festival Audiences",
        culture="European Auteur",
        genre_track="cult_classic_neo_noir",
    )
    result = service.generate_story_premise(req)
    assert "Sacrifice" in result.title
    assert "Sacrifice for Knowledge" in result.logline
    assert "Act_1_Departure" in result.three_act_structure
    assert "Act_2_Initiation" in result.three_act_structure
    assert "Act_3_Return" in result.three_act_structure
    assert len(result.lead_characters) == 4
    assert len(result.mythic_motifs) == 4


def test_screenplay_service_format_scene_english() -> None:
    """Tests screenplay scene formatting in English with two characters."""
    service = ScreenplayService()
    req = ScreenplaySceneRequest(
        scene_heading="ext. royal mountain pass - night",
        characters_present=["Karna", "Krishna"],
        action_description="Rain lashes against the cliff face as thunder rumbles.",
        dramatic_intent="Moral dilemma at twilight",
        language="en",
    )
    result = service.format_screenplay_scene(req)
    assert result.scene_heading == "EXT. ROYAL MOUNTAIN PASS - NIGHT"
    assert "Rain lashes" in result.action_block
    assert len(result.dialogue_blocks) == 2
    assert result.dialogue_blocks[0]["character"] == "KARNA"
    assert "Throne was not won" in result.dialogue_blocks[0]["dialogue"]
    assert result.dialogue_blocks[1]["character"] == "KRISHNA"
    assert "Ancestors belong to dust" in result.dialogue_blocks[1]["dialogue"]
    assert result.scene_pacing_tempo == "ALLEGRO"


def test_screenplay_service_format_scene_tamil() -> None:
    """Tests screenplay scene formatting in Tamil with localized dialogue."""
    service = ScreenplayService()
    req = ScreenplaySceneRequest(
        scene_heading="int. thirumalai nayak palace - day",
        characters_present=["Thalaivan", "Kattappa"],
        action_description="Pillars cast long golden shadows across the courtyard.",
        dramatic_intent="Oaths of valor",
        language="ta",
    )
    result = service.format_screenplay_scene(req)
    assert len(result.dialogue_blocks) == 2
    assert "சிம்மாசனம்" in result.dialogue_blocks[0]["dialogue"]
    assert "முன்னோர்கள்" in result.dialogue_blocks[1]["dialogue"]


def test_screenplay_service_format_scene_single_character() -> None:
    """Tests screenplay scene formatting with solitary character soliloquy."""
    service = ScreenplayService()
    req = ScreenplaySceneRequest(
        scene_heading="ext. desert dunes - dawn",
        characters_present=["Lone Warrior"],
        action_description="The warrior stares at the horizon.",
        dramatic_intent="Solitude and acceptance",
        language="en",
    )
    result = service.format_screenplay_scene(req)
    assert len(result.dialogue_blocks) == 1
    assert result.dialogue_blocks[0]["character"] == "LONE WARRIOR"
    assert "Fate knocked upon the door" in result.dialogue_blocks[0]["dialogue"]


def test_screenplay_service_shot_list() -> None:
    """Tests director's cut shot list generation."""
    service = ScreenplayService()
    shots = service.generate_shot_list(scene_id="SCENE-042", shot_count=4)
    assert len(shots) == 4
    assert shots[0]["shot_id"] == "SCENE-042_S01"
    assert shots[0]["framing"] == "Extreme Wide Establishing"
    assert shots[0]["lens"] == "24mm Ultra-Wide"
    assert shots[0]["estimated_duration_seconds"] == 4.5


@pytest.mark.asyncio
async def test_orchestrator_routes_all_new_departments(sample_incident: StudioIncident) -> None:
    """Tests Orchestrator routing to every newly added cinema department."""
    orchestrator = OrchestratorAgent()
    req = InvestigationRequest(incident_id=sample_incident.id)

    # 1. Story Writing department
    sample_incident.departments_impacted = [DepartmentEnum.STORY_WRITING]
    resp1 = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "StoryWriterOps" for step in resp1.agent_timeline)

    # 2. Screenplay department
    sample_incident.departments_impacted = [DepartmentEnum.SCREENPLAY]
    resp2 = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "ScreenplayOps" for step in resp2.agent_timeline)

    # 3. Dialogue Writing department
    sample_incident.departments_impacted = [DepartmentEnum.DIALOGUE_WRITING]
    resp3 = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "DialogueWriterOps" for step in resp3.agent_timeline)

    # 4. Film Editing department
    sample_incident.departments_impacted = [DepartmentEnum.EDITING]
    resp4 = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "FilmEditorOps" for step in resp4.agent_timeline)

    # 5. Cinematography department
    sample_incident.departments_impacted = [DepartmentEnum.CINEMATOGRAPHY]
    resp5 = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "CinematographerLens" for step in resp5.agent_timeline)

    # 6. Copyright Legal department
    sample_incident.departments_impacted = [DepartmentEnum.COPYRIGHT_LEGAL]
    resp6 = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "CopyrightLegalOps" for step in resp6.agent_timeline)

    # 7. Generic Legal department mapping to CopyrightLegalOps
    sample_incident.departments_impacted = [DepartmentEnum.LEGAL]
    resp7 = await orchestrator.route(req, sample_incident)
    assert any(step.agent_name == "CopyrightLegalOps" for step in resp7.agent_timeline)


def test_new_personas_registered() -> None:
    """Verifies that all 6 new cinema personas are registered and retrievable."""
    all_personas = get_all_personas()
    persona_ids = {p.id for p in all_personas}

    expected_ids = {
        "mythic_story_writer",
        "pan_indian_dialogue_writer",
        "hollywood_screenplay_architect",
        "auteur_cinematographer",
        "feature_film_editor",
        "cyber_copyright_counsel",
    }
    for pid in expected_ids:
        assert pid in persona_ids
        p = INTERNATIONAL_PERSONAS[pid]
        assert len(p.name_en) > 0
        assert len(p.name_ta) > 0
        assert len(p.name_fr) > 0
        assert len(p.compliance_standards) >= 2

    # Verify filtering by culture
    mythic_personas = get_personas_by_culture(StudioCulture.MYTHIC_EPIC)
    assert any(p.id == "mythic_story_writer" for p in mythic_personas)
    assert any(p.id == "pan_indian_dialogue_writer" for p in mythic_personas)


def test_screenplay_fastapi_endpoints() -> None:
    """Tests FastAPI screenplay and story endpoints."""
    # 1. Story premise endpoint
    premise_res = client.post(
        "/api/cinema/story/generate-premise",
        json={
            "core_theme": "Dharma vs Destiny",
            "target_audience": "Pan-Indian Theatrical Audience",
            "culture": "Mythic Epic & High-Energy Masala",
            "genre_track": "epic_historical",
        },
    )
    assert premise_res.status_code == 200
    premise_data = premise_res.json()
    assert "Dharma" in premise_data["title"]
    assert "Act_1_Departure" in premise_data["three_act_structure"]

    # 2. Format scene endpoint
    scene_res = client.post(
        "/api/cinema/screenplay/format-scene",
        json={
            "scene_heading": "int. command bridge - night",
            "characters_present": ["Commander", "AI Operator"],
            "action_description": "Holographic consoles flicker red as warning alarms sound.",
            "dramatic_intent": "Tension before hyperspace breach",
            "language": "en",
        },
    )
    assert scene_res.status_code == 200
    scene_data = scene_res.json()
    assert scene_data["scene_heading"] == "INT. COMMAND BRIDGE - NIGHT"
    assert len(scene_data["dialogue_blocks"]) == 2

    # 3. Shot list endpoint
    shotlist_res = client.get("/api/cinema/screenplay/shot-list/SCENE-99")
    assert shotlist_res.status_code == 200
    shots = shotlist_res.json()
    assert len(shots) == 4
    assert shots[0]["shot_id"] == "SCENE-99_S01"
