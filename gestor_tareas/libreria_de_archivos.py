import json
import libreria_de_tareas

def guardar_tareas(nombre_archivo="tareas.json"):
    with open(nombre_archivo, "w") as f:
        json.dump(libreria_de_tareas.tareas, f, indent=4)

def cargar_tareas(nombre_archivo="tareas.json"):
    try:
        with open(nombre_archivo, "r") as f:
            libreria_de_tareas.tareas = json.load(f)
    except FileNotFoundError:
        libreria_de_tareas.tareas = []
