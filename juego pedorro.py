import json
import random
import os
import time
import sys

# Instalar colorama si no está disponible
try:
    from colorama import init, Fore, Back, Style
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    print("Colorama no está instalado. La salida será en texto plano.")
    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = Back = Style = DummyColor()

if COLORAMA_AVAILABLE:
    init()

# Configuración del juego
SAVE_FILE = 'aventura_save.json'

# Sistema de clases
CLASS_STATS = {
    'guerrero': {'vida': 100, 'ataque': 15, 'defensa': 10, 'mana': 30},
    'mago': {'vida': 70, 'ataque': 8, 'defensa': 5, 'mana': 100},
    'explorador': {'vida': 85, 'ataque': 12, 'defensa': 7, 'mana': 50}
}

# Sistema de items
ITEMS = {
    'pocion_vida': {'nombre': 'Poción de Vida', 'efecto': 'cura 30 vida', 'precio': 15},
    'pocion_mana': {'nombre': 'Poción de Mana', 'efecto': 'restaura 25 mana', 'precio': 12},
    'espada_acero': {'nombre': 'Espada de Acero', 'efecto': '+7 ataque', 'precio': 60},
    'armadura_metal': {'nombre': 'Armadura de Metal', 'efecto': '+5 defensa', 'precio': 50},
    'amuleto_proteccion': {'nombre': 'Amuleto de Protección', 'efecto': '+3 defensa', 'precio': 40},
    'libro_hechizos': {'nombre': 'Libro de Hechizos', 'efecto': 'habilidades mejoradas', 'precio': 80},
    'mapa_antiguo': {'nombre': 'Mapa Antiguo', 'efecto': 'revele secretos', 'precio': 0},
    'llave_antigua': {'nombre': 'Llave Antigua', 'efecto': 'abre puertas', 'precio': 0}
}

# Enemigos
ENEMIES = {
    'goblin': {'vida': 40, 'ataque': 8, 'defensa': 3, 'exp': 20},
    'orco': {'vida': 70, 'ataque': 12, 'defensa': 6, 'exp': 35},
    'esqueleto': {'vida': 35, 'ataque': 10, 'defensa': 2, 'exp': 25},
    'lobo': {'vida': 30, 'ataque': 9, 'defensa': 1, 'exp': 15},
    'guardia_oscuro': {'vida': 90, 'ataque': 16, 'defensa': 8, 'exp': 50},
    'hechicero_maligno': {'vida': 60, 'ataque': 18, 'defensa': 4, 'exp': 60}
}

# NPCs
NPCS = {
    'aldeano': {
        'nombre': 'Aldeano Anciano',
        'dialogos': [
            "¡Cuidado con el bosque! Dicen que criaturas oscuras merodean por allí...",
            "El viejo castillo en las montañas está maldito. Nadie que entra sale vivo.",
            "He oído que el Sabio del Pueblo sabe cosas sobre la antigua profecía."
        ]
    },
    'sabio': {
        'nombre': 'Sabio Arathorn',
        'dialogos': [
            "La profecía habla de un héroe que restaurará el equilibrio...",
            "Las Ruinas Antiguas esconden secretos del pasado olvidado.",
            "Solo con las tres reliquias podrás enfrentar a la Oscuridad."
        ]
    },
    'comerciante': {
        'nombre': 'Comerciante Gideon',
        'dialogos': [
            "¡Bienvenido a mi tienda! Tengo lo necesario para tu aventura.",
            "He oído que el Amuleto de Protección es muy buscado por los aventureros.",
            "Cuidado con los caminos solitarios, bandidos merodean por ahí."
        ]
    }
}

class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.clase = player_class
        self.nivel = 1
        self.experiencia = 0
        self.vida_max = CLASS_STATS[player_class]['vida']
        self.vida_actual = self.vida_max
        self.mana_max = CLASS_STATS[player_class]['mana']
        self.mana_actual = self.mana_max
        self.ataque = CLASS_STATS[player_class]['ataque']
        self.defensa = CLASS_STATS[player_class]['defensa']
        self.inventario = {}
        self.oro = 100
        self.ubicacion = 'pueblo'
        self.misiones = {
            'principal': 0,  # Progreso de misión principal (0-4)
            'secundarias': {}
        }
        self.reputacion = 50  # 0-100 (0=muy mala, 100=muy buena)
        self.decisiones = []
        self.reliquias_obtenidas = 0  # Para el final (0-3)

    def mostrar_estado(self):
        print(f"\n{Fore.CYAN}=== ESTADO ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}{self.name} - Nivel {self.nivel} {self.clase.capitalize()}{Style.RESET_ALL}")
        print(f"{Fore.RED}Vida: {self.vida_actual}/{self.vida_max}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Mana: {self.mana_actual}/{self.mana_max}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Oro: {self.oro}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Reputación: {self.reputacion}/100{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Ubicación: {self.ubicacion.capitalize()}{Style.RESET_ALL}")

    def subir_nivel(self):
        if self.experiencia >= self.nivel * 100:
            self.nivel += 1
            self.vida_max += 20
            self.vida_actual = self.vida_max
            self.mana_max += 15
            self.mana_actual = self.mana_max
            self.ataque += 3
            self.defensa += 2
            print(f"{Fore.YELLOW}¡Has subido al nivel {self.nivel}!{Style.RESET_ALL}")

def guardar_partida(jugador):
    datos = {
        'nombre': jugador.name,
        'clase': jugador.clase,
        'nivel': jugador.nivel,
        'experiencia': jugador.experiencia,
        'vida_actual': jugador.vida_actual,
        'vida_max': jugador.vida_max,
        'mana_actual': jugador.mana_actual,
        'mana_max': jugador.mana_max,
        'ataque': jugador.ataque,
        'defensa': jugador.defensa,
        'inventario': jugador.inventario,
        'oro': jugador.oro,
        'ubicacion': jugador.ubicacion,
        'misiones': jugador.misiones,
        'reputacion': jugador.reputacion,
        'decisiones': jugador.decisiones,
        'reliquias_obtenidas': jugador.reliquias_obtenidas
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(datos, f)
    print(f"{Fore.GREEN}Partida guardada.{Style.RESET_ALL}")

def cargar_partida():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    return None

def combate(jugador, tipo_enemigo):
    enemigo = ENEMIES[tipo_enemigo]
    vida_enemigo = enemigo['vida']
    
    print(f"\n{Fore.RED}¡COMBATE CONTRA {tipo_enemigo.upper()}!{Style.RESET_ALL}")
    
    while vida_enemigo > 0 and jugador.vida_actual > 0:
        print(f"\n{Fore.WHITE}Tu vida: {jugador.vida_actual}{Style.RESET_ALL}")
        print(f"{Fore.RED}Vida enemigo: {vida_enemigo}{Style.RESET_ALL}")
        
        accion = input(f"\n{Fore.CYAN}1. Atacar  2. Usar item  3. Huir: {Style.RESET_ALL}")
        
        if accion == '1':
            daño = max(1, jugador.ataque - enemigo['defensa'])
            vida_enemigo -= daño
            print(f"{Fore.GREEN}¡Has hecho {daño} de daño!{Style.RESET_ALL}")
        elif accion == '2':
            if jugador.inventario:
                items = list(jugador.inventario.keys())
                print(f"{Fore.YELLOW}Items: {', '.join(items)}{Style.RESET_ALL}")
                item = input("¿Qué item usar? ").lower()
                if item in jugador.inventario:
                    # Lógica simplificada de uso de items
                    print(f"{Fore.GREEN}Has usado {item}{Style.RESET_ALL}")
                    jugador.inventario[item] -= 1
                    if jugador.inventario[item] == 0:
                        del jugador.inventario[item]
                else:
                    print(f"{Fore.RED}No tienes ese item.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No tienes items.{Style.RESET_ALL}")
        elif accion == '3':
            if random.random() < 0.5:
                print(f"{Fore.GREEN}¡Has huido!{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.RED}¡No puedes huir!{Style.RESET_ALL}")
        
        # Turno del enemigo
        if vida_enemigo > 0:
            daño = max(1, enemigo['ataque'] - jugador.defensa)
            jugador.vida_actual -= daño
            print(f"{Fore.RED}¡El enemigo te hace {daño} de daño!{Style.RESET_ALL}")
    
    if jugador.vida_actual <= 0:
        print(f"{Fore.RED}¡Has sido derrotado!{Style.RESET_ALL}")
        jugador.vida_actual = jugador.vida_max // 2
        return False
    else:
        print(f"{Fore.GREEN}¡Victoria!{Style.RESET_ALL}")
        jugador.experiencia += enemigo['exp']
        recompensa = random.randint(10, 30)
        jugador.oro += recompensa
        print(f"{Fore.YELLOW}+{enemigo['exp']} EXP, +{recompensa} oro{Style.RESET_ALL}")
        jugador.subir_nivel()
        return True

def evento_pueblo(jugador):
    print(f"\n{Fore.CYAN}=== PUEBLO DE ALDERA ==={Style.RESET_ALL}")
    print("El pueblo parece tranquilo. La taberna está llena de aventureros.")
    
    opciones = [
        "Hablar con el Aldeano Anciano",
        "Visitar al Sabio Arathorn",
        "Ir a la Tienda de Gideon",
        "Explorar el Bosque",
        "Investigar las Montañas",
        "Descansar en la posada"
    ]
    
    for i, opcion in enumerate(opciones, 1):
        print(f"{Fore.YELLOW}{i}. {opcion}{Style.RESET_ALL}")
    
    try:
        eleccion = int(input(f"\n{Fore.WHITE}¿Qué deseas hacer? {Style.RESET_ALL}"))
        
        if eleccion == 1:
            hablar_con_npc(jugador, 'aldeano')
        elif eleccion == 2:
            hablar_con_npc(jugador, 'sabio')
            if jugador.misiones['principal'] == 0:
                print(f"\n{Fore.CYAN}El Sabio te habla sobre una profecía...{Style.RESET_ALL}")
                print("Debes encontrar las tres reliquias antiguas para restaurar el balance.")
                jugador.misiones['principal'] = 1
        elif eleccion == 3:
            tienda(jugador)
        elif eleccion == 4:
            jugador.ubicacion = 'bosque'
            evento_bosque(jugador)
        elif eleccion == 5:
            if jugador.nivel >= 3:
                jugador.ubicacion = 'montanas'
                evento_montanas(jugador)
            else:
                print(f"{Fore.RED}Las montañas son demasiado peligrosas para tu nivel.{Style.RESET_ALL}")
        elif eleccion == 6:
            jugador.vida_actual = jugador.vida_max
            jugador.mana_actual = jugador.mana_max
            print(f"{Fore.GREEN}Has descansado y recuperado tu energía.{Style.RESET_ALL}")
        
    except ValueError:
        print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")

def hablar_con_npc(jugador, npc_tipo):
    npc = NPCS[npc_tipo]
    print(f"\n{Fore.CYAN}=== {npc['nombre'].upper()} ==={Style.RESET_ALL}")
    
    dialogo = random.choice(npc['dialogos'])
    print(f"{Fore.WHITE}{dialogo}{Style.RESET_ALL}")
    
    if npc_tipo == 'sabio' and jugador.misiones['principal'] > 0:
        print(f"\n{Fore.CYAN}El Sabio te entrega un mapa antiguo.{Style.RESET_ALL}")
        jugador.inventario['mapa_antiguo'] = 1

def tienda(jugador):
    print(f"\n{Fore.CYAN}=== TIENDA DE GIDEON ==={Style.RESET_ALL}")
    items = ['pocion_vida', 'pocion_mana', 'espada_acero', 'armadura_metal']
    
    for i, item_id in enumerate(items, 1):
        item = ITEMS[item_id]
        print(f"{Fore.YELLOW}{i}. {item['nombre']} - {item['precio']} oro ({item['efecto']}){Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}0. Salir{Style.RESET_ALL}")
    
    try:
        opcion = int(input(f"\n{Fore.WHITE}¿Qué deseas comprar? {Style.RESET_ALL}"))
        if opcion == 0:
            return
        
        item_id = items[opcion-1]
        item = ITEMS[item_id]
        
        if jugador.oro >= item['precio']:
            jugador.oro -= item['precio']
            if item_id in jugador.inventario:
                jugador.inventario[item_id] += 1
            else:
                jugador.inventario[item_id] = 1
            print(f"{Fore.GREEN}¡Has comprado {item['nombre']}!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No tienes suficiente oro.{Style.RESET_ALL}")
            
    except (ValueError, IndexError):
        print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")

def evento_bosque(jugador):
    print(f"\n{Fore.GREEN}=== BOSQUE OSCURO ==={Style.RESET_ALL}")
    print("Los árboles forman un dosel denso. Se oyen ruidos extraños...")
    
    eventos = [
        "Encontrar un claro pacífico",
        "Ser atacado por criaturas",
        "Descubrir unas ruinas antiguas",
        "Encontrar un tesoro escondido"
    ]
    
    evento = random.choice(eventos)
    print(f"\n{Fore.CYAN}Evento: {evento}{Style.RESET_ALL}")
    
    if evento == "Encontrar un claro pacífico":
        print("Encuentras un claro con aguas cristalinas. Recuperas salud y mana.")
        jugador.vida_actual = min(jugador.vida_max, jugador.vida_actual + 30)
        jugador.mana_actual = min(jugador.mana_max, jugador.mana_actual + 25)
        
    elif evento == "Ser atacado por criaturas":
        enemigo = random.choice(['goblin', 'lobo', 'esqueleto'])
        if combate(jugador, enemigo):
            print("Después del combate, encuentras algunos objetos útiles.")
            jugador.inventario['pocion_vida'] = jugador.inventario.get('pocion_vida', 0) + 1
            
    elif evento == "Descubrir unas ruinas antiguas":
        print("Encuentras unas ruinas que parecen muy antiguas.")
        if 'mapa_antiguo' in jugador.inventario:
            print("El mapa te guía a una reliquia oculta!")
            jugador.reliquias_obtenidas += 1
            jugador.misiones['principal'] = 2
            print(f"{Fore.YELLOW}¡Has obtenido una reliquia! ({jugador.reliquias_obtenidas}/3){Style.RESET_ALL}")
        else:
            print("Parece haber algo importante, pero necesitas un mapa para entenderlo.")
            
    elif evento == "Encontrar un tesoro escondido":
        oro = random.randint(20, 50)
        jugador.oro += oro
        print(f"{Fore.YELLOW}¡Has encontrado {oro} de oro escondido!{Style.RESET_ALL}")

def evento_montanas(jugador):
    print(f"\n{Fore.BLUE}=== MONTAÑAS ESCARPADAS ==={Style.RESET_ALL}")
    print("El aire es frío y el camino peligroso. Se ven cuevas en las paredes.")
    
    if jugador.misiones['principal'] >= 2:
        print("Sientes que una de las reliquias podría estar aquí...")
        if random.random() < 0.7:
            print("¡Encuentras una segunda reliquia en una cueva oculta!")
            jugador.reliquias_obtenidas += 1
            jugador.misiones['principal'] = 3
            print(f"{Fore.YELLOW}¡Has obtenido otra reliquia! ({jugador.reliquias_obtenidas}/3){Style.RESET_ALL}")
        else:
            print("La cueva está vacía. Quizás en otro lugar...")
    else:
        enemigo = random.choice(['orco', 'guardia_oscuro'])
        if combate(jugador, enemigo):
            print("Explorando las montañas encuentras recursos valiosos.")
            jugador.oro += random.randint(30, 60)

def evento_ruinas(jugador):
    print(f"\n{Fore.MAGENTA}=== RUINAS ANTIGUAS ==={Style.RESET_ALL}")
    print("Las ruinas emanan una energía ancestral. Jeroglíficos cubren las paredes.")
    
    if jugador.misiones['principal'] >= 3:
        print("Sientes la presencia de la reliquia final...")
        decision = input(f"{Fore.CYAN}¿Investigar el altar central? (s/n): {Style.RESET_ALL}")
        
        if decision.lower() == 's':
            if jugador.reputacion >= 70:
                print("La reliquia te acepta como su portador.")
                jugador.reliquias_obtenidas += 1
                jugador.misiones['principal'] = 4
                print(f"{Fore.YELLOW}¡Has obtenido la reliquia final! (3/3){Style.RESET_ALL}")
                print(f"{Fore.CYAN}¡Ahora estás listo para enfrentar el desafío final!{Style.RESET_ALL}")
            else:
                print("La reliquia rechaza tu contacto. Necesitas ser más virtuoso.")
        else:
            print("Decides no tocar el altar por ahora.")
    else:
        print("Las ruinas guardan secretos, pero necesitas más preparación.")

def enfrentamiento_final(jugador):
    print(f"\n{Fore.RED}=== ENFRENTAMIENTO FINAL ==={Style.RESET_ALL}")
    print("Te enfrentas a la encarnación de la Oscuridad...")
    
    if jugador.reliquias_obtenidas == 3:
        print("Las tres reliquias brillan con poder. ¡Estás preparado!")
        if combate(jugador, 'hechicero_maligno'):
            return "victoria"
        else:
            return "derrota"
    else:
        print("No estás preparado. La Oscuridad es demasiado poderosa.")
        return "derrota"

def determinar_final(jugador, resultado_combate):
    print(f"\n{Fore.CYAN}=== FINAL ==={Style.RESET_ALL}")
    
    if resultado_combate == "victoria":
        if jugador.reputacion >= 80:
            print(f"{Fore.GREEN}¡Hétero Legendario!{Style.RESET_ALL}")
            print("Has restaurado el balance y eres recordado como un héroe legendario.")
        elif jugador.reputacion >= 50:
            print(f"{Fore.YELLOW}¡Victoria con Honor!{Style.RESET_ALL}")
            print("Derrotaste a la oscuridad, pero tu camino tuvo sombras y luces.")
        else:
            print(f"{Fore.RED}¡Victoria Amarga!{Style.RESET_ALL}")
            print("Ganaste, pero tus métodos cuestionables dejaron cicatrices en el reino.")
    else:
        print(f"{Fore.RED}¡Caída de la Esperanza!{Style.RESET_ALL}")
        print("La oscuridad prevalece. El mundo cae en la desesperación.")
    
    print(f"\n{Fore.CYAN}Tu aventura ha concluido.{Style.RESET_ALL}")
    print(f"Reliquias obtenidas: {jugador.reliquias_obtenidas}/3")
    print(f"Reputación final: {jugador.reputacion}/100")
    print(f"Nivel alcanzado: {jugador.nivel}")

def main():
    print(f"{Fore.CYAN}=== AVENTURA ÉPICA RPG ==={Style.RESET_ALL}")
    
    # Cargar o nueva partida
    datos_guardados = cargar_partida()
    if datos_guardados:
        cargar = input(f"{Fore.WHITE}¿Cargar partida guardada? (s/n): {Style.RESET_ALL}")
        if cargar.lower() == 's':
            jugador = Player(datos_guardados['nombre'], datos_guardados['clase'])
            # Cargar todos los datos
            for key, value in datos_guardados.items():
                if hasattr(jugador, key):
                    setattr(jugador, key, value)
            print(f"{Fore.GREEN}Partida cargada.{Style.RESET_ALL}")
        else:
            nombre = input(f"{Fore.WHITE}Nombre de tu personaje: {Style.RESET_ALL}")
            print(f"{Fore.CYAN}Elige tu clase:{Style.RESET_ALL}")
            for i, clase in enumerate(CLASS_STATS.keys(), 1):
                print(f"{Fore.YELLOW}{i}. {clase.capitalize()}{Style.RESET_ALL}")
            clase_idx = int(input("Opción: ")) - 1
            clase = list(CLASS_STATS.keys())[clase_idx]
            jugador = Player(nombre, clase)
    else:
        nombre = input(f"{Fore.WHITE}Nombre de tu personaje: {Style.RESET_ALL}")
        print(f"{Fore.CYAN}Elige tu clase:{Style.RESET_ALL}")
        for i, clase in enumerate(CLASS_STATS.keys(), 1):
            print(f"{Fore.YELLOW}{i}. {clase.capitalize()}{Style.RESET_ALL}")
        clase_idx = int(input("Opción: ")) - 1
        clase = list(CLASS_STATS.keys())[clase_idx]
        jugador = Player(nombre, clase)
    
    # Bucle principal del juego
    while True:
        jugador.mostrar_estado()
        
        if jugador.ubicacion == 'pueblo':
            evento_pueblo(jugador)
        elif jugador.ubicacion == 'bosque':
            evento_bosque(jugador)
            jugador.ubicacion = 'pueblo'  # Volver al pueblo después
        elif jugador.ubicacion == 'montanas':
            evento_montanas(jugador)
            jugador.ubicacion = 'pueblo'
        elif jugador.ubicacion == 'ruinas':
            evento_ruinas(jugador)
            jugador.ubicacion = 'pueblo'
        
        # Verificar si está listo para el final
        if jugador.misiones['principal'] == 4:
            decision = input(f"{Fore.RED}¿Estás listo para el enfrentamiento final? (s/n): {Style.RESET_ALL}")
            if decision.lower() == 's':
                resultado = enfrentamiento_final(jugador)
                determinar_final(jugador, resultado)
                break
        
        # Opción de guardar y salir
        opcion = input(f"\n{Fore.CYAN}¿Continuar? (s=si, g=guardar y salir): {Style.RESET_ALL}")
        if opcion.lower() == 'g':
            guardar_partida(jugador)
            print(f"{Fore.YELLOW}¡Hasta pronto!{Style.RESET_ALL}")
            break
        elif opcion.lower() != 's':
            print(f"{Fore.RED}Juego terminado.{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()

