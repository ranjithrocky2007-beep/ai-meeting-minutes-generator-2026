
"""
speaker_detection.py

Speaker-turn detection for AI Meeting Minutes Generator.

Important:
Whisper provides speech transcription and timestamps, but it does
not identify individual people by voice.

This module therefore detects approximate speaker turns based on
pauses between speech segments and labels them as:

Speaker 1
Speaker 2
Speaker 3
...

For true voice-based speaker diarization, a dedicated diarization
model can be integrated later.
"""

from pathlib import Path
from typing import Any, Dict, List

import whisper


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

WHISPER_MODEL_NAME = "base"

# A pause longer than this is treated as a possible speaker turn.
SPEAKER_CHANGE_PAUSE = 1.5


# ---------------------------------------------------------
# Load Whisper model
# ---------------------------------------------------------

print("Loading Whisper model for speaker detection...")

model = whisper.load_model(WHISPER_MODEL_NAME)

print("Whisper model loaded successfully!")


# ---------------------------------------------------------
# Validate input file
# ---------------------------------------------------------

def validate_audio_file(file_path: str) -> Path:
    """
    Validate that the input audio/video file exists.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Audio/video file not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"The specified path is not a file: {file_path}"
        )

    return path


# ---------------------------------------------------------
# Detect speaker turns
# ---------------------------------------------------------

def detect_speakers(
    file_path: str,
    pause_threshold: float = SPEAKER_CHANGE_PAUSE
) -> List[Dict[str, Any]]:
    """
    Detect approximate speaker turns.

    Parameters
    ----------
    file_path:
        Path to the meeting audio/video file.

    pause_threshold:
        Minimum pause duration in seconds used to estimate
        a speaker change.

    Returns
    -------
    List[dict]
        Speaker-labelled transcript segments.

    Example
    -------
    [
        {
            "speaker": "Speaker 1",
            "start": 0.0,
            "end": 5.2,
            "text": "Good morning everyone."
        },
        {
            "speaker": "Speaker 2",
            "start": 7.1,
            "end": 12.4,
            "text": "Good morning. Let's begin."
        }
    ]
    """

    path = validate_audio_file(file_path)

    if pause_threshold < 0:
        raise ValueError(
            "pause_threshold cannot be negative."
        )

    print(f"Analyzing meeting: {path.name}")

    try:
        result = model.transcribe(
            str(path),
            fp16=False,
            verbose=False
        )
    except Exception as exc:
        raise RuntimeError(
            f"Whisper transcription failed: {exc}"
        ) from exc

    segments = result.get("segments", [])

    if not segments:
        raise ValueError(
            "No speech was detected in the uploaded file."
        )

    speaker_segments: List[Dict[str, Any]] = []

    speaker_number = 1
    previous_end = None

    for segment in segments:

        text = str(
            segment.get("text", "")
        ).strip()

        if not text:
            continue

        start = float(
            segment.get("start", 0.0)
        )

        end = float(
            segment.get("end", start)
        )

        # Detect a possible speaker change.
        if previous_end is not None:

            pause_duration = start - previous_end

            if pause_duration >= pause_threshold:
                speaker_number += 1

        speaker_segments.append(
            {
                "speaker": f"Speaker {speaker_number}",
                "start": round(start, 2),
                "end": round(end, 2),
                "text": text
            }
        )

        previous_end = end

    if not speaker_segments:
        raise ValueError(
            "No usable speech segments were found."
        )

    print(
        f"Speaker-turn detection completed: "
        f"{len(speaker_segments)} segments."
    )

    return speaker_segments


# ---------------------------------------------------------
# Create readable speaker transcript
# ---------------------------------------------------------

def create_speaker_transcript(
    speaker_segments: List[Dict[str, Any]]
) -> str:
    """
    Convert speaker segments into a readable transcript.

    Example:

    Speaker 1: Good morning everyone.
    Speaker 2: Good morning.
    """

    if not speaker_segments:
        return ""

    lines = []

    for segment in speaker_segments:

        speaker = segment.get(
            "speaker",
            "Speaker 1"
        )

        text = str(
            segment.get("text", "")
        ).strip()

        if text:
            lines.append(
                f"{speaker}: {text}"
            )

    return "\n".join(lines)


# ---------------------------------------------------------
# Get unique speakers
# ---------------------------------------------------------

def get_speakers(
    speaker_segments: List[Dict[str, Any]]
) -> List[str]:
    """
    Return the speaker labels found in the transcript.
    """

    speakers = []

    for segment in speaker_segments:

        speaker = segment.get("speaker")

        if speaker and speaker not in speakers:
            speakers.append(speaker)

    return speakers


# ---------------------------------------------------------
# Speaker statistics
# ---------------------------------------------------------

def get_speaker_statistics(
    speaker_segments: List[Dict[str, Any]]
) -> Dict[str, Dict[str, Any]]:
    """
    Calculate basic statistics for each detected speaker.

    Returns:

    {
        "Speaker 1": {
            "segments": 3,
            "words": 45,
            "duration": 18.5
        }
    }
    """

    statistics: Dict[str, Dict[str, Any]] = {}

    for segment in speaker_segments:

        speaker = segment.get(
            "speaker",
            "Unknown"
        )

        text = str(
            segment.get("text", "")
        ).strip()

        start = float(
            segment.get("start", 0.0)
        )

        end = float(
            segment.get("end", start)
        )

        if speaker not in statistics:

            statistics[speaker] = {
                "segments": 0,
                "words": 0,
                "duration": 0.0
            }

        statistics[speaker]["segments"] += 1

        statistics[speaker]["words"] += len(
            text.split()
        )

        statistics[speaker]["duration"] += max(
            0.0,
            end - start
        )

    for speaker in statistics:

        statistics[speaker]["duration"] = round(
            statistics[speaker]["duration"],
            2
        )

    return statistics


# ---------------------------------------------------------
# Complete speaker analysis
# ---------------------------------------------------------

def analyze_speakers(
    file_path: str,
    pause_threshold: float = SPEAKER_CHANGE_PAUSE
) -> Dict[str, Any]:
    """
    Perform complete speaker-turn analysis.

    Returns:

    {
        "speakers": [...],
        "speaker_count": 2,
        "segments": [...],
        "transcript": "...",
        "statistics": {...}
    }
    """

    segments = detect_speakers(
        file_path,
        pause_threshold
    )

    speakers = get_speakers(
        segments
    )

    transcript = create_speaker_transcript(
        segments
    )

    statistics = get_speaker_statistics(
        segments
    )

    return {
        "speakers": speakers,
        "speaker_count": len(speakers),
        "segments": segments,
        "transcript": transcript,
        "statistics": statistics
    }


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("AI Meeting Minutes Generator")
    print("Speaker Detection Module")
    print("=" * 55)

    print()
    print("Module loaded successfully.")
    print()
    print("Example:")
    print(
        'result = analyze_speakers("uploads/meeting.mp3")'
    )
    print()
    print(
        'print(result["transcript"])'
    )