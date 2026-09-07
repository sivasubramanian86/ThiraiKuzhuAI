"""Screenplay & Narrative Story Architecture Service for Thirai Kuzhu AI.

Provides StoryWriterOps, ScreenplayOps, and DialogueWriterOps pipelines
for autonomous blockbuster movie development and on-set scene breakdown.

Follows PEP 257 Google-style docstrings, type hints, and Pydantic v2 validation.
"""

from typing import Any

from src.models.governance import (
    ScreenplaySceneRequest,
    ScreenplaySceneResult,
    StoryPremiseRequest,
    StoryPremiseResult,
)


class ScreenplayService:
    """Narrative architecture and screenplay generation service."""

    def generate_story_premise(self, request: StoryPremiseRequest) -> StoryPremiseResult:
        """Generates a comprehensive three-act narrative premise and character archetypes.

        Args:
            request: StoryPremiseRequest specifying theme, genre, and culture.

        Returns:
            StoryPremiseResult: Complete narrative blueprint with acts and character motivations.
        """
        title = f"The Chronicle of {request.core_theme.split()[0]} ({request.genre_track.upper()})"
        logline = (
            f"In a torn world, a visionary champion must master {request.core_theme} "
            "before the dawn of an unstoppable cataclysm."
        )

        acts = {
            "Act_1_Departure": (
                f"Ordinary world disrupted. Protagonist uncovers covenant on {request.core_theme}. "
                "Inciting incident triggers refusal of the call and crossing of threshold."
            ),
            "Act_2_Initiation": (
                "Midpoint crisis. The antagonist captures the royal stronghold; all feeds fail. "
                "The hero experiences symbolic death and claims the elixir of truth."
            ),
            "Act_3_Return": (
                "Climax confrontation at the high mountain pass. Sacred principles tested. "
                "Cathartic sacrifice leads to resurrection and enduring peace."
            ),
        }

        characters = [
            {
                "role": "Protagonist",
                "archetype": "The Reluctant Sovereign",
                "trait": "Relentless determination",
            },
            {
                "role": "Antagonist",
                "archetype": "The Tyrant of Order",
                "trait": "Ruthless technological hegemony",
            },
            {
                "role": "Mentor",
                "archetype": "The Ancient Keeper of Dharma",
                "trait": "Deep mythic wisdom",
            },
            {
                "role": "Shadow Companion",
                "archetype": "The Cyber Trickster",
                "trait": "Unpredictable loyalty",
            },
        ]

        motifs = [
            request.core_theme,
            "Sacred geometry and temple bells",
            "Solar eclipse at midnight",
            "Honor above survival",
        ]

        return StoryPremiseResult(
            title=title,
            logline=logline,
            three_act_structure=acts,
            lead_characters=characters,
            mythic_motifs=motifs,
        )

    def format_screenplay_scene(self, request: ScreenplaySceneRequest) -> ScreenplaySceneResult:
        """Formats visual scene sluglines, action blocks, and localized dialogue lines.

        Args:
            request: ScreenplaySceneRequest containing scene heading and dramatic intent.

        Returns:
            ScreenplaySceneResult: Standardized screenplay layout with dialogue and camera cues.
        """
        slugline = request.scene_heading.upper()
        chars = request.characters_present or ["CHAMPION", "SHADOW"]

        action = (
            f"{request.action_description.strip()} "
            "Dust motes dance in single beam of moonlight slicing through obsidian stone arches. "
            "Tension hangs thick in the air. Neither moves."
        )

        dialogues = []
        if len(chars) >= 2:
            d1_en = "Throne was not won with cowardice. Look upon scars of your ancestors."
            d1_ta = "இந்த சிம்மாசனம் கோழைத்தனத்தால் பெற்றதல்ல. உன் முன்னோர்களின் தழும்புகளைப் பார்!"
            d2_en = "Ancestors belong to dust. Dawn belongs to those who forge the future."
            d2_ta = "முன்னோர்கள் சாம்பலுக்குரியவர்கள்! இந்த விடியல் எதிர்காலத்தை உருவாக்குவோருக்கு மட்டுமே!"

            dialogues.append(
                {
                    "character": chars[0].upper(),
                    "parenthetical": "(steely resolve, holding blade level)",
                    "dialogue": d1_en if request.language == "en" else d1_ta,
                }
            )
            dialogues.append(
                {
                    "character": chars[1].upper(),
                    "parenthetical": "(a chilling whisper, stepping from shadow)",
                    "dialogue": d2_en if request.language == "en" else d2_ta,
                }
            )
        else:
            dialogues.append(
                {
                    "character": chars[0].upper(),
                    "parenthetical": "(whispering to the storm)",
                    "dialogue": "Fate knocked upon the door, and I answered without trembling.",
                }
            )

        return ScreenplaySceneResult(
            scene_heading=slugline,
            action_block=action,
            dialogue_blocks=dialogues,
            scene_pacing_tempo="ALLEGRO",
            camera_shot_suggestion="50mm Anamorphic T2.0 Prime, Slow Dolly In on Champion's Eyes",
        )

    def generate_shot_list(self, scene_id: str, shot_count: int = 4) -> list[dict[str, Any]]:
        """Generates director's cut shot list with focal lengths, camera moves, and lighting cues.

        Args:
            scene_id: Identifier of target scene.
            shot_count: Number of shots in the sequence.

        Returns:
            list[dict[str, Any]]: Detailed shot specifications.
        """
        shots = []
        shot_types = [
            "Extreme Wide Establishing",
            "Medium Over-the-Shoulder",
            "Dutch Angle Close-up",
            "Macro Hero Shot",
        ]
        moves = ["Technocrane Arc", "Steadicam Push-In", "Static Locked-Off", "Whip Pan"]
        lenses = [
            "24mm Ultra-Wide",
            "35mm Anamorphic",
            "50mm High-Speed Prime",
            "85mm Portrait Telephoto",
        ]

        for i in range(min(shot_count, 4)):
            shots.append(
                {
                    "shot_id": f"{scene_id}_S{i + 1:02d}",
                    "framing": shot_types[i % len(shot_types)],
                    "lens": lenses[i % len(lenses)],
                    "camera_movement": moves[i % len(moves)],
                    "lighting_setup": "Chiaroscuro rim light with 4:1 key-to-fill ratio",
                    "estimated_duration_seconds": 4.5,
                }
            )

        return shots
