import libreria_de_tareas
import libreria_de_archivos
import libreria_utils

def main():
    libreria_de_archivos.cargar_tareas()  # Cargar tareas guardadas
    while True:
        libreria_utils.limpiar_pantalla()
        libreria_utils.mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            tarea = input("Escribe la nueva tarea: ")
            libreria_de_tareas.agregar_tarea(tarea)

        elif opcion == "2":
            libreria_de_tareas.listar_tareas()
            input("\nPresiona Enter para continuar...")

        elif opcion == "3":
            libreria_de_tareas.listar_tareas()
            indice = int(input("Número de la tarea a completar: ")) - 1
            libreria_de_tareas.completar_tarea(indice)
            input("\nPresiona Enter para continuar...")

        elif opcion == "4":
            libreria_de_archivos.guardar_tareas()
            print("Tareas guardadas. ¡Adiós!")
            break
        else:
            print("Opción inválida.")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()

