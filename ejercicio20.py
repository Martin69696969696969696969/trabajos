import sys
import random

def generar_numeros_aleatorios(cantidad):
    numeros = [random.randint(1, 100) for _ in range(cantidad)]
    return numeros

def main():
    if len(sys.argv) != 2:
        print("Uso: python programa.py <cantidad>")
        return

    try:
        cantidad = int(sys.argv[1])
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser un número entero positivo.")
    except ValueError as e:
        print(f"Error: {e}")
        return

    numeros_aleatorios = generar_numeros_aleatorios(cantidad)
    print("Números aleatorios generados:", ' '.join(map(str, numeros_aleatorios)))

if __name__ == "__main__":
    main()
