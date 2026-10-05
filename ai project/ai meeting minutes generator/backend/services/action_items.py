"""
AI Meeting Minutes Generator
Action Items Management Module

Handles:
- Creating action items
- Getting action items
- Updating action items
- Completing action items
- Deleting action items
- Getting pending action items
"""

from typing import List, Dict, Any, Optional

from database import get_connection


# ============================================================
# CREATE ACTION ITEM
# ============================================================

def create_action_item(
    meeting_id: int,
    title: str,
    assignee: str = "",
    due_date: str = ""
) -> int:
    """
    Create a new action item for a meeting.

    Returns:
        int: Newly created action item ID
    """

    if not title or not title.strip():
        raise ValueError(
            "Action item title cannot be empty."
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO action_items
        (
            meeting_id,
            title,
            assignee,
            due_date,
            completed
        )
        VALUES (?, ?, ?, ?, 0)
        """,
        (
            meeting_id,
            title.strip(),
            assignee.strip(),
            due_date.strip()
        )
    )

    action_item_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return action_item_id


# ============================================================
# GET ACTION ITEM
# ============================================================

def get_action_item(
    action_item_id: int
) -> Optional[Dict[str, Any]]:
    """
    Get one action item by ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM action_items
        WHERE id = ?
        """,
        (action_item_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


# ============================================================
# GET ALL ACTION ITEMS
# ============================================================

def get_all_action_items() -> List[Dict[str, Any]]:
    """
    Get all action items.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM action_items
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# GET ACTION ITEMS FOR MEETING
# ============================================================

def get_meeting_action_items(
    meeting_id: int
) -> List[Dict[str, Any]]:
    """
    Get all action items belonging to a meeting.
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


# ============================================================
# GET PENDING ACTION ITEMS
# ============================================================

def get_pending_action_items() -> List[Dict[str, Any]]:
    """
    Get all incomplete action items.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM action_items
        WHERE completed = 0
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# GET COMPLETED ACTION ITEMS
# ============================================================

def get_completed_action_items() -> List[Dict[str, Any]]:
    """
    Get all completed action items.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM action_items
        WHERE completed = 1
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# COMPLETE ACTION ITEM
# ============================================================

def complete_action_item(
    action_item_id: int
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
        (action_item_id,)
    )

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


# ============================================================
# REOPEN ACTION ITEM
# ============================================================

def reopen_action_item(
    action_item_id: int
) -> bool:
    """
    Mark an action item as incomplete again.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE action_items
        SET completed = 0
        WHERE id = ?
        """,
        (action_item_id,)
    )

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


# ============================================================
# UPDATE ACTION ITEM
# ============================================================

def update_action_item(
    action_item_id: int,
    title: Optional[str] = None,
    assignee: Optional[str] = None,
    due_date: Optional[str] = None,
    completed: Optional[bool] = None
) -> bool:
    """
    Update an existing action item.
    """

    current = get_action_item(action_item_id)

    if current is None:
        return False

    new_title = (
        title.strip()
        if title is not None
        else current["title"]
    )

    new_assignee = (
        assignee.strip()
        if assignee is not None
        else current["assignee"]
    )

    new_due_date = (
        due_date.strip()
        if due_date is not None
        else current["due_date"]
    )

    new_completed = (
        int(completed)
        if completed is not None
        else current["completed"]
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE action_items
        SET title = ?,
            assignee = ?,
            due_date = ?,
            completed = ?
        WHERE id = ?
        """,
        (
            new_title,
            new_assignee,
            new_due_date,
            new_completed,
            action_item_id
        )
    )

    updated = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return updated


# ============================================================
# DELETE ACTION ITEM
# ============================================================

def delete_action_item(
    action_item_id: int
) -> bool:
    """
    Delete an action item.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM action_items
        WHERE id = ?
        """,
        (action_item_id,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


# ============================================================
# SEARCH ACTION ITEMS
# ============================================================

def search_action_items(
    keyword: str
) -> List[Dict[str, Any]]:
    """
    Search action items by title or assignee.
    """

    keyword = keyword.strip()

    if not keyword:
        return get_all_action_items()

    connection = get_connection()
    cursor = connection.cursor()

    pattern = f"%{keyword}%"

    cursor.execute(
        """
        SELECT *
        FROM action_items
        WHERE title LIKE ?
           OR assignee LIKE ?
        ORDER BY created_at DESC
        """,
        (
            pattern,
            pattern
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]


# ============================================================
# ACTION ITEM STATISTICS
# ============================================================

def get_action_item_statistics() -> Dict[str, int]:
    """
    Get action item statistics.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM action_items"
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM action_items
        WHERE completed = 0
        """
    )

    pending = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM action_items
        WHERE completed = 1
        """
    )

    completed = cursor.fetchone()[0]

    connection.close()

    return {
        "total": total,
        "pending": pending,
        "completed": completed
    }


# ============================================================
# TEST MODULE
# ============================================================

if __name__ == "__main__":

    print("\n========================================")
    print("ACTION ITEMS MANAGEMENT")
    print("========================================")

    statistics = get_action_item_statistics()

    print(
        f"Total Action Items : "
        f"{statistics['total']}"
    )

    print(
        f"Pending            : "
        f"{statistics['pending']}"
    )

    print(
        f"Completed          : "
        f"{statistics['completed']}"
    )

    print("\nPending Action Items:")

    pending = get_pending_action_items()

    if not pending:

        print("No pending action items.")

    else:

        for item in pending:

            print(
                f"\nID       : {item['id']}"
            )

            print(
                f"Meeting  : {item['meeting_id']}"
            )

            print(
                f"Task     : {item['title']}"
            )

            print(
                f"Assignee : "
                f"{item['assignee'] or 'Not assigned'}"
            )

            print(
                f"Due Date : "
                f"{item['due_date'] or 'Not specified'}"
            )