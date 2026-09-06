"""ProducerOps subagent for financial exposure and release schedule risk.

Follows PEP 257 Google-style docstrings.
"""

from src.agents.subagents.base import BaseSubAgent
from src.models.department import DepartmentEnum
from src.models.incident import AgentThoughtStep, StudioIncident


class ProducerOpsSubAgent(BaseSubAgent):
    """Calculates box office capital protection and release risk."""

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Computes financial risk exposure for the incident.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: ProducerOps assessment finding.
        """
        exposure_usd = incident.box_office_at_risk_usd
        return AgentThoughtStep(
            agent_name="ProducerOps",
            department=DepartmentEnum.PRODUCING,
            thought="Calculating immediate box-office-at-risk and subscriber churn exposure.",
            mcp_tool_invoked="calculate_box_office_risk",
            tool_output_summary=f"Estimated financial exposure at ${exposure_usd:,.2f} USD.",
        )
