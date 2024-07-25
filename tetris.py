from tkinter import *
import random
import time
import sys
import os
import threading

interface = Tk()
interface.geometry("600x600")

# Classes

class selector():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.shape = canvas.create_rectangle((x,y,x+150,y+50), width = 5, outline = "red")
        self.scope = "Start"

class button():
    def __init__(self,x,y,name, tied_window):
        self.x = x 
        self.y = y
        self.name = name
        self.shape = canvas.create_rectangle((x,y,x+150,y+50), fill="grey", width = 2)
        self.text = canvas.create_text(x+75,y+25,text=name, font=("Arial", 15)) 
        self.tied_window = tied_window

class class_window():
    def __init__(self,name,color,x1,y1,x2,y2):
        self.shape = canvas.create_rectangle((x1,y1,x2,y2), fill=color, width = 0)
        self.name = name

class square():
    def __init__(self,row,column,a,b):
        self.row = row
        self.column = column
        self.a = a
        self.b = b
        self.occupier = "black" # color
        self.shape = canvas.create_rectangle(a,b,a+25,b+25, fill="black", width=0.5, outline = "white")    
        
        
canvas = Canvas(interface, bg = 'white', width = 600, height = 600)
canvas.pack()

def selector_mover(selector, delta_x, delta_y):
    print("selector_mover")
    selector.x += delta_x
    selector.y += delta_y
    canvas.moveto(selector.shape, selector.x-3, selector.y-3) #these are offset by -3 because otherwise they get offset by the moveto function for some reason

#fluid
def boundary_checker(curr_window, delta_y):
    print("boundary_checker")
    for i in range(len(curr_window.buttonlist)):
        print(curr_window.selector.y+delta_y, curr_window.buttonlist[i].y)
        if curr_window.selector.y+delta_y == curr_window.buttonlist[i].y:
            print(curr_window.buttonlist[i].name)
            return curr_window.buttonlist[i].name
    else:
        return False
    
def key_guide(curr_window, direction):
    print("KEY GUIDE ENGAGED")
    if curr_window == mainmenu:
        key_menu(curr_window, direction)
    if curr_window == gamewindow:
        key_game(curr_window, direction)
    if curr_window == highscore:
        key_highscore(curr_window, direction)        
    if curr_window == escape_window:
        key_escape(curr_window, direction)

# t1=threading.Thread(target=key_guide)
# t1.start()

def toggle_escape_window(curr_window, direction):
    global game_paused
    if escape_window.active == False:             
        print("keygame2")
        bring_to_front(escape_window)
        change_window(escape_window)
        escape_window.active = True
        game_paused = True
        return
    if escape_window.active == True:            
        print("keygame3")
        bring_to_front(prev_window)
        change_window(prev_window)
        escape_window.active = False
        game_paused = False
        g = threading.Thread(target=game_loop, args=()) # threading allows us to input while the loop is being ran. If I use just game_loop(), it won't work
        g.start()
        return

def key_game(curr_window, direction):
    print("keygame1")
    if direction == "escape":
        toggle_escape_window(curr_window, direction)
        
def key_highscore(curr_window, direction):
    if direction == "escape":
        bring_to_front(mainmenu)
        change_window(mainmenu)

def key_escape(curr_window, direction):
    if direction == "escape":
        toggle_escape_window(curr_window, direction)
    else:
        print("THIS IS THE CURRENT WINDOW IN KEY_ESCAPE", curr_window.name, direction)
        key_menu(curr_window, direction)
        

def key_menu(curr_window, direction):    
    if direction == ("right" or "left"):
        return
    elif direction == "up":
        d = boundary_checker(curr_window, -75) # this function returns text which is then assigned as an attribute to selector_mover
        if d != False:
            selector_mover(curr_window.selector, 0, -75)
            curr_window.selector.scope = d
    elif direction == "down":
        d = boundary_checker(curr_window, 75)
        if d != False:
            selector_mover(curr_window.selector, 0, 75)
            curr_window.selector.scope = d
    elif direction == "enter":
        select(curr_window, curr_window.selector)
        escape_window.active = False     

def select(curr_window, selector):
    print("we are here")
    print(selector.scope)
    # if selector.scope == "Start":
        # bring_to_front(gamewindow)
    for i in range(len(curr_window.buttonlist)):
        if selector.scope == "Exit":
            sys.exit()
        if selector.scope == curr_window.buttonlist[i].name:
            print("THIS IS IT",curr_window.buttonlist[i].name)
            bring_to_front(curr_window.buttonlist[i].tied_window)
            change_window(curr_window.buttonlist[i].tied_window)
            

def change_window(new_win):
        global curr_window, prev_window, game_started, game_paused, piece_queue
        prev_window = curr_window
        curr_window = new_win
        if curr_window == mainmenu:
            game_paused = False
            suppress_grid()
            canvas.tag_lower(escape_window.selector.shape) # I've added attributes to a completely unrelated window and it had an impact on the selector in another object. The bring to front
            piece_queue = []
            if game_started == True:
                game_started = False
        if curr_window == gamewindow:
            if game_started == False:
                game_started = True
                start_message()
            if game_started == True:
                g = threading.Thread(target=game_loop, args=()) # threading allows us to input while the loop is being ran. If I use just game_loop(), it won't wor
                g.start()

        
def bring_to_front(window):
    global prev_window
    print("THIS IS WINDOW", window)
    instance_dict = vars(window)
    print(instance_dict)
    for key in instance_dict.keys():
        value = instance_dict.get(key)
        print("This is the key",key, ", type", type(key))
        if isinstance(value,button) or isinstance(value,selector):
            print("button FOUND") # I can just put this through the function again.
            bring_to_front(value) # starts another instance of the same function 
        elif key == "score" or key == "level":
            pass
        elif key == "d":
            # for i in range(len(window.d)):
                # print("This iss"window.d[i])
                # canvas.tag_raise(window.d[i].shape)
            for x in value:
                print("this is the value", x)
                canvas.tag_raise(value[x].shape)
        else:
            # print(key)
            # print(type(instance_dict.get(key)))
            canvas.tag_raise(value)

def suppress_grid(): # This is a fix for something strange that happens when generating the grid. Random squares have a mind of their own and don't respond to the bring_to_front function as they should # Man I really dont want to use this
    for x in gamewindow.d:
        print("this is the value", x)
        canvas.tag_lower(gamewindow.d[x].shape)

# Status messages
        
def start_message():
        startrect = canvas.create_rectangle(200, 200, 400, 300, fill="orange", width=1, outline = "white")
        text = canvas.create_text(300,250,text="START", font=("Arial", 17))
        interface.after(1500, delete_message, startrect, text)

        
def delete_message(inv, txt):
    canvas.delete(inv, txt)

def game_loop():
    global interface, game_paused, piece_queue, counter, current_piece
    while game_paused == False:
        counter -= 1
        while len(piece_queue) < 4:
            print("appending to piece list")
            piece_queue_handler(piece_queue)
        if current_piece == False:
            current_piece = piece_queue[0]
            piece_queue.pop(0)
            piece_placer(current_piece)
        print(counter)
        board_updater()
        time.sleep(0.01)
        if counter == 0:
            counter = 200

def piece_placer(current_piece):
    global pieces_d, gamewindow
    print("current piece",current_piece)
    block_color = color_assign(current_piece)
    print(pieces_d[current_piece])
    print(type(pieces_d[current_piece]))
    for x in pieces_d[current_piece]:
        x.occupier = block_color

def board_updater():
    global gamewindow, canvas
    for i in gamewindow.d:
        gamewindow.d[i].shape = canvas.create_rectangle(gamewindow.d[i].a,gamewindow.d[i].b,gamewindow.d[i].a+25,gamewindow.d[i].b+25, fill=gamewindow.d[i].occupier, width=0.5, outline = "white")
        # canvas.itemconfig(gamewindow.d[i], fill=gamewindow.d[i].occupier)
        # canvas.update_idletasks
        # print(gamewindow.d[i].occupier)
    
def color_assign(current_piece):
    colorlist = ["cyan", "blue", "orange", "yellow", "green", "violet", "red"]
    choicelist = ["piece_I", "piece_J", "piece_L", "piece_O", "piece_S", "piece_T", "piece_Z"]
    index = choicelist.index(current_piece)
    color = colorlist[index]
    return color
    
    return current_piece
            
def piece_queue_handler(piece_queue):
    choicelist = ["piece_I", "piece_J", "piece_L", "piece_O", "piece_S", "piece_T", "piece_Z"] 
    piece_queue.append(random.choice(choicelist))
             
def debugprint():
    global curr_window, prev_window
    print(curr_window.name, "curr_window")
    print(prev_window.name, "prev_window")
    print(escape_window.active, "escape_window.active")
    
# Windows - Game
gamewindow = class_window("gamewindow","grey",0,0,600,600)
gamewindow.upnext_shape = canvas.create_rectangle((30,120,145,500), fill="black", width = 0.5, outline = "white")
gamewindow.upnext_text = canvas.create_text(85,105,text="UP NEXT", font=("Arial", 12))
gamewindow.level = 1
gamewindow.level_text = canvas.create_text(300,30,text=("Lv.",gamewindow.level), font=("Arial", 24))
gamewindow.score = 0
gamewindow.score_container = canvas.create_rectangle((450,120,570,150), fill="black", width = 0.5, outline = "white")
gamewindow.score_text = canvas.create_text(510,105,text="SCORE", font=("Arial", 12))
gamewindow.score_display = canvas.create_text(510,135,text=gamewindow.score, font=("Arial", 12),  fill = "white")
                
# Windows - Game - Grid
gamewindow.d = {}
for r in range(1,21):
    for c in range(1,11):
        gamewindow.d["sq_{0}_{1}".format(r,c)] = square(r,c,150+(c*25),40+(r*25))

# Windows - High Score
highscore = class_window("highscore","green",0,0,600,600)
highscore.text = canvas.create_text(300,50,text="High score", font=("Arial", 24))

# Windows - Main Menu
mainmenu = class_window("mainmenu","orange",0,0,600,600)
mainmenu.text = canvas.create_text(300,50,text="Tkinter Tetris", font=("Arial", 24))
mainmenu.startbutton = button(225,100,"Start", gamewindow)
mainmenu.placeholderbutton = button(225,175,"High Scores", highscore)
mainmenu.exitbutton = button(225,250,"Exit", "na")
mainmenu.selector = selector(225,100)
mainmenu.buttonlist = [mainmenu.startbutton, mainmenu.placeholderbutton, mainmenu.exitbutton]

        
# Windows - Escape
escape_window = class_window("escape","orange",150,450,450,150)
escape_window.active = False
escape_window.text = canvas.create_text(300,180,text="Game Paused", font=("Arial", 24))
escape_window.menubutton = button(225,250,"Main Menu", mainmenu)
escape_window.exitbutton = button(225,325,"Exit", "na")
escape_window.selector = selector(225,250)
escape_window.selector.scope = "Main Menu"
escape_window.buttonlist = [escape_window.menubutton, escape_window.exitbutton]

canvas.tag_raise(mainmenu.shape)
canvas.tag_lower(escape_window.selector.shape)
canvas.tag_lower(escape_window.selector.shape)

# Vars
        
curr_window = mainmenu
prev_window = "null"
game_started = False
game_paused = False
piece_queue = []
current_piece = False
counter = 200

bring_to_front(mainmenu)

# Dictionary to declare the relative column and row for each block
# declare everything on one row from left ro right before moving on to the next

pieces_d = { "piece_I" : [ gamewindow.d["sq_1_4"], gamewindow.d["sq_1_5"], gamewindow.d["sq_1_6"], gamewindow.d["sq_1_7"] ],
             "piece_J" : [ gamewindow.d["sq_1_4"], gamewindow.d["sq_2_4"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ],
             "piece_L" : [ gamewindow.d["sq_1_6"], gamewindow.d["sq_2_4"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ],
             "piece_O" : [ gamewindow.d["sq_1_5"], gamewindow.d["sq_1_6"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ],
             "piece_S" : [ gamewindow.d["sq_1_5"], gamewindow.d["sq_1_6"], gamewindow.d["sq_2_4"], gamewindow.d["sq_2_5"] ],
             "piece_T" : [ gamewindow.d["sq_1_5"], gamewindow.d["sq_2_4"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ],
             "piece_Z" : [ gamewindow.d["sq_1_4"], gamewindow.d["sq_1_5"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ]            
             }
             
 
suppress_grid()
canvas.tag_lower(escape_window.selector.shape)

interface.bind("x", lambda x: debugprint())    ### DEBUG 
interface.bind("d", lambda x: print("game_started:",game_started, "game_paused", game_paused))    ### DEBUG 
interface.bind("f", lambda x: print(piece_queue))    ### DEBUG 

interface.bind("<Return>", lambda x: key_guide(curr_window, "enter"))
interface.bind("<Escape>", lambda x: key_guide(curr_window, "escape"))

interface.bind("<Right>", lambda x: key_guide(curr_window, "right"))
interface.bind("<Left>", lambda x: key_guide(curr_window, "left"))
interface.bind("<Up>", lambda x: key_guide(curr_window, "up"))
interface.bind("<Down>", lambda x: key_guide(curr_window, "down"))

# Game Loop

interface.mainloop()