import json
import os
import random
import time
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False

def color_text(text, color=Fore.GREEN):
    """Devuelve texto coloreado si colorama está disponible"""
    return f"{color}{text}{Style.RESET_ALL}" if COLOR else text

FILE = "jugadores.json"

def cargar_jugadores():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_jugadores(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def registrar_jugador(jugadores):
    nombre = input("Ingresa tu nombre de jugador: ")
    if nombre in jugadores:
        print(color_text("Ese jugador ya existe, cargando...", Fore.YELLOW))
        return jugadores[nombre]
    
    print("Clases disponibles: Guerrero, Mago, Explorador")
    clase = input("Elige tu clase: ").capitalize()
    if clase not in ["Guerrero", "Mago", "Explorador"]:
        clase = "Explorador"
        print(color_text("Clase no válida, asignado 'Explorador'", Fore.RED))

    jugador = {
        "nombre": nombre,
        "clase": clase,
        "nivel": 1,
        "vida": 100,
        "inventario": {"Poción": 2},
        "logros": [],
    }
    jugadores[nombre] = jugador
    guardar_jugadores(jugadores)
    print(color_text(f"Jugador {nombre} registrado con éxito.", Fore.GREEN))
    return jugador

def combate(jugador, enemigo):
    print(color_text(f"\n¡Un {enemigo['nombre']} aparece!", Fore.RED))
    while jugador["vida"] > 0 and enemigo["vida"] > 0:
        accion = input("\n¿Quieres (A) Atacar o (U) Usar poción? ").upper()
        if accion == "A":
            daño = random.randint(10, 20) + jugador["nivel"] * 2
            enemigo["vida"] -= daño
            print(color_text(f"Golpeas a {enemigo['nombre']} causando {daño} de daño.", Fore.CYAN))
        elif accion == "U":
            if jugador["inventario"].get("Poción", 0) > 0:
                jugador["vida"] += 30
                jugador["inventario"]["Poción"] -= 1
                print(color_text("Usaste una poción. Vida +30.", Fore.GREEN))
            else:
                print(color_text("No tienes pociones.", Fore.RED))
        else:
            print("Acción no válida.")

        # Turno enemigo
        if enemigo["vida"] > 0:
            daño = random.randint(5, 15)
            jugador["vida"] -= daño
            print(color_text(f"{enemigo['nombre']} te ataca y causa {daño} de daño.", Fore.MAGENTA))
    
    if jugador["vida"] > 0:
        print(color_text(f"¡Has derrotado al {enemigo['nombre']}!", Fore.GREEN))
        jugador["nivel"] += 1
        print(color_text(f"Subes a nivel {jugador['nivel']}!", Fore.YELLOW))
        return True
    else:
        print(color_text("Has sido derrotado... Fin de la aventura.", Fore.RED))
        return False

def aventura(jugador):
    print(color_text("\nComienza tu aventura...", Fore.CYAN))
    
    # Decisión 1
    decision1 = input("\nEncuentras un cruce de caminos. ¿Vas a la (I)zquierda hacia el bosque o a la (D)erecha hacia la montaña? ").upper()
    if decision1 == "I":
        print("Te adentras en el bosque oscuro...")
        enemigo = {"nombre": "Lobo Salvaje", "vida": 50}
    else:
        print("Subes la montaña nevada...")
        enemigo = {"nombre": "Goblin Montañés", "vida": 60}
    
    if not combate(jugador, enemigo):
        return False
    
    # Decisión 2
    decision2 = input("\nEncuentras un cofre misterioso. ¿Lo (A)brirás o lo (I)gnoras? ").upper()
    if decision2 == "A":
        recompensa = random.choice(["Espada", "Armadura", "Poción"])
        jugador["inventario"][recompensa] = jugador["inventario"].get(recompensa, 0) + 1
        print(color_text(f"¡Encontraste un {recompensa}!", Fore.YELLOW))
    else:
        print("Ignoras el cofre y sigues tu camino...")

    # Decisión 3
    decision3 = input("\nUn dragón aparece en el horizonte. ¿Lo (E)nfrentas o (H)uyes? ").upper()
    if decision3 == "E":
        enemigo = {"nombre": "Dragón", "vida": 120}
        if not combate(jugador, enemigo):
            return False
        jugador["logros"].append("Derrotó al Dragón")
    else:
        print("Escapas del dragón, pero tu honor queda en duda...")
    
    return True

def main():
    jugadores = cargar_jugadores()
    jugador = registrar_jugador(jugadores)
    
    continuar = True
    while continuar and jugador["vida"] > 0:
        exito = aventura(jugador)
        guardar_jugadores(jugadores)
        if not exito:
            continuar = False
            break
        continuar = input("\n¿Quieres seguir jugando? (S/N): ").upper() == "S"
    
    print(color_text("\nGracias por jugar. Progreso guardado.", Fore.CYAN))


if __name__ == "__main__":
    main()
