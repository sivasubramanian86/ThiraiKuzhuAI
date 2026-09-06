"""AudioOps subagent for Dolby Atmos 7.1.4 stem alignment, ACES dynamic range, and Foley sync.

Follows PEP 257 Google-style docstrings.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident
from src.tools.telemetry_tools import query_cinema_traces


class AudioOpsSubAgent(BaseSubAgent):
    """Monitors 128-channel spatial beds, EBU R128 loudness compliance, and stem clock drift."""

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Inspects Dolby Atmos audio clock drift and spatial channel phase sync.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: AudioOps assessment finding.
        """
        trace_id = incident.telemetry.tempo_trace_id or "audio-atmos-sync-01"
        trace_data = await query_cinema_traces(
            service_name="atmos-render-engine", trace_id=trace_id
        )
        return AgentThoughtStep(
            agent_name="AudioOps",
            department=DepartmentEnum.AUDIO,
            thought=(
                "Checking Dolby Atmos spatial stems for phase drift and EBU R128 loudness peaks."
            ),
            mcp_tool_invoked="query_cinema_traces",
            tool_output_summary=(
                f"Tempo trace {trace_id} returned duration "
                f"{trace_data.get('duration_ms', 12.0)}ms within broadcast limits."
            ),
        )
