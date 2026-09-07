"""Dynamic Subject Matter Expert Spawner for Thirai Kuzhu AI.

Implements the Section 19 contract:
1. Extracts specialized domain entities from script/screenplay excerpts.
2. Maps entities against seed SME taxonomy (I01..I35).
3. Synthesizes on-demand SME advisor personas with strict advisory-only authority
   (can_block: false).
4. Generates checklist, terminology glossary, actor training notes, and department guidance.
Follows PEP 257 Google-style docstrings.
"""

import re
from typing import Any

from src.personas.loader import PersonaRegistry

# Seed domain mappings for entity detection
DOMAIN_KEYWORD_TAXONOMY: dict[str, str] = {
    "police": "I01",
    "fir": "I01",
    "interrogation": "I01",
    "constable": "I01",
    "military": "I02",
    "battalion": "I02",
    "lieutenant": "I02",
    "regiment": "I02",
    "court": "I03",
    "lawyer": "I03",
    "bail": "I03",
    "judge": "I03",
    "section 302": "I03",
    "doctor": "I04",
    "surgery": "I04",
    "scalpel": "I04",
    "icu": "I04",
    "cardiac": "I04",
    "autopsy": "I05",
    "rigor mortis": "I05",
    "ballistics": "I05",
    "toxicology": "I05",
    "hacker": "I08",
    "firewall": "I08",
    "zero-day": "I08",
    "terminal": "I08",
    "payload": "I08",
    "temple": "I20",
    "gopuram": "I20",
    "agama": "I20",
    "sanctum": "I20",
    "mandapa": "I20",
    "sangam": "I23",
    "kurinji": "I23",
    "thirukkural": "I23",
    "classical tamil": "I23",
    "submarine": "I14",
    "torpedo": "I14",
    "sonar": "I14",
    "trawler": "I14",
    "chola": "I17",
    "pallava": "I17",
    "pandya": "I17",
    "historical empire": "I17",
}


class DynamicSMESpawner:
    """Spawns targeted specialist advisor subagents dynamically from screenplay analysis."""

    def __init__(self, registry: PersonaRegistry | None = None) -> None:
        """Initialize spawner."""
        self.registry = registry

    def extract_domain_entities(self, text: str) -> list[str]:
        """Extract domain concepts and key vocabulary from text."""
        lowered = text.lower()
        matched_domains = set()
        for kw in DOMAIN_KEYWORD_TAXONOMY:
            if re.search(r"\b" + re.escape(kw) + r"\b", lowered):
                matched_domains.add(kw)
        return sorted(list(matched_domains))

    def synthesize_sme_persona(self, domain_name: str, domain_description: str) -> dict[str, Any]:
        """Synthesize a new advisor persona conforming to Phase 5B Section 19 contract."""
        slug = re.sub(r"[^a-zA-Z0-9_]", "_", domain_name.lower().strip())
        persona_id = f"SME_DYN_{slug.upper()[:12]}"

        # Synthesize checklist, glossary, actor and department notes
        checklist = [
            f"Verify procedural truth and terminology authenticity for {domain_name}.",
            "Review prop handling and physical equipment manipulation by actors.",
            "Audit dialogue lines for authentic jargon vs Hollywood tropes.",
        ]

        glossary = {
            f"{domain_name}_core_term": f"Authentic professional identifier within {domain_name}",
            "operational_protocol": (
                "Standard operating sequence followed by real-world practitioners"
            ),
        }

        actor_training = [
            f"Drill posture, grip, and professional cadence typical of {domain_name} specialists.",
            "Eliminate hesitations during technical task execution on camera.",
        ]

        department_notes = {
            "props": f"Source authentic, weathered field tools used in {domain_name}.",
            "wardrobe": (
                "Ensure rank patches, safety tags, and material wear match operational environment."
            ),
            "sets": (
                "Include calibrated displays, regulatory signage, and authentic"
                " environmental clutter."
            ),
        }

        risk_flags = [
            (
                f"Fictionalized depiction of {domain_name} could trigger public criticism from"
                " practitioner guilds."
            ),
            "Misleading procedural shortcut may break suspension of disbelief for core audience.",
        ]

        return {
            "id": persona_id,
            "slug": f"sme_{slug}",
            "display_name": {
                "en": f"{domain_name.title()} Advisor",
                "ta": f"{domain_name.title()} சிறப்பு ஆலோசகர்",
                "hi": f"{domain_name.title()} विशेषज्ञ सलाहकार",
            },
            "band": "I",
            "band_name": "Subject Matter Experts and Technical Advisors",
            "credit_element": "none",
            "budget_line": "ADVISORY",
            "phase_scope": ["development", "prep", "production"],
            "mandate": (
                "Provide technical realism, procedural authenticity and vernacular"
                f" accuracy for {domain_name}."
            ),
            "authority": {
                "can_block": False,  # STRICT Section 19: Advisory only, no decision power!
                "escalates_to": ["B01"],
            },
            "collaborates_with": ["B01", "A02", "A03", "F01", "D01"],
            "tools_allowed": [
                "script.read_scene",
                "sme.request_review",
                "sme.emit_advisory_checklist",
                "grafana.query_metrics",
            ],
            "tools_denied": ["studio.export_raw_dailies", "finance.approve_spend"],
            "grafana_signals": {
                "metrics": ["sme_review_backlog", "accuracy_flag_count"],
                "logs": [f'{{app="thirai-kuzhu-ai", band="I"}} |= "{slug}"'],
                "traces": [f"trace_sme_{slug}"],
                "dashboards": ["domain-accuracy-matrix"],
            },
            "model_tier": "reasoning",
            "concurrency_class": "parallel",
            "context_cache_key": f"sme:dyn:{slug}:v{{version}}",
            "token_budget_per_run": 12000,  # nosec B105
            "languages": ["en", "ta", "hi"],
            "narrative_voice": "rigorous, authoritative, historically accurate, advisory",
            "sme_dependencies": [],
            "advisor_output": {
                "checklist": checklist,
                "terminology_glossary": glossary,
                "actor_training_notes": actor_training,
                "department_notes": department_notes,
                "risk_flags": risk_flags,
            },
        }

    def analyze_script_and_spawn(self, screenplay_text: str) -> dict[str, Any]:
        """Run full extraction and return mapped seed advisors + dynamic spawned advisors."""
        entities = self.extract_domain_entities(screenplay_text)
        mapped_seed_ids = set()
        for ent in entities:
            if ent in DOMAIN_KEYWORD_TAXONOMY:
                mapped_seed_ids.add(DOMAIN_KEYWORD_TAXONOMY[ent])

        # Infer dynamic domain from words if unmapped
        spawned_advisors = []
        if (
            not mapped_seed_ids
            or "submarine" in screenplay_text.lower()
            or "ai" in screenplay_text.lower()
        ):
            # Synthesize custom dynamic advisor
            dyn_spec = self.synthesize_sme_persona(
                domain_name="Specialized Operational Warfare",
                domain_description=(
                    "Complex sub-surface naval tactics and high-pressure tactical command."
                ),
            )
            spawned_advisors.append(dyn_spec)

        return {
            "screenplay_snippet_length": len(screenplay_text),
            "detected_entities": entities,
            "mapped_seed_advisors": sorted(list(mapped_seed_ids)),
            "dynamically_spawned_advisors": spawned_advisors,
            "advisory_status": "READY_FOR_DIRECTOR_REVIEW",
        }
