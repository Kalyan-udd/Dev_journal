import sqlite3
import json

def insert_values(data : dict, time, database_path: str = "Database.db"):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        tags TEXT NOT NULL,
        created_at TEXT NOT NULL,
        comments TEXT NOT NULL
        )
        """)
    comment_json = json.dumps(data.get("comments", []))

    query = """
        INSERT INTO journal (title, content, tags, created_at, comments)
        VALUES (?, ?, ?, ?, ?)    
    """
    cursor.execute(
        query,
            (
                data.get("title"),
                data.get("content"),
                data.get("tags"),
                str(time),
                comment_json
            ),
    )
    conn.commit()
    conn.close()
    return "Inserted values successfully..."

def show_complete_data(database_path:str = "Database.db"):
    conn = sqlite3.connect(database=database_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM journal;
    """)
    rows = cursor.fetchall()
    journal_list = []

    for row in rows:
        post_dict = dict(row)
        if post_dict.get("comments"):
            post_dict['comments'] = json.loads(post_dict['comments'])
        journal_list.append(post_dict)

    return journal_list

def update_comment(entryId:int, new_comment:str, database_path:str = "Database.db"):
    conn = sqlite3.connect(database=database_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT comments FROM journal WHERE id = ?;", (entryId,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
    current_comment = json.loads(row['comments']) if row['comments'] else []
    current_comment.append(new_comment)
    updated_comments = json.dumps(current_comment)

    cursor.execute(
        "UPDATE journal SET comments = ? WHERE id = ?;",
        (updated_comments, entryId),
    )
    conn.commit()
    conn.close()
    return True

def prompt_query(journal_name: str, database_path:str = "Database.db"):
    conn = sqlite3.connect(database=database_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM journal WHERE title = ?", (journal_name,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        return dict(row)
    except:
        return None


def update_content(content_type: str, entry_Id : int, content:str, database_path:str = "Database.db"):
    conn = sqlite3.connect(database=database_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"UPDATE journal SET {content_type} = ? WHERE id = ?;",(content, entry_Id))
    conn.commit()
    cursor.execute("SELECT * FROM journal WHERE id = ?;", (entry_Id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row)

def delete_journal_post(entryId: int, database_path: str = "Database.db"):
    conn = sqlite3.connect(database=database_path)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM journal WHERE id = ?;", (entryId,))
        conn.commit()
        conn.close()
        return f"Successfully deleted the post with id {entryId}."
    except Exception as e:
        conn.close()
        return f"Error occured - {e}"


def delete_comment(entryId: int, comment_index: int, database_path: str = "Database.db"):
    conn = sqlite3.connect(database=database_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT comments FROM journal WHERE id = ?;", (entryId,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
    current_comment = json.loads(row['comments']) if row['comments'] else []
    current_comment.pop(comment_index)
    update_comment = json.dumps(current_comment)

    cursor.execute("UPDATE journal SET comments = ? WHERE id = ?;", (update_comment, entryId,))
    conn.commit()
    conn.close()
    return True
      