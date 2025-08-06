import numpy as np

def obtener_matriz(nombre):
    filas = int(input(f"Ingrese el número de filas de la matriz {nombre}: "))
    columnas = int(input(f"Ingrese el número de columnas de la matriz {nombre}: "))
    matriz = []
    print(f"Ingrese los elementos de la matriz {nombre} fila por fila:")
    for i in range(filas):
        fila = list(map(float, input(f"Fila {i + 1}: ").split()))
        if len(fila) != columnas:
            print("Error: La cantidad de elementos en la fila no coincide con el número de columnas.")
            return None
        matriz.append(fila)
    return np.array(matriz)

def menu():
    print("\nCalculadora de matrices")
    print("1. Suma de matrices")
    print("2. Resta de matrices")
    print("3. Multiplicación de matrices")
    print("4. Transposición de una matriz")
    print("5. Salir")

def main():
    while True:
        menu()
        opcion = input("Seleccione una operación (1-5): ")

        if opcion == '1':
            A = obtener_matriz("A")
            B = obtener_matriz("B")
            if A is not None and B is not None and A.shape == B.shape:
                resultado = A + B
                print("Resultado de la suma:\n", resultado)
            else:
                print("Error: Las dimensiones de las matrices no son compatibles para la suma.")

        elif opcion == '2':
            A = obtener_matriz("A")
            B = obtener_matriz("B")
            if A is not None and B is not None and A.shape == B.shape:
                resultado = A - B
                print("Resultado de la resta:\n", resultado)
            else:
                print("Error: Las dimensiones de las matrices no son compatibles para la resta.")

        elif opcion == '3':
            A = obtener_matriz("A")
            B = obtener_matriz("B")
            if A is not None and B is not None and A.shape[1] == B.shape[0]:
                resultado = np.dot(A, B)
                print("Resultado de la multiplicación:\n", resultado)
            else:
                print("Error: Las dimensiones de las matrices no son compatibles para la multiplicación.")

        elif opcion == '4':
            A = obtener_matriz("A")
            if A is not None:
                resultado = A.T
                print("Resultado de la transposición:\n", resultado)

        elif opcion == '5':
            print("Saliendo de la calculadora.")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 5.")

if __name__ == "__main__":
    main()