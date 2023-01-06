# vn game engine demo for by Keitaro-kun
def start(game): #
    # -------- some options we want to init ---------
    game.sceneDir = "gamedemo/" # please, move all your scene files in separate folder - to avoid collisions with other vn games
    # ----------- actual game start -------
    # ---------------------------
    # 1 lesson: we can output some system text. With basic HTML tags, of course
    # first param ("s") is a character name. If is set to "s", so it SYSTEM message
    # ---------------------------
    game.set_text("s", "Hello, <b>stranger</b>! Do you really want to dive in this slutty little game?")
    # ---------------------------
    # 2 lesson: we must define Buttons and corresponding Actions
    # first param is an array of Buttons texts, second - Actions - as links for functions
    # ---------------------------
    game.set_buttons(["Of course!", "No, really..."], [toSc1_0, toExit1])


def toExit1(game):
    game.set_text("s", "So... I can't help you :)")
    game.set_buttons(["Restart game >"], [start])

def toSc1_0(game):
    # ---------------------------
    # 3 lesson: we can define additional characters
    # first param is an character ID, second - header text color (RRGGBB), third - name 
    # ---------------------------
    game.register_char("me", "aa5555", "John-kun")
    game.set_text("me", "Hi! It's me.\nSo, as you can see, I do nothing in the college.")
    game.set_buttons(["Next >"], [toSc1_1])
    # ---------------------------
    # 4 lesson: we can load scenes from game folder
    # ---------------------------
    game.load_scene("scene1.png")

def toSc1_1(game):
    game.set_text("me", "Hey, what's going on?....")
    game.set_buttons(["Next >"], [toSc1_2])

def zoomIn(game):
    # lesson - we can animate our camera if we want
    game.anim_sim_zoom_in(0.3) # 0.3 seconds zoom in

def zoomOut(game):
    # lesson - we can animate our camera if we want
    game.anim_sim_zoom_out(0.3) # 0.3 seconds zoom out


def toSc1_2(game):
    # define other characters...
    # please, name the main character with "main" id. I hope to use it in future
    game.register_char("main", "55aa55", "Morito-chan")
    game.register_char("teacher", "5555aa", "Teacher")

    # ---------------------------
    # 5 lesson: we can move between cameras by camera num
    # of course, we can load scene instead, but camera move is faster
    # ---------------------------
    game.to_camera(2)

    game.set_text("teacher", "Is everybody here?\nI want to introduce our new transfer student...")
    game.set_buttons(["Next >"], [toSc1_3])
    
def toSc1_3(game):
    #game.move_camera(pos=(0.8, 2.0, -0.1), dir=(0.0, 0.0, -0.4), angle=(11.9, -2.2, 0.0), fov=23.0)
    
    # ---------------------------
    # 6 lesson: if we want to set a number of strict-line texts with "Next >" buttons (with no special choices), we can use construct "texts_next"
    # in array (1 param)
    # - 1 param - char ID
    # - 2 param - text
    # - 3 param (if exist) - function to call during text show
    # - 4 param (if exist) - function param
    # last param (2)
    # - function to move at end
    # ---------------------------
    game.texts_next([
        ["teacher", "...Kawashima Morito", sup_sc1_cameraToMorito, ""], # here we not just show text, but move camera to Morito too
        ["teacher", "Please, Morito, tell something to everyone."], 
        ["main", "Hi! My name is Morito, I'm a new transfer student from Tokyo."],
        ["main", "...m-m...I like cats..."],
        ["main", "...m-m...Glad to see everyone!"],
    ], toSc1_4)

def sup_sc1_cameraToMorito(game,param):
    game.to_camera(3)
    #game.anim_to_camera_num(1,3,"fast-slow4") # animated camera example
   
def toSc1_4(game):    
    game.to_camera(5)
    game.set_text("me", "So, we have new cute transfer student. It may be interested... May be spy on she on break?")
    game.set_buttons(["Wait until break >"], [toSc1_5])
    
def toSc1_5(game):    
    game.to_camera(1)
    game.set_text("me", "What to do?")
    game.set_buttons(["Nothing to do", "Spy on female toilet"], [toSc1_6, toSc2_0])

def toSc1_6(game):
    game.set_text("s", "So... nothing happened :)")
    game.set_buttons_end_game()
    
def toSc2_0(game):
    game.load_scene("scene2.png")
    game.set_text("me", "Wow... and this is so elegant and strict Morito-chan?")
    game.set_buttons(["Finish game >", "Zoom IN >", "Zoom OUT >"], [toEnd, zoomIn, zoomOut])
    
def toEnd(game):
    # ---------------------------
    # Adv lesson: we can enable type hinting
    # use vngameengine.VNController as base, or:
    # - vngameenginestudio.StudioController for Studio projects
    # - vngameengine.VNNeoController for NEO-based engines projects - NEO, CharaStudio
    # ---------------------------
    """:type game: vngameengine.VNController"""
    # here we use universal controller
    game.set_text("s", "Demo finished here... hope you like it and will made something by yourself! :)")
    game.set_buttons_end_game()


"""
Cool developers can see description file and read begin of vngameengine.py
"""
    
    