import sqlite3
from pathlib import Path
from datetime import datetime

# Ruta a la base de datos en instance/
DATABASE = Path(__file__).parent.parent / "instance" / "tasks.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            priority TEXT DEFAULT 'medium',
            created_at TEXT NOT NULL,
            updated_at TEXT
        )"""
    )

    conn.commit()
    conn.close()

    print("Base de datos inicializada")


def create_task(title, description="", priority="medium"):
    conn = get_db_connection()
    cursor = conn.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        "INSERT INTO tasks (title, description, priority, created_at) VALUES (?, ?, ?, ?)",
        (title, description, priority, created_at),
    )

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return task_id
