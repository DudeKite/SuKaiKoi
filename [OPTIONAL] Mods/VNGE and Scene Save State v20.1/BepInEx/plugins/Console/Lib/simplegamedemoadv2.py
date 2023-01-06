# simple Game example for all who need:
# - scene loading
# - advanced - includes examples for move between saved cameras; also includes animation move between cams
# - strict storyline, no choices (only Next button)
def start(game):
    # -------- some options we want to init ---------
    game.sceneDir = "gamedemo/" # please, move all your scene files in separate folder in scene folder - to avoid collisions with other vn games
    #game.sceneDir = "../../Plugins/Console/Lib/gamedemo/" # or place it in subfolder of Lib - this is for Studio
    #game.sceneDir = "../../../Plugins/Console/Lib/gamedemo/" # or place it in subfolder of Lib - this is for NEO-like engines - 1 level bottom
    
    game.btnNextText = "Next >>" # for localization and other purposes
    game.isHideWindowDuringCameraAnimation = True # this setting hide game window during animation between cameras
    game.isfAutoLipSync = True  # enable lip sync in framework
    
    # ---------------------------
    # We can define additional characters (other than "s", system)
    # first param is an character ID, second - header text color (RRGGBB), third - name 
    # ---------------------------
    game.register_char("me", "aa5555", "John-kun")
    game.register_char("main", "55aa55", "Morito-chan")
    game.register_char("teacher", "5555aa", "Teacher")

    # init face expressions
    import vnlibfaceexpressions
    vnlibfaceexpressions.init_faceexpressions(game)

    # ---------------------------
    # If we want to set a number of strict-story-line texts with "Next >" buttons (with no special choices), we can use construct "texts_next"
    # in array (1 param)
    # - 1 param - char ID
    # - 2 param - text
    # - 3 param (if exist) - function to call during text show
    # - 4 param (if exist) - function param
    # last param (2)
    # - function to move at end
    # ---------------------------
    game.texts_next([
        ["me", "Hi! It's me.\nSo, as you can see, I do nothing in the college.", sup_load_scene, "scene1lipsync.png"], # loading scene
        ["me//angry_whatyousay", "Hey, what's going on?...."],
        ["teacher", "Is everybody here?\nI want to introduce our new transfer student...", sup_tocam, 2], # move cam to teacher
        ["teacher//angry_whatyousay", "...Kawashima Morito"],
        ["teacher//normal", "Please, Morito, tell something to everyone.", sup_tocam_animated, 3], # animated move cam to morito
        ["main", "Hi! My name is Morito, I'm a new transfer student from Tokyo."],
        ["main", "!...(what to say)..."], # ! begins the silent construction
        ["main", "...m-m...I like cats..."],
        ["main", "...m-m...Glad to see everyone!"],
        ["me", "So, we have new cute transfer student. It may be interested... May be spy on she on break?", sup_tocam, 5],
        ["me", "..wait until break, and then..."], 
        ["me", "..investigate the female toilet >"],
        ["me", "Wow... and this is so elegant and strict Morito-chan?", sup_load_scene, "scene2.png"]
    ], toEnd)
    
def sup_load_scene(game,param):
    game.fake_lipsync_stop() # required by framework - stop lipsynd if we has it
    game.load_scene(param)
    game.set_timer(0.2, sup_reg_framework) # required by framework - we need actors and props after scene load

def sup_reg_framework(game):
    game.scenef_register_actorsprops()

def sup_tocam(game,param):
    # instant move to camera
    game.to_camera(param)    
    
def sup_tocam_animated(game,param):
    # animated move to camera - 3 seconds, with-fast-slow movement style
    game.anim_to_camera_num(3, param, "fast-slow3")
    #game.anim_to_camera_num(3, param, {'style':"linear",'zooming_in_target_camera':6}) # cool camera move with zoom-out - zoom-in
    
def toEnd(game):
    game.set_text("s", "Demo finished here... hope you like it and will made something by yourself! :)")
    game.set_buttons_end_game()   