"""StoryWriterOps SubAgent for narrative premise and mythic arc development.

Follows PEP 257 Google-style docstrings and typed interfaces.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident


class StoryWriterOpsSubAgent(BaseSubAgent):
    """Subagent responsible for overarching story architecture, themes, and narrative stakes."""

    def __init__(self) -> None:
        """Initializes subagent with department scope."""
        self.department = DepartmentEnum.STORY_WRITING

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Evaluates narrative stakes and thematic continuity impacted by the incident.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: Story writer's thematic evaluation and continuity directives.
        """
        thought = (
            f"StoryWriterOps: Analyzing narrative consequences for '{incident.sequence_affected}'. "
            "Preserving emotional catharsis, hero archetype integrity, and pacing stakes."
        )
        dialogue = (
            f"[Story Lead to Director] Narrative checkpoint for {incident.sequence_affected}. "
            "Ensure character motivations remain uncompromised despite pipeline triage."
        )

        return AgentThoughtStep(
            agent_name="StoryWriterOps",
            department=self.department,
            thought=thought,
            mcp_tool_invoked="audit_narrative_continuity",
            tool_output_summary=dialogue,
        )
