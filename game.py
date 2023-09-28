import numpy as np
import pygame as pg
import os


ALTURA = 500
LARGO = 900
WINDOW = pg.display.set_mode((LARGO,ALTURA))
FPS = 60

def darw_event():
    WINDOW.fill((40,40,240))

def main():
    clock = pg.time.Clock()
    TAMAÑO_TABLERO = [5,5]
    tablero = []   

    runinng = True

    while runinng:
        clock.tick(FPS)
        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    runinng = False

    
    pg.quit()

if __name__ == "__main__":
    main()