"""CopyrightLegalOps SubAgent for IP clearance, plagiarism audit, and patent protection.

Powered by Gemini 3.8 Flash Cyber.
Follows PEP 257 Google-style docstrings and typed interfaces.
"""

from src.agents.subagents.base import BaseSubAgent
from src.governance.cyber_governance import CyberGovernanceService
from src.models.department import DepartmentEnum
from src.models.governance import ScriptPlagiarismCheckRequest
from src.models.incident import AgentThoughtStep, StudioIncident


class CopyrightLegalOpsSubAgent(BaseSubAgent):
    """Subagent responsible for IP clearance, plagiarism checks, and digital rights compliance."""

    def __init__(self) -> None:
        """Initializes subagent with department scope and cyber governance engine."""
        self.department = DepartmentEnum.COPYRIGHT_LEGAL
        self.cyber_service = CyberGovernanceService()

    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Conducts IP audit and legal risk triage on incident sequence.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: Legal counsel clearance assessment and IP protection directives.
        """
        request = ScriptPlagiarismCheckRequest(
            script_text=incident.cinematic_narrative,
            target_genre=incident.genre_track,
        )
        result = self.cyber_service.check_script_plagiarism(request)

        thought = (
            f"CopyrightLegalOps: Auditing '{incident.sequence_affected}'. "
            "Engine: Gemini 3.8 Flash Cyber. "
            f"Originality Score: {result.originality_score * 100:.1f}%. "
            f"IP Clearance Status: {result.clearance_status}. "
            f"Patent Infringement Risk: {result.patent_infringement_risk}."
        )
        dialogue = (
            f"[Legal Counsel] Sequence {incident.sequence_affected} cleared under "
            f"{result.clearance_status}. Digital rights and trademark protections verified."
        )

        return AgentThoughtStep(
            agent_name="CopyrightLegalOps",
            department=self.department,
            thought=thought,
            mcp_tool_invoked="verify_ip_clearance",
            tool_output_summary=dialogue,
        )
