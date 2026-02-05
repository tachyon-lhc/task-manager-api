import sqlite3
from pathlib import Path
from datetime import datetime

# Ruta a la base de datos en instance/
DEFAULT_DATABASE = Path(__file__).parent.parent / "instance" / "tasks.db"


def get_db_connection(db_path=DEFAULT_DATABASE):
    """
    Crea y retorna una conexión a la base de datos.
    Configura row_factory para acceso por nombre de columna.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=DEFAULT_DATABASE):
    """
    Inicializa la base de datos.
    Crea la tabla tasks si no existe.
    """
    conn = get_db_connection(db_path)
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
    print(" Base de datos inicializada")


def create_task(title, description="", priority="medium", db_path=DEFAULT_DATABASE):
    """
    Crea una nueva tarea en la base de datos.

    Args:
        title: Título de la tarea (obligatorio)
        description: Descripción (opcional)
        priority: Prioridad - 'low', 'medium', 'high' (default: 'medium')
        db_path: Ruta a la base de datos

    Returns:
        int: ID de la tarea creada
    """
    conn = get_db_connection(db_path)
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


def get_all_tasks(db_path=DEFAULT_DATABASE):
    """
    Obtiene todas las tareas de la base de datos.

    Args:
        db_path: Ruta a la base de datos

    Returns:
        list: Lista de diccionarios con todas las tareas
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    tasks_list = [dict(row) for row in rows]
    conn.close()
    return tasks_list


def get_task_by_id(task_id, db_path=DEFAULT_DATABASE):
    """
    Obtiene una tarea específica por ID.

    Args:
        task_id: ID de la tarea
        db_path: Ruta a la base de datos

    Returns:
        dict: Diccionario con la tarea, o None si no existe
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    task = dict(row) if row else None
    conn.close()
    return task


def update_task(
    task_id,
    title=None,
    description=None,
    completed=None,
    priority=None,
    db_path=DEFAULT_DATABASE,
):
    """
    Actualiza una tarea existente.
    Solo actualiza los campos que se proporcionan (no None).

    Args:
        task_id: ID de la tarea
        title, description, completed, priority: Campos a actualizar (opcionales)
        db_path: Ruta a la base de datos

    Returns:
        bool: True si se actualizó, False si no existe
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    task = get_task_by_id(task_id, db_path)
    if not task:
        conn.close()
        return False

    new_title = title if title is not None else task["title"]
    new_description = description if description is not None else task["description"]
    new_completed = completed if completed is not None else task["completed"]
    new_priority = priority if priority is not None else task["priority"]
    updated_at = datetime.now().isoformat()

    cursor.execute(
        "UPDATE tasks SET title=?, description=?, completed=?, priority=?, updated_at=? WHERE id=?",
        (new_title, new_description, new_completed, new_priority, updated_at, task_id),
    )
    conn.commit()
    conn.close()
    return True


def delete_task(task_id, db_path=DEFAULT_DATABASE):
    """
    Elimina una tarea de la base de datos.

    Args:
        task_id: ID de la tarea a eliminar
        db_path: Ruta a la base de datos

    Returns:
        bool: True si se eliminó, False si no existía
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    task = get_task_by_id(task_id, db_path)  # ← CORREGIDO: agregado db_path
    if not task:
        conn.close()
        return False

    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return True


def clear_tasks(db_path=DEFAULT_DATABASE):
    """
    Elimina todas las tareas de la base de datos.

    Args:
        db_path: Ruta a la base de datos
    """
    conn = get_db_connection(db_path)  # ← CORREGIDO: agregado db_path
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    conn.commit()
    conn.close()
