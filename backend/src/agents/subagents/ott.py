"""OTTOps subagent for streaming distribution, CDN health, and transcoding pipelines.

Follows PEP 257 Google-style docstrings.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident
from src.tools.telemetry_tools import query_cinema_metrics


class OTTOpsSubAgent(BaseSubAgent):
    """Monitors CDN edge hit ratios, origin transcode latency, and ABR stream health."""

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Executes PromQL telemetry triage on OTT edge delivery.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: OTTOps telemetry finding.
        """
        metrics = await query_cinema_metrics(
            query_type="cdn_throughput", project_id=incident.project_title
        )
        return AgentThoughtStep(
            agent_name="OTTOps",
            department=DepartmentEnum.OTT_DISTRIBUTION,
            thought="Inspecting CDN edge hit ratio and origin transcode latency.",
            mcp_tool_invoked="query_cinema_metrics",
            tool_output_summary=metrics.get(
                "summary",
                f"PromQL confirmed {incident.telemetry.promql_metric or 'CDN 5xx spike'}.",
            ),
        )
