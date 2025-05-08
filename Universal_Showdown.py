import pygame
import random
import textwrap
import ollama
import os

# Configuración inicial
PERSONAJES = {
    "Arturo": {
        "descripcion": "Maestro de la psicología erótica y manipulación mental.",
        "vida_max": 100,
        "frase": "'¿Eso es todo lo que tienes? Qué... aburrido'",
        "color": (70, 130, 180),  # Azul acero
        "velocidad": 80,
        "imagen": "images/arturo.jpg"  # Añadido path de imagen
    },
    "Mike": {
        "descripcion": "Guerrero imparable con resistencia sobrehumana.",
        "vida_max": 150,
        "frase": "'¡Puedes golpearme mil veces, pero sólo necesito una!'",
        "color": (178, 34, 34),  # Rojo fuego
        "velocidad": 60,
        "imagen": "images/jfruiz.png"  # Añadido path de imagen
    },
    "Valeria": {
        "descripcion": "Asesina sigilosa con dagas envenenadas.",
        "vida_max": 80,
        "frase": "'La oscuridad es mi aliada...'",
        "color": (75, 0, 130),  # Índigo
        "velocidad": 90,
        "imagen": "images/valeria.jpeg"  # Añadido path de imagen
    },
    "Drakar": {
        "descripcion": "Bárbaro colérico con hacha de doble filo.",
        "vida_max": 160,
        "frase": "'¡SANGRE Y FURIA!'",
        "color": (220, 20, 60),  # Rojo carmesí
        "velocidad": 50,
        "imagen": "images/drakar.jpeg"  # Añadido path de imagen
    }
}
SONIDOS = {
    "golpe_corte": "sonido/espada.mp3",
    "golpe_contundente": "sonido/espada.mp3",
    "golpe_blaster": "sonido/magia.mp3",
    "impacto": "sonido/hit.mp3",
    "victoria": "sonido/win.mp3",
    "derrota": "sonido/lose.mp3"
}

# Configuración de sprites de ataque
SPRITES_ATAQUE = {
    "corte": "sprites/espada.png",
    "contundente": "sprites/martillo.png",
    "blaster": "sprites/magia.png"
}
# Configuración de archivos multimedia
MENU_BACKGROUND = "images/menu.jpeg"  # Imagen del menú principal
MENU_MUSIC = "Shadows_Rise.mp3"  # Música del menú
GAME_MUSIC = "b2.mp3"  # Música del juego
BATTKE_BK = "images/battle.jpeg"
# Configuración de pantalla (combinación de ambos)
WIDTH, HEIGHT = 1000, 800
MAX_LINE_LENGTH = 78
MAX_VISIBLE_LINES = 5  # Numero de lineas que se ven al final

# Colores (de python.py con ajustes)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (180, 180, 180)
DARK_GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
STAT_BG = (255, 255, 255)

# Configuración para vistas de los personajes
player_size = (80, 80)
column_width = 200
column_height = 400
column1_x = (WIDTH // 4) - (column_width // 2)
column2_x = (3 * WIDTH // 4) - (column_width // 2)
player1_base_pos = (column1_x + (column_width - player_size[0]) // 2, HEIGHT // 4 - player_size[1] // 3)
player2_base_pos = (column2_x + (column_width - player_size[0]) // 2, HEIGHT // 4 - player_size[1] // 3)

# Botones
button_width, button_height = 100, 40
button1_pos = (column1_x + (column_width - button_width) // 2, HEIGHT // 4 + column_height // 2)
button2_pos = (column2_x + (column_width - button_width) // 2, HEIGHT // 4 + column_height // 2)

# Panel de texto
text_panel_height = MAX_VISIBLE_LINES * 30 + 20
text_panel_y = HEIGHT - text_panel_height - 10

# Diccionario para almacenar imágenes cargadas
imagenes_personajes = {}
menu_image = None
background_image = None
# Inicialización de pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Universal Showdown - Final Edition")
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 20)
large_font = pygame.font.SysFont("Arial", 48)
clock = pygame.time.Clock()

# Función para cargar imágenes
def cargar_imagenes():
    """Carga todas las imágenes necesarias"""
    global menu_image
    
    # Cargar imagen del menú
    try:
        if os.path.exists(MENU_BACKGROUND):
            menu_image = pygame.image.load(MENU_BACKGROUND)
            menu_image = pygame.transform.scale(menu_image, (WIDTH, HEIGHT))
        else:
            print(f"⚠️ Imagen de menú no encontrada: {MENU_BACKGROUND}")
            menu_image = None
    except Exception as e:
        print(f"❌ Error al cargar imagen de menú: {e}")
        menu_image = None
    
    # Cargar imágenes de personajes
    for nombre, datos in PERSONAJES.items():
        try:
            # Intentar cargar la imagen, si existe
            if os.path.exists(datos["imagen"]):
                img = pygame.image.load(datos["imagen"])
                # Redimensionar al tamaño del jugador
                imagenes_personajes[nombre] = pygame.transform.scale(img, player_size)
            else:
                print(f"⚠️ Imagen no encontrada para {nombre}: {datos['imagen']}")
                # Usar color de respaldo si no hay imagen
                imagenes_personajes[nombre] = None
        except Exception as e:
            print(f"❌ Error al cargar imagen para {nombre}: {e}")
            imagenes_personajes[nombre] = None

# Función para mostrar el menú principal
def mostrar_menu_principal():
    """Muestra el menú principal y espera a que se pulse la tecla espacio"""
    # Cargar y reproducir música del menú
    try:
        pygame.mixer.music.load(MENU_MUSIC)
        pygame.mixer.music.play(-1)  # Reproducir en bucle
        pygame.mixer.music.set_volume(0.7)
    except pygame.error as e:
        print(f"⚠️ Error al cargar la música del menú: {e}")
    
    # Mensaje para presionar espacio
    mensaje_texto = "Presiona ESPACIO para comenzar"
    mensaje_sombra = large_font.render(mensaje_texto, True, BLACK)
    mensaje = large_font.render(mensaje_texto, True, WHITE)
    
    # Título del juego
    titulo_texto = "UNIVERSAL SHOWDOWN"
    titulo_sombra = pygame.font.SysFont("Arial", 72, bold=True).render(titulo_texto, True, BLACK)
    titulo = pygame.font.SysFont("Arial", 72, bold=True).render(titulo_texto, True, (255, 215, 0))  # Dorado
    
    esperando = True
    parpadeo = 0
    
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    esperando = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        
        # Dibujar fondo
        if menu_image:
            screen.blit(menu_image, (0, 0))
        else:
            # Fondo alternativo si no hay imagen
            screen.fill((50, 50, 100))
            
        # Dibujar título con sombra
        screen.blit(titulo_sombra, (WIDTH//2 - titulo_sombra.get_width()//2 + 3, HEIGHT//4 + 3))
        screen.blit(titulo, (WIDTH//2 - titulo.get_width()//2, HEIGHT//4))
        
        # Efecto de parpadeo en el mensaje
        parpadeo = (parpadeo + 1) % 60
        if parpadeo < 40:  #40 es el equivalente a dos tercios del tiempo
            # Dibujar mensaje con sombra
            screen.blit(mensaje_sombra, (WIDTH//2 - mensaje_sombra.get_width()//2 + 2, 2*HEIGHT//3 + 2))
            screen.blit(mensaje, (WIDTH//2 - mensaje.get_width()//2, 2*HEIGHT//3))
        
        pygame.display.flip()
        clock.tick(30)
    
    # Cambiar a la música del juego
    try:
        pygame.mixer.music.fadeout(1000)  # Fade out de 1 segundo
        pygame.time.delay(1000)  # Esperar a que termine el fade out
        pygame.mixer.music.load(GAME_MUSIC)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    except pygame.error as e:
        print(f"⚠️ Error al cambiar a la música del juego: {e}")
    
    return True
class AnimacionAtaque:
    def __init__(self, tipo, origen, destino):
        self.tipo = tipo
        self.origen = origen
        self.destino = destino
        try:
            self.sprite = pygame.image.load(SPRITES_ATAQUE[tipo]).convert_alpha()
            # Reproducir sonido de ataque al iniciar la animación
            if tipo == "corte":
                self.sonido_ataque = pygame.mixer.Sound(SONIDOS["golpe_corte"])
            elif tipo == "contundente":
                self.sonido_ataque = pygame.mixer.Sound(SONIDOS["golpe_contundente"])
            elif tipo == "blaster":
                self.sonido_ataque = pygame.mixer.Sound(SONIDOS["golpe_blaster"])
            self.sonido_ataque.play()
        except:
            self.sprite = None
            self.sonido_ataque = None
        
        self.posicion = list(origen)
        self.velocidad = 10
        self.activa = True
        self.sonido_impacto = None
        
    def actualizar(self):
        if not self.activa:
            return False
        
        # Calcular dirección del movimiento
        dx = self.destino[0] - self.posicion[0]
        dy = self.destino[1] - self.posicion[1]
        distancia = max(1, (dx**2 + dy**2)**0.5)
        
        # Normalizar y aplicar velocidad
        self.posicion[0] += dx / distancia * self.velocidad
        self.posicion[1] += dy / distancia * self.velocidad
        
        # Verificar si ha llegado al destino
        if abs(self.posicion[0] - self.destino[0]) < 10 and abs(self.posicion[1] - self.destino[1]) < 10:
            self.activa = False
            try:
                impacto = pygame.mixer.Sound(SONIDOS["impacto"])
                impacto.play()
            except:
                pass
            return True  # Indica que el ataque ha impactado
        
        return False
    
    def dibujar(self, superficie):
        if self.activa and self.sprite:
            superficie.blit(self.sprite, self.posicion)

# Función para inicializar el modelo
def inicializar_modelo():
    try:
        print("⚙️ Cargando modelo Llama 3...")
        ollama.generate(model="llama3", prompt="Inicializando")  # Warm-up
        print("✅ Modelo listo")
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")

# Función para generar narrativa
def generar_narrativa(estado):
    atacante = estado["combatientes"][estado["turno"] % 2]
    defensor = estado["combatientes"][(estado["turno"] + 1) % 2]
    
    prompt = f"""**Narra el Turno {estado['turno'] + 1}**:
    - Personajes: {atacante} (ataca) vs {defensor} (defiende)
    - Estilo: Combate épico tipo anime shonen
    - Requisitos:
      * 2 frases máximo, en español
      * 1 diálogo entre comillas, muy corto
      * Incluye 1 técnica, en tres palabras, que tenga que ver con el contexto del personaje
      * Usa un maximo de 20 palabras
      * No es necesario que pongas el turno, solo la narracion
    - Ejemplo: "Con un salto imposible, {atacante} desencadena su 'Onda Sísmica Carmesí'. '¡Ni tus huesos quedarán en pie!', mientras la tormenta electrifica el coliseo..."
    
    **Narración requerida:**"""
    
    try:
        response = ollama.generate(
            model="llama3",
            prompt=prompt,
            options={
                "temperature": 0.7,
                "num_predict": 150
            }
        )
        narrativa = response["response"]
        return textwrap.wrap(narrativa, MAX_LINE_LENGTH)
    
    except Exception as e:
        print(f"⚠️ Error generando texto: {e}")
        return [f"{atacante} lanza un ataque brutal contra {defensor}!"]

# Función para selección aleatoria de personajes (adaptado a lo de Alberto)
def seleccionar_personajes_aleatorio():
    personajes_disponibles = list(PERSONAJES.keys())
    p1, p2 = random.sample(personajes_disponibles, 2)
    return p1, p2

# Función para inicializar el estado del juego (adaptado a lo de Alberto)
def inicializar_estado(personaje1, personaje2):
    return {
        "turno": 0,
        "historial": [
            (f"La batalla comienza entre {personaje1} y {personaje2}", BLACK),
            (f"{personaje1}: {PERSONAJES[personaje1]['frase']}", PERSONAJES[personaje1]["color"]),
            (f"{personaje2}: {PERSONAJES[personaje2]['frase']}", PERSONAJES[personaje2]["color"]),
            ("¡El combate está por comenzar!", BLACK)
        ],
        "combate_activo": True,
        "ganador": None,
        "contexto_combate": "Un coliseo abandonado bajo una tormenta eléctrica",
        "combatientes": [personaje1, personaje2],
        "vidas": {
            personaje1: PERSONAJES[personaje1]["vida_max"],
            personaje2: PERSONAJES[personaje2]["vida_max"]
        },
        "velocidades": {
            personaje1: PERSONAJES[personaje1]["velocidad"],
            personaje2: PERSONAJES[personaje2]["velocidad"]
        }
    }

# Sistema de combate (añadiendo cambios a lo de alberto)

def ejecutar_turno(estado):
    atacante = estado["combatientes"][estado["turno"] % 2]
    defensor = estado["combatientes"][(estado["turno"] + 1) % 2]
    
    # añado el mensaje al historial
    estado["historial"].append(("Generando texto...", YELLOW))
    
    # Dibujar todo de nuevo con el nuevo mensaje
    draw_background()
    draw_stats(column1_x, HEIGHT // 4, estado["combatientes"][0], estado, estado["turno"] % 2 == 0)
    draw_stats(column2_x, HEIGHT // 4, estado["combatientes"][1], estado, estado["turno"] % 2 == 1)
    draw_players(estado["combatientes"][0], estado["combatientes"][1])
    draw_text_panel(estado)
    pygame.display.flip()  # Refresca la pantalla para evitar que no salga el mensaje de generacion
    
    # genero el texto
    lineas_narracion = generar_narrativa(estado)
    
    # aqui cambio el generando texto por el texto que realmente va a salir
    estado["historial"][-1] = (lineas_narracion[0], PERSONAJES[atacante]["color"])
    for linea in lineas_narracion[1:]:
        estado["historial"].append((linea, PERSONAJES[atacante]["color"]))
    
    # Resto de la lógica del turno...
    dano_base = random.randint(15, 20)
    dano = int(dano_base * (PERSONAJES[defensor]["vida_max"] / 100))
    estado["vidas"][defensor] -= dano
    
    if estado["vidas"][defensor] <= 0:
        estado["vidas"][defensor] = 0
        estado["combate_activo"] = False
        estado["ganador"] = atacante
        mensaje_victoria = f"¡{atacante} se alza victorioso con {estado['vidas'][atacante]} de vida restante!"
        estado["historial"].append((mensaje_victoria, PERSONAJES[atacante]["color"]))
    
    estado["turno"] += 1
    return atacante, defensor

# Funciones de dibujo del programa
def draw_background():
    """Dibuja el fondo del juego."""
    global background_image
    if background_image is None:
        try:
            background_image = pygame.image.load("images/batte.jpeg").convert()
            background_image = pygame.transform.scale(background_image, screen.get_size())
        except pygame.error:
            background_image = False  # Señal de que no se pudo cargar

    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill((100, 150, 250))  # Azul cielo

def draw_stats(x, y, personaje, estado, es_turno=False):
    """Dibuja las columnas y las estadísticas de los jugadores."""
    color = PERSONAJES[personaje]["color"]
    vida = estado["vidas"][personaje]
    vida_max = PERSONAJES[personaje]["vida_max"]
    
    # Columna
    pygame.draw.rect(screen, GRAY, (x, y, column_width, column_height))
    
    # Resaltar si es su turno
    if es_turno:
        pygame.draw.rect(screen, YELLOW, (x-3, y-3, column_width+6, column_height+6), 3)
    
    # Nombre en la parte superior
    text_nombre = font.render(f"{personaje}", True, color)
    screen.blit(text_nombre, (x + (column_width - text_nombre.get_width()) // 2, y + 20))
    
    # Barra de vida
    vida_ratio = vida / vida_max
    barra_vida_width = int((column_width - 40) * vida_ratio)
    barra_vida_rect = pygame.Rect(x + 20, y + 60, barra_vida_width, 20)
    pygame.draw.rect(screen, GREEN, barra_vida_rect)
    pygame.draw.rect(screen, BLACK, (x + 20, y + 60, column_width - 40, 20), 2)
    text_vida = small_font.render(f"{vida}/{vida_max}", True, BLACK)
    screen.blit(text_vida, (x + (column_width - text_vida.get_width()) // 2, y + 60))
    
    # Estadísticas
    stats_rect = pygame.Rect(x + 10, y + 100, column_width - 20, 100)
    pygame.draw.rect(screen, STAT_BG, stats_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, stats_rect, 2, border_radius=10)
    
    text_velocidad = small_font.render(f"Velocidad: {estado['velocidades'][personaje]}", True, BLACK)
    screen.blit(text_velocidad, (x + 20, y + 110))

def draw_players(personaje1, personaje2):
    """Dibuja los personajes con sus imágenes y nombres."""
    # Dibujar nombre del jugador 1 (ENCIMA de la imagen)
    nombre1 = small_font.render(personaje1, True, BLACK)
    nombre1_pos = (player1_base_pos[0] + (player_size[0] - nombre1.get_width()) // 2, 
                  player1_base_pos[1] - nombre1.get_height() - 5)
    nombre1_bg = pygame.Rect(nombre1_pos[0] - 5, nombre1_pos[1] - 2, 
                           nombre1.get_width() + 10, nombre1.get_height() + 4)
    pygame.draw.rect(screen, (240, 240, 240, 200), nombre1_bg, border_radius=4)
    screen.blit(nombre1, nombre1_pos)
    
    # Dibujar nombre del jugador 2 (ENCIMA de la imagen)
    nombre2 = small_font.render(personaje2, True, BLACK)
    nombre2_pos = (player2_base_pos[0] + (player_size[0] - nombre2.get_width()) // 2, 
                  player2_base_pos[1] - nombre2.get_height() - 5)
    nombre2_bg = pygame.Rect(nombre2_pos[0] - 5, nombre2_pos[1] - 2, 
                           nombre2.get_width() + 10, nombre2.get_height() + 4)
    pygame.draw.rect(screen, (240, 240, 240, 200), nombre2_bg, border_radius=4)
    screen.blit(nombre2, nombre2_pos)
    
    # Dibujar jugador 1
    if imagenes_personajes[personaje1]:
        screen.blit(imagenes_personajes[personaje1], player1_base_pos)
    else:
        # Usar color de respaldo si no hay imagen
        pygame.draw.rect(screen, PERSONAJES[personaje1]["color"], 
                      (player1_base_pos[0], player1_base_pos[1], *player_size))
    
    # Dibujar jugador 2
    if imagenes_personajes[personaje2]:
        screen.blit(imagenes_personajes[personaje2], player2_base_pos)
    else:
        # Usar color de respaldo si no hay imagen
        pygame.draw.rect(screen, PERSONAJES[personaje2]["color"], 
                      (player2_base_pos[0], player2_base_pos[1], *player_size))

def draw_text_panel(estado):
    """Dibuja el panel de texto en la parte inferior."""
    panel = pygame.Surface((WIDTH - 40, text_panel_height - 20), pygame.SRCALPHA)
    panel.fill((220, 220, 255, 200))
    screen.blit(panel, (20, text_panel_y + 10))
    
    # Historial de combate
    y_offset = text_panel_y + 20
    for linea_info in estado["historial"][-MAX_VISIBLE_LINES:]:
        # Cada elemento de el historial va a ser una tupla con el color para que salga bien
        if isinstance(linea_info, tuple) and len(linea_info) == 2:
            texto, color = linea_info
        else:
            # Esto solo por si no carga bien el color, que salga en negro
            texto = linea_info
            color = BLACK
        
        text_surface = small_font.render(texto, True, color)
        screen.blit(text_surface, (30, y_offset))
        y_offset += 28
def draw_button(x, y, text, hover):
    """Dibuja los botones de acción."""
    color = DARK_GRAY if hover else LIGHT_GRAY
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    text_render = small_font.render(text, True, BLACK)
    screen.blit(text_render, (x + (button_width - text_render.get_width()) // 2, y + 10))

def determinar_primer_turno(estado):
    return 0  # Jugador 1 comienza


def shake_effect(atacante, defensor):
    """Efecto de sacudida cuando un jugador ataca."""
    for _ in range(10):
        offset = random.randint(-5, 5)
        draw_background()
        
        if atacante == estado["combatientes"][0]:  # Jugador 1 ataca
            draw_stats(column1_x, HEIGHT // 4, estado["combatientes"][0], estado, True)
            
            # Nombre del jugador 1 (encima)
            nombre1 = small_font.render(estado["combatientes"][0], True, BLACK)
            nombre1_pos = (player1_base_pos[0] + (player_size[0] - nombre1.get_width()) // 2, 
                          player1_base_pos[1] - nombre1.get_height() - 5)
            pygame.draw.rect(screen, (240, 240, 240, 200), 
                            (nombre1_pos[0] - 5, nombre1_pos[1] - 2, 
                             nombre1.get_width() + 10, nombre1.get_height() + 4), 
                            border_radius=4)
            screen.blit(nombre1, nombre1_pos)
            
            # Dibujar jugador 1 (normal)
            if imagenes_personajes[estado["combatientes"][0]]:
                screen.blit(imagenes_personajes[estado["combatientes"][0]], player1_base_pos)
            else:
                pygame.draw.rect(screen, PERSONAJES[estado["combatientes"][0]]["color"], 
                                (player1_base_pos[0], player1_base_pos[1], *player_size))
            
            # Dibujar stats del jugador 2
            draw_stats(column2_x, HEIGHT // 4, estado["combatientes"][1], estado, False)
            
            # Nombre del jugador 2 (encima, con sacudida)
            pos_sacudida = (player2_base_pos[0] + offset, player2_base_pos[1])
            nombre2 = small_font.render(estado["combatientes"][1], True, BLACK)
            nombre2_pos = (pos_sacudida[0] + (player_size[0] - nombre2.get_width()) // 2, 
                          pos_sacudida[1] - nombre2.get_height() - 5)
            pygame.draw.rect(screen, (240, 240, 240, 200), 
                            (nombre2_pos[0] - 5, nombre2_pos[1] - 2, 
                             nombre2.get_width() + 10, nombre2.get_height() + 4), 
                            border_radius=4)
            screen.blit(nombre2, nombre2_pos)
            
            # Dibujar jugador 2 (con efecto de sacudida)
            if imagenes_personajes[estado["combatientes"][1]]:
                screen.blit(imagenes_personajes[estado["combatientes"][1]], pos_sacudida)
            else:
                pygame.draw.rect(screen, PERSONAJES[estado["combatientes"][1]]["color"], 
                                (pos_sacudida[0], pos_sacudida[1], *player_size))
            
        else:  # Jugador 2 ataca
            # Dibujar stats del jugador 1
            draw_stats(column1_x, HEIGHT // 4, estado["combatientes"][0], estado, False)
            
            # Nombre del jugador 1 (encima, con sacudida)
            pos_sacudida = (player1_base_pos[0] + offset, player1_base_pos[1])
            nombre1 = small_font.render(estado["combatientes"][0], True, BLACK)
            nombre1_pos = (pos_sacudida[0] + (player_size[0] - nombre1.get_width()) // 2, 
                          pos_sacudida[1] - nombre1.get_height() - 5)
            pygame.draw.rect(screen, (240, 240, 240, 200), 
                            (nombre1_pos[0] - 5, nombre1_pos[1] - 2, 
                             nombre1.get_width() + 10, nombre1.get_height() + 4), 
                            border_radius=4)
            screen.blit(nombre1, nombre1_pos)
            
            # Dibujar jugador 1 (con efecto de sacudida)
            if imagenes_personajes[estado["combatientes"][0]]:
                screen.blit(imagenes_personajes[estado["combatientes"][0]], pos_sacudida)
            else:
                pygame.draw.rect(screen, PERSONAJES[estado["combatientes"][0]]["color"], 
                                (pos_sacudida[0], pos_sacudida[1], *player_size))
            
            # Dibujar stats del jugador 2
            draw_stats(column2_x, HEIGHT // 4, estado["combatientes"][1], estado, True)
            
            # Nombre del jugador 2 (encima)
            nombre2 = small_font.render(estado["combatientes"][1], True, BLACK)
            nombre2_pos = (player2_base_pos[0] + (player_size[0] - nombre2.get_width()) // 2, 
                          player2_base_pos[1] - nombre2.get_height() - 5)
            pygame.draw.rect(screen, (240, 240, 240, 200), 
                            (nombre2_pos[0] - 5, nombre2_pos[1] - 2, 
                             nombre2.get_width() + 10, nombre2.get_height() + 4), 
                            border_radius=4)
            screen.blit(nombre2, nombre2_pos)
            
            # Dibujar jugador 2 (normal)
            if imagenes_personajes[estado["combatientes"][1]]:
                screen.blit(imagenes_personajes[estado["combatientes"][1]], player2_base_pos)
            else:
                pygame.draw.rect(screen, PERSONAJES[estado["combatientes"][1]]["color"], 
                                (player2_base_pos[0], player2_base_pos[1], *player_size))
            
        draw_text_panel(estado)
        pygame.display.flip()
        pygame.time.delay(30)

# Función principal
def main():
    # Cargar imágenes de personajes
    cargar_imagenes()
    
    global estado
    # Inicializar modelo de lenguaje
    inicializar_modelo()
    # Mostrar menú principal
    if not mostrar_menu_principal():
        return  # Salir si se cierra el menú
    
    # Selección aleatoria de personajes
    p1, p2 = seleccionar_personajes_aleatorio()
    
    # Inicializar estado
    estado = inicializar_estado(p1, p2)
    turno_actual = determinar_primer_turno(estado)
    
    # Variables para animación
    animacion_actual = None
    esperando_animacion = False

        # Variables para música/sonidos
    musica_reproduciendose = True
    sonido_victoria = pygame.mixer.Sound(SONIDOS["victoria"])
    sonido_derrota = pygame.mixer.Sound(SONIDOS["derrota"])
    # Bucle principal
    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_hover = (button1_pos[0] <= mouse_x <= button1_pos[0] + button_width and 
                       button1_pos[1] <= mouse_y <= button1_pos[1] + button_height and 
                       turno_actual == 0 and estado["combate_activo"] and not esperando_animacion)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    p1, p2 = seleccionar_personajes_aleatorio()
                    estado = inicializar_estado(p1, p2)
                    turno_actual = determinar_primer_turno(estado)
                    esperando_animacion = False
                    animacion_actual = None
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and estado["combate_activo"] and not esperando_animacion:
                if button_hover and turno_actual == 0:
                    # Crear animación de ataque
                    origen = (player1_base_pos[0] + player_size[0]//2, player1_base_pos[1] + player_size[1]//2)
                    destino = (player2_base_pos[0] + player_size[0]//2, player2_base_pos[1] + player_size[1]//2)
                    animacion_actual = AnimacionAtaque(random.choice(list(SPRITES_ATAQUE.keys())), origen, destino)
                    esperando_animacion = True
                elif turno_actual == 1:
                    # Turno automático del oponente
                    origen = (player2_base_pos[0] + player_size[0]//2, player2_base_pos[1] + player_size[1]//2)
                    destino = (player1_base_pos[0] + player_size[0]//2, player1_base_pos[1] + player_size[1]//2)
                    animacion_actual = AnimacionAtaque(random.choice(list(SPRITES_ATAQUE.keys())), origen, destino)
                    esperando_animacion = True
        
        # Actualizar animación si está activa
        if esperando_animacion and animacion_actual:
            impacto = animacion_actual.actualizar()
            if impacto:
                # Cuando el ataque impacta, ejecutar el turno
                atacante, defensor = ejecutar_turno(estado)
                shake_effect(atacante, defensor)
                
                # Verificar si el combate terminó
                if not estado["combate_activo"]:
                    # Reproducir sonido de victoria/derrota
                    if estado["ganador"] == estado["combatientes"][0]:  # Si el jugador 1 ganó
                        sonido_victoria.play()
                    else:
                        sonido_derrota.play()
                
                # Cambiar turno
                turno_actual = 1 if turno_actual == 0 else 0
                esperando_animacion = False
                animacion_actual = None
        
        # Dibujar todo
        draw_background()
        
        # Dibujar estadísticas
        draw_stats(column1_x, HEIGHT // 4, estado["combatientes"][0], estado, turno_actual == 0 and not esperando_animacion)
        draw_stats(column2_x, HEIGHT // 4, estado["combatientes"][1], estado, turno_actual == 1 and not esperando_animacion)
        
        # Dibujar personajes con sus nombres
        draw_players(estado["combatientes"][0], estado["combatientes"][1])
        
        # Dibujar animación de ataque si está activa
        if animacion_actual:
            animacion_actual.dibujar(screen)
        
        # Dibujar botón de ataque si es turno del jugador y no hay animación
        if estado["combate_activo"] and turno_actual == 0 and not esperando_animacion:
            draw_button(*button1_pos, "Atacar", button_hover)
        
        # Dibujar panel de texto
        draw_text_panel(estado)
        
        # Mostrar turno actual
        if not esperando_animacion:
            turno_text = font.render(f"Turno: {estado['combatientes'][turno_actual]}", True, BLACK)
            screen.blit(turno_text, (WIDTH // 2 - turno_text.get_width() // 2, 20))
        
        # Mostrar fin del combate
        if not estado["combate_activo"]:
            fin_text = pygame.font.SysFont("Arial", 36).render(
                f"¡{estado['ganador']} gana el combate!", 
                True, 
                PERSONAJES[estado["ganador"]]["color"]
            )
            screen.blit(fin_text, (WIDTH // 2 - fin_text.get_width() // 2, HEIGHT // 2))
        # Verificar fin del combate y reproducir sonidos
        if not estado["combate_activo"] and musica_reproduciendose:
            # Detener música de fondo
            pygame.mixer.music.fadeout(1000)
            
            # Reproducir sonido de victoria/derrota
            if estado["ganador"] == estado["combatientes"][0]:  # Si el jugador 1 ganó
                sonido_victoria.play()
            else:
                sonido_derrota.play()
            
            musica_reproduciendose = False 
         # Si se reinicia el juego
        if estado["combate_activo"] and not musica_reproduciendose:
            try:
                pygame.mixer.music.load(GAME_MUSIC)
                pygame.mixer.music.play(-1)
                musica_reproduciendose = True
            except:
                pass
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()