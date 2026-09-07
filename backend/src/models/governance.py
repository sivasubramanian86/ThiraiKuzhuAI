"""Cyber Governance, Content Protection, and Creative Writing Models.

Follows PEP 257 Google-style docstrings and Pydantic v2 schemas.
"""

from typing import Any

from pydantic import BaseModel, Field


class CyberThreatAuditRequest(BaseModel):
    """Payload to evaluate through Gemini 3.8 Flash Cyber security governance."""

    prompt_or_payload: str = Field(..., description="Telemetry command, script, or prompt to audit")
    source_service: str = Field(
        default="director_console", description="Originating studio service"
    )
    ip_address: str = Field(default="127.0.0.1", description="Caller IP address")
    user_role: str = Field(default="director", description="Caller IAM role")


class CyberThreatAuditResult(BaseModel):
    """Evaluation result from Gemini 3.8 Flash Cyber security governance engine."""

    is_safe: bool = Field(..., description="Whether the payload is safe to execute")
    threat_level: str = Field(
        ..., description="Threat classification: CLEAN, LOW, MEDIUM, CRITICAL"
    )
    prompt_injection_detected: bool = Field(
        default=False, description="Whether prompt injection was found"
    )
    credential_leak_detected: bool = Field(
        default=False, description="Whether secrets/keys are exposed"
    )
    recommended_action: str = Field(..., description="Recommended mitigation directive")
    audit_log_id: str = Field(..., description="Unique audit event reference ID")
    model_used: str = Field(
        default="gemini-3.8-flash-cyber", description="Evaluating cyber AI model"
    )


class ContentProtectionRequest(BaseModel):
    """Comprehensive media asset protection and digital rights verification request."""

    asset_id: str = Field(..., description="Unique media asset or scene ID")
    title: str = Field(..., description="Scene, song, or movie title")
    content_type: str = Field(
        ..., description="Media modality: 'video', 'audio', 'script', 'storyboard'"
    )
    content_text_or_url: str = Field(
        ..., description="Content body, screenplay segment, or asset URI"
    )
    drm_license_key: str = Field(
        default="", description="DRM license key or token for streaming rights"
    )
    perceptual_hash: str = Field(
        default="", description="pHash of image/video or Chromaprint of audio"
    )


class ContentProtectionResult(BaseModel):
    """Comprehensive content shield and digital rights verification verdict."""

    asset_id: str = Field(..., description="Target asset identifier")
    is_approved: bool = Field(..., description="Whether content passes all studio governance gates")
    governance_verdict: str = Field(
        ..., description="'APPROVED', 'NEEDS_LEGAL_REVIEW', 'REJECTED_ILLICIT'"
    )
    ai_generated_probability: float = Field(
        ..., ge=0.0, le=1.0, description="Probability of AI generation"
    )
    synthid_watermark_detected: bool = Field(
        default=False, description="SynthID forensic watermark status"
    )
    c2pa_provenance_verified: bool = Field(
        default=False, description="C2PA cryptographic provenance validity"
    )
    piracy_risk_level: str = Field(
        default="CLEAN", description="'CLEAN', 'SUSPECTED_LEAK', 'COMPROMISED_KEY'"
    )
    drm_license_valid: bool = Field(default=True, description="DRM license authorization status")
    illicit_content_detected: bool = Field(
        default=False, description="Flag for illegal/illicit content"
    )
    illicit_categories: list[str] = Field(
        default_factory=list, description="Categories flagged (e.g. 'violence', 'hate')"
    )
    duplicate_content_detected: bool = Field(
        default=False, description="Perceptual hash collision match"
    )
    copyright_similarity_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Similarity to existing protected IP"
    )
    patent_clearance: bool = Field(
        default=True, description="Proprietary filming technique patent clearance"
    )
    legal_recommendation: str = Field(
        ..., description="Actionable clearance advice for production crew"
    )


class ScriptPlagiarismCheckRequest(BaseModel):
    """Screenplay plagiarism and copyright infringement comparison request."""

    script_text: str = Field(..., description="Screenplay scene or dialogue text to audit")
    target_genre: str = Field(default="action_stunts", description="Genre track")
    known_reference_id: str = Field(default="", description="Optional comparative script ID")


class ScriptPlagiarismCheckResult(BaseModel):
    """Results of screenplay copyright similarity and patent protection check."""

    script_fingerprint: str = Field(
        ..., description="Cryptographic SHA-256 fingerprint of script text"
    )
    originality_score: float = Field(
        ..., ge=0.0, le=1.0, description="Script originality score (1.0 = 100% original)"
    )
    plagiarism_detected: bool = Field(
        ..., description="True if script similarity exceeds allowable fair-use threshold"
    )
    matched_prior_art: list[dict[str, Any]] = Field(
        default_factory=list, description="Similar existing scripts or story arcs"
    )
    patent_infringement_risk: str = Field(default="NONE", description="'NONE', 'LOW', 'HIGH'")
    clearance_status: str = Field(
        ..., description="'CLEARED_FOR_PRODUCTION', 'REVISE_BEATS', 'LEGAL_HOLD'"
    )


class StoryPremiseRequest(BaseModel):
    """Request for StoryWriterOps to draft a cinematic narrative premise."""

    genre_track: str = Field(
        ..., description="Cinematic genre track e.g. 'epic_historical', 'action_stunts'"
    )
    core_theme: str = Field(
        ..., description="Central thematic motif e.g. 'Dharma vs Modern AI Dominion'"
    )
    culture: str = Field(default="mythic_epic", description="Studio cultural tradition")
    target_runtime_minutes: int = Field(default=150, description="Target movie runtime")


class StoryPremiseResult(BaseModel):
    """Three-act narrative structure and character archetypes generated by StoryWriterOps."""

    title: str = Field(..., description="Working project title")
    logline: str = Field(..., description="One-sentence cinematic logline")
    three_act_structure: dict[str, str] = Field(
        ..., description="Act 1, Act 2, Act 3 structural breakdowns"
    )
    lead_characters: list[dict[str, str]] = Field(
        ..., description="Hero, Antagonist, and Mentor archetypes"
    )
    mythic_motifs: list[str] = Field(..., description="Core thematic and cultural motifs")


class ScreenplaySceneRequest(BaseModel):
    """Request for ScreenplayOps and DialogueWriterOps to format a screenplay scene."""

    scene_heading: str = Field(..., description="Slugline e.g. 'INT. ANCIENT TEMPLE VAULT - NIGHT'")
    characters_present: list[str] = Field(
        default_factory=list, description="Character names in the scene"
    )
    action_description: str = Field(
        ..., description="Visual camera directions and physical actions"
    )
    dialogue_intent: str = Field(
        default="", description="Emotional conflict or dramatic tension"
    )
    dramatic_intent: str = Field(
        default="", description="Dramatic intent or beat description"
    )
    language: str = Field(default="en", description="Dialogue language code e.g. 'ta', 'hi', 'en'")


class ScreenplaySceneResult(BaseModel):
    """Formatted industry-standard screenplay scene with localized dialogue."""

    scene_heading: str = Field(..., description="Standardized scene slugline")
    action_block: str = Field(..., description="Action descriptions in present tense")
    dialogue_blocks: list[dict[str, str]] = Field(
        ..., description="Character, parenthetical, and dialogue lines"
    )
    scene_pacing_tempo: str = Field(
        ..., description="Pacing directive: 'ALLEGRO', 'ANDANTE', 'PRESTO'"
    )
    camera_shot_suggestion: str = Field(
        ..., description="Recommended focal length and camera movement"
    )
