
# A VNGE text plugin, add textmesh into scene
# Specially optimized for VNSS
# By Countd360
# 
# Thanks jim60105 for useful code reference
# 
# v1.0
# - everything
# v1.1
# - auto correct vntext id if duplicate found
#

from vngameengine import HSNeoOCI, HSNeoOCIFolder
from scenesavestate import folder_add_child
from UnityEngine import GameObject, Resources, AssetBundle, TextMesh, MeshRenderer, Material
from UnityEngine import Vector3, Vector2, Quaternion, Color, Font
from UnityEngine import TextAnchor, TextAlignment
from System import Action, Array, String
from vnframe import script2string
from vnactor import value_2_enum, tuple3_2_vector3, get_camera_data
import traceback

def init_vntext_manager(game):
    # create vntext manager
    game.gdata.vnTextManager = TextManager(game)
    game.scenedata.vntxtGuiInitFlag = False

    # re-register update function
    game.event_unreg_listener("update", update_vntext_process, "vntext_update")
    game.event_reg_listener("update", update_vntext_process, "vntext_update")

    return game.gdata.vnTextManager

def clear_vntext_manager(game):
    game.event_unreg_listener("update", update_vntext_process, "vntext_update")
    game.gdata.vnTextManager = None

def get_vntext_manager(game):
    if not check_vnText(game):
        return init_vntext_manager(game)
    else:
        return game.gdata.vnTextManager

def check_vnText(game):
    return hasattr(game.gdata, "vnTextManager") and game.gdata.vnTextManager != None

def update_vntext_process(game, evid, param):
    mgr = get_vntext_manager(game)
    mgr.housekeep()
    mgr.cameraWork(game)
    mgr.animeUpdate(game)

def vntxt_GUI(game, backfunc, okBtnSetting = None):
    vntxt_GUI_editor(game, backfunc, okBtnSetting)

def vntxt_GUI_editor(game, backfunc, okBtnSetting):
    from UnityEngine import GUI, GUILayout, GUIStyle, Texture2D, TextureWrapMode, TextClipping
    # size and style
    fullw = game.wwidth-36
    btnstyle = GUIStyle("button")
    btnstyle.fontSize = 14
    nameW = 70

    # data shortcuts
    sd = game.scenedata
    mgr = get_vntext_manager(game)
    tis = mgr.getCurrentSelected()
    ti0 = tis[0]

    # data init
    if not hasattr(sd, "vntxtGuiInitFlag") or not sd.vntxtGuiInitFlag:
        sd.vntxtGuiInitFlag = True
        sd.vntxtGuiScrollPos = Vector2.zero
        sd.vntxtGuiViewMode = "text"
        sd.vntxtGuiAdvanced = True
        sd.vntxtGuiOnAnchor = False
        sd.vntxtGuiOnAlignment = False
        
        sd.vntxtLastTextInfo = None
        sd.vntxtTempText = "New Text"
        sd.vntxtTempColor = Color.white
        sd.vntxtTempVisible = True
        sd.vntxtTempInFront = not mgr.font3DMaterialValid
        sd.vntxtTempFontName = "Arial"
        sd.vntxtTempSize = 1
        sd.vntxtTempScaleX = 1
        sd.vntxtTempScaleY = 1
        sd.vntxtTempAnchor = 0
        sd.vntxtTempAlignment = 0
        sd.vntxtTempManaged = True
        sd.vntxtTempBindCameraFace = False
        sd.vntxtTempBindCameraFaceWOZ = False
        sd.vntxtTempBindCameraPos = False
        sd.vntxtTempAnimeOneByOne = False
        sd.vntxtTempAnimeOneByOneSpeed = 0.1
        sd.vntxtTempId = ""

    if sd.vntxtLastTextInfo != ti0:
        sd.vntxtLastTextInfo = ti0
        if ti0 != None:
            sd.vntxtTempText = ti0.text
            sd.vntxtTempColor = ti0.color
            sd.vntxtTempVisible = ti0.visible
            sd.vntxtTempInFront = ti0.inFront
            sd.vntxtTempFontName = ti0.fontName
            sd.vntxtTempSize = ti0.size
            sd.vntxtTempScaleX = ti0.scale.x
            sd.vntxtTempScaleY = ti0.scale.y
            sd.vntxtTempAnchor = ti0.anchorStyle
            sd.vntxtTempAlignment = ti0.alignment
            sd.vntxtTempManaged = ti0.managed
            sd.vntxtTempBindCameraFace = ti0.bindCamera != None and "FaceCam" in ti0.bindCamera[0]
            sd.vntxtTempBindCameraFaceWOZ = ti0.bindCamera != None and "FaceCamWOZ" in ti0.bindCamera[0]
            sd.vntxtTempBindCameraPos = ti0.bindCamera != None and "BindPos" in ti0.bindCamera[0]
            sd.vntxtTempAnimeOneByOne = len(ti0.animeController) > 0 and isinstance(ti0.animeController[0], TextAnimeOneByOne)
            sd.vntxtTempAnimeOneByOneSpeed = 0.1 if not sd.vntxtTempAnimeOneByOne else ti0.animeController[0].speed
            sd.vntxtTempId = ti0.id

    # local functions
    def create():
        nti = mgr.newTextInfo()
        nti.text = sd.vntxtTempText
        nti.color = sd.vntxtTempColor
        nti.visible = sd.vntxtTempVisible
        nti.inFront = sd.vntxtTempInFront
        nti.fontName = sd.vntxtTempFontName
        nti.size = sd.vntxtTempSize
        nti.scale = Vector3(sd.vntxtTempScaleX, sd.vntxtTempScaleY, 1)
        nti.anchorStyle = sd.vntxtTempAnchor
        nti.alignment = sd.vntxtTempAlignment
        nti.managed = sd.vntxtTempManaged
        mgr.createText(nti)
    def delete():
        for ti in tis:
            mgr.deleteText(ti)
    def deleteAll():
        mgr.deleteAll()
    def deleteManaged():
        mgr.deleteAll(True, False)
    def changeColor(color):
        sd.vntxtTempColor = color
        for ti in tis:
            if ti: ti.setColor(color)
    def changeVisible(v):
        sd.vntxtTempVisible = v
        for ti in tis:
            if ti: ti.setVisible(v)
    def changeInFront(v):
        sd.vntxtTempInFront = v
        for ti in tis:
            if ti: ti.setInFront(v)
    def changeSize():
        for ti in tis:
            if ti: ti.setSize(sd.vntxtTempSize, mgr.charSizeRate)
    def changeScale():
        for ti in tis:
            if ti: ti.setScale(sd.vntxtTempScaleX, sd.vntxtTempScaleY)
    def changeAnchor(anchor):
        sd.vntxtTempAnchor = anchor
        sd.vntxtGuiOnAnchor = False
        for ti in tis:
            if ti: ti.setAnchorStyle(anchor)
    def changeAlignment(align):
        sd.vntxtTempAlignment = align
        sd.vntxtGuiOnAlignment = False
        for ti in tis:
            if ti: ti.setAlignment(align)
    def changeManaged(v):
        sd.vntxtTempManaged = v
        for ti in tis:
            if ti: mgr.setManaged(ti, v)
    def changeID(id):
        ti0.setID(id)
    def changeBindCamera():
        # build bind cmd
        bindCmd = ""
        if sd.vntxtTempBindCameraFaceWOZ:
            bindCmd += "FaceCamWOZ"
        elif sd.vntxtTempBindCameraFace:
            bindCmd += "FaceCam"
        if sd.vntxtTempBindCameraPos:
            bindCmd += "BindPos"
        # set bind
        camData = get_camera_data(game)
        for ti in tis:
            if ti: ti.setBindCamera(bindCmd, camData)
    def changeAnime():
        # setup anime
        if sd.vntxtTempAnimeOneByOne:
            ac = TextAnimeOneByOne()
            ac.speed = sd.vntxtTempAnimeOneByOneSpeed
            for ti in tis:
                if ti: ti.setAnime([ac])
        else:
            for ti in tis:
                if ti: ti.setAnime([])
    def color2htmlhex(color):
        return "#%02x%02x%02x"%(color.r * 255, color.g * 255, color.b * 255)

    # GUI starts
    # Title
    if sd.vntxtGuiViewMode == "font":
        GUILayout.Label("Choise a font:")
    elif sd.vntxtGuiViewMode == "listall":
        #GUILayout.Label("List of all vntexts:")
        pass
    elif sd.vntxtGuiViewMode == "confirm":
        GUILayout.Label(sd.vntxtGuiConfirmTitle)
    elif len(tis) > 1:
        ids = "<color=#00ff00>%s</color>"%ti0.id
        for i in range(1, len(tis)):
            ids += ", <color=#00ff00>%s</color>"%tis[i].id
        GUILayout.BeginHorizontal()
        GUILayout.Label("Edit texts (IDs=%s):"%ids)
        GUILayout.Space(10)
        if GUILayout.Button("New", GUILayout.Width(40)):
            ti0.deselect()
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()
    elif ti0:
        GUILayout.BeginHorizontal()
        GUILayout.Label("Edit text (ID=<color=#00ff00>%s</color>):"%ti0.id)
        GUILayout.Space(10)
        if GUILayout.Button("New", GUILayout.Width(40)):
            ti0.deselect()
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()
    else:
        GUILayout.BeginHorizontal()
        GUILayout.Label("Create a <color=#ff0000>NEW</color> text:")
        GUILayout.Space(10)
        if GUILayout.Button("Reset", GUILayout.Width(60)):
            sd.vntxtGuiInitFlag = False
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()

    # begin of scroll zone
    sd.vntxtGuiScrollPos = GUILayout.BeginScrollView(sd.vntxtGuiScrollPos)
    
    if sd.vntxtGuiViewMode == "text":
        # normal view
        # properties: text
        if len(tis) == 1:
            GUILayout.BeginHorizontal()
            GUILayout.Label("Text:", GUILayout.Width(nameW))
            inputtext = GUILayout.TextArea(sd.vntxtTempText, GUILayout.Width(fullw-nameW-20))
            if sd.vntxtTempText != inputtext:
                sd.vntxtTempText = inputtext
                if ti0:
                    ti0.setText(inputtext)
            GUILayout.EndHorizontal()

        # properties: color, visible, infront
        GUILayout.BeginHorizontal()
        GUILayout.Label("Color:", GUILayout.Width(nameW))
        colorTex = Texture2D(50, 20)
        colorTex.SetPixels(Array[Color]([sd.vntxtTempColor]*50*20))
        colorTex.Apply()
        if GUILayout.Button(colorTex, GUILayout.Height(20), GUILayout.Width(70)):
            if game.isNEOV2 or game.isCharaStudio:
                ca = Action[Color](changeColor)
                game.studio.colorPalette.Setup("VNText Color", sd.vntxtTempColor, ca, True)
                game.studio.colorPalette.visible = True
            elif game.isPlayHomeStudio:
                from Studio import UI_ColorInfo
                ca = UI_ColorInfo.UpdateColor(changeColor)
                game.studio.colorMenu.updateColorFunc = ca
                game.studio.colorMenu.SetColor(sd.vntxtTempColor, UI_ColorInfo.ControlType.PresetsSample)
                game.studio.colorPaletteCtrl.visible = True
            elif game.isStudioNEO:
                import UI_ColorInfo
                ca = UI_ColorInfo.UpdateColor(changeColor)
                game.studio.colorMenu.updateColorFunc = ca
                game.studio.colorMenu.SetColor(sd.vntxtTempColor, UI_ColorInfo.ControlType.PresetsSample)
                game.studio.colorPaletteCtrl.visible = True

        GUILayout.Space(10)
        nvisible = GUILayout.Toggle(sd.vntxtTempVisible, "Visible")
        if sd.vntxtTempVisible != nvisible:
            changeVisible(nvisible)
        if mgr.font3DMaterialValid:
            GUILayout.Space(10)
            ninfront = not GUILayout.Toggle(not sd.vntxtTempInFront, "3D Material")
            if sd.vntxtTempInFront != ninfront:
                changeInFront(ninfront)
            GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()

        # properties: font
        GUILayout.BeginHorizontal()
        GUILayout.Label("Font:", GUILayout.Width(nameW))
        if GUILayout.Button(sd.vntxtTempFontName, GUILayout.Width(fullw-nameW-20)):
            sd.vntxtGuiViewMode = "font"
        GUILayout.EndHorizontal()

        # properties: size, w, h
        GUILayout.BeginHorizontal()
        GUILayout.Label("Size:", GUILayout.Width(nameW))
        if GUILayout.RepeatButton("<"):
            sd.vntxtTempSize -= 0.01
            if sd.vntxtTempSize <= 0.001: sd.vntxtTempSize = 0.001
            changeSize()
        inputsize = GUILayout.TextField("%.3f"%sd.vntxtTempSize)
        try:
            nsize = float(inputsize)
            if sd.vntxtTempSize != nsize:
                sd.vntxtTempSize = nsize
                changeSize()
        except:
            pass
        if GUILayout.RepeatButton(">"):
            sd.vntxtTempSize += 0.01
            changeSize()
        GUILayout.Space(10)
        GUILayout.Label("Width:")
        if GUILayout.RepeatButton("<"):
            sd.vntxtTempScaleX -= 0.01
            if sd.vntxtTempScaleX < 0.001: sd.vntxtTempScaleX = 0.001
            changeScale()
        inputsize = GUILayout.TextField("%.3f"%sd.vntxtTempScaleX)
        try:
            nsize = float(inputsize)
            if sd.vntxtTempScaleX != nsize:
                sd.vntxtTempScaleX = nsize
                if sd.vntxtTempScaleX <= 0.001: sd.vntxtTempScaleX = 0.001
                changeScale()
        except:
            pass
        if GUILayout.RepeatButton(">"):
            sd.vntxtTempScaleX += 0.01
            changeScale()
        GUILayout.Space(10)
        GUILayout.Label("Height:")
        if GUILayout.RepeatButton("<"):
            sd.vntxtTempScaleY -= 0.01
            if sd.vntxtTempScaleY <= 0.001: sd.vntxtTempScaleY = 0.001
            changeScale()
        inputsize = GUILayout.TextField("%.3f"%sd.vntxtTempScaleY)
        try:
            nsize = float(inputsize)
            if sd.vntxtTempScaleY != nsize:
                sd.vntxtTempScaleY = nsize
                if sd.vntxtTempScaleY <= 0.001: sd.vntxtTempScaleY = 0.001
                changeScale()
        except:
            pass
        if GUILayout.RepeatButton(">"):
            sd.vntxtTempScaleY += 0.01
            changeScale()
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()

        # advanced
        #sd.vntxtGuiAdvanced = GUILayout.Toggle(sd.vntxtGuiAdvanced, "Advanced options")
        if sd.vntxtGuiAdvanced:
            # anchor, alignment
            anchorStyleList = ("UpperLeft", "UpperCenter", "UpperRight", "MiddleLeft", "MiddleCenter", "MiddleRight", "LowerLeft", "LowerCenter", "LowerRight")
            alignmentStyleList = ("Left", "Center", "Right", "Vertical Left<<<Right", "Vertical Left>>>Right")
            if sd.vntxtGuiOnAnchor:
                GUILayout.BeginHorizontal()
                GUILayout.Label("Anchor:", GUILayout.Width(nameW))
                if GUILayout.Button(anchorStyleList[0] if sd.vntxtTempAnchor != 0 else "<color=#00ff00>"+anchorStyleList[0]+"</color>", GUILayout.Width(100)):
                    changeAnchor(0)
                if GUILayout.Button(anchorStyleList[1] if sd.vntxtTempAnchor != 1 else "<color=#00ff00>"+anchorStyleList[1]+"</color>", GUILayout.Width(100)):
                    changeAnchor(1)
                if GUILayout.Button(anchorStyleList[2] if sd.vntxtTempAnchor != 2 else "<color=#00ff00>"+anchorStyleList[2]+"</color>", GUILayout.Width(100)):
                    changeAnchor(2)
                GUILayout.EndHorizontal()
                GUILayout.BeginHorizontal()
                GUILayout.Label(" ", GUILayout.Width(nameW))
                if GUILayout.Button(anchorStyleList[3] if sd.vntxtTempAnchor != 3 else "<color=#00ff00>"+anchorStyleList[3]+"</color>", GUILayout.Width(100)):
                    changeAnchor(3)
                if GUILayout.Button(anchorStyleList[4] if sd.vntxtTempAnchor != 4 else "<color=#00ff00>"+anchorStyleList[4]+"</color>", GUILayout.Width(100)):
                    changeAnchor(4)
                if GUILayout.Button(anchorStyleList[5] if sd.vntxtTempAnchor != 5 else "<color=#00ff00>"+anchorStyleList[5]+"</color>", GUILayout.Width(100)):
                    changeAnchor(5)
                GUILayout.EndHorizontal()
                GUILayout.BeginHorizontal()
                GUILayout.Label(" ", GUILayout.Width(nameW))
                if GUILayout.Button(anchorStyleList[6] if sd.vntxtTempAnchor != 6 else "<color=#00ff00>"+anchorStyleList[6]+"</color>", GUILayout.Width(100)):
                    changeAnchor(6)
                if GUILayout.Button(anchorStyleList[7] if sd.vntxtTempAnchor != 7 else "<color=#00ff00>"+anchorStyleList[7]+"</color>", GUILayout.Width(100)):
                    changeAnchor(7)
                if GUILayout.Button(anchorStyleList[8] if sd.vntxtTempAnchor != 8 else "<color=#00ff00>"+anchorStyleList[8]+"</color>", GUILayout.Width(100)):
                    changeAnchor(8)
                GUILayout.EndHorizontal()
            elif sd.vntxtGuiOnAlignment:
                GUILayout.BeginHorizontal()
                GUILayout.Label("Alignment:", GUILayout.Width(nameW))
                if GUILayout.Button(alignmentStyleList[0] if sd.vntxtTempAlignment != 0 else "<color=#00ff00>"+alignmentStyleList[0]+"</color>", GUILayout.Width(100)):
                    changeAlignment(0)
                if GUILayout.Button(alignmentStyleList[1] if sd.vntxtTempAlignment != 1 else "<color=#00ff00>"+alignmentStyleList[1]+"</color>", GUILayout.Width(100)):
                    changeAlignment(1)
                if GUILayout.Button(alignmentStyleList[2] if sd.vntxtTempAlignment != 2 else "<color=#00ff00>"+alignmentStyleList[2]+"</color>", GUILayout.Width(100)):
                    changeAlignment(2)
                GUILayout.EndHorizontal()
                GUILayout.BeginHorizontal()
                GUILayout.Label(" ", GUILayout.Width(nameW))
                if GUILayout.Button(alignmentStyleList[3] if sd.vntxtTempAlignment != 3 else "<color=#00ff00>"+alignmentStyleList[3]+"</color>", GUILayout.Width(152)):
                    changeAlignment(3)
                if GUILayout.Button(alignmentStyleList[4] if sd.vntxtTempAlignment != 4 else "<color=#00ff00>"+alignmentStyleList[4]+"</color>", GUILayout.Width(152)):
                    changeAlignment(4)
                GUILayout.EndHorizontal()
            else:
                GUILayout.BeginHorizontal()
                GUILayout.Label("Anchor:", GUILayout.Width(nameW))
                if GUILayout.Button(anchorStyleList[sd.vntxtTempAnchor], GUILayout.Width(100)):
                    sd.vntxtGuiOnAnchor = True
                GUILayout.Space(10)
                GUILayout.Label("Alignment:")
                if GUILayout.Button(alignmentStyleList[sd.vntxtTempAlignment], GUILayout.Width(150)):
                    sd.vntxtGuiOnAlignment = True
                GUILayout.FlexibleSpace()
                GUILayout.EndHorizontal()

            # manager, id
            GUILayout.BeginHorizontal()
            GUILayout.Label("ID Manage:", GUILayout.Width(nameW))
            nmanaged = GUILayout.Toggle(sd.vntxtTempManaged, "Dynamic manage")
            if sd.vntxtTempManaged != nmanaged:
                changeManaged(nmanaged)
            if ti0 and len(tis) == 1:
                GUILayout.Space(10)
                GUILayout.Label("ID:")
                sd.vntxtTempId = GUILayout.TextField(sd.vntxtTempId, GUILayout.Width(100))
                sd.vntxtTempId = sd.vntxtTempId.strip()
                if len(sd.vntxtTempId) == 0:
                    GUILayout.Label("<color=#ff0000>Empty ID!!</color>")
                elif sd.vntxtTempId != ti0.id and sd.vntxtTempId in TextManager.listAllIds():
                    GUILayout.Label("<color=#ff0000>Duplicated ID!!</color>")
                elif sd.vntxtTempId != ti0.id and GUILayout.Button("Apply", GUILayout.Width(50)):
                    changeID(sd.vntxtTempId)
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()

            # bind camera, not valid for new
            if ti0:
                GUILayout.BeginHorizontal()
                GUILayout.Label("Bind Cam:", GUILayout.Width(nameW))
                bindPos = GUILayout.Toggle(sd.vntxtTempBindCameraPos, "Move with camera")
                if sd.vntxtTempBindCameraPos != bindPos:
                    sd.vntxtTempBindCameraPos = bindPos
                    changeBindCamera()
                GUILayout.Space(10)
                bindCamFace = GUILayout.Toggle(sd.vntxtTempBindCameraFace, "Face to camera")
                if sd.vntxtTempBindCameraFace != bindCamFace:
                    sd.vntxtTempBindCameraFace = bindCamFace
                    changeBindCamera()
                if bindCamFace:
                    GUILayout.Space(10)
                    bindCamFaceWoz = GUILayout.Toggle(sd.vntxtTempBindCameraFaceWOZ, "exclude z-rot")
                    if sd.vntxtTempBindCameraFaceWOZ != bindCamFaceWoz:
                        sd.vntxtTempBindCameraFaceWOZ = bindCamFaceWoz
                        changeBindCamera()
                else:
                    if sd.vntxtTempBindCameraFaceWOZ:
                        sd.vntxtTempBindCameraFaceWOZ = False
                        changeBindCamera()
                GUILayout.FlexibleSpace()
                GUILayout.EndHorizontal()

            # anime control, not valid for new
            if ti0:
                GUILayout.BeginHorizontal()
                GUILayout.Label("Animation:", GUILayout.Width(nameW))
                onebyone = GUILayout.Toggle(sd.vntxtTempAnimeOneByOne, "Show letters one by one, with ")
                if sd.vntxtTempAnimeOneByOne != onebyone:
                    sd.vntxtTempAnimeOneByOne = onebyone
                    changeAnime()
                oldSpdTxt = "%.2f"%sd.vntxtTempAnimeOneByOneSpeed
                newSpdTxt = GUILayout.TextField(oldSpdTxt, GUILayout.Width(50))
                if newSpdTxt != oldSpdTxt:
                    try:
                        sd.vntxtTempAnimeOneByOneSpeed = float(newSpdTxt)
                        changeAnime()
                    except:
                        pass
                GUILayout.Label(" sec per letter.")
                GUILayout.FlexibleSpace()
                GUILayout.EndHorizontal()

        else:
            sd.vntxtGuiOnAnchor = False
            sd.vntxtGuiOnAlignment = False

    elif sd.vntxtGuiViewMode == "font":
        # font selection preview
        prevTxt = sd.vntxtTempText.splitlines()[0].strip()
        if len(prevTxt) == 0: prevTxt = "New Text"
        enablePreview = mgr.dynamicFonts != None
        previewStyle = GUIStyle("label")
        previewStyle.fontSize = 25
        previewStyle.clipping = TextClipping.Overflow
        previewStyle.wordWrap = False
        previewStyle.stretchHeight = True

        for fontName in TextManager.fontList:
            sel = GUILayout.Toggle(fontName == sd.vntxtTempFontName, fontName)
            if sel != (fontName == sd.vntxtTempFontName):
                sd.vntxtTempFontName = fontName
                sd.vntxtGuiViewMode = "text"
                font = mgr.checkAndGetFont(sd.vntxtTempFontName)
                for ti in tis:
                    if ti: ti.setFont(font)
            if enablePreview:
                previewStyle.font = mgr.checkAndGetFont(fontName)
                GUILayout.BeginHorizontal()
                GUILayout.Space(20)
                GUILayout.Label(prevTxt, previewStyle, GUILayout.Width(fullw-20-20))
                GUILayout.EndHorizontal()

    elif sd.vntxtGuiViewMode == "listall":
        if mgr.allTextCount == 0:
            GUILayout.Label("No vntext found, create some or try reload.")
        else:
            if mgr.managedTextCount > 0:
                GUILayout.Label("<color=#00ff00>Managed Texts</color>:")
                for ti in mgr.managedTexts:
                    tinfo = "%s: <color=%s>%s</color>"%(ti.id, color2htmlhex(ti.color), ti.text)
                    GUILayout.BeginHorizontal()
                    sel = GUILayout.Toggle(False, tinfo)
                    if sel:
                        ti.select()
                        sd.vntxtGuiViewMode = "text"
                    GUILayout.EndHorizontal()
            if mgr.staticTextCount > 0:
                GUILayout.Label("<color=#ffff00>Static Texts</color>:")
                for ti in mgr.staticTexts:
                    tinfo = "%s: <color=%s>%s</color>"%(ti.id, color2htmlhex(ti.color), ti.text)
                    GUILayout.BeginHorizontal()
                    sel = GUILayout.Toggle(False, tinfo)
                    if sel:
                        ti.select()
                        sd.vntxtGuiViewMode = "text"
                    GUILayout.EndHorizontal()


    elif sd.vntxtGuiViewMode == "confirm":
        GUILayout.Label(sd.vntxtGuiConfirmText)

    # end of scroll zone
    GUILayout.EndScrollView()

    # end button
    GUILayout.FlexibleSpace()
    GUILayout.BeginHorizontal()
    if sd.vntxtGuiViewMode == "text":
        # normal
        if okBtnSetting != None and GUILayout.Button(okBtnSetting[0], btnstyle, GUILayout.Width(fullw/4-3)):
            okBtnSetting[1]()
        if GUILayout.Button("<color=#ff0000>Delete</color>" if ti0 else "<color=#00ff00>Create</color>", btnstyle, GUILayout.Width(fullw/4-3)):
            if ti0:
                sd.vntxtGuiConfirmTitle = "Warning:"
                sd.vntxtGuiConfirmText = "Are you sure to delete selected text(s):"
                for ti in tis:
                    sd.vntxtGuiConfirmText += "\n<color=#00ff00>" + ti.id + "</color>: " + ti.text
                sd.vntxtGuiConfirmFunc = delete
                sd.vntxtGuiViewMode = "confirm"
            else:
                create()
        if GUILayout.Button("List All", btnstyle, GUILayout.Width(fullw/4-3)):
            sd.vntxtGuiViewMode = "listall"
        if okBtnSetting == None and GUILayout.Button("Reload", btnstyle, GUILayout.Width(fullw/4-3)):
            mgr.reloadTextInfo()
        if GUILayout.Button("Back", btnstyle, GUILayout.Width(fullw/4-3)):
            backfunc()
    elif sd.vntxtGuiViewMode == "font":
        # font preview
        if GUILayout.Button(" ", btnstyle, GUILayout.Width(fullw/4-3)):
            pass
        if GUILayout.Button(" ", btnstyle, GUILayout.Width(fullw/4-3)):
            pass
        if GUILayout.Button(" ", btnstyle, GUILayout.Width(fullw/4-3)):
            pass
        if GUILayout.Button("Cancel", btnstyle, GUILayout.Width(fullw/4-3)):
            sd.vntxtGuiViewMode = "text"
    elif sd.vntxtGuiViewMode == "listall":
        # font preview
        if GUILayout.Button("<color=#ff0000>Delete Managed</color>" if mgr.managedTextCount > 0 else " ", btnstyle, GUILayout.Width(fullw/4-3)) and mgr.managedTextCount > 0:
            sd.vntxtGuiConfirmTitle = "Warning:"
            sd.vntxtGuiConfirmText = "Are you sure to delete all %d managed texts?"%mgr.managedTextCount
            sd.vntxtGuiConfirmFunc = deleteManaged
            sd.vntxtGuiViewMode = "confirm"
        if GUILayout.Button("<color=#ff0000>Delete All</color>" if mgr.allTextCount > 0 else " ", btnstyle, GUILayout.Width(fullw/4-3)) and mgr.allTextCount > 0:
            sd.vntxtGuiConfirmTitle = "Warning:"
            sd.vntxtGuiConfirmText = "Are you sure to delete all %d texts?"%mgr.allTextCount
            sd.vntxtGuiConfirmFunc = deleteAll
            sd.vntxtGuiViewMode = "confirm"
        if GUILayout.Button("Reload", btnstyle, GUILayout.Width(fullw/4-3)):
            mgr.reloadTextInfo()
        if GUILayout.Button("Back", btnstyle, GUILayout.Width(fullw/4-3)):
            sd.vntxtGuiViewMode = "text"
    elif sd.vntxtGuiViewMode == "confirm":
        # confirm preview
        if GUILayout.Button("OK", btnstyle, GUILayout.Width(fullw/4-3)):
            sd.vntxtGuiConfirmFunc()
            sd.vntxtGuiViewMode = "text"
        if GUILayout.Button(" ", btnstyle, GUILayout.Width(fullw/4-3)):
            pass
        if GUILayout.Button(" ", btnstyle, GUILayout.Width(fullw/4-3)):
            pass
        if GUILayout.Button("Cancel", btnstyle, GUILayout.Width(fullw/4-3)):
            sd.vntxtGuiViewMode = "text"
    else:
        print "Unknown view mode = %s"%sd.vntxtGuiViewMode
        sd.vntxtGuiViewMode = "text"
    GUILayout.EndHorizontal()

    # GUI Ends

class TextInfo():
    def __init__(self):
        # basic setting
        self.id = ""
        self.text = ""
        self.size = 1
        self.visible = True
        self.inFront = True
        self.color = Color.white
        self.fontName = "Arial"
        self.anchorStyle = 0
        self.alignment = 0

        self.position = Vector3.zero
        self.rotation = Vector3.zero
        self.scale = Vector3.one

        # advanced setting
        self.version = 1
        self.managed = False
        self.bindCamera = None
        self.animeController = []

        # runtime
        self.meshObj = None
        self.anchorFolder = None

    @staticmethod
    def buildFromFolder(folder):
        if not isinstance(folder, HSNeoOCIFolder):
            return None
        if not folder.name.startswith("-vntext:"):
            return None
        id = folder.name[8:]
        for cto in folder.objctrl.treeNodeObject.child:
            if cto.textName.startswith("-vntextdata:"):
                sstxt = cto.textName[12:]
                nti = TextInfo()
                nti.id = id
                if nti.loadSetting(sstxt):
                    nti.anchorFolder = folder
                    nti.meshObj = nti.anchorFolder.objctrl.objectItem.GetComponentInChildren(TextMesh, True)
                    return nti
        return None

    @staticmethod
    def buildRenderText(text, alignment):
        if len(text) == 0:
            return text
        if alignment == 3:
            # Vertical R->L
            ls = text.splitlines()
            ls.reverse()
            lenOfLine = [len(s) for s in ls]
            rows = []
            for i in range(max(lenOfLine)):
                row = ""
                for j in range(len(ls)):
                    if i < lenOfLine[j]:
                        row += ls[j][i]
                    else:
                        if len(row) > 0:
                            row += u'\u3000'
                rows.append(row)
            ot = "\n".join(rows)
            return ot
        elif alignment == 4:
            # Vertical L->R
            ls = text.splitlines()
            lenOfLine = [len(s) for s in ls]
            rows = []
            for i in range(max(lenOfLine)):
                row = ""
                for j in range(len(ls)):
                    if i < lenOfLine[j]:
                        row += ls[j][i]
                    else:
                        row += u'\u3000'
                rows.append(row)
            ot = "\n".join(rows)
            return ot
        else:
            return text        

    @property
    def valid(self):
        return self.anchorFolder != None and self.anchorFolder.objctrl != None and hasattr(self.anchorFolder.objctrl, "treeNodeObject") and self.anchorFolder.objctrl.treeNodeObject != None

    @property
    def isSelected(self):
        if self.valid:
            from Studio import Studio
            return self.anchorFolder.objctrl.treeNodeObject in Studio.Instance.treeNodeCtrl.selectNodes
        else:
            return False

    def select(self):
        # set as the selected
        if self.valid and not self.isSelected:
            from Studio import Studio
            from vngameengine import get_engine_id
            try:
                engid = get_engine_id()
                if engid == "charastudio" or engid == "neov2":
                    # function in KK and AI
                    Studio.Instance.treeNodeCtrl.SelectSingle(self.anchorFolder.objctrl.treeNodeObject, False)
                elif engid == "phstudio" or engid == "neo":
                    # function in PH
                    Studio.Instance.treeNodeCtrl.SelectSingle(self.anchorFolder.objctrl.treeNodeObject)
                else:
                    print "VNText error: Unsupported Game engine %s"%engid
                    return
            except:
                print "VNText error: Fail to select vntext [%s]"%self.id
                traceback.print_exc()

    def deselect(self):
        # deselect if selected
        if self.isSelected:
            from Studio import Studio
            from vngameengine import get_engine_id
            try:
                engid = get_engine_id()
                if engid == "charastudio" or engid == "neov2":
                    # function in KK and AI
                    Studio.Instance.treeNodeCtrl.SelectSingle(self.anchorFolder.objctrl.treeNodeObject, False)
                    Studio.Instance.treeNodeCtrl.SelectSingle(self.anchorFolder.objctrl.treeNodeObject, True)
                elif engid == "phstudio" or engid == "neo":
                    # function in PH
                    Studio.Instance.treeNodeCtrl.SelectSingle(None)
                else:
                    print "VNText error: Unsupported Game engine %s"%engid
                    return
            except:
                print "VNText error: Fail to deselect vntext [%s]"%self.id
                traceback.print_exc()


    def delete(self):
        # delete anchor
        if self.valid:
            self.deselect()
            self.anchorFolder.delete()
            self.anchorFolder = None
            self.meshObj = None

    def updateSetting(self):
        # update some setting from anchor folder
        if self.valid:
            changed = False
            if self.position != self.anchorFolder.pos:
                self.position = self.anchorFolder.pos
                changed = True
            if self.rotation != self.anchorFolder.rot:
                self.rotation = self.anchorFolder.rot
                changed = True
            if self.visible != self.anchorFolder.objctrl.treeNodeObject.visible:
                self.visible = self.anchorFolder.objctrl.treeNodeObject.visible
                changed = True
            return changed
        return False

    def exportSetting(self):
        self.updateSetting()
        ss = {}
        # basic
        ss["text"] = self.text.replace("\n", "\\n").replace("'", "\\'")
        ss["color"] = self.color
        ss["visible"] = self.visible
        ss["infront"] = self.inFront
        ss["font"] = self.fontName
        ss["size"] = self.size
        ss["anchor"] = self.anchorStyle
        ss["alignment"] = self.alignment
        ss["position"] = self.position
        ss["rotation"] = self.rotation
        ss["scale"] = self.scale
        # advanced
        ss["ver"] = self.version
        ss["managed"] = self.managed
        ss["bindcam"] = self.bindCamera
        ss["anime"] = [s.export() for s in self.animeController]

        return ss

    def saveSetting(self):
        if self.valid:
            # build save data
            sstxt = "-vntextdata:" + script2string(self.exportSetting())
            #print sstxt
            ssFld = None
            for cto in self.anchorFolder.objctrl.treeNodeObject.child:
                if cto.textName.startswith("-vntextdata:"):
                    ssFld = HSNeoOCI.create_from_treenode(cto)
                    ssFld.name = sstxt
            if ssFld == None:
                ssFld = HSNeoOCIFolder.add(sstxt)
                ssFld.set_parent(self.anchorFolder)

    def loadSetting(self, setting):
        try:
            if isinstance(setting, dict):
                ss = setting
            elif isinstance(setting, str):
                ss = eval(setting)
            else:
                raise Exception("Unknown setting input value: " + str(setting))
            # basic
            self.text = ss["text"]
            self.size = ss["size"]
            self.visible = bool(ss["visible"])
            self.inFront = bool(ss["infront"])
            self.color = Color(ss["color"][0], ss["color"][1], ss["color"][2], ss["color"][3])
            self.fontName = ss["font"]
            self.anchorStyle = ss["anchor"]
            self.alignment = ss["alignment"]
            self.position = Vector3(ss["position"][0], ss["position"][1], ss["position"][2])
            self.rotation = Vector3(ss["rotation"][0], ss["rotation"][1], ss["rotation"][2])
            self.scale = Vector3(ss["scale"][0], ss["scale"][1], ss["scale"][2])
            # advanced
            self.version = ss["ver"]
            self.managed = ss["managed"]
            self.bindCamera = ss["bindcam"]
            self.animeController = TextAnime.parseSettings(ss["anime"])

            return True
        except:
            traceback.print_exc()
            return False

    @property
    def renderText(self):
        return TextInfo.buildRenderText(self.text, self.alignment)

    def setText(self, text):
        if self.text != text:
            self.text = text
            self.saveSetting()
            if self.meshObj != None:
                self.meshObj.text = self.renderText

    def setVisible(self, visible):
        if self.visible != visible:
            self.visible = visible
            if self.valid:
                self.anchorFolder.objctrl.treeNodeObject.visible = visible
            self.saveSetting()
            if self.meshObj != None:
                self.meshObj.gameObject.SetActive(visible)

    def setPosition(self, pos):
        if self.position != pos:
            self.position = pos
            self.saveSetting()
            if self.valid and self.anchorFolder.pos != pos:
                self.anchorFolder.pos = pos

    def setRotation(self, rot):
        if self.rotation != rot:
            self.rotation = rot
            self.saveSetting()
            if self.valid and self.anchorFolder.rot != rot:
                self.anchorFolder.rot = rot

    def setInFront(self, inFront):
        if self.inFront != inFront:
            self.inFront = inFront
            self.saveSetting()
            if self.meshObj != None:
                meshRender = self.meshObj.GetComponent(MeshRenderer)
                if meshRender != None:
                    if self.inFront or TextManager.font3DMaterial == None:
                        #meshRender.materials = Array[Material]((t.font.material,))
                        meshRender.material = self.meshObj.font.material
                        meshRender.material.color = self.color
                        self.meshObj.color = self.color
                        print "restore infront color",self.color
                    else:
                        meshRender.material = TextManager.font3DMaterial
                        meshRender.material.SetTexture("_MainTex", self.meshObj.font.material.mainTexture)
                        meshRender.material.EnableKeyword("_NORMALMAP")
                        meshRender.material.color = self.color
                        self.meshObj.color = self.color
                        print "restore 3d color",self.color
                else:
                    print "VNText setInFront error: MeshRenderer Missed!?"
                
    def setColor(self, color):
        if self.color != color:
            self.color = color
            self.saveSetting()
            if self.meshObj != None:
                self.meshObj.color = color
                meshRender = self.meshObj.GetComponent(MeshRenderer)
                if meshRender != None:
                    meshRender.material.color = color
                else:
                    print "VNText setColor error: MeshRenderer Missed!?"

    def setFont(self, font):
        if self.fontName != font.name:
            self.fontName = font.name
            self.saveSetting()
            if self.meshObj != None:
                print "set font:", font
                self.meshObj.font = font
                #self.meshObj.font.RequestCharactersInTexture(self.text)
                #meshRender = self.anchorFolder.objctrl.objectItem.GetComponentInChildren(MeshRenderer, True)
                meshRender = self.meshObj.GetComponent(MeshRenderer)
                if meshRender != None:
                    if self.inFront or TextManager.font3DMaterial == None:
                        #meshRender.materials = Array[Material]((font.material,))
                        meshRender.material = font.material
                    else:
                        meshRender.material = TextManager.font3DMaterial
                        meshRender.material.SetTexture("_MainTex", self.meshObj.font.material.mainTexture)
                        meshRender.material.EnableKeyword("_NORMALMAP")
                    meshRender.material.color = self.color
                else:
                    print "VNText setFont error: MeshRenderer Missed!?"
                self.meshObj.color = self.color

    def setSize(self, size, charSizeRate):
        if self.size != size:
            self.size = size
            self.saveSetting()
            if self.meshObj != None:
                self.meshObj.characterSize = self.size * charSizeRate

    def setScale(self, scaleX, scaleY):
        if self.scale.x != scaleX or self.scale.y != scaleY:
            self.scale.Set(scaleX, scaleY, 1)
            self.saveSetting()
            if self.meshObj != None:
                self.meshObj.transform.localScale = Vector3(scaleX, scaleY, 1)

    def setAnchorStyle(self, anStyle):
        if self.anchorStyle != anStyle:
            self.anchorStyle = anStyle
            self.saveSetting()
            if self.meshObj != None:
                self.meshObj.anchor = value_2_enum(TextAnchor, anStyle)

    def setAlignment(self, align):
        if self.alignment != align:
            self.alignment = align
            self.saveSetting()
            if self.meshObj != None:
                if align == 3: align = 2
                if align == 4: align = 0
                self.meshObj.text = self.renderText
                self.meshObj.alignment = value_2_enum(TextAlignment, align)

    def setManaged(self, managed):
        if self.managed != managed:
            self.managed = managed
            self.saveSetting()
            #if self.valid:
            #    if managed:
            #        self.anchorFolder.set_parent(TextManager.getManagerFolder())
            #    else:
            #        self.anchorFolder.set_parent_treenodeobject(None)

    def setID(self, newId):
        if self.id != newId and newId not in TextManager.listAllIds():
            self.id = newId
            if self.valid:
                self.anchorFolder.name = "-vntext:" + newId

    def setBindCamera(self, bindType, camData):
        #if bindType == None:
        #    self.bindCamera = None
        oldFaceCam = self.bindCamera != None and "FaceCam" in self.bindCamera[0]
        newBindSetting = ["",]
        if "FaceCamWOZ" in bindType:
            newBindSetting[0] += "FaceCamWOZ"
        elif "FaceCam" in bindType:
            newBindSetting[0] += "FaceCam"
        if "BindPos" in bindType and camData != None and self.valid:
            newBindSetting[0] += "BindPos"
            posOffset = self.anchorFolder.pos - camData[0]
            newBindSetting.append(posOffset)
        if "BindRot" in bindType and camData != None and self.valid:
            newBindSetting[0] += "BindRot"
            rotOffset = self.anchorFolder.rot - camData[2]
            newBindSetting.append(rotOffset)
        # set
        if len(newBindSetting[0]) > 0:
            self.bindCamera = tuple(newBindSetting)
        else:
            self.bindCamera = None
        newFaceCam = self.bindCamera != None and "FaceCam" in self.bindCamera[0]
        # save
        self.saveSetting()
        # unface cam
        if oldFaceCam and not newFaceCam and self.valid:
            self.anchorFolder.objctrl.objectItem.transform.localRotation = Quaternion.identity

    def cameraWork(self, camData):
        if not self.valid or self.bindCamera == None or not camData:
            return
        if "FaceCam" in self.bindCamera[0]:
            rx = -camData[2].x
            ry = camData[2].y - 180
            rz = self.anchorFolder.objctrl.objectInfo.changeAmount.rot.z if "FaceCamWOZ" in self.bindCamera[0] else -camData[2].z
            #self.anchorFolder.objctrl.objectInfo.changeAmount.rot = Vector3(rx, ry, rz)
            self.anchorFolder.objctrl.objectItem.transform.eulerAngles = Vector3(rx, ry, rz)
            #print "%s camera work: cam rot (%.3f, %.3f, %.3f), text rot (%.3f, %.3f, %.3f)"%(self.id, camData[2].x, camData[2].y, camData[2].z, rx, ry, rz)
        oi = 1
        if "BindPos" in self.bindCamera[0]:
            newPos = camData[0] + tuple3_2_vector3(self.bindCamera[oi])
            self.anchorFolder.objctrl.objectInfo.changeAmount.pos = newPos
            oi += 1
            #print "%s camera work: cam bind pos (%.3f, %.3f, %.3f)"%(self.id, newPos.x, newPos.y, newPos.z)
        if "BindRot" in self.bindCamera[0]:
            newRot = camData[2] + tuple3_2_vector3(self.bindCamera[oi])
            newRot2 = Vector3(-newRot.x, newRot.y, -newRot.z)
            self.anchorFolder.objctrl.objectInfo.changeAmount.rot = newRot2
            oi += 1
            #print "%s camera work: cam bind rot (%.3f, %.3f, %.3f)"%(self.id, newRot.x, newRot.y, newRot.z)

    def setAnime(self, animes):
        self.animeController = animes
        self.saveSetting()
        self.animePlay()

    def animePlay(self):
        for ac in self.animeController:
            ac.play()

    def animeWork(self, game):
        for ac in self.animeController:
            ac.update(game, self)

    def getAnimeByType(self, animeType):
        for ac in self.animeController:
            if isinstance(ac, animeType):
                return ac
        return None

    def __str__(self):
        return "VN TextInfo %s: %s"%(self.id, self.text)

class TextAnime():
    def __init__(self):
        self.type = "unknown"
        self.status = "init"
        self.localTime = 0

    def play(self):
        self.status = "play"
        self.localTime = 0

    def export(self):
        ss = {}
        ss["type"] = self.type
        return ss

    @staticmethod
    def parseSettings(settings):
        #print "start parse anime setting:", settings
        acs = []
        for ss in settings:
            # try TextAnimeOneByOne
            ac = TextAnimeOneByOne.tryParse(ss)
            if ac:
                acs.append(ac)
                continue
        #print "parsed result:", acs
        return acs

    def update(self, game, textInfo):
        pass

class TextAnimeOneByOne(TextAnime):
    def __init__(self):
        self.type = "OneByOne"
        self.status = "init"
        self.localTime = 0
        #
        self.speed = 0.1

    def export(self):
        ss = {}
        ss["type"] = self.type
        ss["speed"] = self.speed
        return ss

    @staticmethod
    def tryParse(setting):
        try:
            if setting["type"] != "OneByOne":
                return None
            ac = TextAnimeOneByOne()
            ac.speed = setting["speed"]
            return ac
        except:
            print "TextAnimeOneByOne parse error:"
            traceback.print_exc()
            return None

    def update(self, game, textInfo):
        if self.status == "play":
            # check
            if not textInfo.valid:
                self.status = "error"
                return
            # update
            from UnityEngine import Time
            self.localTime += Time.deltaTime
            dispCount = int(self.localTime / self.speed + 1)
            textInfo.meshObj.text = TextInfo.buildRenderText(textInfo.text[:dispCount], textInfo.alignment)
            if dispCount >= len(textInfo.renderText):
                #print "TextAnimeOneByOne for %s over"%(textInfo.text)
                self.status = "over"

class TextManager():
    fontList = None
    font3DMaterial = None

    def __init__(self, game):
        self.game = game
        self.managedTexts = []
        self.staticTexts = []

        # font size setting
        if game.isNEOV2:
            self.fontSize = 500
            self.charSizeRate = 0.02
        else:
            self.fontSize = 500
            self.charSizeRate = 0.002

        # load fonts
        self.createDynamicFonts()

        # load texts
        self.reloadTextInfo()

    @staticmethod
    def listAllIds():
        tagflds = HSNeoOCIFolder.find_all_startswith("-vntext:")
        ids = [f.name[8:] for f in tagflds]
        return ids

    @staticmethod
    def getManagerFolder():
        mngFld = HSNeoOCIFolder.find_single_startswith("-vntextmanager:")
        if mngFld == None:
            mngFld = HSNeoOCIFolder.add("-vntextmanager:v1")
            mngFld.set_pos((0, 0, 0))
        return mngFld

    @property
    def managedTextCount(self):
        return len(self.managedTexts)

    @property
    def staticTextCount(self):
        return len(self.staticTexts)

    @property
    def allTextCount(self):
        return self.managedTextCount + self.staticTextCount

    @property
    def font3DMaterialValid(self):
        return (TextManager.font3DMaterial != None) and (not self.game.isPlayHomeStudio)

    def createDynamicFonts(self):
        TextManager.fontList = list(Font.GetOSInstalledFontNames())

        if hasattr(self.game, "vntextDynamicFonts"):
            self.dynamicFonts = self.game.vntextDynamicFonts
            print "VNText Info: Restore dynamic fonts from game."
        elif len(TextManager.fontList) >= 500:
            self.dynamicFonts = None
            print "VNText Warning: %d fonts found in your system, that's too many for Unity to load at same time, font preview disabled."
        else:            
            self.dynamicFonts = {}
            arialLoaded = False
            if "Arial" in TextManager.fontList:
                self.dynamicFonts["Arial"] = Resources.GetBuiltinResource(Font, "Arial.ttf")
                arialLoaded = True
            for fontname in TextManager.fontList:
                if fontname == "Arial" and arialLoaded:
                    continue
                fontnames = Array[String]((fontname, "Arial"))
                self.dynamicFonts[fontname] = Font.CreateDynamicFontFromOSFont(fontnames, 20)
            self.game.vntextDynamicFonts = self.dynamicFonts
            print "VNText Info: %d fonts loaded from your system"%(len(TextManager.fontList))

        if hasattr(self.game, "vntextFont3DMaterial") and self.game.vntextFont3DMaterial != None:
            TextManager.font3DMaterial = self.game.vntextFont3DMaterial
            #print "VNText Info: Restore font 3d material."
        else:
            try:
                from os import path
                abName = path.splitext(__file__)[0] + '.assetbundle'
                assetbundle = AssetBundle.LoadFromFile(abName)
                TextManager.font3DMaterial = self.game.vntextFont3DMaterial = assetbundle.LoadAsset("Font3DMaterial", Material)
                TextManager.font3DMaterial.color = Color.white
                assetbundle.Unload(False)
                #print "VNText Info: Load font 3d material from assetbundle:", TextManager.font3DMaterial
            except:
                traceback.print_exc()
                TextManager.font3DMaterial = self.game.vntextFont3DMaterial = None
                print "VNText Error: Fail to load font 3d material from assetbundle, all text will be render in front"

    def checkAndGetFont(self, fontName):
        if self.dynamicFonts:
            if fontName in self.dynamicFonts:
                return self.dynamicFonts[fontName]
            elif "MS Gothic" in self.dynamicFonts:
                print "VNText Warning: Font <%s> not found on your system, use <MS Gothic> instead!"%fontName
                return self.dynamicFonts["MS Gothic"]
            else:
                print "VNText Warning: Font <%s> not found on your system, use <Arial> instead!"%fontName
                return self.dynamicFonts["Arial"]
        else:
            try:
                font = Font.CreateDynamicFontFromOSFont(fontName, 20)
                if font == None: raise Exception()
                return font
            except:
                print "VNText Warning: Font <%s> not found on your system, use <Arial> instead!"%fontName
                return Font.CreateDynamicFontFromOSFont("Arial", 20)

    def reloadTextInfo(self):
        self.managedTexts = []
        self.staticTexts = []
        self.suspendHousekeep = True

        tagflds = HSNeoOCIFolder.find_all_startswith("-vntext:")
        toload = []
        toloadids = []
        for fld in tagflds:
            ti = TextInfo.buildFromFolder(fld)
            if ti:
                if ti.id in toloadids:
                    nid = ti.id
                    no = len(toloadids) + 1
                    while nid in toloadids or nid in TextManager.listAllIds():
                        nid = "vntxt%d"%no
                        no += 1
                    print "Found VNText: %s->%s in folder objctrl %s"%(ti.id, nid, ti.anchorFolder.objctrl)
                    ti.setID(nid)
                else:
                    print "Found VNText: %s in folder objctrl %s"%(ti.id, ti.anchorFolder.objctrl)
                toload.append(ti)
                toloadids.append(ti.id)
        if len(toload) > 0:
            self.createText(toload)
        else:
            self.suspendHousekeep = False

    def getCurrentSelected(self):
        sels = []
        for tno in self.game.studio.treeNodeCtrl.selectNodes:
            try:
                sel = HSNeoOCI.create_from_treenode(tno)
                if isinstance(sel, HSNeoOCIFolder):
                    if sel.name.startswith("-vntext:"):
                        tid = sel.name[8:]
                        sels.append(self.getTextInfo(tid))
            except:
                pass
        return [None] if len(sels) == 0 else sels
    
    def getTextInfo(self, tid):
        self.checkInfo()
        for ti in self.managedTexts:
            if ti.id == tid:
                return ti
        for ti in self.staticTexts:
            if ti.id == tid:
                return ti
        return None

    def setManaged(self, textInfo, manage):
        textInfo.setManaged(manage)
        if manage:
            if textInfo in self.staticTexts:
                self.staticTexts.remove(textInfo)
            else:
                print "VNText Error: %d is not in static list"%textInfo.id
            if textInfo not in self.managedTexts:
                self.managedTexts.append(textInfo)
            else:
                print "VNText Error: %d is already in managed list"%textInfo.id
        else:
            if textInfo in self.managedTexts:
                self.managedTexts.remove(textInfo)
            else:
                print "VNText Error: %d is not in managed list"%textInfo.id
            if textInfo not in self.staticTexts:
                self.staticTexts.append(textInfo)
            else:
                print "VNText Error: %d is already in static list"%textInfo.id

    def checkInfo(self):
        for ti in self.managedTexts:
            if not ti.valid:
                self.managedTexts.remove(ti)
        for ti in self.staticTexts:
            if not ti.valid:
                self.staticTexts.remove(ti)

    def newTextId(self):
        extids = TextManager.listAllIds()
        no = len(extids) + 1
        while True:
            nid = "vntxt%d"%no
            if nid not in extids:
                return nid
            no += 1

    def newTextInfo(self):
        nti = TextInfo()
        nti.id = self.newTextId()
        nti.text = "new text"
        nti.inFront = not self.font3DMaterialValid
        nti.managed = True
        if self.game.studio.optionSystem.initialPosition == 1:
            nti.position = self.game.studio.cameraCtrl.cameraData.pos
        return nti

    def housekeep(self):
        if self.suspendHousekeep:
            return

        def hk(ti):
            # visible
            ti.setVisible(ti.anchorFolder.objctrl.treeNodeObject.visible)
            # position
            ti.setPosition(ti.anchorFolder.pos)
            # rotation
            ti.setRotation(ti.anchorFolder.rot)

        for ti in self.managedTexts:
            if not ti.valid:
                self.managedTexts.remove(ti)
            else:
                hk(ti)
        for ti in self.staticTexts:
            if not ti.valid:
                self.staticTexts.remove(ti)
            else:
                hk(ti)

    def cameraWork(self, game):
        cam_data = get_camera_data(game)
        for ti in self.managedTexts:
            if ti.bindCamera:
                ti.cameraWork(cam_data)
        for ti in self.staticTexts:
            if ti.bindCamera:
                ti.cameraWork(cam_data)

    def animeUpdate(self, game):
        for ti in self.managedTexts:
            ti.animeWork(game)
        for ti in self.staticTexts:
            ti.animeWork(game)

    def createText(self, textInfo = None):
        if textInfo == None:
            textInfos = [self.newTextInfo(),]
            self.selectAfterCreate = True
        elif not isinstance(textInfo, list):
            textInfos = [textInfo,]
            self.selectAfterCreate = True
        else:
            textInfos = textInfo
            self.selectAfterCreate = False
        self.game.updFuncParam = textInfos
        self.game.updFunc = self._createTextMesh

    def _createTextMesh(self, textInfos):
        """:type textInfo:TextInfo"""
        for textInfo in textInfos:
            try:
                # create anchor folder
                tagid = "-vntext:" + textInfo.id
                txtbase = HSNeoOCIFolder.find_single(tagid)
                if txtbase == None:
                    txtbase = HSNeoOCIFolder.add(tagid)
                    newbase = True
                else:
                    newbase = False
                #if textInfo.managed:
                #    txtbase.set_parent(TextManager.getManagerFolder())

                # create textmesh
                txtbase.objctrl.objectItem.layer = 10
                if not newbase and textInfo.meshObj == None:
                    emo = txtbase.objctrl.objectItem.GetComponentInChildren(TextMesh, True)
                    if emo and emo.name == "VNTextObj":
                        textInfo.meshObj = emo
                if newbase or textInfo.meshObj == None:
                    # create TextMesh and setup
                    go = GameObject()
                    go.transform.SetParent(txtbase.objctrl.objectItem.transform)
                    go.layer = 10
                    go.transform.localPosition = Vector3.zero
                    go.transform.localRotation = Quaternion.Euler(0, 180, 0)
                    
                    t = go.AddComponent(TextMesh)
                    textInfo.meshObj = t
                    t.name = "VNTextObj"
                    t.fontSize = self.fontSize
                else:
                    t = textInfo.meshObj

                # text
                #t.text = textInfo.renderText
                t.text = ""

                # font and color
                t.font = self.checkAndGetFont(textInfo.fontName)
                #t.font.RequestCharactersInTexture(textInfo.text)
                #meshRender = txtbase.objctrl.objectItem.GetComponentInChildren(MeshRenderer, True)
                meshRender = t.GetComponent(MeshRenderer)
                if meshRender != None:
                    if textInfo.inFront or not self.font3DMaterialValid:
                        meshRender.material = t.font.material
                    else:
                        meshRender.material = TextManager.font3DMaterial
                        meshRender.material.SetTexture("_MainTex", t.font.material.mainTexture)
                        meshRender.material.EnableKeyword("_NORMALMAP")
                        meshRender.material.color = textInfo.color
                t.color = textInfo.color

                # other properties
                t.characterSize = textInfo.size * self.charSizeRate
                t.transform.localScale = textInfo.scale
                t.anchor = value_2_enum(TextAnchor, textInfo.anchorStyle)
                if textInfo.alignment == 3:
                    align = 2
                elif textInfo.alignment == 4:
                    align = 0
                else:
                    align = textInfo.alignment
                t.alignment = value_2_enum(TextAlignment, align)
                txtbase.objctrl.treeNodeObject.visible = textInfo.visible
                t.gameObject.SetActive(textInfo.visible)

                # store/restore position, rotation
                #if newbase:
                #    textInfo.position = txtbase.pos
                #    textInfo.rotation = txtbase.rot

                # store info back to manager
                textInfo.anchorFolder = txtbase                
                if textInfo.managed:
                    self.managedTexts.append(textInfo)
                else:
                    self.staticTexts.append(textInfo)

                #print "%s Text <%s>: %s"%(("Created" if newbase else "Restored"), textInfo.id, textInfo.text)
            except:
                print "VNText error:"
                traceback.print_exc()

        # do select
        if self.selectAfterCreate:
            textInfos[0].select()

        # plan for next update
        self.game.updFunc = self._updateTextMesh

    def _updateTextMesh(self, textInfos):
        for textInfo in textInfos:
            # position, rotation
            textInfo.anchorFolder.objctrl.objectInfo.changeAmount.pos = textInfo.position
            textInfo.anchorFolder.objctrl.objectInfo.changeAmount.rot = textInfo.rotation

            # set text if no one-by-one anime
            if textInfo.getAnimeByType(TextAnimeOneByOne) == None:
                textInfo.meshObj.text = textInfo.renderText

            # start anime
            textInfo.animePlay()
            
            # save setting
            textInfo.saveSetting()

        # create all done
        self.suspendHousekeep = False

    def deleteText(self, textInfo):
        # delete one
        if textInfo.managed:
            self.managedTexts.remove(textInfo)
        else:
            self.staticTexts.remove(textInfo)
        textInfo.delete()
    
    def deleteAll(self, managed = True, static = True):
        # managed
        if managed:
            for ti in self.managedTexts:
                ti.delete()
            self.managedTexts = []
        # static
        if static:
            for ti in self.staticTexts:
                ti.delete()
            self.staticTexts = []

    def exportDynamicTextSetting(self):
        ds = {}
        for ti in self.managedTexts:
            ds[ti.id] = ti.exportSetting()
        return script2string(ds)

    def importDynamicTextSetting(self, settingScript):
        try:
            self.suspendHousekeep = True
            ss = eval(settingScript)

            toupd = []
            toupd_id = []
            todel = []
            for ti in self.managedTexts:
                if ti.id in ss.keys():
                    ti.loadSetting(ss[ti.id])
                    toupd.append(ti)
                    toupd_id.append(ti.id)
                else:
                    todel.append(ti)

            tonew = [s for s in ss.keys() if s not in toupd_id]
            for nid in tonew:
                ti = TextInfo()
                ti.id = nid
                ti.loadSetting(ss[nid])
                toupd.append(ti)

            #print "Import Dynamic Text Setting"
            #print "  New    :", tonew
            #print "  Update :", toupd_id
            #print "  Delete :", [s.id for s in todel]
            #for ti in toupd:
            #    print "  upd: %s: %s"%(ti.id, ti.text)

            # do delete
            for ti in todel:
                self.deleteText(ti)
            # clear managed texts
            self.managedTexts = []
            # update
            self.createText(toupd)

        except:
            self.suspendHousekeep = False
            traceback.print_exc()
