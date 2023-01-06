"""
Simple VN Scenes Manager
v1.0

Changelog:
1.0
- initial release
"""

from vngameengine import HSNeoOCIFolder
import codecs

from vngameengine import color_text_gray

def start(game):
    """:type game: vngameengine.VNNeoController"""
    if game.isClassicStudio:
        game.show_blocking_message_time("This is not for Classic Studio. Use NEO")
        return

    # -------- some options we want to init ---------
    game.sceneDir = "vnscenes/" # please, move all your scene files in separate folder in scene folder - to avoid collisions with other vn games

    game.skin_set_byname("skin_renpy")
    #game.sceneDir = "../../Plugins/Console/Lib/gamedemo/" # or place it in subfolder of Lib - this is for Studio
    #game.sceneDir = "../../../Plugins/Console/Lib/gamedemo/" # or place it in subfolder of Lib - this is for NEO-like engines - 1 level bottom

    game.btnNextText = "Next >>" # for localization and other purposes
    game.isHideWindowDuringCameraAnimation = True # this setting hide game window during animation between cameras
    
    # ---------------------------
    # We can define additional characters (other than "s", system)
    # first param is an character ID, second - header text color (RRGGBB), third - name 
    # ---------------------------
    #game.register_char("me", "ff3333", "Me")
    #game.register_char("girl", "ff00ff", "Girl")
    #game.register_char("teacher", "5555aa", "Teacher")
    
    game.gdata.custom_girl = None
    game.gdata.replace_girl_name = None
    game.gdata.replace_mode = "full"
    # game.gdata.replace_girl_name = "Morishima Haruka" # this we need if we change girl by English name

    # if you want to start story immediately (without customize female functions)
    # start_story(game)

    # otherwise, show start menu

    # game.set_text_s("<size=32>Auto Chara Moments 1.0</size>\n\n"+
    #                 "Make a set of screenshots, replacing female chars to chosen in template scenes in 'autocharamoments' folder.")
    # game.set_buttons_alt([
    #     #"Choose girl", cust_female,
    #     "1. Choose template folder", choose_template_folder,
    # ])
    choose_template_folder(game)

def choose_template_folder(game):
    import os

    mypath = game.get_scene_dir() + "/" + game.sceneDir
    listdir = [o for o in os.listdir(mypath) if os.path.isdir(os.path.join(mypath, o))]
    btns = []
    for dir in listdir:
        # print fil[:-3]
        if not dir.startswith("_"):
            # print fil
            btns += [
                dir, (choose_template_folder_on, dir)
            ]

    btns += [
        color_text_gray("<<"), back_to_title
    ]

    game.set_text_s("Choose one of folders in vnscenes:")
    game.set_buttons_alt(btns, "compact")

def choose_template_folder_on(game,param):
    """:type game: vngameengine.VNNeoController"""
    #game.show_blocking_message_time(param)
    game.gdata.tplfolder = param


    choose_template_folder_on2(game)




def choose_template_folder_on2(game):
    #game.gdata.mode_screens = param

    # calc array of files
    from os import listdir
    from os.path import isfile, join

    ar = []
    mypath = game.get_scene_dir() + "/" + game.sceneDir + "/" + game.gdata.tplfolder
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    for fil in onlyfiles:
        # print fil[:-3]
        if fil.endswith(".png") and not fil.startswith("_"):
            ar.append(fil)

    game.gdata.arfiles = ar
    game.gdata.curfile = -1

    move_to_scene(game)




def move_to_scene(game):
    game.set_text_s("Choose scene file:")
    btns = []
    for i in range(len(game.gdata.arfiles)):
        btns.append((game.gdata.arfiles[i])[:-4])
        btns.append((move_to_scene_index, i))
    btns += [
        color_text_gray("<<"), choose_template_folder
    ]
    game.set_buttons_alt(btns, "compact")

def move_to_scene_index(game,index):
    game.gdata.curfile = index-1
    game.skin_set_byname("skin_renpymini")
    next_file_screen(game)

def next_file_screen(game):
    """:type game: vngameengine.VNNeoController"""
    game.gdata.curfile += 1
    curfile = game.gdata.curfile
    if curfile >= len(game.gdata.arfiles):
        game.set_text_s("<size=32>End of Story</size>")
        game.set_buttons_alt([
            "Choose another novel", back_to_start,
            "End game", back_to_title,
        ])
    else:
        game.set_text_s("...")
        game.set_buttons_alt([])
        if "neoadvik" in game.gdata.arfiles[curfile]:
            print "Try loading Advanced IK scene file...", game.gdata.arfiles[curfile]
            sup_load_scene_advancedik(game,game.gdata.tplfolder+"/"+game.gdata.arfiles[curfile])
        else:
            print "Try loading normal scene file...", game.gdata.arfiles[curfile]
            sup_load_scene(game,game.gdata.tplfolder+"/"+game.gdata.arfiles[curfile])

        game.set_timer(0.3, scene_loaded)

        #if game.gdata.mode_screens == "manual":
        #game.set_text_s("Scene %s / %s"%(curfile+1,str(len(game.gdata.arfiles))))

        # game.set_buttons_alt([
        #     #"Make screenshot", make_screenshot,
        #     "Next scene > ", next_file_screen
        # ])

def scene_loaded(game):
    """:type game: vngameengine.VNNeoController"""
    game.set_text_s(".....")

    if HSNeoOCIFolder.find_single_startswith(":vnscenescript:"):
        pass
        game.set_timer(0.5, scene_loaded2)
    else:
        game.show_blocking_message_time("Can't find VNSceneScript header. This is not correct VN Scene file; please, try other")



def scene_loaded2(game):
    """:type game: vngameengine.VNNeoController"""
    try:
        game.vnscenescript_run_current(scene_script_ended)
    except Exception, e:
        import traceback
        print "vnscenescript_run_current execute"
        traceback.print_exc()
        game.show_blocking_message_time("Error during running scene script - some errors in txt file")

def scene_script_ended(game):
    game.set_text_s("<size=32>End of Story</size>")
    game.set_buttons_alt([
        "End game", back_to_title,
    ])
    # special case if last scene
    """
    curfile = game.gdata.curfile
    if curfile == len(game.gdata.arfiles)-1:
        next_file_screen(game)
        return



    game.set_text_s("...")
    game.set_buttons_alt([
        "Next scene > ", next_file_screen
    ])
    """

def back_to_start(game):
    """:type game: vngameengine.VNNeoController"""
    game.reset()
    game.skin_set_byname("skin_default")
    start(game)

def back_to_title(game):
    game.return_to_start_screen_clear()

# --------------- below is support functions ------------
# --------------- normally, you don't need to change them ------------
# but you can add some more of them

# --------- support functions -----------

def sup_load_scene(game,param):
    # load scene
    # if game.gdata.custom_girl != None: # if we have custom girl, we need more proceed
    #     load_scene_with_replace(game,param)

    game.load_scene(param)


def sup_load_scene_advancedik(game, path):
    # if game.gdata.custom_girl != None: # if we have custom girl, we need more proceed
    #     load_scene_with_replace(game,path)

    game.load_scene(path)
    game.set_timer(0.5, (load_scene_advancedik_late, path))

def load_scene_advancedik_late(game, file):
    game.set_timer(1.5, (load_scene_advancedik_late2, file))


def load_scene_advancedik_late2(game, file):
    import clr
    clr.AddReference('HSStudioNEOExtSave')
    from HSStudioNEOExtSave import StudioNEOExtendSaveMgr
    from os import path
    fullpath = path.join(game.get_scene_dir(), game.sceneDir + file)
    StudioNEOExtendSaveMgr.Instance.LoadExtData(fullpath)
    StudioNEOExtendSaveMgr.Instance.LoadExtDataRaw(fullpath)


