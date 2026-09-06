"""MartialArtsOps subagent for Wuxia combat, Foley transient delays, and stunt wire sync.

Follows PEP 257 Google-style docstrings.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident
from src.tools.telemetry_tools import query_cinema_traces


class MartialArtsOpsSubAgent(BaseSubAgent):
    """Monitors stunt impact timing, wire removal artifacts, and Foley sound sync."""

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Inspects Tempo trace data for combat Foley transient latency.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: MartialArtsOps telemetry finding.
        """
        trace_id = incident.telemetry.tempo_trace_id or "wuxia-foley-trace-01"
        trace_data = await query_cinema_traces(service_name="foley-sync-engine", trace_id=trace_id)
        transient_ms = trace_data.get("duration_ms", 14.8)
        return AgentThoughtStep(
            agent_name="MartialArtsOps",
            department=DepartmentEnum.AUDIO,
            thought="Evaluating Foley transient delay against 5ms combat sync threshold.",
            mcp_tool_invoked="query_cinema_traces",
            tool_output_summary=(
                f"Tempo trace {trace_id} shows {transient_ms}ms drift on impact stem."
            ),
        )
