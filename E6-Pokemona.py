import random
import json
import os

class Movimiento:
    def __init__(self, nombre, poder, tipo):
        self.nombre = nombre
        self.poder = poder
        self.tipo = tipo

    def atacar(self, atacante, defensor):
        efectividad = 1.0
        daño = int(self.poder * efectividad)
        defensor.hp -= daño
        print(f"{atacante.nombre} usa {self.nombre} y causa {daño} puntos de daño a {defensor.nombre}.")

class pokemona:
    def __init__(self, nombre, tipo, hp, defensa, movimientos, arte_ascii):
        self.nombre = nombre
        self.tipo = tipo
        self.hp = hp
        self.defensa = defensa
        self.movimientos = movimientos
        self.arte_ascii = arte_ascii

    def esta_derrotado(self):
        return self.hp <= 0

    def atacar(self, movimiento, pokemona_objetivo):
        if movimiento in self.movimientos:
            movimiento.atacar(self, pokemona_objetivo)
        else:
            print("Este pokemona no conoce ese movimiento.")

    def mostrar_estado(self):
        print(self.arte_ascii)
        print(f"Nombre: {self.nombre}")
        print(f"Tipo: {self.tipo}")
        print(f"HP: {self.hp}")
        print("Movimientos:")
        for mov in self.movimientos:
            print(f"- {mov.nombre} (Poder: {mov.poder}, Tipo: {mov.tipo})")

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "hp": self.hp,
            "defensa": self.defensa,
            "movimientos": [ { "nombre": m.nombre, "poder": m.poder, "tipo": m.tipo } for m in self.movimientos],
            "arte_ascii": self.arte_ascii
        }

    @staticmethod
    def from_dict(data):
        movimientos = [Movimiento(m["nombre"], m["poder"], m["tipo"]) for m in data["movimientos"]]
        return pokemona(data["nombre"], data["tipo"], data["hp"], data["defensa"], movimientos, data["arte_ascii"])

salpicadura = Movimiento("Salpicadura", 0, "Agua")
ataque_basico = Movimiento("Ataque básico", 40, "Normal")
ataque_doble = Movimiento("Ataque doble", 60, "Normal")
hiperrayo = Movimiento("Hiperrayo", 90, "Normal")

lanza_llamas = Movimiento("Lanza Llamas", 75, "Fuego")
chorro_agua = Movimiento("Chorro de Agua", 70, "Agua")
hoja_afilada = Movimiento("Hoja Afilada", 65, "Planta")

llamartija_arte = """
   (\\_/)
   ( •_•)
  / >🔥 
"""
tortuagua_arte = """
   (~_~)
  <(   )>
    /   \\
"""
sapochuga_arte = """
   /\\_/\\
  ( o.o )
   > ^ <
"""

pokemona_iniciales = {
    "llamartija": pokemona("llamartija", "Fuego", 100, 10, [ataque_basico, ataque_doble, hiperrayo, lanza_llamas], llamartija_arte),
    "tortuagua": pokemona("tortuagua", "Agua", 110, 12, [ataque_basico, salpicadura, ataque_doble, chorro_agua], tortuagua_arte),
    "sapochuga": pokemona("sapochuga", "Planta", 105, 11, [ataque_basico, ataque_doble, hiperrayo, hoja_afilada], sapochuga_arte)
}

pajarritho_arte = """
(v·ᴥ·v)
"""
ratamaniaca_arte = """
(\_/)
( . .)
c(")(")
"""
murcieleco_arte = """
  (\\(\\
  (-.-)
  o_(")(")
"""
venecobra_arte = """
  ~~~~~
 (o   o)
  \   /
"""

pokemonaes_enemigos = [
    pokemona("pajarritho", "Normal", 50, 8, [ataque_basico], pajarritho_arte),
    pokemona("ratamaniaca", "Normal", 45, 7, [ataque_basico, ataque_doble], ratamaniaca_arte),
    pokemona("murcieleco", "Veneno", 55, 9, [ataque_basico], murcieleco_arte),
    pokemona("venecobra", "Veneno", 60, 8, [ataque_basico, ataque_doble], venecobra_arte)
]

class Juegopokemona:
    ARCHIVO_PARTIDA = "partida_guardada.json"

    def __init__(self):
        self.pokemona_jugador = None
        self.nombre_jugador = ""
        self.posiciones_enemigos = {}
        self.pokemones_enemigos = ["Enemigo1", "Enemigo2", "Enemigo3", "Enemigo4"]  
        self.mapa = self.crear_mapa()
        self.juego_activo = True

    def crear_mapa(self):
        mapa = [["." for _ in range(10)] for _ in range(10)]
        mapa[5][5] = "P"
        posiciones = [(2, 2), (7, 7), (1, 8), (8, 1)]
        for idx, pos in enumerate(posiciones):
            fila, col = pos
            mapa[fila][col] = "E"
            if idx < len(pokemonaes_enemigos):
                self.posiciones_enemigos[(fila, col)] = pokemonaes_enemigos[idx]
        return mapa

    def mostrar_mapa(self):
        print("\nMapa:")
        for fila in self.mapa:
            print(" ".join(fila))
        print("WASD para moverse, M para menú, V para volver")

    def mover_jugador(self, direccion):
        fila_actual, col_actual = 0, 0
        for i in range(10):
            for j in range(10):
                if self.mapa[i][j] == "P":
                    fila_actual, col_actual = i, j
                    break

        nueva_fila, nueva_col = fila_actual, col_actual
        if direccion == "w" and fila_actual > 0:
            nueva_fila -= 1
        elif direccion == "s" and fila_actual < 9:
            nueva_fila += 1
        elif direccion == "a" and col_actual > 0:
            nueva_col -= 1
        elif direccion == "d" and col_actual < 9:
            nueva_col += 1
        else:
            print("Movimiento no válido.")
            return

        if self.mapa[nueva_fila][nueva_col] == "E":
            enemigo = self.posiciones_enemigos.get((nueva_fila, nueva_col))
            if enemigo:
                self.ocurrir_combate(enemigo)
                if self.pokemona_jugador.esta_derrotado():
                    return
                self.mapa[nueva_fila][nueva_col] = "."
                del self.posiciones_enemigos[(nueva_fila, nueva_col)]

        self.mapa[fila_actual][col_actual] = "."
        self.mapa[nueva_fila][nueva_col] = "P"
        self.guardar_partida()

    def menu_principal(self):
        while self.juego_activo:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Crear Partida")
            print("2. Continuar Partida")
            print("3. Borrar Partida")
            print("4. Salir")
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                self.crear_partida()
                self.jugar()
            elif opcion == "2":
                if self.continuar_partida():
                    self.jugar()
            elif opcion == "3":
                self.borrar_partida()
            elif opcion == "4":
                print("Saliendo del juego...")
                self.juego_activo = False
            else:
                print("Opción no válida.")

    def crear_partida(self):
        self.nombre_jugador = input("Introduce tu nombre: ")
        print("Elige tu pokemona inicial:")
        for nombre in pokemona_iniciales:
            print(f"- {nombre}")
        elegido = ""
        while elegido not in pokemona_iniciales:
            elegido = input("Nombre del pokemona: ")
            if elegido not in pokemona_iniciales:
                print("Elige un pokemona válido.")
        self.pokemona_jugador = pokemona_iniciales[elegido]
        print(f"Has elegido a {self.pokemona_jugador.nombre}.")

        self.mapa = self.crear_mapa()
        self.guardar_partida()

    def continuar_partida(self):
        if not os.path.exists(self.ARCHIVO_PARTIDA):
            print("No hay partida guardada disponible.")
            return False

        with open(self.ARCHIVO_PARTIDA, "r") as archivo:
            data = json.load(archivo)

        self.nombre_jugador = data["nombre_jugador"]
        self.pokemona_jugador = pokemona.from_dict(data["pokemona_jugador"])
        self.mapa = data["mapa"]
        self.posiciones_enemigos.clear()
        enemigos_cargados = []
        for p_dict in data.get("enemigos", []):
            enemigos_cargados.append(pokemona.from_dict(p_dict))
        idx = 0
        for i in range(10):
            for j in range(10):
                if self.mapa[i][j] == "E":
                    if idx < len(enemigos_cargados):
                        self.posiciones_enemigos[(i,j)] = enemigos_cargados[idx]
                        idx += 1
        print(f"Partida cargada. Bienvenido de nuevo, {self.nombre_jugador}.")
        return True

    def borrar_partida(self):
        if os.path.exists(self.ARCHIVO_PARTIDA):
            os.remove(self.ARCHIVO_PARTIDA)
            print("Partida borrada correctamente.")
        else:
            print("No hay partida guardada para borrar.")

    def guardar_partida(self):
        data = {
            "nombre_jugador": self.nombre_jugador,
            "pokemona_jugador": self.pokemona_jugador.to_dict() if self.pokemona_jugador else None,
            "mapa": self.mapa,
            "enemigos": [p.to_dict() for p in self.posiciones_enemigos.values()]
        }
        with open(self.ARCHIVO_PARTIDA, "w") as archivo:
            json.dump(data, archivo)

    def jugar(self):
        jugando = True
        while jugando:
            self.mostrar_mapa()
            comando = input("Ingresa comando (WASD/M/V): ").lower()
            if comando in ["w", "a", "s", "d"]:
                self.mover_jugador(comando)
            elif comando == "m":
                self.menu_estados()
            elif comando == "v":
                jugando = False
            else:
                print("Comando no válido.")

    def menu_estados(self):
        print("\n--- ESTADO DEL pokemona ---")
        self.pokemona_jugador.mostrar_estado()

    def ocurrir_combate(self, enemigo):
        print(f"\n¡Ha ocurrido un combate contra {enemigo.nombre}!")
        self.menu_combate(enemigo)

    def menu_combate(self, enemigo):
        print("\n--- MENÚ DE COMBATE ---")
        while not self.pokemona_jugador.esta_derrotado() and not enemigo.esta_derrotado():
            print(f"\nTu pokemona: {self.pokemona_jugador.nombre} HP: {self.pokemona_jugador.hp}")
            print(f"Enemigo: {enemigo.nombre} HP: {enemigo.hp}")
            print("1. Luchar")
            print("2. Estado")
            print("3. Huir")
            opcion = input("Elige una opción: ")
            if opcion == "1":
                self.luchar(enemigo)
            elif opcion == "2":
                self.pokemona_jugador.mostrar_estado()
                enemigo.mostrar_estado()
            elif opcion == "3":
                print("Huyendo del combate...")
                return
            else:
                print("Opción inválida.")
        if self.pokemona_jugador.esta_derrotado():
            print("Has sido derrotado... Fin del juego.")
            self.juego_activo = False
        elif enemigo.esta_derrotado():
            print("¡Has ganado el combate!")

    def luchar(self, enemigo):
        print("\nSelecciona un movimiento:")
        for i, mov in enumerate(self.pokemona_jugador.movimientos):
            print(f"{i+1}. {mov.nombre} (Poder: {mov.poder})")
        try:
            opcion = int(input("Movimiento a usar: ")) - 1
            if 0 <= opcion < len(self.pokemona_jugador.movimientos):
                movimiento_elegido = self.pokemona_jugador.movimientos[opcion]
                self.pokemona_jugador.atacar(movimiento_elegido, enemigo)
                if enemigo.esta_derrotado():
                    return
                movimiento_enemigo = random.choice(enemigo.movimientos)
                enemigo.atacar(movimiento_enemigo, self.pokemona_jugador)
            else:
                print("Movimiento inválido.")
        except ValueError:
            print("Entrada inválida.")

if __name__ == "__main__":
    juego = Juegopokemona()
    juego.menu_principal()
