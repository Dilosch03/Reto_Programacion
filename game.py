import math as mth
import pygame as pg
import aux_funtions as af


ALTURA = 720
LARGO = 1080
FPS = 60
BOXZONESIZE = [LARGO-int(LARGO*0.05)*2, ALTURA-int(ALTURA*0.05)*2]



def main(num_jugadores):
    WINDOW = pg.display.set_mode((LARGO,ALTURA))
    
    runinng = True

    clock = pg.time.Clock()
    TAMAÑO_TABLERO = [5,5]
    BOXSIZE = [int(BOXZONESIZE[0] / TAMAÑO_TABLERO[0]),int(BOXZONESIZE[1] / (TAMAÑO_TABLERO[1]+1))]
    BOXSIZE = [BOXSIZE[0] - BOXSIZE[0] * 0.07,BOXSIZE[1] - BOXSIZE[1] * 0.07]  
    Scores = [0]*num_jugadores
    pg.font.init() 
    font = pg.font.SysFont('Arial', 30)
    

    position_matrix = []
    discard_index = []
    
    question_matrix,answres_matrix,headers,warning = af.string_loder(TAMAÑO_TABLERO)

    popup_type = "Warning"
    if question_matrix == "err":
        popup_type = "Critical error"
        warning.insert(0,"Juego no puede ejecutarse.")
    
    if len(warning)>0:
        runinng = af.popup(warning,popup_type)

    WINDOW.fill(af.BLUE)

    for num_heder,heder in enumerate(headers):
        _x = int(LARGO * 0.05) + (int(BOXSIZE[0] * 0.1) + BOXSIZE[0]) * (num_heder - TAMAÑO_TABLERO[0] * mth.floor(num_heder / TAMAÑO_TABLERO[0]))
        _y = int(ALTURA * 0.03)

        position_matrix.append([_x,_y,af.GREEN])

        pg.draw.rect(WINDOW,af.GREEN, pg.Rect(_x,_y,BOXSIZE[0],BOXSIZE[1]))
        superficie = font.render(heder,True,af.BLACK)
        text_rect = superficie.get_rect(center = (_x+BOXSIZE[0]//2,_y+BOXSIZE[1]//2))
        WINDOW.blit(superficie,text_rect)
        pg.display.flip()

    for num_box in range(TAMAÑO_TABLERO[0] * TAMAÑO_TABLERO[1]):
        _x = int(LARGO * 0.05) + (int(BOXSIZE[0] * 0.1) + BOXSIZE[0]) * (num_box - TAMAÑO_TABLERO[0] * mth.floor(num_box / TAMAÑO_TABLERO[0]))
        _y = int(ALTURA * 0.18) + (int(BOXSIZE[1] * 0.1) + BOXSIZE[1]) * mth.floor(num_box / TAMAÑO_TABLERO[0])

        position_matrix.append([_x,_y,af.RED])

        pg.draw.rect(WINDOW,af.RED, pg.Rect(_x,_y,BOXSIZE[0],BOXSIZE[1]))
        puntos = str(((num_box // TAMAÑO_TABLERO[0])+1)*100)
        superficie = font.render(puntos,True,af.AQUA)
        text_rect = superficie.get_rect(center = (_x+BOXSIZE[0]//2,_y+BOXSIZE[1]//2))
        WINDOW.blit(superficie,text_rect)
        pg.display.flip()


    pg.display.update()

    escena = 0
    current_team = 0
    turn = 0
    points = 0

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
                
                if(escena == 0):
                    index = af.click_in_box(position_matrix,mouse,BOXSIZE)
                    
                    if index == None or (index in discard_index):
                        break

                    discard_index.append(index)
                    position_matrix[index][2] = af.GREY
                    escena = abs(escena-1)
                    points = int(question_matrix[index][1])
                    af.question_screen(question_matrix[index][0],answres_matrix[index][:4],BOXZONESIZE,font,WINDOW,[LARGO,ALTURA])
                    start_turn = turn
                else:
                    
                    correct = af.answer_detect(mouse,answres_matrix[index][4:],answres_matrix[index][:4],BOXZONESIZE,WINDOW,font,[LARGO,ALTURA])

                    pg.time.wait(int(1000*0.5))

                    if correct:
                        escena = abs(escena-1) 
                        af.selection_screen(position_matrix,headers,BOXSIZE,TAMAÑO_TABLERO,font,WINDOW)
                        Scores[current_team] += points
                    elif ((turn - start_turn) > 1):
                        escena = abs(escena-1) 
                        af.selection_screen(position_matrix,headers,BOXSIZE,TAMAÑO_TABLERO,font,WINDOW)

                    turn += 1
                    current_team = turn - num_jugadores * (turn // num_jugadores)
                    
                    
        

        if draw:
            pg.display.update()
        
        if (len(discard_index) == TAMAÑO_TABLERO[0]*TAMAÑO_TABLERO[1]):
            WINDOW.fill(af.BLUE)
            new_box = [BOXZONESIZE[0]//2,BOXZONESIZE[1]//num_jugadores]
            if new_box[1] > BOXSIZE[1]:
                new_box[1] = BOXSIZE[1]
            
            for team in range(num_jugadores*2):
                _x = int(LARGO * 0.05) + (int(BOXSIZE[0] * 0.1) + BOXSIZE[0]) * (num_box - 2 * mth.floor(num_box // 2))
                _y = int(ALTURA * 0.18) + (int(BOXSIZE[1] * 0.1) + BOXSIZE[1]) * mth.floor(num_box // 2)

                pg.draw.rect(WINDOW,af.RED, pg.Rect(_x,_y,BOXSIZE[0],BOXSIZE[1]))
                puntos = str(((num_box // TAMAÑO_TABLERO[0])+1)*100)
                superficie = font.render(puntos,True,af.AQUA)
                text_rect = superficie.get_rect(center = (_x+BOXSIZE[0]//2,_y+BOXSIZE[1]//2))
                WINDOW.blit(superficie,text_rect)
                pg.display.flip()


    
    pg.quit()

if __name__ == "__main__":
    num_jugadores = input("Numero de equipos: ")
    if num_jugadores.isnumeric():
        num_jugadores = int(num_jugadores)
        if num_jugadores<2:
            num_jugadores = 2
            print("Numero de equipos tiene que ser mayor a 1.")
    else:
        num_jugadores = 2
        print("Tiene que ser un numero mayor a 1.")
    
    print()
    print("Numero de equipos: " + str(num_jugadores))
    pg.time.wait(500)
    print("Initializing...")
    pg.time.wait(1000)

    main(num_jugadores)
    print("Done.")