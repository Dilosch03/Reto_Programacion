import math as mth
import pygame as pg
import os


ALTURA = 500
LARGO = 900
WINDOW = pg.display.set_mode((LARGO,ALTURA))
FPS = 60
BOXZONESIZE = [LARGO-int(LARGO*0.05)*2, ALTURA-int(ALTURA*0.05)*2]
NUM_JUGADORES = 2
PATH=os.getcwd()

BLUE = (40,40,240)

RED = (250,40,40)
ORANGE = (250,75,0)
GREEN = (40,250,40)
YELLOW = (250,250,40)
PINK = (250,40,250)
PURPLE = (125,0,125)
AQUA = (0,150,135)
BROWN = (110, 35, 25)
LIGHTBLUE = (55, 210, 250)


COLORES = [BLUE,RED,ORANGE,YELLOW,GREEN,AQUA,LIGHTBLUE,PINK,PURPLE,BROWN]

def sting_loder(Tablero_size):
    question_matrix = []
    answer_matrix = []
    file = PATH + "/questions.txt"
    file = open(file)
    for line in file:
        text = line.split(" ")
        question_matrix.append(text[0])
        answer_matrix.append(text[1])


def click_in_box(position_matrix,mouse,BOXSIZE):
    index = None
    for i,position in enumerate(position_matrix):
        in_range_x = (position[0]< mouse[0] and position[0]+BOXSIZE[0] > mouse[0])
        in_range_y = (position[1]< mouse[1] and position[1]+BOXSIZE[1] > mouse[1])

        hover = in_range_y and in_range_x
        if hover:
            index = i
            break
    return index


def main():
    runinng = True

    clock = pg.time.Clock()
    TAMAÑO_TABLERO = [9,9]
    BOXSIZE = [int(BOXZONESIZE[0]/TAMAÑO_TABLERO[0]),int(BOXZONESIZE[1]/TAMAÑO_TABLERO[1])]
    BOXSIZE = [BOXSIZE[0]-BOXSIZE[0]*0.07,BOXSIZE[1]-BOXSIZE[1]*0.07]  
    Scores = [0]*NUM_JUGADORES

    position_matrix = []
    

    WINDOW.fill(BLUE)

    for num_box in range(TAMAÑO_TABLERO[0]*TAMAÑO_TABLERO[1]):
        _x = int(LARGO * 0.05) + (int(BOXSIZE[0] * 0.1) + BOXSIZE[0]) * (num_box - TAMAÑO_TABLERO[0] * mth.floor(num_box / TAMAÑO_TABLERO[0]))
        _y = int(ALTURA * 0.05) + (int(BOXSIZE[1] * 0.1) + BOXSIZE[1]) * mth.floor(num_box / TAMAÑO_TABLERO[0])

        position_matrix.append([_x,_y])
        colorid = mth.floor((mth.floor(num_box/3)-3*mth.floor(num_box/TAMAÑO_TABLERO[0]))+3*mth.floor(num_box/(3*TAMAÑO_TABLERO[0])))+1
        color = COLORES[colorid]

        pg.draw.rect(WINDOW,color, pg.Rect(_x,_y,BOXSIZE[0],BOXSIZE[1]))
        pg.display.flip()


    pg.display.update()
    while runinng:
        clock.tick(FPS)
        draw = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                runinng = False
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                draw = True
                mouse = pg.mouse.get_pos()
                index = click_in_box(position_matrix,mouse,BOXSIZE)
        

        if draw:
            pg.display.update()

                    
                    
                        
                    

                    
                        
                        

    
    pg.quit()

if __name__ == "__main__":
    main()