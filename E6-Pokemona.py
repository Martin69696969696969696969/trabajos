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

class Pokemona:
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
            print("Este Pokemona no conoce ese movimiento.")

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
            "movimientos": [{"nombre": m.nombre, "poder": m.poder, "tipo": m.tipo} for m in self.movimientos],
            "arte_ascii": self.arte_ascii
        }

    @staticmethod
    def from_dict(data):
        movimientos = [Movimiento(m["nombre"], m["poder"], m["tipo"]) for m in data["movimientos"]]
        return Pokemona(data["nombre"], data["tipo"], data["hp"], data["defensa"], movimientos, data["arte_ascii"])

# Movimientos
salpicadura = Movimiento("Salpicadura", 0, "Agua")
ataque_basico = Movimiento("Ataque básico", 40, "Normal")
ataque_doble = Movimiento("Ataque doble", 60, "Normal")
hiperrayo = Movimiento("Hiperrayo", 90, "Normal")
lanza_llamas = Movimiento("Lanza Llamas", 75, "Fuego")
chorro_agua = Movimiento("Chorro de Agua", 70, "Agua")
hoja_afilada = Movimiento("Hoja Afilada", 65, "Planta")

rayo = Movimiento("Rayo", 80, "Eléctrico")
pedrada = Movimiento("Pedrada", 70, "Roca")
tornado = Movimiento("Tornado", 75, "Volador")

# Ascii arts
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
pajarritho_arte = """
(v·ᴥ·v)
"""
ratamaniaca_arte = """
(\\_/)
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
  \\   /
"""

electrifox_arte = """
   /\\_/\\ 
  ( e.e )
   > ^ <⚡
"""
rocamon_arte = """
   _____
  /     \\
 |  ROCK |
  \\_____/
"""
aguila_arte = """
     /\\
    /  \\ 
   ( >.<)
    \\  /
     \\/
"""
fantasmito_arte = """
     .-.
    (   )
     |~|
    /   \\
"""

# Clases concretas
class Llamartija(Pokemona):
    def __init__(self):
        super().__init__("llamartija", "Fuego", 100, 10, [ataque_basico, ataque_doble, hiperrayo, lanza_llamas], llamartija_arte)

class Tortuagua(Pokemona):
    def __init__(self):
        super().__init__("tortuagua", "Agua", 110, 12, [ataque_basico, salpicadura, ataque_doble, chorro_agua], tortuagua_arte)

class Sapochuga(Pokemona):
    def __init__(self):
        super().__init__("sapochuga", "Planta", 105, 11, [ataque_basico, ataque_doble, hiperrayo, hoja_afilada], sapochuga_arte)

class Pajarritho(Pokemona):
    def __init__(self):
        super().__init__("pajarritho", "Normal", 50, 8, [ataque_basico], pajarritho_arte)

class Ratamaniaca(Pokemona):
    def __init__(self):
        super().__init__("ratamaniaca", "Normal", 45, 7, [ataque_basico, ataque_doble], ratamaniaca_arte)

class Murcieleco(Pokemona):
    def __init__(self):
        super().__init__("murcieleco", "Veneno", 55, 9, [ataque_basico], murcieleco_arte)

class Venecobra(Pokemona):
    def __init__(self):
        super().__init__("venecobra", "Veneno", 60, 8, [ataque_basico, ataque_doble], venecobra_arte)

class Electrifox(Pokemona):
    def __init__(self):
        super().__init__("electrifox", "Eléctrico", 55, 8, [ataque_basico, rayo], electrifox_arte)

class Rocamon(Pokemona):
    def __init__(self):
        super().__init__("rocamon", "Roca", 70, 15, [ataque_basico, pedrada], rocamon_arte)

class Aguila(Pokemona):
    def __init__(self):
        super().__init__("aguila", "Volador", 50, 7, [ataque_basico, ataque_doble, tornado], aguila_arte)

class Fantasmito(Pokemona):
    def __init__(self):
        super().__init__("fantasmito", "Fantasma", 60, 9, [ataque_basico, ataque_doble], fantasmito_arte)

clases_iniciales = {
    "llamartija": Llamartija,
    "tortuagua": Tortuagua,
    "sapochuga": Sapochuga
}

clases_enemigas = [Pajarritho, Ratamaniaca, Murcieleco, Venecobra, Electrifox, Rocamon, Aguila, Fantasmito]

class Mapa:
    def __init__(self):
        self.grid = None
        self.posiciones_enemigos = {}
        self.crear_mapa()

    def crear_mapa(self):
        self.grid = [["." for _ in range(10)] for _ in range(10)]
        self.grid[5][5] = "P"
        posiciones = [(2, 2), (7, 7), (1, 8), (8, 1)]
        enemigos_seleccionados = random.sample(clases_enemigas, 4)
        for idx, pos in enumerate(posiciones):
            fila, col = pos
            self.grid[fila][col] = "E"
            self.posiciones_enemigos[(fila, col)] = enemigos_seleccionados[idx]()

    def mostrar_mapa(self, limpiar=True):
        if limpiar:
            os.system('cls' if os.name == 'nt' else 'clear')
        print("\nMapa:")
        for fila in self.grid:
            print(" ".join(fila))
        print("WASD para moverse, M para menú, V para volver")

    def encontrar_posicion_jugador(self):
        for i in range(10):
            for j in range(10):
                if self.grid[i][j] == "P":
                    return i, j
        return 0, 0

    def calcular_nueva_posicion(self, fila_actual, col_actual, direccion):
        nueva_fila, nueva_col = fila_actual, col_actual
        if direccion == "w" and fila_actual > 0:
            nueva_fila -= 1
        elif direccion == "s" and fila_actual < 9:
            nueva_fila += 1
        elif direccion == "a" and col_actual > 0:
            nueva_col -= 1
        elif direccion == "d" and col_actual < 9:
            nueva_col += 1
        return nueva_fila, nueva_col

    def es_movimiento_valido(self, nueva_fila, nueva_col):
        return 0 <= nueva_fila < 10 and 0 <= nueva_col < 10

    def mover_jugador(self, direccion):
        fila_actual, col_actual = self.encontrar_posicion_jugador()
        nueva_fila, nueva_col = self.calcular_nueva_posicion(fila_actual, col_actual, direccion)
        if not self.es_movimiento_valido(nueva_fila, nueva_col):
            return None
        if self.grid[nueva_fila][nueva_col] == "E":
            enemigo = self.posiciones_enemigos.get((nueva_fila, nueva_col))
            if enemigo:
                return ("combat", enemigo, (nueva_fila, nueva_col))
            
        self.grid[fila_actual][col_actual] = "."
        self.grid[nueva_fila][nueva_col] = "P"
        return ("moved",)

    def eliminar_enemigo(self, pos):
        if pos in self.posiciones_enemigos:
            del self.posiciones_enemigos[pos]
            self.grid[pos[0]][pos[1]] = "."

    def to_dict(self):
        return {
            "grid": self.grid,
            "posiciones_enemigos": {f"{k[0]}_{k[1]}": v.to_dict() for k, v in self.posiciones_enemigos.items()}
        }

    def cargar(self, data):
        self.grid = data["grid"]
        self.posiciones_enemigos = {}
        for key, p_dict in data.get("posiciones_enemigos", {}).items():
            f, c = map(int, key.split('_'))
            pos = (f, c)
            self.posiciones_enemigos[pos] = Pokemona.from_dict(p_dict)

class Juego:
    ARCHIVO_PARTIDA = "partida_guardada.json"

    def __init__(self):
        self.pokemona_jugador = None
        self.nombre_jugador = ""
        self.mapa = None
        self.juego_activo = True

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
        print("Elige tu Pokemona inicial:")
        for nombre in clases_iniciales:
            print(f"- {nombre}")
        elegido = ""
        while elegido not in clases_iniciales:
            elegido = input("Nombre del Pokemona: ")
            if elegido not in clases_iniciales:
                print("Elige un Pokemona válido.")
        self.pokemona_jugador = clases_iniciales[elegido]()
        print(f"Has elegido a {self.pokemona_jugador.nombre}.")
        self.mapa = Mapa()
        self.guardar_partida()

    def continuar_partida(self):
        if not os.path.exists(self.ARCHIVO_PARTIDA):
            print("No hay partida guardada disponible.")
            return False
        with open(self.ARCHIVO_PARTIDA, "r") as archivo:
            data = json.load(archivo)
        self.nombre_jugador = data["nombre_jugador"]
        self.pokemona_jugador = Pokemona.from_dict(data["pokemona_jugador"])
        mapa_data = data["mapa"]
        self.mapa = Mapa()
        self.mapa.cargar(mapa_data)
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
            "mapa": self.mapa.to_dict() if self.mapa else None
        }
        with open(self.ARCHIVO_PARTIDA, "w") as archivo:
            json.dump(data, archivo)

    def jugar(self):
        jugando = True
        while jugando and self.juego_activo:
            self.mapa.mostrar_mapa(limpiar=True)
            comando = input("Ingresa comando (WASD/M/V): ").lower()
            if comando in ["w", "a", "s", "d"]:
                resultado = self.mapa.mover_jugador(comando)
                if resultado is None:
                    print("Movimiento no válido.")
                elif resultado[0] == "combat":
                    _, enemigo, pos = resultado
                    self.ocurrir_combate(enemigo)
                    if self.juego_activo:
                        self.mapa.eliminar_enemigo(pos)
                        self.mapa.grid[pos[0]][pos[1]] = "P"
                        self.guardar_partida()
                else:
                    self.guardar_partida()

            elif comando == "m":
                self.menu_estados()
                self.mapa.mostrar_mapa(limpiar=False)

            elif comando == "v":
                jugando = False
            else:
                print("Comando no válido.")

    def menu_estados(self):
        print("\n--- ESTADO DEL POKEMONA ---")
        if self.pokemona_jugador:
            self.pokemona_jugador.mostrar_estado()
        else:
            print("No tienes ningún Pokemona actualmente.")
        input("\nPresiona Enter para volver al mapa...")

    def ocurrir_combate(self, enemigo):
        print(f"\n¡Ha ocurrido un combate contra {enemigo.nombre}!")
        self.menu_combate(enemigo)

    def menu_combate(self, enemigo):
        print("\n--- MENÚ DE COMBATE ---")
        while not self.pokemona_jugador.esta_derrotado() and not enemigo.esta_derrotado():
            print(f"\nTu Pokemona: {self.pokemona_jugador.nombre} HP: {self.pokemona_jugador.hp}")
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
                input("\nPresiona Enter para continuar combate...")
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
    juego = Juego()
    juego.menu_principal()
