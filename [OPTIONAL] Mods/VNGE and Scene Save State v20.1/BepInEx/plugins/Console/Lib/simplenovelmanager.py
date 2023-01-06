"""
Simple Novel Manager
v1.2

Changelog:
1.0
- initial release
1.1
- no individual header, integrated in VNGE 9.0
1.2
- UTF-8 support in config and text files
- support "skin" param in config. Example: "skin": "skin_renpy"
"""

from vngameengine import HSNeoOCIFolder
import codecs

def start(game):
    """:type game: vngameengine.VNNeoController"""
    if game.isClassicStudio:
        game.show_blocking_message_time("This is not for Classic Studio. Use NEO")
        return

    # -------- some options we want to init ---------
    game.sceneDir = "simple_novels/" # please, move all your scene files in separate folder in scene folder - to avoid collisions with other vn games
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

    game.set_text_s("Choose one of installed simple novels:")
    game.set_buttons_alt(btns, "compact")

def choose_template_folder_on(game,param):
    """:type game: vngameengine.VNNeoController"""
    #game.show_blocking_message_time(param)
    game.gdata.tplfolder = param

    try:
        mypath = game.get_scene_dir() + "/" + game.sceneDir + "/" + game.gdata.tplfolder
        confstr = game.file_get_content_utf8(mypath+"/_sn_config.txt")
        import ast
        config = ast.literal_eval(confstr)
        game.gdata.sn_config = config
    except Exception, e:
        game.show_blocking_message_time("Error during load _sn_config.txt")
        return

    game.gdata.sn_name = "-No name-"
    if "name" in config:
        game.gdata.sn_name = config["name"]

    game.gdata.sn_desc = ""
    if "description" in config:
        game.gdata.sn_desc = config["description"]

    try:
        if "characters" in config:
            characters = config["characters"]
            for char in characters:
                game.register_char(char[0],char[1],char[2])
    except Exception, e:
        game.show_blocking_message_time("Error during processing characters in Config")
        return

    try:
        if "skin" in config:
            game.skin_set_byname(config["skin"])
        else:
            game.skin_set_byname("skin_renpymini")
    except Exception, e:
        game.show_blocking_message_time("Error during setup Skin in Config")
        return

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



    before_start(game)


def before_start(game):

    game.set_text_s("<size=32>%s</size>\n%s\n"
        "(Includes %s scenes)" % (game.gdata.sn_name, game.gdata.sn_desc, str(len(game.gdata.arfiles))))

    btns = [
        "Start!", next_file_screen,
        "(move to scene)", move_to_scene,
        #"(set expert settings)", adv_par_girl
    ]

    game.set_buttons_alt(btns, "compact")

    titlefile = game.get_scene_dir() + "/" + game.sceneDir + "/" + game.gdata.tplfolder+"/_title.png"
    # set title, if we have one
    import os.path
    if os.path.isfile(titlefile):
        game.scene_set_bg_png(game.gdata.tplfolder+"/_title.png")

def move_to_scene(game):
    game.set_text_s("Choose part (scene file):")
    btns = []
    for i in range(len(game.gdata.arfiles)):
        btns.append((game.gdata.arfiles[i])[:-4])
        btns.append((move_to_scene_index, i))
    game.set_buttons_alt(btns, "compact")

def move_to_scene_index(game,index):
    game.gdata.curfile = index-1
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
    game.set_text_s(".....")

    if HSNeoOCIFolder.find_single_startswith(":vnscenescript:"):
        pass
    else:
        # making standart vnscenescript header
        actions = []
        actions.append(":vnscenescript:v20:50")
        actions.append(":useext:vnframe11")
        actions.append(":a:i:f_stinit")

        for act in actions:
            HSNeoOCIFolder.add(act)



        codefile = (game.gdata.tplfolder+"/"+game.gdata.arfiles[game.gdata.curfile])[:-4]+".txt"
        fullcodefile = game.get_scene_dir() + "/" + game.sceneDir + "/"+codefile

        import os.path
        if os.path.isfile(fullcodefile):
            import vnscenescript
            vnscenescript.dutil_syncwithfile_full_acode(game, (':acode',fullcodefile))

    game.set_timer(0.5, scene_loaded2)

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

    # special case if last scene
    curfile = game.gdata.curfile
    if curfile == len(game.gdata.arfiles)-1:
        next_file_screen(game)
        return



    game.set_text_s("...")
    game.set_buttons_alt([
        "Next scene > ", next_file_screen
    ])

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
    if game.gdata.custom_girl != None: # if we have custom girl, we need more proceed
        load_scene_with_replace(game,param)

    game.load_scene(param)


def sup_load_scene_advancedik(game, path):
    if game.gdata.custom_girl != None: # if we have custom girl, we need more proceed
        load_scene_with_replace(game,path)

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


def sup_tocam(game,param):
    # instant move to camera
    game.to_camera(param)    
    
def sup_tocam_animated(game,param):
    # animated move to camera - 3 seconds, with-fast-slow movement style
    game.anim_to_camera_num(3, param, "fast-slow")
    #game.anim_to_camera_num(3, param, {'style':"linear",'zooming_in_target_camera':6}) # cool camera move with zoom-out - zoom-in

def sup_tocam_showhidefolders(game,param):
    # param - (folder_to_hide, folder_to_show, move_to_camera)
    foldhide, foldshow, cam = param

    if foldhide:
        f1 = HSNeoOCIFolder.find_single(foldhide)
        f1.visible_treenode = False

    if foldshow:
        f2 = HSNeoOCIFolder.find_single(foldshow)
        f2.visible_treenode = True

    if cam:
        game.to_camera(cam)

# -------- customize female ----------
# --------------- normally, you don't need to change them ------------
def cust_female(game):
    run_hire_scene(game)

def run_hire_scene(game):
    game.set_text_s("...")
    game.set_buttons_alt([])

    game.load_scene("_sys/_custfemale.png")

    game.set_timer(0.3, _hire_scene_loaded)

def _hire_scene_loaded(game):
    game.set_text_s(
        "2. Choose main Girl character to place in all Moments \n(use menu Add / Girls)\n"+
        "")
    game.set_buttons_alt([
        "<<", _hire_end
    ])
    game.set_timer(1, _hire_wait)

def _hire_wait(game):
    ofems = game.scene_get_all_females()
    if len(ofems) > 0:
        game.set_timer(0.1, _hire_ready)
        game.set_buttons_alt([])
        ofem = ofems[0]
        """:type ofem: vngameengine.HSNeoOCIChar"""
        game.set_text_s("Wait...")
        ofem.animate(0, 0, 8, 0.0, 1.0)
        ofem.as_actor.move((0, 0, 0))
        ofem.look_eyes_ptn = 1
        ofem.look_neck_ptn = 1
    else:
        game.set_timer(1, _hire_wait)

def _hire_ready(game):
    ofem = game.scene_get_all_females()[0]
    """:type ofem: vngameengine.HSNeoOCIChar"""
    game.anim_to_camera_num(1, 2, "fast-slow")
    text = "This is <b>%s</b>\n" % ofem.text_name

    text += "\nSet as main character?"
    game.set_text_s(text)
    btns = [
        "Set!", _hire_hire,
        "Choose another...", _hire_another,
    ]
    game.set_buttons_alt(btns, "compact")

def _hire_end(game):
    game.clear_timers()
    start(game)

def _hire_hire(game):
    ofem = game.scene_get_all_females()[0]
    """:type ofem: vngameengine.HSNeoOCIChar"""
    game.gdata.custom_girl = ofem.charInfo.chaFile.charaFileName
    game.gdata.custom_girlname = ofem.text_name
    start_story(game)

def _hire_another(game):
    ofem = game.scene_get_all_females()[0]
    """:type ofem: vngameengine.HSNeoOCIChar"""
    ofem.delete()
    game.to_camera(1)
    _hire_scene_loaded(game)


# ----- support functions with customize -------
def load_scene_with_replace(game,param):
    game.set_timer(0.5, on_load_scene_replace)

def on_load_scene_replace(game):
    game.set_timer(1.0, on_load_scene_replace2)

def on_load_scene_replace2(game):
    # calculate set of girls to replace
    ofems = game.scene_get_all_females()
    ar = []
    for ofem in ofems:
        ofem = ofem
        """:type ofem: vngameengine.HSNeoOCIChar"""
        if game.gdata.replace_girl_name != None:
            if ofem.text_name.startswith(game.gdata.replace_girl_name): # here if we process concrete girl name - in English!
                ar.append(ofem)
        else: # here we process ALL girls, no matter what name is
            ar.append(ofem)

    game.repAr = ar

    replaceFunc(game, game.gdata.custom_girl, game.gdata.replace_mode)


# --------- replacing char - with clothes and without -----------
# it's a kind of mess for now :(( but it works with NEO and CharaStudio

def replaceFunc(game,charfilename,style):
    """:type game: vngameengine.VNNeoController"""

    game.repArMax = []
    for ofem in game.repAr:
        ofem = ofem
        """:type ofem: vngameengine.HSNeoOCIChar"""

        if style == "full":
            ofem.objctrl.ChangeChara(charfilename)
        if style == "full_keep_height_reset_anime_option":
            #print "Height0: ", ofem.charInfo.GetShapeBodyValue(0)
            h0 = ofem.charInfo.GetShapeBodyValue(0)
            #print "0", ofem.as_actor.get_anime_option_param()
            optp = ofem.as_actor.get_anime_option_param()
            ofem.objctrl.ChangeChara(charfilename)
            #print "1", ofem.as_actor.get_anime_option_param()
            #print "Height: ", ofem.charInfo.GetShapeBodyValue(0)
            ofem.charInfo.SetShapeBodyValue(0,h0)
            ofem.as_actor.set_anime_option_param(optp)
            #ofem.restart_anime()
            #game.repArMax.append([ofem, coordinateType, memoryStream.ToArray()])
            #print "Height: ", ofem.objctrl.charBody.charCustom.GetShapeBodyValue(1)
            #print "Height: ", ofem.charInfo.GetShapeBodyValue(0)
        if style == "bodyex":
            #ofem.charInfo.chaFile.LoadCharaFile(charfilename)
            #ofem2.charInfo.Reload()
            if game.isStudioNEO:
                ReplaceBodyOnly(game,ofem.objctrl,charfilename)
            if game.isCharaStudio:
                ReplaceBodyOnlyChara(game, ofem.objctrl, charfilename)
            """
            if game.isCharaStudio:
                ofem.charInfo.chaFile.LoadCharaFile(charfilename)
                # ofem2.charInfo.Reload(True,True,True,True)
                # ofem2.charInfo.ChangeClothes(True)
                ofem.charInfo.Reload()
            """
    # in bodyex - call later
    #if game.isStudioNEO:
    if style == "bodyex":
        if game.isStudioNEO:
            game.set_timer(0.2,ReplaceBodyLate)

        if game.isCharaStudio:
            game.set_timer(0.2, ReplaceBodyLateChara)

    # clean up
    game.repAr = None

    #toReplaceAct(game, param)

# --- from HSNeoAddon ----
# // HSStudioNEOAddon.StudioCharaListSortUtil
def ReplaceBodyOnly(game, ociChar, path):
    from System.IO import MemoryStream,BinaryWriter
    chaFile = ociChar.charInfo.chaFile;
    memoryStream = MemoryStream();
    binaryWriter = BinaryWriter(memoryStream);
    chaFile.clothesInfo.Save(binaryWriter);
    binaryWriter.Close();
    memoryStream.Close();
    coordinateType = ociChar.charInfo.statusInfo.coordinateType;
    #ChangeChara(ociChar);
    ociChar.ChangeChara(path)

    game.repArMax.append([ociChar.charInfo,coordinateType,memoryStream.ToArray()])

def ReplaceBodyLate(game):
    from System.IO import MemoryStream, BinaryWriter

    for lat in game.repArMax:
        charInfo = lat[0]
        coordinateType = lat[1]
        clothesInfoData = lat[2]

        charInfo.chaFile.clothesInfo.Load(MemoryStream(clothesInfoData), True);
        charInfo.chaFile.SetCoordinateInfo(coordinateType);
        charInfo.Reload(False, True, True);
        if (charInfo.Sex == 1): # only female
            charInfo.UpdateBustSoftnessAndGravity();

    # cleanup
    game.repArMax = None

def ReplaceBodyOnlyChara(game, ociChar, path):
    from System.IO import MemoryStream, BinaryWriter
    """:type ociChar: OCIChar"""
    #bytes = ociChar.charInfo.chaFile.GetCoordinateBytes()
    bytes = ociChar.charInfo.nowCoordinate.SaveBytes()

    """
    chaFile = ociChar.charInfo.chaFile;
    memoryStream = MemoryStream();
    binaryWriter = BinaryWriter(memoryStream);
    chaFile.clothesInfo.Save(binaryWriter);
    binaryWriter.Close();
    memoryStream.Close();
    coordinateType = ociChar.charInfo.statusInfo.coordinateType;
    # ChangeChara(ociChar);
    """
    ociChar.ChangeChara(path)
    #print bytes
    game.repArMax.append([ociChar, bytes])

    #base.StartCoroutine(ChangeClothesCo(ociChar.charInfo, coordinateType, memoryStream.ToArray()));
def ReplaceBodyLateChara(game):
    from System.IO import MemoryStream, BinaryWriter
    import ChaFileDefine

    for lat in game.repArMax:
        ociChar = lat[0]
        """:type ociChar: OCIChar"""
        coordBytes = lat[1]
        #print coordBytes
        #clothesInfoData = lat[2]
        try:
            #ociChar.charInfo.chaFile.SetCoordinateBytes(coordBytes, ChaFileDefine.ChaFileCoordinateVersion)
            ociChar.charInfo.nowCoordinate.LoadBytes(coordBytes, ChaFileDefine.ChaFileCoordinateVersion)
            #ociChar.charInfo.Reload(False, True, True);
            ociChar.charInfo.Reload();

            """
            if (ociChar.charInfo.Sex == 1): # only female
                ociChar.charInfo.UpdateBustSoftnessAndGravity();
            """
        except Exception, e:
            print "Exception in ReplaceBodyLateChara, ", str(e)
    # cleanup
    game.repArMax = None
