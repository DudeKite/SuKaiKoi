#vngame;charastudio;Demos/VNFrame Tutorial for Chara

# UTF-8 encode is not supported T.T
# -*- coding: UTF-8 -*-
from vnactor import *
from vnframe import *

def start(game):
    # use importOrReload to keep vnactor and vnframe updated
    # it is useful if you want to modify vnactor or vnframe script
    from vngameengine import importOrReload
    importOrReload("vnactor")
    importOrReload("vnframe")

    # enable scene anime function provide by vnframe
    init_scene_anime(game)

    # enable lip sync provide by vngameengine
    game.isfAutoLipSync = True # enable lip sync in vngameengine
    
    # auto hide and lock style for your game, these are global settings
    game.isHideWindowDuringCameraAnimation = False
    game.isLockWindowDuringSceneAnimation = True
    
    # -------- some options we want to init ---------
    game.sceneDir = "wcf\\" # please, move all your scene files in separate folder - to avoid collisions with other vn games
    game.btnNextText = "Next >>" # for localization and other purposes
    
    # load scene and start a timer to init scene after loaded
    game.load_scene("vnftut.png")
    game.scnLoadTID = game.set_timer(60, load_scene_timeout, load_scene_wait)   # 60s should be enough, if your scene is really big, make the number bigger!
    print "start load scene"
    
def load_scene_timeout(game):
    # this is called when load scene timeouted
    toEnd(game, "ERROR: Load scene timeout!")
    
def load_scene_wait(game, dt, time, duration):
    # check if scene is loaded
    if game.isFuncLocked == False:
        game.clear_timer(game.scnLoadTID)
        init_scene(game)
        print "load and init scene done!\n"

def init_scene(game):
    try:
        # show our game window
        game.visible = 1
        game.isHideGameButtons = 0
        
        # load actor/prop from scene by "tag folder", must be called after scene is loaded
        register_actor_prop_by_tag(game)
        
        # init script helper, must be called after actor/prop registered
        sh = init_script_helper(game)
        # you can change some script helper setting here
        #sh.baseNest = "        "       # base nest space of dumpped script
        #sh.nestWord = "    "           # space inserted when script is nested
        #sh.masterMode = True           # enable master mode can disable the prompt message for DANGEROUS buttons

        # here game start! For a long story, separate it into several parts is good for test. 
        # You can skip to your interested scene by enable it and comment out others
        start_seq1(game)   # Just hello scene
        #start_seq2(game)   # Test space for you
        #start_seq3(game)   # The introduce and basic idea of VNFrame
        #start_seq4(game)   # Details about script
        #start_seq5(game)   # Introduce of script helper

    except Exception as e:
        toEnd(game, "init_scene FAILED: "+str(e))

def start_seq1(game):
    # in an sequence scene, which user only click next to move forward, we can just use game.texts_next() provided by vngameengine
    # first parameter is a "text-list", the first text in the list will be displayed immediately, then wait for user click 'next' button to process the next text
    # every text can set a function and its parameter, which will be called by game engine when the text is displayed.
    # second parameter is a function which will be called after all texts in list is displayed, usually we go next.
    game.texts_next([
        ["main", "Hello! Me again!"],          # the simplest todo-item is a list with just two number: 1st is who, 2nd is the words what he say
    ], start_seq2)                      # and after user click "next", goto next sequence

def start_seq2(game):
    # this sequence is left empty for you to test you own script.
    game.texts_next([
        # Paste your script here and restart the game to see the result


    ], start_seq3)

def start_seq3(game):
    game.texts_next([
        ["main", "This simple game is a step-by-step tutorial for you if you are interested in VNFrame and plan to build game with it.\nIt's boring! Because I'm trying sooooooo hard to not move a lot to keep the script simple!!", act, {
            'cam': {'goto_pos': ((0.156, 1.246, -0.466), (0.000, 0.000, -2.688), (2.600, 182.450, 0.000))},
            'main': {'anim': (0, 5, 15)},
        }],
        ["main", "OK. VNFrame is a framework to help you control characters and items. Just need some scripts in the texts_next() function and they will be animated!"],
        ["main", "You should explore the simplegamedemo.py to get the basic idea of vngameengine, and then this python script for the sample code to initialize VNFrame."],
        ["main", "At first, to use this frame, you need do some work when build your scene in CharaStudio. There may be a lot of charaters and items, the framework need to know which one to deal with."],
        ["main", "In this simple scene, open the workspace tree view please, you can see there are just me, a floor and a magicbox folder. There is a folder named '-actor:main:ff5555' under my hair->pony, a folder named '-prop:box' under the magicbox folder, and a folder named '-prop:led' under the core.", act, {
            'cam': {'goto_pos': ((0.544, 1.271, 0.025), (0.000, 0.000, -2.080), (0.000, 185.650, 0.000))},
            'main': {'anim': (0, 0, 13)},
        }],
        ["main", "These folders are called 'TAG', our frame scan the TAGs at initialization stage and then get a list of 'Actors' and 'Props'. Anything without TAG will be ignored by frame."],
        ["main", "The '-actor:<id>:<color>:<name>' TAG is for actor. It must be 3-level child of character, for example under hair->pony. It also register character for text output with <color> and <name>. If <name> is obmitted, frame will use the char's name in the tree view."],
        ["main", "The '-prop:<id>' TAG is for prop. It must be 1-level child of item or folder. They are almost the same, except folder has no color attribute and it can't be scaled."],
        ["main", "And there are two reserved ids. 'cam' for camera and 'sys' for system. You don't need to define them.\nAll ids must be ASCII encoded because UTF-8 is not supported yet, and of course, no repetition!", act, {
            'cam': {'goto_pos': ((0.456, 1.246, 0.106), (0.000, 0.000, -2.255), (-0.850, 179.700, 0.000))},
            'main': {'anim': (0, 5, 25)},
        }],
        ["main", "Now let's talk about anime. The anime is based on timer. VNFrame uses two timers, one for camera and the other for scene anime. So camera can move separately but everything else in the scene share one timer."],
        ["main", "If you have looked inside simplegamedemoadv.py, you should known that texts_next() function can set one function to callback when texts are displayed. In the VNFrame, we prepared two powerful functions for you."],
        ["main", "One is 'act()' function, which takes a dict as parameter. The dict is a todo list, and act() function will do them at once. So act() is not for scene anime, but it can start a camera anime."],
        ["main", "The other is 'anime()' function, this one takes a tuple as parameter. The tuple is a sequenced todo list, and anime() will use the scene timer to do the anime work!"],
        ["main", "Functions are ready, what you need to do is write the parameter for the function, and I call them 'scripts'. If you open the python file vngdemo.py of <Laboratory Girl>, you will notice most of the codes are these scripts in veeeery complicated nested struction."],
    ], start_sel1)
    
def start_sel1(game):
    game.set_text("main", "Are you ready for this?")
    game.set_buttons(["Yeah, go on please.", "Er... I heard there is a simple way ..."], [start_seq4, start_seq5_p1])

def start_seq4(game):
    #game.texts_next([
    debug_game_texts_next(game, 0, [    # instead of game.texts_next(), you can use debug_game_texts_next(), which let you assign which text start from by index. Good for debug.
        ["main", "Great!"],
        ["main", "I will need my magicbox to help...", act, {
            'cam': {'goto_pos': ((0.005, 1.091, -0.031), (0.000, 0.000, -3.680), (1.050, 180.450, 0.000))}, # this one set the camera
            'main': {'anim': (0, 0, 24)},   # this one set the anime of main actor
        }],
        ["main", "Appears! Magicbox!", act, {   # act() function take a dict as parameter
            'box': {'visible': 1},   # use id of actor/prop/cam/sys as the key to appoint the target, then a dict of action function and parameter
        }],
        ["main", "To do this simplest action, we use act() function with a script:\n<b>{'box': {'visible': 1}}</b>\nIt is a dictionary. The key of dict is the id of target prop, in this script the 'box'. Contents of this dict is nested dict. In this case, it says call the 'visible' function with param '1', and so it appeared!"],
        ["main", "You can set multi action function at same time, use script like:\n<b>{'box': {'move_to': (0, 1.2, 0), 'rotate_to': (0, 45, 45)}}</b>\nIt tells act() we want to run <b>move</b> and <b>rotate</b> for <b>box</b>.", act, {   
            'box': {'move_to': (0, 1.2, 0), 'rotate_to': (0, 45, 45)}   # you can set multi action function for a target id at the same time
        }],
        ["main", "And set action for multi id at same time, use script like:\n<b>{'box': {'move_to': (0, 1, 0), 'rotate_to': (0, 0, 0)},\n' led': {'color': (1, 0, 0)}}</b>\nIt tells act() we want to run <b>move</b> and <b>rotate</b> for <b>box</b> and <b>color</b> for <b>led</b>.", act, {
            'box': {'move_to': (0, 1, 0), 'rotate_to': (0, 0, 0)},   # And also to multi target id as the same time
            'led': {'color': (1, 0, 0)},    # just add another key in the param dict of act()
        }],
        ["main", "We can control the actor/cam/sys in just the same way! But action function valid for actor/prop/cam/sys are different. They can be found in the vnframe.py, search for <b>char_act_funcs</b>, <b>prop_act_funcs</b>, <b>cam_act_funcs</b>, <b>sys_act_funcs</b> for a completed list, and refer to defination of each function for their parameters."],
        ["main", "Thank you magicbox and Bye!\nThat's all about script for act(). Not so difficult isn't it? Though act() takes action at once so it can't do anime...", act, {
            'box': {'visible': 0},
            'led': {'color': (0, 1, 1)},
        }],
        ["main", "NO! Try this!\n<b>{'main': {'anim': (7, 22, 1)},\n 'cam' : {'rotate': ((0, 360, 0), 10)}}</b>\nact() can not do scene anime, but capable for play build-in anime and start a camera anime! For details of camera anime, check techdemo.", act, {
            'main': {'anim': (7, 22, 1)},   # by calling the "anim" function, we can play in-game anime of actor
            'cam' : {'rotate': ((0, 360, 0), 10)}   # and all function for cam can be animated, it use camera timer separated from scene timer.
        }],
        ["main", "Ok, when you can understand the script for act(), let's move on to anime().", act, {
            'main': {'anim': (0, 0, 24)}, 
        }],
        ["main", "Magicbox Again!", anime, (   # act() function take a tuple as parameter, so if you have only one element int tuple, dont forget add a ',' at the end
            {'box': {'visible': 1}},   # the element of tuple can be just the same dict script used for act()
        )],
        ["main", "This time we used anime() function with a script:\n<b>({'box': {'visible': 1}},)</b>\nMmm... it seems we just put our act() script into a tuple...\nActually it is, and in fact anime() will call act() to process the script."],
        ["main", "Because tuple is a sequenced data, and anime should be sequenced. So if we do this:\n<b>({'box': {'move_to': (0, 1.2, 0)}},\n {'box': {'rotate_to': (0, 45, 45)}},)</b>\nThe box should be moved and then rotated! But sorry, it happens too fast, we can't tell the difference with the trick we did with act().", anime, (
            {'box': {'move_to': (0, 1.2, 0)}},      # there are sequened act() script, but it happens too fast so looks just act the same time
            {'box': {'rotate_to': (0, 45, 45)}},
        )],
        ["main", "To make the anime, we need to write the script like this:\n<b>(({'box': {'move_to': ((0, 1, 0), (0, 1.2, 0))}}, 2, 'linear'),)</b>\nAha! Another nested tuple! That's the real format of anime script! Put a act() script into a tuple, follow by the anime duration and anime style... Oh, notice the parameter of <b>move_to</b> becomes tuple too! A tuple likes (from, to).", anime, (
            {'box': {'rotate_to': (0, 0, 0)}},
            ({'box': {'move_to': ((0, 1, 0), (0, 1.2, 0))}}, 2, 'linear'),      # full format of single element of anime() script should be a tuple with 3 element, 1st the act() like script, 2nd the duration of anime, 3rd the style of anime
        )],
        ["main", "And then we can see the two sub-animes happen in sequence clearly:\n<b>(({'box': {'move_to': ((0, 1, 0), (0, 1.2, 0))}}, 2),\n ({'box': {'rotate_to': ((0, 0, 0), (0, 45, 45))}}, 2))</b>\nIn this case, we obmitted the anime style, so it will use linear style by default. Valid anime style is just the same as camera anime, check vngameengine for detail.", anime, (
            ({'box': {'move_to': ((0, 1, 0), (0, 1.2, 0))}}, 2),        # if 3rd element (style) is obmitted, use the 'linear' by default. And if 2nd element (duration) is obmitted too, it shrinks into a act() script.
            ({'box': {'rotate_to': ((0, 0, 0), (0, 45, 45))}}, 2),
        )],
        ["main", "It can animated in sequence, and it can animated in the same time:\n<b>((({'box': {'move_to': ((0, 1, 0), (0, 1.2, 0)), 'rotate_to': ((0, 0, 0), (0, 45, 45))}}, 2))</b>\nJust like act() script. Write the script in the same sub-anime.", anime, (
            ({'box': {'move_to': ((0, 1, 0), (0, 1.2, 0)), 'rotate_to': ((0, 0, 0), (0, 45, 45))}}, 2),        # anime in the same time, just like act() script
        )],
        ["main", "You can control multi props/actors at the sametime. And then put them in sequence to make a cool animation. Check the start_seq4() function in this python script, it contains the actual scripts demonstrated here with comments.", anime, (
            ({
                'box': {'move_to': ((0, 1, 0), (0, 1.3, 0)), 'rotate_to': ((0, 0, 0), (0, 45, 45))},
                'led': {'color': ((0, 1, 1), (1, 0, 0))},
            }, 2, 'fast-slow'),        # control two props at the same time, not a problem, wrote them into one sub-anime
            ({
                'box': {'move_to': ((0, 1.3, 0), (0, 1, 0)), 'rotate_to': ((0, 45, 45), (0, 90, 90))},
                'led': {'color': ((1, 0, 0), (0, 1, 1))},
            }, 2, 'slow-fast'),        # and combine sub-animes together to design your animation
            ({
                'box': {'move_to': ((0, 1, 0), (0, 1.3, 0)), 'rotate_to': ((0, 90, 90), (0, 180, 180))},
                'led': {'color': ((0, 1, 1), (1, 0, 0))},
            }, 2, 'fast-slow'),
            ({
                'box': {'move_to': ((0, 1.3, 0), (0, 1, 0)), 'rotate_to': ((0, 180, 180), (0, 0, 0))},
                'led': {'color': ((1, 0, 0), (0, 1, 1))},
            }, 2, 'slow-fast'),
        )], 
        ["main", "That's all about anime() script. Please note that not all action function can do anime. Those functions take boolean value and int value can not do animation. If you want to use them in the anime() script, write separately in a sub-anime without duration setting, so act() will take care about them.", act, {
            'box': {'visible': 0},
        }],
        ["main", "act() script is simple but anime() script is really deep nested. You must be careful! One misplaced comma or bracket will break the script. So my advice is:\n1. Use act() script as much as possible.\n2. Use build-in anime as much as possible.\n3. Use 'script helper' as much as possible.", act, {
            'sys': {'btn_next': "What script helper?"},     # temporary set the next button text of current scene, it will be restore to default on next scene.
        }],
        ["main", "Script helper is the new experimental feature of VNFrame, which can dump script of act() and anime() by setting on UI.", act, {
            'sys': {'btn_next': "... Tell me that first!!"},
        }],
        
    ], start_seq5)
    
def start_seq5_p1(game):
    game.texts_next([
        ["main", "All right... there is...An experimental feature calls 'script helper'."],
    ], start_seq5)

def start_seq5(game):
    game.texts_next([
        ["main", "It looks like this...\nThis is the default view, a lot of option is hidden by now.", act, {
            'sys': {'bg_png': 'vnftut_cap1.png'},
            'cam': {'goto_pos': ((-0.531, 1.023, 0.629), (0.000, 0.000, -4.025), (3.850, 202.500, 0.000))},
            'main': {'anim': (0, 0, 13)},
        }],
        ["main", "Now I expanded all options. Looks complicated isn't it? So I added some note for you.\n If you can't see the background picture clearly, you can find the png file in UserData\Studio\scene\wcf folder and open it with a viewer soft.", act, {
            'sys': {'bg_png': 'vnftut_cap2.png'},
        }],
        ["main", "It is as an enhanced scene dumper, press Ctrl-F5 to toggle between main window and script helper. Or you can press Ctrl-F4 to call the Develop console out, and then press 'Dump Scene' button to access script helper.\nOh Wait! It will hijack the main game window, so when you open it, you cannot read my words. Remember if you want to back to the game window, press the 'Back To Scene' button or hit Ctrl-F5 again!"],
        ["main", "Script helper will save all the supported properties of actors and props, Oh, and camera of course, when you initialize it. And then you can set you scene, press the dump button, and scripts are ready for you! Fantastic isnt it!?"],
        ["main", "To make it more clear, magicbox sample again! But this time you do the operation, follow my instruction please...\nIn the studio workspace tree view check the magicbox to show it. Now open script helper(CTRL-F5), choose dump 'diff' as 'new act', uncheck 'include camera' but check 'To file', then click 'Dump Script'.", act, {
            'main': {'anim': (0, 0, 3), 'move_to': (0.460, 0.000, 0.100), 'cloth_all': (0, 0, 0, 0, 3, 0, 0, 0), 'acc_all': (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1), 'look_at': 1, 'visible': 1, 'rotate_to': (0.000, 355.000, 0.000)},
        }],
        ["main", "Open the dumppython.txt in your game folder. A new script added into it. Its a act script, which can make the magicbox visible!\nOh, and may be some script for me, if you dump the script before I finished my talk."],
        ["main", "Now let's try some anime. Move the magicbox in the scene, open script helper, choose dump 'diff' as 'new anime', set duration to 3 second, then click 'Dump Script'. DaDa, the anime script for the move is ready for you!"],
        ["main", "You want to check the anime you just made at once right? Understood, click the 'To Anime Buffer' button at the center bottom of the script helper window."],
        ["main", "And window changed to this...\nAs you just build an anime, click the 'Replay' and you should see it! 'To Start' and 'To End' button can be used to check the start and end status of current clip, and if you have several clips ready, 'Play & Next' can check them one by one.", act, {
            'sys': {'bg_png': 'vnftut_cap3.png'},
        }],
        ["main", "If you are reviewing an anime clip, you can adjust texts, anime duration and style. But notice anything else include camera anime setting can not be adjusted by now, means you must roll back and build the script again if you are not satisfied with them."],
        ["main", "When you are OK with you work, click 'Dump Anime Buffer' button to dump all script into dumppython.txt. The output code can be used as the first parameter of texts_next() function directly."],
        ["main", "Now, some advice on build script!\n-Dump 'Diff' is good enough for most case, dump 'Full' will output a long-long stript which is hard to read, dump 'None' if you only want some texts output or only care about the camera.", act, {
            'sys': {'bg_png': 'vnftut_cap2.png'},
            'main': {'anim': (0, 5, 23)},
        }],
        ["main", "-'new act' make things happen immediately, 'new anime' make animation, both of them need you click the 'Next >>' button in game to start play, except they are the first one in sequence. 'sub anime' make animation too, but it will be played after previous anime is over, without user operation. All anime can do act work, just set the duration to 0." ],
        ["main", "-Texts can be modified easily after you dump the script, but it good to write something just as the comment of script clip.\n-Hide window or button in anime if you don't want player to interrupt your anime. There are global settings for hide window or button, check the python code. If you used the global setting, you dont need to check them here."],
        ["main", "-There is some limitation with the script helper, some feature like change coordinate, add voice is not supported yet. And if you want to make IK/FK anime, you need do addition work. IK/FK anime is not well supported yet!\n-And if you think this window is disturbing you when setting scene, press Ctrl-F8 will hide it and hit Ctrl-F8 again to show."],
        ["main", "Some notice on those <color=#ff0000>DANGEROUS</color> buttons:\n-'Preview in scene' let you preview your clips in game play. Preview start from current selected clip. Unlike the 'play & next', preview will display texts and combine the sub-anime together. <b>BUT</b>, preview will overwrite the previous texts_next() setting, and when preview over, returns to script helper.", act, {
            'sys': {'bg_png': 'vnftut_cap3.png'},
            'main': {'anim': (0, 5, 25)},
        }],
        ["main", "-'Roll back' will delete not just current clip but also following clips! And set the reference status to the end of previous clip.\n - Reference status is which we take diff from when we build script clip. If you want to assign current scene as the reference status, use the 'Ref to current' button. But notice, it only affect next clip you build, not existed ones."],
        ["main", "-'Rescan & Reset' will rescan the TAG folder, clear all clips, and set reference status to current scene. It may be convenient if you edited TAGs, Oh, don't forget save your scene."],
        ["main", "The last but not the least, from vngameengine 7.6 you can always call the 'Script Helper' out by press Ctrl-F5. And the scene when you call 'Script Helper' first time will be the reference scene by default.", act, {
            'sys': {'bg_png': ''},
            'cam': {'goto_pos': ((0.432, 1.052, 0.130), (0.000, 0.000, -2.960), (0.000, 165.650, 0.000))},
            'main': {'anim': (0, 1, 21)},
        }],
        ["main", "Also you can initialize it manually then access from 'dump scene' of develop console. In this game, I've already do the initialization for you. When you write your own game, copy the magic words <b>init_script_helper(game)</b> into your code! It should be called after you registered actors/props."],
        ["main", "Now, it's your time. Try it yourself. You can paste your script to start_seq2() function and restart the game to check!", act, {
            'main': {'anim': (0, 0, 25)},
        }],
    ], start_seq6)

def start_seq6(game):
    game.texts_next([
        ["main", "Oh, I am really tired now... If you like the frame and want to use its code, feel free to do! All I wish is to see your cool game!", act, {
            'cam': {'goto_pos': ((0.432, 1.362, 0.130), (0.000, 0.000, -1.235), (5.750, 176.000, 0.000))},
            'main': {'anim': (0, 2, 1)},
        }],
    ], toEnd)
    
def toEnd(game, text="<size=32>THE END</size>"):
    game.set_text_s(text)
    game.set_buttons_end_game()
