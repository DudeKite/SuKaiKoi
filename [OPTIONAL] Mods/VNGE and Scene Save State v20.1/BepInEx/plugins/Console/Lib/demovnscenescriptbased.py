#vngame;all;Demos/Game based on VNSceneScript files
def start(game):
    """:type game: vngameengine.VNNeoController"""
    game.skin_set_byname("skin_renpy")
    # -------- some options we want to init ---------
    game.sceneDir = "gamedemo/" # please, move all your scene files in separate folder - to avoid collisions with other vn games

    if game.isClassicStudio:
        game.show_blocking_message_time("Sorry, this is only for NEO engines")
        return

    game.set_text_s("This is demo game, that provides examples of:\n- how to run multiple linear VNSceneScript files\n- how to make in-game choices\n(source: demovnscenescriptbased.py)")
    game.set_buttons_alt(["Start game", startGame])

def startGame(game):
    # demo files located in main folder, not in subfolder - so we need ../ construct before it
    # please, move YOUR files to subfolder
    game.vnscenescript_run_filescene("../vnscscriptdemo1.png", end1)

def end1(game):
    """:type game: vngameengine.VNNeoController"""
    game.set_text_s("What to do next? (example of choice)")
    btns = [
        "To demo 0", startDemo1,
        "To demo Ext", startDemo2,
    ]
    # we run different VNSceneScript files based on choice
    game.set_buttons_alt(btns, "compact")

def startDemo1(game):
    """:type game: vngameengine.VNNeoController"""
    game.vnscenescript_run_filescene("../vnscscriptdemo0.png", endDemo)

def startDemo2(game):
    """:type game: vngameengine.VNNeoController"""
    game.vnscenescript_run_filescene("../vnscscriptdemoext.png", endDemo)

def endDemo(game):
    game.set_text_s("Now demo ended...")
    game.set_buttons_end_game()