def start(game):
    """:type game: vngameengine.VNController"""
    #game.skin_set_byname("skin_renpy")
    # -------- some options we want to init ---------
    game.sceneDir = "gamedemo/" # please, move all your scene files in separate folder - to avoid collisions with other vn games

    game.set_text("s", "Hello, game! In <b>horizontal</b> groups, the pixels are measured horizontally:")

    game.event_reg_listener("before_scene_load",hook_set_text)
    game.event_reg_listener("before_scene_unload", hook_set_text)

    if game.engine_name == "studio": # Studio only ruris demo
        game.set_buttons(["Simple examples", "Advanced examples", "Ruris demo (manipulating chars alt)"],
                         [simple_tests, (adv_tests, "Advanced examples as param"), ruris_dream])
    else:
        game.set_buttons(["Simple examples", "Advanced examples"],
                         [simple_tests, (adv_tests, "Advanced examples as param")])

    #game.set_buttons(["test"], [toBG])

def toBG(game, newframe):
    """:type game: vngameengine.VNNeoController"""
    if newframe != None:
        game.scene_set_bg_png(newframe)

    game.set_text_s("Cur backg file is %s"%game.scene_get_bg_png_orig())
    btns = [
        "Set bg 1", (toBG, "scene1.png"),
        "Set bg 2", (toBG, "scene2.png"),
        "Set no bg", (toBG, "")
    ]
    game.set_buttons_alt(btns)

def simple_tests(game):
    """:type game: vngameengine.VNController"""
    game.set_text("s", "Simple examples")
    #game.set_buttons(["Text test", "Timer test (15 seconds)", "System message"], [to0, toTimer, toSysMsg])

    btns = [ # alt receive 1 array intermediately placed Text and Functions
        "Text test", to0,
        "Timer test(15 seconds)", toTimer,
        "System message", toSysMsg,
        "Number of buttons", toNumberButtons,
        "Number of compact buttons", toNumberButtons2,
        "Custom Buttons GUI", toCustButtonsGUI,
        "Events handling", eventExample,
        "Save/load game data", saveLoadExample,
    ]
    if not game.isClassicStudio:
        btns += ["Run VNSceneScript as intro", toVNScr]
    if not game.isClassicStudio:
        btns += ["Manipulate folders", manipFolders]
    if game.isCharaStudio:
        btns += ["Set frame file", (toCharaSetFrame, None)]

    game.set_buttons_alt(btns,"compact")

def manipFolders(game):
    game.set_text("s", "Manipulate folders")
    btns = []
    btns += ["Add folders to scene", toAddFolders]
    btns += ["Find and rename folder", foldFindRename]
    btns += ["Find and show/hide folder", foldFindHideShow]
    btns += ["Find and delete all child", foldFindDeleteChild]
    game.set_buttons_alt(btns)

def toAddFolders(game):
    from vngameengine import HSNeoOCIFolder
    fold = HSNeoOCIFolder.add()
    fold.name = "Generated folder"
    fold2 = HSNeoOCIFolder.add("Subfolder")
    fold2.set_parent(fold)
    fold2 = HSNeoOCIFolder.add("Subfolder2")
    fold2.set_parent(fold)

def foldFindRename(game):
    from vngameengine import HSNeoOCIFolder
    try:
        obj = HSNeoOCIFolder.find_single("Generated folder")
        if obj != None:
            obj.name = "Generated folder rename!"
            #obj.visible_treenode = False
        else:
            game.show_blocking_message_time("Can't find folder with name Generated folder")
    except Exception, e:
        print str(e)

def foldFindHideShow(game):
    from vngameengine import HSNeoOCIFolder
    try:
        obj = HSNeoOCIFolder.find_single_startswith("Generated")
        if obj != None:
            #obj.name = "Generated folder rename!"
            obj.visible_treenode = not obj.visible_treenode
        else:
            game.show_blocking_message_time("Can't find folder started with name Generated")
    except Exception, e:
        print str(e)

def foldFindDeleteChild(game):
    from vngameengine import HSNeoOCIFolder
    try:
        obj = HSNeoOCIFolder.find_single_startswith("Generated")
        if obj != None:
            #obj.name = "Generated folder rename!"
            obj.delete_all_children()
        else:
            game.show_blocking_message_time("Can't find folder started with name Generated")
    except Exception, e:
        print str(e)

def toCharaSetFrame(game, newframe):
    if newframe != None:
        game.scene_set_framefile(newframe)

    game.set_text_s("Cur frame file is %s"%game.scene_get_framefile())
    btns = [
        "Set frame 0", (toCharaSetFrame, "koi_studio_frame_00.png"),
        "Set frame 2", (toCharaSetFrame, "koi_studio_frame_02.png"),
        "Set no frame", (toCharaSetFrame, "")
    ]
    game.set_buttons_alt(btns)

def toVNScr(game):
    """:type game: vngameengine.VNNeoController"""
    game.vnscenescript_run_filescene("../vnscscriptdemo1.png", onEndVNScr)

def onEndVNScr(game):
    game.set_text_s("We returned to main game...")
    game.set_buttons_end_game()

def toNumberButtons(game):
    """:type game: vngameengine.VNController"""
    try:
        ar = []
        for i in range(10):
            ar.append("Button number %s"%(str(i+1)))
            ar.append((_NumBtnsCall, i+1))
        game.set_buttons_alt(ar)
    except Exception, e:
        print("Error: " + str(e))


def toNumberButtons2(game):
    """:type game: vngameengine.VNController"""
    try:
        ar = []
        for i in range(13):
            ar.append("Button number %s"%(str(i+1)))
            ar.append((_NumBtnsCall, i+1))
        game.set_buttons_alt(ar, "compact")
    except Exception, e:
        print("Error: " + str(e))

def _NumBtnsCall(game,param):
    game.set_text_s("Btn number %s clicked!"%(str(param)))

def toSysMsg(game):
    """:type game: vngameengine.VNController"""
    game.show_blocking_message_time("System msg will be shown for 5 seconds", 5)

def adv_tests(game, param):
    game.set_text("s", param) # we can pass parameters to functions from set_buttons
    game.set_buttons(["Set custon PNG file as background","Animated camera movement", "Menus", "Manipulating chars"], [(toBG, None),camAnim0, toMenus, toChangeAnim])

def ruris_dream(game):
    import ruris_dream
    ruris_dream.start(game)
    
def to0(game):
    game.register_char("test", "aa5555", "Test-kun")
    game.set_text("test", "Hello, world!")
    game.set_buttons(["Mult texts"], [to02])
    
def to02(game):
    game.texts_next([
        ["s", "Who are you, stranger?"],
        ["test", "I'm so-called Test-kun"],
        ["s", "If you want to load_scene, press Next"]
    ], to1)
    
def to1(game):
    game.set_text("s", "First scene")
    game.set_buttons_end_game()
    #game.load_scene("test.png")
    #import hsgameui
    #
    #import hs
    #hs.load_scene("test.png")
    #hs.place_char("female", "test.png")

def toTimer(game):
    print "Timer start"
    game.set_text("s", "Timer start")
    game.set_timer(15,tEnd,tUpd)
    print "Timer start 2"
    
def tEnd(game):
    game.set_text("s", "Timer end")
    
def tUpd(game,dt,time,duration):
    game.set_text("s", "Time: %s"%str(time))
    #print "Time: %s"%(str(time))

def camAnim0(game):
    game.load_scene("techdemo.png")
    game.set_text("s", "Scene - 1 man, 2 womans")
    #game.set_buttons(["Animate to camera!", "Animate to camera 2 by num!", "By num - slow-fast", "By num - fast-slow"], [camAnim, camAnimNum, camAnimNum2, camAnimNum3])
    game.set_buttons(["Instant move to arbitrary pos","Animate to arbitrary pos","Animate to cam 2!", "To cam 2 - slow-fast style", "Next demos >>"],
                     [toPosInst, toPosAnim, camAnimNum, camAnimNum2, camAnim1])

def camAnim1(game):
    game.set_buttons(
        ["To cam 2 - fast-slow style + on_end_movement_function!", "To cam 2 + zooming-in target camera",
         "Zoom out from cur pos", "Rotate from cur pos", "Next demos >>"],
        [camAnimNum3, camAnimNum4, camAnimNum5, camAnimNum6, camAnim2])

def camAnim2(game):
    game.set_buttons(
        ["To cam 2 + zooming-in + rotate-z",
         "To cam 2 + zooming-in + rotate-x", "To cam 2 + zooming-in + rotate-y", "To cam 2 + zoom-in + rot-x + pos-y", "Next demos >>"],
        [camAnimNum7, camAnimNum8, camAnimNum9, camAnimNum10, None])


def toPosInst(game):
    # for dumping camera position press Ctrl+F3 and read dumppython.txt
    game.move_camera(pos=(0.0, 0.9, 0.0), distance=(0.0, 0.0, -6.7), rotate=(17.6, 204.1, 0.0), fov=23.0)

def toPosAnim(game):
    # for dumping camera position press Ctrl+F3 and read dumppython.txt
    game.anim_to_camera(3,(0.0, 0.9, 0.0), (0.0, 0.0, -6.7), (17.6, 204.1, 0.0), 23.0)

def camAnimNum(game):
    game.anim_to_camera_num(2.5, 2) # 2.5-second move to camera 2 in-scene

def camAnimNum2(game):
    game.anim_to_camera_num(2.5, 2, "slow-fast4") # move to camera 2 in-scene

def camAnimNum3(game):
    game.anim_to_camera_num(2.5, 2, "fast-slow4", onCamEnd) # move to camera 2 in-scene

def camAnimNum4(game):
    game.anim_to_camera_num(4, 2, {'style':"linear",'target_camera_zooming_in':15}) # move to camera 2 in-scene

def camAnimNum5(game):
    """:type game: vngameengine.VNController"""
    camobj = game.get_camera_num(0) # get current camera position - as 0 index
    v3 = camobj["distance"] # getting vector for distance
    camobj["distance"] = game.vec3(v3.x,v3.y,v3.z-5) # set new distance - new Vector3 with z-5 - so, new camera will be far from current position
    game.anim_to_camera_obj(4,camobj) # animate to this camera

def camAnimNum6(game):
    """:type game: vngameengine.VNController"""
    camobj = game.get_camera_num(0) # get current camera position - as 0 index
    v3 = camobj["rotate"] # getting vector for rotate
    camobj["rotate"] = game.vec3(v3.x,v3.y-45,v3.z) # set new rotation
    game.anim_to_camera_obj(2,camobj) # animate to this camera

def camAnimNum7(game):
    game.anim_to_camera_num(4, 2, {'style':"linear",'target_camera_zooming_in':8,'target_camera_rotating_z':50})

def camAnimNum8(game):
    game.anim_to_camera_num(4, 2, {'style':"linear",'target_camera_zooming_in':20,'target_camera_rotating_x':-100})

def camAnimNum9(game):
    game.anim_to_camera_num(4, 2, {'style':"linear",'target_camera_zooming_in':15,'target_camera_rotating_y':-90})

def camAnimNum10(game):
    game.anim_to_camera_num(4, 2, {'style':"linear",'target_camera_zooming_in':2,'target_camera_posing_y':-1,'target_camera_rotating_x':-200})


def onCamEnd(game):
    game.set_text("s", "Camera end movement!")

"""
# only Studio demo test
def toDump(game):
    import hs
    #hs.reset(); hs.configsetup()
    #hs.move_camera(pos=(0.0, 0.9, 0.0), dir=(0.0, 0.0, -5.0), angle=(-26.4, 168.7, 0.0), fov=23.0)
    # begin females
    # girl number 1
    # girl filename 0bd66f425fce0bff5fdd8e98c2d50f79fef62d03.png
    #hsfem = hs.HSFemale.create_female('Loly Nok', attach=True)
    hsfemtmp = hs.place_char("female","0bd66f425fce0bff5fdd8e98c2d50f79fef62d03.png")
    hsfem = hs.HSFemale(chara=hsfemtmp)
    hsfem.reset()
    hsfem.load_animation('custom/cf_anim_custom.unity3d', 'edit_F')
    hsfem.move(pos=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0))
    hsfem.chara.ChangeBlinkFlag(True)
    hsfem.chara.ChangeEyesPtn(0,True)
    hsfem.chara.ChangeMouthPtn(1,True)
    hsfem.chara.ChangeLookNeckPtn(3)
    hsfem.chara.ChangeLookEyesPtn(1)
    hsfem.set_hand_position('l', 'dummy')
    hsfem.set_hand_position('r', 'dummy')
    hsfem.set_clothes_state_all(0)
    hsfem.enable_accessories(1)
"""

def toChangeAnim(game):
    """:type game: vngameengine.VNController"""
    game.load_scene("techdemo.png")
    game.set_text("s", "Scene - 1 man, 2 womans with default animation")
    #game.set_buttons(["Undress girl","Move girl to man"], [undressGirl, moveToMan])
    btns = [
        "Undress girl",undressGirl,
        "Move girl to man",moveToMan
    ]
    if not game.isClassicStudio:
        btns += [
            "Change chara face (old)", neoChangeCharaFace,
            "Change chara (VNActor)", neoChangeCharaFaceActor
        ]
    game.set_buttons_alt(btns)

def neoChangeCharaFace(game):
    """:type game: vngameengine.VNNeoController"""
    ofem = game.scene_get_all_females()[0]
    """:type ofem: vngameengine.HSNeoOCIChar"""
    if not game.isPlayHomeStudio:
        ofem.look_eyes_ptn = 5-ofem.look_eyes_ptn

    # game.show_blocking_message_time("lneck: %s" % str(ofem.look_neck_ptn))
    if not game.isPlayHomeStudio:
        ofem.look_neck_ptn = 1-ofem.look_neck_ptn

    # game.show_blocking_message_time("mouthptn: %s" % str(ofem.mouth_ptn))
    ofem.mouth_ptn = 20-ofem.mouth_ptn

    # game.show_blocking_message_time("mouthopenmax: %s" % str(ofem.mouth_openmax))
    if not game.isPlayHomeStudio:
        ofem.mouth_openmax = 20-ofem.mouth_openmax

    # game.show_blocking_message_time("eyes: %s" % str(ofem.eyes_ptn))
    ofem.eyes_ptn = 37-ofem.eyes_ptn

    # game.show_blocking_message_time("eyebrow: %s" % str(ofem.eyebrow_ptn))
    if game.isCharaStudio: # no eyebrow_ptn in NEO, only in Chara
        ofem.eyebrow_ptn = 16 - ofem.eyebrow_ptn

    # game.show_blocking_message_time("eyeomax: %s" % str(ofem.eyes_openmax))
    if not game.isPlayHomeStudio:
        ofem.eyes_openmax = 1-ofem.eyes_openmax
    game.show_blocking_message_time("Face changed!")

def neoChangeCharaFaceActor(game):
    """:type game: vngameengine.VNNeoController"""
    ofem0 = game.scene_get_all_females()[0]
    """:type ofem0: vngameengine.HSNeoOCIChar"""

    ofem = ofem0.as_actor
    # here we receive Actor object from vnactor.
    # it provide universal interface for all NEO-based engines
    # use it!!

    clothes = ofem.get_cloth()
    ofem.set_cloth(0,1-clothes[0])

    ofem.set_mouth_ptn(20-ofem.get_mouth_ptn())

    game.show_blocking_message_time("Chara changed using VNActor functions!")


def undressGirl(game):
    """:type game: vngameengine.VNController"""
    ofem = game.scene_get_all_females()[0]

    """
    game.scene_get_all_females return array of Females for current scene
    game.scene_get_all_males return array of Males for current scene

    but for Studio this is array of hs.HSFemale or hs.Male
    and for NEO-based engines array of HSNeoOCIChar
    so we must use if to test if this is one engine or another
    """

    if game.isClassicStudio: #
        ofem = ofem; """:type ofem: hs.HSFemale""" # trick for typehinting - ofem is hs.HSFemale object in Studio
        ofem.set_clothes_state_all(1)
    else:
        ofem = ofem; """:type ofem: vngameengine.HSNeoOCIChar"""  # trick for typehinting - ofem is HSNeoOCIChar object in NEO-based engines
        ofem.female_all_clothes_state(1)

def moveToMan(game):
    """:type game: vngameengine.VNController"""
    if game.isClassicStudio:  #
        ofem = game.scene_get_all_females()[0]; """:type ofem: hs.HSFemale"""
        om = game.scene_get_all_males()[0]; """:type om: hs.HSMale"""
        ofem.move(om.pos, om.rot) # move female to man - setting the same pos and rotation
    else:
        ofem = game.scene_get_all_females()[0]; """:type ofem: vngameengine.HSNeoOCIChar"""
        om = game.scene_get_all_males()[0]; """:type om: vngameengine.HSNeoOCIChar"""
        ofem.move(om.pos, om.rot, om.scale) # move female to man - setting the same pos, rotation and scale if needed

    if game.isClassicStudio:
        game.set_buttons(["Change animation"], [toChangeAnim2])
    else:
        game.set_buttons(["Change animation"], [changeAnimNeo])

"""studio classic specific demo animations"""
def toChangeAnim2(game):
    #import hs
    hsfem = game.scene_get_all_females()[0]; # """:type hsfem: hs.HSFemale"""
    # animate params we can receive from Dump scene, using Ctrl+F5 keys and see dumppython.txt
    # you don't need to load_animation inside one animation group - only play_animation_clip
    hsfem.load_animation('h/anim/female/00.unity3d', 'ha_f_01')
    hsfem.play_animation_clip('OLoop')
    
    hsm = game.scene_get_all_males()[0]; # getting Male under num 0
    hsm.load_animation('h/anim/male/00.unity3d', 'ha_m_01')
    hsm.play_animation_clip('OLoop')
    
    game.set_buttons(["Change animation (core functions)!"], [toChangeAnim3]) 

def toChangeAnim3(game):
    game.change_female_num_animation(0, 'WLoop', 'h/anim/female/00.unity3d', 'ha_f_00')
    game.change_male_num_animation(0, 'WLoop', 'h/anim/male/00.unity3d', 'ha_m_00')
    
    game.set_buttons(["Change animation 2 (core functions)!"], [toChangeAnim4]) 

def toChangeAnim4(game):
    #  you don't need to load_animation inside one animation group - only change clip name
    game.change_female_num_animation(0, 'OLoop')
    game.change_male_num_animation(0, 'OLoop')
"""end studio specific"""

def changeAnimNeo(game):
    """:type game: vngameengine.VNController"""
    ofem = game.scene_get_all_females()[0]; """:type ofem: vngameengine.HSNeoOCIChar"""
    om = game.scene_get_all_males()[0]; """:type om: vngameengine.HSNeoOCIChar"""

    # animate params we can receive from Dump scene, using Ctrl+F5 keys and see dumppython.txt
    if game.isStudioNEO:
        # for NEO one params
        ofem.animate(3, 32, 1, 0.0, 1.0)
        om.animate(3, 32, 1, 0.0, 1.0)

    if game.isCharaStudio:
        # for CharaStudio - another
        om.animate(5, 142, 3, 0.0, 2.0)
        ofem.animate(4, 142, 3, 0.0, 2.0)

    if game.isPlayHomeStudio:
        # for PHStudio - another
        om.animate2(7, 66, 3, 1.0)
        ofem.animate2(7, 66, 3, 1.0)


# ----------- menus -------------
def toMenus(game):
    """:type game: vngameengine.VNController"""
    game.load_scene("techdemo.png")
    game.set_text_s("Choose menu demo:")
    game.set_buttons(["Simple menu 1", "Simple menu 2", "Combined menu 1"], [menu1, menu2, menu3])

def menu1(game):
    """:type game: vngameengine.VNController"""
    """
    menus is a powerful subroutines, that allows user to made some decisions until endFunc will be called
    see examples in vnmenusupport
    """
    import vnmenusupport
    game.set_text_s("This menu get all girl list and allows you choose one of them.\nSo, please, choose scene female")
    game.run_menu(vnmenusupport.menu_example_choose_female,"",_menu1)

def _menu1(game):
    """:type game: vngameengine.VNController"""
    femnum = game.menu_result
    ofem = game.scene_get_all_females()[femnum]
    game.set_text_s("You selected girl %s, named %s"%(str(femnum), ofem.text_name))
    game.set_buttons_end_game()

def menu2(game):
    """:type game: vngameengine.VNController"""
    import vnmenusupport
    game.set_text_s("This menu allows you change girl dresses")
    game.run_menu(vnmenusupport.menu_example_undress_female,0,_menuFinished) # undress 0 female - student

def _menuFinished(game):
    game.set_text_s("Menu ended")
    game.set_buttons_end_game()

def menu3(game):
    """:type game: vngameengine.VNController"""
    import vnmenusupport
    game.set_text_s("This as example of combining menu - choose girl and play with clothes")
    game.run_menu(vnmenusupport.menu_exampleadv_choose_undress_female, "", _menuFinished)

# ----------- custom GUI example ---------------

def toCustButtonsGUI(game):
    game.set_text_s("Demo custom buttons interface function\n(you can do whatever you want in Unity functions - colorize etc.)")
    game.set_buttons_alt([],("function", custFunctionGUI))

def custFunctionGUI(game,info):
    """:type game: vngameengine.VNNeoController"""
    from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode

    fullw = info["fwidth"]
    btnheight = info["btnheight"]
    btnstyle = info["btnstyle"]
    labelstyle = info["labelstyle"]



    GUILayout.BeginHorizontal()
    if GUILayout.Button("Btn 1", btnstyle,
            GUILayout.Width(fullw/3-6), GUILayout.Height(btnheight)):
        game.call_game_func((showText, "Clicked btn 1"))

    GUILayout.Label("          some text", labelstyle, GUILayout.Width(fullw/3))

    if GUILayout.Button("<color=#ff6666ff>Btn 2</color>", btnstyle,
            GUILayout.Width(fullw/3-6), GUILayout.Height(btnheight)):
        game.call_game_func((showText, "Clicked btn 2"))

    GUILayout.EndHorizontal()

    GUILayout.BeginHorizontal()
    if GUILayout.Button("Btn Full", btnstyle,
                        GUILayout.Width(fullw), GUILayout.Height(btnheight)):
        game.call_game_func((showText, "Clicked btn Full"))
    GUILayout.EndHorizontal()

def showText(game,param):
    game.set_text_s(param)

# ----------- events example ---------------
def eventExample(game):
    game.set_text_s("Event handling example\nPress button and see console output and code to understand. Also you can load scene and test too")

    game.set_buttons_alt(["Event handle", eventExample2])

def eventExample2(game):
    # register listener for some event
    game.event_reg_listener("set_text", hook_set_text)
    # during this calls we also see the hooks called
    game.set_text_s("Test!")
    game.set_text_s("Test2!")
    game.event_unreg_listener("set_text", hook_set_text)
    # now we unregister listener - and hook will not called
    game.set_text_s("Test3!")

    if(game.isSceneEventsSupported):
        game.event_reg_listener("scene_loaded", hook_scene_loaded)
    # handling

def hook_set_text(game,evid,param):
    print "Hook: ", evid, param

def hook_scene_loaded(game,evid,param):
    print "Hook techdemo scene_loaded: ", evid, param


# ------- save/load example ----
def saveLoadExample(game):
    """:type game: vngameengine.VNNeoController"""

    if game.gpersdata_exists():
        game.gpersdata_load()
        #print game.gpersdata

    if game.gpersdata_get("counter") == None: # is counter already saved?
        game.gpersdata_set("counter", 0)
        # you can save anything you want - list, dictionaries, even objects
        # please, just use only Python objects - not linked with Studio objects (Studio objects can't be serialized to save)

    render_counter(game)

def render_counter(game):
    game.set_text_s("Saved counter: %s\n(press Ctrl+F3 to stop game end return to main window)"%(str(game.gpersdata_get("counter"))))

    game.set_buttons_alt([
        "+1", add1,
        "-1", min1,
        "(clear)", gpersClear
    ])

def add1(game):
    counter = game.gpersdata_get("counter")
    game.gpersdata_set("counter", counter+1)
    render_counter(game)

def min1(game):
    counter = game.gpersdata_get("counter")
    game.gpersdata_set("counter", counter - 1)
    render_counter(game)

def gpersClear(game):
    game.gpersdata_clear()
    saveLoadExample(game)