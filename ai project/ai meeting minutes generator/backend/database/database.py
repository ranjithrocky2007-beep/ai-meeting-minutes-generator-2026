"""
AI Meeting Minutes Generator
Database Configuration and Helper Functions

Database: SQLite
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any


# ============================================================
# DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "meeting_minutes.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():
    """
    Create all required database tables.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # Meetings table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            transcript TEXT,
            minutes TEXT,
            status TEXT DEFAULT 'Completed',
            duration REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # --------------------------------------------------------
    # Action items table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS action_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            assignee TEXT,
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (meeting_id)
            REFERENCES meetings(id)
            ON DELETE CASCADE
        )
    """)

    # --------------------------------------------------------
    # Decisions table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER NOT NULL,
            decision TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (meeting_id)
            REFERENCES meetings(id)
            ON DELETE CASCADE
        )
    """)

    # --------------------------------------------------------
    # Participants table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meeting_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            role TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (meeting_id)
            REFERENCES meetings(id)
            ON DELETE CASCADE
        )
    """)

    connection.commit()
    connection.close()

    print("Database initialized successfully.")


# ============================================================
# CREATE MEETING
# ============================================================

def create_meeting(
    filename: str,
    transcript: str = "",
    minutes: str = "",
    status: str = "Completed",
    duration: float = 0
) -> int:
    """
    Insert a new meeting into the database.

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
            minutes,
            status,
            duration
        )
    )

    meeting_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return meeting_id


# ============================================================
# GET ALL MEETINGS
# ============================================================

def get_all_meetings() -> List[Dict[str, Any]]:
    """
    Return all meetings from newest to oldest.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM meetings
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# GET SINGLE MEETING
# ============================================================

def get_meeting(meeting_id: int) -> Optional[Dict[str, Any]]:
    """
    Return one meeting by ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM meetings
        WHERE id = ?
        """,
        (meeting_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


# ============================================================
# UPDATE MEETING
# ============================================================

def update_meeting(
    meeting_id: int,
    transcript: Optional[str] = None,
    minutes: Optional[str] = None,
    status: Optional[str] = None
) -> bool:
    """
    Update meeting information.
    """

    connection = get_connection()
    cursor = connection.cursor()

    meeting = get_meeting(meeting_id)

    if meeting is None:
        connection.close()
        return False

    new_transcript = (
        transcript
        if transcript is not None
        else meeting["transcript"]
    )

    new_minutes = (
        minutes
        if minutes is not None
        else meeting["minutes"]
    )

    new_status = (
        status
        if status is not None
        else meeting["status"]
    )

    cursor.execute(
        """
        UPDATE meetings
        SET transcript = ?,
            minutes = ?,
            status = ?
        WHERE id = ?
        """,
        (
            new_transcript,
            new_minutes,
            new_status,
            meeting_id
        )
    )

    connection.commit()
    connection.close()

    return True


# ============================================================
# DELETE MEETING
# ============================================================

def delete_meeting(meeting_id: int) -> bool:
    """
    Delete a meeting and its related records.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM meetings
        WHERE id = ?
        """,
        (meeting_id,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


# ============================================================
# ACTION ITEMS
# ============================================================

def create_action_item(
    meeting_id: int,
    title: str,
    assignee: str = "",
    due_date: str = ""
) -> int:
    """
    Create a new action item.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO action_items
        (
            meeting_id,
            title,
            assignee,
            due_date
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            meeting_id,
            title,
            assignee,
            due_date
        )
    )

    action_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return action_id


def get_action_items(
    meeting_id: int
) -> List[Dict[str, Any]]:
    """
    Get action items for a meeting.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM action_items
        WHERE meeting_id = ?
        ORDER BY created_at DESC
        """,
        (meeting_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


def complete_action_item(
    action_id: int
) -> bool:
    """
    Mark an action item as completed.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE action_items
        SET completed = 1
        WHERE id = ?
        """,
        (action_id,)
    )

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


# ============================================================
# DECISIONS
# ============================================================

def create_decision(
    meeting_id: int,
    decision: str
) -> int:
    """
    Save a meeting decision.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO decisions
        (
            meeting_id,
            decision
        )
        VALUES (?, ?)
        """,
        (
            meeting_id,
            decision
        )
    )

    decision_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return decision_id


def get_decisions(
    meeting_id: int
) -> List[Dict[str, Any]]:
    """
    Get all decisions for a meeting.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM decisions
        WHERE meeting_id = ?
        ORDER BY created_at DESC
        """,
        (meeting_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# PARTICIPANTS
# ============================================================

def create_participant(
    meeting_id: int,
    name: str,
    role: str = ""
) -> int:
    """
    Add a participant to a meeting.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO participants
        (
            meeting_id,
            name,
            role
        )
        VALUES (?, ?, ?)
        """,
        (
            meeting_id,
            name,
            role
        )
    )

    participant_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return participant_id


def get_participants(
    meeting_id: int
) -> List[Dict[str, Any]]:
    """
    Get all participants for a meeting.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM participants
        WHERE meeting_id = ?
        ORDER BY name ASC
        """,
        (meeting_id,)
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# DATABASE STATISTICS
# ============================================================

def get_database_statistics() -> Dict[str, int]:
    """
    Return basic database statistics.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM meetings"
    )
    total_meetings = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM action_items"
    )
    total_action_items = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM decisions"
    )
    total_decisions = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM participants"
    )
    total_participants = cursor.fetchone()[0]

    connection.close()

    return {
        "total_meetings": total_meetings,
        "total_action_items": total_action_items,
        "total_decisions": total_decisions,
        "total_participants": total_participants
    }


# ============================================================
# INITIALIZE DATABASE WHEN FILE IS RUN
# ============================================================

if __name__ == "__main__":
    init_database()

    print("\nDatabase:", DATABASE_PATH)

    statistics = get_database_statistics()

    print("\nDatabase Statistics:")
    print(
        f"Meetings      : {statistics['total_meetings']}"
    )
    print(
        f"Action Items  : {statistics['total_action_items']}"
    )
    print(
        f"Decisions     : {statistics['total_decisions']}"
    )
    print(
        f"Participants  : {statistics['total_participants']}"
    )