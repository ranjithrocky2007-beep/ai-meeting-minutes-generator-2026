"""
AI Meeting Minutes Generator
Meeting History Management
"""

from typing import List, Dict, Any, Optional

from database import (
    get_connection,
    get_all_meetings,
    get_meeting,
    delete_meeting
)


# ============================================================
# SAVE MEETING TO HISTORY
# ============================================================

def save_to_history(
    filename: str,
    transcript: str = "",
    minutes: Any = "",
    status: str = "Completed",
    duration: float = 0
) -> int:
    """
    Save a processed meeting to the database.

    Returns:
        int: Newly created meeting ID
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO meetings
        (
            filename,
            transcript,
            minutes,
            status,
            duration
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            filename,
            transcript,
            str(minutes),
            status,
            duration
        )
    )

    meeting_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return meeting_id


# ============================================================
# GET MEETING HISTORY
# ============================================================

def get_history() -> List[Dict[str, Any]]:
    """
    Return all processed meetings.
    """

    return get_all_meetings()


# ============================================================
# GET RECENT MEETINGS
# ============================================================

def get_recent_meetings(
    limit: int = 10
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
# GET MEETING BY ID
# ============================================================

def get_history_item(
    meeting_id: int
) -> Optional[Dict[str, Any]]:
    """
    Return a single meeting from history.
    """

    return get_meeting(meeting_id)


# ============================================================
# SEARCH MEETINGS
# ============================================================

def search_history(
    keyword: str
) -> List[Dict[str, Any]]:
    """
    Search meetings by filename,
    transcript, or minutes.
    """

    keyword = keyword.strip()

    if not keyword:
        return get_history()

    connection = get_connection()
    cursor = connection.cursor()

    search_pattern = f"%{keyword}%"

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
            search_pattern,
            search_pattern,
            search_pattern
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# FILTER BY STATUS
# ============================================================

def get_meetings_by_status(
    status: str
) -> List[Dict[str, Any]]:
    """
    Return meetings with a specific status.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM meetings
        WHERE status = ?
        ORDER BY created_at DESC
        """,
        (status,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# DELETE FROM HISTORY
# ============================================================

def remove_from_history(
    meeting_id: int
) -> bool:
    """
    Delete a meeting from history.
    """

    return delete_meeting(meeting_id)


# ============================================================
# HISTORY STATISTICS
# ============================================================

def get_history_statistics() -> Dict[str, Any]:
    """
    Return useful statistics for the dashboard.
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

    # Processing / failed meetings
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM meetings
        WHERE status != 'Completed'
        """
    )

    other_meetings = cursor.fetchone()[0]

    # Total meeting duration
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
        "other_meetings": other_meetings,
        "total_duration": total_duration
    }


# ============================================================
# CLEAR ALL HISTORY
# ============================================================

def clear_history() -> int:
    """
    Delete all meeting history.

    Returns:
        int: Number of deleted meetings
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM meetings"
    )

    count = cursor.fetchone()[0]

    cursor.execute(
        "DELETE FROM meetings"
    )

    connection.commit()
    connection.close()

    return count


# ============================================================
# TEST HISTORY FUNCTIONS
# ============================================================

if __name__ == "__main__":

    print("\n================================")
    print("MEETING HISTORY")
    print("================================")

    history = get_history()

    if not history:

        print("No meetings found.")

    else:

        for meeting in history:

            print(
                f"\nID       : {meeting['id']}"
            )

            print(
                f"Filename : {meeting['filename']}"
            )

            print(
                f"Status   : {meeting['status']}"
            )

            print(
                f"Duration : {meeting['duration']} minutes"
            )

            print(
                f"Created  : {meeting['created_at']}"
            )

    print("\n================================")
    print("HISTORY STATISTICS")
    print("================================")

    statistics = get_history_statistics()

    print(
        f"Total Meetings     : "
        f"{statistics['total_meetings']}"
    )

    print(
        f"Completed Meetings : "
        f"{statistics['completed_meetings']}"
    )

    print(
        f"Other Meetings     : "
        f"{statistics['other_meetings']}"
    )

    print(
        f"Total Duration     : "
        f"{statistics['total_duration']} minutes"
    )