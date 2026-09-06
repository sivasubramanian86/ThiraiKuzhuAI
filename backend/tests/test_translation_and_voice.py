"""Unit and integration tests for Translation and Voice services.

Follows PEP 257 Google-style docstrings and enforces 100% statement coverage.
"""

import base64

import pytest
from httpx import AsyncClient

from src.tools.translation_service import CinemaTranslationService
from src.tools.voice_service import CinemaVoiceService


@pytest.mark.asyncio
async def test_translation_service_direct() -> None:
    """Tests CinemaTranslationService with empty text, English, Tamil, and fallback."""
    service = CinemaTranslationService()

    # 1. Empty text
    empty_res = await service.translate_narrative("", "ta")
    assert empty_res["translated_text"] == ""
    assert empty_res["glossary_applied"] is True

    # 2. English text pass-through
    en_res = await service.translate_narrative("Standard incident on PromQL", "en")
    assert en_res["translated_text"] == "Standard incident on PromQL"

    # 3. Tamil translation with lexicon substitution and preserved tokens
    sample_text = (
        "Report: video playback stall and box office at risk. "
        "Verified with PromQL metric cdn_5xx_rate and SMPTE standard."
    )
    ta_res = await service.translate_narrative(sample_text, "ta")
    assert "காணொளித் தேக்கம்" in ta_res["translated_text"]
    assert "வசூல் இழப்பு அபாயம்" in ta_res["translated_text"]
    assert "PromQL" in ta_res["preserved_tokens"]
    assert "SMPTE" in ta_res["preserved_tokens"]
    assert "cdn_5xx_rate" in ta_res["preserved_tokens"]

    # 4. Unknown language fallback with prefix
    sv_res = await service.translate_narrative("Nordic noir pipeline alert", "sv")
    assert "[SV Studio Feed]" in sv_res["translated_text"]


@pytest.mark.asyncio
async def test_voice_service_direct() -> None:
    """Tests CinemaVoiceService voice profiles, squelch markers, and base64 output."""
    voice = CinemaVoiceService()

    # 1. English director voice
    en_voice = await voice.synthesize_walkie_talkie_alert(
        script_text="All cameras roll on sequence 14.",
        language_code="en",
        speaker_name="DirectorOps",
    )
    assert en_voice["voice_name"] == "en-US-Neural2-J"
    assert en_voice["speaker"] == "DirectorOps"
    assert en_voice["audio_encoding"] == "MP3_RADIO_SQUELCH"

    decoded_en = base64.b64decode(en_voice["audio_base64"]).decode("utf-8")
    assert "[SQUELCH_START]" in decoded_en
    assert "[SQUELCH_END]" in decoded_en

    # 2. Tamil Neural2 voice
    ta_voice = await voice.synthesize_walkie_talkie_alert(
        script_text="தயாரிப்பு தயாராக உள்ளது.",
        language_code="ta-IN",
        speaker_name="ProducerOps",
    )
    assert ta_voice["voice_name"] == "ta-IN-Neural2-A"

    # 3. Fallback voice for unknown language
    unk_voice = await voice.synthesize_walkie_talkie_alert(
        script_text="Testing generic radio squelch.",
        language_code="xx-ZZ",
        speaker_name="TechLead",
    )
    assert unk_voice["voice_name"] == "en-US-Neural2-J"


@pytest.mark.asyncio
async def test_translation_and_voice_api_routes(async_client: AsyncClient) -> None:
    """Tests /api/translation/translate and /api/voice/synthesize endpoints.

    Args:
        async_client: Async HTTP client fixture.
    """
    # 1. Translate API
    trans_payload = {
        "text": "Critical video playback stall reported on sequence 14.",
        "target_language": "hi",
    }
    trans_resp = await async_client.post("/api/translation/translate", json=trans_payload)
    assert trans_resp.status_code == 200
    trans_data = trans_resp.json()
    assert "वीडियो रुकावट" in trans_data["translated_text"]

    # 2. Voice API
    voice_payload = {
        "script_text": "Mitigation applied: traffic re-routed to Mumbai origin.",
        "language_code": "fr",
        "speaker_name": "OTTOps",
    }
    voice_resp = await async_client.post("/api/voice/synthesize", json=voice_payload)
    assert voice_resp.status_code == 200
    voice_data = voice_resp.json()
    assert voice_data["voice_name"] == "fr-FR-Neural2-A"
    assert voice_data["speaker"] == "OTTOps"
    assert len(voice_data["audio_base64"]) > 20
