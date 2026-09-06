"""Base interface for all Thirai Kuzhu cinema department subagents.

Follows PEP 257 Google-style docstrings and typed interfaces.
"""

from abc import ABC, abstractmethod

from src.models.incident import AgentThoughtStep, StudioIncident


class BaseSubAgent(ABC):
    """Abstract base class for cinema department operational subagents."""

    @abstractmethod
    async def investigate(self, incident: StudioIncident) -> AgentThoughtStep:
        """Executes department-specific technical investigation and telemetry triage.

        Args:
            incident: Target studio incident object.

        Returns:
            AgentThoughtStep: Structured reasoning and findings.
        """
