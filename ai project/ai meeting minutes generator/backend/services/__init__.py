"""
Services package for AI Meeting Minutes Generator.

This package contains modules for:
- Audio transcription
- Speaker detection
- Meeting minutes generation
"""

from .transcription import transcribe_audio
from .minutes_generator import generate_minutes
from .speaker_detection import (
    detect_speakers,
    create_speaker_transcript,
    get_speaker_statistics,
    analyze_speakers
)

__all__ = [
    "transcribe_audio",
    "generate_minutes",
    "detect_speakers",
    "create_speaker_transcript",
    "get_speaker_statistics",
    "analyze_speakers"
]