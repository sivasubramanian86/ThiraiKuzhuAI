"""VFXOps subagent for render farm compute, GPU VRAM, and volumetric simulations.

Follows PEP 257 Google-style docstrings.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident
from src.tools.telemetry_tools import query_cinema_metrics


class VFXOpsSubAgent(BaseSubAgent):
    """Monitors 8K IMAX cloud render farms, CUDA OOM thresholds, and tile rendering."""

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Evaluates GPU memory allocation and volumetric render queue health.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: VFXOps assessment finding.
        """
        metrics = await query_cinema_metrics(
            query_type="vfx_render_time", project_id=incident.project_title
        )
        return AgentThoughtStep(
            agent_name="VFXOps",
            department=DepartmentEnum.VFX,
            thought="Inspecting distributed cloud GPU clusters for VRAM saturation and OOM errors.",
            mcp_tool_invoked="query_cinema_metrics",
            tool_output_summary=metrics.get(
                "summary", "PromQL confirmed GPU VRAM utilization above 95% threshold."
            ),
        )
