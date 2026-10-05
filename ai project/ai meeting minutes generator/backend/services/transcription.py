
"""
transcription.py

Audio/Video transcription module for
AI Meeting Minutes Generator.

Uses OpenAI Whisper for local speech-to-text conversion.
"""

from pathlib import Path
from typing import Any, Dict, List

import whisper


# =========================================================
# Configuration
# =========================================================

WHISPER_MODEL_NAME = "base"

SUPPORTED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".webm",
    ".mpeg",
}


# =========================================================
# Load Whisper Model
# =========================================================

print("Loading Whisper model...")

try:
    model = whisper.load_model(WHISPER_MODEL_NAME)
    print("Whisper model loaded successfully!")

except Exception as exc:
    print("ERROR: Whisper model could not be loaded.")
    print(f"Details: {exc}")
    model = None


# =========================================================
# Validate File
# =========================================================

def validate_file(file_path: str) -> Path:
    """
    Validate the uploaded audio/video file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Audio/video file not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Specified path is not a file: {file_path}"
        )

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {path.suffix}"
        )

    return path


# =========================================================
# Transcribe Audio
# =========================================================

def transcribe_audio(
    file_path: str,
    language: str | None = None
) -> str:
    """
    Transcribe an audio/video file.

    Parameters
    ----------
    file_path:
        Path to the audio/video file.

    language:
        Optional language code such as:
        "en" for English
        "ta" for Tamil
        "hi" for Hindi

        If None, Whisper automatically detects the language.

    Returns
    -------
    str
        Full transcript.
    """

    path = validate_file(file_path)

    if model is None:
        raise RuntimeError(
            "Whisper model is not available. "
            "Please check your Whisper installation."
        )

    print(
        f"Starting transcription: {path.name}"
    )

    try:

        options: Dict[str, Any] = {
            "fp16": False,
            "verbose": False,
        }

        if language:
            options["language"] = language

        result = model.transcribe(
            str(path),
            **options
        )

        transcript = result.get(
            "text",
            ""
        ).strip()

        if not transcript:
            raise ValueError(
                "No speech was detected in the uploaded file."
            )

        print(
            "Transcription completed successfully."
        )

        return transcript

    except Exception as exc:

        print(
            f"Transcription failed: {exc}"
        )

        raise RuntimeError(
            f"Unable to transcribe the file: {exc}"
        ) from exc


# =========================================================
# Transcribe With Timestamps
# =========================================================

def transcribe_with_timestamps(
    file_path: str,
    language: str | None = None
) -> List[Dict[str, Any]]:
    """
    Transcribe audio/video and return timestamped segments.

    Example output:

    [
        {
            "start": 0.0,
            "end": 4.5,
            "text": "Good morning everyone."
        }
    ]
    """

    path = validate_file(file_path)

    if model is None:
        raise RuntimeError(
            "Whisper model is not available."
        )

    try:

        options: Dict[str, Any] = {
            "fp16": False,
            "verbose": False,
        }

        if language:
            options["language"] = language

        result = model.transcribe(
            str(path),
            **options
        )

        segments = result.get(
            "segments",
            []
        )

        formatted_segments = []

        for segment in segments:

            text = str(
                segment.get("text", "")
            ).strip()

            if not text:
                continue

            formatted_segments.append(
                {
                    "start": round(
                        float(
                            segment.get(
                                "start",
                                0.0
                            )
                        ),
                        2
                    ),
                    "end": round(
                        float(
                            segment.get(
                                "end",
                                0.0
                            )
                        ),
                        2
                    ),
                    "text": text,
                }
            )

        return formatted_segments

    except Exception as exc:

        raise RuntimeError(
            f"Timestamped transcription failed: {exc}"
        ) from exc


# =========================================================
# Get Full Transcription Result
# =========================================================

def get_transcription_result(
    file_path: str,
    language: str | None = None
) -> Dict[str, Any]:
    """
    Return the complete Whisper transcription result.

    Includes:
    - detected language
    - complete transcript
    - timestamped segments
    """

    path = validate_file(file_path)

    if model is None:
        raise RuntimeError(
            "Whisper model is not available."
        )

    try:

        options: Dict[str, Any] = {
            "fp16": False,
            "verbose": False,
        }

        if language:
            options["language"] = language

        result = model.transcribe(
            str(path),
            **options
        )

        transcript = result.get(
            "text",
            ""
        ).strip()

        if not transcript:
            raise ValueError(
                "No speech was detected."
            )

        segments = []

        for segment in result.get(
            "segments",
            []
        ):

            text = str(
                segment.get("text", "")
            ).strip()

            if not text:
                continue

            segments.append(
                {
                    "start": round(
                        float(
                            segment.get(
                                "start",
                                0.0
                            )
                        ),
                        2
                    ),
                    "end": round(
                        float(
                            segment.get(
                                "end",
                                0.0
                            )
                        ),
                        2
                    ),
                    "text": text,
                }
            )

        return {
            "filename": path.name,
            "language": result.get(
                "language",
                "unknown"
            ),
            "text": transcript,
            "segments": segments,
        }

    except Exception as exc:

        raise RuntimeError(
            f"Transcription failed: {exc}"
        ) from exc


# =========================================================
# Save Transcript
# =========================================================

def save_transcript(
    transcript: str,
    output_file: str
) -> str:
    """
    Save transcript to a text file.
    """

    if not transcript:
        raise ValueError(
            "Transcript is empty."
        )

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        transcript,
        encoding="utf-8"
    )

    return str(output_path)


# =========================================================
# Test
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("AI MEETING MINUTES GENERATOR")
    print("Transcription Module")
    print("=" * 60)

    print()
    print("Whisper transcription module is ready.")

    print()
    print("Example:")
    print(
        'text = transcribe_audio("uploads/meeting.mp3")'
    )
    print(
        'print(text)'
    )

    print()
    print("For Tamil audio:")
    print(
        'text = transcribe_audio("uploads/meeting.mp3", language="ta")'
    )
