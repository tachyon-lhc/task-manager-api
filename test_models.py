from app.models import (
    init_db,
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)

# Inicializar DB
init_db()

# Crear tareas
task1_id = create_task("Aprender Flask", "Crear API REST", "high")
task2_id = create_task("Practicar SQL", priority="medium")

print(f" Creadas tareas con IDs: {task1_id}, {task2_id}")

# Listar todas
tasks = get_all_tasks()
print(f"\n Todas las tareas: {len(tasks)}")
for task in tasks:
    print(f"  - {task['title']} (Priority: {task['priority']})")

# Obtener una
task = get_task_by_id(task1_id)
print(f"\n Tarea #{task1_id}: {task['title']}")

# Actualizar
update_task(task1_id, completed=1)
print(f"\n Tarea #{task1_id} marcada como completada")

# Verificar actualización
task = get_task_by_id(task1_id)
print(f" Completed: {task['completed']}")

# Eliminar
delete_task(task2_id)
print(f"\n Tarea #{task2_id} eliminada")

# Verificar eliminación
tasks = get_all_tasks()
print(f"\n Tareas restantes: {len(tasks)}")
