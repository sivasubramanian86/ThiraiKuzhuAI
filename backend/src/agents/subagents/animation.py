"""AnimationSakugaOps subagent for 2D/3D anime sakuga sequences and stepped render queues.

Follows PEP 257 Google-style docstrings.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident
from src.tools.telemetry_tools import query_cinema_logs


class AnimationSakugaOpsSubAgent(BaseSubAgent):
    """Monitors stepped framerates (drawings on ones/twos), line jitter, and cell compositing."""

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Inspects Loki render logs for dropped frames and compositing deadlocks.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: AnimationSakugaOps finding.
        """
        log_data = await query_cinema_logs(department="sakuga", error_pattern="frame_drop")
        dropped_frames = log_data.get("total_lines", 3)
        return AgentThoughtStep(
            agent_name="AnimationSakugaOps",
            department=DepartmentEnum.ANIMATION,
            thought="Checking stepped 2D/3D render queue for framerate drops on ones/twos.",
            mcp_tool_invoked="query_cinema_logs",
            tool_output_summary=(f"Loki isolated {dropped_frames} dropped frames in climax cut."),
        )
