"""Tests for Multimodal Generative Cinema Service (Veo 2 & Lyria Integration).

Validates:
1. Multimodal Scene Asset Ingestion & Continuity Analysis
2. Google DeepMind Veo 2 Prompt Expansion & Shot Synthesis
3. Google DeepMind Lyria Score, Orchestral Leitmotif, and Foley Synthesis
4. Full Cinematic Reel Compilation & Packaging
5. FastAPI Endpoints for Multimodal, Veo, and Lyria Synthesis
"""

from fastapi.testclient import TestClient

from src.main import app
from src.models.department import CinemaGenreTrack, StudioCulture
from src.services.multimodal_cinema_service import (
    LyriaScoreGenerationRequest,
    LyriaScoreGenerationResult,
    MultimodalCinemaService,
    MultimodalSceneAsset,
    VeoVideoGenerationRequest,
    VeoVideoGenerationResult,
)

client = TestClient(app)


class TestMultimodalCinemaService:
    """Validates standalone service logic for Veo and Lyria generation."""

    def test_multimodal_analysis_complete_assets(self) -> None:
        """Verifies multimodal analysis when both visual and acoustic stems are present."""
        service = MultimodalCinemaService()
        asset = MultimodalSceneAsset(
            scene_id="SCENE-01-EXPEDITION",
            script_prompt="The explorer gazes at the bioluminescent monolith in the rain.",
            visual_reference_b64="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            acoustic_reference_b64="UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQAAAAA=",
            culture=StudioCulture.HOLLYWOOD_TENTPOLE,
            genre_track=CinemaGenreTrack.ACTION_STUNTS,
        )
        report = service.analyze_multimodal_assets(asset)
        assert report["scene_id"] == "SCENE-01-EXPEDITION"
        assert report["has_visual_frame"] is True
        assert report["has_acoustic_stem"] is True
        assert report["continuity_risk_score"] == 0.0
        assert "Multimodal alignment nominal" in report["director_recommendations"][0]

    def test_multimodal_analysis_missing_assets(self) -> None:
        """Verifies risk calculation and remediation advice when assets are missing."""
        service = MultimodalCinemaService()
        asset = MultimodalSceneAsset(
            scene_id="SCENE-02-BAMBOO",
            script_prompt="Sword clash atop the bamboo canopy under full moonlight.",
            visual_reference_b64=None,
            acoustic_reference_b64=None,
            culture=StudioCulture.EAST_ASIAN_ANIME,
            genre_track=CinemaGenreTrack.MARTIAL_ARTS_WUXIA,
        )
        report = service.analyze_multimodal_assets(asset)
        assert report["has_visual_frame"] is False
        assert report["has_acoustic_stem"] is False
        assert report["continuity_risk_score"] > 0.20
        assert len(report["director_recommendations"]) == 2

    def test_veo_2_video_generation(self) -> None:
        """Verifies Veo 2 prompt expansion and video render metadata synthesis."""
        service = MultimodalCinemaService()
        request = VeoVideoGenerationRequest(
            director_prompt="Hero steps out from the burning fortress, slow motion rain",
            genre_track=CinemaGenreTrack.EPIC_HISTORICAL,
            camera_movement="tracking_crane_tilt",
            aspect_ratio="2.39:1",
            resolution="4K",
            duration_seconds=12.5,
            fps=24,
        )
        result: VeoVideoGenerationResult = service.generate_veo_video_scene(request)
        assert "VEO-SHOT-" in result.shot_id
        assert "Cinematic 4K master shot" in result.expanded_veo_prompt
        assert "tracking_crane_tilt" in result.expanded_veo_prompt
        assert result.render_status == "COMPLETED"
        assert result.camera_metadata["fps"] == 24
        assert result.camera_metadata["duration_seconds"] == 12.5

    def test_lyria_score_and_foley_generation(self) -> None:
        """Verifies Lyria musical leitmotif and Dolby Atmos spatial audio bed synthesis."""
        service = MultimodalCinemaService()
        request = LyriaScoreGenerationRequest(
            scene_mood="triumphant",
            musical_scale="D_Minor_Epic",
            tempo_bpm=135,
            instrumentation=["Symphonic Strings", "Taiko War Drums"],
            foley_elements=["Sword Clashes", "Arrow Whistle"],
        )
        result: LyriaScoreGenerationResult = service.generate_lyria_score(request)
        assert "LYRIA-TRK-" in result.track_id
        assert "Triumphant" in result.musical_theme
        assert "D_Minor_Epic" in result.musical_theme
        assert len(result.stems_generated) == 4
        assert result.dolby_atmos_bed_active is True
        assert result.lufs_loudness == -14.0

    def test_assemble_movie_reel(self) -> None:
        """Verifies compilation of multiple Veo shots and Lyria audio into final cinema reel."""
        service = MultimodalCinemaService()
        shot1 = service.generate_veo_video_scene(
            VeoVideoGenerationRequest(director_prompt="Shot 1 opening")
        )
        shot2 = service.generate_veo_video_scene(
            VeoVideoGenerationRequest(director_prompt="Shot 2 climax")
        )
        score = service.generate_lyria_score(LyriaScoreGenerationRequest(scene_mood="epic"))
        reel = service.assemble_movie_reel(
            movie_title="Baahubali 3: The Immortal Crown",
            veo_shots=[shot1, shot2],
            lyria_score=score,
        )
        assert reel.movie_title == "Baahubali 3: The Immortal Crown"
        assert reel.total_scenes == 2
        assert reel.total_duration_minutes > 0.0
        assert reel.dci_dcp_package_ready is True
        assert "baahubali-3-the-immortal-crown" in reel.ott_multi_bitrate_hls_url


class TestMultimodalCinemaEndpoints:
    """Validates FastAPI HTTP endpoints for multimodal cinema pipeline."""

    def test_api_multimodal_analyze(self) -> None:
        """Tests POST /api/cinema/multimodal/analyze endpoint."""
        payload = {
            "scene_id": "SCENE-API-01",
            "script_prompt": "Neon hovercraft speeding through rainy skyline.",
            "visual_reference_b64": "dummy-visual-base64",
            "acoustic_reference_b64": "dummy-acoustic-base64",
            "culture": "hollywood_tentpole",
            "genre_track": "action_stunts",
        }
        resp = client.post("/api/cinema/multimodal/analyze", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["scene_id"] == "SCENE-API-01"
        assert data["multimodal_status"] == "INGESTED_AND_VERIFIED"

    def test_api_veo_generate_scene(self) -> None:
        """Tests POST /api/cinema/veo/generate-scene endpoint."""
        payload = {
            "director_prompt": "Samurai drawn sword duel in snowstorm",
            "genre_track": "martial_arts_wuxia",
            "camera_movement": "orbital_pan",
            "resolution": "8K",
        }
        resp = client.post("/api/cinema/veo/generate-scene", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "VEO-SHOT-" in data["shot_id"]
        assert "orbital_pan" in data["expanded_veo_prompt"]

    def test_api_lyria_generate_score(self) -> None:
        """Tests POST /api/cinema/lyria/generate-score endpoint."""
        payload = {
            "scene_mood": "ominous",
            "musical_scale": "Phrygian_Dominant",
            "tempo_bpm": 110,
        }
        resp = client.post("/api/cinema/lyria/generate-score", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "LYRIA-TRK-" in data["track_id"]
        assert data["dolby_atmos_bed_active"] is True

    def test_api_assemble_reel(self) -> None:
        """Tests POST /api/cinema/assemble-reel endpoint."""
        payload = {
            "movie_title": "Dune: Prophecy of Arrakis",
            "veo_shots": [
                {
                    "shot_id": "VEO-SHOT-001",
                    "expanded_veo_prompt": "Sandworm emerges at sunrise",
                    "camera_metadata": {"duration_seconds": 15.0},
                    "video_stream_url": "https://storage.googleapis.com/test.mp4",
                    "render_status": "COMPLETED",
                }
            ],
            "lyria_score": {
                "track_id": "LYRIA-TRK-001",
                "musical_theme": "Desert choir and overtone flute",
                "audio_stream_url": "https://storage.googleapis.com/test.flac",
            },
        }
        resp = client.post("/api/cinema/assemble-reel", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["movie_title"] == "Dune: Prophecy of Arrakis"
        assert data["total_scenes"] == 1
        assert data["dci_dcp_package_ready"] is True
