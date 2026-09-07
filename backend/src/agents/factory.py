"""ADK and Gemini Agent Factory for Thirai Kuzhu AI.

Materializes typed PersonaDefinition instances into executable Google Cloud ADK / Gemini subagents:
1. Model tier selection (cheap -> Flash Lite, standard -> Flash, reasoning -> Pro).
2. Tool allow-list and deny-list enforcement at bind time.
3. Context cache key resolution.
4. Token budget enforcement with graceful fidelity degradation.
Follows PEP 257 Google-style docstrings.
"""

from typing import Any

from src.personas.loader import PersonaDefinition, PersonaRegistry, load_registry

MODEL_TIER_MAPPING: dict[str, str] = {
    "cheap": "gemini-2.5-flash-lite",
    "standard": "gemini-2.5-flash",
    "reasoning": "gemini-2.5-pro",
}

FALLBACK_MODEL_TIER: dict[str, str] = {
    "reasoning": "standard",
    "standard": "cheap",
    "cheap": "cheap",
}


class MaterializedAgent:
    """Represents a fully configured, bind-time verified subagent."""

    def __init__(
        self,
        persona: PersonaDefinition,
        resolved_model: str,
        active_tools: list[str],
        resolved_cache_key: str,
        effective_token_budget: int,
    ) -> None:
        """Initialize materialized agent with bound tools and model."""
        self.persona = persona
        self.resolved_model = resolved_model
        self.active_tools = active_tools
        self.resolved_cache_key = resolved_cache_key
        self.effective_token_budget = effective_token_budget

    def execute(self, prompt: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Simulate agent step execution under bound constraints."""
        context = context or {}
        # Format response tailored to persona narrative voice and language
        lang = context.get("language", "en")
        title = (
            getattr(self.persona.display_name, lang, self.persona.display_name.en)
            or self.persona.display_name.en
        )

        return {
            "agent_id": self.persona.id,
            "agent_name": title,
            "band": self.persona.band,
            "model_used": self.resolved_model,
            "tokens_consumed": min(self.effective_token_budget, len(prompt.split()) * 4 + 150),
            "cache_key_hit": self.resolved_cache_key,
            "tools_available": self.active_tools,
            "can_block": self.persona.authority.can_block,
            "thought": f"[{title}] Analyzing situation under mandate: '{self.persona.mandate}'",
            "decision": f"Approved and verified per {self.persona.band_name} cinematic standards.",
            "metrics_reported": {m: 1.0 for m in self.persona.grafana_signals.metrics[:2]},
        }


class AgentFactory:
    """Factory to instantiate subagents from persona specifications."""

    def __init__(self, registry: PersonaRegistry | None = None) -> None:
        """Initialize factory with persona registry."""
        self.registry = registry or load_registry()

    def materialize(
        self,
        persona_id: str,
        script_version: str = "1.0",
        available_tools: list[str] | None = None,
        budget_constraint: int | None = None,
    ) -> MaterializedAgent:
        """Create a bound agent respecting allow/deny lists and token budgets."""
        persona = self.registry.get(persona_id)
        if not persona:
            raise KeyError(f"Persona '{persona_id}' not found in registry.")

        # 1. Model tier selection with token budget degradation
        target_tier = persona.model_tier
        effective_budget = persona.token_budget_per_run

        if budget_constraint is not None and budget_constraint < effective_budget:
            # Degrade model tier if budget is constrained
            target_tier = FALLBACK_MODEL_TIER.get(target_tier, "cheap")
            effective_budget = budget_constraint

        resolved_model = MODEL_TIER_MAPPING.get(target_tier, "gemini-2.5-flash")

        # 2. Bind-time tool filtering (Allow-list minus Deny-list)
        system_tools = available_tools if available_tools is not None else persona.tools_allowed
        allowed_set = set(persona.tools_allowed).intersection(set(system_tools))
        denied_set = set(persona.tools_denied)
        active_tools = sorted(list(allowed_set - denied_set))

        # 3. Context cache key resolution
        resolved_cache_key = persona.context_cache_key.format(version=script_version)

        return MaterializedAgent(
            persona=persona,
            resolved_model=resolved_model,
            active_tools=active_tools,
            resolved_cache_key=resolved_cache_key,
            effective_token_budget=effective_budget,
        )
