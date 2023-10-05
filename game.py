import math as mth
import pygame as pg
import os


ALTURA = 720
LARGO = 1080
WINDOW = pg.display.set_mode((LARGO,ALTURA))
FPS = 60
BOXZONESIZE = [LARGO-int(LARGO*0.05)*2, ALTURA-int(ALTURA*0.05)*2]
NUM_JUGADORES = 2
PATH=os.getcwd()

BLUE = (40,40,240)

WHITE = (250,250,250)
BLACK = (0,0,0)

RED = (250,40,40)
ORANGE = (250,75,0)
GREEN = (40,250,40)
YELLOW = (250,250,40)
PINK = (250,40,250)
PURPLE = (125,0,125)
AQUA = (0,150,135)
BROWN = (110, 35, 25)
LIGHTBLUE = (55, 210, 250)

teams = [WHITE,BLACK]

COLORES = [BLUE,RED,ORANGE,YELLOW,GREEN,AQUA,LIGHTBLUE,PINK,PURPLE,BROWN]

def sting_loder(Tablero_size):
    question_matrix = []
    answer_matrix = []
    file = PATH + "/questions.txt"
    file = open(file)
    file = file.read()
    for line in file:
        text = line.split(" ")
        question_matrix.append(text[0])
        answer_matrix.append(text[1])


def update_box(index,turn,position,BOXSIZE):
    _x = position[index][0]
    _y =  position[index][1]

    pg.draw.rect(WINDOW,teams[turn], pg.Rect(_x,_y,BOXSIZE[0],BOXSIZE[1]))
    pg.display.flip()


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
    BOXSIZE = [int(BOXZONESIZE[0] / TAMAÑO_TABLERO[0]),int(BOXZONESIZE[1] / TAMAÑO_TABLERO[1])]
    BOXSIZE = [BOXSIZE[0] - BOXSIZE[0] * 0.07,BOXSIZE[1] - BOXSIZE[1] * 0.07]  
    Scores = [0]*NUM_JUGADORES

    position_matrix = []
    discard_index = []
    tablero = ["N/A"] * 9
    for i in range(len(tablero)):
        tablero[i] = [["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"]]
    
    

    WINDOW.fill(BLUE)

    for num_box in range(TAMAÑO_TABLERO[0] * TAMAÑO_TABLERO[1]):
        _x = int(LARGO * 0.05) + (int(BOXSIZE[0] * 0.1) + BOXSIZE[0]) * (num_box - TAMAÑO_TABLERO[0] * mth.floor(num_box / TAMAÑO_TABLERO[0]))
        _y = int(ALTURA * 0.05) + (int(BOXSIZE[1] * 0.1) + BOXSIZE[1]) * mth.floor(num_box / TAMAÑO_TABLERO[0])

        position_matrix.append([_x,_y])
        colorid = mth.floor((mth.floor(num_box / 3) - 3 * mth.floor(num_box/TAMAÑO_TABLERO[0])) + 3 * mth.floor(num_box / (3 * TAMAÑO_TABLERO[0]))) + 1
        color = COLORES[colorid]

        pg.draw.rect(WINDOW,color, pg.Rect(_x,_y,BOXSIZE[0],BOXSIZE[1]))
        pg.display.flip()


    pg.display.update()
    turn = 0
    while runinng:
        clock.tick(FPS)
        draw = False

        for event in pg.event.get():

            if event.type == pg.QUIT:
                runinng = False
                break

            elif event.type == pg.MOUSEBUTTONDOWN:
                draw = True
                pg.font.init() 
                my_font = pg.font.SysFont('Comic Sans MS', 30)
                mouse = pg.mouse.get_pos()

                index = click_in_box(position_matrix,mouse,BOXSIZE)
                
                if index == None or (index in discard_index):
                    break

                big_matrix = mth.floor(index / 3) - 3 * mth.floor(index/TAMAÑO_TABLERO[0]) + 3 * mth.floor(index / (3 * TAMAÑO_TABLERO[0]))
                smol_matrix = [(index - TAMAÑO_TABLERO[0] * mth.floor(index / TAMAÑO_TABLERO[0]) - 3 * mth.floor((index - TAMAÑO_TABLERO[0] * mth.floor(index / TAMAÑO_TABLERO[0]))/3)),mth.floor(index / TAMAÑO_TABLERO[0]) - 3 * mth.floor((index / TAMAÑO_TABLERO[0]) / 3)]
                
                tablero[big_matrix][smol_matrix[0]][smol_matrix[1]] = turn
                check = False
                for l in range(7):
                    if l < 3:
                        check = ((tablero[big_matrix][l][0] == turn) and (tablero[big_matrix][l][2] == turn) and (tablero[big_matrix][l][1] == turn))
                        if check:
                            break
                    elif l < 6:
                        l = l-3
                        check = ((tablero[big_matrix][0][l] == turn) and (tablero[big_matrix][2][l] == turn) and (tablero[big_matrix][1][l] == turn))
                        if check:
                            break
                    else:
                        check = ((tablero[big_matrix][0][0] == turn) and (tablero[big_matrix][2][2] == turn) and (tablero[big_matrix][1][1] == turn))
                        if check:
                            break
                        check = ((tablero[big_matrix][0][2] == turn) and (tablero[big_matrix][2][0] == turn) and (tablero[big_matrix][1][1] == turn))

                if check:
                    for i in range(9):
                        id = mth.floor(((i - 3 * mth.floor(i / 3)) + TAMAÑO_TABLERO[0] * mth.floor(i / 3)) + 3 * (big_matrix-3*mth.floor(big_matrix/3)) + (3 * TAMAÑO_TABLERO[0] * mth.floor(big_matrix / 3)))
                        update_box(id,turn,position_matrix,BOXSIZE)
                    tablero[big_matrix] = turn

                    for l in range(7):
                        if l < 3:
                            check = ((isinstance(tablero[l],int)) and (isinstance(tablero[l + 5],int)) and (isinstance(tablero[l + 2],int)))
                            if check:
                                check = ((tablero[l] == turn) and (tablero[l + 5] == turn) and (tablero[l + 2] == turn))
                                if check:
                                    break
                        elif l < 6:
                            j = l-2+2*(l-3)
                            check = ((isinstance(tablero[j - 1],int)) and (isinstance(tablero[j + 1],int)) and (isinstance(tablero[j],int)))
                            if check:
                                check = ((tablero[j] == turn) and (tablero[j - 1] == turn) and (tablero[j + 1] == turn))
                                if check:
                                    break
                        else:
                            check = ((isinstance(tablero[0],int)) and (isinstance(tablero[7],int)) and (isinstance(tablero[4],int)))
                            if check:
                                check = ((tablero[0] == turn) and (tablero[7] == turn) and (tablero[4] == turn))
                                if check:
                                    break
                            check = ((isinstance(tablero[2],int)) and (isinstance(tablero[6],int)) and (isinstance(tablero[4],int)))
                            if check:
                                check = ((tablero[2] == turn) and (tablero[6] == turn) and (tablero[4] == turn))
                            
                    if(check):
                        tablero = turn

                        
                        
                update_box(index,turn,position_matrix,BOXSIZE)

                discard_index.append(index)
                turn = abs(turn-1)
        

        if draw:
            pg.display.update()
        
        if (isinstance(tablero,int)):
            for i in range(len(position_matrix)):
                update_box(i,abs(turn - 1),position_matrix,BOXSIZE)
            pg.display.update()

    
    pg.quit()

if __name__ == "__main__":
    main()