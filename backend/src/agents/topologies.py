"""Orchestration Topologies for Thirai Kuzhu AI Screen Crew.

Features:
1. Bounded concurrency parallel fan-out per Band (Section 21 policy table).
2. Sequential dependency chains.
3. Multi-agent debate & arbitration loops.
4. Telemetry gather stage for Grafana signal aggregation.
Follows PEP 257 Google-style docstrings.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from src.agents.factory import AgentFactory

# Section 21 Concurrency Limits per Band
CONCURRENCY_POLICY: dict[str, int] = {
    "A": 10,
    "B": 15,
    "C": 20,
    "D": 30,
    "E": 25,
    "F": 30,
    "G": 20,
    "H": 12,
    "I": 20,
    "J": 20,
    "K": 50,
    "L": 20,
    "M": 50,
    "N": 10,
    "O": 30,
    "P": 15,
    "Q": 8,
    "COMP": 8,
    "ANTG": 5,
}

# Arbitration Rules
ARBITRATION_RULES: dict[tuple[str, str], str] = {
    ("B01", "C04"): "C02",  # Director vs Line Producer -> Executive Producer arbitrates
    ("G01", "G09"): "B01",  # Music Director vs Music Supervisor -> Director arbitrates
    ("L01", "O09"): "C01",  # Distribution Head vs Festival Programmer -> Producer arbitrates
    ("H01", "B01"): "H01",  # Fight Master vs Director -> Fight Master STOP authority wins
}


class OrchestrationTopologies:
    """Manages multi-agent execution topologies across bands."""

    def __init__(self, factory: AgentFactory | None = None) -> None:
        """Initialize topology manager with agent factory."""
        self.factory = factory or AgentFactory()

    def run_band_fanout(
        self, band: str, prompt: str, script_version: str = "1.0", max_workers: int | None = None
    ) -> list[dict[str, Any]]:
        """Execute parallel fan-out for all personas in a band with bounded concurrency."""
        personas = self.factory.registry.list_by_band(band)
        if not personas:
            return []

        limit = max_workers or CONCURRENCY_POLICY.get(band, 10)
        results: list[dict[str, Any]] = []

        with ThreadPoolExecutor(max_workers=min(limit, len(personas))) as executor:
            future_to_id = {
                executor.submit(
                    self.factory.materialize(p.id, script_version=script_version).execute, prompt
                ): p.id
                for p in personas
            }
            for future in as_completed(future_to_id):
                try:
                    res = future.result()
                    results.append(res)
                except Exception as e:
                    results.append({"agent_id": future_to_id[future], "error": str(e)})

        return sorted(results, key=lambda x: x.get("agent_id", ""))

    def run_sequential_chain(
        self, persona_ids: list[str], initial_prompt: str, script_version: str = "1.0"
    ) -> list[dict[str, Any]]:
        """Run sequential dependent chain where each persona receives predecessor output."""
        chain_log: list[dict[str, Any]] = []
        current_input = initial_prompt

        for p_id in persona_ids:
            agent = self.factory.materialize(p_id, script_version=script_version)
            step_result = agent.execute(current_input)
            chain_log.append(step_result)
            current_input = f"{step_result['thought']}\nDirective: {step_result['decision']}"

        return chain_log

    def run_debate(
        self, persona_a_id: str, persona_b_id: str, topic: str, script_version: str = "1.0"
    ) -> dict[str, Any]:
        """Orchestrate a structured debate and apply defined arbitration rules."""
        agent_a = self.factory.materialize(persona_a_id, script_version=script_version)
        agent_b = self.factory.materialize(persona_b_id, script_version=script_version)

        # 1. Opposing arguments
        arg_a = agent_a.execute(f"Debate position on: {topic}")
        arg_b = agent_b.execute(f"Counter-position on: {topic}")

        # 2. Check arbitration rule
        pair = (persona_a_id, persona_b_id)
        reverse_pair = (persona_b_id, persona_a_id)
        arbitrator_id = ARBITRATION_RULES.get(pair) or ARBITRATION_RULES.get(reverse_pair)

        if not arbitrator_id:
            # Default to Director (B01) or Producer (C01)
            arbitrator_id = "B01" if "B01" not in pair else "C01"

        arbitrator = self.factory.materialize(arbitrator_id, script_version=script_version)
        ruling = arbitrator.execute(
            f"Arbitrate between {persona_a_id} and {persona_b_id} on topic '{topic}':\n"
            f"- {persona_a_id} argues: {arg_a['decision']}\n"
            f"- {persona_b_id} argues: {arg_b['decision']}"
        )

        return {
            "topic": topic,
            "debater_a": {
                "id": persona_a_id,
                "name": agent_a.persona.display_name.en,
                "argument": arg_a["decision"],
            },
            "debater_b": {
                "id": persona_b_id,
                "name": agent_b.persona.display_name.en,
                "argument": arg_b["decision"],
            },
            "arbitrator": {
                "id": arbitrator_id,
                "name": arbitrator.persona.display_name.en,
                "ruling": ruling["decision"],
            },
            "status": "RESOLVED",
        }

    def gather_band_telemetry(self, step_results: list[dict[str, Any]]) -> dict[str, Any]:
        """Aggregate band step outputs into a single narrative and metric set for Grafana."""
        total_tokens = sum(r.get("tokens_consumed", 0) for r in step_results)
        blocking_vetoes = [
            r["agent_name"]
            for r in step_results
            if r.get("can_block") and "blocking" in r.get("thought", "").lower()
        ]
        all_metrics: dict[str, float] = {}

        for r in step_results:
            for k, v in r.get("metrics_reported", {}).items():
                all_metrics[k] = all_metrics.get(k, 0.0) + float(v)

        return {
            "agents_reported_count": len(step_results),
            "total_tokens_consumed": total_tokens,
            "has_blocking_veto": len(blocking_vetoes) > 0,
            "blocking_agents": blocking_vetoes,
            "aggregated_metrics": all_metrics,
            "narrative_summary": (
                f"Aggregated output across {len(step_results)} crew agents. Pipeline operational."
            ),
        }
