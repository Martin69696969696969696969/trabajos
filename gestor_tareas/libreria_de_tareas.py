# Manejo de tareas

tareas = []  # Lista global para almacenar las tareas

def agregar_tarea(tarea):
    tareas.append({"tarea": tarea, "completada": False})

def listar_tareas():
    if not tareas:
        print("No hay tareas registradas.")
    else:
        for i, t in enumerate(tareas, 1):
            estado = "✔️" if t["completada"] else "❌"
            print(f"{i}. {t['tarea']} - {estado}")

def completar_tarea(indice):
    if 0 <= indice < len(tareas):
        tareas[indice]["completada"] = True
        print("Tarea marcada como completada.")
    else:
        print("Índice inválido.")
