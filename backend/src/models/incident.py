"""Incident, Telemetry, and Investigation Models for Thirai Kuzhu AI.

Follows PEP 257 Google-style docstrings and Pydantic v2 schemas.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from src.models.department import CinemaGenreTrack, DepartmentEnum, StudioCulture


class SeverityLevel(str, Enum):
    """Incident severity classification aligned with Grafana IRM."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TechnicalTelemetry(BaseModel):
    """Raw infrastructure telemetry extracted from Grafana Cloud MCP."""

    grafana_alert_uid: str = Field(..., description="Grafana IRM Alert Rule UID")
    promql_metric: str = Field(default="", description="Prometheus PromQL query executed")
    loki_log_pattern: str = Field(default="", description="Loki LogQL pattern detected")
    tempo_trace_id: str = Field(default="", description="Tempo distributed trace ID")
    raw_telemetry_payload: dict[str, Any] = Field(
        default_factory=dict, description="Structured telemetry metrics and labels"
    )


class StudioIncident(BaseModel):
    """Represents a live film production or distribution incident."""

    id: str = Field(..., description="Unique incident identifier, e.g. 'INC-2026-OTT-504'")
    project_title: str = Field(..., description="Film or series title")
    sequence_affected: str = Field(..., description="Impacted scene or sequence name")
    culture: StudioCulture = Field(default=StudioCulture.HOLLYWOOD_TENTPOLE)
    genre_track: CinemaGenreTrack = Field(default=CinemaGenreTrack.ACTION_STUNTS)
    severity: SeverityLevel = Field(default=SeverityLevel.HIGH)
    departments_impacted: list[DepartmentEnum] = Field(default_factory=list)
    telemetry: TechnicalTelemetry
    cinematic_narrative: str = Field(
        default="", description="Human-readable film impact explanation"
    )
    box_office_at_risk_usd: float = Field(
        default=0.0, description="Real-time estimated financial exposure in USD"
    )
    director_directive: str = Field(
        default="", description="Operational mitigation ordered by DirectorOps"
    )
    grafana_annotated: bool = Field(
        default=False, description="Whether mitigation has been written to Grafana dashboard"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved: bool = Field(default=False)


class InvestigationRequest(BaseModel):
    """Request payload to dispatch the Thirai Kuzhu multi-agent mesh on an incident."""

    incident_id: str = Field(..., description="ID of incident to investigate")
    target_language: str = Field(
        default="en", description="Target language code (e.g. 'en', 'ta', 'fr')"
    )
    include_graph_rag: bool = Field(default=True, description="Enable blast radius graph traversal")


class AgentThoughtStep(BaseModel):
    """Represents a single thought step emitted by a department agent."""

    agent_name: str = Field(..., description="Emitting agent, e.g. 'VFXOps'")
    department: DepartmentEnum
    thought: str = Field(..., description="Reasoning and domain assessment")
    mcp_tool_invoked: str = Field(default="", description="Name of MCP tool called")
    tool_output_summary: str = Field(default="", description="Summary of tool telemetry result")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class InvestigationResponse(BaseModel):
    """Complete synthesized investigation report produced by Thirai Kuzhu Orchestrator."""

    incident_id: str
    project_title: str
    root_cause_summary: str
    cinematic_impact: str
    box_office_at_risk_usd: float
    mitigation_plan: list[str]
    agent_timeline: list[AgentThoughtStep]
    cri_score_after_mitigation: float
    grafana_annotation_status: str


class StudioProject(BaseModel):
    """Studio film production or series tracked by Thirai Kuzhu AI."""

    id: str
    title: str
    culture: StudioCulture
    genre_track: CinemaGenreTrack
    release_date: str
    status: str = "active"
    cri_score: float = 94.0


class CRIEvaluationReport(BaseModel):
    """Cinematic Readiness Index (CRI) evaluation report with radar metrics."""

    project_id: str
    cri_score: float
    overall_score: float
    radar_metrics: dict[str, float] = Field(default_factory=dict)
    verdict: str
    recommendations: list[str] = Field(default_factory=list)


class MitigationApplyRequest(BaseModel):
    """Request payload to execute automated director mitigation."""

    incident_id: str
    action_taken: str = Field(..., description="Mitigation action description")
    annotation_text: str = Field(..., description="Operational note to annotate on dashboard")
    dashboard_uid: str = Field(default="cinema-ops-main")


class MitigationApplyResponse(BaseModel):
    """Response returned upon applying a mitigation action."""

    status: str = "applied"
    success: bool = True
    incident_id: str
    message: str
    grafana_annotation_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
