"""
AI Meeting Minutes Generator
Meeting Minutes Export Utilities

Supported formats:
- TXT
- JSON
- HTML
"""

import json
import html
from pathlib import Path
from datetime import datetime
from typing import Any, Dict


# ============================================================
# EXPORT DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "exports"

EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# SAFE FILE NAME
# ============================================================

def create_safe_filename(filename: str) -> str:
    """
    Create a safe filename for exported files.
    """

    filename = Path(filename).stem

    allowed_characters = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        "_-"
    )

    safe_name = "".join(
        character
        if character in allowed_characters
        else "_"
        for character in filename
    )

    return safe_name.strip("_") or "meeting"


# ============================================================
# EXPORT AS TXT
# ============================================================

def export_txt(
    filename: str,
    transcript: str = "",
    minutes: Any = ""
) -> str:
    """
    Export meeting minutes as a TXT file.

    Returns:
        str: Path of the generated file
    """

    safe_name = create_safe_filename(filename)

    output_file = EXPORT_DIR / f"{safe_name}_minutes.txt"

    if isinstance(minutes, dict):
        minutes_text = json.dumps(
            minutes,
            indent=4,
            ensure_ascii=False
        )
    elif isinstance(minutes, list):
        minutes_text = json.dumps(
            minutes,
            indent=4,
            ensure_ascii=False
        )
    else:
        minutes_text = str(minutes)

    content = f"""
AI MEETING MINUTES
==================

Meeting File:
{filename}

Generated:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


MEETING MINUTES
---------------

{minutes_text}


TRANSCRIPT
----------

{transcript}
"""

    output_file.write_text(
        content.strip(),
        encoding="utf-8"
    )

    return str(output_file)


# ============================================================
# EXPORT AS JSON
# ============================================================

def export_json(
    filename: str,
    transcript: str = "",
    minutes: Any = ""
) -> str:
    """
    Export meeting information as JSON.

    Returns:
        str: Path of the generated file
    """

    safe_name = create_safe_filename(filename)

    output_file = EXPORT_DIR / f"{safe_name}_minutes.json"

    meeting_data: Dict[str, Any] = {
        "application": "AI Meeting Minutes Generator",

        "filename": filename,

        "generated_at":
            datetime.now().isoformat(),

        "transcript": transcript,

        "minutes": minutes
    }

    output_file.write_text(
        json.dumps(
            meeting_data,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    return str(output_file)


# ============================================================
# EXPORT AS HTML
# ============================================================

def export_html(
    filename: str,
    transcript: str = "",
    minutes: Any = ""
) -> str:
    """
    Export meeting minutes as an HTML document.

    Returns:
        str: Path of the generated file
    """

    safe_name = create_safe_filename(filename)

    output_file = EXPORT_DIR / f"{safe_name}_minutes.html"

    if isinstance(minutes, (dict, list)):
        minutes_text = json.dumps(
            minutes,
            indent=4,
            ensure_ascii=False
        )
    else:
        minutes_text = str(minutes)

    safe_filename = html.escape(filename)
    safe_minutes = html.escape(minutes_text)
    safe_transcript = html.escape(transcript)

    html_content = f"""
<!DOCTYPE html>

<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>AI Meeting Minutes</title>

    <style>

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 40px;
            font-family:
                Arial,
                Helvetica,
                sans-serif;
            background: #f4f7fb;
            color: #1f2937;
        }}

        .container {{
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 40px;
            border-radius: 18px;
            box-shadow:
                0 10px 30px
                rgba(0, 0, 0, 0.08);
        }}

        .header {{
            text-align: center;
            margin-bottom: 35px;
        }}

        .header h1 {{
            margin-bottom: 10px;
            font-size: 32px;
        }}

        .header p {{
            color: #6b7280;
        }}

        .section {{
            margin-top: 30px;
        }}

        .section h2 {{
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
        }}

        .content {{
            white-space: pre-wrap;
            line-height: 1.7;
        }}

        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            text-align: center;
            color: #6b7280;
            font-size: 14px;
        }}

    </style>

</head>

<body>

<div class="container">

    <div class="header">

        <h1>AI Meeting Minutes</h1>

        <p>
            AI Meeting Minutes Generator
        </p>

        <p>
            Meeting File:
            <strong>{safe_filename}</strong>
        </p>

        <p>
            Generated:
            {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </p>

    </div>


    <div class="section">

        <h2>Meeting Minutes</h2>

        <div class="content">
            {safe_minutes}
        </div>

    </div>


    <div class="section">

        <h2>Transcript</h2>

        <div class="content">
            {safe_transcript}
        </div>

    </div>


    <div class="footer">

        Generated by
        <strong>AI Meeting Minutes Generator</strong>

    </div>

</div>

</body>

</html>
"""

    output_file.write_text(
        html_content,
        encoding="utf-8"
    )

    return str(output_file)


# ============================================================
# EXPORT ALL FORMATS
# ============================================================

def export_all(
    filename: str,
    transcript: str = "",
    minutes: Any = ""
) -> Dict[str, str]:
    """
    Export meeting minutes in all supported formats.

    Returns:
        Dictionary containing generated file paths.
    """

    txt_file = export_txt(
        filename,
        transcript,
        minutes
    )

    json_file = export_json(
        filename,
        transcript,
        minutes
    )

    html_file = export_html(
        filename,
        transcript,
        minutes
    )

    return {
        "txt": txt_file,
        "json": json_file,
        "html": html_file
    }


# ============================================================
# TEST EXPORT
# ============================================================

if __name__ == "__main__":

    sample_filename = "sample_meeting.mp3"

    sample_transcript = (
        "The team discussed the project "
        "timeline and upcoming tasks."
    )

    sample_minutes = {
        "summary":
            "The team reviewed the project timeline.",

        "key_points": [
            "Project timeline reviewed",
            "Upcoming tasks discussed",
            "Responsibilities assigned"
        ],

        "decisions": [
            "The next review meeting will be scheduled."
        ],

        "action_items": [
            {
                "title":
                    "Prepare the project progress report",
                "assignee":
                    "Project Team",
                "due_date":
                    "Next Meeting"
            }
        ]
    }

    exported_files = export_all(
        sample_filename,
        sample_transcript,
        sample_minutes
    )

    print("\nExport completed successfully!\n")

    for file_type, file_path in exported_files.items():

        print(
            f"{file_type.upper():5} : {file_path}"
        )