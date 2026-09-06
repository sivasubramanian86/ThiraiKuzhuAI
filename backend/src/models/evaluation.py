"""Evaluation, Indices, and Narrative Report Models for Thirai Kuzhu AI.

Follows PEP 257 Google-style docstrings and Pydantic v2 schemas.
"""

from typing import Any

from pydantic import BaseModel, Field


class CinematicIndices(BaseModel):
    """Four core quantitative cinematic indices for studio intelligence."""

    cri_score: float = Field(..., ge=0.0, le=100.0, description="Cinematic Readiness Index (0-100)")
    aer_score: float = Field(
        ..., ge=0.0, le=1.0, description="Audience Experience Risk (0.0=safe, 1.0=severe)"
    )
    ucs_score: float = Field(
        ..., ge=0.0, le=100.0, description="Universe Continuity Stability (0-100)"
    )
    cwv_score: float = Field(..., ge=0.0, le=100.0, description="Crew Workload Volatility (0-100)")
    release_blocked: bool = Field(
        default=False, description="Whether the production is blocked from release due to AER > 0.7"
    )
    component_breakdown: dict[str, float] = Field(
        default_factory=dict, description="Raw component inputs and sub-metrics"
    )


class SceneCriticalReport(BaseModel):
    """High-impact executive report translating technical telemetry to film narrative."""

    incident_id: str = Field(..., description="Unique incident identifier")
    project_title: str = Field(..., description="Film production title")
    sequence_affected: str = Field(..., description="Film scene or sequence affected")
    departments_impacted: list[str] = Field(
        default_factory=list, description="List of studio departments involved"
    )
    technical_telemetry: dict[str, Any] = Field(
        default_factory=dict, description="Underlying Grafana alert and metric snapshot"
    )
    cinematic_narrative: str = Field(
        ..., description="Creative explanation of scene impact and audience experience"
    )
    box_office_at_risk_usd: float = Field(..., ge=0.0, description="Financial capital at risk")
    director_mitigation_directive: str = Field(
        ..., description="Director instructions for resolution"
    )
    grafana_annotation_posted: bool = Field(
        default=False, description="Whether Grafana dashboard annotation was posted"
    )


class UniverseBulletin(BaseModel):
    """Franchise-level executive digest monitoring asset and timeline consistency."""

    franchise_name: str = Field(..., description="Franchise or cinematic universe title")
    active_productions: list[str] = Field(
        default_factory=list, description="Titles of linked films or series"
    )
    overall_ucs_score: float = Field(
        ..., ge=0.0, le=100.0, description="Franchise-wide continuity score"
    )
    asset_drift_summary: str = Field(
        ..., description="Summary of 3D asset drift and timeline consistency"
    )
    vfx_version_drift_detected: bool = Field(
        default=False, description="Flag indicating asset version mismatch across branches"
    )
    recommended_action: str = Field(..., description="Actionable recommendation for showrunners")


class DirectorsPostMortem(BaseModel):
    """Post-incident retrospective synthesizing timeline and permanent mitigations."""

    incident_id: str = Field(..., description="Incident identifier")
    project_title: str = Field(..., description="Film production title")
    incident_timeline: list[dict[str, str]] = Field(
        default_factory=list, description="Chronological event log from alert to resolution"
    )
    crew_communication_log: list[dict[str, str]] = Field(
        default_factory=list, description="Inter-department deliberation excerpts"
    )
    root_cause_analysis: str = Field(..., description="Technical and cinematic root cause summary")
    permanent_mitigations: list[str] = Field(
        default_factory=list, description="Permanent pipeline architectural safeguards"
    )
    box_office_recovered_usd: float = Field(
        ..., ge=0.0, description="Financial loss prevented by mitigation"
    )


class LLMJudgeScore(BaseModel):
    """Evaluation grading score produced by LLM-as-a-Judge for agent responses."""

    technical_accuracy: float = Field(
        ..., ge=1.0, le=5.0, description="Precision of Grafana PromQL/LogQL interpretation (1-5)"
    )
    cinematic_relevance: float = Field(
        ..., ge=1.0, le=5.0, description="Grounding in scenes, shots, and audience experience (1-5)"
    )
    actionability: float = Field(
        ..., ge=1.0, le=5.0, description="Concreteness of proposed mitigation (1-5)"
    )
    overall_grade: float = Field(
        ..., ge=1.0, le=5.0, description="Weighted average quality score (1-5)"
    )
    passed_benchmark: bool = Field(
        ..., description="True if overall_grade >= 4.5/5.0 benchmark target"
    )
    feedback: str = Field(..., description="Detailed qualitative feedback for agent improvement")
