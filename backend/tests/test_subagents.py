"""Unit tests for modular cinema department subagents.

Verifies isolated behavior and 100% statement coverage.
"""

import pytest

from src.agents.subagents import (
    AnimationSakugaOpsSubAgent,
    AudioOpsSubAgent,
    DirectorOpsSubAgent,
    MartialArtsOpsSubAgent,
    OTTOpsSubAgent,
    ProducerOpsSubAgent,
    VFXOpsSubAgent,
)
from src.models.department import DepartmentEnum
from src.models.incident import StudioIncident


@pytest.mark.asyncio
async def test_director_subagent(sample_incident: StudioIncident) -> None:
    """Tests DirectorOpsSubAgent blast radius and narrative triage.

    Args:
        sample_incident: Fixture incident.
    """
    director = DirectorOpsSubAgent()

    # 1. Standard CDN alert
    sample_incident.telemetry.grafana_alert_uid = "Alert-OTT-504"
    res1 = await director.investigate(sample_incident)
    assert res1.agent_name == "DirectorOps"
    assert res1.department == DepartmentEnum.DIRECTING
    assert "query_cinematic_graph" in res1.mcp_tool_invoked

    # 2. VFX OOM alert branch
    sample_incident.telemetry.grafana_alert_uid = "Alert-VFX-CUDA-OOM"
    res2 = await director.investigate(sample_incident)
    assert res2.agent_name == "DirectorOps"


@pytest.mark.asyncio
async def test_producer_subagent(sample_incident: StudioIncident) -> None:
    """Tests ProducerOpsSubAgent financial exposure calculation.

    Args:
        sample_incident: Fixture incident.
    """
    producer = ProducerOpsSubAgent()
    sample_incident.box_office_at_risk_usd = 45000.0
    res = await producer.investigate(sample_incident)
    assert res.agent_name == "ProducerOps"
    assert res.department == DepartmentEnum.PRODUCING
    assert "$45,000.00" in res.tool_output_summary


@pytest.mark.asyncio
async def test_ott_subagent(sample_incident: StudioIncident) -> None:
    """Tests OTTOpsSubAgent CDN throughput triage.

    Args:
        sample_incident: Fixture incident.
    """
    ott = OTTOpsSubAgent()
    res = await ott.investigate(sample_incident)
    assert res.agent_name == "OTTOps"
    assert res.department == DepartmentEnum.OTT_DISTRIBUTION


@pytest.mark.asyncio
async def test_martial_arts_subagent(sample_incident: StudioIncident) -> None:
    """Tests MartialArtsOpsSubAgent Foley sync triage.

    Args:
        sample_incident: Fixture incident.
    """
    martial_arts = MartialArtsOpsSubAgent()
    sample_incident.telemetry.tempo_trace_id = "test-tempo-trace-42"
    res = await martial_arts.investigate(sample_incident)
    assert res.agent_name == "MartialArtsOps"
    assert "test-tempo-trace-42" in res.tool_output_summary


@pytest.mark.asyncio
async def test_animation_sakuga_subagent(sample_incident: StudioIncident) -> None:
    """Tests AnimationSakugaOpsSubAgent stepped render queue triage.

    Args:
        sample_incident: Fixture incident.
    """
    sakuga = AnimationSakugaOpsSubAgent()
    res = await sakuga.investigate(sample_incident)
    assert res.agent_name == "AnimationSakugaOps"
    assert res.department == DepartmentEnum.ANIMATION


@pytest.mark.asyncio
async def test_vfx_subagent(sample_incident: StudioIncident) -> None:
    """Tests VFXOpsSubAgent GPU VRAM and render metrics triage.

    Args:
        sample_incident: Fixture incident.
    """
    vfx = VFXOpsSubAgent()
    res = await vfx.investigate(sample_incident)
    assert res.agent_name == "VFXOps"
    assert res.department == DepartmentEnum.VFX
    assert "query_cinema_metrics" in res.mcp_tool_invoked


@pytest.mark.asyncio
async def test_audio_subagent(sample_incident: StudioIncident) -> None:
    """Tests AudioOpsSubAgent Dolby Atmos trace triage.

    Args:
        sample_incident: Fixture incident.
    """
    audio = AudioOpsSubAgent()
    sample_incident.telemetry.tempo_trace_id = ""
    res = await audio.investigate(sample_incident)
    assert res.agent_name == "AudioOps"
    assert res.department == DepartmentEnum.AUDIO
    assert "query_cinema_traces" in res.mcp_tool_invoked
