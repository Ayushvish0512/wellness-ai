from .database import conn


def save_message(user_id, role, message):
    conn.execute(
        "INSERT INTO chats (user_id, role, message) VALUES (?, ?, ?)",
        (user_id, role, message)
    )
    conn.commit()


def get_history(user_id, limit=6):
    cursor = conn.execute(
        "SELECT role, message FROM chats WHERE user_id=? ORDER BY id DESC LIMIT ?",
        (user_id, limit)
    )

    rows = cursor.fetchall()

    return [
        {"role": role, "content": message}
        for role, message in reversed(rows)
    ]
