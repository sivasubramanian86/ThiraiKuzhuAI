"""Department subagents for Thirai Kuzhu AI Screen Crew."""

from src.agents.subagents.animation import AnimationSakugaOpsSubAgent
from src.agents.subagents.audio import AudioOpsSubAgent
from src.agents.subagents.base import BaseSubAgent
from src.agents.subagents.cinematographer import CinematographerLensSubAgent
from src.agents.subagents.copyright_legal import CopyrightLegalOpsSubAgent
from src.agents.subagents.dialogue_writer import DialogueWriterOpsSubAgent
from src.agents.subagents.director import DirectorOpsSubAgent
from src.agents.subagents.film_editor import FilmEditorOpsSubAgent
from src.agents.subagents.martial_arts import MartialArtsOpsSubAgent
from src.agents.subagents.ott import OTTOpsSubAgent
from src.agents.subagents.producer import ProducerOpsSubAgent
from src.agents.subagents.screenplay import ScreenplayOpsSubAgent
from src.agents.subagents.story_writer import StoryWriterOpsSubAgent
from src.agents.subagents.vfx import VFXOpsSubAgent

__all__ = [
    "AnimationSakugaOpsSubAgent",
    "AudioOpsSubAgent",
    "BaseSubAgent",
    "CinematographerLensSubAgent",
    "CopyrightLegalOpsSubAgent",
    "DialogueWriterOpsSubAgent",
    "DirectorOpsSubAgent",
    "FilmEditorOpsSubAgent",
    "MartialArtsOpsSubAgent",
    "OTTOpsSubAgent",
    "ProducerOpsSubAgent",
    "ScreenplayOpsSubAgent",
    "StoryWriterOpsSubAgent",
    "VFXOpsSubAgent",
]
