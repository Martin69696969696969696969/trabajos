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

# =====================
# Configuración general
# =====================
SAVE_FILE = 'rpg_save_data.json'

# Sistema de clases y estadísticas
CLASS_STATS = {
    'guerrero': {
        'vida_base': 100,
        'ataque_base': 15,
        'defensa_base': 10,
        'mana_base': 30,
        'habilidades': ['Ataque poderoso', 'Grito de guerra', 'Defensa total']
    },
    'mago': {
        'vida_base': 70,
        'ataque_base': 8,
        'defensa_base': 5,
        'mana_base': 100,
        'habilidades': ['Bola de fuego', 'Rayo eléctrico', 'Curación']
    },
    'explorador': {
        'vida_base': 85,
        'ataque_base': 12,
        'defensa_base': 7,
        'mana_base': 50,
        'habilidades': ['Ataque rápido', 'Sigilo', 'Trampas']
    }
}

# Costes y efectos sencillos de habilidades
HABILIDAD_COSTE = {
    'Bola de fuego': 15,
    'Rayo eléctrico': 20,
    'Curación': 12,
    'Ataque poderoso': 0,
    'Grito de guerra': 0,
    'Defensa total': 0,
    'Ataque rápido': 5,
    'Sigilo': 5,
    'Trampas': 10,
}

# Sistema de items
ITEMS = {
    'pocion_vida': {
        'nombre': 'Poción de Vida',
        'tipo': 'consumible',
        'efecto': lambda p: setattr(p, 'vida_actual', min(p.vida_maxima, p.vida_actual + 30)),
        'descripcion': 'Restaura 30 puntos de vida'
    },
    'pocion_mana': {
        'nombre': 'Poción de Mana',
        'tipo': 'consumible',
        'efecto': lambda p: setattr(p, 'mana_actual', min(p.mana_maxima, p.mana_actual + 25)),
        'descripcion': 'Restaura 25 puntos de mana'
    },
    'espada_hierro': {
        'nombre': 'Espada de Hierro',
        'tipo': 'equipamiento',
        'efecto': lambda p: setattr(p, 'ataque_base', p.ataque_base + 5),
        'descripcion': '+5 de ataque'
    },
    'armadura_cuero': {
        'nombre': 'Armadura de Cuero',
        'tipo': 'equipamiento',
        'efecto': lambda p: setattr(p, 'defensa_base', p.defensa_base + 3),
        'descripcion': '+3 de defensa'
    },
    'espada_acero': {
        'nombre': 'Espada de Acero',
        'tipo': 'equipamiento',
        'efecto': lambda p: setattr(p, 'ataque_base', p.ataque_base + 10),
        'descripcion': '+10 de ataque'
    },
    'armadura_acero': {
        'nombre': 'Armadura de Acero',
        'tipo': 'equipamiento',
        'efecto': lambda p: setattr(p, 'defensa_base', p.defensa_base + 6),
        'descripcion': '+6 de defensa'
    },
    'anillo_mana': {
        'nombre': 'Anillo de Maná',
        'tipo': 'equipamiento',
        'efecto': lambda p: setattr(p, 'mana_maxima', p.mana_maxima + 20) or setattr(p, 'mana_actual', p.mana_actual + 20),
        'descripcion': '+20 de maná máximo'
    },
    'pergamino_curacion': {
        'nombre': 'Pergamino de Curación',
        'tipo': 'consumible',
        'efecto': lambda p: setattr(p, 'vida_actual', min(p.vida_maxima, p.vida_actual + 60)),
        'descripcion': 'Restaura 60 puntos de vida'
    },
    'llave_castillo': {
        'nombre': 'Llave Antigua del Castillo',
        'tipo': 'clave',
        'efecto': lambda p: None,
        'descripcion': 'Abre las puertas del Castillo del Señor Oscuro'
    }
}

# Sistema de enemigos
ENEMIES = {
    'goblin': {
        'nombre': 'Goblin',
        'vida': 40,
        'ataque': 8,
        'defensa': 3,
        'experiencia': 15,
        'loot': ['pocion_vida', 'oro']
    },
    'orco': {
        'nombre': 'Orco',
        'vida': 70,
        'ataque': 12,
        'defensa': 6,
        'experiencia': 25,
        'loot': ['espada_hierro', 'pocion_vida']
    },
    'esqueleto': {
        'nombre': 'Esqueleto',
        'vida': 35,
        'ataque': 10,
        'defensa': 2,
        'experiencia': 18,
        'loot': ['armadura_cuero', 'oro']
    },
    'lobo': {
        'nombre': 'Lobo',
        'vida': 45,
        'ataque': 9,
        'defensa': 3,
        'experiencia': 20,
        'loot': ['pocion_vida', 'pocion_mana']
    },
    'troll': {
        'nombre': 'Troll de Montaña',
        'vida': 120,
        'ataque': 16,
        'defensa': 8,
        'experiencia': 45,
        'loot': ['espada_acero', 'armadura_acero']
    },
    'orco_lider': {
        'nombre': 'Orco Líder (Jefe)',
        'vida': 140,
        'ataque': 18,
        'defensa': 10,
        'experiencia': 60,
        'loot': ['espada_acero', 'oro']
    },
    'caballero_no_muerto': {
        'nombre': 'Caballero No-Muerto (Jefe)',
        'vida': 160,
        'ataque': 20,
        'defensa': 12,
        'experiencia': 80,
        'loot': ['anillo_mana', 'pergamino_curacion']
    },
    'senor_oscuro': {
        'nombre': 'Señor Oscuro (Jefe Final)',
        'vida': 220,
        'ataque': 24,
        'defensa': 14,
        'experiencia': 150,
        'loot': ['oro']
    }
}

# =====================
# Clases del juego
# =====================
class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.experience = 0
        self.vida_maxima = CLASS_STATS[player_class]['vida_base']
        self.vida_actual = self.vida_maxima
        self.mana_maxima = CLASS_STATS[player_class]['mana_base']
        self.mana_actual = self.mana_maxima
        self.ataque_base = CLASS_STATS[player_class]['ataque_base']
        self.defensa_base = CLASS_STATS[player_class]['defensa_base']
        self.inventory = {}
        self.habilidades = CLASS_STATS[player_class]['habilidades']
        self.oro = 50
        self.historial_decisiones = []
        # Progreso de historia
        self.progreso = {
            'montanas_desbloqueadas': False,
            'ruinas_desbloqueadas': False,
            'castillo_desbloqueado': False,
        }
        self.jefes_derrotados = []  # lista de ids de jefes

    # ----------
    # Progresión
    # ----------
    def add_experience(self, exp):
        self.experience += exp
        print(f"{Fore.GREEN}¡Has ganado {exp} puntos de experiencia!{Style.RESET_ALL}")
        while self.experience >= self.experiencia_requerida():
            self.experience -= self.experiencia_requerida()
            self.subir_nivel()

    def experiencia_requerida(self):
        return self.level * 100

    def subir_nivel(self):
        self.level += 1
        self.vida_maxima += 10
        self.mana_maxima += 5
        self.ataque_base += 2
        self.defensa_base += 1
        self.vida_actual = self.vida_maxima
        self.mana_actual = self.mana_maxima
        print_nivel(self)

    # --------
    # Inventario
    # --------
    def add_item(self, item_id, quantity=1):
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

    def use_item(self, item_id):
        if item_id in self.inventory and self.inventory[item_id] > 0:
            item = ITEMS[item_id]
            item['efecto'](self)
            self.inventory[item_id] -= 1
            if self.inventory[item_id] == 0:
                del self.inventory[item_id]
            print(f"{Fore.GREEN}Has usado {item['nombre']}.{Style.RESET_ALL}")
            return True
        print(f"{Fore.RED}No puedes usar ese ítem ahora.{Style.RESET_ALL}")
        return False

    # -------
    # Varios
    # -------
    def mostrar_stats(self):
        print(f"{Fore.CYAN}╔{'═' * 60}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{'ESTADÍSTICAS DEL JUGADOR':^60}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Nombre: {self.name:<25} Nivel: {self.level:<3}{' ' * 20}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Clase: {self.player_class:<23} EXP: {self.experience}/{self.experiencia_requerida():<4}{' ' * 16}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Vida: {self.vida_actual}/{self.vida_maxima:<19} Mana: {self.mana_actual}/{self.mana_maxima:<4}{' ' * 16}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Ataque: {self.ataque_base:<20} Defensa: {self.defensa_base:<4}{' ' * 22}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Oro: {self.oro:<26}{' ' * 30}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Progreso: Montañas={'Sí' if self.progreso['montanas_desbloqueadas'] else 'No'} | Ruinas={'Sí' if self.progreso['ruinas_desbloqueadas'] else 'No'} | Castillo={'Sí' if self.progreso['castillo_desbloqueado'] else 'No'}{' ' * 2}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 60}╝{Style.RESET_ALL}")

    def save(self):
        return {
            'name': self.name,
            'class': self.player_class,
            'level': self.level,
            'experience': self.experience,
            'vida_maxima': self.vida_maxima,
            'vida_actual': self.vida_actual,
            'mana_maxima': self.mana_maxima,
            'mana_actual': self.mana_actual,
            'ataque_base': self.ataque_base,
            'defensa_base': self.defensa_base,
            'inventory': self.inventory,
            'oro': self.oro,
            'historial_decisiones': self.historial_decisiones,
            'progreso': self.progreso,
            'jefes_derrotados': self.jefes_derrotados
        }

# =====================
# Utilidades de impresión
# =====================
def print_titulo():
    print(f"{Fore.MAGENTA}{'*' * 70}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}*{' ':^68}*{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}*{Fore.CYAN}{'REINO DE ELDORIA':^68}{Fore.MAGENTA}*{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}*{Fore.YELLOW}{'Una aventura épica RPG':^68}{Fore.MAGENTA}*{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}*{' ':^68}*{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{'*' * 70}{Style.RESET_ALL}")

def print_nivel(player):
    print(f"{Fore.YELLOW}╔{'═' * 50}╗{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{' ' * 20}{Fore.CYAN}¡NIVEL {player.level}!{' ' * 20}{Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{' ' * 50}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Fore.WHITE} Vida: {player.vida_maxima}{' ' * 40}{Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Fore.WHITE} Mana: {player.mana_maxima}{' ' * 40}{Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Fore.WHITE} Ataque: {player.ataque_base}{' ' * 38}{Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}║{Fore.WHITE} Defensa: {player.defensa_base}{' ' * 38}{Fore.YELLOW}║{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}╚{'═' * 50}╝{Style.RESET_ALL}")

# =====================
# Guardado / Carga
# =====================
def cargar_partida():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception:
            print(f"{Fore.RED}Error al cargar la partida.{Style.RESET_ALL}")
            return {}
    return {}

def guardar_partida(player):
    data = player.save()
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{Fore.GREEN}Partida guardada correctamente.{Style.RESET_ALL}")

# =====================
# Combate
# =====================
def calcular_dano_jugador(player, enemy):
    base = max(1, player.ataque_base - enemy['defensa'] // 2)
    return random.randint(max(1, base - 2), base + 2)

def calcular_dano_enemigo(player, enemy):
    base = max(1, enemy['ataque'] - player.defensa_base // 2)
    return random.randint(max(1, base - 2), base + 2)

def usar_habilidad(player, enemy, enemy_vida):
    print(f"\n{Fore.CYAN}Habilidades disponibles:{Style.RESET_ALL}")
    for i, habilidad in enumerate(player.habilidades, 1):
        coste = HABILIDAD_COSTE.get(habilidad, 0)
        print(f"{Fore.YELLOW}{i}. {habilidad} (Coste: {coste} MP){Style.RESET_ALL}")

    try:
        idx = int(input(f"{Fore.WHITE}Elige una habilidad (1-{len(player.habilidades)}): {Style.RESET_ALL}"))
    except ValueError:
        print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
        return enemy_vida

    if not (1 <= idx <= len(player.habilidades)):
        print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
        return enemy_vida

    habilidad = player.habilidades[idx - 1]
    coste = HABILIDAD_COSTE.get(habilidad, 0)
    if player.mana_actual < coste:
        print(f"{Fore.RED}No tienes suficiente maná.{Style.RESET_ALL}")
        return enemy_vida

    # Aplicar efectos sencillos por clase/habilidad
    if habilidad in ('Bola de fuego', 'Rayo eléctrico'):
        dano = random.randint(12, 24) if habilidad == 'Bola de fuego' else random.randint(15, 28)
        enemy_vida -= dano
        print(f"{Fore.BLUE}¡Lanzas {habilidad} e infliges {dano} de daño mágico!{Style.RESET_ALL}")
    elif habilidad == 'Curación':
        cura = random.randint(25, 45)
        antes = player.vida_actual
        player.vida_actual = min(player.vida_maxima, player.vida_actual + cura)
        print(f"{Fore.GREEN}Te curas {player.vida_actual - antes} puntos de vida.{Style.RESET_ALL}")
    elif habilidad == 'Ataque poderoso':
        dano = random.randint(10, 18)
        enemy_vida -= dano
        print(f"{Fore.RED}¡Descargas un golpe demoledor por {dano} de daño!{Style.RESET_ALL}")
    elif habilidad == 'Grito de guerra':
        player.ataque_base += 2
        print(f"{Fore.YELLOW}Tu ataque aumenta temporalmente (+2).{Style.RESET_ALL}")
    elif habilidad == 'Defensa total':
        player.defensa_base += 2
        print(f"{Fore.YELLOW}Refuerzas tu defensa temporalmente (+2).{Style.RESET_ALL}")
    elif habilidad == 'Ataque rápido':
        total = 0
        for _ in range(2):
            golpe = random.randint(6, 10)
            total += golpe
        enemy_vida -= total
        print(f"{Fore.GREEN}¡Golpeas dos veces por {total} de daño!{Style.RESET_ALL}")
    elif habilidad == 'Sigilo':
        print(f"{Fore.CYAN}Te ocultas... tu próximo ataque será más certero (+50% daño).{Style.RESET_ALL}")
        player.ataque_base += max(1, player.ataque_base // 2)
    elif habilidad == 'Trampas':
        dano = random.randint(8, 16)
        enemy_vida -= dano
        print(f"{Fore.YELLOW}Activas una trampa que causa {dano} de daño.{Style.RESET_ALL}")

    player.mana_actual -= coste
    return enemy_vida

def combate(player, enemy_type):
    enemy = ENEMIES[enemy_type]
    enemy_vida = enemy['vida']

    print(f"\n{Fore.RED}╔{'═' * 60}╗{Style.RESET_ALL}")
    print(f"{Fore.RED}║{'COMBATE':^60}{Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}╠{'═' * 60}╣{Style.RESET_ALL}")
    print(f"{Fore.RED}║ {Fore.WHITE}Te enfrentas a: {Fore.YELLOW}{enemy['nombre']:<43}{Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}╚{'═' * 60}╝{Style.RESET_ALL}")

    turno = 0
    while enemy_vida > 0 and player.vida_actual > 0:
        turno += 1
        print(f"\n{Fore.YELLOW}— Turno {turno} —{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Tu vida: {player.vida_actual}/{player.vida_maxima} | Maná: {player.mana_actual}/{player.mana_maxima}{Style.RESET_ALL}")
        print(f"{Fore.RED}Vida del enemigo: {enemy_vida}/{enemy['vida']}{Style.RESET_ALL}")

        # Turno del jugador
        print(f"\n{Fore.CYAN}¿Qué deseas hacer?{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}1. Atacar{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}2. Usar habilidad{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}3. Usar item{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}4. Intentar huir{Style.RESET_ALL}")

        accion = input(f"{Fore.WHITE}Elige una opción (1-4): {Style.RESET_ALL}").strip()

        if accion == '1':
            danio = calcular_dano_jugador(player, enemy)
            enemy_vida -= danio
            print(f"{Fore.GREEN}¡Has infligido {danio} puntos de daño!{Style.RESET_ALL}")
        elif accion == '2':
            enemy_vida = usar_habilidad(player, enemy, enemy_vida)
        elif accion == '3':
            if player.inventory:
                print(f"\n{Fore.CYAN}Items disponibles:{Style.RESET_ALL}")
                items_list = list(player.inventory.keys())
                for i, item_id in enumerate(items_list, 1):
                    print(f"{Fore.YELLOW}{i}. {ITEMS[item_id]['nombre']} x{player.inventory[item_id]}{Style.RESET_ALL}")
                try:
                    item_opcion = int(input(f"{Fore.WHITE}Elige un item (1-{len(items_list)}): {Style.RESET_ALL}"))
                    if 1 <= item_opcion <= len(items_list):
                        item_id = items_list[item_opcion - 1]
                        player.use_item(item_id)
                    else:
                        print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}No tienes items en tu inventario.{Style.RESET_ALL}")
        elif accion == '4':
            if random.random() < 0.35:
                print(f"{Fore.GREEN}¡Has huido exitosamente!{Style.RESET_ALL}")
                return False
            else:
                print(f"{Fore.RED}¡No has logrado huir!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Opción inválida. Pierdes tu turno.{Style.RESET_ALL}")

        # Turno del enemigo si sigue vivo
        if enemy_vida > 0:
            danio_enemigo = calcular_dano_enemigo(player, enemy)
            player.vida_actual -= danio_enemigo
            print(f"{Fore.RED}¡{enemy['nombre']} te inflige {danio_enemigo} puntos de daño!{Style.RESET_ALL}")

    # Resultado del combate
    if player.vida_actual <= 0:
        print(f"\n{Fore.RED}╔{'═' * 60}╗{Style.RESET_ALL}")
        print(f"{Fore.RED}║{'HAS SIDO DERROTADO':^60}{Fore.RED}║{Style.RESET_ALL}")
        print(f"{Fore.RED}╚{'═' * 60}╝{Style.RESET_ALL}")
        player.vida_actual = max(1, player.vida_maxima // 4)
        return False
    else:
        print(f"\n{Fore.GREEN}╔{'═' * 60}╗{Style.RESET_ALL}")
        print(f"{Fore.GREEN}║{'¡VICTORIA!':^60}{Fore.GREEN}║{Style.RESET_ALL}")
        print(f"{Fore.GREEN}╚{'═' * 60}╝{Style.RESET_ALL}")
        exp_ganada = enemy['experiencia']
        player.add_experience(exp_ganada)
        # Loot
        if random.random() < 0.75:
            loot = random.choice(enemy['loot'])
            if loot == 'oro':
                oro_ganado = random.randint(10, 30)
                player.oro += oro_ganado
                print(f"{Fore.YELLOW}¡Has obtenido {oro_ganado} piezas de oro!{Style.RESET_ALL}")
            else:
                player.add_item(loot)
                print(f"{Fore.GREEN}¡Has obtenido {ITEMS[loot]['nombre']}!{Style.RESET_ALL}")
        return True

# =====================
# Aventuras / Zonas
# =====================
def aventura_bosque(player):
    print(f"\n{Fore.GREEN}Te adentras en el Bosque Oscuro...{Style.RESET_ALL}")
    time.sleep(1)
    print(f"{Fore.GREEN}Los árboles susurran secretos antiguos mientras avanzas entre la espesura.{Style.RESET_ALL}")

    decisiones = [
        "Seguir el camino principal",
        "Explorar un claro cercano",
        "Investigar ruidos extraños",
        "Retar al Orco Líder (Jefe)",
        "Regresar al pueblo"
    ]

    print(f"\n{Fore.CYAN}¿Qué deseas hacer?{Style.RESET_ALL}")
    for i, decision in enumerate(decisiones, 1):
        print(f"{Fore.YELLOW}{i}. {decision}{Style.RESET_ALL}")

    opcion = leer_opcion(1, len(decisiones))
    player.historial_decisiones.append(f"Bosque - Opción {opcion}")

    if opcion == 1:
        print(f"\n{Fore.GREEN}Sigues el camino y encuentras un pequeño tesoro escondido.{Style.RESET_ALL}")
        player.add_item('pocion_vida', 2)
        oro = random.randint(10, 20)
        player.oro += oro
        print(f"{Fore.YELLOW}Obtienes {oro} de oro.{Style.RESET_ALL}")
        player.progreso['montanas_desbloqueadas'] = True
        print(f"{Fore.CYAN}Se ha desbloqueado el camino a las Montañas Heladas.{Style.RESET_ALL}")
    elif opcion == 2:
        print(f"\n{Fore.GREEN}En el claro, encuentras un lago cristalino con aguas curativas.{Style.RESET_ALL}")
        player.vida_actual = player.vida_maxima
        player.mana_actual = player.mana_maxima
        print(f"{Fore.BLUE}¡Tu vida y maná han sido restaurados por completo!{Style.RESET_ALL}")
    elif opcion == 3:
        print(f"\n{Fore.RED}¡Los ruidos resultan ser un grupo de goblins!{Style.RESET_ALL}")
        if combate(player, 'goblin'):
            print(f"{Fore.GREEN}Después del combate, encuentras algo de valor en los restos.{Style.RESET_ALL}")
            player.add_item('armadura_cuero')
            player.progreso['montanas_desbloqueadas'] = True
            print(f"{Fore.CYAN}Se ha desbloqueado el camino a las Montañas Heladas.{Style.RESET_ALL}")
    elif opcion == 4:
        print(f"\n{Fore.RED}¡Te internas en la guarida del Orco Líder!{Style.RESET_ALL}")
        if combate(player, 'orco_lider'):
            player.jefes_derrotados.append('orco_lider')
            player.progreso['montanas_desbloqueadas'] = True
            print(f"{Fore.CYAN}Al derrotarlo, descubres un mapa hacia las Montañas Heladas.{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}Regresas al pueblo a reagruparte.{Style.RESET_ALL}")

    return True


def aventura_montanas(player):
    if not player.progreso['montanas_desbloqueadas']:
        print(f"{Fore.RED}Aún no conoces el camino hacia las Montañas Heladas.{Style.RESET_ALL}")
        return True

    print(f"\n{Fore.CYAN}Subes por los senderos helados de las Montañas...{Style.RESET_ALL}")
    time.sleep(1)
    evento = random.choice(['lobo', 'troll', 'tesoro'])

    if evento == 'lobo':
        print(f"{Fore.RED}¡Un lobo hambriento aparece!{Style.RESET_ALL}")
        combate(player, 'lobo')
    elif evento == 'troll':
        print(f"{Fore.RED}¡Un troll de las montañas bloquea el paso!{Style.RESET_ALL}")
        if combate(player, 'troll'):
            print(f"{Fore.GREEN}Has derrotado al troll. Encuentras un sendero oculto hacia unas ruinas antiguas.{Style.RESET_ALL}")
            player.progreso['ruinas_desbloqueadas'] = True
    else:
        print(f"{Fore.YELLOW}Encuentras una cueva con un cofre bien conservado.{Style.RESET_ALL}")
        loot = random.choice(['pocion_mana', 'pergamino_curacion', 'oro'])
        if loot == 'oro':
            oro = random.randint(20, 40)
            player.oro += oro
            print(f"{Fore.YELLOW}¡Obtienes {oro} de oro!{Style.RESET_ALL}")
        else:
            player.add_item(loot)
            print(f"{Fore.GREEN}¡Obtienes {ITEMS[loot]['nombre']}!{Style.RESET_ALL}")

    return True


def aventura_ruinas(player):
    if not player.progreso['ruinas_desbloqueadas']:
        print(f"{Fore.RED}No has descubierto aún la ubicación de las Ruinas Antiguas.{Style.RESET_ALL}")
        return True

    print(f"\n{Fore.MAGENTA}Exploras las Ruinas Antiguas, llenas de trampas y ecos del pasado...{Style.RESET_ALL}")
    time.sleep(1)

    print(f"{Fore.CYAN}Encuentras una sala con inscripciones y dos pasillos.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. Pasillo con antorchas apagadas{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Pasillo con estatuas de caballeros{Style.RESET_ALL}")

    eleccion = leer_opcion(1, 2)
    player.historial_decisiones.append(f"Ruinas - Opción {eleccion}")

    if eleccion == 1:
        print(f"{Fore.RED}¡Una trampa! Flechas salen de las paredes.{Style.RESET_ALL}")
        danio = random.randint(8, 18)
        player.vida_actual = max(1, player.vida_actual - danio)
        print(f"{Fore.RED}Recibes {danio} de daño.{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Un esqueleto guardián aparece.{Style.RESET_ALL}")
        combate(player, 'esqueleto')
    else:
        print(f"{Fore.WHITE}Una de las estatuas cobra vida: ¡el Caballero No-Muerto!{Style.RESET_ALL}")
        if combate(player, 'caballero_no_muerto'):
            player.jefes_derrotados.append('caballero_no_muerto')
            print(f"{Fore.YELLOW}En su sarcófago, encuentras una {ITEMS['llave_castillo']['nombre']}.{Style.RESET_ALL}")
            player.add_item('llave_castillo')
            player.progreso['castillo_desbloqueado'] = True

    return True


def aventura_castillo(player):
    if not player.progreso['castillo_desbloqueado']:
        print(f"{Fore.RED}No conoces aún la ubicación del Castillo del Señor Oscuro.{Style.RESET_ALL}")
        return True

    print(f"\n{Fore.RED}¡Te presentas ante las puertas del Castillo del Señor Oscuro!{Style.RESET_ALL}")
    if 'llave_castillo' not in player.inventory:
        print(f"{Fore.RED}Las puertas están cerradas con una magia antigua. Necesitas la llave.{Style.RESET_ALL}")
        return True

    print(f"{Fore.WHITE}La llave brilla y las puertas se abren lentamente...{Style.RESET_ALL}")
    time.sleep(1)

    # Encuentro previo aleatorio
    if random.random() < 0.5:
        print(f"{Fore.RED}Un grupo de guardianes se interpone en tu camino.{Style.RESET_ALL}")
        combate(player, 'esqueleto')

    print(f"{Fore.MAGENTA}Al ascender a la torre más alta, una oscuridad palpable te rodea...{Style.RESET_ALL}")
    time.sleep(1)
    print(f"{Fore.RED}¡El Señor Oscuro aparece envuelto en sombras!{Style.RESET_ALL}")

    if combate(player, 'senor_oscuro'):
        player.jefes_derrotados.append('senor_oscuro')
        final_epico(player)

    return True

# =====================
# Finales
# =====================
def final_epico(player):
    print(f"\n{Fore.YELLOW}Tras una ardua batalla, la oscuridad comienza a disiparse...{Style.RESET_ALL}")

    # Determinar final según decisiones y jefes
    heroico = ('Bosque - Opción 2' in player.historial_decisiones) or ('Ruinas - Opción 2' in player.historial_decisiones)
    tragico = ('Bosque - Opción 3' in player.historial_decisiones) and ('orco_lider' not in player.jefes_derrotados)

    if heroico:
        print(f"{Fore.GREEN}Tu compasión y valentía inspiran a Eldoria. El pueblo te proclama Héroe del Reino.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Rey y consejo ofrecen un puesto como Protector de las Fronteras.{Style.RESET_ALL}")
    elif tragico:
        print(f"{Fore.RED}El poder oscuro te susurra promesas... y cedes. Te coronas como el nuevo Señor Oscuro.{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Eldoria cae en una noche eterna. Tu nombre será temido por generaciones.{Style.RESET_ALL}")
    else:
        print(f"{Fore.WHITE}Has cumplido con tu misión. Vuelves al pueblo en silencio, como un aventurero más.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Quizá la historia de Eldoria continúe en otra canción de bardo...{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}— FIN —{Style.RESET_ALL}")

# =====================
# Gestión de inventario y tienda
# =====================
def gestionar_inventario(player):
    while True:
        print(f"\n{Fore.CYAN}╔{'═' * 50}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{'INVENTARIO':^50}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 50}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Oro: {player.oro:<43}{Fore.CYAN}║{Style.RESET_ALL}")

        if player.inventory:
            keys = list(player.inventory.keys())
            for i, item_id in enumerate(keys, 1):
                nombre_item = ITEMS[item_id]['nombre']
                print(f"{Fore.CYAN}║ {Fore.YELLOW}{i}. {nombre_item:<30} x{player.inventory[item_id]:<10}{Fore.CYAN}║{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}║ {Fore.RED}El inventario está vacío{' ' * 25}{Fore.CYAN}║{Style.RESET_ALL}")

        print(f"{Fore.CYAN}╠{'═' * 50}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}1. Usar item{' ' * 38}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}2. Volver{' ' * 40}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 50}╝{Style.RESET_ALL}")

        opcion = input(f"{Fore.WHITE}Elige una opción: {Style.RESET_ALL}").strip()
        if opcion == '2':
            break
        elif opcion == '1' and player.inventory:
            items_list = list(player.inventory.keys())
            for i, item_id in enumerate(items_list, 1):
                print(f"{Fore.YELLOW}{i}. {ITEMS[item_id]['nombre']}{Style.RESET_ALL}")
            try:
                item_opcion = int(input(f"{Fore.WHITE}Elige un item para usar: {Style.RESET_ALL}"))
                if 1 <= item_opcion <= len(items_list):
                    item_id = items_list[item_opcion - 1]
                    player.use_item(item_id)
                else:
                    print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")


def tienda(player):
    items_tienda = {
        'pocion_vida': 15,
        'pocion_mana': 12,
        'pergamino_curacion': 30,
        'espada_hierro': 50,
        'armadura_cuero': 40,
        'espada_acero': 90,
        'armadura_acero': 80,
        'anillo_mana': 70
    }

    while True:
        print(f"\n{Fore.CYAN}╔{'═' * 50}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{'TIENDA DEL PUEBLO':^50}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 50}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.WHITE}Tu oro: {player.oro:<41}{Fore.CYAN}║{Style.RESET_ALL}")

        for i, (item_id, precio) in enumerate(items_tienda.items(), 1):
            nombre = ITEMS[item_id]['nombre']
            print(f"{Fore.CYAN}║ {Fore.YELLOW}{i}. {nombre:<30} {precio:<3} oro{' ' * 8}{Fore.CYAN}║{Style.RESET_ALL}")

        print(f"{Fore.CYAN}╠{'═' * 50}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}0. Salir de la tienda{' ' * 28}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 50}╝{Style.RESET_ALL}")

        try:
            opcion = int(input(f"{Fore.WHITE}Elige un item para comprar (0 para salir): {Style.RESET_ALL}"))
            if opcion == 0:
                break
            elif 1 <= opcion <= len(items_tienda):
                items_list = list(items_tienda.keys())
                item_id = items_list[opcion - 1]
                precio = items_tienda[item_id]
                if player.oro >= precio:
                    player.oro -= precio
                    player.add_item(item_id)
                    print(f"{Fore.GREEN}¡Has comprado {ITEMS[item_id]['nombre']}!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}No tienes suficiente oro.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")

# =====================
# Menú principal
# =====================
def menu_principal(player):
    while True:
        print(f"\n{Fore.CYAN}╔{'═' * 60}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{'MENÚ PRINCIPAL':^60}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╠{'═' * 60}╣{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}1. Aventurarse en el Bosque Oscuro{' ' * 25}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}2. Viajar a las Montañas Heladas{' ' * 26}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}3. Explorar las Ruinas Antiguas{' ' * 27}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}4. Asaltar el Castillo del Señor Oscuro{' ' * 20}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}5. Ver estadísticas{' ' * 40}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}6. Gestionar inventario{' ' * 36}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}7. Visitar la tienda{' ' * 39}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}8. Guardar partida{' ' * 41}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║ {Fore.YELLOW}9. Salir del juego{' ' * 41}{Fore.CYAN}║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 60}╝{Style.RESET_ALL}")

        opcion = input(f"{Fore.WHITE}Elige una opción: {Style.RESET_ALL}").strip()

        if opcion == '1':
            aventura_bosque(player)
        elif opcion == '2':
            aventura_montanas(player)
        elif opcion == '3':
            aventura_ruinas(player)
        elif opcion == '4':
            aventura_castillo(player)
        elif opcion == '5':
            player.mostrar_stats()
        elif opcion == '6':
            gestionar_inventario(player)
        elif opcion == '7':
            tienda(player)
        elif opcion == '8':
            guardar_partida(player)
        elif opcion == '9':
            print(f"{Fore.YELLOW}¡Hasta pronto, {player.name}!{Style.RESET_ALL}")
            return False
        else:
            print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")

        input(f"\n{Fore.WHITE}Presiona Enter para continuar...{Style.RESET_ALL}")

# =====================
# Creación y arranque
# =====================
def registrar_jugador():
    print(f"\n{Fore.CYAN}CREACIÓN DE PERSONAJE{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'═' * 40}{Style.RESET_ALL}")

    nombre = input(f"{Fore.WHITE}Ingresa tu nombre: {Style.RESET_ALL}").strip()
    while not nombre:
        nombre = input(f"{Fore.RED}El nombre no puede estar vacío: {Style.RESET_ALL}").strip()

    print(f"\n{Fore.CYAN}Elige tu clase:{Style.RESET_ALL}")
    clases = list(CLASS_STATS.keys())
    for i, clase in enumerate(clases, 1):
        stats = CLASS_STATS[clase]
        print(f"{Fore.YELLOW}{i}. {clase.capitalize():<12} - Vida: {stats['vida_base']} | Ataque: {stats['ataque_base']} | Defensa: {stats['defensa_base']} | Maná: {stats['mana_base']}{Style.RESET_ALL}")

    while True:
        try:
            opcion = int(input(f"\n{Fore.WHITE}Selecciona una clase (1-{len(clases)}): {Style.RESET_ALL}"))
            if 1 <= opcion <= len(clases):
                clase_elegida = clases[opcion - 1]
                break
            else:
                print(f"{Fore.RED}Opción inválida. Intenta de nuevo.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Por favor, ingresa un número.{Style.RESET_ALL}")

    return Player(nombre, clase_elegida)


def mostrar_titulo():
    print_titulo()


def leer_opcion(min_v, max_v):
    while True:
        try:
            opcion = int(input(f"{Fore.WHITE}Elige una opción ({min_v}-{max_v}): {Style.RESET_ALL}"))
            if min_v <= opcion <= max_v:
                return opcion
            else:
                print(f"{Fore.RED}Opción inválida.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Por favor, ingresa un número.{Style.RESET_ALL}")


def main():
    mostrar_titulo()

    # Cargar partida existente
    partida_guardada = cargar_partida()

    if partida_guardada:
        print(f"\n{Fore.CYAN}Partida guardada encontrada:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Jugador: {partida_guardada.get('name','?')} - Nivel {partida_guardada.get('level',1)}{Style.RESET_ALL}")
        cargar = input(f"{Fore.WHITE}¿Deseas cargar esta partida? (s/n): {Style.RESET_ALL}").lower().strip()
        if cargar == 's':
            player = Player(partida_guardada['name'], partida_guardada['class'])
            # Cargar datos
            player.level = partida_guardada.get('level', 1)
            player.experience = partida_guardada.get('experience', 0)
            player.vida_maxima = partida_guardada.get('vida_maxima', player.vida_maxima)
            player.vida_actual = partida_guardada.get('vida_actual', player.vida_maxima)
            player.mana_maxima = partida_guardada.get('mana_maxima', player.mana_maxima)
            player.mana_actual = partida_guardada.get('mana_actual', player.mana_maxima)
            player.ataque_base = partida_guardada.get('ataque_base', player.ataque_base)
            player.defensa_base = partida_guardada.get('defensa_base', player.defensa_base)
            player.inventory = partida_guardada.get('inventory', {})
            player.oro = partida_guardada.get('oro', 50)
            player.historial_decisiones = partida_guardada.get('historial_decisiones', [])
            player.progreso = partida_guardada.get('progreso', player.progreso)
            player.jefes_derrotados = partida_guardada.get('jefes_derrotados', [])
            print(f"{Fore.GREEN}¡Partida cargada exitosamente!{Style.RESET_ALL}")
        else:
            player = registrar_jugador()
    else:
        player = registrar_jugador()

    print(f"\n{Fore.GREEN}¡Bienvenido a Eldoria, {player.name} el {player.player_class}!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Tu aventura comienza ahora...{Style.RESET_ALL}")

    jugando = True
    while jugando:
        jugando = menu_principal(player)

    # Guardar al salir
    guardar_opcion = input(f"{Fore.WHITE}¿Deseas guardar antes de salir? (s/n): {Style.RESET_ALL}").lower().strip()
    if guardar_opcion == 's':
        guardar_partida(player)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Juego interrumpido.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error inesperado: {e}{Style.RESET_ALL}")
    finally:
        if COLORAMA_AVAILABLE:
            print(Style.RESET_ALL)
