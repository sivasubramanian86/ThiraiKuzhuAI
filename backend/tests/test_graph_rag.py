"""Unit tests for Cinematic Knowledge Graph RAG Service.

Follows PEP 257 Google-style docstrings and rigorous assertions.
"""

import pytest

from src.models.department import CinemaGenreTrack, StudioCulture
from src.services.graph_rag_service import BlastRadiusReport, CinematicGraphService


@pytest.mark.asyncio
async def test_graph_rag_vfx_node_traversal() -> None:
    """Tests multi-hop traversal starting from failing VFX GPU node."""
    service = CinematicGraphService()
    report: BlastRadiusReport = await service.get_blast_radius(
        fault_node_id="vfx-node-14",
        genre_track=CinemaGenreTrack.ACTION_STUNTS,
        culture=StudioCulture.HOLLYWOOD_TENTPOLE,
    )

    assert report.origin_node_id == "vfx-node-14"
    assert report.origin_type == "hardware_node"
    assert any("Mine" in s for s in report.affected_shots)
    assert any("Scene 08" in s for s in report.affected_scenes)
    assert report.box_office_at_risk_usd == 15000.00
    assert "texture mipmaps" in report.recommended_mitigation.lower()


@pytest.mark.asyncio
async def test_graph_rag_cdn_origin_traversal() -> None:
    """Tests multi-hop traversal starting from CDN origin transcoder."""
    service = CinematicGraphService()
    report: BlastRadiusReport = await service.get_blast_radius(
        fault_node_id="cdn-origin-southasia",
        genre_track=CinemaGenreTrack.EPIC_HISTORICAL,
        culture=StudioCulture.MYTHIC_EPIC,
    )

    assert report.origin_node_id == "cdn-origin-southasia"
    assert any("Coronation" in s for s in report.affected_scenes)
    assert report.box_office_at_risk_usd == 38500.00
    assert "mumbai pop bypass" in report.recommended_mitigation.lower()


@pytest.mark.asyncio
async def test_graph_rag_unknown_node_fallback() -> None:
    """Tests graceful fallback when querying an unmapped hardware node."""
    service = CinematicGraphService()
    report: BlastRadiusReport = await service.get_blast_radius(fault_node_id="unregistered-node-99")

    assert report.origin_node_id == "unregistered-node-99"
    assert len(report.affected_shots) >= 1
    assert len(report.affected_scenes) >= 1
    assert report.box_office_at_risk_usd > 0.0


@pytest.mark.asyncio
async def test_graph_rag_cycle_handling() -> None:
    """Tests graph traversal when graph contains converging diamond edges."""
    from src.services.graph_rag_service import CinematicNode

    service = CinematicGraphService()
    service.nodes["start"] = CinematicNode(id="start", label="Start", node_type="hardware")
    service.nodes["branch-1"] = CinematicNode(id="branch-1", label="B1", node_type="hardware")
    service.nodes["branch-2"] = CinematicNode(id="branch-2", label="B2", node_type="hardware")
    service.nodes["converged"] = CinematicNode(id="converged", label="C", node_type="shot")

    service.edges["start"] = ["branch-1", "branch-2"]
    service.edges["branch-1"] = ["converged"]
    service.edges["branch-2"] = ["converged"]

    report = await service.get_blast_radius(fault_node_id="start")
    assert report.origin_node_id == "start"
    assert "C" in report.affected_shots
