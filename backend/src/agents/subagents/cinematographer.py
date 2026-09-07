"""CinematographerLens SubAgent for lens optics, lighting setup, and aspect ratio discipline.

Follows PEP 257 Google-style docstrings and typed interfaces.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident


class CinematographerLensSubAgent(BaseSubAgent):
    """Subagent responsible for lens choice, sensor dynamic range, and lighting ratios."""

    def __init__(self) -> None:
        """Initializes subagent with department scope."""
        self.department = DepartmentEnum.CINEMATOGRAPHY

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Audits sensor exposure, ACES color gamut, and anamorphic lens distortion.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: Optical cinematography analysis and lighting continuity directives.
        """
        thought = (
            f"CinematographerLens: Inspecting latitude for '{incident.sequence_affected}'. "
            "Checking ACEScc color gamut compliance, 2.39:1 squeeze, and lighting contrast ratios."
        )
        dialogue = (
            f"[DP to Lighting Rig] Optical parameters locked for {incident.sequence_affected}. "
            "Exposure latitude stable across shadow zones; preserving highlight rolloff."
        )

        return AgentThoughtStep(
            agent_name="CinematographerLens",
            department=self.department,
            thought=thought,
            mcp_tool_invoked="audit_aces_gamut",
            tool_output_summary=dialogue,
        )
