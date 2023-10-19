import csv
import os
import pygame as pg
import random as rd
import tkinter as tk
import math as mth

def string_loder(Tablero_size):
    #carga de los temas y sus preguntas con la validacion del documento "jeopardy_questions.csv"
    question_matrix = []
    questionare_matrix = []
    answer_matrix = []
    headers = []
    errores = []
    
    MAIN_PATH = os.path.dirname(__file__)
    FILE = "jeopardy_questions.csv"
    PATH = os.path.join(MAIN_PATH,FILE)

    if not(os.path.isfile(PATH)):
        return "err","err","err", ["Archivo de preguntas no se encuentra."]

    with open(PATH, newline='',encoding="utf-8") as csvfile:
        has_header = csv.Sniffer().has_header(csvfile.readline())
        csvfile.seek(0)  
        reader = csv.reader(csvfile)

        if has_header:
            next(reader)  
        
        num = [0,0]
        flag = True

        for row in reader:
            index_error = 0
            flag = False
            if len(row)==0:
                continue

            if row[0] in headers:
                index =  int(headers.index(row[0]))
                
            else:
                headers.append(row[0])
                questionare_matrix.append([])
                index = int(len(headers)-1.)
            
            err = False

            for element in row:
                if (element==""):
                    err = True
                    break
            
            for element in row[6:10]:
                    if not(element.lower() in ['false','true','verdadero','falso']):
                        err = True
                        index_error = 1
                        break


            
            if err:
                num[index_error]+=1
                continue


            questionare_matrix[index].insert(0,row)
        
        if flag:
            errores.append("Archivo no contiene preguntas.")

        if(num[0]>0):
            errores.append(str(num[0])+" preguntas no tienen todas las areas con datos.")
        
        if(num[1]>0):
            errores.append(str(num[1])+" preguntas no tienen correcto el formato de la tabla de verdad.")

    not_valid = []
    counter = [0,0,0,0]
    for i,theme in enumerate(questionare_matrix):
        _temp = [[],[],[],[],[]]

        if not(len(theme)>=Tablero_size[1]):
            not_valid.append(i)
            continue

        for question in theme:
            if not(len(question)==11):
                counter[0] += 1
                continue
            if not(question[10].isnumeric()):
                counter[1] += 1
                continue
            points = int(question[10])//100
            if not(points <= Tablero_size[1] and points>0):
                counter[2] += 1
                continue
            index = (points)-1
            _temp[index].insert(0,question)
        
        err = False

        for l,points in enumerate(_temp):
            if(len(points)<1):
                err = True
            rd.shuffle(points)
            _temp[l] = points

        if err:
            counter[3] += 1
            not_valid.append(i)
            continue

        questionare_matrix[i] = _temp

    caracteristica = [" el tamaño adecuado.",
                      " un numero en el area de puntos.",
                      " un valor dentro de rango para los puntos.",
                      " temas no tienen preguntas para todas las categorias de puntos."]
    
    for l,i in enumerate(counter):
        if i>0:
            text = " preguntas no tienen" + caracteristica[l]
            if (l == 3):
                text = caracteristica[l]
            
            errores.append(str(i)+text)

    not_valid.reverse()
    if len(not_valid)>0:
        errores.append(str(len(not_valid))+" temas no cumplen con el numero minimo de preguntas aceptadas.")

    for i in not_valid:
        del questionare_matrix[i]

    if not(len(questionare_matrix)>=Tablero_size[0]):
        errores.append("Numero de temas aceptados es menor al tamaño del tablero.")
        return "err","err","err", errores
    
    #elecion random de los temas que se utiliazran
    for i in range(len(questionare_matrix)):
        answer_matrix.append(i)
    
    rd.shuffle(answer_matrix)

    index = answer_matrix[0:Tablero_size[0]]
    answer_matrix = []
    headers = []

    for i in range(Tablero_size[1]):
        for l in index:
            if not(questionare_matrix[l][i][0][0] in  headers):
                headers.append(questionare_matrix[l][i][0][0])
            answer_matrix.append(questionare_matrix[l][i][0][2:10])
            question_matrix.append([questionare_matrix[l][i][0][1],questionare_matrix[l][i][0][10]])
            

    return question_matrix,answer_matrix,headers,errores


def update_box(index,turn,position,BOXSIZE,WINDOW,teams):
    _x = position[index][0]
    _y =  position[index][1]

    pg.draw.rect(WINDOW,teams[turn], pg.Rect(_x,_y,BOXSIZE[0],BOXSIZE[1]))
    pg.display.flip()


def click_in_box(position_matrix,mouse,BOXSIZE):
    index = None
    for i,position in enumerate(position_matrix):
        in_range_x = (position[0] < mouse[0] and position[0] + BOXSIZE[0] > mouse[0])
        in_range_y = (position[1] < mouse[1] and position[1] + BOXSIZE[1] > mouse[1])

        hover = in_range_y and in_range_x
        if hover:
            index = i
            break
    return index

def selection_screen(position,heders,BOXSIZE,tamaño_tablero,font,WINDOW):
    WINDOW.fill(BLUE)
    for i,element in enumerate(position):
        pg.draw.rect(WINDOW,element[2], pg.Rect(element[0],element[1],BOXSIZE[0],BOXSIZE[1]))

        puntos = str((i // tamaño_tablero[0])*100)
        color = AQUA

        if i<tamaño_tablero[0]:
            puntos = heders[i]
            color = BLACK

        superficie = font.render(puntos,True,color)
        text_rect = superficie.get_rect(center = (element[0]+BOXSIZE[0]//2,element[1]+BOXSIZE[1]//2))

        WINDOW.blit(superficie,text_rect)
        pg.display.flip()

def question_screen(question,answes,size,font,WINDOW,window_size):
    sub_area = [size[0],size[1] // 2]
    _x = int(window_size[0] * 0.05)
    _y = int(window_size[1] * 0.05)
    WINDOW.fill(BLUE)
    pg.draw.rect(WINDOW,RED, pg.Rect(_x,_y,sub_area[0],sub_area[1]))
    superficie = font.render(question,True,BLACK)
    text_rect = superficie.get_rect(center = (_x + sub_area[0] // 2,_y + sub_area[1] // 2))
    WINDOW.blit(superficie,text_rect)

    box_size = [sub_area[0] // 2,sub_area[1] // 2]
    box_size = [box_size[0] - box_size[0] * 0.07,box_size[1] - box_size[1] * 0.07]

    for num_box,text in enumerate(answes):
        _x = int(window_size[0] * 0.05) + (int(box_size[0] * 0.159) + box_size[0]) * (num_box - 2 * (num_box // 2))
        _y = int(window_size[1] * 0.06) + sub_area[1] + (int(box_size[1] * 0.1) + box_size[1]) * (num_box // 2)

        pg.draw.rect(WINDOW,LIGHTBLUE, pg.Rect(_x,_y,box_size[0],box_size[1]))
        superficie = font.render(answes[num_box],True,BLACK)
        text_rect = superficie.get_rect(center = (_x+box_size[0]//2,_y+box_size[1]//2))
        WINDOW.blit(superficie,text_rect)

def answer_detect(mouse,truth_list,answes,size,WINDOW,font,window_size):
    box_size = [size[0] // 2,size[1] // 4]
    box_size = [box_size[0] - box_size[0] * 0.07,box_size[1] - box_size[1] * 0.07]

    result = False
    inbox = False
    for num_box,_bool in enumerate(truth_list):
        _x = int(window_size[0] * 0.05) + (int(box_size[0] * 0.159) + box_size[0]) * (num_box - 2 * (num_box // 2))
        _y = int(window_size[1] * 0.06) + (size[1] // 2) + (int(box_size[1] * 0.1) + box_size[1]) * (num_box // 2)

        in_range_x = (_x < mouse[0] and _x + box_size[0] > mouse[0])
        in_range_y = (_y < mouse[1] and _y + box_size[1] > mouse[1])

        hover = in_range_y and in_range_x
        color = RED

        if hover:
            inbox = True
            if (_bool.lower() in ["true","verdadero"]):
                color = GREEN
                result = True

            pg.draw.rect(WINDOW,color, pg.Rect(_x,_y,box_size[0],box_size[1]))
            superficie = font.render(answes[num_box],True,BLACK)
            text_rect = superficie.get_rect(center = (_x+box_size[0]//2,_y+box_size[1]//2))
            WINDOW.blit(superficie,text_rect)
            break

    if not inbox:
        result = None

    pg.display.update()
    return result


def popup(warning,type):
    window = tk.Tk()

    window.title(type)

    color = "red"
    if type == "Warning" :
        color = "yellow"

    tk.Label(window,text=type,bg=color).pack()
    tk.Label(window,text="").pack()
    for text in warning:
        tk.Label(window,text=text).pack()

    tk.Button(window,text=" OK ",command=window.destroy).pack(pady=20)

    window.mainloop()

    if type == "Warning" :
        return True 
    return False


def score_sort(arr):
    teams =[]
    for i in range(len(arr)):
        teams.append(i)
        arr[i] = arr[i]//100


    _min = min(arr)
    _max = max(arr)

    temp_arr = [0]*(_max-_min+1)
    temp_arr_2 = [0]*(_max-_min+1)

    for j,i in enumerate(arr):
        temp_arr[i-_min] += 1
        if not(temp_arr_2[i-_min] == 0):
            if hasattr(temp_arr_2[i-_min],"__len__"):
                temp_arr_2[i-_min].append(teams[j])
            else:
                temp_arr_2[i-_min] = [temp_arr_2[i-_min],teams[j]]
        else:
            temp_arr_2[i-_min] = teams[j]

        
    arr = []
    teams = []

    for i,j in enumerate(temp_arr):
        for l in range(j):
            arr.append(_min+i)
        if not(j==0):
            if hasattr(temp_arr_2[i],"__len__"):
                temp_arr_2[i].reverse()
                for element in temp_arr_2[i]:
                    teams.append(element)
            else:
                teams.append(temp_arr_2[i])

    for i,element in enumerate(arr):
        arr[i] = element*100
    
    arr.reverse()
    teams.reverse()

    return arr,teams

def restauracion(path,exist):
    text = "altura de la ventana:720\nlargo de la ventana:1080\nnumero de equipos base:2\nFPS:60\nnumero de temas:5\numero de preguntas por tema:5"
    if not exist:
        open(path,"x")
    
    File = open(path,"w")
    File.write(text)
    File.close()
    

def load_constants():
    #carga de las constantes almacenadas en el archivo "config.txt" y si validacion
    constants = []
    FILE = "config.txt"
    MAIN_PATH = os.path.dirname(__file__)
    PATH = os.path.join(MAIN_PATH,FILE)

    if not(os.path.isfile(PATH)):
        popup(["Archivo config no se encuentra.","Restaurando archivo config"],"Warning")
        restauracion(PATH,False)
        return "err","err","err","err"

    File = open(PATH,"r")
    text = File.read().split("\n")
    File.close()

    if not(len(text) == 6):
        popup(["Numero de constantes en archivo config no es el esperado.","Restaurando archivo config"],"Warning")
        restauracion(PATH,True)
        return "err","err","err","err"

    err = 0
    for element in text:
        element = element.split(":")
        element = element.pop()
        
        if element.isnumeric():
            element = int(element)
            constants.append(element)

        else:
            err += 1
        
    if err>0:
        popup([str(err)+" constantes no tienen valor numerico.","Restaurando archivo config"],"Warning")
        restauracion(PATH,True)
        return "err","err","err","err"
    
    return constants[0],constants[1],constants[2],constants[3],[constants[4],constants[5]]
    
def team_turn(turn,box_size,window_size,WINDOW,font,tablero_y):
    centro = window_size[0]//2
    _x = centro-(centro*0.3)
    y_min = int(window_size[1] * 0.17) + (int(box_size[1] * 0.1) + box_size[1]) * tablero_y
    diference = window_size[1] - y_min

    text = "Turno de equipo " + str(turn+1)
    pg.draw.rect(WINDOW,AQUA, pg.Rect(_x,y_min,(centro*0.6),diference))
    superficie = font.render(text,True,BLACK)
    text_rect = superficie.get_rect(center = (centro,y_min + (diference//2)))
    WINDOW.blit(superficie,text_rect)
    pg.display.flip()


BLUE = (40,40,240)

WHITE = (250,250,250)
GREY = (125,125,125)
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

