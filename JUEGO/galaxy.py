import pygame
from pygame import mixer
import random
import sqlite3
import parametros   
import funciones
import nave

try:
    conexion = sqlite3.connect("puntuaciones.db")
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS player_scores (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,score INTEGER NOT NULL)''')
    conexion.commit
except Exception as ex:
    print(ex)

pygame.init()

try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
except Exception as ex:
    print(ex)

#TXT

texto_intro = pygame.font.SysFont('console', 30, True)
txt_contador = pygame.font.SysFont('comicsans', 30, True)    
txt_puntos = pygame.font.SysFont('comicsans', 30, True)
txt_nivel = pygame.font.SysFont('comicsans', 30, True)

parametros.musica_fondo_fx.play()

################ JUEGO ################

repetir = True
while repetir == True:
    while parametros.flag_intro:
        parametros.clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    parametros.flag_intro = False
                    parametros.status = True
                elif evento.key == pygame.K_BACKSPACE:
                    parametros.input_nombre = parametros.input_nombre[:-1]
                else:
                    parametros.input_nombre += evento.unicode
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouseX, mouseY = pygame.mouse.get_pos()
                if 250 <= mouseX <= 450 and 750 <= mouseY <= 770:
                    parametros.sonido_muteado = not parametros.sonido_muteado
                    if parametros.sonido_muteado:
                        parametros.musica_fondo_fx.set_volume(0)
                    else:
                        parametros.musica_fondo_fx.set_volume(0.008)

        funciones.dibujar_fondo(parametros.ventana, parametros.fondo)
        titulo = parametros.texto_intro.render("Galaxy Game", 1, (255, 0, 0))
        controles = parametros.texto_intro.render("Enter para continuar", 1, (255, 255, 255))
        salir = parametros.texto_intro.render("Q para salir", 1, (255, 255, 255))
        volumen = parametros.texto_intro.render("Presione para mutear", 1, (255, 255, 255))

        parametros.ventana.blit(titulo, ((parametros.ancho_ventana // 2) - (titulo.get_width() // 2), 20))
        parametros.ventana.blit(controles, (int((parametros.ancho_ventana // 2) - controles.get_width() // 2), 60))
        parametros.ventana.blit(salir, (int((parametros.ancho_ventana // 2) - controles.get_width() // 2), 100))
        parametros.ventana.blit(volumen, ((parametros.ancho_ventana // 2) - (volumen.get_width() // 2), 750))

        nombre_texto = parametros.texto_intro.render(f"Ingrese su nombre: {parametros.input_nombre}", 1, (255, 255, 255))
        parametros.ventana.blit(nombre_texto, (int((parametros.ancho_ventana // 2) - nombre_texto.get_width() // 2), 150))

        tecla = pygame.key.get_pressed()
        if(tecla[pygame.K_RETURN] and not parametros.nombre_ingresado):
            parametros.nombre = parametros.input_nombre
            parametros.nombre_ingresado = True
            print(parametros.input_nombre)
        if(tecla[pygame.K_q]):
            quit()

        pygame.display.update()

    while parametros.status and not parametros.game_over:

        

        funciones.dibujar_fondo(parametros.ventana, parametros.fondo)
        
        tiempo = pygame.time.get_ticks()
        contador_tiempo_transcurrido = tiempo - parametros.contador_tiempo_anterior

        temp = parametros.txt_contador.render("Temporizador: " + str(parametros.contador), 1, (255, 255, 255))
        parametros.ventana.blit(temp, (10, 750))

        puntos = parametros.txt_puntos.render("Puntaje " + str(parametros.puntaje), 1, (255, 255, 255))
        parametros.ventana.blit(puntos,(300, 10))

        lvl = parametros.txt_puntos.render("Nivel " + str(parametros.nivel), 1, (255, 255, 255))
        parametros.ventana.blit(lvl,(10, 10))

        try:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    parametros.status = False
        except:
            print("Error")

        if contador_tiempo_transcurrido >= 1000:
            parametros.contador += 1
            parametros.contador_tiempo_anterior = tiempo

        if len(nave.alien_group) == 0 and parametros.nivel < 2:
            parametros.nivel += 1
            parametros.alien_cooldown -= 300
            funciones.create_aliens(parametros.filas, parametros.columnas, nave.Enemies, nave.alien_group)

        if parametros.puntaje == 40 and parametros.nivel == 2:
            parametros.nivel = 3
            nave.boss_final = nave.BossFinal(250, 300, 10)
            nave.boss_group.add(nave.boss_final)
            
        if parametros.puntaje == 50:
            parametros.status = False
            parametros.flag_gana = True

        if nave.boss_group and tiempo - parametros.ultimo_disparo_boss > parametros.boss_cooldown:
            boss_disparando = random.choice(nave.boss_group.sprites())
            boss_bala = nave.Boss_Bullets(boss_disparando.rect.centerx, boss_disparando.rect.bottom)
            nave.boss_bullets_group.add(boss_bala)
            parametros.ultimo_disparo_boss = tiempo

        if nave.alien_group and tiempo - parametros.ultimo_disparo_alien > parametros.alien_cooldown:
            alien_disparando = random.choice(nave.alien_group.sprites())    
            alien_bala = nave.Enemie_Bullets(alien_disparando.rect.centerx, alien_disparando.rect.bottom)
            nave.alien_balas_group.add(alien_bala)
            parametros.ultimo_disparo_alien = tiempo
        else:
            pass

        if parametros.flag_gana:
            cursor.execute("INSERT INTO player_scores (name, score) VALUES (?, ?)", (parametros.nombre, parametros.puntaje))
            conexion.commit()            
        
        if parametros.game_over:
            print("1")
            parametros.status = False
            parametros.game_over = True

        nave.nave_player.update()
        nave.balas_group.update()
        nave.misil_group.update()
        nave.alien_group.update()
        nave.alien_balas_group.update()
        nave.explosion_group.update()
        nave.boss_group.update()
        nave.boss_bullets_group.update()

        nave.nave_group.draw(parametros.ventana)
        nave.balas_group.draw(parametros.ventana)
        nave.misil_group.draw(parametros.ventana)
        nave.alien_group.draw(parametros.ventana)
        nave.alien_balas_group.draw(parametros.ventana)
        nave.explosion_group.draw(parametros.ventana)
        nave.boss_group.draw(parametros.ventana)
        nave.boss_bullets_group.draw(parametros.ventana)


        pygame.display.update()
        parametros.clock.tick(60)

    cursor.execute("SELECT name, score FROM player_scores ORDER BY score DESC LIMIT 5")
    puntuaciones = cursor.fetchall()


    while parametros.flag_gana == True:
        parametros.clock.tick(60)
        try:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    quit()
        except Exception as ex:
            print(ex)
        
        funciones.dibujar_fondo(parametros.ventana, parametros.fondo)
        titulo = parametros.texto_intro.render("Galaxy Game", 1, (255, 0, 0))
        score = parametros.texto_intro.render("Score: " + str(parametros.puntaje), 1, (255, 255, 255))
        salir = parametros.texto_intro.render("Q para salir", 1, (255, 255, 255))
        volumen = parametros.texto_intro.render("R para volver a jugar", 1, (255, 255, 255))
        
        parametros.ventana.blit(volumen, ((parametros.ancho_ventana // 2) - (volumen.get_width() // 2), 750))
        parametros.ventana.blit(titulo, ((parametros.ancho_ventana // 2) - (titulo.get_width() // 2), 20))
        parametros.ventana.blit(score, (int((parametros.ancho_ventana // 2) - controles.get_width() // 2), 60))
        parametros.ventana.blit(salir, (int((parametros.ancho_ventana // 2) - controles.get_width() // 2), 100))

        y_pos = 150
        for nombre, score in puntuaciones:
            texto_puntuacion = parametros.texto_intro.render(f"{nombre}: {score}", 1, (255, 255, 255))
            parametros.ventana.blit(texto_puntuacion, (int((parametros.ancho_ventana // 2) - texto_puntuacion.get_width() // 2), y_pos))
            y_pos += 30

        tecla = pygame.key.get_pressed()
        if(tecla[pygame.K_q]):
            quit()
        if(tecla[pygame.K_r]):
            parametros.flag_intro = True
            parametros.flag_gana = False
            parametros.game_over = False
            parametros.nivel = 0
            parametros.alien_cooldown = 1000
            parametros.ultimo_disparo_boss = 0
            parametros.ultimo_disparo_alien = 0
            nave.nave_player.vida_restante = 3
            nave.nave_group.add(nave.nave_player)
            parametros.input_nombre = ""
            parametros.nombre_ingresado = False
            parametros.puntaje = 0
            parametros.contador = 0

        pygame.display.update()

    while parametros.game_over:
        
        parametros.clock.tick(60)
        try:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    quit()
        except Exception as ex:
            print(ex)

        funciones.dibujar_fondo(parametros.ventana, parametros.fondo)
        titulo_perdiste = parametros.texto_intro.render("¡Perdiste!", 1, (255, 0, 0))
        score = parametros.texto_intro.render("Score: " + str(parametros.puntaje), 1, (255, 255, 255))
        salir_perdiste = parametros.texto_intro.render("Q para salir", 1, (255, 255, 255))
        volumen = parametros.texto_intro.render("R para volver a jugar", 1, (255, 255, 255))
        
        parametros.ventana.blit(volumen, ((parametros.ancho_ventana // 2) - (volumen.get_width() // 2), 750))
        parametros.ventana.blit(titulo_perdiste, ((parametros.ancho_ventana // 2) - (titulo_perdiste.get_width() // 2), 20))
        parametros.ventana.blit(score, (int((parametros.ancho_ventana // 2) - controles.get_width() // 2), 60))
        parametros.ventana.blit(salir_perdiste, (int((parametros.ancho_ventana // 2) - salir_perdiste.get_width() // 2), 100))

        y = 150
        for nombre, score in puntuaciones:
            texto_puntuacion = parametros.texto_intro.render(f"{nombre}: {score}", 1, (255, 255, 255))
            parametros.ventana.blit(texto_puntuacion, (int((parametros.ancho_ventana // 2) - texto_puntuacion.get_width() // 2), y))
            y += 30
        
        tecla = pygame.key.get_pressed()
        if(tecla[pygame.K_q]):
            quit()
        if(tecla[pygame.K_r]):
            parametros.flag_intro = True
            parametros.game_over = False
            nave.nave_player.vida_restante = 3
            nave.nave_group.add(nave.nave_player)
            parametros.nivel = 0
            parametros.alien_cooldown = 1000
            parametros.input_nombre = ""
            parametros.nombre_ingresado = False
            parametros.puntaje = 0
            parametros.contador = 0
            
        pygame.display.update()

conexion.close()
pygame.quit()