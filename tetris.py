from tkinter import *
from types import MethodType # to alter certain methods
import random
import time
import sys
import os
import threading
import copy

colors = ["red", "blue", "cyan", "orange", "purple", "green", "yellow"]

pieces_d = { 
            "piece_I" : [  [1,4],  [1,5],  [1,6],  [1,7] ],
            "piece_J" : [  [1,4],  [2,4],  [2,5],  [2,6] ],
            "piece_L" : [  [1,6],  [2,4],  [2,5],  [2,6] ],
            "piece_O" : [  [1,5],  [1,6],  [2,5],  [2,6] ],
            "piece_S" : [  [1,5],  [1,6],  [2,4],  [2,5] ],
            "piece_T" : [  [1,5],  [2,4],  [2,5],  [2,6] ],
            "piece_Z" : [  [1,4],  [1,5],  [2,5],  [2,6] ]            
            }

rotation_matrix_3x3 = {
                    "1x1" : [] , "2x1" : [], "3x1" : [],
                    "1x2" : [] , "2x2" : [], "3x2" : [],
                    "1x3" : [] , "2x3" : [], "3x3" : []
                    }


rotation_matrix_4x4 = {
                    "1x1" : [] , "2x1" : [], "3x1" : [], "4x1" : [],
                    "1x2" : [] , "2x2" : [], "3x2" : [], "4x2" : [],
                    "1x3" : [] , "2x3" : [], "3x3" : [], "4x3" : [],
                    "1x4" : [] , "2x4" : [], "3x4" : [], "4x4" : []
                    }
class tetrisapp():
    def __init__(self):
        self.running = True
        self.game_started = False
        self.interface = Tk()
        self.interface.geometry("600x600")        
        self.canvas = Canvas(self.interface, bg = "white", width = 600, height = 600)
        self.canvas.pack()
        self.counter = 100
        self.current_win = "na"
        self.previous_win = "na"
        self.can_pause = False
        
    def bringtofront(self, previous_win, new_win):
        if game.previous_win == "na":
            game.previous_win = game.mainmenu_win
        self.previous_win = previous_win
        self.current_win = new_win
        if self.current_win == game.mainmenu_win:
            game.interface.unbind("<Key>")
            game.interface.unbind("<BackSpace>")
            game.tetrisgame_win.level = 1
            game.tetrisgame_win.score = 0
            game.canvas.delete(game.tetrisgame_win.level_text)
            game.canvas.delete(game.tetrisgame_win.score_display)
            game.tetrisgame_win.level_text = game.canvas.create_text(300,30,text=("Lv.",game.tetrisgame_win.level), font=("Arial", 24))
            game.tetrisgame_win.score_display = game.canvas.create_text(510,135,text=game.tetrisgame_win.score, font=("Arial", 12),  fill = "white")
            game.tetrisgame_win.shapelist.append(game.tetrisgame_win.level_text)
            game.tetrisgame_win.shapelist.append(game.tetrisgame_win.score_display)
            self.game_started = False
            game.tetrisgame_win.stamper_queue = []
            game.interface.bind("<y>", lambda x: print(game.current_win))
            game.interface.bind("<Down>", lambda x: game.current_win.selector_mover(75))      
            game.interface.bind("<Up>", lambda x: game.current_win.selector_mover(-75))  
            game.interface.bind("<Return>", lambda x: game.current_win.selector.scope()) 
            game.interface.bind("<Escape>", lambda x:  game.method_handler())
            game.tetrisgame_win.grid_cleaner()
        for i in new_win.shapelist:
            game.canvas.tag_raise(i)
        if hasattr(new_win, "grid_dict"):
            for i in new_win.grid_dict:
                game.canvas.tag_raise(new_win.grid_dict[i].shape)
        if hasattr(new_win, "shapelist_1_5"):
            for i in new_win.shapelist_1_5:
                game.canvas.tag_raise(i)
        if hasattr(new_win, "shapelist_2"):
            for i in new_win.shapelist_2:
                game.canvas.tag_raise(i)
        for i in new_win.buttonlist:
            if hasattr(i, "scope"):
                self.current_win.selector = i
        if self.current_win == game.highscore_win:
            self.game_started = False
            game.interface.bind("<Down>", lambda x: game.current_win.selector_mover(75))      
            game.interface.bind("<Up>", lambda x: game.current_win.selector_mover(-75))  
            game.interface.bind("<Return>", lambda x: game.current_win.selector.scope()) 
            game.interface.bind("<Escape>", lambda x:  game.method_handler())
        if self.current_win == game.tetrisgame_win:
            self.game_started = True
            self.can_pause = True
            game.interface.bind("<q>", lambda x: game.current_win.current_stamper.rotate("clockwise"))
            game.interface.bind("<w>", lambda x: game.current_win.current_stamper.rotate("counterclockwise"))
            game.interface.bind("<Down>", lambda x: game.current_win.current_stamper.move_ud(25))
            game.interface.bind("<Left>", lambda x: game.current_win.current_stamper.move_lr(-25))       
            game.interface.bind("<Right>", lambda x: game.current_win.current_stamper.move_lr(25))     
            game.interface.bind("<space>", lambda x: game.current_win.current_stamper.move_space())                
        if self.current_win == game.pause_win:
            game.interface.bind("<y>", lambda x: print(game.current_win))
            game.interface.bind("<Down>", lambda x: game.current_win.selector_mover(75))      
            game.interface.bind("<Up>", lambda x: game.current_win.selector_mover(-75))  
            game.interface.bind("<Return>", lambda x: game.current_win.selector.scope())  
            game.interface.bind("<Escape>", lambda x:  game.method_handler())            
            self.can_pause = False
        if self.current_win == game.gameover_win:
            game.gameover_win.textpos = 0
            self.can_pause = False
            self.game_started = False
            unbindlist = ["<Down>", "<Up>","<Escape>","<q>","<w>","<Down>","<Left>","<y>"]
            for i in unbindlist:
                game.interface.unbind(i)
            game.interface.bind("<Key>", lambda x: self.current_win.text_handler(x, "na"))
            game.interface.bind("<BackSpace>", lambda x: self.current_win.text_handler(x, "back"))
        print(game.current_win)
                
    def rungame(self):
        self.g = threading.Thread(target=game_loop) # threading allows us to input while the loop is being ran. If I use just game_loop(), it won't wor
        self.g.start()
        self.interface.mainloop()
        
    def exit(self):
        self.running = False
        sys.exit()
        
    def method_handler(self):
        if self.current_win == game.pause_win:
            self.can_pause = False
            game.bringtofront(game.pause_win, game.tetrisgame_win)
            return
        if self.can_pause == False:
            if self.current_win == game.highscore_win:
                game.bringtofront(game.previous_win, game.mainmenu_win)
        else:
            game.bringtofront(game.previous_win, game.pause_win)
        

game = tetrisapp()  
        
class class_window():    
    def __init__(self,name,color,x1,y1,x2,y2):
        self.shape = game.canvas.create_rectangle((x1,y1,x2,y2), fill=color, width = 0)
        self.name = name
        self.shapelist = [self.shape] # To be used when changing the z-index of all the elements of the window
        self.buttonlist = []
        self.current_stamper = False
        self.selector = "null"
        self.charlist = []
        self.playername_text = ""
        self.playername_shape = False
        
    def __str__(self):
        return f"{self.name}"

    def selector_mover(self, delta_y):
        for i in self.buttonlist:
            if hasattr(i, "scope"):
                for d in self.buttonlist:
                    if d.y == (i.y + delta_y):
                        i.y = d.y
                        game.canvas.moveto(i.shape, d.x-4, d.y-4)
                        i.scope = d.role
                        return

    def text_handler(self, event, extra):
        print("RUNNING")
        game.canvas.delete(self.playername_shape)
        if len(self.playername_text) > 16:
            return
        if extra == "back":
            print("this is running")
            print(len(self.playername_text))
            if len(self.playername_text)>0:            
                self.playername_text = self.playername_text[:-1]
                self.playername_shape = game.canvas.create_text(300,280,text=self.playername_text, font=("Arial", 12),  fill = "black")
            else:
                self.playername_text = " "
            return
        self.playername_text += event.char
        self.playername_text.upper()
        self.playername_shape = game.canvas.create_text(300,280,text=self.playername_text, font=("Arial", 12),  fill = "black")

class class_window_game():    
    def __init__(self,name,color,x1,y1,x2,y2):
        self.shape = game.canvas.create_rectangle((x1,y1,x2,y2), fill=color, width = 0)
        self.name = name
        self.shadowplaced = 0
        self.grid_dict = {}
        self.shapelist = [self.shape] # To be used when changing the z-index of all the elements of the window
        self.shapelist_1_5 = [] # For shadow stamper shapes. I guess we can consider the numbers next to the list the z-index 
        self.shapelist_2 = [] # For stampers only. Separate list so UI elements don't get accidentally deleted 
        self.buttonlist = []
        self.stamper_queue = []
        self.current_matrix = []
        self.current_stamper = False
        self.shadow_stamper = False
        self.selector = "null"
        
    def __str__(self):
        return f"{self.name}"

    def grid_cleaner(self):
        grid = self.grid_dict
        for i in grid:
            if grid[i].occupier != "#bfb7b6":
                grid[i].occupier = "#bfb7b6"
                game.canvas.delete(grid[i].shape)
                grid[i].shape = 0
                grid[i].shape = game.canvas.create_rectangle(grid[i].a, grid[i].b, grid[i].a+25, grid[i].b+25, fill=grid[i].occupier, width=0.25, outline="white")
                
    def selector_mover(self, delta_y):
        for i in self.buttonlist:
            if hasattr(i, "scope"):
                for d in self.buttonlist:
                    if d.y == (i.y + delta_y):
                        i.y = d.y
                        game.canvas.moveto(i.shape, d.x-4, d.y-4)
                        i.scope = d.role
                        return
       
    def put_on_matrix(self):
            for i in rotation_matrix_3x3:
                rotation_matrix_3x3[i] = [] # problem in the future? might wanna deepcopy 
            for i in rotation_matrix_4x4:
                rotation_matrix_4x4[i] = []
            currstamper = self.current_stamper
            shadowstamper = self.shadow_stamper
            if currstamper.blocktype == "piece_I":
                self.current_matrix = rotation_matrix_4x4
                self.current_matrix["1x2"] = [currstamper.squarelist[0], shadowstamper.squarelist[0] ]
                self.current_matrix["2x2"] = [currstamper.squarelist[1], shadowstamper.squarelist[1] ]
                self.current_matrix["3x2"] = [currstamper.squarelist[2], shadowstamper.squarelist[2] ]
                self.current_matrix["4x2"] = [currstamper.squarelist[3], shadowstamper.squarelist[3] ]
            if currstamper.blocktype == "piece_J":
                self.current_matrix = rotation_matrix_3x3
                self.current_matrix["1x1"] = [currstamper.squarelist[0], shadowstamper.squarelist[0] ]
                self.current_matrix["1x2"] = [currstamper.squarelist[1], shadowstamper.squarelist[1] ]
                self.current_matrix["2x2"] = [currstamper.squarelist[2], shadowstamper.squarelist[2] ]
                self.current_matrix["3x2"] = [currstamper.squarelist[3], shadowstamper.squarelist[3] ]
            if currstamper.blocktype == "piece_L":
                self.current_matrix = rotation_matrix_3x3
                self.current_matrix["3x1"] = [currstamper.squarelist[0], shadowstamper.squarelist[0] ]
                self.current_matrix["1x2"] = [currstamper.squarelist[1], shadowstamper.squarelist[1] ]
                self.current_matrix["2x2"] = [currstamper.squarelist[2], shadowstamper.squarelist[2] ]
                self.current_matrix["3x2"] = [currstamper.squarelist[3], shadowstamper.squarelist[3] ]
            if currstamper.blocktype == "piece_O":
                return
            if currstamper.blocktype == "piece_S":
                self.current_matrix = rotation_matrix_3x3
                self.current_matrix["2x1"] = [currstamper.squarelist[0], shadowstamper.squarelist[0] ]
                self.current_matrix["3x1"] = [currstamper.squarelist[1], shadowstamper.squarelist[1] ]
                self.current_matrix["1x2"] = [currstamper.squarelist[2], shadowstamper.squarelist[2] ]
                self.current_matrix["2x2"] = [currstamper.squarelist[3], shadowstamper.squarelist[3] ]
            if currstamper.blocktype == "piece_T":
                self.current_matrix = rotation_matrix_3x3
                self.current_matrix["2x1"] = [currstamper.squarelist[0], shadowstamper.squarelist[0] ]
                self.current_matrix["1x2"] = [currstamper.squarelist[1], shadowstamper.squarelist[1] ]
                self.current_matrix["2x2"] = [currstamper.squarelist[2], shadowstamper.squarelist[2] ]
                self.current_matrix["3x2"] = [currstamper.squarelist[3], shadowstamper.squarelist[3] ]
            if currstamper.blocktype == "piece_Z":
                self.current_matrix = rotation_matrix_3x3
                self.current_matrix["1x1"] = [currstamper.squarelist[0], shadowstamper.squarelist[0] ]
                self.current_matrix["2x1"] = [currstamper.squarelist[1], shadowstamper.squarelist[1] ]
                self.current_matrix["2x2"] = [currstamper.squarelist[2], shadowstamper.squarelist[2] ]
                self.current_matrix["3x2"] = [currstamper.squarelist[3], shadowstamper.squarelist[3] ]

    def gameoverchecker(self):
        current_line_color = []
        for c in range(1,11):
            current_line_color.append(game.tetrisgame_win.grid_dict["sq_1_{0}".format(c)].occupier)  
            for i in current_line_color:
                if i != "#bfb7b6":
                    # gg_message()
                    game.bringtofront(game.previous_win, game.gameover_win)
                    return
            
    def linechecker(self, shadowstamper_y_max, shadowstamper_y_min):
        deleted_rows = []
        start = int((shadowstamper_y_max - 40) / 25)
        shadowstamper_y_min = int((shadowstamper_y_min - 40) / 25) -1
        end = 0
        for r in range(1,20): # setting the end of the loop, last instance of clean rows
            current_line_color = []
            for c in range(1,11):
                current_line_color.append(game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(r,c)].occupier)  
            for i in current_line_color:
                if i != "#bfb7b6":
                    end = r-1
                    break
            else: 
                continue
            break

        found = 0
        for r in range(start,shadowstamper_y_min,-1):
            current_line_square = []
            current_line_color = []
            for c in range(10,0,-1):
                if r <= 0:
                    return
                current_line_color.append( game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(r,c)].occupier )
                current_line_square.append( game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(r,c)] )
            if "#bfb7b6" not in current_line_color:
                found = 1
                deleted_rows.append(r)
                for i in current_line_square:
                    i.occupier = "#bfb7b6"
                    game.canvas.delete(i.shape)
                    i.shape = game.canvas.create_rectangle(i.a, i.b, i.a+25, i.b+25, fill = "#bfb7b6", width=0.25, outline="white")
        if found == 1:
            delta_y = -1
            for dr in deleted_rows:
                delta_y += 1
                for i in range(dr+delta_y,end,-1): # row
                    for d in range(10,0,-1): # column
                        if i-1 == 0:
                            return
                        square = game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(i,d)]
                        abovesquare = game.tetrisgame_win.grid_dict["sq_{0}_{1}".format( (i-1) ,d)]
                        abovesquare.occupier, square.occupier = square.occupier, abovesquare.occupier
                    for i in self.grid_dict:
                        grid = self.grid_dict[i]
                        game.canvas.delete(grid.shape) # memory leak?
                        ol = "white"
                        if grid.occupier != "#bfb7b6":
                            ol = "black"
                        grid.shape = game.canvas.create_rectangle(grid.a, grid.b, grid.a+25, grid.b+25, fill = grid.occupier, width=0.25, outline=ol)
                        game.canvas.tag_raise(grid.shape)
                    for i in self.grid_dict:
                        grid = self.grid_dict[i]
                        if grid.occupier != "#bfb7b6":
                            game.canvas.tag_raise(grid.shape)
            game.tetrisgame_win.score += 50*(2*(delta_y+1))
            game.canvas.delete(game.tetrisgame_win.score_display)
            game.tetrisgame_win.score_display = game.canvas.create_text(510,135,text=game.tetrisgame_win.score, font=("Arial", 12),  fill = "white")
            game.tetrisgame_win.shapelist.append(game.tetrisgame_win.score_display)
            if game.tetrisgame_win.level <= game.tetrisgame_win.score/500:
                game.tetrisgame_win.level += 1
                game.counterbase = 200 - (game.tetrisgame_win.level*15)
                if game.counterbase < 10:
                    game.counterbase = 10
                game.canvas.delete(game.tetrisgame_win.level_text)
                game.tetrisgame_win.level_text = game.canvas.create_text(300,30,text=("Lv.",game.tetrisgame_win.level), font=("Arial", 24))
                game.tetrisgame_win.shapelist.append(game.tetrisgame_win.level_text)
            
    def stamp_maker(self):
        colorlist = ["cyan", "blue", "orange", "yellow", "green", "#bc8ad0", "red"]
        choicelist = ["piece_I", "piece_J", "piece_L", "piece_O", "piece_S", "piece_T", "piece_Z"]
        piece = random.choice(choicelist)
        index = choicelist.index(piece)
        color = colorlist[index]
        slist = []
        for i in range(0,4): # creating the object
            r = pieces_d[piece][i][0]
            c = pieces_d[piece][i][1]
            object = square(r,c,-55+(c*25),110+(r*25), color)
            slist.append(object)
        for d in slist: # appending the squares to shapelist_2
            self.shapelist_2.append(d.shape)
        if color == "yellow":
            for i in slist:
                i.a += -12
        if color == "cyan":
            for i in slist:
                i.a += -10
        object = stamper(slist, piece)
        return object

    def print_piece(self):
        counter = 0
        grid = game.tetrisgame_win.grid_dict
        while counter < 4: # so it doesn't waste extra miliseconds processing pointlessly
            for i in self.current_stamper.squarelist:
                for d in grid:
                    if (i.a == grid[d].a) and (i.b == grid[d].b):
                        grid[d].occupier = i.occupier
                        game.canvas.delete(grid[d].shape)
                        grid[d].shape = 0
                        grid[d].shape = game.canvas.create_rectangle(grid[d].a, grid[d].b, grid[d].a+25, grid[d].b+25, fill=grid[d].occupier, width=0.25, outline="black")
                        counter += 1

    def create_shadowstamper(self):
        slist = []
        for i in self.current_stamper.squarelist:
            shadowsquare = square(i.row, i.column, i.a, i.b, "white")
            slist.append(shadowsquare)
        for d in slist:
            self.shapelist_1_5.append(d.shape) # problems might arise later, keep this one in mind
        shadow_instance = stamper(slist, self.current_stamper.blocktype)
        self.shadow_stamper = stamper(slist, self.current_stamper.blocktype)
            
    def queue_arranger(self):
        for d in range(0,4):
            object = self.stamper_queue[d]
            for i in object.squarelist:
                i.b = 120 + (i.row * 25)
                game.canvas.moveto(i.shape, i.a , i.b)
        for d in range(0,4):
            object = self.stamper_queue[d]
            for x in object.squarelist:
                x.b = x.b + (d*85)
                x.a = x.a
                game.canvas.moveto(x.shape, x.a, x.b)
        pass
   

class button():
    def __init__(self,x,y,name, tied_window):
        self.x = x 
        self.y = y
        self.name = name
        self.shape = game.canvas.create_rectangle((x,y,x+150,y+50), fill="grey", width = 2)
        self.text = game.canvas.create_text(x+75,y+25,text=name, font=("Arial", 15)) 
        self.tied_window = tied_window

    def role(self):
        game.bringtofront(game.previous_win, self.tied_window)

class selector():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.shape = game.canvas.create_rectangle((x,y,x+150,y+50), width = 5, outline = "red")
        self.scope = "Start"

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
        self.shape = game.canvas.create_rectangle(a,b,a+25,b+25, fill=self.occupier, width=w, outline = self.outl)       

class stamper():
    def __init__(self, squarelist, blocktype):
        self.squarelist = squarelist # we're going to have square instances      
        self.blocktype = blocktype

    def check_rotation(self, direction, previous_pos):
        currentstamper_y_max = 0
        currentstamper_y_min = 1000
        currstampsq = game.tetrisgame_win.current_stamper.squarelist
        for i in currstampsq: 
            if i.b > currentstamper_y_max:
                currentstamper_y_max = i.b      
        for i in currstampsq:
            if i.b < currentstamper_y_min:
                currentstamper_y_min = i.b
        d = 1
        # if self.blocktype == "piece_I":
            # d = 1
        currentstamper_y_max = int((currentstamper_y_max - 40) / 25) +d
        currentstamper_y_min = int((currentstamper_y_min - 40) / 25) -1
        if (currentstamper_y_min < 1) or (currentstamper_y_max > 20):
            for i in range(0,4):
                self.squarelist[i].a = previous_pos[i][0]
                self.squarelist[i].b = previous_pos[i][1]
                shadow_handler(game.tetrisgame_win.shadow_stamper)
            return False
        for square in currstampsq:
            for r in range(currentstamper_y_min, currentstamper_y_max):
                for c in range(1,11):
                    if (game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(r,c)].a == square.a) and (game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(r,c)].b == square.b):
                        if game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(r,c)].occupier != "#bfb7b6":
                            for i in range(0,4):
                                self.squarelist[i].a = previous_pos[i][0]
                                self.squarelist[i].b = previous_pos[i][1]
                                shadow_handler(game.tetrisgame_win.shadow_stamper)
                            return False
        return True
        
    def rotate(self,direction): # a=x b=y
        if game.tetrisgame_win.shadowplaced == 0:
            return
        matrix = game.tetrisgame_win.current_matrix
        previous_pos = [] 
        for i in self.squarelist:
            previous_pos.append([i.a,i.b])
        if self.blocktype == "piece_O":
            return 
        elif self.blocktype == "piece_I":
            self.rotate2(direction)
            return
        else:
            if direction == "counterclockwise":
                rotation1 = [ matrix["1x1"], matrix["1x3"], matrix["3x3"], matrix["3x1"] ]
                rotation2 = [ matrix["1x2"], matrix["2x3"], matrix["3x2"], matrix["2x1"] ]
                values1 = [ [0, 50] , [50, 0] , [0, -50] , [-50, 0] ]
                values2 = [ [25, 25] , [25, -25] , [-25, -25] , [-25, 25] ]
            if direction == "clockwise":
                rotation1 = [ matrix["1x1"], matrix["3x1"], matrix["3x3"], matrix["1x3"] ]
                rotation2 = [ matrix["1x2"], matrix["2x1"], matrix["3x2"], matrix["2x3"] ]
                values1 = [ [50, 0] , [0, 50] , [-50, 0] , [0, -50] ]
                values2 = [ [25, -25] , [25, 25] , [-25, 25] , [-25, -25] ]
            for i in range(0,2): # each matrix element holds a list with 2 squares, that of the current_stamper and the shadow_stamper
                for d in range(0,4):
                    if len(rotation1[d]) != 0:
                        rotation1[d][i].a += values1[d][0]
                        rotation1[d][i].b += values1[d][1]
                    if len(rotation2[d]) != 0:
                        rotation2[d][i].a += values2[d][0]
                        rotation2[d][i].b += values2[d][1]
            proceed = self.check_rotation(direction, previous_pos)
            if proceed == False:
                return
            ########## # check_rotation was here
                    ########
            for i in game.tetrisgame_win.current_stamper.squarelist:
                game.canvas.moveto(i.shape, i.a, i.b)
            for i in game.tetrisgame_win.shadow_stamper.squarelist:
                game.canvas.moveto(i.shape, i.a, i.b)
            if direction == "counterclockwise":
                matrix["1x1"], matrix["3x1"], matrix["3x3"], matrix["1x3"] = matrix["3x1"], matrix["3x3"], matrix["1x3"], matrix["1x1"]
                matrix["1x2"], matrix["2x1"], matrix["3x2"], matrix["2x3"] = matrix["2x1"], matrix["3x2"], matrix["2x3"], matrix["1x2"]
            if direction == "clockwise":
                matrix["1x1"], matrix["3x1"], matrix["3x3"], matrix["1x3"] = matrix["1x3"], matrix["1x1"], matrix["3x1"], matrix["3x3"]
                matrix["1x2"], matrix["2x1"], matrix["3x2"], matrix["2x3"] = matrix["2x3"], matrix["1x2"], matrix["2x1"], matrix["3x2"]
            for i in range(0,4):
                if game.tetrisgame_win.current_stamper.squarelist[i].a < 175 or game.tetrisgame_win.current_stamper.squarelist[i].a > 400:
                    self.rotate(direction)
            shadow_handler(game.tetrisgame_win.shadow_stamper)

    def rotate2(self, direction):
            if game.tetrisgame_win.shadowplaced == 0:
                return
            previous_pos = [] 
            for i in self.squarelist:
                previous_pos.append([i.a,i.b])
            matrix = game.tetrisgame_win.current_matrix
            if direction == "clockwise":
                rotation1 = [ matrix["1x3"], matrix["2x1"], matrix["4x2"], matrix["3x4"] ]
                rotation2 = [ matrix["1x2"], matrix["3x1"], matrix["4x3"], matrix["2x4"] ]
                rotation3 = [ matrix["2x2"], matrix["3x2"], matrix["3x3"], matrix["2x3"] ]
                values1 = [ [25,-50] , [50,25] , [-25,50] , [-50,-25] ]
                values2 = [ [50,-25] , [25,50] , [-50,25] , [-25,-50] ]
                values3 = [ [25,0] , [0,25] , [-25,0] , [0,-25] ]           
            if direction == "counterclockwise":
                rotation1 = [ matrix["1x3"], matrix["2x1"], matrix["4x2"], matrix["3x4"] ]
                rotation2 = [ matrix["1x2"], matrix["3x1"], matrix["4x3"], matrix["2x4"] ]
                rotation3 = [ matrix["2x2"], matrix["3x2"], matrix["3x3"], matrix["2x3"] ]
                values1 = [ [50,25] , [-25,50] , [-50,-25] , [25,-50] ]
                values2 = [ [25,50] , [-50,25] , [-25,-50] , [50,-25] ]
                values3 = [ [0,25] , [-25,0] , [0,-25] , [25,0] ]
                
            for i in range(0,2): # each matrix element holds a list with 2 squares, that of the current_stamper and the shadow_stamper
                for d in range(0,4):
                    if len(rotation1[d]) != 0:
                        rotation1[d][i].a += values1[d][0]
                        rotation1[d][i].b += values1[d][1]
                    if len(rotation2[d]) != 0:
                        rotation2[d][i].a += values2[d][0]
                        rotation2[d][i].b += values2[d][1]
                    if len(rotation3[d]) != 0:
                        rotation3[d][i].a += values3[d][0]
                        rotation3[d][i].b += values3[d][1]
            proceed = self.check_rotation(direction, previous_pos)
            if proceed == False:
                return
            for i in game.tetrisgame_win.current_stamper.squarelist:
                game.canvas.moveto(i.shape, i.a, i.b)
            for i in game.tetrisgame_win.shadow_stamper.squarelist:
                game.canvas.moveto(i.shape, i.a, i.b)
            if direction == "clockwise":             
                matrix["1x2"], matrix["3x1"], matrix["4x3"], matrix["2x4"] = matrix["2x4"], matrix["1x2"], matrix["3x1"], matrix["4x3"] 
                matrix["1x3"], matrix["2x1"], matrix["4x2"], matrix["3x4"] = matrix["3x4"], matrix["1x3"], matrix["2x1"], matrix["4x2"]
                matrix["2x2"], matrix["3x2"], matrix["3x3"], matrix["2x3"] = matrix["2x3"], matrix["2x2"], matrix["3x2"], matrix["3x3"]
            if direction == "counterclockwise":                             
                matrix["1x2"], matrix["3x1"], matrix["4x3"], matrix["2x4"] = matrix["3x1"], matrix["4x3"], matrix["2x4"], matrix["1x2"]
                matrix["1x3"], matrix["2x1"], matrix["4x2"], matrix["3x4"] = matrix["2x1"], matrix["4x2"], matrix["3x4"], matrix["1x3"]
                matrix["2x2"], matrix["3x2"], matrix["3x3"], matrix["2x3"] = matrix["3x2"], matrix["3x3"], matrix["2x3"], matrix["2x2"]
            for i in range(0,4):
                if game.tetrisgame_win.current_stamper.squarelist[i].a < 175 or game.tetrisgame_win.current_stamper.squarelist[i].a > 400:
                    self.rotate(direction)
            shadow_handler(game.tetrisgame_win.shadow_stamper)

    def move_space(self):
        if game.tetrisgame_win.shadowplaced == 0:
            return
        for i in range(0,4):
            game.tetrisgame_win.current_stamper.squarelist[i].a = game.tetrisgame_win.shadow_stamper.squarelist[i].a
            game.tetrisgame_win.current_stamper.squarelist[i].b = game.tetrisgame_win.shadow_stamper.squarelist[i].b
            game.canvas.moveto(game.tetrisgame_win.current_stamper.squarelist[i].shape, game.tetrisgame_win.current_stamper.squarelist[i].a, game.tetrisgame_win.current_stamper.squarelist[i].b)
            game.canvas.tag_raise(game.tetrisgame_win.current_stamper.squarelist[i].shape)
        game.current_win.current_stamper.move_ud(25)
        
    def move_ud(self, delta_y):
        if game.tetrisgame_win.shadowplaced == 0:
            return
        if game.tetrisgame_win.current_stamper.squarelist[0].b == game.tetrisgame_win.shadow_stamper.squarelist[0].b: # Leak?
            shadowstamper_y_max = 0
            shadowstamper_y_min = 1000
            for i in game.tetrisgame_win.shadow_stamper.squarelist: # setting the start of the loop, highest y value of the shadowstamper
                if i.b > shadowstamper_y_max:
                    shadowstamper_y_max = i.b      
            for i in game.tetrisgame_win.shadow_stamper.squarelist: # setting the start of the loop, highest y value of the shadowstamper
                if i.b < shadowstamper_y_min:
                    shadowstamper_y_min = i.b
            if game.tetrisgame_win.shadow_stamper.blocktype == "piece_I":
                shadowstamper_y_min += -25
            game.tetrisgame_win.print_piece()
            for i in game.tetrisgame_win.current_stamper.squarelist:
                game.canvas.delete(i.shape)
                del i
            for i in game.tetrisgame_win.shadow_stamper.squarelist:
                game.canvas.delete(i.shape)
                del i
            del game.tetrisgame_win.current_stamper
            del game.tetrisgame_win.shadow_stamper
            game.tetrisgame_win.current_stamper = False
            game.tetrisgame_win.shadow_stamper = False
            game.tetrisgame_win.linechecker(shadowstamper_y_max, shadowstamper_y_min)
        for i in self.squarelist:
            i.b = i.b + delta_y
            game.canvas.moveto(i.shape, i.a, i.b)
            game.canvas.tag_raise(i.shape)
        game.counter = game.counterbase
    
    def move_lr(self, delta_x):
        if game.tetrisgame_win.shadowplaced == 0:
            return
        shadowlist = game.tetrisgame_win.shadow_stamper.squarelist
        for i in range(0,4):
            if ( (self.squarelist[i].a + delta_x) < 175 ) or ( (self.squarelist[i].a + delta_x) > 400 ):
                return
        for i in game.tetrisgame_win.current_stamper.squarelist:
            for d in game.tetrisgame_win.grid_dict:
                if ( i.b == game.tetrisgame_win.grid_dict[d].b ) and ( (i.a + delta_x) == game.tetrisgame_win.grid_dict[d].a ) and ( game.tetrisgame_win.grid_dict[d].occupier != "#bfb7b6" ):
                    return
        for i in range(0,4):
            self.squarelist[i].a = self.squarelist[i].a + delta_x
            game.canvas.moveto(self.squarelist[i].shape, self.squarelist[i].a, self.squarelist[i].b)
            shadowlist[i].a = shadowlist[i].a + delta_x 
            game.canvas.moveto(shadowlist[i].shape, shadowlist[i].a, shadowlist[i].b)
        shadow_handler(game.tetrisgame_win.shadow_stamper)
    
def start_message():
        startrect = game.canvas.create_rectangle(200, 200, 400, 300, fill="orange", width=1, outline = "white")
        text = game.canvas.create_text(300,250,text="START", font=("Arial", 17))
        game.interface.after(400, delete_message, startrect, text)

def gg_message():
        startrect = game.canvas.create_rectangle(200, 200, 400, 300, fill="red", width=1, outline = "white")
        text = game.canvas.create_text(300,250,text="GAME OVER", font=("Arial", 17))
        game.interface.after(20000, delete_message, startrect, text)

def delete_message(inv, txt):
    game.canvas.delete(inv, txt)

def clear_shapelists():
    for i in game.tetrisgame_win.shapelist_2:
        game.canvas.delete(i)
    for i in game.tetrisgame_win.shapelist_1_5:
        game.canvas.delete(i)
    game.tetrisgame_win.shapelist_2 = []
    game.tetrisgame_win.shapelist_1_5= []

def reposition_stamper():
    for i in game.tetrisgame_win.current_stamper.squarelist:
        i.a = (i.column*25) + 150
        i.b = (i.row*25) + 40
        game.canvas.moveto(i.shape, i.a, i.b)
    stop = 0
    shadow_handler(game.tetrisgame_win.shadow_stamper)

            
def shadow_handler(shadowstamper):
    game.tetrisgame_win.shadowplaced = 0
    for i in range(0,4):
        game.tetrisgame_win.shadow_stamper.squarelist[i].a = game.tetrisgame_win.current_stamper.squarelist[i].a
        game.tetrisgame_win.shadow_stamper.squarelist[i].b = game.tetrisgame_win.current_stamper.squarelist[i].b
        for d in range(0,4):
            game.canvas.moveto(game.tetrisgame_win.shadow_stamper.squarelist[d].shape, game.tetrisgame_win.shadow_stamper.squarelist[d].a, game.tetrisgame_win.shadow_stamper.squarelist[d].b)
    grid = game.tetrisgame_win.grid_dict
    clear = 1
    previous_coords1 = ["na","na"] # a b
    previous_coords2 = ["na","na"] # a b
    previous_coords3 = ["na","na"] # a b
    previous_coords4 = ["na","na"] # a b
    previous_coords1[0], previous_coords1[1] = shadowstamper.squarelist[0].a, shadowstamper.squarelist[0].b
    previous_coords2[0], previous_coords2[1] = shadowstamper.squarelist[1].a, shadowstamper.squarelist[1].b
    previous_coords3[0], previous_coords3[1] = shadowstamper.squarelist[2].a, shadowstamper.squarelist[2].b
    previous_coords4[0], previous_coords4[1] = shadowstamper.squarelist[3].a, shadowstamper.squarelist[3].b
    while clear == 1:
        for i in shadowstamper.squarelist:
            i.b += 25
            game.canvas.moveto(i.shape, i.a, i.b)
        for i in shadowstamper.squarelist:
            for d in grid:
                if i.b == 565:
                    shadowstamper.squarelist[0].a, shadowstamper.squarelist[0].b = previous_coords1[0], previous_coords1[1]
                    shadowstamper.squarelist[1].a, shadowstamper.squarelist[1].b = previous_coords2[0], previous_coords2[1]
                    shadowstamper.squarelist[2].a, shadowstamper.squarelist[2].b = previous_coords3[0], previous_coords3[1]
                    shadowstamper.squarelist[3].a, shadowstamper.squarelist[3].b = previous_coords4[0], previous_coords4[1]
                    for p in shadowstamper.squarelist:
                        game.canvas.moveto(p.shape, p.a, p.b)
                    game.tetrisgame_win.shadowplaced = 1
                    return                    
                if ( grid[d].occupier != "#bfb7b6" ):
                    if ( (grid[d].b == i.b) and (grid[d].a == i.a) ):
                        shadowstamper.squarelist[0].a, shadowstamper.squarelist[0].b = previous_coords1[0], previous_coords1[1]
                        shadowstamper.squarelist[1].a, shadowstamper.squarelist[1].b = previous_coords2[0], previous_coords2[1]
                        shadowstamper.squarelist[2].a, shadowstamper.squarelist[2].b = previous_coords3[0], previous_coords3[1]
                        shadowstamper.squarelist[3].a, shadowstamper.squarelist[3].b = previous_coords4[0], previous_coords4[1]
                        for p in shadowstamper.squarelist:
                            game.canvas.moveto(p.shape, p.a, p.b)
                        game.tetrisgame_win.shadowplaced = 1
                        return
        previous_coords1[0], previous_coords1[1] = shadowstamper.squarelist[0].a, shadowstamper.squarelist[0].b
        previous_coords2[0], previous_coords2[1] = shadowstamper.squarelist[1].a, shadowstamper.squarelist[1].b
        previous_coords3[0], previous_coords3[1] = shadowstamper.squarelist[2].a, shadowstamper.squarelist[2].b
        previous_coords4[0], previous_coords4[1] = shadowstamper.squarelist[3].a, shadowstamper.squarelist[3].b        
    
    
def game_loop():
    game.current_win.selector_mover(0)
    game.pause_win.selector_mover(0)
    game.gameover_win.selector_mover(0)
    while game.running == True:
        while (game.current_win != game.tetrisgame_win):
            if game.running == False:
                return
            if game.current_win == game.mainmenu_win:
                game.tetrisgame_win.current_stamper = False
                game.tetrisgame_win.shadow_stamper = False 
                game.tetrisgame_win.game_started = False
                game.tetrisgame_win.stamper_queue = []
                clear_shapelists()
                game.counter = 200
                game.counterbase = 200
            time.sleep(0.01)
        while game.current_win == game.tetrisgame_win:
            if game.running == False:
                return
            if game.tetrisgame_win.game_started == False:
                start_message()
                game.tetrisgame_win.game_started = True
            while len(game.tetrisgame_win.stamper_queue) < 4:
                instance = game.tetrisgame_win.stamp_maker()
                game.tetrisgame_win.stamper_queue.append(instance)
                if len(game.tetrisgame_win.stamper_queue) == 4:
                    game.tetrisgame_win.queue_arranger()
            if game.tetrisgame_win.current_stamper == False:
                game.tetrisgame_win.gameoverchecker()
                game.tetrisgame_win.current_stamper = game.tetrisgame_win.stamper_queue[0]
                game.tetrisgame_win.create_shadowstamper()
                reposition_stamper()
                game.tetrisgame_win.put_on_matrix()
                game.tetrisgame_win.stamper_queue.pop(0)
                for i in game.tetrisgame_win.current_stamper.squarelist:
                    game.canvas.tag_raise(i.shape)
            instance = False
            game.counter += -1
            time.sleep(0.01)
            if game.counter == 0:
                game.counter = game.counterbase
                game.tetrisgame_win.current_stamper.move_ud(25)


# Windows                
game.mainmenu_win = class_window("mainmenu_win", "orange", 0, 0, 600,600)     
game.tetrisgame_win = class_window_game("tetrisgame_win", "green", 0, 0, 600,600)  
game.highscore_win = class_window("highscore_win", "green", 0, 0, 600,600) 
game.pause_win = class_window("pause_win", "grey", 150,450,450,150)
game.gameover_win = class_window("gameover_win", "orange", 125,475,475,125)

# highscore
game.highscore_win.scoredict = {}
game.highscore_win.titletext = game.canvas.create_text(300,50, text="High Scores", font=("Arial", 24))
game.highscore_win.shapelist.append(game.highscore_win.titletext)

# mainmenu_win
startbutton = button(225,100,"Start", game.tetrisgame_win) # need to change the last arg
highscoresbutton = button(225,175,"High Scores", game.highscore_win)
exitbutton = button(225,250,"Exit", "na")
menuselector = selector(225,100)
game.mainmenu_win.titletext = game.canvas.create_text(300,50, text="Tkinter Tetris", font=("Arial", 24))
game.mainmenu_win.shapelist.append(game.mainmenu_win.titletext)
game.mainmenu_win.buttonlist = [startbutton, highscoresbutton, exitbutton, menuselector]

# tetrisgame_win
game.tetrisgame_win.upnext_shape = game.canvas.create_rectangle((30,120,145,500), fill="black", width = 0.5, outline = "white")
game.tetrisgame_win.upnext_text = game.canvas.create_text(85,105,text="UP NEXT", font=("Arial", 12))
game.tetrisgame_win.level = 1
game.tetrisgame_win.level_text = game.canvas.create_text(300,30,text=("Lv.",game.tetrisgame_win.level), font=("Arial", 24))
game.tetrisgame_win.score = 0
game.tetrisgame_win.score_container = game.canvas.create_rectangle((450,120,570,150), fill="black", width = 0.5, outline = "white")
game.tetrisgame_win.score_text = game.canvas.create_text(510,105,text="SCORE", font=("Arial", 12))
game.tetrisgame_win.instructions_text = game.canvas.create_text(510,175,text="Q,W - Rotate", font=("Arial", 12), fill = "white")
game.tetrisgame_win.instructions_text2 = game.canvas.create_text(510,200,text="Space - Place instantly", font=("Arial", 12), fill = "white")
game.tetrisgame_win.score_display = game.canvas.create_text(510,135,text=game.tetrisgame_win.score, font=("Arial", 12),  fill = "white")
game.tetrisgame_win.shapelist = [game.tetrisgame_win.shape,game.tetrisgame_win.upnext_shape,game.tetrisgame_win.upnext_text,game.tetrisgame_win.level_text,game.tetrisgame_win.score_container,game.tetrisgame_win.score_text,game.tetrisgame_win.score_display, game.tetrisgame_win.instructions_text, game.tetrisgame_win.instructions_text2]

# pausewin
game.pause_win.pause_text = game.canvas.create_text(300,180,text="Game Paused", font=("Arial", 24))
game.pause_win.shapelist.append(game.pause_win.pause_text)
pause_menubutton = button(225,250,"Main Menu", game.mainmenu_win)
pause_exitbutton = button(225,325,"Exit", "na")
pauseselector = selector(225,250)
game.pause_win.buttonlist = [pause_menubutton, pause_exitbutton, pauseselector]

# gameover screen

game.gameover_win.gg_text = game.canvas.create_text(300,155,text="Game Over", font=("Arial", 24))
game.gameover_win.gg_text2 = game.canvas.create_text(300,200,text="Enter your name:", font=("Arial", 12))
game.gameover_win.inputbox = game.canvas.create_rectangle((190,300,410,260), fill="white", width=1, outline = "black")
game.gameover_win.shapelist.append(game.gameover_win.gg_text)
game.gameover_win.shapelist.append(game.gameover_win.gg_text2)
game.gameover_win.shapelist.append(game.gameover_win.inputbox)
gameover_menubutton = button(225,400,"Return", game.mainmenu_win)
gameoverselector = selector(225,400)
game.gameover_win.buttonlist = [gameover_menubutton, gameoverselector]

w1 = game.mainmenu_win # self
def exit_role(w1):
    game.running = False
    sys.exit()
exitbutton.role = MethodType(exit_role, exitbutton)

w2 = game.pause_win # self
def exit_role(w2):
    game.running = False
    sys.exit()
pause_exitbutton.role = MethodType(exit_role, pause_exitbutton)

w3 = game.gameover_win # self
def store_highscore(w3):
    for i in range(2, len(game.highscore_win.shapelist)):
        game.canvas.delete(game.highscore_win.shapelist[i])
    game.highscore_win.scoredict[game.gameover_win.playername_text] = game.tetrisgame_win.score
    game.gameover_win.playername_text = ""
    # for i in len(game.highscore_win.scoredict):
    sortdict = sorted(game.highscore_win.scoredict.items(), key=lambda x:x[1], reverse=True)
    sortdict = dict(sortdict)
    print(sortdict)
    game.highscore_win.scoredict = sortdict        
    cntr = 1
    t_cntr = -1
    for i in game.highscore_win.scoredict:
        game.highscore_win.shapelist.append(game.canvas.create_text(250,135+cntr,text=i, font=("Arial", (18+t_cntr) ),  fill = "white"))
        game.highscore_win.shapelist.append(game.canvas.create_text(350,135+cntr,text=game.highscore_win.scoredict[i], font=("Arial", (18+t_cntr)),  fill = "white"))
        cntr += 25
        t_cntr += -1
    game.tetrisgame_win.score = 0
    game.canvas.delete(game.tetrisgame_win.score_display)
    game.tetrisgame_win.score_display = game.canvas.create_text(510,135,text=game.tetrisgame_win.score, font=("Arial", 12),  fill = "white")
    game.tetrisgame_win.shapelist.append(game.tetrisgame_win.score_display)
    game.bringtofront(game.previous_win, w3.tied_window)
gameover_menubutton.role = MethodType(store_highscore, gameover_menubutton)
                        
for r in range(1,21): # grid creation
    for c in range(1,11):
        game.tetrisgame_win.grid_dict["sq_{0}_{1}".format(r,c)] = square(r,c,150+(c*25),40+(r*25), "#bfb7b6") 

for i in game.mainmenu_win.buttonlist:
    game.mainmenu_win.shapelist.append(i.shape)
    if hasattr(i, "text"):
        game.mainmenu_win.shapelist.append(i.text)

for i in game.pause_win.buttonlist:
    game.pause_win.shapelist.append(i.shape)
    if hasattr(i, "text"):
        game.pause_win.shapelist.append(i.text)        

for i in game.gameover_win.buttonlist:
    game.gameover_win.shapelist.append(i.shape)
    if hasattr(i, "text"):
        game.gameover_win.shapelist.append(i.text)      
        
game.interface.bind("<Destroy>", lambda x: game.exit())

game.bringtofront("na",game.mainmenu_win)
game.rungame()