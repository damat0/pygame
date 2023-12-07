import parametros

def dibujar_fondo(ventana, fondo):
    ventana.blit(fondo, (-60, 0))

def actualizar_puntaje():
    parametros.puntaje += 1

def create_aliens(filas, columnas, Enemies, alien_group):
    for fila in range(filas):
        for columna in range(columnas):
            alien = Enemies(50 + columna * 100, 100 + fila * 70)
            alien_group.add(alien)
