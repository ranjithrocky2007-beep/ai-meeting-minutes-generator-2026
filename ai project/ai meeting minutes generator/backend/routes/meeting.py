"""
AI Meeting Minutes Generator
Meeting Management Module
"""

from typing import List, Dict, Any, Optional

from database import (
    get_connection,
    create_meeting,
    get_meeting,
    get_all_meetings,
    update_meeting,
    delete_meeting
)


# ============================================================
# CREATE MEETING
# ============================================================

def add_meeting(
    filename: str,
    transcript: str = "",
    minutes: Any = "",
    status: str = "Completed",
    duration: float = 0
) -> int:
    """
    Create and save a new meeting.

    Returns:
        int: Meeting ID
    """

    meeting_id = create_meeting(
        filename=filename,
        transcript=transcript,
        minutes=str(minutes),
        status=status,
        duration=duration
    )

    return meeting_id


# ============================================================
# GET MEETING
# ============================================================

def get_meeting_details(
    meeting_id: int
) -> Optional[Dict[str, Any]]:
    """
    Get complete meeting details by ID.
    """

    meeting = get_meeting(meeting_id)

    if meeting is None:
        return None

    return meeting


# ============================================================
# GET ALL MEETINGS
# ============================================================

def list_meetings() -> List[Dict[str, Any]]:
    """
    Return all meetings.
    """

    return get_all_meetings()


# ============================================================
# UPDATE MEETING
# ============================================================

def edit_meeting(
    meeting_id: int,
    transcript: Optional[str] = None,
    minutes: Optional[Any] = None,
    status: Optional[str] = None
) -> bool:
    """
    Update an existing meeting.
    """

    if minutes is not None:
        minutes = str(minutes)

    return update_meeting(
        meeting_id=meeting_id,
        transcript=transcript,
        minutes=minutes,
        status=status
    )


# ============================================================
# DELETE MEETING
# ============================================================

def remove_meeting(
    meeting_id: int
) -> bool:
    """
    Delete a meeting.
    """

    return delete_meeting(meeting_id)


# ============================================================
# SEARCH MEETINGS
# ============================================================

def search_meetings(
    keyword: str
) -> List[Dict[str, Any]]:
    """
    Search meetings by filename,
    transcript, or minutes.
    """

    keyword = keyword.strip()

    if not keyword:
        return list_meetings()

    connection = get_connection()
    cursor = connection.cursor()

    pattern = f"%{keyword}%"

    cursor.execute(
        """
        SELECT *
        FROM meetings
        WHERE filename LIKE ?
           OR transcript LIKE ?
           OR minutes LIKE ?
        ORDER BY created_at DESC
        """,
        (
            pattern,
            pattern,
            pattern
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# GET RECENT MEETINGS
# ============================================================

def get_recent_meetings(
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Return the most recent meetings.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM meetings
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# GET COMPLETED MEETINGS
# ============================================================

def get_completed_meetings() -> List[Dict[str, Any]]:
    """
    Return meetings that were successfully processed.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM meetings
        WHERE status = 'Completed'
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# GET MEETING COUNT
# ============================================================

def get_meeting_count() -> int:
    """
    Return total number of meetings.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM meetings"
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ============================================================
# GET MEETING STATISTICS
# ============================================================

def get_meeting_statistics() -> Dict[str, Any]:
    """
    Return meeting statistics.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # Total meetings
    cursor.execute(
        "SELECT COUNT(*) FROM meetings"
    )

    total_meetings = cursor.fetchone()[0]

    # Completed meetings
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM meetings
        WHERE status = 'Completed'
        """
    )

    completed_meetings = cursor.fetchone()[0]

    # Failed meetings
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM meetings
        WHERE status = 'Failed'
        """
    )

    failed_meetings = cursor.fetchone()[0]

    # Total duration
    cursor.execute(
        """
        SELECT COALESCE(SUM(duration), 0)
        FROM meetings
        """
    )

    total_duration = cursor.fetchone()[0]

    connection.close()

    return {
        "total_meetings": total_meetings,
        "completed_meetings": completed_meetings,
        "failed_meetings": failed_meetings,
        "total_duration_minutes": total_duration
    }


# ============================================================
# TEST MEETING MODULE
# ============================================================

if __name__ == "__main__":

    print("\n================================")
    print("MEETING MANAGEMENT")
    print("================================")

    meetings = list_meetings()

    if not meetings:

        print("No meetings available.")

    else:

        for meeting in meetings:

            print(
                f"\nMeeting ID : "
                f"{meeting['id']}"
            )

            print(
                f"Filename   : "
                f"{meeting['filename']}"
            )

            print(
                f"Status     : "
                f"{meeting['status']}"
            )

            print(
                f"Duration   : "
                f"{meeting['duration']} minutes"
            )

            print(
                f"Created    : "
                f"{meeting['created_at']}"
            )

    print("\n================================")
    print("MEETING STATISTICS")
    print("================================")

    statistics = get_meeting_statistics()

    print(
        f"Total Meetings     : "
        f"{statistics['total_meetings']}"
    )

    print(
        f"Completed Meetings : "
        f"{statistics['completed_meetings']}"
    )

    print(
        f"Failed Meetings    : "
        f"{statistics['failed_meetings']}"
    )

    print(
        f"Total Duration     : "
        f"{statistics['total_duration_minutes']} minutes"
    )
    