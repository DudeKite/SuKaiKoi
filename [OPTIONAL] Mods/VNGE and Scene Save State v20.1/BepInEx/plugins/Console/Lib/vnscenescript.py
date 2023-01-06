#vngame;all;VN Scene Script Editor-Viewer
"""
VN Scene Script by Keitaro
v3.0

Changelog:
1.0
- Initial release
1.1
- Added Developer utils - button to add typical header
- Devutil: save action with current camera in debug mode
- Devutil: can add dummy texts on default cameras
- Devutil: sync with file vnscene_sync.txt.
Just place commands in that file, and then sync it with scene.
You can do it multiple times
- Debug mode use compact buttons
1.2
- Cleanup after finishing game
- Dutil: added function dutil_syncwithfile_full
1.5
- Dev: some useful buttons
- A action: return no more than 3 params. 3 param can contain : symbols (needed for vnframe ext)
2.0
!! acode construction
- dev utils for new version
- version is saved in game.scenedata.scVer
- internal vars moved to game.scenedata to correct cleaning
!! "nul" action - do nothing
- in text actions - "\n" replaces to \n
!! "txtf" action - show text as third param, can contain ":" symbols;
example :a:1:txtf:s::Some text with : symbol
- flipsync10 extension to start engine fake lip sync
2.1
- Devutil: sync with files acode, sync
- Devutil: template for v20
- Devutil: colorizing
2.2
- Devutil: vnframe11
- Devutil: gagency01
2.3
- UTF-8 support during sync with text files
2.5
- show custom buttons in compact way
- support scene params "end" in nextstate and addbtn calls
- optimized blank states processing - no recursion, while cycle now
- added emergency out if state is over 1000000
- "addbtnrnd" action to move to state randomly. Syntax: addbtnrnd:<btntext>:<states separated by ",">  Example: addbtnrnd:Random action:200,300,400
- v25 by default - changed menu items to handle it
2.6
- option to run scene from arbitrary state (start_menu(param = {"startState": arbitState})
3.0
- timernext support syntax: timernext:<time>:<nextstate>
- new commands: showui, hideui, hideui:<timerforhide>
- Ministate button run cmd - addbtnms:<text>:<ministatename>
- upgrade to run v30
- Adv cam function - camoanim3:<camstr>:<duration>:<style>:<effZoomOut>:<effRotX>:<effRotZ> (use 0.0 if you don't want effects)
- Ministate immediately run cmd - runms:<ministatename>
- game is not hide UI during animation by default - you can do it manually
- support scene params "next" in addbtn calls
- commands for control buttons in UI - lockui/lockui:timeout/unlockui
3.1
- small update handling new way :acode folder
"""
from vngameengine import HSNeoOCIFolder, HSNeoOCI

def start(game):
    """:type game: vngameengine.VNNeoController"""
    # -------- some options we want to init ---------
    game.btnNextText = ">>" # for localization and other purposes
    #game.isHideWindowDuringCameraAnimation = True # this setting hide game window during animation between cameras

    if game.isClassicStudio:
        game.show_blocking_message_time("VN Scene Script can't run on Old Studio. Use NEO")
        return

    #game.set_text_s("Scene script test")
    #game.set_text_s(get_all_infos(game))
    #start_menu(game, {'mode': 'view'})

    #game.set_text_s("---")
    #game.set_buttons_end_game()

    # :paramint:maxstate:5
    # :param:test:testval
    game.set_text_s("Welcome to "+"<b>VN Scene Script</b>!"+"\nIt's a way to implement and run code, located in scene folders text")
    game.set_buttons_alt([
        "Run current scene as VN Scene Script scene", start_current_menu,
        "Demos", start_demos,
        "Developer utils", dev_utils,
    ])

def dev_utils(game):
    game.set_text_s("Developer utils:\nModify scene in way:")
    game.set_buttons_alt([
        color_text_yellowlight("Add headers >>"), dev_utils_headers,
        "", None,
        color_text_green("vnscene_acode.txt > :acode"), (dutil_syncwithfile_full_acode, (":acode", "vnscene_acode.txt")),
        color_text_red(":acode > vnscene_acode.txt"), (dutil_syncwithfile_param_back, (":acode", "vnscene_acode.txt")),

        "vnscene_sync.txt > -syncfile-", (dutil_syncwithfile_param, ("-syncfile-","vnscene_sync.txt")),
        "-syncfile- > vnscene_sync.txt", (dutil_syncwithfile_param_back, ("-syncfile-","vnscene_sync.txt")),
        #"vnscene_cam.txt > -cams-", (dutil_syncwithfile_param, ("-cams-", "vnscene_cam.txt")),

        "vnscene_mline.txt > selected", (dutil_syncwithfile_loadmline_to_selected, "vnscene_mline.txt"),
        "<<", start,
    ], "compact")

def dev_utils_headers(game):
    game.set_text_s("Developer utils:\nHeaders:")
    game.set_buttons_alt([
        color_text_yellowlight("Add template for v25"), dutil_header20,
        #"Add header (110f)", dutil_header0,
        #"Add header (30f)", dutil_header00,
        #"Add header (110) and defpack", dutil_header1,
        "Tpl v10 (header+defpack)", dutil_header1,

        color_text_blue("AddExt 'vnframe11' and init"), dutil_header3,
        color_text_blue("AddExt 'flipsync' and init"), dutil_header4,
        "Add :acode", dutil_header2,
        "Add dummy text for 10 cameras", dutil_adddummytext_forcameras,
        color_text_blue("AddExt 'gagency01'"), (dutil_header_param, [":useext:gagency01"]),
        #"+Ext 'gagency01'", (dutil_header_param, [":useext:gagency01"]),
        "<<", dev_utils,
    ], "compact")

def dutil_header0(game):
    fold1 = HSNeoOCIFolder.add(":vnscenescript:v25:110")

def dutil_header00(game):
    fold1 = HSNeoOCIFolder.add(":vnscenescript:v25:30")

def dutil_header20(game):
    fold1 = HSNeoOCIFolder.add(":vnscenescript:v25:30")
    lines = ["next", "txtf:s::Some text on cam 1", "cam:1", "next", "txtf:Girl::Hey! This text show on cam 2!", "cam:2"]
    dutil_acode_addlines(game,(':acode', lines))

def dutil_header1(game):
    fold1 = HSNeoOCIFolder.add(":vnscenescript:v25:110")
    fold2 = HSNeoOCIFolder.add(":a:i:util:defpack")
    fold2.set_parent(fold1)

def dutil_header2(game):
    fold1 = HSNeoOCIFolder.add(":acode")

def dutil_header3(game):
    addaction_to_headerfolder(game, ":useext:vnframe12")
    addaction_to_headerfolder(game, ":a:i:f_stinit")

def dutil_header4(game):
    addaction_to_headerfolder(game, ":useext:flipsync10")
    addaction_to_headerfolder(game, ":a:i:initflipsync:v10")

def dutil_header_param(game,param):
    for str in param:
        addaction_to_headerfolder(game, str)

def start_file(game,file):
    """:type game: vngameengine.VNNeoController"""
    game.load_scene(file)
    start_current_menu(game)

def start_demos(game):
    """:type game: vngameengine.VNNeoController"""
    game.set_text_s("Available demos:")
    btns = [
        "0.Simplest demo", (start_file, "vnscscriptdemo0.png"),
        "1.Simple demo", (start_file,"vnscscriptdemo1.png"),
        "2.Demo for extension making (adv)", (start_file,"vnscscriptdemoext.png")
    ]
    if game.isCharaStudio:
        btns += [
            "Hot Story (CharaStudio, large story, long load)", (start_file, "vnschotstory.png"),
        ]

    game.set_buttons_alt(btns)

def start_current_menu(game):
    game.set_text_s("Choose mode for run story:")
    game.set_buttons_alt([
        "View mode >", start_cur_view,
        "Debug mode (for developers) >", start_cur_debug
    ])

def start_cur_view(game):
    """:type game: vngameengine.VNNeoController"""
    game.run_menu(start_menu,{'mode': 'view'},game_end_buttons)

def start_cur_debug(game):
    """:type game: vngameengine.VNNeoController"""
    game.run_menu(start_menu,{'mode': 'debug'},game_end_buttons)

def game_end_buttons(game):
    #game.set_text("s", "Demo finished here... hope you like it and will made something by yourself! :)")
    game.set_text_s("Game ended!")
    game.set_buttons(["Restart game >", "Return to title >"],[toRestart, toEnd2])

def toEnd2(game):
    """:type game: vngameengine.VNNeoController"""
    cleanup(game)
    game.return_to_start_screen()

def toRestart(game):
    game.run_menu(start_menu, game.scenedata.scRunParams, game_end_buttons)

# ------------------------ actual VN Scene Script functions ------------------

def start_menu(game,param = None):
    """:type game: vngameengine.VNNeoController"""
    if param == None:
        param = {'mode': 'view'}

    game.scenedata.scRunMode = param["mode"]
    game.scenedata.scRunParams = param

    # remove frame for preview in CharaStudio
    if game.scenedata.scRunMode == "view":
        if game.isCharaStudio:
            if str(game.scene_get_framefile()).startswith('vnscenescriptframe'):
                game.scene_set_framefile("")

    # set all to default
    game.scenedata.scMaxState = 0

    # initialize script
    try:
        game.scenedata.scScriptAll = scene_get_all_infos(game)
    except Exception, e:
        err = "ERROR: can't analyze scene\n"
        err += "(details: %s)"%str(e)
        game.show_blocking_message_time(err)
        return
    #print "--- raw ---"
    #print game.scenedata.scScriptAll

    checkerr = check_correct(game)
    if checkerr == "":

        txt_to_script_tree(game)
        """
        print "--- params ---"
        print game.scenedata.scScriptParams
        print "--- actions ---"
        print game.scenedata.scScriptActions
        """
        print "--- extensions ---"
        print game.scenedata.scScriptExtsTxt
        #print "--- show declares ---"
        #print game.scenedata.scScriptShowDeclares

        load_extensions(game)
        run_state_actions(game,-1) # prepare

        startState = 0
        if "startState" in param:
            startState = param["startState"]

        run_state(game,startState,True)
    else:
        game.show_blocking_message_time(checkerr)

def check_correct(game):
    scrtxt = game.scenedata.scScriptAll
    try:
        for obj in scrtxt:
            txt = obj[0]
            """:type txt: string"""
            if txt.startswith(':vnscenescript:'):
                ar = txt.split(":")
                if ar[2][0] == "v":
                    ver = int(ar[2][1:])
                    if (ver == 10 or ver == 20 or ver == 25 or ver == 30):
                        maxstate = int(ar[3])
                        if maxstate > 0:
                            game.scenedata.scMaxState = maxstate
                            game.scenedata.scVer = ver
                            return ""
                        else:
                            return "Incorrect maxstate in header (must be >0)\n\n(header must be like :vnscenescript:v10:<maxstate>)"
                    else:
                        return "Incorrect VNSceneScript version in header (must be v10)\n\n(header must be like :vnscenescript:v10:<maxstate>)"
                else:
                    return "Sorry, can't find VNSceneScript version in header\n\n(header must be like :vnscenescript:v10:<maxstate>)"
    except Exception, e:
        err = "ERROR: can't check scene header correctness\n"
        err += "(details: %s)"%str(e)
        return err
    return "Sorry, but this scene is not a VNSceneScript\n\n(can't find the :vnscenescript: header)"

def get_all_infos(game):
    str = ""
    #from UnityEngine import Object
    #from Studio import BackgroundCtrl
    #UnityEngine.Object.FindObjectsOfType < CharAnimeCtrl > ();
    ar = game.scenedata.scScriptAll
    for obj in ar:
        str += obj[0]+"\n"
    return str

def load_extensions(game):
    exts = []
    error = ""
    for ext in game.scenedata.scScriptExtsTxt:
        try:
            import vngameengine
            mod = vngameengine.import_or_reload("vnscenescriptext_"+ext)
            if mod:
                exts.append(mod)
            else:
                error += "Can't find or load extension '"+ext+"'\n"
        except Exception, e:
            error += "Can't find or load extension '" + ext + "'\n"

    if error != "":
        game.show_blocking_message_time("ERROR in loading extensions:\n"+error+"\n(please, download fresh version of VNSceneScript - it may contain this extensions)")

    game.scenedata.scScriptExts = exts
    return error

def txt_to_script_tree(game):
    scrtxt = game.scenedata.scScriptAll

    params = {}
    actions = []
    showdeclares = []
    exts = []
    for obj in scrtxt:
        txt = obj[0]
        """:type txt: string"""
        ar = txt.split(":")
        #print ar

        if len(ar) > 1:
            if ar[1] == "param":
                params[ar[2]] = ar[3]
            if ar[1] == "paramint":
                params[ar[2]] = int(ar[3])
            if ar[1] == "a":
                act = parse_action_string(txt)
                act["treeobj"] = obj[2]
                actions.append(act)
            if ar[1] == "show" or ar[1] == "showch":
                act = {}
                act["action"] = ar[1]
                act["states"] = parse_states_str(ar[2])
                act["treeobj"] = obj[2]
                showdeclares.append(act)
            if ar[1] == "useext":
                exts.append(ar[2])

            # v2.0 feature

            if ar[1] == "acode":
                if game.scenedata.scVer >= 20:
                    #print game.scenedata.scVer
                    curframe = 0
                    if len(ar) > 2:
                        curframe = int(ar[2])

                    #treeobj0 = obj[2]
                    """:type treeobj0: dummyneoclasses.TreeNodeObject"""
                    #targ = treeobj0.child[0]
                    targ = obj[2]
                    for treeobj in targ.child:
                        treeobj = treeobj
                        """:type treeobj: dummyneoclasses.TreeNodeObject"""
                        #ar2.append(HSNeoOCI.create_from_treenode(treeobj))
                        res = acode_parse(treeobj,curframe)
                        if isinstance(res,int):
                            curframe = res
                        else:
                            actions.append(res)

                        # process subchilds
                        for treeobj2 in treeobj.child:
                            res = acode_parse(treeobj2, curframe)
                            if isinstance(res, int):
                                curframe = res
                            else:
                                actions.append(res)

                else:
                    print "Error: acode support for versions 2.0 and above, cur version is {0}".format(game.scenedata.scVer)



    game.scenedata.scScriptParams = params
    game.scenedata.scScriptActions = actions
    game.scenedata.scScriptShowDeclares = showdeclares
    game.scenedata.scScriptExtsTxt = exts

def acode_parse(treeobj,curframe):
    return acode_parse_text(treeobj.textName,curframe,treeobj)

def acode_parse_text(textName,curframe,treeobj):
    if textName == "next":
        curframe += 1
        return curframe
    else:
        if textName.startswith('nextf:'):
            arr = textName.split(":")
            curframe = int(arr[1])
            return curframe
        else:
            acttext = ":a:{0}:{1}".format(curframe, textName)
            # print acttext
            act = parse_action_string(acttext)
            act["treeobj"] = treeobj
            #actions.append(act)
            return act

def parse_action_string(txt):
    ar = txt.split(":", 6)
    act = {}
    # act["arcode"] = ar
    act["origintext"] = txt
    act["states"] = parse_states_str(ar[2])
    act["action"] = ar[3]
    if len(ar) > 4:
        act["actionparam"] = ar[4]
        if len(ar) > 5:
            act["actionparam2"] = ar[5]
            if len(ar) > 6:
                act["actionparam3"] = ar[6]
    return act

def util_action_append(game,actiontxt):
    game.scenedata.scScriptActions.append(parse_action_string(actiontxt))

def parse_states_str(str):
    if str == "i": return [-1]
    result = []
    ar1 = str.split(",")
    for el in ar1:
        ar2 = el.split("-")
        if len(ar2) == 1:
            # no '-' - so simple case like 2
            result.append(int(ar2[0]))
        else:
            # case 1-3
            result += range(int(ar2[0]),int(ar2[1])+1)
    return result

    # simple now
    #return [int(str)]


def scene_get_all_infos(game):
    """:type game: vngameengine.VNNeoController"""
    from Studio import OCIFolder
    ar = []
    dobjctrl = game.studio.dicInfo
    for key in dobjctrl.Keys:
        objctrl = dobjctrl[key]
        if isinstance(objctrl, OCIFolder):
            txt = objctrl.name
            if txt[0] == ":":
                # all starting with :
                ar.append((objctrl.name, objctrl, key))
    return ar

def run_state_wr(game,param):
    run_state(game,param[0],param[1])

def run_ministate(game,param):
    import libministates
    libministates.ministates_run_elem_by_name(game,param)

def run_state(game,state,skipnull):
    """:type game: vngameengine.VNNeoController"""

    isRunCycle = True

    while isRunCycle:
        # if finished - go out
        if state == game.scenedata.scMaxState+1 or state >= 1000000: # 1000000 is enough for all
            if state >= 1000000:
                print "VNGE: VNSceneScript: emergency out, state is over 1000000"
            cleanup(game)
            game.menu_finish(state)
            return

        game.scenedata.scNextState = state+1
        game.scenedata.scIsTimerNext = False
        game.scenedata.scACustomButtons = []

        # running actions

        # at first - obviously actions
        cntactions = run_state_actions(game,state)

        # hide unneeded
        cntshow = 0
        cnthide = 0
        for act in game.scenedata.scScriptShowDeclares:
            if act["action"] == "show":
                if state in act["states"]:
                    if set_treeobj_visible(act["treeobj"],True):
                        cntshow+=1
            if act["action"] == "showch":
                if state in act["states"]:
                    if set_treeobj_visible(act["treeobj"].parent.parent.parent,True):
                        cntshow+=1

        for act in game.scenedata.scScriptShowDeclares:
            if act["action"] == "show":
                if not (state in act["states"]):
                    if set_treeobj_visible(act["treeobj"], False):
                        cnthide+=1
            if act["action"] == "showch":
                if not (state in act["states"]):
                    if set_treeobj_visible(act["treeobj"].parent.parent.parent, False):
                        cnthide+=1

        #print "State %s: actions %s, show %s, hide %s"%(str(state),str(cntactions),str(cntshow),str(cnthide))

        nextstate = game.scenedata.scNextState # this may be modified by actions

        isRunCycle = False # we processed anything

        #... but....
        if skipnull:
            # if we have no actions - progress to next state
            if cntactions == 0 and cntshow == 0:
                #run_state(game, nextstate, True)
                state = nextstate
                isRunCycle = True
                #return

    # end IS RUN CYCLE to find first non-empty state

    # otherwise, set buttons
    if game.scenedata.scIsTimerNext:
        # setted timer for next state, no need to buttons
        game.set_buttons_alt([])
    else:
        if len(game.scenedata.scACustomButtons) > 0:
            # we have action-defined buttons - so, render them
            game.set_buttons_alt(game.scenedata.scACustomButtons, "compact")
        else:
            if game.scenedata.scRunMode == "view":
                game.set_buttons_alt([">>", (run_state_wr, (nextstate, True))])
            if game.scenedata.scRunMode == "debug":
                btnsalt = [
                    "Cur state %s >>" % (str(state)), (run_state_wr, (nextstate, True)),
                    "Cur state %s >> (no skip)" % (str(state)), (run_state_wr, (nextstate, False)),
                    "Save :a:st:camo:<campos>", (dutil_campos, str(state)),
                           ]
                for ext in game.scenedata.scScriptExts:
                    try:
                        btnsalt += ext.debug_buttons(game,state)
                    except Exception, e:
                        pass
                game.set_buttons_alt(btnsalt, "compact")
            if game.scenedata.scRunMode == "hiddenscript":
                # don't render buttons - it's up to main game
                pass
    game.scenedata.scLastRunnedState = state
    game.scenedata.scNextExpectedState = nextstate

def run_state_actions(game,state):
    cntprocessed = 0
    for act in game.scenedata.scScriptActions:
        if state in act["states"]:
            res = run_action(game,act)
            if not res:
                print "Error: Can't find action like '%s' in '%s'"%(act["action"],act["origintext"])
            cntprocessed += 1
    return cntprocessed

def set_treeobj_visible(treeobj,visible):
    if treeobj.visible != visible:
        treeobj.SetVisible(visible)
        return True
    return False

def run_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    # nul action in 2.0
    if act["action"] == "nul":
        return True

    # ------- texts --------
    if act["action"] == "txt":
        text = act["actionparam2"].replace("\\n","\n")
        game.set_text(act["actionparam"],text)
        return True
    if act["action"] == "txtf":
        text = act["actionparam3"].replace("\\n","\n")
        game.set_text(act["actionparam"],text)
        return True
    if act["action"] == "txts":
        text = act["actionparam"].replace("\\n", "\n")
        game.set_text_s(text)
        return True
    if act["action"] == "regchar":
        game.register_char(act["actionparam"],act["actionparam2"],act["actionparam3"])
        return True

    # ------- cameras --------
    if act["action"] == "cam":
        game.to_camera(int(act["actionparam"]))
        return True
    if act["action"] == "camanim":
        game.anim_to_camera_num(1,int(act["actionparam"]),"fast-slow")
        return True
    if act["action"] == "camanim2":
        game.anim_to_camera_num(2,int(act["actionparam"]),{'style':"linear",'target_camera_zooming_in':float(act["actionparam2"])})
        return True
    if act["action"] == "camcuranim" or act["action"] == "camcur":
        #game.anim_to_camera_num(1,int(act["actionparam"]),"fast-slow")

        camobj = game.get_camera_num(0)  # get current camera position - as 0 index
        if act["actionparam"] == "roty":
            v3 = camobj["rotate"]  # getting vector for rotate
            camobj["rotate"] = game.vec3(v3.x, v3.y + float(act["actionparam2"]), v3.z)  # set new rotation
        if act["actionparam"] == "rotz":
            v3 = camobj["rotate"]  # getting vector for rotate
            camobj["rotate"] = game.vec3(v3.x, v3.y, v3.z + float(act["actionparam2"]))  # set new rotation
        if act["actionparam"] == "rotx":
            v3 = camobj["rotate"]  # getting vector for rotate
            camobj["rotate"] = game.vec3(v3.x + float(act["actionparam2"]), v3.y, v3.z)  # set new rotation
        if act["actionparam"] == "disz":
            v3 = camobj["distance"]  # getting vector for distance
            camobj["distance"] = game.vec3(v3.x, v3.y, v3.z+ float(act["actionparam2"]))

        # target
        if act["action"] == "camcuranim":
            game.anim_to_camera_obj(1, camobj, "fast-slow")  # animate to this camera
        if act["action"] == "camcur":
            game.move_camera_obj(camobj)
        return True

    if act["action"] == "camo" or act["action"] == "camoanim" or act["action"] == "camoanim2" or act["action"] == "camoanim3":
        try:
            ar = act["actionparam"].split(",")
            pos = (float(ar[0]),float(ar[1]),float(ar[2]))
            dist = (float(ar[3]), float(ar[4]), float(ar[5]))
            rot = (float(ar[6]), float(ar[7]), float(ar[8]))
            fov = float(ar[9])
            camobj = game.camparams2vec(pos,dist,rot,fov)
            #print "camo: "
            #print camobj
            if act["action"] == "camo":
                game.move_camera_obj(camobj)
            if act["action"] == "camoanim":
                game.anim_to_camera_obj(1, camobj, "fast-slow")  # animate to this camera
            if act["action"] == "camoanim2":
                game.anim_to_camera_obj(2, camobj,
                                        {'style': "linear", 'target_camera_zooming_in': float(act["actionparam2"])})
            if act["action"] == "camoanim3":
                endparams = act["actionparam3"].split(":")
                objrun = {'style': endparams[0]}

                p1 = float(endparams[1])
                p2 = float(endparams[2])
                p3 = float(endparams[3])

                if p1 != 0.0:
                    objrun["target_camera_zooming_in"] = p1*2
                if p2 != 0.0:
                    objrun["target_camera_rotating_x"] = p2*2
                if p3 != 0.0:
                    objrun["target_camera_rotating_z"] = p3*2

                game.anim_to_camera_obj(float(act["actionparam2"]), camobj, objrun)
            return True
        except Exception, e:
            print "Error in camo action: "+str(e)

    # ------- utils --------
    if act["action"] == "util":
        run_util(game, act["actionparam"])
        return True
    if act["action"] == "nextstate":
        game.scenedata.scNextState = statestr_to_int(game,act["actionparam"])
        return True
    if act["action"] == "timernext":
        if act.has_key("actionparam2") and len(act["actionparam2"]) > 0:
            game.scenedata.scNextState = statestr_to_int(game,act["actionparam2"])
        game.scenedata.scIsTimerNext = True
        game.set_timer(float(act["actionparam"]),_on_timer_next)
        return True
    if act["action"] == "addbtn":
        st = statestr_to_int(game,act["actionparam2"])
        game.scenedata.scACustomButtons.append(act["actionparam"])
        game.scenedata.scACustomButtons.append((run_state_wr, (st, True)))
        return True
    if act["action"] == "addbtnrnd":
        #st = statestr_to_int(game,act["actionparam2"])
        arr = act["actionparam2"].split(",")
        print arr
        from vngameengine import random_choice
        st = statestr_to_int(game, random_choice(arr))
        game.scenedata.scACustomButtons.append(act["actionparam"])
        game.scenedata.scACustomButtons.append((run_state_wr, (st, True)))
        return True
    if act["action"] == "addbtnms":
        #st = statestr_to_int(game,act["actionparam2"])
        game.scenedata.scACustomButtons.append(act["actionparam"])
        game.scenedata.scACustomButtons.append((run_ministate, act["actionparam2"]))
        return True
    if act["action"] == "runms":
        #st = statestr_to_int(game,act["actionparam2"])
        #game.scenedata.scACustomButtons.append(act["actionparam"])
        #game.scenedata.scACustomButtons.append((run_ministate, act["actionparam2"]))
        run_ministate(game,act["actionparam"])
        return True
    if act["action"] == "showui":
        game.visible = True
        return True
    if act["action"] == "hideui":
        game.visible = False
        if act.has_key("actionparam") and len(act["actionparam"]) > 0:
            #game.scenedata.scNextState = statestr_to_int(game,act["actionparam2"])
            game.set_timer(float(act["actionparam"]),show_ui)
        return True
    if act["action"] == "unlockui":
        game.isHideGameButtons = False
        return True
    if act["action"] == "lockui":
        game.isHideGameButtons = True
        if act.has_key("actionparam") and len(act["actionparam"]) > 0:
            game.set_timer(float(act["actionparam"]),unlock_ui)
        return True




    # ------- extensions --------
    for ext in game.scenedata.scScriptExts:
        if ext.custom_action(game,act):
            return True

    return False

def show_ui(game):
    game.visible = True

def unlock_ui(game):
    game.isHideGameButtons = False

def statestr_to_int(game,statestr):
    if statestr == "end":
        #print "end, ", game.scenedata.scMaxState + 1
        return game.scenedata.scMaxState + 1

    if statestr == "next":
        #print "next: ", game.scenedata.scNextState
        return game.scenedata.scNextState

    return int(statestr)

def _on_timer_next(game):
    """:type game: vngameengine.VNNeoController"""

    # simple hack - run 0 button in game
    #game.call_game_func(game._vnButtonsActions[0])
    run_state(game,game.scenedata.scNextExpectedState,True)

def run_util(game,param):
    # utils for start
    if param == "cam110":
        for i in range(10):
            atxt = ":a:%s:cam:%s"%(str((i+1)*10),str(i+1))
            util_action_append(game,atxt)
    if param == "charsg4b4":
        gcolor = "ee99ee"
        gcolor3 = "99ee99"
        bcolor = "9999ee"
        game.register_char("q", "aaaaaa", "? ? ?")
        game.register_char("g",gcolor,"Girl")
        game.register_char("gs", gcolor, "Girls")
        game.register_char("g1", gcolor, "Girl 1")
        game.register_char("g2", gcolor, "Girl 2")
        game.register_char("g3", gcolor3, "Girl 3")
        game.register_char("b", bcolor, "Boy")
        game.register_char("bs", bcolor, "Boys")
        game.register_char("b1", bcolor, "Boy 1")
        game.register_char("b2", bcolor, "Boy 2")
    if param == "defpack":
        run_util(game, "cam110")
        run_util(game, "charsg4b4")

# new in 1.1.

def get_headerfolder(game):
    """
    scrtxt = game.scenedata.scScriptAll
    for obj in scrtxt:
        txt = obj[0]
        if txt.startswith(':vnscenescript:'):
            return HSNeoOCIFolder(obj[1])
    return None
    """
    return HSNeoOCIFolder.find_single_startswith(':vnscenescript:')

def addaction_to_headerfolder(game,name):
    fold = HSNeoOCIFolder.add(name)
    fold.set_parent(get_headerfolder(game))

def dutil_campos(game,state):
    #game.show_blocking_message_time(game.camera_calcstr_for_vnscene())

    c = game.studio.cameraCtrl
    cdata = c.cameraData

    s1 = "%s,%s,%s,23.0" % (str(cdata.pos), str(cdata.distance), str(cdata.rotate))

    calcstr = ":a:%s:camo:%s" % (str(state), s1.replace("(", "").replace(")", "").replace(" ", ""))
    #game.show_blocking_message_time(calcstr)
    fold = HSNeoOCIFolder.add(calcstr)
    fold.set_parent(get_headerfolder(game))
    game.show_blocking_message_time("Action saved for state %s under vnscenescript header!\n(%s)"%(str(state),calcstr))

def dutil_adddummytext_forcameras(game):
    for i in range(10):
        atxt = ":a:%s:txt:s:(text on cam %s)" % (str((i + 1) * 10), str(i + 1))
        addaction_to_headerfolder(game,atxt)

    game.show_blocking_message_time(
        "Actions added to vnscenescript header!")

def dutil_syncwithfile(game):
    dutil_syncwithfile_full(game,"-syncfile-","vnscene_sync.txt")

def dutil_syncwithfile_param(game, param):
    dutil_syncwithfile_full(game,param[0],param[1])

def dutil_syncwithfile_param_back(game, param):
    dutil_syncwithfile_full_back(game,param[0],param[1])

def dutil_syncwithfile_full(game,foldername,filename):
    import codecs
    fold = HSNeoOCIFolder.find_single(foldername)
    if fold == None:
        # create
        header = get_headerfolder(game)
        fold = HSNeoOCIFolder.add(foldername)
        if header != None:
            fold.set_parent(header)

    fname = filename
    try:
        with codecs.open(fname, encoding="utf-8") as f:
            content = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]

        # remove old content
        fold.delete_all_children()

        for x in content:
            if not x.startswith("#"):
                if x != "":
                    newfld = HSNeoOCIFolder.add(x)
                    newfld.set_parent(fold)

    except Exception, e:
        game.show_blocking_message_time("Can't find or read file %s in game root folder"%fname)


def dutil_syncwithfile_full_acode(game,param):
    import codecs
    foldername, filename = param
    fold = HSNeoOCIFolder.find_single(foldername)
    if fold == None:
        # create
        header = get_headerfolder(game)
        fold = HSNeoOCIFolder.add(foldername)
        if header != None:
            fold.set_parent(header)

    fname = filename
    try:
        with codecs.open(fname, encoding="utf-8") as f:
            content = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]

        # remove old content
        fold.delete_all_children()

        fldnext = fold
        for x in content:
            if not x.startswith("#"):
                if x != "":
                    newfld = HSNeoOCIFolder.add(x)
                    if x == "next":
                        newfld.set_parent(fold)
                        fldnext = newfld
                    else:
                        newfld.set_parent(fldnext)

    except Exception, e:
        game.show_blocking_message_time("Can't find or read file %s in game root folder"%fname)

def dutil_acode_addlines(game,param):
    foldername, content = param

    fold = HSNeoOCIFolder.find_single(foldername)
    if fold == None:
        # create
        #header = get_headerfolder(game)
        fold = HSNeoOCIFolder.add(foldername)
        #if header != None:
        #    fold.set_parent(header)

    fldnext = fold
    for x in content:
        if not x.startswith("#"):
            if x != "":
                newfld = HSNeoOCIFolder.add(x)
                if x == "next":
                    newfld.set_parent(fold)
                    fldnext = newfld
                else:
                    newfld.set_parent(fldnext)



def dutil_syncwithfile_full_back(game,foldername,filename):
    import codecs
    fold = HSNeoOCIFolder.find_single(foldername)

    if fold == None:
        game.show_blocking_message_time("Can't find folder '%s'" % foldername)
        return

    fname = filename
    try:
        f = codecs.open(filename, 'w+', encoding="utf-8")
        for fch in fold.treeNodeObject.child:
            obj = HSNeoOCI.create_from_treenode(fch)
            if isinstance(obj,HSNeoOCIFolder):
                f.write("%s\n"%obj.name)
                # process subchildren
                if obj.treeNodeObject.childCount > 0:
                    for fch2 in obj.treeNodeObject.child:
                        obj2 = HSNeoOCI.create_from_treenode(fch2)
                        if isinstance(obj2, HSNeoOCIFolder):
                            f.write("%s\n" % obj2.name)
        f.close()

    except Exception, e:
        game.show_blocking_message_time("Can't write to file %s in game root folder"%fname)
        return

    game.show_blocking_message_time("Writed to file!")

def dutil_syncwithfile_loadmline_to_selected(game,filename):
    import codecs
    fold = HSNeoOCI.create_from_selected()
    if isinstance(fold,HSNeoOCIFolder):

        fname = filename
        try:
            with codecs.open(fname, encoding="utf-8") as f:
                content = f.readlines()
            # remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]

            fold.name = "\\n".join(content)

        except Exception, e:
            game.show_blocking_message_time("Can't find or read file %s in game root folder"%fname)
    else:
        game.show_blocking_message_time("No selected folder; you must select folder to import" % fname)

def cleanup(game):
    game.scenedata.scScriptAll = None
    game.scenedata.scScriptParams = None
    game.scenedata.scScriptActions = None
    game.scenedata.scACustomButtons = None
    game.scenedata.scScriptExts = None
    game.scenedata.scVer = None
    #game.

# util colors

def color_text(text,color):
    return '<color=#{1}ff>{0}</color>'.format(text,color)

def color_text_green(text):
    return color_text(text,"aaffaa")

def color_text_red(text):
    return color_text(text,"ffaaaa")

def color_text_yellowlight(text):
    return color_text(text, "f8e473")

def color_text_blue(text):
    return color_text(text,"aaaaff")

