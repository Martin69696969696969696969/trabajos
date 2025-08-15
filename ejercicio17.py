def mostrar_menu():
    print("\n--- Menú de Gestión de Estudiantes ---")
    print("1. Agregar un nuevo estudiante")
    print("2. Mostrar todos los estudiantes")
    print("3. Calcular el promedio de un estudiante por su ID")
    print("4. Eliminar un estudiante")
    print("5. Salir")

def agregar_estudiante(estudiantes):
    id_estudiante = input("Ingrese el ID del estudiante: ")
    if id_estudiante in estudiantes:
        print("Error: El ID ya existe. Intente con otro.")
        return
    
    nombre = input("Ingrese el nombre completo del estudiante: ")
    edad = input("Ingrese la edad del estudiante: ")
    
    if not edad.isdigit():
        print("Error: La edad debe ser un número.")
        return
    
    calificaciones = input("Ingrese las calificaciones separadas por comas: ")
    try:
        calificaciones = [float(cal) for cal in calificaciones.split(",")]
    except ValueError:
        print("Error: Las calificaciones deben ser numéricas.")
        return
    
    estudiantes[id_estudiante] = {
        "nombre": nombre,
        "edad": int(edad),
        "calificaciones": calificaciones
    }
    print(f"Estudiante {id_estudiante} agregado exitosamente.")

def mostrar_estudiantes(estudiantes):
    if not estudiantes:
        print("No hay estudiantes registrados.")
        return
    
    for id_estudiante, info in estudiantes.items():
        promedio = sum(info["calificaciones"]) / len(info["calificaciones"]) if info["calificaciones"] else 0
        print(f"Estudiante {id_estudiante} - {info['nombre']} - Promedio: {promedio:.2f}")

def calcular_promedio(estudiantes):
    id_estudiante = input("Ingrese el ID del estudiante: ")
    if id_estudiante not in estudiantes:
        print("Error: Estudiante no encontrado.")
        return
    
    info = estudiantes[id_estudiante]
    promedio = sum(info["calificaciones"]) / len(info["calificaciones"]) if info["calificaciones"] else 0
    print(f"Promedio de {info['nombre']}: {promedio:.2f}")

def eliminar_estudiante(estudiantes):
    id_estudiante = input("Ingrese el ID del estudiante a eliminar: ")
    if id_estudiante in estudiantes:
        del estudiantes[id_estudiante]
        print(f"Estudiante {id_estudiante} eliminado exitosamente.")
    else:
        print("Error: Estudiante no encontrado.")

def main():
    estudiantes = {}
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_estudiante(estudiantes)
        elif opcion == "2":
            mostrar_estudiantes(estudiantes)
        elif opcion == "3":
            calcular_promedio(estudiantes)
        elif opcion == "4":
            eliminar_estudiante(estudiantes)
        elif opcion == "5":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
