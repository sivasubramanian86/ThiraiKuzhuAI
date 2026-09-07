"""Comprehensive Unit Tests for Persona Registry, Topologies, Spawner and API.

Tests:
1. Complete 369-persona catalog loading and band integrity.
2. Search and filter capabilities.
3. Rejection of invalid bands, invalid escalation targets, cycles, and PII violations.
4. Agent factory materialization, model tier mapping, and tool bind filtering.
5. Orchestration topologies, bounded fan-out, debate arbitration, and telemetry gather.
6. Dynamic SME Spawner entity extraction and advisor generation.
7. Antagonist engine red-team attack vectors.
8. FastAPI REST endpoints for all Phase 5 capabilities.
Follows PEP 257 Google-style docstrings.
"""

from typing import Any

import pytest
from fastapi.testclient import TestClient

from src.agents.antagonists import AntagonistEngine
from src.agents.factory import AgentFactory
from src.agents.sme_spawner import DynamicSMESpawner
from src.agents.topologies import OrchestrationTopologies
from src.main import app
from src.personas.loader import (
    GrafanaSignalConfig,
    PersonaAuthority,
    PersonaDefinition,
    PersonaDisplayName,
    PersonaRegistry,
    load_registry,
)


@pytest.fixture
def client() -> TestClient:
    """Provide FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def registry() -> PersonaRegistry:
    """Provide loaded registry."""
    return load_registry()


def test_registry_completeness(registry: PersonaRegistry) -> None:
    """Assert all 369 personas across 19 bands are present."""
    all_p = registry.all_personas()
    assert len(all_p) == 369

    # Check that key core personas exist
    assert registry.get("A01") is not None
    assert registry.get("A02") is not None
    assert registry.get("A03") is not None
    assert registry.get("B01") is not None
    assert registry.get("H01") is not None
    assert registry.get("I36") is not None
    assert registry.get("E23") is not None  # Addition: Light Boy Helper
    assert registry.get("COMP01") is not None  # Composite: Continuity Guardian
    assert registry.get("ANTG01") is not None  # Antagonist: Schedule Breaker


def test_registry_search_and_filters(registry: PersonaRegistry) -> None:
    """Test searching by keyword and band filtering."""
    results = registry.search("fight")
    assert len(results) > 0
    assert any(p.id == "H01" for p in results)

    # Filter by band
    band_a = registry.list_by_band("A")
    assert len(band_a) == 17
    band_h = registry.list_by_band("H")
    assert len(band_h) == 12


def test_registry_validation_rejects_unknown_band() -> None:
    """Ensure loader rejects unknown band outside valid taxonomy."""
    with pytest.raises(ValueError, match="Unknown band 'Z'"):
        PersonaDefinition(
            id="Z01",
            slug="unknown_band_role",
            display_name=PersonaDisplayName(en="Unknown"),
            band="Z",
            band_name="Invalid Band",
            mandate="Invalid mandate",
            authority=PersonaAuthority(),
            grafana_signals=GrafanaSignalConfig(),
            context_cache_key="test",
        )


def test_registry_validation_rejects_strict_pii_with_raw_media() -> None:
    """Ensure loader rejects strict PII policy when granted raw media tools."""
    with pytest.raises(ValueError, match="pii_policy='strict' but is granted raw media tools"):
        PersonaDefinition(
            id="A99",
            slug="strict_pii_violator",
            display_name=PersonaDisplayName(en="Strict Violator"),
            band="A",
            band_name="Story",
            mandate="Audit",
            authority=PersonaAuthority(),
            tools_allowed=["studio.export_raw_dailies"],
            grafana_signals=GrafanaSignalConfig(),
            context_cache_key="test",
            pii_policy="strict",
        )


def test_registry_integrity_rejects_unknown_escalation_target() -> None:
    """Ensure registry rejects personas that escalate to non-existent IDs."""
    bad_persona = PersonaDefinition(
        id="T01",
        slug="bad_target",
        display_name=PersonaDisplayName(en="Bad Target"),
        band="A",
        band_name="Story",
        mandate="Audit",
        authority=PersonaAuthority(escalates_to=["NON_EXISTENT_ID"]),
        grafana_signals=GrafanaSignalConfig(),
        context_cache_key="test",
    )
    with pytest.raises(ValueError, match="escalates to unknown target ID: 'NON_EXISTENT_ID'"):
        PersonaRegistry([bad_persona])


def test_registry_integrity_rejects_cyclic_escalations() -> None:
    """Ensure registry rejects cyclic dependency in escalation hierarchy."""
    node_a = PersonaDefinition(
        id="CYC_A",
        slug="cycle_a",
        display_name=PersonaDisplayName(en="Cycle A"),
        band="A",
        band_name="Story",
        mandate="Audit",
        authority=PersonaAuthority(escalates_to=["CYC_B"]),
        grafana_signals=GrafanaSignalConfig(),
        context_cache_key="test",
    )
    node_b = PersonaDefinition(
        id="CYC_B",
        slug="cycle_b",
        display_name=PersonaDisplayName(en="Cycle B"),
        band="A",
        band_name="Story",
        mandate="Audit",
        authority=PersonaAuthority(escalates_to=["CYC_A"]),
        grafana_signals=GrafanaSignalConfig(),
        context_cache_key="test",
    )
    with pytest.raises(ValueError, match="Detected cyclic dependency in escalates_to"):
        PersonaRegistry([node_a, node_b])


def test_agent_factory_materialization(registry: PersonaRegistry) -> None:
    """Test materializing subagent with tool filtering and model tiering."""
    factory = AgentFactory(registry)
    agent = factory.materialize("B01", script_version="2.1")
    assert agent.persona.id == "B01"
    assert agent.resolved_model == "gemini-2.5-pro"
    assert agent.resolved_cache_key == "persona:B01:v2.1"
    assert "governance.raise_blocking_veto" in agent.active_tools

    # Test step execution
    res = agent.execute("Review climax action safety.")
    assert res["agent_id"] == "B01"
    assert res["can_block"] is True
    assert "Director" in res["agent_name"]


def test_agent_factory_budget_degradation(registry: PersonaRegistry) -> None:
    """Test graceful degradation to cheap tier when budget is constrained."""
    factory = AgentFactory(registry)
    agent = factory.materialize("B01", budget_constraint=1000)
    assert agent.effective_token_budget == 1000
    assert agent.resolved_model == "gemini-2.5-flash"  # Degraded from reasoning


def test_agent_factory_unknown_persona(registry: PersonaRegistry) -> None:
    """Test factory raises KeyError on unknown persona ID."""
    factory = AgentFactory(registry)
    with pytest.raises(KeyError, match="Persona 'INVALID' not found"):
        factory.materialize("INVALID")


def test_topologies_fanout_and_gather(registry: PersonaRegistry) -> None:
    """Test parallel fan-out across a band and telemetry gathering."""
    factory = AgentFactory(registry)
    topologies = OrchestrationTopologies(factory)

    results = topologies.run_band_fanout(band="H", prompt="Action sequence check", max_workers=4)
    assert len(results) == 12  # All Band H personas
    assert results[0]["band"] == "H"

    gathered = topologies.gather_band_telemetry(results)
    assert gathered["agents_reported_count"] == 12
    assert gathered["total_tokens_consumed"] > 0
    assert "aggregated_metrics" in gathered


def test_topologies_sequential_chain(registry: PersonaRegistry) -> None:
    """Test sequential dependency chain."""
    factory = AgentFactory(registry)
    topologies = OrchestrationTopologies(factory)

    chain = topologies.run_sequential_chain(
        ["A01", "A02", "A03"], initial_prompt="Original concept idea"
    )
    assert len(chain) == 3
    assert chain[0]["agent_id"] == "A01"
    assert chain[1]["agent_id"] == "A02"
    assert chain[2]["agent_id"] == "A03"


def test_topologies_debate_arbitration(registry: PersonaRegistry) -> None:
    """Test debate between Director and Line Producer arbitrated by Executive Producer."""
    factory = AgentFactory(registry)
    topologies = OrchestrationTopologies(factory)

    debate = topologies.run_debate(
        persona_a_id="B01", persona_b_id="C04", topic="Helicopter stunt crash vs CGI plate"
    )
    assert debate["status"] == "RESOLVED"
    assert debate["debater_a"]["id"] == "B01"
    assert debate["debater_b"]["id"] == "C04"
    assert debate["arbitrator"]["id"] == "C02"  # Executive Producer arbitrated


def test_dynamic_sme_spawner(registry: PersonaRegistry) -> None:
    """Test dynamic entity extraction and on-demand advisor synthesis."""
    spawner = DynamicSMESpawner(registry)
    screenplay_snippet = (
        "EXT. ROYAL TEMPLE GATES - NIGHT\n"
        "The police constable draws his firearm. The doctor enters the ICU ward with a scalpel. "
        "Submarine sonar pings in the distance while Chola empire inscriptions glow."
    )
    res = spawner.analyze_script_and_spawn(screenplay_snippet)
    assert len(res["detected_entities"]) > 0
    assert "I01" in res["mapped_seed_advisors"]  # Police
    assert "I04" in res["mapped_seed_advisors"]  # Medical
    assert len(res["dynamically_spawned_advisors"]) > 0
    dyn = res["dynamically_spawned_advisors"][0]
    assert dyn["authority"]["can_block"] is False  # Strictly advisory
    assert len(dyn["advisor_output"]["checklist"]) > 0


def test_antagonist_engine_all_vectors() -> None:
    """Test all 5 adversarial red-team stress attack vectors."""
    engine = AntagonistEngine()
    for antag_id in ["ANTG01", "ANTG02", "ANTG03", "ANTG04", "ANTG05"]:
        attack = engine.simulate_attack(
            antagonist_id=antag_id, project_title="Baahubali III", scene_description="Climax Battle"
        )
        assert attack["status"] == "STRESS_TEST_COMPLETED"
        assert attack["antagonist_id"] == antag_id
        assert len(attack["recommended_countermeasures"]) > 0


def test_topologies_edge_cases(registry: PersonaRegistry) -> None:
    """Test arbitration fallback, gather blocking vetoes, and fanout errors."""
    factory = AgentFactory(registry)
    topologies = OrchestrationTopologies(factory)

    # Debate with unknown pair defaults to Director or Producer
    res = topologies.run_debate("A01", "A02", "Story point arbitration")
    assert res["status"] == "RESOLVED"
    assert res["arbitrator"]["id"] in ["B01", "C01"]

    # Gather with blocking veto
    mock_results = [
        {
            "agent_id": "H01",
            "agent_name": "Fight Master",
            "can_block": True,
            "thought": "[Fight Master] Raising blocking veto on unsafe wire rig.",
            "tokens_consumed": 200,
            "metrics_reported": {"safety_alert": 1.0},
        }
    ]
    gathered = topologies.gather_band_telemetry(mock_results)
    assert gathered["has_blocking_veto"] is True
    assert "Fight Master" in gathered["blocking_agents"]

    # Unknown band fanout returns empty
    empty_fanout = topologies.run_band_fanout("UNKNOWN_BAND", "Prompt")
    assert empty_fanout == []

    # Fanout error handling
    class FailingAgent:
        def execute(self, prompt: str) -> None:
            raise RuntimeError("Simulated thread execution crash")

    class FailingFactory(AgentFactory):
        def materialize(self, persona_id: str, **kwargs: Any) -> FailingAgent:
            return FailingAgent()

    failing_topologies = OrchestrationTopologies(FailingFactory(registry))
    failing_res = failing_topologies.run_band_fanout("ANTG", "Prompt")
    assert len(failing_res) > 0
    assert any("error" in r for r in failing_res)


def test_loader_default_and_missing_file() -> None:
    """Test load_registry default path, yaml path, and file not found error."""
    reg = load_registry()
    assert len(reg.all_personas()) == 369

    # Load via yaml extension (resolves to json)
    from pathlib import Path

    yaml_file = Path(__file__).resolve().parent.parent / "src" / "personas" / "registry.yaml"
    reg_yaml = load_registry(yaml_file)
    assert len(reg_yaml.all_personas()) == 369

    with pytest.raises(FileNotFoundError, match="not found at:"):
        load_registry("non_existent_file.yaml")


# =========================================================================
# API Endpoints Integration Tests
# =========================================================================


def test_api_list_personas(client: TestClient) -> None:
    """Test GET /api/v1/personas with various filters."""
    res = client.get("/api/v1/personas")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 369

    # Filter by band
    res_band = client.get("/api/v1/personas?band=B")
    assert res_band.status_code == 200
    assert res_band.json()["total"] == 15

    # Filter by search
    res_search = client.get("/api/v1/personas?search=fight")
    assert res_search.status_code == 200
    assert res_search.json()["total"] > 0

    # Filter by model_tier and budget_line
    res_tier_budget = client.get("/api/v1/personas?model_tier=reasoning&budget_line=ATL")
    assert res_tier_budget.status_code == 200
    assert res_tier_budget.json()["total"] > 0


def test_api_get_persona_detail(client: TestClient) -> None:
    """Test GET /api/v1/personas/{id} success and 404."""
    res = client.get("/api/v1/personas/H01")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == "H01"
    assert data["slug"] == "fight_master"
    assert data["authority"]["can_block"] is True

    # 404 case
    res_404 = client.get("/api/v1/personas/NONEXISTENT")
    assert res_404.status_code == 404


def test_api_sme_spawn(client: TestClient) -> None:
    """Test POST /api/v1/personas/sme/spawn endpoint."""
    payload = {
        "screenplay_text": (
            "The surgeon handles the scalpel while police officers secure the crime scene."
        )
    }
    res = client.post("/api/v1/personas/sme/spawn", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "I01" in data["mapped_seed_advisors"]

    # Empty payload 400
    res_bad = client.post("/api/v1/personas/sme/spawn", json={"screenplay_text": "   "})
    assert res_bad.status_code == 400


def test_api_persona_debate(client: TestClient) -> None:
    """Test POST /api/v1/personas/debate endpoint."""
    payload = {
        "persona_a_id": "B01",
        "persona_b_id": "C04",
        "topic": "Practical pyro explosion vs digital render",
    }
    res = client.post("/api/v1/personas/debate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "RESOLVED"
    assert data["arbitrator"]["id"] == "C02"

    # Bad persona ID
    res_bad = client.post(
        "/api/v1/personas/debate", json={"persona_a_id": "UNKNOWN", "persona_b_id": "C04"}
    )
    assert res_bad.status_code == 404


def test_api_antagonist_simulate(client: TestClient) -> None:
    """Test POST /api/v1/personas/antagonist/simulate endpoint."""
    payload = {
        "antagonist_id": "ANTG03",
        "project_title": " Baahubali III",
        "scene_description": "Second act midpoint reveal",
    }
    res = client.post("/api/v1/personas/antagonist/simulate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "STRESS_TEST_COMPLETED"
    assert data["antagonist_id"] == "ANTG03"


def test_api_multimodal_analyze(client: TestClient) -> None:
    """Test POST /api/v1/multimodal/analyze endpoint."""
    payload = {
        "sample_id": "sample_foley_01",
        "media_type": "audio",
        "title": "Sword Clash Foley Take 4",
    }
    res = client.post("/api/v1/multimodal/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["sample_id"] == "sample_foley_01"
    assert data["audio_foley_telemetry"] is not None
    assert "director_verdict" in data
