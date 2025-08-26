def calcular_promedio(calificaciones):
    if not calificaciones:
        return 0
    return sum(calificaciones) / len(calificaciones)

def leer_estudiantes(archivo):
    calificaciones = []
    try:
        with open(archivo, 'r') as f:
            for linea in f:
                nombre, calificacion = linea.strip().split(',')
                calificaciones.append(float(calificacion))
        return calificaciones
    except FileNotFoundError:
        print(f"Error: El archivo {archivo} no existe.")
        return []
    except ValueError:
        print("Error: Formato de archivo incorrecto.")
        return []

def escribir_reporte(archivo, calificaciones, promedio):
    with open(archivo, 'w') as f:
        f.write("Nombre,Calificación\n")
        for nombre, calificacion in calificaciones:
            f.write(f"{nombre},{calificacion}\n")
        f.write(f"Promedio general: {promedio:.1f}\n")

def agregar_estudiante(archivo):
    nombre = input("Ingrese el nombre del estudiante: ")
    calificacion = input("Ingrese la calificación del estudiante: ")
    try:
        calificacion = float(calificacion)
        with open(archivo, 'a') as f:
            f.write(f"{nombre},{calificacion}\n")
    except ValueError:
        print("Error: La calificación debe ser un número.")

def main():
    archivo_estudiantes = 'estudiantes.txt'
    archivo_reporte = 'reporte.txt'

    # Leer estudiantes y calcular promedio
    calificaciones = leer_estudiantes(archivo_estudiantes)
    if calificaciones:
        promedio = calcular_promedio(calificaciones)
        print(f"Promedio calculado: {promedio:.1f}")

        # Crear lista de tuplas (nombre, calificacion) para el reporte
        estudiantes = []
        with open(archivo_estudiantes, 'r') as f:
            for linea in f:
                nombre, calificacion = linea.strip().split(',')
                estudiantes.append((nombre, calificacion))

        # Escribir el reporte
        escribir_reporte(archivo_reporte, estudiantes, promedio)

    # Agregar nuevos estudiantes
    while True:
        agregar_nuevo = input("¿Desea agregar un nuevo estudiante? (s/n): ")
        if agregar_nuevo.lower() == 's':
            agregar_estudiante(archivo_estudiantes)
        else:
            break

if __name__ == "__main__":
    main()
