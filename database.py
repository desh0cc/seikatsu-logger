import sqlite3
from datetime import datetime, timezone

def get_connection():
    return sqlite3.connect("seikatsu.db")

def create_db():
    try:
        connection = None

        connection = get_connection()
        cursor = connection.cursor()

        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                activity_name TEXT NOT NULL,
                start_time TIME NOT NULL,
                end_time TIME NOT NULL,
                duration FLOAT NOT NULL 
            );

            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL DEFAULT CURRENT_DATE,
                note_text TEXT
            );

            CREATE TABLE IF NOT EXISTS chat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                external_id TEXT UNIQUE DEFAULT None,
                character_id TEXT DEFAULT None,
                source TEXT CHECK (source IN ('cai', 'local')),
                avatar VARCHAR,
                name VARCHAR,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                hide INTEGER DEFAULT 0
            );


            CREATE TABLE IF NOT EXISTS message (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER,
                external_id VARCHAR,
                text TEXT,
                sender TEXT CHECK (sender IN ('user', 'ai')),
                send_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chat(id) ON DELETE CASCADE
            );

            """
        )

        print("[DEBUG]: Таблиці створені")

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_log
            ON log (date, activity_name, start_time, end_time, duration)
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_message
            ON message (chat_id, text, sender, send_time);
            """
        )

        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_chat_external
            ON chat (external_id);
            """
        )

        connection.commit()
    except Exception as e:
        print(f"[DEBUG]: Виникла проблема: {e}")
    finally:
        if connection:
            connection.close()
            print("[DEBUG]: Зв'язок закрито")


def add_chat(source, avatar, name, external_id=None, character_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO chat (external_id, character_id, source, avatar, name)
            VALUES (?, ?, ?, ?, ?)
            """,
            (external_id, character_id, source, avatar, name)
        )
        chat_id = cursor.lastrowid
        conn.commit()
        print(f"[DEBUG]: Додано чат {name}")
        
    return chat_id

def get_character_id(chat_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT character_id
            FROM chat
            WHERE id = ?
            """,
            (chat_id,)
        )

        return cursor.fetchone()

def chat_exists(external_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, external_id FROM chat WHERE external_id = ?",
            (external_id,)
        )

        return cursor.fetchone()

def get_chats():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT chat.*, COALESCE(MAX(message.send_time), 0) AS last_message_time
            FROM chat
            LEFT JOIN message ON chat.id = message.chat_id
            GROUP BY chat.id
            ORDER BY last_message_time DESC
        """)
        return cursor.fetchall()


def get_chat_info(chat_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM chat WHERE id = ?", (chat_id,))
            return cursor.fetchone()
    except Exception:
        return None

def get_chat_messages(chat_id, last:bool = False):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM message WHERE chat_id = ? ORDER BY send_time DESC", (chat_id,))

        if last:
            return cursor.fetchone()
        return cursor.fetchall()
    
def get_message_info(message_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * 
            FROM message
            WHERE id = ?
            """,
            (message_id,)
        )

        return cursor.fetchone()
    
    
def message_exists(external_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM message
            WHERE external_id = ?
            """,
            (external_id,)
        )

        return bool(cursor.fetchone())
    
def update_message_exid(message_id, external_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE message
            SET external_id = ?
            WHERE id = ?
            """,
            (external_id, message_id)
        )

        conn.commit()

def add_message(chat_id, text, sender, external_id=None, send_time=None):
    with get_connection() as conn:
        cursor = conn.cursor()

        if send_time is None:
            send_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f%z")

        cursor.execute(
            """
            INSERT INTO message (chat_id, external_id, text, sender, send_time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (chat_id, external_id, text, sender, send_time)
        )

        message_id = cursor.lastrowid
        conn.commit()

    return message_id

def add_note(text):
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO note (note_text)
            VALUES (?)
            """,
            (text,)
        )

        conn.commit()

def get_note(date):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT note_text FROM note
            WHERE date = ?
            """,
            (date,)
        )

        result = cursor.fetchone()
        return result[0] if result else None
    
def update_note(date, text):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE note 
            SET note_text = ?
            WHERE date = ?
            """,
            (text, date)
        )

        conn.commit()
    
def delete_cai_chats():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id FROM chat
            WHERE external_id IS NOT NULL
            """
        )
        chat_ids = [row[0] for row in cursor.fetchall()]

        if chat_ids:
            cursor.execute(
                f"""
                DELETE FROM message
                WHERE chat_id IN ({','.join(['?'] * len(chat_ids))})
                """,
                chat_ids
            )

            cursor.execute(
                """
                DELETE FROM chat
                WHERE id IN ({})
                """.format(','.join(['?'] * len(chat_ids))),
                chat_ids
            )

        conn.commit()

def delete_chat(chat_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM chat
            WHERE id = ?
            """,
            (chat_id,)
        )

        cursor.execute(
            """
            DELETE FROM message
            WHERE chat_id = ?
            """,
            (chat_id,)
        )

        conn.commit()
    
def delete_message(message_id):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM message
            WHERE id = ?
            """,
            (message_id,)
        )

        conn.commit()