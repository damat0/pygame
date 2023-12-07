import pygame
import parametros
import random
import funciones
import sqlite3

try:
    conexion = sqlite3.connect("puntuaciones.db")
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS player_scores (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,score INTEGER NOT NULL)''')
    conexion.commit
except Exception as ex:
    print(ex)



class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, vida,alien_group, misil_group, balas_group, Explosiones, explosion_group, boss_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\FedShuttle.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vida_start = vida
        self.vida_restante = vida
        self.ultima_bala = pygame.time.get_ticks()
        self.ultimo_misil = pygame.time.get_ticks()
        self.misil_group = misil_group
        self.balas_group = balas_group
        self.Explosiones = Explosiones
        self.alien_group = alien_group
        self.explosion_group = explosion_group
        self.cursor = cursor
        self.conexion = conexion
        self.boss_group = boss_group


    def update(self):
        speed = 8
        cooldown = 0
        cooldown_misil = 10000
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if tecla[pygame.K_RIGHT] and self.rect.right < parametros.ancho_ventana:
            self.rect.x += speed

        tiempo = pygame.time.get_ticks()
        
        if tecla[pygame.K_z] and tiempo - self.ultimo_misil > cooldown_misil:
            parametros.disparo_fx.play()
            misil = Misiles(self.rect.centerx, self.rect.top, alien_group, Explosiones, explosion_group)
            self.misil_group.add(misil)
            self.ultimo_misil = tiempo

        if tecla[pygame.K_UP] and tiempo - self.ultima_bala > cooldown:
            parametros.disparo_fx.play()
            bala = Balas(self.rect.centerx, self.rect.top, self.alien_group, self.Explosiones, self.explosion_group, self.boss_group)
            self.balas_group.add(bala)
            self.ultima_bala = tiempo

        pygame.draw.rect(parametros.ventana, parametros.rojo, ((self.rect.x), (self.rect.bottom), self.rect.width, 10))
        if self.vida_restante > 0:
            pygame.draw.rect(parametros.ventana, parametros.verde, ((self.rect.x), (self.rect.bottom), int(self.rect.width * (self.vida_restante / self.vida_start)), 10))
        elif self.vida_restante <= 0:
            explosion = self.Explosiones(self.rect.centerx, self.rect.centery, 3)
            self.explosion_group.add(explosion)
            self.kill()

        if nave_player.vida_restante <= 0:
            self.cursor.execute("INSERT INTO player_scores (name, score) VALUES (?, ?)", (parametros.nombre, parametros.puntaje))
            self.conexion.commit()


        self.mask = pygame.mask.from_surface(self.image)

class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_group, Explosiones, explosion_group, boss_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\bullets.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.alien_group = alien_group
        self.Explosiones = Explosiones
        self.explosion_group = explosion_group
        self.boss_group = boss_group

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, self.alien_group, True):
            self.kill()
            explosion = self.Explosiones(self.rect.centerx, self.rect.centery, 2)
            self.explosion_group.add(explosion)
            parametros.puntaje += 1
        if pygame.sprite.spritecollide(self, self.boss_group, False):
            self.kill()
            explosion = self.Explosiones(self.rect.centerx, self.rect.centery, 2)
            boss_final.vida_restante -= 1
            self.explosion_group.add(explosion)
            parametros.puntaje += 1
        if len(self.alien_group) == 0 and parametros.nivel == 2:
            self.kill()
        if parametros.nivel == 0:
            self.kill()

class Misiles(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_group, Explosiones, explosion_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\misil.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.alien_group = alien_group
        self.Explosiones = Explosiones
        self.explosion_group = explosion_group

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, self.alien_group, True):
            explosion = self.Explosiones(self.rect.centerx, self.rect.centery, 2)
            self.explosion_group.add(explosion)
            parametros.puntaje += 1
        if len(self.alien_group) == 0:
            self.kill()

class BossFinal(pygame.sprite.Sprite):
    def __init__(self, x, y, vida):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\JUEGO\\Ships\\alien_final.png")
        self.image.set_colorkey(parametros.negro)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vida_inicial = vida
        self.vida_restante = vida
        self.movimiento = 1
        self.movimiento_speed = 0

    
    def update(self):       
        self.rect.x += self.movimiento
        self.movimiento_speed += 1
        if abs(self.movimiento_speed) > 150:
            self.movimiento *= -1
            self.movimiento_speed *= self.movimiento
        pygame.draw.rect(parametros.ventana, parametros.rojo, ((self.rect.x), (self.rect.bottom), self.rect.width, 10))
        if self.vida_restante > 0:
            pygame.draw.rect(parametros.ventana, parametros.verde, ((self.rect.x), (self.rect.bottom), int(self.rect.width * (self.vida_restante / self.vida_inicial)), 10))
        if self.vida_restante <= 0:
            pygame.draw.rect(parametros.ventana, parametros.verde, ((self.rect.x), (self.rect.bottom), int(self.rect.width * (self.vida_restante / self.vida_inicial)), 10))
            self.kill()
            parametros.flag_gana = True
        if nave_player.vida_restante <= 0:
            self.kill()        
            parametros.game_over = True


class Boss_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\JUEGO\\Ships\\alien_bullets.png")
        self.image.set_colorkey(parametros.blanco)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 3
        if self.rect.top > parametros.altura_ventana:
            self.kill()
        if pygame.sprite.spritecollide(self, nave_group, False, pygame.sprite.collide_mask):
            self.kill()
            nave_player.vida_restante -= 1
            explosion = Explosiones(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
        if len(boss_group) == 0:
            self.kill()

class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\alien" + str(random.randint(1, 5)) + ".png")
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
            parametros.game_over = True

class Enemie_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\alien_bullets.png")
        self.image.set_colorkey(parametros.blanco)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


    def update(self):
        self.rect.y += 3
        if self.rect.top > parametros.altura_ventana:
            self.kill()
        if pygame.sprite.spritecollide(self, nave_group, False, pygame.sprite.collide_mask):
            self.kill()
            nave_player.vida_restante -= 1
            explosion = Explosiones(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
        if len(alien_group) == 0:
            self.kill()
        
class Explosiones(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = []
        for n in range(1, 6):
            imagen = pygame.image.load(f"C:\\Users\\emili\\OneDrive\\Escritorio\\Programacion\\PYGAME\\Ships\\exp{n}.png")
            if size == 1:
                imagen = pygame.transform.scale(imagen, (30, 30))
            if size == 2:
                imagen = pygame.transform.scale(imagen, (60, 60))
            if size == 3:
                imagen = pygame.transform.scale(imagen, (120, 120))
            self.imagenes.append(imagen)
        self.index = 0
        self.image = self.imagenes[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    
    def update(self):
        velocidad_exp = 3
        self.counter += 1
        if self.counter >= velocidad_exp and self.index < len(self.imagenes) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.imagenes[self.index]
        if self.index >= len(self.imagenes) -1 and self.counter >= velocidad_exp:
            self.kill()


nave_group = pygame.sprite.Group()
balas_group = pygame.sprite.Group()
misil_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_balas_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
boss_bullets_group = pygame.sprite.Group()

boss_final = 1


nave_player = Nave(int(parametros.ancho_ventana / 2), parametros.altura_ventana - 100, 3, alien_group, misil_group, balas_group, Explosiones, explosion_group, boss_group)
nave_group.add(nave_player)