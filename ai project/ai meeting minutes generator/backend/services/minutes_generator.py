"""
AI Meeting Minutes Generator
Minutes Generation Service

Input:
    Meeting transcript

Output:
    Structured meeting minutes
"""

import re
from typing import Dict, List, Any


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_transcript(transcript: str) -> str:
    """
    Clean and normalize the transcript.
    """

    if not transcript:
        return ""

    transcript = transcript.strip()

    transcript = re.sub(
        r"\s+",
        " ",
        transcript
    )

    return transcript


# ============================================================
# SPLIT INTO SENTENCES
# ============================================================

def split_sentences(text: str) -> List[str]:
    """
    Split transcript into simple sentences.
    """

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


# ============================================================
# GENERATE SUMMARY
# ============================================================

def generate_summary(
    transcript: str,
    max_sentences: int = 5
) -> str:
    """
    Generate a simple summary from the transcript.

    The most useful first sentences are selected.
    """

    sentences = split_sentences(transcript)

    if not sentences:
        return "No meeting summary available."

    selected = sentences[:max_sentences]

    return " ".join(selected)


# ============================================================
# EXTRACT KEY POINTS
# ============================================================

def extract_key_points(
    transcript: str,
    max_points: int = 8
) -> List[str]:
    """
    Extract important sentences as key points.
    """

    sentences = split_sentences(transcript)

    if not sentences:
        return []

    keywords = [
        "discuss",
        "discussed",
        "important",
        "project",
        "plan",
        "planning",
        "update",
        "deadline",
        "budget",
        "schedule",
        "problem",
        "issue",
        "goal",
        "target",
        "review",
        "development",
        "decision"
    ]

    scored_sentences = []

    for index, sentence in enumerate(sentences):

        sentence_lower = sentence.lower()

        score = 0

        for keyword in keywords:

            if keyword in sentence_lower:
                score += 1

        # Slightly prefer earlier sentences
        position_score = max(
            0,
            5 - index
        )

        score += position_score * 0.1

        scored_sentences.append(
            (
                score,
                index,
                sentence
            )
        )

    scored_sentences.sort(
        key=lambda item: (
            -item[0],
            item[1]
        )
    )

    selected = scored_sentences[:max_points]

    # Restore original transcript order
    selected.sort(
        key=lambda item: item[1]
    )

    return [
        item[2]
        for item in selected
    ]


# ============================================================
# EXTRACT DECISIONS
# ============================================================

def extract_decisions(
    transcript: str
) -> List[str]:
    """
    Extract sentences that appear to contain decisions.
    """

    sentences = split_sentences(transcript)

    decision_keywords = [
        "decided",
        "decision",
        "agreed",
        "approved",
        "we will",
        "will proceed",
        "finalized",
        "confirmed",
        "accepted",
        "agreed to"
    ]

    decisions = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(
            keyword in sentence_lower
            for keyword in decision_keywords
        ):
            decisions.append(sentence)

    return unique_items(decisions)


# ============================================================
# EXTRACT ACTION ITEMS
# ============================================================

def extract_action_items(
    transcript: str
) -> List[Dict[str, Any]]:
    """
    Extract sentences that appear to contain
    action items.
    """

    sentences = split_sentences(transcript)

    action_keywords = [
        "action",
        "task",
        "todo",
        "to-do",
        "need to",
        "needs to",
        "should",
        "must",
        "will",
        "prepare",
        "complete",
        "send",
        "review",
        "create",
        "update",
        "finish",
        "submit"
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
                    "assignee": extract_assignee(sentence),
                    "due_date": extract_due_date(sentence),
                    "completed": False
                }
            )

    return action_items


# ============================================================
# EXTRACT ASSIGNEE
# ============================================================

def extract_assignee(
    sentence: str
) -> str:
    """
    Try to identify a person responsible
    for an action item.
    """

    patterns = [
        r"([A-Z][a-z]+)\s+will\s+",
        r"([A-Z][a-z]+)\s+should\s+",
        r"([A-Z][a-z]+)\s+must\s+",
        r"([A-Z][a-z]+)\s+needs\s+to\s+"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            sentence
        )

        if match:
            return match.group(1)

    return ""


# ============================================================
# EXTRACT DUE DATE
# ============================================================

def extract_due_date(
    sentence: str
) -> str:
    """
    Try to identify a due date or deadline.
    """

    patterns = [
        r"by\s+([A-Za-z0-9 ,/-]+)",
        r"before\s+([A-Za-z0-9 ,/-]+)",
        r"on\s+([A-Za-z0-9 ,/-]+)",
        r"deadline\s*(?:is|:)?\s*([A-Za-z0-9 ,/-]+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            sentence,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            if len(value) <= 40:
                return value

    return ""


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def unique_items(
    items: List[str]
) -> List[str]:
    """
    Remove duplicate strings.
    """

    result = []

    seen = set()

    for item in items:

        normalized = item.lower().strip()

        if normalized not in seen:

            seen.add(normalized)

            result.append(item)

    return result


# ============================================================
# GENERATE STRUCTURED MINUTES
# ============================================================

def generate_structured_minutes(
    transcript: str
) -> Dict[str, Any]:
    """
    Generate structured meeting minutes.
    """

    transcript = clean_transcript(
        transcript
    )

    if not transcript:

        return {
            "title": "Meeting Minutes",
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

    return {
        "title": "AI Generated Meeting Minutes",

        "summary": summary,

        "key_points": key_points,

        "decisions": [
            {
                "decision": decision
            }
            for decision in decisions
        ],

        "action_items": action_items,

        "participants": []
    }


# ============================================================
# GENERATE MINUTES
# ============================================================

def generate_minutes(
    transcript: str
) -> Dict[str, Any]:
    """
    Main function used by main.py.

    Args:
        transcript: Meeting transcript

    Returns:
        Structured meeting minutes dictionary
    """

    if not transcript:
        raise ValueError(
            "Transcript cannot be empty."
        )

    return generate_structured_minutes(
        transcript
    )


# ============================================================
# TEXT FORMAT
# ============================================================

def generate_minutes_text(
    transcript: str
) -> str:
    """
    Convert structured minutes into
    readable plain text.
    """

    minutes = generate_minutes(
        transcript
    )

    output = []

    output.append(
        "AI GENERATED MEETING MINUTES"
    )

    output.append(
        "=" * 35
    )

    output.append("")

    # Summary
    output.append("SUMMARY")
    output.append("-" * 20)
    output.append(
        minutes["summary"]
    )

    output.append("")

    # Key points
    output.append("KEY POINTS")
    output.append("-" * 20)

    if minutes["key_points"]:

        for point in minutes["key_points"]:

            output.append(
                f"• {point}"
            )

    else:

        output.append(
            "No key points identified."
        )

    output.append("")

    # Decisions
    output.append("DECISIONS")
    output.append("-" * 20)

    if minutes["decisions"]:

        for item in minutes["decisions"]:

            output.append(
                f"• {item['decision']}"
            )

    else:

        output.append(
            "No decisions identified."
        )

    output.append("")

    # Action items
    output.append("ACTION ITEMS")
    output.append("-" * 20)

    if minutes["action_items"]:

        for item in minutes["action_items"]:

            assignee = (
                item["assignee"]
                or "Not assigned"
            )

            due_date = (
                item["due_date"]
                or "Not specified"
            )

            output.append(
                f"• {item['title']}"
            )

            output.append(
                f"  Assignee: {assignee}"
            )

            output.append(
                f"  Due Date: {due_date}"
            )

    else:

        output.append(
            "No action items identified."
        )

    return "\n".join(output)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_transcript = """
    The team discussed the new AI meeting project.
    We reviewed the development schedule and project deadline.
    Ranjith will prepare the project documentation by Friday.
    The team agreed to complete the testing phase next week.
    We decided to review the final results in the next meeting.
    """

    print("\n========================================")
    print("AI MEETING MINUTES GENERATOR")
    print("========================================\n")

    minutes = generate_minutes(
        sample_transcript
    )

    print(
        generate_minutes_text(
            sample_transcript
        )
    )

    print("\n========================================")
    print("STRUCTURED OUTPUT")
    print("========================================\n")

    print(minutes)