import pygame
import random
import time
# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Combate RPG")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (180, 180, 180)
DARK_GRAY = (150, 150, 150)
STAT_BG = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Fuente para los textos
font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 24)

# Fondo (color o imagen)
background_color = (100, 150, 250)  # Azul cielo
background_image = None  # Se puede asignar una imagen aquí

# Configuración de personajes y columnas
player_size = (80, 80)
column_width = 200
column_height = 400
column1_x = (WIDTH // 4) - (column_width // 2)
column2_x = (3 * WIDTH // 4) - (column_width // 2)
player1_base_pos = (column1_x + (column_width - player_size[0]) // 2, HEIGHT // 4 - player_size[1] // 3)
player2_base_pos = (column2_x + (column_width - player_size[0]) // 2, HEIGHT // 4 - player_size[1] // 3)

# Submenú de ataques
submenu_width = 180
submenu_height = 0  # Se calculará dinámicamente
submenu_active = False
submenu_pos = None
current_attacks = []

# Mensajes
message = ""
message_time = 0

# Botones
button_width, button_height = 100, 40
button1_pos = (column1_x + (column_width - button_width) // 2, HEIGHT // 4 + column_height // 2)
button2_pos = (column2_x + (column_width - button_width) // 2, HEIGHT // 4 + column_height // 2)

batalla_actual = 1
victorias = 0
juego_activo = True
turno_jugador = True  # Comienza el jugador con más velocidad
ultimo_turno = time.time()
delay_turno = 1.0  # Segundos entre turnos

# Clases del juego
class Ataque:
    def __init__(self, nombre: str, tipo: str, puntos_daño: int, 
                 razas_vulnerables: list[str], razas_resistentes: list[str],
                 anim_index: int = 0):  # Nuevo parámetro para índice de animación
        if tipo not in ['corte', 'contundente', 'blaster']:
            raise ValueError("Tipo de ataque debe ser 'corte', 'contundente' o 'blaster'")
        if not (50 <= puntos_daño <= 100):
            raise ValueError("Puntos de daño deben estar entre 50 y 100")
            
        self.nombre = nombre
        self.tipo = tipo
        self.puntos_daño = puntos_daño
        self.razas_vulnerables = razas_vulnerables
        self.razas_resistentes = razas_resistentes
        self.anim_index = anim_index  # Índice de animación asociada

    def __str__(self):
        return f"{self.nombre} ({self.tipo}): {self.puntos_daño} daño"

class Personaje:
    MAX_ATAQUES = 4
    
    def __init__(self, nombre: str, raza: str, nivel: int, vida: int, velocidad: int):
        if not (1 <= nivel <= 100):
            raise ValueError("Nivel debe estar entre 1 y 100")
        if not (50 <= vida <= 100):
            raise ValueError("Vida debe estar entre 50 y 100")
        if not (1 <= velocidad <= 100):
            raise ValueError("Velocidad debe estar entre 1 y 100")
            
        self.nombre = nombre
        self.raza = raza
        self.nivel = nivel
        self.vida_maxima = vida
        self.vida_actual = vida
        self.velocidad = velocidad
        self.ataques = []
        self.contador_ataques = 0
        self.es_jugador = False  # Por defecto es CPU

    def agregar_ataque(self, ataque: Ataque):
        if self.contador_ataques >= self.MAX_ATAQUES:
            raise ValueError(f"No se pueden añadir más de {self.MAX_ATAQUES} ataques")
        self.ataques.append(ataque)
        self.contador_ataques += 1

    def recibir_daño(self, cantidad: int):
        self.vida_actual = max(0, self.vida_actual - cantidad)
        return self.vida_actual > 0  # Devuelve True si sigue vivo

    def elegir_ataque(self):
        """Elige un ataque aleatorio para la CPU"""
        if not self.ataques:
            return None
        return random.choice(self.ataques)

    def __str__(self):
        return (f"{self.nombre} ({self.raza}) - Nivel {self.nivel}\n"
                f"Vida: {self.vida_actual}/{self.vida_maxima} | Velocidad: {self.velocidad}\n"
                f"Ataques: {', '.join(a.nombre for a in self.ataques)}")

# Crear ataques disponibles
ataques_disponibles = [
    Ataque("Espada Santa", "corte", 80, ["no-muerto", "demonio"], ["robot", "dragón"], 0),
    Ataque("Martillo Justicia", "contundente", 75, ["demonio", "vampiro"], ["golem", "elemental"], 1),
    Ataque("Rayo Láser", "blaster", 90, ["robot", "humano"], ["fantasma", "espíritu"], 2),
    Ataque("Garra Demoníaca", "corte", 85, ["ángel", "humano"], ["demonio", "no-muerto"], 0),
    Ataque("Bola de Fuego", "blaster", 95, ["planta", "hielo"], ["dragón", "fuego"], 2),
    Ataque("Golpe Trueno", "contundente", 70, ["agua", "máquina"], ["tierra", "roca"], 1),
    Ataque("Flecha Veneno", "corte", 65, ["humano", "bestia"], ["no-muerto", "máquina"], 3),
    Ataque("Canto Sirena", "blaster", 60, ["humano", "demonio"], ["robot", "no-muerto"], 2)
]

# Animaciones básicas (puedes reemplazarlas con sprites más adelante)
animaciones_ataque = [
    # Animación 0: Golpe básico (cuadrado amarillo que aparece y desaparece)
    [pygame.Surface((50, 50)) for _ in range(4)],
    
    # Animación 1: Rayo (línea vertical azul)
    [pygame.Surface((20, 80)) for _ in range(4)],
    
    # Animación 2: Explosión (círculo rojo que crece)
    [pygame.Surface((60, 60), pygame.SRCALPHA) for _ in range(4)],
    
    # Animación 3: Corte (media luna blanca)
    [pygame.Surface((60, 60), pygame.SRCALPHA) for _ in range(4)]
]

# Configurar las animaciones básicas
for i in range(4):
    # Animación 0: Golpe básico
    animaciones_ataque[0][i].fill(YELLOW)
    
    # Animación 1: Rayo
    animaciones_ataque[1][i].fill(BLUE)
    
    # Animación 2: Explosión (círculo rojo)
    pygame.draw.circle(animaciones_ataque[2][i], (255, 0, 0, 200), (30, 30), 10 + i*5)
    
    # Animación 3: Corte (media luna)
    pygame.draw.arc(animaciones_ataque[3][i], WHITE, (0, 0, 60, 60), 0, 3.14, 5)

# Crear personajes disponibles
razas_disponibles = ["humano", "elfo", "enano", "no-muerto", "demonio", "robot", "bestia", "dragón"]
personajes_disponibles = [
    Personaje("Sir Galad", "humano", random.randint(30, 70), random.randint(70, 100), random.randint(50, 90)),
    Personaje("Thorin", "enano", random.randint(40, 80), random.randint(80, 100), random.randint(30, 70)),
    Personaje("Legolas", "elfo", random.randint(50, 90), random.randint(60, 90), random.randint(70, 100)),
    Personaje("Necron", "no-muerto", random.randint(60, 100), random.randint(50, 90), random.randint(40, 80)),
    Personaje("Demonix", "demonio", random.randint(70, 100), random.randint(60, 100), random.randint(50, 90)),
    Personaje("T-800", "robot", random.randint(50, 90), random.randint(90, 100), random.randint(30, 70)),
    Personaje("Fang", "bestia", random.randint(40, 80), random.randint(70, 100), random.randint(60, 100)),
    Personaje("Drogon", "dragón", random.randint(80, 100), random.randint(90, 100), random.randint(40, 80))
]

# Asignar ataques aleatorios a los personajes
for personaje in personajes_disponibles:
    num_ataques = random.randint(2, 4)
    ataques_asignados = random.sample(ataques_disponibles, num_ataques)
    for ataque in ataques_asignados:
        personaje.agregar_ataque(ataque)

# Seleccionar dos personajes aleatorios para la batalla
jugador1 = random.choice(personajes_disponibles)
jugador2 = random.choice([p for p in personajes_disponibles if p != jugador1])

def draw_background():
    """Dibuja el fondo del juego."""
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(background_color)

def draw_stats(x, y, color, personaje, es_turno=False):
    """Dibuja las columnas y las estadísticas de los jugadores."""
    pygame.draw.rect(screen, color, (x, y, column_width, column_height))
    
    # Resaltar si es su turno
    if es_turno:
        pygame.draw.rect(screen, YELLOW, (x-3, y-3, column_width+6, column_height+6), 3)
    
    # Nombre y raza en la parte superior
    text_nombre = font.render(f"{personaje.nombre}", True, BLACK)
    text_raza = small_font.render(f"Raza: {personaje.raza}", True, BLACK)
    screen.blit(text_nombre, (x + (column_width - text_nombre.get_width()) // 2, y + 20))
    screen.blit(text_raza, (x + (column_width - text_raza.get_width()) // 2, y + 50))
    
    # Barra de vida debajo del nombre
    vida_ratio = personaje.vida_actual / personaje.vida_maxima
    barra_vida_width = int((column_width - 40) * vida_ratio)
    barra_vida_rect = pygame.Rect(x + 20, y + 80, barra_vida_width, 20)
    pygame.draw.rect(screen, GREEN, barra_vida_rect)
    pygame.draw.rect(screen, BLACK, (x + 20, y + 80, column_width - 40, 20), 2)
    text_vida = small_font.render(f"{personaje.vida_actual}/{personaje.vida_maxima}", True, BLACK)
    screen.blit(text_vida, (x + (column_width - text_vida.get_width()) // 2, y + 85))
    
    # Estadísticas en el centro
    stats_rect = pygame.Rect(x + 10, y + 120, column_width - 20, 150)
    pygame.draw.rect(screen, STAT_BG, stats_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, stats_rect, 2, border_radius=10)
    
    text_nivel = small_font.render(f"Nivel: {personaje.nivel}", True, BLACK)
    text_velocidad = small_font.render(f"Velocidad: {personaje.velocidad}", True, BLACK)
    
    screen.blit(text_nivel, (x + 20, y + 130))
    screen.blit(text_velocidad, (x + 20, y + 160))

def elegir_mejor_ataque(atacante, defensor):
    """Elige el ataque más efectivo contra el defensor"""
    mejor_ataque = None
    max_daño = 0
    
    for ataque in atacante.ataques:
        daño, _ = calcular_daño(atacante, defensor, ataque)
        if daño > max_daño:
            max_daño = daño
            mejor_ataque = ataque
    
    return mejor_ataque if mejor_ataque else random.choice(atacante.ataques)

def determinar_primer_turno():
    """Determina quién comienza basado en velocidad"""
    global turno_jugador
    if jugador1.velocidad > jugador2.velocidad:
        turno_jugador = True
    elif jugador2.velocidad > jugador1.velocidad:
        turno_jugador = False
    else:  # Empate en velocidad
        turno_jugador = random.choice([True, False])


def cambiar_turno():
    """Cambia el turno al otro jugador"""
    global turno_jugador, ultimo_turno
    turno_jugador = not turno_jugador
    ultimo_turno = time.time()

def ataque_cpu():
    """Realiza el ataque de la CPU"""
    if time.time() - ultimo_turno > delay_turno and not turno_jugador:
        mejor_ataque = elegir_mejor_ataque(jugador2, jugador1)
        shake_column("right", mejor_ataque)
        cambiar_turno()
        

def draw_button(x, y, text, hover):
    """Dibuja los botones de ataque."""
    color = DARK_GRAY if hover else LIGHT_GRAY
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    text_render = font.render(text, True, BLACK)
    screen.blit(text_render, (x + (button_width - text_render.get_width()) // 2, y + 10))

def draw_submenu(x, y, ataques):
    """Dibuja el submenú de ataques."""
    global submenu_height
    submenu_height = len(ataques) * 40 + 10
    pygame.draw.rect(screen, WHITE, (x, y, submenu_width, submenu_height))
    pygame.draw.rect(screen, BLACK, (x, y, submenu_width, submenu_height), 2)
    
    for i, ataque in enumerate(ataques):
        # Resaltar si el mouse está sobre el ataque
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hover = x <= mouse_x <= x + submenu_width and y + 10 + (i * 40) <= mouse_y <= y + 10 + (i * 40) + 35
        
        color = YELLOW if hover else WHITE
        pygame.draw.rect(screen, color, (x + 5, y + 10 + (i * 40), submenu_width - 10, 35))
        pygame.draw.rect(screen, BLACK, (x + 5, y + 10 + (i * 40), submenu_width - 10, 35), 1)
        
        # Mostrar nombre y tipo de ataque
        text_nombre = small_font.render(ataque.nombre, True, BLACK)
        text_tipo = small_font.render(f"Tipo: {ataque.tipo}", True, BLACK)
        
        screen.blit(text_nombre, (x + 10, y + 15 + (i * 40)))
        screen.blit(text_tipo, (x + 10, y + 30 + (i * 40)))

def draw_message():
    """Muestra mensajes emergentes cuando un ataque ocurre."""
    global message
    if message:
        elapsed_time = time.time() - message_time
        if elapsed_time > 3:
            message = ""  # Oculta el mensaje después de 3 segundos
        else:
            # Fondo del mensaje
            text_render = font.render(message, True, BLACK)
            msg_width = text_render.get_width() + 20
            msg_height = text_render.get_height() + 10
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - msg_width // 2, HEIGHT - 40, msg_width, msg_height))
            pygame.draw.rect(screen, BLACK, (WIDTH // 2 - msg_width // 2, HEIGHT - 40, msg_width, msg_height), 2)
            
            # Texto del mensaje
            screen.blit(text_render, (WIDTH // 2 - text_render.get_width() // 2, HEIGHT - 35))

def calcular_daño(atacante, defensor, ataque):
    """Calcula el daño considerando vulnerabilidades y resistencias."""
    daño_base = ataque.puntos_daño * (atacante.nivel / 100)
    
    # Ajustar por raza
    if defensor.raza in ataque.razas_vulnerables:
        daño_base *= 1.5
        mensaje_extra = " ¡Es muy efectivo!"
    elif defensor.raza in ataque.razas_resistentes:
        daño_base *= 0.5
        mensaje_extra = " ¡No es muy efectivo..."
    else:
        mensaje_extra = ""
    
    # Variación aleatoria
    daño_final = int(daño_base * random.uniform(0.9, 1.1))
    
    return daño_final, mensaje_extra

def shake_column(side, ataque):
    """Efecto de sacudida cuando un jugador ataca."""
    global message, message_time, jugador1, jugador2, batalla_actual, victorias, juego_activo
    
    if ataque.nombre == "Cancelar":
        return
    
    atacante = jugador1 if side == "left" else jugador2
    defensor = jugador2 if side == "left" else jugador1
    
    daño, mensaje_extra = calcular_daño(atacante, defensor, ataque)
    sigue_vivo = defensor.recibir_daño(daño)
    
    message = f"{atacante.nombre} usa {ataque.nombre}: {daño} de daño{mensaje_extra}"
    if not sigue_vivo:
        message += f" ¡{defensor.nombre} ha sido derrotado!"
    
    message_time = time.time()
    
    # Mostrar animación del ataque
    mostrar_animacion_ataque(side, ataque.anim_index)
    
    # Efecto de sacudida
    for _ in range(10):
        offset = random.randint(-5, 5)
        draw_background()
        
        if side == "left":
            draw_stats(column1_x, HEIGHT // 4, GRAY, jugador1, side == "left")
            pygame.draw.rect(screen, BLUE, (player1_base_pos[0], player1_base_pos[1], *player_size))
            draw_stats(column2_x, HEIGHT // 4, GRAY, jugador2, side == "right")
            pygame.draw.rect(screen, RED, (player2_base_pos[0] + offset, player2_base_pos[1], *player_size))
        else:
            draw_stats(column1_x, HEIGHT // 4, GRAY, jugador1, side == "left")
            pygame.draw.rect(screen, BLUE, (player1_base_pos[0] + offset, player1_base_pos[1], *player_size))
            draw_stats(column2_x, HEIGHT // 4, GRAY, jugador2, side == "right")
            pygame.draw.rect(screen, RED, (player2_base_pos[0], player2_base_pos[1], *player_size))
        
        draw_button(*button1_pos, "Atacar", False)
        draw_button(*button2_pos, "Atacar", False)
        draw_message()
        pygame.display.flip()
        pygame.time.delay(30)
    
    # Manejar el fin de la batalla
    if not sigue_vivo:
        if defensor == jugador2:  # Derrotaste al enemigo
            victorias += 1
            if victorias >= 5:
                message = "¡VICTORIA! Has derrotado a 5 enemigos."
                juego_activo = False
            else:
                # Generar nuevo enemigo
                jugador2 = random.choice([p for p in personajes_disponibles if p != jugador1])
                jugador2.vida_actual = jugador2.vida_maxima
                batalla_actual += 1
        else:  # Tu personaje fue derrotado
            message = "¡Has perdido! Juego terminado."
            juego_activo = False


def mostrar_animacion_ataque(posicion, anim_index):
    """Muestra una animación en la posición dada"""
    animacion = animaciones_ataque[anim_index]
    clock = pygame.time.Clock()
    
    for i in range(len(animacion)):
        # Dibujar todo el estado actual del juego
        draw_background()
        draw_stats(column1_x, HEIGHT // 4, GRAY, jugador1, posicion == "left")
        draw_stats(column2_x, HEIGHT // 4, GRAY, jugador2, posicion == "right")
        pygame.draw.rect(screen, BLUE, (player1_base_pos[0], player1_base_pos[1], *player_size))
        pygame.draw.rect(screen, RED, (player2_base_pos[0], player2_base_pos[1], *player_size))
        
        # Dibujar la animación en la posición correcta
        if posicion == "left":
            screen.blit(animacion[i], (player2_base_pos[0] - 30, player2_base_pos[1] - 20))
        else:
            screen.blit(animacion[i], (player1_base_pos[0] - 30, player1_base_pos[1] - 20))
        
        # Actualizar botones y mensajes
        if jugador1.vida_actual > 0 and jugador2.vida_actual > 0:
            draw_button(*button1_pos, "Atacar", False)
            draw_button(*button2_pos, "Atacar", False)
        draw_message()
        
        pygame.display.flip()
        clock.tick(10)  # Controla la velocidad de la animación

# Bucle principal del juego
determinar_primer_turno()  # Determinar quién comienza primero
running = True
while running:
    screen.fill(WHITE)

    # Manejar ataque de la CPU si es su turno
    if juego_activo and not turno_jugador and jugador1.vida_actual > 0 and jugador2.vida_actual > 0:
        ataque_cpu()

    # Obtener la posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button1_hover = (button1_pos[0] <= mouse_x <= button1_pos[0] + button_width and 
                     button1_pos[1] <= mouse_y <= button1_pos[1] + button_height and 
                     turno_jugador)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and juego_activo and turno_jugador:
            x, y = event.pos
            if submenu_active:
                if submenu_pos and submenu_pos[1] <= y <= submenu_pos[1] + submenu_height:
                    attack_idx = (y - submenu_pos[1] - 10) // 40
                    if 0 <= attack_idx < len(current_attacks):
                        shake_column("left", current_attacks[attack_idx])
                        cambiar_turno()
                submenu_active = False
            elif button1_hover and jugador1.vida_actual > 0 and jugador2.vida_actual > 0:
                current_attacks = jugador1.ataques.copy()
                submenu_active, submenu_pos = True, button1_pos

    draw_background()
    
    # Mostrar número de batalla actual
    batalla_text = font.render(f"Batalla: {batalla_actual}/5", True, BLACK)
    screen.blit(batalla_text, (20, 20))
    
    # Mostrar turno actual
    turno_text = font.render(f"Turno: {'Jugador' if turno_jugador else 'CPU'}", True, BLACK)
    screen.blit(turno_text, (WIDTH - turno_text.get_width() - 20, 20))
    
    draw_stats(column1_x, HEIGHT // 4, GRAY, jugador1, turno_jugador)
    draw_stats(column2_x, HEIGHT // 4, GRAY, jugador2, not turno_jugador)
    
    # Dibujar personajes
    pygame.draw.rect(screen, BLUE, (player1_base_pos[0], player1_base_pos[1], *player_size))
    pygame.draw.rect(screen, RED, (player2_base_pos[0], player2_base_pos[1], *player_size))
    
    # Dibujar botones solo si es turno del jugador y ambos están vivos
    if juego_activo and jugador1.vida_actual > 0 and jugador2.vida_actual > 0 and turno_jugador:
        draw_button(*button1_pos, "Atacar", button1_hover)
    elif not juego_activo:
        # Mostrar mensaje de victoria o derrota
        if victorias >= 5:
            mensaje_final = font.render("¡VICTORIA! Has derrotado a 5 enemigos.", True, BLACK)
        else:
            mensaje_final = font.render("¡Has perdido! Juego terminado.", True, BLACK)
        screen.blit(mensaje_final, (WIDTH // 2 - mensaje_final.get_width() // 2, HEIGHT - 50))
    
    if submenu_active and juego_activo and turno_jugador:
        draw_submenu(submenu_pos[0], submenu_pos[1], current_attacks)
    
    draw_message()
    pygame.display.flip()

pygame.quit()