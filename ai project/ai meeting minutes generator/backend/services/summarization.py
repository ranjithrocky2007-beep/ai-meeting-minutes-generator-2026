
"""
summarization.py

Text summarization module for AI Meeting Minutes Generator.

This module:
- Cleans the transcript
- Creates a concise summary
- Extracts important points
- Detects possible decisions
- Detects possible action items

This version works locally and does not require an API key.
"""

import re
from typing import Dict, List


# ---------------------------------------------------------
# Text Cleaning
# ---------------------------------------------------------

def clean_text(text: str) -> str:
    """
    Clean unnecessary spaces and characters from transcript.
    """

    if not text:
        return ""

    text = str(text)

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text


# ---------------------------------------------------------
# Split Text into Sentences
# ---------------------------------------------------------

def split_sentences(text: str) -> List[str]:
    """
    Split transcript into individual sentences.
    """

    text = clean_text(text)

    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


# ---------------------------------------------------------
# Generate Summary
# ---------------------------------------------------------

def generate_summary(
    transcript: str,
    max_sentences: int = 5
) -> str:
    """
    Generate a simple extractive summary.

    The most informative sentences are selected based on
    their length and important meeting-related keywords.
    """

    transcript = clean_text(transcript)

    if not transcript:
        return "No transcript available."

    sentences = split_sentences(transcript)

    if not sentences:
        return transcript

    if len(sentences) <= max_sentences:
        return " ".join(sentences)

    important_words = {
        "meeting",
        "project",
        "decision",
        "decided",
        "deadline",
        "task",
        "action",
        "update",
        "issue",
        "problem",
        "solution",
        "plan",
        "discuss",
        "discussed",
        "agree",
        "agreed",
        "complete",
        "completed",
        "future",
        "next",
        "requirement",
        "development",
    }

    scored_sentences = []

    for index, sentence in enumerate(sentences):

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            sentence.lower()
        )

        if not words:
            continue

        keyword_score = sum(
            1
            for word in words
            if word in important_words
        )

        length_score = min(
            len(words) / 20,
            1
        )

        score = keyword_score * 2 + length_score

        scored_sentences.append(
            (
                score,
                index,
                sentence
            )
        )

    # Select highest scoring sentences
    selected = sorted(
        scored_sentences,
        key=lambda item: item[0],
        reverse=True
    )[:max_sentences]

    # Restore original order
    selected = sorted(
        selected,
        key=lambda item: item[1]
    )

    return " ".join(
        item[2]
        for item in selected
    )


# ---------------------------------------------------------
# Extract Key Points
# ---------------------------------------------------------

def extract_key_points(
    transcript: str,
    max_points: int = 8
) -> List[str]:
    """
    Extract important sentences from the transcript.
    """

    transcript = clean_text(transcript)

    if not transcript:
        return []

    sentences = split_sentences(transcript)

    keywords = {
        "important",
        "project",
        "update",
        "issue",
        "problem",
        "solution",
        "plan",
        "decision",
        "deadline",
        "task",
        "action",
        "requirement",
        "development",
        "testing",
        "deployment",
        "budget",
        "schedule",
        "client",
        "customer",
    }

    scored = []

    for index, sentence in enumerate(sentences):

        words = sentence.lower().split()

        score = sum(
            1
            for word in words
            if any(
                keyword in word
                for keyword in keywords
            )
        )

        # Slight preference for useful-length sentences
        if len(words) >= 6:
            score += 1

        if score > 0:
            scored.append(
                (
                    score,
                    index,
                    sentence
                )
            )

    scored.sort(
        key=lambda item: (
            -item[0],
            item[1]
        )
    )

    selected = scored[:max_points]

    # Keep transcript order
    selected.sort(
        key=lambda item: item[1]
    )

    return [
        item[2]
        for item in selected
    ]


# ---------------------------------------------------------
# Extract Decisions
# ---------------------------------------------------------

def extract_decisions(
    transcript: str
) -> List[Dict[str, str]]:
    """
    Find sentences that appear to contain decisions.
    """

    sentences = split_sentences(transcript)

    decision_keywords = [
        "decided",
        "decision",
        "agreed",
        "we will",
        "we'll",
        "approved",
        "approve",
        "confirmed",
        "finalized",
        "chosen",
        "selected",
        "going to"
    ]

    decisions = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(
            keyword in sentence_lower
            for keyword in decision_keywords
        ):
            decisions.append(
                {
                    "decision": sentence
                }
            )

    return decisions


# ---------------------------------------------------------
# Extract Action Items
# ---------------------------------------------------------

def extract_action_items(
    transcript: str
) -> List[Dict[str, object]]:
    """
    Find sentences that appear to contain tasks or actions.
    """

    sentences = split_sentences(transcript)

    action_keywords = [
        "will",
        "need to",
        "needs to",
        "should",
        "must",
        "assign",
        "complete",
        "prepare",
        "send",
        "review",
        "update",
        "create",
        "develop",
        "test",
        "submit",
        "finish",
        "follow up"
    ]

    action_items = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(
            keyword in sentence_lower
            for keyword in action_keywords
        ):

            action_items.append(
                {
                    "title": sentence,
                    "assignee": "Unassigned",
                    "due_date": "Not specified",
                    "completed": False
                }
            )

    return action_items


# ---------------------------------------------------------
# Extract Participants
# ---------------------------------------------------------

def extract_participants(
    transcript: str
) -> List[str]:
    """
    Detect simple participant names from patterns such as:

        John: We should...
        Priya: I will...

    This is a basic text-based method.
    """

    participants = []

    for line in transcript.splitlines():

        match = re.match(
            r"^\s*([A-Za-z][A-Za-z .'-]{1,40}):",
            line
        )

        if match:

            name = match.group(1).strip()

            if name not in participants:
                participants.append(name)

    return participants


# ---------------------------------------------------------
# Remove Duplicate Items
# ---------------------------------------------------------

def remove_duplicates(
    items: List[str]
) -> List[str]:
    """
    Remove duplicate text items while preserving order.
    """

    result = []
    seen = set()

    for item in items:

        normalized = item.lower().strip()

        if normalized not in seen:

            seen.add(normalized)
            result.append(item)

    return result


# ---------------------------------------------------------
# Complete Summarization
# ---------------------------------------------------------

def summarize_meeting(
    transcript: str
) -> Dict[str, object]:
    """
    Generate complete meeting summarization.

    Returns:
        {
            "summary": "...",
            "key_points": [...],
            "decisions": [...],
            "action_items": [...],
            "participants": [...]
        }
    """

    transcript = clean_text(transcript)

    if not transcript:
        return {
            "summary": "No transcript available.",
            "key_points": [],
            "decisions": [],
            "action_items": [],
            "participants": []
        }

    summary = generate_summary(
        transcript
    )

    key_points = extract_key_points(
        transcript
    )

    decisions = extract_decisions(
        transcript
    )

    action_items = extract_action_items(
        transcript
    )

    participants = extract_participants(
        transcript
    )

    return {
        "summary": summary,
        "key_points": remove_duplicates(
            key_points
        ),
        "decisions": decisions,
        "action_items": action_items,
        "participants": participants
    }


# ---------------------------------------------------------
# Generate Plain Text Summary
# ---------------------------------------------------------

def generate_summary_text(
    transcript: str
) -> str:
    """
    Generate a readable meeting summary.
    """

    result = summarize_meeting(
        transcript
    )

    lines = []

    lines.append("MEETING SUMMARY")
    lines.append("=" * 50)

    lines.append("")
    lines.append("Summary:")
    lines.append(
        str(result["summary"])
    )

    lines.append("")
    lines.append("Key Points:")

    key_points = result["key_points"]

    if key_points:

        for point in key_points:
            lines.append(
                f"- {point}"
            )

    else:
        lines.append(
            "- No key points detected."
        )

    lines.append("")
    lines.append("Decisions:")

    decisions = result["decisions"]

    if decisions:

        for decision in decisions:
            lines.append(
                f"- {decision['decision']}"
            )

    else:
        lines.append(
            "- No decisions detected."
        )

    lines.append("")
    lines.append("Action Items:")

    action_items = result["action_items"]

    if action_items:

        for item in action_items:
            lines.append(
                f"- {item['title']}"
            )

    else:
        lines.append(
            "- No action items detected."
        )

    return "\n".join(lines)


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_transcript = """
    Good morning everyone. Today we discussed the new AI project.
    The frontend development is almost completed.
    Ranjith will complete the backend development next week.
    The team agreed to finish testing by Friday.
    We decided to deploy the application after testing.
    Priya will prepare the project documentation.
    """

    print("=" * 60)
    print("AI MEETING MINUTES GENERATOR")
    print("Summarization Module Test")
    print("=" * 60)

    result = summarize_meeting(
        sample_transcript
    )

    print("\nSUMMARY:")
    print(result["summary"])

    print("\nKEY POINTS:")

    for point in result["key_points"]:
        print(f"- {point}")

    print("\nDECISIONS:")

    for decision in result["decisions"]:
        print(
            f"- {decision['decision']}"
        )

    print("\nACTION ITEMS:")

    for item in result["action_items"]:
        print(
            f"- {item['title']}"
        )

    print("\nPARTICIPANTS:")

    for participant in result["participants"]:
        print(
            f"- {participant}"
        )

    print("\nTest completed successfully.")
