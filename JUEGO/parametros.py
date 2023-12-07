import pygame
from pygame import mixer

try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
    pygame.font.init()
except Exception as ex:
    print(ex)

################ PARAMETROS ################

#COLORES
rojo = (255, 0, 0)
verde = (0, 255, 0)
negro = (0, 0, 0)
blanco = (255, 255, 255)

#CONTADORES

contador = 0
contador_tiempo_anterior = pygame.time.get_ticks()
puntaje = 0
nivel = 0
nivel_maximo = 3

#FLAGS

status = False
flag_intro = True
flag_opciones = False
flag_gana = False
flag_puntuaciones = False
game_over = False
sonido_muteado = False
flag_final = False

#ALIENS

filas = 4
columnas = 5
alien_cooldown = 1200
boss_cooldown = 500
velocidad_aliens = 1
ultimo_disparo_alien = pygame.time.get_ticks()
ultimo_disparo_boss = pygame.time.get_ticks()

#SCREEN - CLOCK

fondo = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\fondo.png")
ancho_ventana = 500
altura_ventana = 800
clock = pygame.time.Clock()
ventana = pygame.display.set_mode((ancho_ventana, altura_ventana))
pygame.display.set_caption("Galaxy Game")

#SONIDOS

disparo_fx = pygame.mixer.Sound("C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\disparo.wav")
disparo_fx.set_volume(0.10)
musica_fondo_fx = pygame.mixer.Sound("C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\musicafondo.wav")
musica_fondo_fx.set_volume(0.008)

#NOMBRE DEL JUGADOR

nombre = ""
input_nombre = ""
nombre_ingresado = False

#TXT

texto_intro = pygame.font.SysFont('console', 30, True)
txt_contador = pygame.font.SysFont('comicsans', 30, True)    
txt_puntos = pygame.font.SysFont('comicsans', 30, True)
txt_nivel = pygame.font.SysFont('comicsans', 30, True)


"""class Bossfinal(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\JUEGO\\Ships\\alien_final.png")
        self.image.set_colorkey(parametros.negro)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.movimiento = 1
        self.movimiento_speed = 0
    
    def update(self):
        self.rect.x += self.movimiento
        self.movimiento_speed += 1
        if abs(self.movimiento_speed) > 20:
            self.movimiento *= -1
            self.movimiento_speed *= self.movimiento
        if nave_player.vida_restante <= 0:
            self.kill()
            parametros.game_over = True"""