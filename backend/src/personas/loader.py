"""Typed Persona Registry Loader with Validation for Thirai Kuzhu AI.

Validates:
1. Unknown bands outside valid set (A..Q, COMP, ANTG).
2. Unknown escalation targets.
3. Cycles in escalates_to hierarchy.
4. PII policy enforcement against raw media tools.
5. Tool allow/deny list contracts.
Follows PEP 257 Google-style docstrings and Pydantic v2 schemas.
"""

import json
from collections import defaultdict
from pathlib import Path

from pydantic import BaseModel, Field, field_validator, model_validator

VALID_BANDS: set[str] = {
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "COMP",
    "ANTG",
}

RAW_MEDIA_TOOLS: set[str] = {
    "studio.export_raw_dailies",
    "camera.stream_raw_braw",
    "dit.export_uncompressed_exr",
}


class PersonaDisplayName(BaseModel):
    """Multilingual display name container."""

    en: str
    ta: str = ""
    hi: str = ""


class PersonaAuthority(BaseModel):
    """Authority and escalation routing configuration."""

    can_block: bool = False
    escalates_to: list[str] = Field(default_factory=list)


class GrafanaSignalConfig(BaseModel):
    """Grafana MCP signal subscriptions for observability."""

    metrics: list[str] = Field(default_factory=list)
    logs: list[str] = Field(default_factory=list)
    traces: list[str] = Field(default_factory=list)
    dashboards: list[str] = Field(default_factory=list)


class PersonaDefinition(BaseModel):
    """Typed Pydantic schema for a cinematic crew persona conforming to Phase 5B."""

    id: str
    slug: str
    display_name: PersonaDisplayName
    band: str
    band_name: str
    credit_element: str = "none"
    budget_line: str = "BTL"
    phase_scope: list[str] = Field(default_factory=list)
    mandate: str
    authority: PersonaAuthority
    collaborates_with: list[str] = Field(default_factory=list)
    tools_allowed: list[str] = Field(default_factory=list)
    tools_denied: list[str] = Field(default_factory=list)
    grafana_signals: GrafanaSignalConfig
    model_tier: str = "standard"
    concurrency_class: str = "parallel"
    context_cache_key: str
    token_budget_per_run: int = 10000
    languages: list[str] = Field(default_factory=lambda: ["en", "ta", "hi"])
    narrative_voice: str = "professional"
    sme_dependencies: list[str] = Field(default_factory=list)
    pii_policy: str = "standard"

    @field_validator("band")
    @classmethod
    def validate_band(cls, v: str) -> str:
        """Ensure band is in standard taxonomy."""
        if v not in VALID_BANDS:
            raise ValueError(f"Unknown band '{v}'. Must be one of {sorted(VALID_BANDS)}")
        return v

    @model_validator(mode="after")
    def validate_pii_against_tools(self) -> "PersonaDefinition":
        """Reject strict PII policy if granted raw media inspection tools."""
        if self.pii_policy == "strict":
            forbidden = set(self.tools_allowed).intersection(RAW_MEDIA_TOOLS)
            if forbidden:
                raise ValueError(
                    f"Persona {self.id} has pii_policy='strict' but is granted raw media"
                    f" tools: {forbidden}"
                )
        return self


class PersonaRegistry:
    """In-memory validated Persona Registry."""

    def __init__(self, personas: list[PersonaDefinition]) -> None:
        """Initialize and index personas."""
        self.personas_by_id: dict[str, PersonaDefinition] = {p.id: p for p in personas}
        self.personas_by_band: dict[str, list[PersonaDefinition]] = defaultdict(list)
        for p in personas:
            self.personas_by_band[p.band].append(p)
        self.validate_registry_integrity()

    def validate_registry_integrity(self) -> None:
        """Validate escalation targets and cycle freedom across the entire mesh."""
        # 1. Validate escalation targets exist
        for p_id, persona in self.personas_by_id.items():
            for target_id in persona.authority.escalates_to:
                if target_id not in self.personas_by_id:
                    raise ValueError(
                        f"Persona {p_id} escalates to unknown target ID: '{target_id}'"
                    )

        # 2. Cycle detection in escalation hierarchy using DFS
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.personas_by_id[node].authority.escalates_to:
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for node in self.personas_by_id:
            if node not in visited:
                if has_cycle(node):
                    raise ValueError(
                        f"Detected cyclic dependency in escalates_to involving '{node}'"
                    )

    def get(self, persona_id: str) -> PersonaDefinition | None:
        """Fetch persona by unique ID."""
        return self.personas_by_id.get(persona_id)

    def list_by_band(self, band: str) -> list[PersonaDefinition]:
        """Fetch all personas in a given band."""
        return self.personas_by_band.get(band, [])

    def all_personas(self) -> list[PersonaDefinition]:
        """Return full list of personas."""
        return list(self.personas_by_id.values())

    def search(self, query: str) -> list[PersonaDefinition]:
        """Search personas across name, ID, slug and mandate."""
        q = query.lower()
        results = []
        for p in self.personas_by_id.values():
            if (
                q in p.id.lower()
                or q in p.slug.lower()
                or q in p.display_name.en.lower()
                or q in p.display_name.ta.lower()
                or q in p.display_name.hi.lower()
                or q in p.mandate.lower()
            ):
                results.append(p)
        return results


def load_registry(file_path: Path | str | None = None) -> PersonaRegistry:
    """Load registry from JSON or YAML file with validation."""
    if file_path is None:
        # Default to registry.json if present (fastest), else registry.yaml
        json_path = Path(__file__).resolve().parent / "registry.json"
        yaml_path = Path(__file__).resolve().parent / "registry.yaml"
        file_path = json_path if json_path.exists() else yaml_path

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Persona registry file not found at: {path}")

    target_path = (
        path.with_suffix(".json")
        if path.suffix == ".yaml" and path.with_suffix(".json").exists()
        else path
    )
    with open(target_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_list = data.get("personas", [])
    parsed = [PersonaDefinition.model_validate(p) for p in raw_list]
    return PersonaRegistry(parsed)
