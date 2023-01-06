#vngame;all;Utilities/Scene utils
"""
Scene Utils by Keitaro (and countd360)
v3.3

Features:
- moving/rotating/scaling selected objects using button interface
- mass replacing characters with options:
-- replace all / selected / sharing one name
-- choose from predefined set (in sceneutils_favchars.txt file) / from normal menu
-- replace all / body only (keep clothes) (in NEO and CharaStudio)
- utils: enable/disable eyes blinking for ALL chars on scene
- Sync-H - auto-adjusting H-animation for female and male like in main game
(In main game H-animations are adjusted to suit the concrete female with height and breast size.
This tool does it for you in Studio)

2.5
- added "Items: mass change FK"
2.6
- fix to support subfolders in Female folder
2.7
- add something like BodySlidels lite
2.8
- upd for NeoV2
3.0 (countd360)
- add "Body Slider" and "face Slider" tools 
- add "VNActor setting" tool
3.1
- added "Copy/paste clothes" / "Paste closes without accessories" for KK
3.1.1 (countd360)
- seperate "Body Slider" and "face Slider" 's clipboard 
3.2 (countd360)
- add "VNText Editor" for every game engine
3.2.1 (Keitaro)
- NeoV2: added English translation for Face sliders (by ccyu)
3.3
- NeoV2: save/load DHH function
"""

from vngameengine import HSNeoOCIFolder, HSNeoOCI, import_or_reload
from vnactor import *
from UnityEngine import Vector3, Vector2, Color

#import_or_reload("vnactor")

def start(game):
    #game.gdata.isSceneUtilsRun = True
    """:type game: vngameengine.VNNeoController"""

    if game.isClassicStudio:
        game.show_blocking_message_time("Sorry, this is only for NEO engines")
        return

    game.set_text_s("<b>Scene Utils 3.3</b> by Keitaro. What to do?")
    btns = [

        "Manipulate selected chars/it", start_man,
        "Replace chars", start_replace,
        #"Make screenshot", start_screenshot,
        "Utils", start_utils,
        "Sync-H (adjust H animation)", sync_h,
        "Items: mass change FK", start_man_fk,
        "Change chara body", start_BodySliders,
        "Body Slider", start_body_sliders,
        "Face Slider", start_face_sliders,
        "Copy/paste clothes", start_clothes,
        "VNActor Setting", start_vnactor_setting,
        "VNText Editor", start_vntext_editor,
    ]

    if(game.isNEOV2):
        btns += [
            "AI: Save DHH to scene", ai_save_dhh,
            #"AI: Load DHH from scene", ai_load_dhh,
        ]


    game.set_buttons_alt(btns, "compact")

def start_replace(game):
    """:type game: vngameengine.VNNeoController"""
    #start_menu(game, "asuna.png")
    game.set_text_s("What to do?\nReplace...")
    btns = [
        "Selected chars", m11,
        "All female chars", m12,
        "All chars with the same name as selected", m13,

    ]
    game.set_buttons_alt(btns)

# --- first menu ---

def m11(game):
    """:type game: vngameengine.VNNeoController"""
    mtreeman = game.studio.treeNodeCtrl
    ar = []
    for node in mtreeman.selectNodes:
        ar.append(HSNeoOCI.create_from_treenode(node))
    game.repAr = ar
    toSelectChar(game)

def m12(game):
    game.repAr = game.scene_get_all_females()
    toSelectChar(game)

def m13(game):
    """:type game: vngameengine.VNNeoController"""
    ofems = game.scene_get_all_females()
    mtreeman = game.studio.treeNodeCtrl
    name = mtreeman.selectNode.textName

    ar = []
    for ofem in ofems:
        if ofem.text_name == name:
            ar.append(ofem)

    game.repAr = ar


    toSelectChar(game)


# --- second menu ---

def toSelectChar(game):
    """:type game: vngameengine.VNNeoController"""
    game.set_text_s("Selected objects: %s\nReplace to..."%(str(len(game.repAr))))
    btns = []

    import sys, os.path
    fname = (os.path.splitext(__file__)[0] + '_favchars.txt')

    import codecs

    try:
        with codecs.open(fname, encoding="utf-8") as f:
            content = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        content = [x.strip() for x in content]

        for x in content:
            if isinstance(x,str):
                ar = x.split(";")
                btns += [ar[0],(m2x, ar[1])]

    except Exception, e:
        game.show_blocking_message_time("Can't find or read file replacechar.txt")

    btns += ["<< Add arbitrary char >>", m2arb]

    #btns += ["Gagency", (m2x, "gagency.png")]
    #btns += ["Student", (m2x, "student.png")]

    game.set_buttons_alt(btns, "compact")


def m2x(game,param):
    """:type game: vngameengine.VNNeoController"""
    game.repFile = param
    toSelectReplaceMode(game)

def m2arb(game):
    game.set_text_s("Please, add your char to scene and press 'I added char'\n"+
                    "Latest char filename will be saved to replace characters and also latest char will be removed")
    btns = [
        "<< Return ", toSelectChar,
        "I added char >>", m2arb2,
    ]
    game.set_buttons_alt(btns)

def m2arb2(game):
    """:type game: vngameengine.VNNeoController"""
    ofems = game.scene_get_all_females()
    ofem = ofems[len(ofems)-1]
    """:type ofem: vngameengine.HSNeoOCIChar"""
    fname = ofem.charInfo.chaFile.charaFileName
    game.repFile = fname
    ofem.delete()
    game.show_blocking_message_time("Char scanned and deleted!")
    toSelectReplaceMode(game)


# --- third menu ----

def toSelectReplaceMode(game):
    """:type game: vngameengine.VNNeoController"""
    game.set_text_s("Selected objects: %s\nChoose replace mode:" % (str(len(game.repAr))))
    btns = []

    btns += ["Full", (m3x, "full")]
    if not game.isPlayHomeStudio:
        btns += ["Body only (experimental)", (m3x, "bodyex")]
    game.set_buttons_alt(btns)

def m3x(game,param):
    replaceFunc(game,game.repFile,param)
    game.show_blocking_message_time("Done!")
    start(game)

def replaceFunc(game,charfilename,style):
    """:type game: vngameengine.VNNeoController"""
    charfilename = "UserData/chara/female/"+charfilename

    game.repArMax = []
    for ofem in game.repAr:
        ofem = ofem
        """:type ofem: vngameengine.HSNeoOCIChar"""

        if style == "full":
            ofem.objctrl.ChangeChara(charfilename)
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
            game.set_timer(0.6, ReplaceBodyLateChara)

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



def toReplaceAct(game,charfilename):
    """:type game: vngameengine.VNNeoController"""
    try:
        females = game.scene_get_all_females()
        for ofem in females:
            """:type ofem: vngameengine.HSNeoOCIChar"""
            ofem.objctrl.ChangeChara(charfilename)
        print "Done!"
        game.show_blocking_message_time("Female replaced %s times!"%len(females))
    except Exception, e:
        print("Error: " + str(e))

# -------- old functions ----------

def toReplace(game):
    ofem = game.scene_get_all_females()[0]; """:type ofem: vngameengine.HSNeoOCIChar"""
    ofem2 = game.scene_get_all_females()[1]; """:type ofem2: vngameengine.HSNeoOCIChar"""

    file1 = ofem.charInfo.chaFile.charaFileName
    print file1
    #ofem2.charInfo.chaFile.LoadCharaFile(file1)
    ofem2.charInfo.chaFile.LoadCharaFile(file1)
    #ofem2.charInfo.Reload(True,True,True,True)
    #ofem2.charInfo.ChangeClothes(True)
    ofem2.charInfo.Reload()
    print "Done!"


def toReplace3(game):
    ofem = game.scene_get_all_females()[0]; """:type ofem: vngameengine.HSNeoOCIChar"""
    ofem2 = game.scene_get_all_females()[1]; """:type ofem2: vngameengine.HSNeoOCIChar"""

    file1 = ofem.charInfo.chaFile.charaFileName
    print file1
    #ofem2.charInfo.chaFile.LoadCharaFile(file1)
    try:
        from System import Byte
        ofem2.charInfo.chaFile.LoadCharaFile(file1, Byte.MaxValue, True, True)
        # ofem2.charInfo.Reload(True,True,True,True)
        # ofem2.charInfo.ChangeClothes(True)
        ofem2.charInfo.Reload(True, True, True, True)
        print "Done!"
    except Exception, e:
        print("Error: " + str(e))

# ----- screenshot ----------
def start_screenshot(game):
    game.set_text_s("What to do?")
    btns = [
        "Make screenshot (internal func, with Alpha) ", start_screenshot_internal,
        "Make screenshot (using F11)", start_screenshot_f11,
    ]
    game.set_buttons_alt(btns)

def start_screenshot_f11(game):
    """:type game: vngameengine.VNNeoController"""
    from WindowsInput import InputSimulator
    from WindowsInput import VirtualKeyCode
    InputSimulator.SimulateKeyPress(VirtualKeyCode.F11)

    game.show_blocking_message_time("Screenshot done!")
    start(game)


def start_screenshot_internal(game):
    """:type game: vngameengine.VNNeoController"""
    capture_noblock(game)
    game.show_blocking_message_time("Screenshot done!")
    start(game)
    
def capture_noblock(game, _path='', _alpha=True, autofit=True):
    """:type game: vngameengine.VNNeoController"""
    import System
    import Manager
    from System import *
    from System.IO import *
    from UnityEngine import *
    from UnityEngine import Object as Object
    from UnityEngine import Time as Time
    width = Screen.width
    height = Screen.height
    tex = Texture2D(width, height, TextureFormat.RGB24 if not _alpha else TextureFormat.ARGB32, False)
    tex2 = Texture2D(width, height, TextureFormat.RGB24 if not _alpha else TextureFormat.ARGB32, False)
    if QualitySettings.antiAliasing != 0:
        rt = RenderTexture.GetTemporary(width, height, 0x18 if not _alpha else 0x20, RenderTextureFormat.Default, RenderTextureReadWrite.Default, QualitySettings.antiAliasing)
        rt2 = RenderTexture.GetTemporary(width, height, 0x18 if not _alpha else 0x20, RenderTextureFormat.Default, RenderTextureReadWrite.Default, QualitySettings.antiAliasing)
    else:
        rt = RenderTexture.GetTemporary(width, height, 0x18 if not _alpha else 0x20)
        rt2 = RenderTexture.GetTemporary(width, height, 0x18 if not _alpha else 0x20)
    #RenderCam = Camera.main
    #RenderCam = Manager.Studio.Instance.MainCamera
    RenderCam = game.studio.cameraCtrl.mainCmaera
    backRenderTexture = RenderCam.targetTexture
    backRect = RenderCam.rect
    oldBackground = RenderCam.backgroundColor
    oldFlags = RenderCam.clearFlags
    RenderCam.backgroundColor = Color(Single(1), Single(1), Single(1), Single(1))
    RenderCam.clearFlags = CameraClearFlags.Color
    RenderCam.targetTexture = rt
    RenderCam.Render()
    RenderCam.targetTexture = backRenderTexture
    RenderCam.rect = backRect
    RenderTexture.active = rt
    tex.ReadPixels(Rect(Single(0), Single(0), width, height), 0, 0)
    tex.Apply()
    RenderTexture.active = None
    RenderCam.backgroundColor = Color(Single(0), Single(0), Single(0), Single(1))
    RenderCam.clearFlags = CameraClearFlags.Color
    RenderCam.targetTexture = rt2
    RenderCam.Render()
    RenderCam.targetTexture = backRenderTexture
    RenderCam.rect = backRect
    RenderTexture.active = rt2
    tex2.ReadPixels(Rect(Single(0), Single(0), width, height), 0, 0)
    tex2.Apply()
    RenderTexture.active = None
    RenderCam.backgroundColor = oldBackground
    RenderCam.clearFlags = oldFlags
    RenderTexture.ReleaseTemporary(rt)
    RenderTexture.ReleaseTemporary(rt2)
    
    cols1 = tex.GetPixels()
    cols2 = tex2.GetPixels()
    x1, x2 = width, 0
    y1, y2 = height, 0
    
    for i in xrange(0,cols1.Length-1):
        c1 = cols1[i]
        c2 = cols2[i]
        a = 1.0
        if c1 != c2:
            a = Single(1) - Math.Max(Math.Abs(c1.r - c2.r), Math.Max(Math.Abs(c1.g - c2.g), Math.Abs(c1.b - c2.b)))
            cols1[i] = Color(c1.r, c1.g, c1.b, a)
        if autofit and a > 0.05:
            y = i // width
            x = i - y*width
            if x < x1: x1 = x
            if x > x2: x2 = x
            if y < y1: y1 = y
            if y > y2: y2 = y
    if autofit:
        def irnd(x):
            return x + x%2
        # add padding then truncate
        padding = 4
        x1,y1 = max(0, irnd(x1-padding)), max(0, irnd(y1-padding))
        x2,y2 = min(width, irnd(x2+padding)), min(height, irnd(y2+padding))
        Object.Destroy(tex)
        w,h = x2-x1, y2-y1
        tex = Texture2D(x2-x1, y2-y1, TextureFormat.ARGB32, False)
        cols = tex.GetPixels()
        for i in range(x1, x2):
            for j in range(y1, y2):
                cols[(j-y1)*w+(i-x1)] = cols1[j*width+i]
        tex.SetPixels(cols)
        tex.Apply()
    else:
        tex.SetPixels(cols1)
        tex.Apply()
    bytes = tex.EncodeToPNG()
    Object.Destroy(tex)
    tex = None
    if str.Empty == _path:
        import UserData, datetime
        _path = UserData.Create("cap")
        fileName = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        _path = Path.GetFullPath(Path.Combine(_path, fileName + ".png"))
        #Console.WriteLine("Capture: " + _path)
    File.WriteAllBytes(_path, bytes)
    return True

# --------- manipulate selected char -----------

def start_man(game):
    """:type game: vngameengine.VNNeoController"""
    game.set_text_s("What to do?\nManipulate selected chars and items...")
    btns = [
        "Move", manM,
        "Rotate", manR,
        "Scale", manS,
        "<<", start,
    ]
    game.set_buttons_alt(btns)

def manM(game):
    """:type game: vngameengine.VNNeoController"""
    #start_menu(game, "asuna.png")
    game.set_text_s("What to do?\nMove...")
    addv = 0.02
    btns = [
        "-X", (manMutil,(-addv,0,0)),
        "+X", (manMutil, (addv, 0, 0)),
        "-Z", (manMutil, (0, 0, -addv)),
        "+Z", (manMutil, (0, 0, addv)),
        "-Y (Vert)", (manMutil, (0, -addv, 0)),
        "+Y (Vert)", (manMutil, (0, addv, 0)),
        "<<", start,
    ]
    game.set_buttons_alt(btns, "compact")

def manR(game):
    """:type game: vngameengine.VNNeoController"""
    #start_menu(game, "asuna.png")
    game.set_text_s("What to do?\nRotate...")
    addv = 0.75
    btns = [
        "-X", (manRutil,(-addv,0,0)),
        "+X", (manRutil, (addv, 0, 0)),
        "-Z", (manRutil, (0, 0, -addv)),
        "+Z", (manRutil, (0, 0, addv)),
        "-Y", (manRutil, (0, -addv*2, 0)),
        "+Y", (manRutil, (0, addv*2, 0)),
        "<<", start,
    ]
    game.set_buttons_alt(btns, "compact")

def manS(game):
    """:type game: vngameengine.VNNeoController"""
    #start_menu(game, "asuna.png")
    game.set_text_s("What to do?\nScale...")
    addv = 0.02
    btns = [
        "-X", (manSutil,(-addv,0,0)),
        "+X", (manSutil, (addv, 0, 0)),
        "-Z", (manSutil, (0, 0, -addv)),
        "+Z", (manSutil, (0, 0, addv)),
        "-Y", (manSutil, (0, -addv, 0)),
        "+Y", (manSutil, (0, addv, 0)),
        "..", None,
        "-All", (manSutil, (-addv, -addv, -addv)),
        "+All", (manSutil, (addv, addv, addv)),
        "<< start", start,
    ]
    game.set_buttons_alt(btns, "compact")

def get_selected_actor(game):
    mtreeman = game.studio.treeNodeCtrl
    if mtreeman.selectNode != None:
        ochar = HSNeoOCI.create_from_treenode(mtreeman.selectNode)
        if ochar != None:
            #actor = Actor(ochar.objctrl)
            actor = ochar.as_actor
            return actor
    return None

def get_selected_objs(game):
    mtreeman = game.studio.treeNodeCtrl
    ar = []
    for node in mtreeman.selectNodes:
        ochar = HSNeoOCI.create_from_treenode(node)
        #ar.append(HSNeoOCI.create_from_treenode(node))
        if isinstance(ochar,HSNeoOCIChar):
            ar.append(Actor(ochar.objctrl))
        else:
            ar.append(ochar.objctrl)

    return ar

def get_selected_objs2(game):
    mtreeman = game.studio.treeNodeCtrl
    ar = []
    for node in mtreeman.selectNodes:
        ochar = HSNeoOCI.create_from_treenode(node)
        #ar.append(HSNeoOCI.create_from_treenode(node))
        if isinstance(ochar,HSNeoOCIChar):
            ar.append(ochar.as_actor)
        else:
            ar.append(ochar.as_prop)

    return ar

def manMutil(game,param):
    objs = get_selected_objs(game)
    for obj in objs:
        if isinstance(obj, Actor):
            char_move(obj,param)
        else:
            item_move(obj,param)

def manRutil(game,param):
    objs = get_selected_objs(game)
    for obj in objs:
        if isinstance(obj, Actor):
            char_turn(obj,param)
        else:
            item_rotate(obj,param)

def manSutil(game,param):
    objs = get_selected_objs(game)
    for obj in objs:
        if isinstance(obj, Actor):
            char_scale(obj,param)
        else:
            item_scale(obj,param)

# manipulating functions from vnframe by @countd360

def char_move(char, param):
    # param = (pos_delta_x, pos_delta_y, pos_delta_z)
    cp = char.pos
    ncp = Vector3(cp.x + param[0], cp.y + param[1], cp.z + param[2])
    char.move(pos=ncp)


def char_turn(char, param):
    # param = rot_delta_y
    rt = char.rot
    nrt = Vector3(rt.x + param[0], rt.y  + param[1], rt.z + param[2])
    char.move(rot=nrt)

def char_scale(char, param):
    """:type char: vnactor.Actor"""
    # param = rot_delta_y
    rt = char.scale
    nrt = Vector3(rt.x + param[0], rt.y  + param[1], rt.z + param[2])
    char.move(scale=nrt)


def item_move(item, param):
    # param = (pos_delta_x, pos_delta_y, pos_delta_z)
    cp = item.objectInfo.changeAmount.pos
    ncp = Vector3(cp.x + param[0], cp.y + param[1], cp.z + param[2])
    item.objectInfo.changeAmount.pos = ncp

def item_move_to(item, param):
    # param = (pos_x, pos_y, pos_z)
    ncp = Vector3(param[0], param[1], param[2])
    item.objectInfo.changeAmount.pos = ncp

def item_rotate(item, param):
    # param = (rot_delta_x, rot_delta_y, rot_delta_z)
    rt = item.objectInfo.changeAmount.rot
    nrt = Vector3(rt.x + param[0], rt.y + param[1], rt.z + param[2])
    item.objectInfo.changeAmount.rot = nrt

def item_rotate_to(item, param):
    # param = (rot_x, rot_y, rot_z)
    nrt = Vector3(param[0], param[1], param[2])
    item.objectInfo.changeAmount.rot = nrt

def item_scale(item, param):
    # param = (scale_x, scale_y, scale_z) or scale
    from Studio import OCIItem
    if isinstance(item, OCIItem):
        # for item only, folder can not set scale
        rt = item.itemInfo.changeAmount.scale
        nrt = Vector3(rt.x + param[0], rt.y + param[1], rt.z + param[2])
        item.itemInfo.changeAmount.scale = nrt

def item_scale_to(item, param):
    # param = (scale_x, scale_y, scale_z) or scale
    from Studio import OCIItem
    if isinstance(item, OCIItem):
        # for item only, folder can not set scale
        if isinstance(param, tuple):
            nsl = Vector3(param[0], param[1], param[2])
        else:
            nsl = Vector3(param, param, param)
        item.itemInfo.changeAmount.scale = nsl

# ---------- utils -----------
from vngameengine import *

def start_utils(game):
    """:type game: vngameengine.VNNeoController"""
    game.set_text_s("What to do?\nUtils...")
    btns = [
        #"Add to crotch", uAddCrch,
        "All charas: eye blink ON", (toggle_all_eyes_blink,1),
        "All charas: eye blink OFF", (toggle_all_eyes_blink, 0),
        "<<", start,
    ]
    game.set_buttons_alt(btns)

def toggle_all_eyes_blink(game,param):
    """:type game: vngameengine.VNNeoController"""
    charas = game.scene_get_all_females()
    charas += game.scene_get_all_males()
    for chara in charas:
        chara = chara
        """:type chara: vngameengine.HSNeoOCIChar"""
        chara.as_actor.set_eyes_blink(param)

    game.show_blocking_message_time("Eyes blink changed!")

# ------- sync-h ----------
def sync_h(game):
    """:type game: vngameengine.VNNeoController"""
    objs = get_selected_objs(game)
    if len(objs) != 2:
        game.show_blocking_message_time("Please, select female and male char to sync their H animation.")
        return

    try:
        fem = objs[0]
        if isinstance(fem, Actor):
            man = objs[1]
            if isinstance(man, Actor):
                game.sync_h(fem,man)
                fem.restart_anime()
                man.restart_anime()
                game.show_blocking_message_time("H-animation synchronized!")
                return

    except:
        pass

    game.show_blocking_message_time("Please, select female and male char to sync their H animation.\nFemale must be FIRST!")
    return


# ------- adding items -----------
def uAddCrch(game):
    """:type game: vngameengine.VNNeoController"""
    char = HSNeoOCI.create_from_selected()
    if isinstance(char,HSNeoOCIChar):
        game.targPos = char.treeNodeObject.child[1].child[2]
    else:
        game.show_blocking_message_time("No char selected!")
        return

    btns = [
        "Vibe 1", (uAddCrchVibe, 321),
        "Vibe 2", (uAddCrchVibe, 580),
        "Vibe 3", (uAddCrchVibe, 322),
        "Yellow Liquid", uAddCrchLiq,
        "<<", start,
    ]
    game.set_buttons_alt(btns, "compact")


def uAddCrchVibe(game, no):
    item = HSNeoOCIItem.add_item(no)
    item.set_parent_treenodeobject(game.targPos)
    item.set_move((0, -0.308, 0.193))
    item.set_rotate((310, 0, 0))
    game.show_blocking_message_time("Done!")

def uAddCrchLiq(game):
    item = HSNeoOCIItem.add_item(344)
    item.set_parent_treenodeobject(game.targPos)
    item.set_move((0, -0.158, 0.05))
    item.set_rotate((10, 0, 0))
    game.show_blocking_message_time("Done!")

# ------- add FK ---------
def start_man_fk(game):
    """:type game: vngameengine.VNNeoController"""
    #start_menu(game, "asuna.png")
    game.set_text_s("What to do?\nAdd rotation...")
    addv = 0.04
    btns = [
        "-X", (manRFKutil,(-addv,0,0)),
        "+X", (manRFKutil, (addv, 0, 0)),
        "-Z", (manRFKutil, (0, 0, -addv)),
        "+Z", (manRFKutil, (0, 0, addv)),
        "-Y", (manRFKutil, (0, -addv, 0)),
        "+Y", (manRFKutil, (0, addv, 0)),
        "<<", start,
    ]
    game.set_buttons_alt(btns, "compact")

def manRFKutil(game,param):
    objs = get_selected_objs2(game)
    for obj in objs:
        if isinstance(obj, Actor):
            #char_turn(obj,param)
            pass
        elif isinstance(obj, Prop):
            #obj
            try:
                fklist = obj.export_fk_bone_info()
                fknew = []
                for fk in fklist:
                    fknew.append(Vector3(fk[0]+param[0],fk[1]+param[1],fk[2]+param[2]))

                obj.import_fk_bone_info(fknew)
            except:
                pass
        else:
            pass

# ------ body sliders ----------
def bodysliders_get_localized(game):
    arrs = []

    if game.isPlayHomeStudio:
        arrs = [    "Height",
                    "Tits",
                    ]

    if game.isNEOV2:
        arrs = [    "Height",
                    "BustSize",
                    "BustY",
                    "BustRotX",
                    "BustX",
                    "BustRotY",
                    "BustSharp",
                    "AreolaBulge",
                    "NipWeight",
                    "HeadSize",
                    "NeckW",
                    "NeckZ",
                    "BodyShoulderW",
                    "BodyShoulderZ",
                    "BodyUpW",
                    "BodyUpZ",
                    "BodyLowW",
                    "BodyLowZ",
                    "WaistY",
                    "WaistUpW",
                    "WaistUpZ",
                    "WaistLowW",
                    "WaistLowZ",
                    "Hip",
                    "HipRotX",
                    "ThighUp",
                    "ThighLow",
                    "Calf",
                    "Ankle",
                    "Shoulder",
                    "ArmUp",
                    "ArmLow",
                    "NipStand"
                    ]

    if game.isStudioNEO:
        arrs = [    "Height",
                    "Tits",
                    "Tits Space",
                    "Tits Angle",
                    "Tits Length",
                    "Tits Angle2",
                    "Nips Length",
                    "Areolas",
                    "Nips Size",
                    "Head",
                    "Neck X",
                    "Neck Z",
                    "Thorax X",
                    "Thorax Z",
                    "Chest X",
                    "Chest Z",
                    "Waist X",
                    "Waist Z",
                    "Waist Y",
                    "Pelvis X",
                    "Pelvis Z",
                    "Hips X",
                    "Hips Z",
                    "Ass",
                    "Ass Angle",
                    "Thighs",
                    "Legs",
                    "Calves",
                    "Ankles",
                    "Shoulders",
                    "Arms Up",
                    "Arms Low"]

    if game.isCharaStudio:
        arrs = ["Height",
                "Head size",
                "Neck width",
                "Neck thickness",
                "Breast",
                "Breast Vertical pos",
                "Breast spacing",
                "Breast Horizontal pos",
                "Breast Vertical angle",
                "Breast depth",
                "Breast roundness",
                "Areola depth",
                "Nipple thickness",
                "Nipple depth",
                "Shoulder width",
                "Shoulder thickness",
                "Upper torso width",
                "Upper torso thickness",
                "Lower torso width",
                "Lower torso thickness",
                "Waist position",
                "Belly thickness",
                "Waist width",
                "Waist thickness",
                "Hip width",
                "Hip thickness",
                "Butt size",
                "Butt angle",
                "Upper thigh width",
                "Upper thigh thickness",]

    return arrs

def facesliders_get_localized(game):
    arrs = []

    if game.isPlayHomeStudio:
        arrs = []

    if game.isNEOV2:
        arrs = ["Face Width",
                "Upper Face Depth",
                "Upper Face Height",
                "Lower Face Depth",
                "Lower Face Width",
                "Jaw Width",
                "Jaw Length",
                "Jaw Depth",
                "Jaw Angle",
                "Lower Jaw Height",
                "Chin Width",
                "Chin Length",
                "Chin Depth",
                "Lower Cheek Height",
                "Lower Cheek Depth",
                "Lower Cheek Width",
                "Upper Cheek Height",
                "Upper Cheek Depth",
                "Upper Cheek Height",
                "Eye Height",
                "Eye Distance",
                "Eye Depth",
                "Eye Width",
                "Eye Length",]

    if game.isStudioNEO:
        arrs = []

    if game.isCharaStudio:
        arrs = []

    return arrs

def start_BodySliders(game):
    """:type game: vngameengine.VNNeoController"""

    arrs = bodysliders_get_localized(game)

    btns = []

    for i in range(len(arrs)):
        btns += [
            arrs[i]+" +", (act_bodysliders, (i,0.03)),
            arrs[i] + " -", (act_bodysliders, (i,-0.03)),
        ]
        if ((i+1) % 3) == 0:
            btns += [
                "(to start)", start
            ]

    btns += [
        "(to start)", start
    ]

    game.set_text_s("Select char and do something:")
    game.set_buttons_alt(btns,"compact")

def act_bodysliders(game,param):

    """:type game: vngameengine.VNNeoController"""
    actor = get_selected_actor(game)

    if actor == None:
        game.show_blocking_message_time("No selected char")
        return

    p1,p2 = param
    #for actor in sel:

    if game.isStudioNEO:
        bparam = actor.objctrl.charBody.charCustom.GetShapeBodyValue(p1)
        actor.objctrl.charBody.charCustom.SetShapeBodyValue(p1, bparam + p2)

    if game.isCharaStudio:
        bparam = actor.charInfo.GetShapeBodyValue(p1)
        actor.charInfo.SetShapeBodyValue(p1, bparam + p2)
    
    if game.isPlayHomeStudio:
        bparam = actor.charInfo.GetShapeBodyValue(p1)
        actor.charInfo.human.body.SetShape(p1,bparam + p2)

    if game.isNEOV2:
        bparam = actor.charInfo.GetShapeBodyValue(p1)
        actor.charInfo.SetShapeBodyValue(p1, bparam + p2)

def start_body_sliders(game):
    game.set_text_s("")
    game.scenedata.body_slider_target = "body"
    game.scenedata.body_slider_scroll_pos = Vector2.zero
    game.set_buttons_alt([],("function", start_body_sliders_gui))

def start_face_sliders(game):
    game.set_text_s("")
    game.scenedata.body_slider_target = "face"
    game.scenedata.body_slider_scroll_pos = Vector2.zero
    game.set_buttons_alt([],("function", start_body_sliders_gui))

def start_body_sliders_gui(game, info):
    from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode

    sd = game.scenedata
    wwidth = game.windowRect.width - 20
    wheight = game.windowRect.height - 150
    sels = get_selected_objs2(game)
    actor = None if len(sels) != 1 or not isinstance(sels[0], Actor) else sels[0]

    if actor == None:
        GUILayout.Label("Select a charactor to adjust %s"%sd.body_slider_target)
    else:
        if sd.body_slider_target == "body":
            bnames = actor.get_body_shape_names()
            get_values_func = actor.get_body_shapes_all
            set_value_func = actor.set_body_shape
            set_value_all_func = actor.set_body_shapes_all
            if is_ini_value_true("TryLocalizedBodyFaceSliders"):
                loc = bodysliders_get_localized(game)
                bnamesnew = []
                for i in range(len(bnames)):
                    bnamesnew.append(bnames[i])
                    if i < len(loc):
                        bnamesnew[i] = loc[i]
                bnames = bnamesnew
        else:
            bnames = actor.get_face_shape_names()
            get_values_func = actor.get_face_shapes_all
            set_value_func = actor.set_face_shape
            set_value_all_func = actor.set_face_shapes_all
            if is_ini_value_true("TryLocalizedBodyFaceSliders"):
                loc = facesliders_get_localized(game)
                bnamesnew = []
                for i in range(len(bnames)):
                    bnamesnew.append(bnames[i])
                    if i < len(loc):
                        bnamesnew[i] = loc[i]
                bnames = bnamesnew

        #bnames = get_names_func()
        bvalues = [round(i * 100) for i in get_values_func()]
        GUILayout.Label("Selected charactor: %s"%(actor.text_name))
        sd.body_slider_scroll_pos = GUILayout.BeginScrollView(sd.body_slider_scroll_pos, GUILayout.Height(wheight), GUILayout.Width(wwidth))
        for i in range(len(bvalues)):
            GUILayout.BeginHorizontal()
            GUILayout.Label(bnames[i], GUILayout.Width(100))
            nvalue = bvalues[i]
            ntxt = GUILayout.TextField(str(int(bvalues[i])), GUILayout.Width(40))
            if ntxt != str(bvalues[i]):
                try:
                    nvalue = int(ntxt)
                except:
                    pass
            if GUILayout.Button("-10", GUILayout.Width(40)):
                nvalue = nvalue - 10
            if GUILayout.Button("-1", GUILayout.Width(30)):
                nvalue = nvalue - 1
            nsld = GUILayout.HorizontalSlider(bvalues[i], -100, 200, GUILayout.Width(wwidth - 100 - 40 - 140 - 50))
            if nsld != bvalues[i]:
                nvalue = nsld
            if GUILayout.Button("+1", GUILayout.Width(30)):
                nvalue = nvalue + 1
            if GUILayout.Button("+10", GUILayout.Width(40)):
                nvalue = nvalue + 10
            if nvalue != bvalues[i]:
                if nvalue > 200: nvalue = 200
                if nvalue < -100: nvalue = -100
                #print "set %s = %d(%f)"%(bnames[i], nvalue, float(nvalue)/100)
                set_value_func(i, float(nvalue) / 100)
            GUILayout.EndHorizontal()
        GUILayout.EndScrollView()
    
    GUILayout.FlexibleSpace()
    GUILayout.BeginHorizontal()
    if GUILayout.Button("Back", GUILayout.Width(50)):
        start(game)
    if actor and GUILayout.Button("Copy %s's %s"%(actor.text_name, sd.body_slider_target), GUILayout.Width(150)):
        if sd.body_slider_target == "body":
            sd.body_slider_copy_name = actor.text_name
            sd.body_slider_copy_data = get_values_func()
        else:
            sd.face_slider_copy_name = actor.text_name
            sd.face_slider_copy_data = get_values_func()
    if actor and sd.body_slider_target == "body" and hasattr(sd, "body_slider_copy_data") and GUILayout.Button("Paste %s's %s to %s"%(sd.body_slider_copy_name, sd.body_slider_target, actor.text_name), GUILayout.Width(wwidth - 200 - 20)):
        set_value_all_func(sd.body_slider_copy_data)
    if actor and sd.body_slider_target == "face" and hasattr(sd, "face_slider_copy_data") and GUILayout.Button("Paste %s's %s to %s"%(sd.face_slider_copy_name, sd.body_slider_target, actor.text_name), GUILayout.Width(wwidth - 200 - 20)):
        set_value_all_func(sd.face_slider_copy_data)
    
    GUILayout.EndHorizontal()

def start_vnactor_setting(game):
    game.set_text_s("")
    game.set_buttons_alt([],("function", start_vnactor_setting_gui))

def start_vnactor_setting_gui(game, info):
    from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
    from vnactor import load_ini_file, get_ini_options, is_ini_value_true, set_ini_value, get_ini_exportOptionDesp

    sd = game.scenedata
    wwidth = game.windowRect.width - 20
    wheight = game.windowRect.height - 150

    # option list
    GUILayout.Label("Check the extend data you want to export with VNActor:")
    if not hasattr(sd, "vnactorSettingScrollPos"):
        sd.vnactorSettingScrollPos = Vector2.zero
    sd.vnactorSettingScrollPos = GUILayout.BeginScrollView(sd.vnactorSettingScrollPos, GUILayout.Height(wheight), GUILayout.Width(wwidth))
    for optname in get_ini_options():
        optdesp = get_ini_exportOptionDesp(optname)
        if optdesp == None:
            optdesp = "<color=#00ff00>" + optname + "</color>"
        else:
            optdesp = "<color=#00ff00>" + optname + "</color>: " + optdesp
        optold = is_ini_value_true(optname)
        optnew = GUILayout.Toggle(optold, optdesp)
        if optold != optnew:
            set_ini_value(optname, optnew)
    GUILayout.EndScrollView()
    # Tail button
    GUILayout.FlexibleSpace()
    GUILayout.BeginHorizontal()
    if GUILayout.Button("Back", GUILayout.Width(wwidth/3-2), GUILayout.Height(24)):
        start(game)
    if GUILayout.Button("Readme", GUILayout.Width(wwidth/3-2), GUILayout.Height(24)):
        from vngameengine import get_engine_id
        msg = "VNActor extend export settings, which are wrtten in vnactor.ini file, can be modified here in run time. These settings affect the behavior of other components that depends on vnactor (such as VNFrame, VNAnime and SceneSaveState).\nTo keep you setting permanently, please edit them in vnactor.ini under <color=#00ff00>[" + get_engine_id() + "]</color> category and then click <Reload>."
        game.show_blocking_message_time(msg)
    if GUILayout.Button("Reload", GUILayout.Width(wwidth/3-2), GUILayout.Height(24)):
        load_ini_file(True)
    GUILayout.EndHorizontal()

# -------------- clothes --------------------

def start_clothes(game):
    """:type game: vngameengine.VNNeoController"""
    if game.isPlayHomeStudio:
        game.show_blocking_message_time("Sorry, this not supported in PlayHome Studio")
        return

    game.set_text_s("What to do to selected char?\nClothes...")
    btns = [
        #"Add to crotch", uAddCrch,
        "Copy clothes", clothes_copy,
        "Paste clothes", clothes_paste,

    ]

    if game.isCharaStudio:
        btns += [
            "Paste clothes without acc", clothes_paste_no_acc,
        ]

    btns += [
        "<<", start,
    ]
    game.set_buttons_alt(btns, "compact")

def clothes_copy(game):
    """:type game: vngameengine.VNNeoController"""
    actor = get_selected_actor(game)

    if actor == None:
        game.show_blocking_message_time("No selected char")
        return

    game.gdata.clothes = actor.get_curcloth_coordinate()
    game.show_blocking_message_time("Copied!", 1)

def clothes_paste(game):
    """:type game: vngameengine.VNNeoController"""
    actor = get_selected_actor(game)

    if actor == None:
        game.show_blocking_message_time("No selected char")
        return

    actor.set_curcloth_coordinate(game.gdata.clothes)

def clothes_paste_no_acc(game):
    """:type game: vngameengine.VNNeoController"""
    actor = get_selected_actor(game)

    if actor == None:
        game.show_blocking_message_time("No selected char")
        return

    actor.set_curcloth_coordinate_no_accessory(game.gdata.clothes)

# -------------- vntext --------------------
def start_vntext_editor(game):
    game.set_text_s("")
    game.set_buttons_alt([],("function", start_vntext_editor_gui))

def start_vntext_editor_gui(game, info):
    def backfunc():
        start(game)
    from vntext import vntxt_GUI
    vntxt_GUI(game, backfunc)

# --------------- ai dhh ---------------
def ai_save_dhh(game):
    import extplugins
    try:
        pl_dhh = extplugins.DHH_AI()
        expsettings = pl_dhh.exportGraphSetting();
        foldername = "-vngedhhaisave:"
        fold = HSNeoOCIFolder.find_single(foldername)
        if fold == None:
            fold = HSNeoOCIFolder.add(foldername)
        fold.delete_all_children()
        sett = fold.add(expsettings)
        sett.set_parent(fold)
        game.show_blocking_message_time("DHH settings saved!")
    except Exception, e:
        game.show_blocking_message_time("Can't save DHH. May be no plugin or other error.")

def ai_load_dhh(game):
    from vngameengine import HSNeoOCIFolder
    fld = HSNeoOCIFolder.find_single_startswith("-vngedhhaisave:")
    if fld != None:
        if fld.treeNodeObject.childCount > 0:
            obj2 = HSNeoOCI.create_from_treenode(fld.treeNodeObject.child[0])
            str = obj2.name
            import extplugins
            try:
                pl_dhh = extplugins.DHH_AI()
                pl_dhh.importGraphSetting(str)
                #game.show_blocking_message_time("DHH loaded!")
            except Exception, e:
                game.show_blocking_message_time("Can't load DHH. May be no plugin or other error.")

# config ini values
# ini file

_iniOptions = None

def get_ini_value(elem): # get ini value for cur engine
    global _iniOptions
    if _iniOptions != None:
        # already parsed
        pass
    else:
        # need to parse and cache
        _iniOptions = {}

        import ConfigParser, sys, os.path
        config = ConfigParser.SafeConfigParser()
        config.read(os.path.splitext(__file__)[0] + '.ini')

        for k, v in config.items("Options"):
            _iniOptions[k.lower()] = v


    # main code
    #print _iniOptions
    elemlower = elem.lower()
    if elemlower in _iniOptions:
        return _iniOptions[elemlower]

    return None

def get_ini_value_def_int(elem,defint):
    val = get_ini_value(elem)
    if val == None:
        return defint
    else:
        val2 = int(val)
        if val2 == -1:
            return defint
        else:
            return val2

def is_ini_value_true(elem):
    val = get_ini_value(elem)
    if val != None and val != 0 and val != "0":
        return True
    return False


# this.charInfo.nowCoordinate.LoadFile(_path);
# this.charInfo.AssignCoordinate((ChaFileDefine.CoordinateType)this.charInfo.fileStatus.coordinateType);
# this.charInfo.Reload(false, true, true, true)