"""DirectorOps subagent for creative vision and narrative blast radius assessment.

Follows PEP 257 Google-style docstrings.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident
from src.tools.telemetry_tools import query_cinematic_graph


class DirectorOpsSubAgent(BaseSubAgent):
    """Assesses narrative continuity, emotional pacing, and blast radius across scenes."""

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Evaluates narrative risk using Cinematic Graph RAG.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: DirectorOps assessment finding.
        """
        fault_node = incident.telemetry.grafana_alert_uid.lower()
        if "oom" in fault_node or "vfx" in fault_node:
            node_key = "vfx-node-14"
        else:
            node_key = "cdn-origin-southasia"

        blast_radius = await query_cinematic_graph(fault_node_id=node_key)
        affected_shots_str = ", ".join(blast_radius.get("affected_shots", ["Shot 112"]))

        return AgentThoughtStep(
            agent_name="DirectorOps",
            department=DepartmentEnum.DIRECTING,
            thought=(
                f"Assessing narrative risk for '{incident.project_title}', "
                f"sequence '{incident.sequence_affected}'."
            ),
            mcp_tool_invoked="query_cinematic_graph",
            tool_output_summary=(
                f"Identified {len(blast_radius.get('affected_shots', []))} shots "
                f"impacted ({affected_shots_str})."
            ),
        )
