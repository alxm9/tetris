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
    def __init__(self,row,column,a,b,color):
        self.row = row
        self.column = column
        self.a = a
        self.b = b
        self.occupier = color # color
        self.outl = "white"
        w = 0.5
        if self.occupier == "#dde5e3":
            self.outl = "grey"
            w = 2
        elif self.occupier != "#bfb7b6":
            w = 1
            self.outl = "black"
        self.shape = canvas.create_rectangle(a,b,a+25,b+25, fill=self.occupier, width=w, outline = self.outl)         
        
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
        return

def key_game(curr_window, direction):
    global current_stamper, spacecounter
    print("keygame1")
    if direction == "escape":
        toggle_escape_window(curr_window, direction)
    elif direction == "right":
        stamp_lr(current_stamper, 25)
    elif direction == "left":
        stamp_lr(current_stamper, -25)
    elif direction == "down":
        stamp_lower(current_stamper)
    elif direction == "space":
        if spacecounter == 0:
            spacecounter = 10
            instant_lower()
        
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
    global game_started, force_exit
    print("we are here")
    print(selector.scope)
    # if selector.scope == "Start":
        # bring_to_front(gamewindow)
    for i in range(len(curr_window.buttonlist)):
        if selector.scope == "Exit":
            force_exit = 1
            game_started = False
            sys.exit()
        if selector.scope == curr_window.buttonlist[i].name:
            print("THIS IS IT",curr_window.buttonlist[i].name)
            bring_to_front(curr_window.buttonlist[i].tied_window)
            change_window(curr_window.buttonlist[i].tied_window)

def cleaner():
    global gamewindow
    for i in gamewindow.d:
        canvas.delete(gamewindow.d[i].shape)
        del i
    gamewindow.d = {}
    for r in range(1,21):
        for c in range(1,11):
            gamewindow.d["sq_{0}_{1}".format(r,c)] = square(r,c,150+(c*25),40+(r*25), "#bfb7b6")
    for i in gamewindow.stamper:
        print(i)
        canvas.delete(gamewindow.stamper[i].shape)
    for i in gamewindow.shadow:
        print(i)
        canvas.delete(gamewindow.shadow[i].shape)
    gamewindow.shadow = ""
    gamewindow.stamper = ""
    return

def cleaner2():
    global gamewindow
    for i in gamewindow.stamper:
        print(i)
        canvas.delete(gamewindow.stamper[i].shape)
    for i in gamewindow.shadow:
        print(i)
        canvas.delete(gamewindow.shadow[i].shape)
    gamewindow.shadow = ""
    gamewindow.stamper = ""
    return    
         

def change_window(new_win):
        global curr_window, prev_window, game_started, game_paused, piece_queue, escape_window
        prev_window = curr_window
        curr_window = new_win
        if curr_window == mainmenu:
            cleaner()
            game_started = False
            game_paused = True
            suppress_grid()
            canvas.tag_lower(escape_window.selector.shape) # I've added attributes to a completely unrelated window and it had an impact on the selector in another object. The bring to front
            piece_queue = []
        if curr_window == gamewindow:
            game_paused = False
            if game_started == False:
                game_started = True
                start_message()
            # if game_started == True:
                # g = threading.Thread(target=game_loop, args=()) # threading allows us to input while the loop is being ran. If I use just game_loop(), it won't wor
                # g.start()

        
def bring_to_front(window):
    global prev_window
    print("THIS IS WINDOW", window)
    instance_dict = vars(window)
    print(instance_dict)
    for key in instance_dict.keys():
        value = instance_dict.get(key)
        if isinstance(value,button) or isinstance(value,selector):
            bring_to_front(value) # starts another instance of the same function 
        elif key == "score" or key == "level":
            pass
        elif key == "d":
            # for i in range(len(window.d)):
                # print("This iss"window.d[i])
                # canvas.tag_raise(window.d[i].shape)
            for x in value:
                canvas.tag_raise(value[x].shape)
        elif key == "shadow":
            for i in value:
                canvas.tag_raise(window.shadow[i].shape)
        elif key == "stamper":
            for i in value:
                canvas.tag_raise(window.stamper[i].shape)
        else:
            # print(key)
            # print(type(instance_dict.get(key)))
            canvas.tag_raise(value)

def suppress_grid(): # This is a fix for something strange that happens when generating the grid. Random squares have a mind of their own and don't respond to the bring_to_front function as they should # Man I really dont want to use this
    for x in gamewindow.d:
        canvas.tag_lower(gamewindow.d[x].shape)

# Status messages
        
def start_message():
        startrect = canvas.create_rectangle(200, 200, 400, 300, fill="orange", width=1, outline = "white")
        text = canvas.create_text(300,250,text="START", font=("Arial", 17))
        interface.after(1500, delete_message, startrect, text)

        
def delete_message(inv, txt):
    canvas.delete(inv, txt)

def game_loop():
    global interface, game_paused, piece_queue, counter, current_piece, current_stamper, gamewindow, spacecounter
    while True:
        if force_exit == 1:
            return
        while game_started == False and force_exit == 0: # Holds here until the game starts
            # print("Main Menu")
            time.sleep(0.01)
        # print("STARTING")
        while game_started == True and force_exit == 0: # game paused
            # print("pause")
            while game_paused == False and force_exit == 0: # game being ran
                counter -= 1
                if spacecounter > 0:
                    spacecounter += -1
                while len(piece_queue) < 5:
                    print("appending to piece list")
                    piece_queue_handler(piece_queue)
                if current_piece == False:
                    current_piece = piece_queue[0]
                    piece_queue.pop(0)
                    stamp_placer(current_piece)
                    piece_queue_drawer()
                print(counter)
                # board_updater() # Shelved
                time.sleep(0.01)
                if counter == 0:
                    stamp_lower(current_stamper)
                    counter = 130
            if curr_window == mainmenu:
                counter = 130
                time.sleep(0.01)
                print("breaking")
                clear_state()

def piece_queue_drawer():
    global piece_queue, gamewindow
    y = 110
    xx = -50
    for i in gamewindow.q:
        for t in range(len(gamewindow.q)):
            for d in range(0,4):
                canvas.delete(gamewindow.q[t]["block_{0}".format(d)].shape)
    gamewindow.q = []
    for p in piece_queue:
        cr_coords = pieces_d[p] # cr_coords = value. Value being a list containing 4 lists
        block_color = color_assign(p)
        if block_color == "cyan":
            xx = -62
        elif block_color == "yellow":
            xx = -60
        elif (block_color != "cyan") or (block_color != "yellow"):
            xx = -50
        queueobj = {}
        for i in range(0,4):
            r = cr_coords[i][0]
            c = cr_coords[i][1]
            queueobj["block_{0}".format(i)] = square(r,c,xx+(c*25),y+(r*25), block_color)
        for x in queueobj:
            print(x)
            canvas.tag_raise(queueobj[x].shape)
        gamewindow.q.append(queueobj)
        y += 100
    
    # cr_coords = pieces_d[current_piece] # cr_coords = value. Value being a list containing 4 lists
    # block_color = color_assign(current_piece)
    # shadow_stamper = {}
    # for i in range(0,4):
        # print("APPENDING STAMPER")
        # r = cr_coords[i][0]
        # c = cr_coords[i][1]
        # current_stamper["block_{0}".format(i)] = square(r,c,150+(c*25),40+(r*25), block_color)
        # shadow_stamper["block_{0}".format(i)] = square(r,c,150+(c*25),40+(r*25), "#dde5e3")
    # stamp_shadow(shadow_stamper)
    # gamewindow.stamper = current_stamper
    # for x in gamewindow.stamper:
        # canvas.tag_raise(gamewindow.stamper[x].shape)
        
def stamp_lower(current_stamper):
    allignment_checker()
    for x in current_stamper:
        current_stamper[x].b += 25
        canvas.moveto(current_stamper[x].shape, current_stamper[x].a, current_stamper[x].b)

def instant_lower():
    global gamewindow, current_stamper
    for x in current_stamper:
        current_stamper[x].b = gamewindow.shadow[x].b
        current_stamper[x].a = gamewindow.shadow[x].a
        canvas.moveto(current_stamper[x].shape, gamewindow.shadow[x].a, gamewindow.shadow[x].b)
    allignment_checker()
        
def stamp_lr(current_stamper, deltax):
    global gamewindow
    for i in range(0,4):        
        if ( (current_stamper["block_{0}".format(i)].a + deltax) < 175 ) or ( (current_stamper["block_{0}".format(i)].a + deltax) > 400 ):
            return
    for x in current_stamper:
        canvas.moveto(current_stamper[x].shape, current_stamper[x].a+deltax, current_stamper[x].b)
        current_stamper[x].a += deltax
    for x in gamewindow.shadow:
        canvas.moveto(gamewindow.shadow[x].shape, gamewindow.shadow[x].a+deltax, gamewindow.shadow[x].b)
        gamewindow.shadow[x].a += deltax

def stamp_rotate(current_stamper, direction):
    global gamewindow
    
    
    
def clear_state():
    global gamewindow, current_stamper, piece_queue, current_piece, game_started
    gamewindow.stamper = {} 
    current_stamper = {}
    piece_queue = []
    current_piece = False
    
def stamp_placer(current_piece):
    global current_stamper, gamewindow, canvas # dictionary which will hold 4 objects which are the squares of the given shape
    # gamewindow.d["sq_{0}_{1}".format(r,c)] = square(r,c,150+(c*25),40+(r*25))
    cr_coords = pieces_d[current_piece] # cr_coords = value. Value being a list containing 4 lists
    block_color = color_assign(current_piece)
    shadow_stamper = {}
    for i in range(0,4):
        print("APPENDING STAMPER")
        r = cr_coords[i][0]
        c = cr_coords[i][1]
        current_stamper["block_{0}".format(i)] = square(r,c,150+(c*25),40+(r*25), block_color)
        shadow_stamper["block_{0}".format(i)] = square(r,c,150+(c*25),40+(r*25), "#dde5e3")
    stamp_shadow(shadow_stamper)
    gamewindow.stamper = current_stamper
    for x in gamewindow.stamper:
        canvas.tag_raise(gamewindow.stamper[x].shape)

def allignment_checker(): # checks if the stamper and shadow are alligned
    global gamewindow, counter, current_piece
    to_stamp = []
    if (gamewindow.shadow["block_0"].a == gamewindow.stamper["block_0"].a) and (gamewindow.shadow["block_0"].b == gamewindow.stamper["block_0"].b):
        for i in gamewindow.shadow:
            for f in gamewindow.d:
                if (gamewindow.shadow[i].a == gamewindow.d[f].a) and (gamewindow.shadow[i].b == gamewindow.d[f].b):
                    print("MATCH FOUND")
                    print(gamewindow.d[f].occupier)
                    gamewindow.d[f].occupier = gamewindow.stamper[i].occupier
                    print(gamewindow.d[f].occupier)
                    canvas.delete(gamewindow.d[f].shape)
                    gamewindow.d[f].shape = canvas.create_rectangle(gamewindow.d[f].a,gamewindow.d[f].b,gamewindow.d[f].a+25,gamewindow.d[f].b+25, fill=gamewindow.d[f].occupier, width=0.25, outline = "black")
        counter = 130
        current_piece = False
        cleaner2()
        
def stamp_shadow(shadow):
    global gamewindow
    gamewindow.shadow = shadow
    if gamewindow.shadow["block_0"].b == gamewindow.shadow["block_1"].b == gamewindow.shadow["block_2"].b == gamewindow.shadow["block_3"].b:
        for i in gamewindow.shadow: 
            gamewindow.shadow[i].b += 25 # If the piece is I, it gets placed a row lower
    for i in gamewindow.shadow:
        gamewindow.shadow[i].b += 450
        canvas.moveto(gamewindow.shadow[i].shape, gamewindow.shadow[i].a, gamewindow.shadow[i].b)
    
def color_assign(current_piece):
    colorlist = ["cyan", "blue", "orange", "yellow", "green", "#bc8ad0", "red"]
    choicelist = ["piece_I", "piece_J", "piece_L", "piece_O", "piece_S", "piece_T", "piece_Z"]
    index = choicelist.index(current_piece)
    color = colorlist[index]
    return color
            
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
gamewindow.q = []
gamewindow.score_container = canvas.create_rectangle((450,120,570,150), fill="black", width = 0.5, outline = "white")
gamewindow.score_text = canvas.create_text(510,105,text="SCORE", font=("Arial", 12))
gamewindow.score_display = canvas.create_text(510,135,text=gamewindow.score, font=("Arial", 12),  fill = "white")
           
# Windows - Game - Grid
gamewindow.d = {}
for r in range(1,21):
    for c in range(1,11):
        gamewindow.d["sq_{0}_{1}".format(r,c)] = square(r,c,150+(c*25),40+(r*25), "#bfb7b6")

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
force_exit = 0
spacecounter = 10
counter = 130

bring_to_front(mainmenu)

# Dictionary to declare the relative column and row for each block
# declare everything on one row from left ro right before moving on to the next
        # gamewindow.d["sq_{0}_{1}".format(r,c)] = square(r,c,150+(c*25),40+(r*25))
        
# pieces_d = { "piece_I" : [ gamewindow.d["sq_1_4"], gamewindow.d["sq_1_5"], gamewindow.d["sq_1_6"], gamewindow.d["sq_1_7"] ],
             # "piece_J" : [ gamewindow.d["sq_1_4"], gamewindow.d["sq_2_4"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ],
             # "piece_L" : [ gamewindow.d["sq_1_6"], gamewindow.d["sq_2_4"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ],
             # "piece_O" : [ gamewindow.d["sq_1_5"], gamewindow.d["sq_1_6"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ],
             # "piece_S" : [ gamewindow.d["sq_1_5"], gamewindow.d["sq_1_6"], gamewindow.d["sq_2_4"], gamewindow.d["sq_2_5"] ],
             # "piece_T" : [ gamewindow.d["sq_1_5"], gamewindow.d["sq_2_4"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ],
             # "piece_Z" : [ gamewindow.d["sq_1_4"], gamewindow.d["sq_1_5"], gamewindow.d["sq_2_5"], gamewindow.d["sq_2_6"] ]            
             # }   # Old pieces_d from when I was trying to regenerate the grid every frame

# Dicts              
pieces_d = { 
            "piece_I" : [  [1,4],  [1,5],  [1,6],  [1,7] ],
            "piece_J" : [  [1,4],  [2,4],  [2,5],  [2,6] ],
            "piece_L" : [  [1,6],  [2,4],  [2,5],  [2,6] ],
            "piece_O" : [  [1,5],  [1,6],  [2,5],  [2,6] ],
            "piece_S" : [  [1,5],  [1,6],  [2,4],  [2,5] ],
            "piece_T" : [  [1,5],  [2,4],  [2,5],  [2,6] ],
            "piece_Z" : [  [1,4],  [1,5],  [2,5],  [2,6] ]            
            }


current_stamper = {} 
suppress_grid()
canvas.tag_lower(escape_window.selector.shape)

interface.bind("x", lambda x: debugprint())    ### DEBUG 
interface.bind("d", lambda x: print("game_started:",game_started, "game_paused", game_paused))    ### DEBUG 
interface.bind("f", lambda x: print(current_stamper[0].occupier))    ### DEBUG 

interface.bind("<Return>", lambda x: key_guide(curr_window, "enter"))
interface.bind("<Escape>", lambda x: key_guide(curr_window, "escape"))

interface.bind("<Right>", lambda x: key_guide(curr_window, "right"))
interface.bind("<Left>", lambda x: key_guide(curr_window, "left"))
interface.bind("<Up>", lambda x: key_guide(curr_window, "up"))
interface.bind("<Down>", lambda x: key_guide(curr_window, "down"))
interface.bind("<space>", lambda x: key_guide(curr_window, "space"))
# Game Loop
g = threading.Thread(target=game_loop, args=()) # threading allows us to input while the loop is being ran. If I use just game_loop(), it won't wor
g.start()

interface.mainloop()