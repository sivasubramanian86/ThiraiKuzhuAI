"""Department, Persona, and Genre Track Models for Thirai Kuzhu AI.

Follows PEP 257 Google-style docstrings and Pydantic v2 schemas.
"""

from enum import Enum

from pydantic import BaseModel, Field


class StudioCulture(str, Enum):
    """Global cinematic studio cultures supported by Thirai Kuzhu AI."""

    HOLLYWOOD_TENTPOLE = "hollywood_tentpole"
    EAST_ASIAN_ANIME = "east_asian_anime"
    EUROPEAN_AUTEUR = "european_auteur"
    MYTHIC_EPIC = "mythic_epic"
    GLOBAL_OTT = "global_ott"
    INDIE_LEAN = "indie_lean"


class CinemaGenreTrack(str, Enum):
    """Universal world cinema genre tracks modeled in pipeline telemetry."""

    ANIMATION = "animation"
    ACTION_STUNTS = "action_stunts"
    MARTIAL_ARTS_WUXIA = "martial_arts_wuxia"
    CULT_CLASSIC_NEO_NOIR = "cult_classic_neo_noir"
    EPIC_HISTORICAL = "epic_historical"
    MUSICALS_MASALA = "musicals_masala"


class DepartmentEnum(str, Enum):
    """Studio departments represented in the Thirai Kuzhu multi-agent mesh."""

    DIRECTING = "directing"
    PRODUCING = "producing"
    VFX = "vfx"
    ACTION_STUNTS = "action_stunts"
    MARTIAL_ARTS = "martial_arts"
    ANIMATION = "animation"
    CINEMATOGRAPHY = "cinematography"
    AUDIO = "audio"
    EDITING = "editing"
    OTT_DISTRIBUTION = "ott_distribution"
    MARKETING = "marketing"
    LEGAL = "legal"
    STORY_WRITING = "story_writing"
    SCREENPLAY = "screenplay"
    DIALOGUE_WRITING = "dialogue_writing"
    CYBER_GOVERNANCE = "cyber_governance"
    COPYRIGHT_LEGAL = "copyright_legal"


class DepartmentPersona(BaseModel):
    """Represents a specialized cinematic crew agent persona."""

    id: str = Field(..., description="Unique persona identifier")
    culture: StudioCulture = Field(..., description="Cinematic cultural archetype")
    genre_track: CinemaGenreTrack = Field(..., description="Specialized world cinema genre")
    department: DepartmentEnum = Field(..., description="Studio department scope")
    name_en: str = Field(..., description="English designation, e.g. 'DirectorOps'")
    name_fr: str = Field(default="", description="French designation")
    name_ja: str = Field(default="", description="Japanese designation")
    name_ta: str = Field(default="", description="Tamil designation, e.g. 'இயக்குநர்'")
    name_hi: str = Field(default="", description="Hindi designation")
    system_prompt_directive: str = Field(..., description="Directives injected into Gemini")
    compliance_standards: list[str] = Field(
        default_factory=list, description="Industry standards tracked, e.g. SMPTE, DCI, ACES, EBU"
    )
