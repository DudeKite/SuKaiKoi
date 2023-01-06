"""
SceneSaveState VNSceneScript extension file

1.0

1.1
- name can be used - set name in wizard, target as {name} in cmds
- cam calculated as scene*100+cam
- Adv Options 1: camera anim, hide, hideui, timernext

1.2
- Wizard: support 'next' keyword for addbtn/addbtnrnd cmd
- Wizard: support runms command, choice and name check for runms/addbtnms 
- Wizard: VNFrame ext support track system info

1.3
- Wizard: support synch and synchr command
- some bug fix in wizard

1.4
- Add Adv Options 2: setting for run vnss ext cmd on camera change.
  defualt behavious can be set in scenesavestate_config.ini
- UI renewed, vnss ext cmd can be run by click ">" button in cmds mode.
  defualt UI mode can be set in scenesavestate_config.ini
- New vnss ext cmd to support obj camera: objcam from vnscenescriptext_objcam10
- vnframe ext up to vnscenescriptext_vnframe12, vnanime ext up to vnscenescriptext_vnanime10
- support flipsync on export VNSS by default

1.5
- Detect necessary ext on export, support vnframe12,vnanime10,vntext10,objcam10,blackrain10,gameutil10
- VNSS fast export mode: try update folders instead of delete and re-create all. EXPERIMENTAL, can be turn off in ini.
- Skip export 'txtf' cmd when detect 'txtfv' or 'printvar' cmd (blackrain)
- fix a bug param data linked after copy cam, back button can cancel param data change now.
- Wizard: support 'f_height'/'f_breast'
- Wizard: support some of the Blackrain commands
- Wizard: support VNText commands
- Wizard: support GameUtil commands
- Wizard: VNFrame ext support manual mode

"""
import scenesavestate
from scenesavestate import *
from vngameengine import *
from Studio import OCIFolder, OCIChar, Studio, OCIItem, Studio
from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Vector2, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Color, Time
from System import String, Array
import os
from System import Single, Byte
import copy
import sys
from libjsoncoder import *
import traceback


# export to VNSceneScript function

def add_folder_if_not_exists(foldertxt, folderfind, parentifcreate, overwrite=False):
    from scenesavestate import folder_add_child

    vnext = HSNeoOCIFolder.find_single_startswith(folderfind)
    if vnext:
        if overwrite:
            vnext.name = foldertxt
        return vnext
    else:
        return folder_add_child(parentifcreate, foldertxt)

def add_folder_if_not_exists_dup(foldertxt, parentifcreate):
    return add_folder_if_not_exists(foldertxt,foldertxt,parentifcreate)

def exportToVNSS(self,params): # params will be needed later
    from scenesavestate import folder_add_child
    import vnframe
    import time

    self = self
    """:type self:SceneConsole"""
    start = time.clock()

    # arCamMoveStyle = (
    #     "linear", "slow-fast", "fast-slow", "slow-fast3", "fast-slow3", "slow-fast4", "fast-slow4")

    # ---------------- making headers ----------------
    vnss = HSNeoOCIFolder.find_single_startswith(":vnscenescript:")

    calcMaxFrame = str((len(self.block) + 1) * 100)
    # calcMaxFrame = 100000

    if vnss == None:
        vnss = HSNeoOCIFolder.add(":vnscenescript:v30:" + calcMaxFrame)
        #folder_add_child(vnss, ":useext:vnframe12")
        #folder_add_child(vnss, ":a:i:f_stinit")
        # folder_add_child(vnss, ":acode")
    else:
        # updating max frame
        vnss.name = ":vnscenescript:v30:" + calcMaxFrame
        #vnext = HSNeoOCIFolder.find_single_startswith(":useext:vnframe")
        #if vnext:
        #    vnext.name = ":useext:vnframe12"

    # ----------------- add ext support if needed -------
    extVNFrame = False
    extVNAnime = False
    extVNText = False
    extObjCam = False
    extBlackRain = False
    extGameUtil = False
    for i in range(len(self.block)):
        scene = self.block[i]
        for j in range(len(scene.cams)):
            cam = scene.cams[j]
            addparams = cam[4]
            if "addvncmds" in addparams:
                addvncmds = addparams["addvncmds"]
                acmds = analysis_vnss_cmd(addvncmds)
                for acmd in acmds:
                    if not extVNFrame and acmd["catelog"] == "vnframe":
                        extVNFrame = True
                    if not extVNAnime and acmd["catelog"] == "vnanime":
                        extVNAnime = True
                    if not extVNText and acmd["catelog"] == "vntext":
                        extVNText = True
                    if not extObjCam and acmd["catelog"] == "objcam":
                        extObjCam = True
                    if not extBlackRain and acmd["catelog"] == "blackrain":
                        extBlackRain = True
                    if not extGameUtil and acmd["catelog"] == "gameutil":
                        extGameUtil = True
    #print "ext vnframe =", extVNFrame
    #print "ext vnanime =", extVNAnime
    #print "ext vntext =", extVNText
    #print "ext objcam =", extObjCam
    #print "ext blackrain =", extBlackRain
    #print "ext gameutil =", extGameUtil

    # add vnframe, must include for scene change
    if extVNFrame or True:
        add_folder_if_not_exists(":useext:vnframe12", ":useext:vnframe", vnss)
        add_folder_if_not_exists_dup(":a:i:f_stinit", vnss)

    # add vnanime
    if extVNAnime:
        add_folder_if_not_exists(":useext:vnanime10", ":useext:vnanime", vnss)
        add_folder_if_not_exists_dup(":a:i:f_clipinit", vnss)

    # add vntext
    if extVNText:
        add_folder_if_not_exists(":useext:vntext10", ":useext:vntext", vnss)

    # add object camera support for KK and AI
    if extObjCam and (self.game.isCharaStudio or self.game.isNEOV2):
        add_folder_if_not_exists(":useext:objcam10", ":useext:objcam", vnss)

    # add blackrain
    if extBlackRain:
        add_folder_if_not_exists(":useext:blackrain10", ":useext:blackrain", vnss)

    # add gameutil
    if extGameUtil:
        add_folder_if_not_exists(":useext:gameutil10", ":useext:gameutil", vnss)        


    # ------------ calculating list of names --------------
    dictNames = {}
    for i in range(len(self.block)):
        scene = self.block[i]

        for j in range(len(scene.cams)):
            cam = scene.cams[j]
            addparams = cam[4]

            if addparams["addparam"]:
                if "addprops" in addparams:
                    addprops = addparams["addprops"]
                    if "a1" in addprops and addprops["a1"]:
                        if "name" in addprops["a1o"] and addprops["a1o"]["name"] != "":

                            dictNames[addprops["a1o"]["name"]] = str((i+1)*100+j)
    #print "DictNames: ", dictNames

    # ---------------- actual render ------------------------
    nextfData = []
    acodeData = {}
    nextfstr = None
    totalscene = 0
    totalcam = 0
    latestRenderScene = None  # this we save latest VN render scene - to calc difference
    # adding new elems
    for i in range(len(self.block)):
        scene = self.block[i]
        """:type scene:Scene"""

        # only process scene if 1 cam is VN cam - other, skip
        cam = scene.cams[0]
        addparams = cam[4]
        if addparams["addparam"]:  # only process if 1 cam is VN cam
            totalscene += 1
            #fld_next = folder_add_child(fld_acode, str((i + 1) * 100))
            nextfstr = "nextf:" + str((i + 1) * 100)
            nextfData.append(nextfstr)
            acodeData[nextfstr] = []

            # making actions for switch to scene
            for actid in scene.actors:
                # calc optimized status
                optstatus = scene.actors[actid]

                # delete cloth status if set in advance - by @countd360
                if actid != "sys":
                    try:
                        _sc = self
                        if _sc and hasattr(_sc, "skipClothesChanges") and _sc.skipClothesChanges:
                            optstatus = dict(optstatus)  # make a copy
                            del optstatus["acc_all"]
                            del optstatus["cloth_all"]
                            if "cloth_type" in optstatus:
                                del optstatus["cloth_type"]
                    except Exception, e:
                        print "Error in skip cloth process when export to VNSceneScript:", e

                isRenderOptimized = False  # we need to move between scenes freely since 5.0 and adv VN cmds
                if latestRenderScene and isRenderOptimized:
                    optstatus = get_status_diff_optimized(latestRenderScene[actid], scene.actors[actid])

                if actid != "sys":
                    action = vnframe.script2string(optstatus)
                    fulltext = "f_actm:" + actid + "::" + action
                else:
                    action = json_encode(optstatus)
                    fulltext = "f_actm_j:" + actid + "::" + action
                #folder_add_child(fld_next, fulltext)
                acodeData[nextfstr].append(fulltext)

            latestRenderScene = scene.actors

            for propid in scene.props:
                action = vnframe.script2string(scene.props[propid])
                fulltext = "f_actm:" + propid + "::" + action
                #folder_add_child(fld_next, fulltext)
                acodeData[nextfstr].append(fulltext)

            # make actions for switch to cam
            for j in range(len(scene.cams)):
                cam = scene.cams[j]
                addparams = cam[4]
                if addparams["addparam"]:
                    totalcam += 1

                    # trick to render next
                    #if fld_next == None:
                    #    fld_next = folder_add_child(fld_acode, "nextf:" + str((i + 1) * 100+j))
                    if nextfstr == None:
                        nextfstr = "nextf:" + str((i + 1) * 100+j)
                        nextfData.append(nextfstr)
                        acodeData[nextfstr] = []


                    # calc cam str:
                    scamstr = "%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.3f,%0.2f" % (
                        cam[0].x, cam[0].y, cam[0].z, cam[1].x, cam[1].y, cam[1].z, cam[2].x, cam[2].y, cam[2].z,
                        cam[3])

                    isCamAddRendered = False
                    isTextOverwrited = False

                    # calc wizard props
                    if addparams["addparam"]:
                        if "addprops" in addparams:
                            addprops = addparams["addprops"]
                            if "a1o" in addprops:
                                a1o = addprops["a1o"]
                                if "isTime" in a1o and a1o["isTime"]:
                                    ttime = a1o["time"]
                                    if a1o["isTAnimCam"]:
                                        cmd = "camoanim3:"+scamstr+":"+ttime+":"+a1o["tacStyle"]
                                        cmd += ":"+a1o["tacZOut"]+":"+a1o["tacRotX"]+":"+a1o["tacRotZ"]
                                        isCamAddRendered = True
                                        #folder_add_child(fld_next, cmd)
                                        acodeData[nextfstr].append(cmd)
                                    if a1o["isTHideUI"]:
                                        cmd = "hideui:" + ttime
                                        #folder_add_child(fld_next, cmd)
                                        acodeData[nextfstr].append(cmd)
                                    if a1o["isTTimerNext"]:
                                        cmd = "timernext:" + str(float(ttime)+0.2) # slightly after
                                        #folder_add_child(fld_next, cmd)
                                        acodeData[nextfstr].append(cmd)

                                if a1o["keepcam"]:
                                    # keeping cam
                                    isCamAddRendered = True

                    # calc and add additional commands

                    if "addvncmds" in addparams:
                        addvncmds = addparams["addvncmds"]

                        # replacing names
                        for key in dictNames:
                            addvncmds = addvncmds.replace("{{%s}}" % key, dictNames[key]) # old version - {{name}}
                            addvncmds = addvncmds.replace("{%s}" % key, dictNames[key])

                        # is cam set in addvncmds? old version vnss 'camo:{camstr}'
                        if "{camstr}" in addvncmds:
                            addvncmds = addvncmds.replace("{camstr}", scamstr)
                            isCamAddRendered = True

                        # save all vnss cmd
                        acmds = analysis_vnss_cmd(addvncmds)
                        for acmd in acmds:
                            if not acmd["error"]:
                                #folder_add_child(fld_next, acmd["org"])
                                acodeData[nextfstr].append(acmd["org"])
                            else:
                                print "Fail to export vnss cmd in scene %d cam %d:"%(i,j)
                                print "  error  :", acmd["desp"]
                                print "  org cmd:", acmd["org"]
                            if acmd["action"] == "objcam" and len(acmd["ap1"]) > 0:
                                isCamAddRendered = True
                            if acmd["action"] == "txtfv" or acmd["action"] == "printvar":
                                isTextOverwrited = True

                    # making text action
                    if not isTextOverwrited:
                        act = "txtf:" + addparams["whosay"] + "::" + addparams["whatsay"]
                        #folder_add_child(fld_next, act)
                        acodeData[nextfstr].append(act)

                    # making cam action
                    if not isCamAddRendered:
                        #folder_add_child(fld_next, "camo:" + scamstr)
                        acodeData[nextfstr].append("camo:" + scamstr)

                    #fld_next = None
                    nextfstr = None

    # tricky making special state to end - not needed
    # fldlast = folder_add_child(fld_acode, "nextf:100000")
    # folder_add_child(fldlast, "nextstate:"+calcMaxFrame)
    # folder_add_child(fldlast, "timernext:0.1")


    # ---------------- export to acode folder ------------------------
    fld_acode = HSNeoOCIFolder.find_single(":acode")
    if fld_acode == None:
        fld_acode = folder_add_child(vnss, ":acode")

    if scenesavestate.is_ini_value_true("VnssFastExport"):
        # new fashion, skip same folder and reuse old folder
        addCount = 0
        updCount = 0
        delCount = 0
        tno_acode = fld_acode.treeNodeObject
        for nextfi in range(len(nextfData)):
            # process nextf folder
            nextf = nextfData[nextfi]
            if nextfi < tno_acode.childCount:
                tno_nextf = tno_acode.child[nextfi]
                fld_next = HSNeoOCIFolder.create_from_treenode(tno_nextf)
                if fld_next.name != nextf:
                    updCount += 1
                    #print "update nextf folder: %s -> %s"%(fld_next.name, nextf)
                    fld_next.name = nextf
            else:
                addCount += 1
                #print "add nextf folder: %s"%(nextf)
                fld_next = folder_add_child(fld_acode, nextf)
                tno_nextf = fld_next.treeNodeObject
            
            # process code folder under nextf folder
            for codei in range(len(acodeData[nextf])):
                code = acodeData[nextf][codei]
                if codei < tno_nextf.childCount:
                    tno_code = tno_nextf.child[codei]
                    if tno_code.textName != code:
                        updCount += 1
                        #print "update code folder: %s -> %s"%(tno_code.textName, code)
                        fld_code = HSNeoOCIFolder.create_from_treenode(tno_code)
                        fld_code.name = code
                else:
                    addCount += 1
                    #print "add code folder: %s"%(code)
                    fld_code = folder_add_child(fld_next, code)

            # remove unused code folder
            while len(acodeData[nextf]) < tno_nextf.childCount:
                delCount += 1
                #print "remove code folder: %s"%(tno_nextf.child[len(acodeData[nextf])].textName)
                self.game.studio.treeNodeCtrl.DeleteNode(tno_nextf.child[len(acodeData[nextf])])

        # remove unused nextf folder
        while len(nextfData) < tno_acode.childCount:
            delCount += 1
            #print "remove nextf folder: %s"%(tno_acode.child[len(nextfData)].textName)
            self.game.studio.treeNodeCtrl.DeleteNode(tno_acode.child[len(nextfData)])
        
        print "Vnss fast export mode: %d folder added, %d folder updated, %d folder deleted."%(addCount, updCount, delCount)

    else:
        # old fashion, delete all and rebuild
        fld_acode.delete_all_children()
        for nextf in nextfData:
            fld_next = folder_add_child(fld_acode, nextf)
            for code in acodeData[nextf]:
                folder_add_child(fld_next, code)

    # ---------------- DONE ------------------------
    end = time.clock()
    print "VNSS Export Done in %.3f sec, totally %d scenes and %d cams."%(end - start, totalscene, totalcam)

def runAdvVNSS(self, addata):
    # run Adv VNSS
    # pick adv param 2 option

    isallrun = scenesavestate.is_ini_value_true("EnableAutorunVnssCmdInEditor")
    if not isallrun:
        return

    runvnframe = scenesavestate.is_ini_value_true("RunVNFrameExtDefault")
    runvnanime = scenesavestate.is_ini_value_true("RunVNAnimeExtDefault")
    runvntext = scenesavestate.is_ini_value_true("RunVNTextExtDefault")
    runobjcam = scenesavestate.is_ini_value_true("RunObjCamExtDefault")
    keepCamera = False
    try:
        # check option
        if "addprops" in addata:
            addprops = addata["addprops"]
            if ("a1" in addprops) and addprops["a1"]:
                a1o = addprops["a1o"]
                if "keepcam" in a1o:
                    keepCamera = a1o["keepcam"]
                    #print "found a1:keepcam, keep camera = %s"%keepCamera
            if ("a2" in addprops) and addprops["a2"]:
                a2o = addprops["a2o"]
                if "run-vnframe-ext" in a2o:
                    runvnframe = a2o["run-vnframe-ext"]
                    #print "found a2:run-vnframe-ext, run vnframe ext = %s"%runvnframe
                if "run-vnanime-ext" in a2o:
                    runvnanime = a2o["run-vnanime-ext"]
                    #print "found a2:run-vnanime-ext, run vnanime ext = %s"%runvnanime
                if "run-vntext-ext" in a2o:
                    runvntext = a2o["run-vntext-ext"]
                    #print "found a2:run-vntext-ext, run vntext ext = %s"%runvntext
                if "run-objcam-ext" in a2o:
                    runobjcam = a2o["run-objcam-ext"]
                    #print "found a2:run-objcam-ext, run objcam ext = %s"%runobjcam
        # prepare vncmds
        if "addvncmds" in addata:
            vncmds = analysis_vnss_cmd(addata["addvncmds"])
        else:
            vncmds = ()
    except Exception, e:
        print "Fail to parse camera addate:", e
        return False

    # run vnss command
    for vncmd in vncmds:
        if runvnframe and vncmd["catelog"] == "vnframe":
            #print "Run vnframe-ext:", vncmd["org"]
            runVNSSExtCmd(self.game, vncmd)
        if runvnanime and vncmd["catelog"] == "vnanime":
            #print "Run vnanime-ext:", vncmd["org"]
            runVNSSExtCmd(self.game, vncmd)
        if runvntext and vncmd["catelog"] == "vntext":
            #print "Run vntext-ext:", vncmd["org"]
            runVNSSExtCmd(self.game, vncmd)
        if runobjcam and vncmd["catelog"] == "objcam":
            #print "Run objcam-ext:", vncmd["org"]
            runVNSSExtCmd(self.game, vncmd)
            if vncmd["action"] == "objcam" and len(vncmd["ap1"]) > 0:
                keepCamera = True

    return keepCamera

# render wizard
tablePadding = 20
btnBigHeight = 40

def render_wizard_ui(self):
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""

    if not hasattr(self, "vnss_wizard_ui_mode"):
        self.vnss_wizard_ui_mode = "main"

    if self.vnss_wizard_ui_mode == "main":
        render_wizard_main(self)
    elif self.vnss_wizard_ui_mode == "vntext":
        render_vntext_editor(self)
    elif self.vnss_wizard_ui_mode == "vnframe_manual":
        render_vnframe_manual(self)
    else:
        print "Unknown vnss_wizard_ui_mode:", self.vnss_wizard_ui_mode
        self.vnss_wizard_ui_mode = "main"

# --------- main --------------------
def render_wizard_main(self):
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""

    if not hasattr(self, "vnss_wizard_ui_scroll"):
        self.vnss_wizard_ui_scroll = Vector2.zero
    _sc.vnss_wizard_ui_scroll = GUILayout.BeginScrollView(_sc.vnss_wizard_ui_scroll)

    # Title
    GUILayout.BeginHorizontal()
    GUILayout.FlexibleSpace()
    GUILayout.Label("Advanced properties for cam for VNSceneScript")
    GUILayout.FlexibleSpace()
    GUILayout.EndHorizontal()
    GUILayout.Space(15)

    # vnss block
    GUILayout.BeginHorizontal()
    GUILayout.Space(tablePadding)
    GUILayout.BeginVertical()
    # who say line
    GUILayout.BeginHorizontal()
    GUILayout.Label("Who say:", GUILayout.Width(85))
    _sc.cam_whosay = GUILayout.TextField(_sc.cam_whosay, GUILayout.Width(210))
    if GUILayout.Button("<", GUILayout.Width(20)):
        _sc.cam_whosay = _sc.get_next_speaker(_sc.cam_whosay, False)
    if GUILayout.Button(">", GUILayout.Width(20)):
        _sc.cam_whosay = _sc.get_next_speaker(_sc.cam_whosay, True)
    GUILayout.EndHorizontal()
    # what say line
    GUILayout.BeginHorizontal()
    GUILayout.BeginVertical(GUILayout.Width(85))
    GUILayout.Label("What say:", GUILayout.Width(85))
    if GUILayout.Button("clear", GUILayout.Width(60)):
        _sc.cam_whatsay = ""
    GUILayout.EndVertical()
    _sc.cam_whatsay = GUILayout.TextArea(_sc.cam_whatsay, GUILayout.Height(54))
    GUILayout.EndHorizontal()
    # VNSS line
    GUILayout.Space(5)
    GUILayout.BeginHorizontal()
    if not hasattr(_sc, "wiz_view_mode"):
        _sc.wiz_view_mode = "<color=#00ffff>cmds</color>" if scenesavestate.is_ini_value_true("VnssViewCmdModeDefault") else "text"
        #_sc.wiz_cmd_view_sclpos = Vector2.zero
    GUILayout.BeginVertical(GUILayout.Width(85))
    GUILayout.Label("VNSS cmds:", GUILayout.Width(85))
    if GUILayout.Button("clear", GUILayout.Width(60)):
        _sc.cam_addvncmds = ""
    if GUILayout.Button(_sc.wiz_view_mode, GUILayout.Width(60)):
        if _sc.wiz_view_mode == "text":
            _sc.wiz_view_mode = "<color=#00ffff>cmds</color>"
        else:
            _sc.wiz_view_mode = "text"
    GUILayout.EndVertical()
    if _sc.wiz_view_mode == "text":
        _sc.cam_addvncmds = GUILayout.TextArea(_sc.cam_addvncmds, GUILayout.Height(80))
    else:
        #_sc.wiz_cmd_view_sclpos = GUILayout.BeginScrollView(_sc.wiz_cmd_view_sclpos, GUILayout.Height(80))
        GUILayout.BeginVertical()
        acmds = analysis_vnss_cmd(_sc.cam_addvncmds)
        for acmd in acmds:
            GUILayout.BeginHorizontal()
            if not acmd["error"]:
                GUILayout.Label("<color=#00ffff>" + acmd["desp"] + "</color>")
            else:
                GUILayout.Label("<color=#ff0000>" + acmd["desp"] + "</color>")
            GUILayout.FlexibleSpace()
            if not acmd["error"] and acmd["catelog"] == "vntext" and GUILayout.Button("<color=#00ffff>..</color>", GUILayout.Width(20)):
                # edit vntext
                self.vnss_wizard_ui_mode = "vntext"
            if not acmd["error"] and (acmd["action"] == "f_act" or acmd["action"] == "f_anime") and GUILayout.Button("<color=#00ffff>..</color>", GUILayout.Width(20)):
                # edit vnframe script
                vnframe_manual_start(self, acmd)
            if not acmd["error"] and acmd["runable"] and GUILayout.Button("<color=#00ffff>"+u'\u25b6'+"</color>", GUILayout.Width(20)):
                # run current vnss cmd
                runVNSSExtCmd(self.game, acmd)
            if GUILayout.Button("<color=#ff0000>X</color>", GUILayout.Width(20)):
                # remove current vnss cmd
                acmds.remove(acmd)
                _sc.cam_addvncmds = "\n".join((c["org"] for c in acmds))
            GUILayout.EndHorizontal()
        if len(acmds) == 0:
            GUILayout.Label("<color=#00ffff>[NONE]</color>")
        #GUILayout.EndScrollView()
        GUILayout.EndVertical()
    GUILayout.EndHorizontal()

    # VNSS wizard
    GUILayout.Space(5)
    render_vnss_wizard(self)

    GUILayout.EndVertical()

    GUILayout.Space(tablePadding)
    GUILayout.EndHorizontal()

    GUILayout.Space(20)

    # adv params 1
    GUILayout.BeginHorizontal()
    GUILayout.Space(tablePadding)

    GUILayout.BeginVertical()

    # build a local copy 
    if not hasattr(self, "wiz_tempProps"):
        camera_data = self.block[self.cur_index].cams[self.cur_cam]
        if len(camera_data) > 4:
            addata = camera_data[4]
            self.wiz_tempProps = copy.deepcopy(addata["addprops"])
        else:
            self.wiz_tempProps = {"a1": False, "a2": False}
    tempProps = self.wiz_tempProps

    tempProps["a1"] = GUILayout.Toggle(tempProps["a1"], "Advanced params 1")
    if tempProps["a1"]:
        if "a1o" in tempProps:
            adv_update(tempProps["a1o"], adv1_def_values())
        else:
            tempProps["a1o"] = adv1_def_values()
        GUILayout.Space(5)
        render_wizard_adv1(self, tempProps)
    else:
        if "a1o" in tempProps:
            del tempProps["a1o"]

    GUILayout.Space(10)

    tempProps["a2"] = GUILayout.Toggle(tempProps["a2"], "Advanced params 2")
    if tempProps["a2"]:
        if "a2o" in tempProps:
            adv_update(tempProps["a2o"], adv2_def_values())
        else:
            tempProps["a2o"] = adv2_def_values()
        GUILayout.Space(5)
        render_wizard_adv2(self, tempProps)
    else:
        if "a2o" in tempProps:
            del tempProps["a2o"]

    GUILayout.EndVertical()

    GUILayout.Space(tablePadding)
    GUILayout.EndHorizontal()

    GUILayout.Space(20)

    # save and exit
    GUILayout.BeginHorizontal()
    GUILayout.Space(tablePadding)
    if GUILayout.Button("Save cam+params and return to main", GUILayout.Height(btnBigHeight)):
        del self.wiz_step
        del self.wiz_tempProps
        self.cam_addprops = tempProps
        _sc.changeSceneCam("upd")
        _sc.subwinindex = 0
    if GUILayout.Button("Back", GUILayout.Height(btnBigHeight), GUILayout.Width(60)):
        del self.wiz_step
        del self.wiz_tempProps
        _sc.subwinindex = 0
        camera_data = self.block[self.cur_index].cams[self.cur_cam]
        addata = camera_data[4]
        self.cam_addparam = addata["addparam"]
        self.cam_whosay = addata["whosay"]
        self.cam_whatsay = addata["whatsay"]
        if "addvncmds" in addata:
            self.cam_addvncmds = addata["addvncmds"]
        else:
            self.cam_addvncmds = ""
    GUILayout.Space(tablePadding)
    GUILayout.EndHorizontal()

    # end
    GUILayout.EndScrollView()

# --------- adv properties 1 --------

def adv1_def_values():
    return {"name": "",
            "isTime": False, "time": "2.0", "isTAnimCam": False, "isTHideUI": False, "isTTimerNext": False,
            "tacStyle": "fast-slow", "tacZOut": "0.0", "tacRotX": "0.0", "tacRotZ": "0.0", "keepcam": False}

def render_wizard_adv1(self, tempProps):
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""

    cam_style_list = ("linear", "slow-fast", "fast-slow", "slow-fast3", "fast-slow3", "slow-fast4", "fast-slow4")

    GUILayout.BeginHorizontal()
    GUILayout.Label("Name (you can address by name):")

    tempProps["a1o"]["name"] = GUILayout.TextField(tempProps["a1o"]["name"], GUILayout.Width(200))
    if GUILayout.Button("X", GUILayout.Width(20)):
        tempProps["a1o"]["name"] = ""

    tabWidth = 30

    GUILayout.FlexibleSpace()
    GUILayout.EndHorizontal()

    GUILayout.BeginHorizontal()
    tempProps["a1o"]["isTime"] = GUILayout.Toggle(tempProps["a1o"]["isTime"], " In time ")
    tempProps["a1o"]["time"] = GUILayout.TextField(tempProps["a1o"]["time"], GUILayout.Width(100))
    GUILayout.Label(" seconds do ")
    GUILayout.FlexibleSpace()
    GUILayout.EndHorizontal()

    if tempProps["a1o"]["isTime"]:
        #GUILayout.BeginHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Space(tabWidth)
        tempProps["a1o"]["isTAnimCam"] = GUILayout.Toggle(tempProps["a1o"]["isTAnimCam"], "Animate camera")
        if tempProps["a1o"]["isTAnimCam"]:
            GUILayout.Label(" with ")
            if GUILayout.Button(tempProps["a1o"]["tacStyle"]):
                si = cam_style_list.index(tempProps["a1o"]["tacStyle"])
                si += 1
                si %= len(cam_style_list)
                tempProps["a1o"]["tacStyle"] = cam_style_list[si]
            GUILayout.Label(" style.")
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()

        if tempProps["a1o"]["isTAnimCam"]:
            # GUILayout.BeginHorizontal()
            # GUILayout.Space(tabWidth*2)
            # GUILayout.Label("Move style:")
            # aniStyleTexts = Array[String](("Linear", "S-F", "F-S", "S-F3", "F-S3", "S-F4", "F-S4"))
            # tempProps["a1o"]["tacamStyle"] = GUILayout.SelectionGrid(tempProps["a1o"]["tacamStyle"], aniStyleTexts, 7)
            # GUILayout.EndHorizontal()

            GUILayout.BeginHorizontal()
            GUILayout.Space(tabWidth * 2)
            GUILayout.Label("Effects: zoom out (m): ")
            #aniStyleTexts = Array[String](("Linear", "S-F", "F-S", "S-F3", "F-S3", "S-F4", "F-S4"))
            tempProps["a1o"]["tacZOut"] = GUILayout.TextField(tempProps["a1o"]["tacZOut"])
            GUILayout.Label(" rotation x ")
            tempProps["a1o"]["tacRotX"] = GUILayout.TextField(tempProps["a1o"]["tacRotX"])
            GUILayout.Label(" rot z (tilt)")
            tempProps["a1o"]["tacRotZ"] = GUILayout.TextField(tempProps["a1o"]["tacRotZ"])
            GUILayout.EndHorizontal()

        GUILayout.BeginHorizontal()
        GUILayout.Space(tabWidth)
        tempProps["a1o"]["isTHideUI"] = GUILayout.Toggle(tempProps["a1o"]["isTHideUI"], "Hide UI")
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()

        GUILayout.BeginHorizontal()
        GUILayout.Space(tabWidth)
        tempProps["a1o"]["isTTimerNext"] = GUILayout.Toggle(tempProps["a1o"]["isTTimerNext"], "Move to next state after that time")
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()

    GUILayout.BeginHorizontal()
    #GUILayout.Label(" or just ")
    tempProps["a1o"]["keepcam"] = GUILayout.Toggle(tempProps["a1o"]["keepcam"], " Skip camera update, just keep previous camera. (advanced)")


    GUILayout.FlexibleSpace()
    GUILayout.EndHorizontal()
        #tempProps["a1o"]["time"] = GUILayout.TextField(tempProps["a1o"]["time"], GUILayout.Width(100))
        # GUILayout.Label(" do ")
        # GUILayout.FlexibleSpace()
        # GUILayout.EndHorizontal()

# --------- adv properties 2 --------

def adv2_def_values():
    return {"run-vnframe-ext": scenesavestate.is_ini_value_true("RunVNFrameExtDefault"), 
            "run-vnanime-ext": scenesavestate.is_ini_value_true("RunVNAnimeExtDefault"), 
            "run-vntext-ext": scenesavestate.is_ini_value_true("RunVNTextExtDefault"), 
            "run-objcam-ext": scenesavestate.is_ini_value_true("RunObjCamExtDefault"),
           }

def render_wizard_adv2(self, tempProps):
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""

    # object camera support
    GUILayout.BeginHorizontal()
    GUILayout.Label("  On cam change:")
    tempProps["a2o"]["run-vnframe-ext"] = GUILayout.Toggle(tempProps["a2o"]["run-vnframe-ext"], "Run VNFrame ext")
    tempProps["a2o"]["run-vnanime-ext"] = GUILayout.Toggle(tempProps["a2o"]["run-vnanime-ext"], "Run VNAnime ext")
    tempProps["a2o"]["run-objcam-ext"] = GUILayout.Toggle(tempProps["a2o"]["run-objcam-ext"], "Run VNFrame ext")
    GUILayout.EndHorizontal()
    #tempProps["a2o"]["run-vntext-ext"] = GUILayout.Toggle(tempProps["a2o"]["run-vntext-ext"], "Run VNText ext")

# ---------- utils ------------------
def adv_update(o1,o2):
    for key in o2:
        if key in o1:
            pass
        else:
            o1[key] = o2[key]
    return o1
    
def render_vnss_wizard(self):
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""

    # clear for initial
    if not hasattr(self, "wiz_step"):
        self.wiz_step = 0

    # step 0
    if self.wiz_step == 0:          # wait for start
        if GUILayout.Button("Wizard: Start adding a VNSS command.", GUILayout.Height(55)):
            self.wiz_step = 1

    elif self.wiz_step == 1:        # select command menu
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: What do you want to do?")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
        GUILayout.EndHorizontal()
        if GUILayout.Button("<color=#00ff00>addbtn</color>: Add a custom button to fork story line"):
            self.wiz_step = 10
            self.wiz_data = {"text": "", "jump": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>nextstate</color>: Make a jump when clicked 'Next' button"):
            self.wiz_step = 11
            self.wiz_data = {"jump": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>timernext</color>: Goto next cam/scene automatically when time passed"):
            self.wiz_step = 12
            self.wiz_data = {"time": "", "jump": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>addbtnrnd</color>: Add a custom button jump to random scene/cam"):
            self.wiz_step = 13
            self.wiz_data = {"text": "", "jump": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>addbtnms</color>: Add a custom button to invoke ministate"):
            self.wiz_step = 14
            self.wiz_data = {"text": "", "ministate": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>showui/hideui</color>: Hide or show the text dialog (UI)"):
            self.wiz_step = 15
            self.wiz_data = {"show": True, "time": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>lockui/unlockui</color>: Hide or show the buttons on dialog (UI)"):
            self.wiz_step = 16
            self.wiz_data = {"lock": False, "time": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>runms</color>: Invoke a ministate on this cam"):
            self.wiz_step = 17
            self.wiz_data = {"ministate": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>synch/height/breast</color>: Sync H or set height/breast for charators"):
            self.wiz_step = 18
            self.wiz_data = {"action": "f_synch", "fid": "", "mid": "", "value": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>VNFrame ext</color>: Change the status of actor/props"):
            self.wiz_step = 20
            self.wiz_data = {"script": {}, "anime": False, "time": "1", "style": "linear"}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>VNAnime ext</color>: Control the playback of Keyframe clips"):
            self.wiz_step = 21
            self.wiz_data = {"action": "play", "clip": "", "loop": "", "speed": "", "frame": ""}
            self.wiz_error = None
        if (self.game.isCharaStudio or self.game.isNEOV2) and GUILayout.Button("<color=#00ff00>ObjCam ext</color>: switch to object camera"):
            self.wiz_step = 22
            self.wiz_data = {"name": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>VNText ext</color>: Editor VNText in scene"):
            self.wiz_step = 23
            self.wiz_data = {"action": "update"}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>Blackrain ext</color>: Variable and logic"):
            self.wiz_step = 24
        if GUILayout.Button("<color=#00ff00>GameUtil ext</color>: Some game utilities"):
            self.wiz_step = 25

    elif self.wiz_step == 10:       # addbtn command
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Setup a custom button")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            self.wiz_error = None
            btxt = self.wiz_data["text"].strip()
            if len(btxt) == 0:
                self.wiz_error = "Input a string for button text!"
            dtxt = self.wiz_data["jump"].strip()
            if dtxt != "end" and dtxt != "next" and (not dtxt.startswith("{") or not dtxt.endswith("}")):
                try:
                    dno = int(dtxt)
                except:
                    self.wiz_error = "Input a valid number for jump destination! Or 'next' for next cam, 'end' for end of game, '{camname}' for named cam."
                    dno = None
                if dno != None:
                    dno_cam = dno % 100
                    dno_scn = int(dno / 100)
                    if dno_cam != 0 and dno_scn != self.cur_index + 1:
                        self.wiz_error = "%d is not a valid jump destination! You can only jump to cam0 of other scene (n00), or any cam of the same scene (%dnn)."%(dno, self.cur_index + 1)
            if self.wiz_error == None:
                cmd = "addbtn:%s:%s"%(btxt, dtxt)
                append_vnss_cmd(self, cmd)
                self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Button text:", GUILayout.Width(80))
        self.wiz_data["text"] = GUILayout.TextField(self.wiz_data["text"], GUILayout.Width(120))
        GUILayout.Space(10)
        GUILayout.Label("Click the button jump to:", GUILayout.Width(150))
        self.wiz_data["jump"] = GUILayout.TextField(self.wiz_data["jump"], GUILayout.Width(100))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        else:
            GUILayout.Label("* Jump destination is <color=#00ff00>(scene number) * 100 + (cam number)</color>. For example, set 200 for first cam of scene2, 202 for scene2 cam2. Or set <color=#00ff00>{camname}</color> to jump to a named cam. Or set <color=#00ff00>next</color> for next cam, <color=#00ff00>end</color> for end of game.")
        GUILayout.EndHorizontal()

    elif self.wiz_step == 11:       # nextstate command
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Setup a jump when click next")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            self.wiz_error = None
            dtxt = self.wiz_data["jump"].strip()
            if dtxt != "end" and (not dtxt.startswith("{") or not dtxt.endswith("}")):
                try:
                    dno = int(dtxt)
                except:
                    self.wiz_error = "Input a valid number for jump destination! Or 'end' for end of game, '{camname}' for named cam."
                    dno = None
                if dno != None:
                    dno_cam = dno % 100
                    dno_scn = int(dno / 100)
                    if dno_cam != 0 and dno_scn != self.cur_index + 1:
                        self.wiz_error = "%d is not a valid jump destination! You can only jump to cam0 of other scene (n00), or any cam of the same scene (%dnn)."%(dno, self.cur_index + 1)
            if self.wiz_error == None:
                cmd = "nextstate:%s"%(dtxt)
                append_vnss_cmd(self, cmd)
                self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Click the next then jump to:", GUILayout.Width(170))
        self.wiz_data["jump"] = GUILayout.TextField(self.wiz_data["jump"], GUILayout.Width(100))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        else:
            GUILayout.Label("* Jump destination is <color=#00ff00>(scene number) * 100 + (cam number)</color>. For example, set 200 for first cam of scene2, 202 for scene2 cam2. Or set <color=#00ff00>{camname}</color> to jump to a named cam. Or set <color=#00ff00>end</color> for end of game.")
        GUILayout.EndHorizontal()

    elif self.wiz_step == 12:       # timernext command
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Setup a auto next timer")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            self.wiz_error = None
            ttxt = self.wiz_data["time"].strip()
            try:
                tmr = float(ttxt)
                if tmr <= 0:
                    raise Exception()
            except:
                self.wiz_error = "Input a valid float number for timer in second!"
            dtxt = self.wiz_data["jump"].strip()
            if len(dtxt) > 0 and dtxt != "end" and (not dtxt.startswith("{") or not dtxt.endswith("}")):
                try:
                    dno = int(dtxt)
                except:
                    self.wiz_error = "Input a valid number for jump destination! Or 'end' for end of game, '{camname}' for named cam."
                    dno = None
                if dno != None:
                    dno_cam = dno % 100
                    dno_scn = int(dno / 100)
                    if dno_cam != 0 and dno_scn != self.cur_index + 1:
                        self.wiz_error = "%d is not a valid jump destination! You can only jump to cam0 of other scene (n00), or any cam of the same scene (%dnn)."%(dno, self.cur_index + 1)
            if self.wiz_error == None:
                if len(dtxt) > 0:
                    cmd = "timernext:%s:%s"%(ttxt, dtxt)
                else:
                    cmd = "timernext:%s"%(ttxt)
                append_vnss_cmd(self, cmd)
                self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Goto next scene after:", GUILayout.Width(150))
        self.wiz_data["time"] = GUILayout.TextField(self.wiz_data["time"], GUILayout.Width(50))
        GUILayout.Label("seconds", GUILayout.Width(60))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Set jump destination:", GUILayout.Width(150))
        self.wiz_data["jump"] = GUILayout.TextField(self.wiz_data["jump"], GUILayout.Width(100))
        GUILayout.Label(", leave it blank to just go next.")
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        else:
            GUILayout.Label("* Jump destination is <color=#00ff00>(scene number) * 100 + (cam number)</color>. For example, set 200 for first cam of scene2, 202 for scene2 cam2. Or set <color=#00ff00>{camname}</color> to jump to a named cam. Or set <color=#00ff00>end</color> for end of game.")
        GUILayout.EndHorizontal()

    elif self.wiz_step == 13:       # addbtnrnd command
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Setup a random custom button")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            self.wiz_error = None
            txt = self.wiz_data["text"].strip()
            if len(txt) == 0:
                self.wiz_error = "Input a string for button text!"
            try:
                dtxts = self.wiz_data["jump"].strip().split(",")
                for dtxt in dtxts:
                    dtxt = dtxt.strip()
                    if dtxt != "end" and dtxt != "next" and (not dtxt.startswith("{") or not dtxt.endswith("}")):
                        dno = int(dtxt)
                        dno_cam = dno % 100
                        dno_scn = int(dno / 100)
                        if dno_cam != 0 and dno_scn != self.cur_index + 1:
                            raise Exception("%d is not a valid jump destination! You can only jump to cam0 of other scene (n00), or any cam of the same scene (%dnn)."%(dno, self.cur_index + 1))
                dtxts = ",".join(dtxts)
            except Exception, e:
                self.wiz_error = "Input a valid jump destination! " + str(e)
                dtxts = None
            if self.wiz_error == None:
                cmd = "addbtnrnd:%s:%s"%(txt, dtxts)
                append_vnss_cmd(self, cmd)
                self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Button text:", GUILayout.Width(80))
        self.wiz_data["text"] = GUILayout.TextField(self.wiz_data["text"], GUILayout.Width(120))
        GUILayout.Space(10)
        GUILayout.Label("Click the button jump to:", GUILayout.Width(150))
        self.wiz_data["jump"] = GUILayout.TextField(self.wiz_data["jump"], GUILayout.Width(100))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        else:
            GUILayout.Label("* Jump destination is <color=#00ff00>(scene number) * 100 + (cam number)</color>. For example, set 200 for first cam of scene2, 202 for scene2 cam2. Or set <color=#00ff00>{camname}</color> to jump to a named cam. Or set <color=#00ff00>next</color> for next cam, <color=#00ff00>end</color> for end of game. Set multiple jump destination separated by comma (ex: 201,202,203). When user click this button story will jump to one of them randomly.")
        GUILayout.EndHorizontal()

    elif self.wiz_step == 14:       # addbtnms command
        from libministates import ministates_get_list
        mslist = [i[0] for i in ministates_get_list(self.game)]
        if len(mslist) > 0:
            GUILayout.BeginHorizontal()
            GUILayout.Label("Wizard: Setup a ministate button")
            GUILayout.FlexibleSpace()
            if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
                self.wiz_error = None
                btxt = self.wiz_data["text"].strip()
                if len(btxt) == 0:
                    self.wiz_error = "Input a string for button text!"
                sts = self.wiz_data["ministate"].strip()
                if self.wiz_error == None and (len(sts) == 0 or mslist.count(sts) == 0):
                    self.wiz_error = "[%s] is not a valid ministate name!"%(sts)
                if self.wiz_error == None:
                    cmd = "addbtnms:%s:%s"%(btxt, sts)
                    append_vnss_cmd(self, cmd)
                    self.wiz_step = 0
            if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
                self.wiz_step = 0
                self.wiz_error = None
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Button text:", GUILayout.Width(80))
            self.wiz_data["text"] = GUILayout.TextField(self.wiz_data["text"], GUILayout.Width(120))
            GUILayout.Space(10)
            GUILayout.Label("Click invokes:", GUILayout.Width(90))
            self.wiz_data["ministate"] = GUILayout.TextField(self.wiz_data["ministate"], GUILayout.Width(120))
            if GUILayout.Button("<", GUILayout.Width(20)):
                msname = self.wiz_data["ministate"].strip()
                if len(msname) == 0 or mslist.count(msname) == 0:
                    self.wiz_data["ministate"] = mslist[0]
                else:
                    ci = mslist.index(msname)
                    self.wiz_data["ministate"] = mslist[(ci - 1)]                
            if GUILayout.Button(">", GUILayout.Width(20)):
                msname = self.wiz_data["ministate"].strip()
                if len(msname) == 0 or mslist.count(msname) == 0:
                    self.wiz_data["ministate"] = mslist[0]
                else:
                    ci = mslist.index(msname)
                    self.wiz_data["ministate"] = mslist[(ci + 1) % len(mslist)]                
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            if self.wiz_error:
                GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
            else:
                GUILayout.Label("* Create a button to invoke a ministate by its name.")
            GUILayout.EndHorizontal()
        else:
            GUILayout.BeginHorizontal()
            GUILayout.Label("Wizard: Invoke a ministate")
            GUILayout.FlexibleSpace()
            if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
                self.wiz_step = 0
                self.wiz_error = None
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("No ministate found in this scene. Create one in Ministates panel first.")
            GUILayout.EndHorizontal()

    elif self.wiz_step == 15:       # showui/hideui command
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Show/Hide the dialog box (UI)")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            self.wiz_error = None
            cmd = "showui" if self.wiz_data["show"] else "hideui"
            try:
                tmrTxt = self.wiz_data["time"].strip()
                if cmd == "hideui" and len(tmrTxt) > 0:
                    tmr = float(tmrTxt)
                    if tmr <= 0:
                        raise Exception()
                    cmd += ":" + tmrTxt
            except:
                self.wiz_error = "Input a valid float number for timer in second!"
                cmd = None
            if self.wiz_error == None:
                append_vnss_cmd(self, cmd)
                self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        self.wiz_data["show"] = GUILayout.Toggle(self.wiz_data["show"], "Show UI", GUILayout.Width(100))
        self.wiz_data["show"] = not GUILayout.Toggle(not self.wiz_data["show"], "Hide UI", GUILayout.Width(60))
        if not self.wiz_data["show"]:
            GUILayout.Label("for ", GUILayout.Width(25))
            self.wiz_data["time"] = GUILayout.TextField(self.wiz_data["time"], GUILayout.Width(30))
            GUILayout.Label("seconds, leave it blank for manual re-show")
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        else:
            GUILayout.Label("* You can't hit any button when UI was hidden. Set a timeout for hide UI command, or you must call show UI by yourself! In this case use it with <color=#00ff00>timernext</color>, and be sure to re-show it on the next scene/cam.")
        GUILayout.EndHorizontal()

    elif self.wiz_step == 16:       # unlockui/lockui command
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Show/Hide the dialog box (UI)")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            self.wiz_error = None
            cmd = "lockui" if self.wiz_data["lock"] else "unlockui"
            try:
                tmrTxt = self.wiz_data["time"].strip()
                if cmd == "lockui" and len(tmrTxt) > 0:
                    tmr = float(tmrTxt)
                    if tmr <= 0:
                        raise Exception()
                    cmd += ":" + tmrTxt
            except:
                self.wiz_error = "Input a valid float number for timer in second!"
                cmd = None
            if self.wiz_error == None:
                append_vnss_cmd(self, cmd)
                self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        self.wiz_data["lock"] = not GUILayout.Toggle(not self.wiz_data["lock"], "Unlock UI", GUILayout.Width(100))
        self.wiz_data["lock"] = GUILayout.Toggle(self.wiz_data["lock"], "Lock UI", GUILayout.Width(60))
        if self.wiz_data["lock"]:
            GUILayout.Label("for ", GUILayout.Width(25))
            self.wiz_data["time"] = GUILayout.TextField(self.wiz_data["time"], GUILayout.Width(30))
            GUILayout.Label("seconds, leave it blank for manual unlock")
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        else:
            GUILayout.Label("* You can't hit any button when UI was locked! Set a timeout for lock UI command, or you must call unlock UI by yourself! In this case use it with <color=#00ff00>timernext</color>, and be sure to unlock it on the next scene/cam.")
        GUILayout.EndHorizontal()

    elif self.wiz_step == 17:       # runms command
        from libministates import ministates_get_list
        mslist = [i[0] for i in ministates_get_list(self.game)]
        if len(mslist) > 0:
            GUILayout.BeginHorizontal()
            GUILayout.Label("Wizard: Invoke a ministate")
            GUILayout.FlexibleSpace()
            if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
                self.wiz_error = None
                msname = self.wiz_data["ministate"].strip()
                if len(msname) == 0 or mslist.count(msname) == 0:
                    self.wiz_error = "[%s] is not a valid ministate name!"%(msname)
                if self.wiz_error == None:
                    cmd = "runms:%s"%(msname)
                    append_vnss_cmd(self, cmd)
                    self.wiz_step = 0
            if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
                self.wiz_step = 0
                self.wiz_error = None
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Ministate to run:", GUILayout.Width(150))
            self.wiz_data["ministate"] = GUILayout.TextField(self.wiz_data["ministate"], GUILayout.Width(150))
            if GUILayout.Button("<", GUILayout.Width(20)):
                msname = self.wiz_data["ministate"].strip()
                if len(msname) == 0 or mslist.count(msname) == 0:
                    self.wiz_data["ministate"] = mslist[0]
                else:
                    ci = mslist.index(msname)
                    self.wiz_data["ministate"] = mslist[(ci - 1)]                
            if GUILayout.Button(">", GUILayout.Width(20)):
                msname = self.wiz_data["ministate"].strip()
                if len(msname) == 0 or mslist.count(msname) == 0:
                    self.wiz_data["ministate"] = mslist[0]
                else:
                    ci = mslist.index(msname)
                    self.wiz_data["ministate"] = mslist[(ci + 1) % len(mslist)]                
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            if self.wiz_error:
                GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
            else:
                GUILayout.Label("* Set a ministate to run when this cam starts.")
            GUILayout.EndHorizontal()
        else:
            GUILayout.BeginHorizontal()
            GUILayout.Label("Wizard: Invoke a ministate")
            GUILayout.FlexibleSpace()
            if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
                self.wiz_step = 0
                self.wiz_error = None
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("No ministate found in this scene. Create one in Ministates panel first.")
            GUILayout.EndHorizontal()

    elif self.wiz_step == 18:       # f_synch/f_synchr/f_height/f_breast command
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Sync H animation for charators")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            self.wiz_error = None
            cmd = self.wiz_data["action"]
            fid = self.wiz_data["fid"]
            try:
                if not self.game.scenef_get_actor(fid):
                    raise Exception("<" + fid + "> is not a valid charactor id!")
                if cmd.startswith("f_synch"):
                    mid = self.wiz_data["mid"]
                    if len(mid) > 0 and not self.game.scenef_get_actor(mid):
                        raise Exception("<" + mid + "> is not a valid charactor id!")
                    if fid == mid:
                        raise Exception("Choice a different actor to sync with base actor!")
                    if len(mid) > 0:
                        cmd += ":" + fid + ":" + mid
                    else:
                        cmd += ":" + fid
                else:
                    valstr = self.wiz_data["value"].strip()
                    valnum = float(valstr)
                    cmd += ":" + fid + ":" + valstr                   
            except Exception, e:
                self.wiz_error = "Wrong input: " + str(e)
                cmd = None
            if self.wiz_error == None:
                append_vnss_cmd(self, cmd)
                self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        curActors = self.game.scenef_get_all_actors()
        if len(curActors) == 0:
            self.wiz_error = "No charactor tracked! Please track charactor first."
        else:
            def selectPrevNext(sid, dir):
                cids = sorted(curActors.keys())
                if sid in cids:
                    return cids[(cids.index(sid) + dir)%len(cids)]
                else:
                    return cids[0]
            def dispNameOfId(sid):
                if sid in curActors.keys():
                    return "<color=#00ff00>" + sid + ": " + curActors[sid].text_name + "</color>"
                else:
                    return "<color=#ff0000>Not Set</color>"
            GUILayout.BeginHorizontal()
            GUILayout.Label("Command: ", GUILayout.Width(70))
            if GUILayout.Toggle(self.wiz_data["action"] == "f_synch", "Sync H-anime "):
                self.wiz_data["action"] = "f_synch"
            if GUILayout.Toggle(self.wiz_data["action"] == "f_synchr", "Sync and restart "):
                self.wiz_data["action"] = "f_synchr"
            if GUILayout.Toggle(self.wiz_data["action"] == "f_height", "Set height "):
                self.wiz_data["action"] = "f_height"
            if GUILayout.Toggle(self.wiz_data["action"] == "f_breast", "Set breast"):
                self.wiz_data["action"] = "f_breast"
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Base actor:" if self.wiz_data["action"].startswith("f_synch") else "Tgt actor:", GUILayout.Width(70))
            if GUILayout.Button("<", GUILayout.Width(20)):
                self.wiz_data["fid"] = selectPrevNext(self.wiz_data["fid"], -1)
            if GUILayout.Button(">", GUILayout.Width(20)):
                self.wiz_data["fid"] = selectPrevNext(self.wiz_data["fid"], +1)
            GUILayout.Space(24)
            GUILayout.Label(dispNameOfId(self.wiz_data["fid"]))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            if self.wiz_data["action"].startswith("f_synch"):
                GUILayout.Label("Partner:", GUILayout.Width(70))
                if GUILayout.Button("<", GUILayout.Width(20)):
                    self.wiz_data["mid"] = selectPrevNext(self.wiz_data["mid"], -1)
                if GUILayout.Button(">", GUILayout.Width(20)):
                    self.wiz_data["mid"] = selectPrevNext(self.wiz_data["mid"], +1)
                if GUILayout.Button("x", GUILayout.Width(20)):
                    self.wiz_data["mid"] = ""
                GUILayout.Label(dispNameOfId(self.wiz_data["mid"]))
            else:
                GUILayout.Label("Value:", GUILayout.Width(70))
                self.wiz_data["value"] = GUILayout.TextField(self.wiz_data["value"], GUILayout.Width(50))
                GUILayout.Label(" (normally between 0 to 1)")
            GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        elif self.wiz_data["action"] == "f_synch":
            GUILayout.Label("* Sync H animation can automatically adjust actor's anime aux param according to base actor's height and breast. The base actor usually is the female actor.")
        elif self.wiz_data["action"] == "f_synchr":
            GUILayout.Label("* Sync H animation can automatically adjust actor's anime aux param according to base actor's height and breast. The base actor usually is the female actor.\nAnd this command restart anime too, BUT MAY CAUSE BUG IF RESTART JUST AFTER SET ANIME?")
        elif self.wiz_data["action"] == "f_height":
            GUILayout.Label("* Set height of target actor, unlike actor's scale height is not tracked by SSS by default. The value is normally between 0 to 1, map to 0 to 100 when create charactor.")
        elif self.wiz_data["action"] == "f_breast":
            GUILayout.Label("* Set breast of target actor, breast is not tracked by SSS by default. The value is normally between 0 to 1, map to 0 to 100 when create charactor.")
        else:
            self.wiz_error = "Unknown command <%s>"%self.wiz_data["action"]
        GUILayout.EndHorizontal()

    elif self.wiz_step == 20:       # VNFrame command
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Addition VNFrame command to make scene variant")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            if len(self.wiz_data["script"]) > 0:
                from vnframe import script2string
                if self.wiz_data["anime"]:
                    try:
                        tmr = float(self.wiz_data["time"])
                        if tmr <= 0:
                            raise Exception()
                        self.wiz_error = None
                        aniScript = ((self.wiz_data["script"], tmr, self.wiz_data["style"]), )
                        cmd = "f_anime:::%s"%script2string(aniScript).replace(" ", "").strip()
                    except:
                        self.wiz_error = "Input a valid time value in second for animation!"
                else:
                    cmd = "f_act:::%s"%script2string(self.wiz_data["script"]).replace(" ", "").strip()
                if self.wiz_error == None:
                    append_vnss_cmd(self, cmd)
                    self.wiz_step = 0
            else:
                self.wiz_error = "No script found, make some change and take a snapshot, or setup by manual mode first!"
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if GUILayout.Button("Snapshot", GUILayout.Width(100)):
            self.wiz_data["script"] = vnframe_take_snapshot(self)
            if len(self.wiz_data["script"]) == 0:
                self.wiz_error = "No change on tracked actor/prop found, please make some change against base scene."
            else:
                self.wiz_error = None
        if GUILayout.Button("Manual Mode", GUILayout.Width(100)):
            vnframe_manual_start(self, None)
        if len(self.wiz_data["script"]) > 0 and GUILayout.Button("Reset", GUILayout.Width(100)):
            self.block[self.cur_index].setSceneState(self.game)
        if len(self.wiz_data["script"]) > 0 and GUILayout.Button("Preview", GUILayout.Width(100)):
            from vnframe import act, anime, scriptCopy
            if self.wiz_data["anime"]:
                try:
                    tmr = float(self.wiz_data["time"])
                    if tmr <= 0:
                        raise Exception()
                    self.wiz_error = None
                except:
                    self.wiz_error = "Input a valid time value in second for animation!"
                if self.wiz_error == None:
                    ss = scriptCopy(self.wiz_data["script"])
                    aniScript = ((ss, tmr, self.wiz_data["style"]), )
                    #print "anime script:", aniScript
                    anime(self.game, aniScript)
            else:
                ss = scriptCopy(self.wiz_data["script"])
                #print "act script:", self.wiz_data["script"]
                act(self.game, ss)
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        self.wiz_data["anime"] = GUILayout.Toggle(self.wiz_data["anime"], "Render in animation", GUILayout.Width(140))
        if self.wiz_data["anime"]:
            GUILayout.Label("length:", GUILayout.Width(50))
            self.wiz_data["time"] = GUILayout.TextField(self.wiz_data["time"], GUILayout.Width(40))
            GUILayout.Label("sec, style:", GUILayout.Width(80))
            if GUILayout.Button(self.wiz_data["style"], GUILayout.Width(100)):
                vnfa_style_list = ("linear", "slow-fast", "fast-slow", "slow-fast3", "fast-slow3", "slow-fast4", "fast-slow4")
                si = vnfa_style_list.index(self.wiz_data["style"])
                si += 1
                si %= len(vnfa_style_list)
                self.wiz_data["style"] = vnfa_style_list[si]
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        else:
            GUILayout.Label("* Setup you scene and click the <color=#00ff00>[Snapshot]</color> button to get a diff snapshot with the <color=#ff0000>base scene (not the last cam!)</color>, or use <color=#00ff00>Manual Mode</color> button to setup by yourself. Then use <color=#00ff00>[Reset]</color> and <color=#00ff00>[Preview]</color> button to preview your vnframe act/anime. Hit <color=#00ff00>[OK]</color> if you are done. VNFrame anime is NOT RECOMMENDED for complicated animation, use VNAnime Keyframe Clip instead.")
        GUILayout.EndHorizontal()

    elif self.wiz_step == 21:       # VNAnime command
        # syntax check enable
        if not hasattr(self.game, "gdata") or not hasattr(self.game.gdata, "kfaManagedClips"):
            self.wiz_error = "WARNING: Keyframe function not initialized! Syntax check DISABLED! Set all parameters on your own risk!"
            synChk = False
        elif len(self.game.gdata.kfaManagedClips) == 0:
            self.wiz_error = "WARNING: No keyframe clips found! Syntax check DISABLED! Set all parameters on your own risk!"
            synChk = False
        else:
            synChk = True
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: VNAnime command to control keyframe clip playback")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            clpname = self.wiz_data["clip"].strip()
            cmd = None
            if synChk:
                if len(clpname) > 0 and not self.game.gdata.kfaManagedClips.has_key(clpname):
                    self.wiz_error = "Keyframe clip [%s] not found! Input a valid clip name."%clpname
                else:
                    self.wiz_error = None
                if self.wiz_error == None and self.wiz_data["action"] == "play":
                    if len(clpname) > 0:
                        try:
                            if len(self.wiz_data["loop"].strip()) > 0:
                                loop = int(self.wiz_data["loop"])
                                if loop < -1:
                                    raise Exception()
                            else:
                                loop = None
                        except:
                            self.wiz_error = "Input a valid number for loop count. -1 for infinite loop, 0 for non-loop, 1 for loop once and so on."
                        try:
                            if len(self.wiz_data["speed"].strip()) > 0:
                                speed = float(self.wiz_data["speed"])
                                if speed <= 0:
                                    raise Exception()
                            else:
                                speed = None
                        except:
                            self.wiz_error = "Input a valid float number for speed rate. 1 for normal speed, 2 for 2x speed and so on."
                        if self.wiz_error == None:
                            if speed != None:
                                cmd = "f_clipplay:%s:%s:%.1f"%(clpname, "" if loop == None else str(loop), speed)
                            elif loop != None:
                                cmd = "f_clipplay:%s:%d"%(clpname, loop)
                            else:
                                cmd = "f_clipplay:%s"%clpname
                    else:
                        cmd = "f_clipplay"
                if self.wiz_error == None and self.wiz_data["action"] == "pause":
                    if len(clpname) > 0:
                        cmd = "f_clippause:%s"%clpname
                    else:
                        cmd = "f_clippause"
                if self.wiz_error == None and self.wiz_data["action"] == "stop":
                    if len(clpname) > 0:
                        cmd = "f_clipstop:%s"%clpname
                    else:
                        cmd = "f_clipstop"
                if self.wiz_error == None and self.wiz_data["action"] == "seek":
                    if len(clpname) > 0:
                        try:
                            frame = int(self.wiz_data["frame"])
                            if frame < 0 or frame > self.game.gdata.kfaManagedClips[clpname].frameLength:
                                raise Exception()
                        except:
                            self.wiz_error = "Input a valid number for frame. Valid frame range of clip [%s] is 0-%d."%(clpname, self.game.gdata.kfaManagedClips[clpname].frameLength)
                        if self.wiz_error == None:
                            cmd = "f_clipseek:%s:%d"%(clpname, frame)
                    else:
                        self.wiz_error = "Clip name not setted!"
            else:
                if self.wiz_data["action"] == "play":
                    if len(clpname) > 0:
                        if len(self.wiz_data["loop"].strip()) > 0:
                            loop = self.wiz_data["loop"].strip()
                        else:
                            loop = None
                        if len(self.wiz_data["speed"].strip()) > 0:
                            speed = self.wiz_data["speed"].strip()
                        else:
                            speed = None
                        if speed != None:
                            cmd = "f_clipplay:%s:%s:%s"%(clpname, "" if loop == None else loop, speed)
                        elif loop != None:
                            cmd = "f_clipplay:%s:%s"%(clpname, loop)
                        else:
                            cmd = "f_clipplay:%s"%clpname
                    else:
                        cmd = "f_clipplay"
                if self.wiz_data["action"] == "pause":
                    if len(clpname) > 0:
                        cmd = "f_clippause:%s"%clpname
                    else:
                        cmd = "f_clippause"
                if self.wiz_data["action"] == "stop":
                    if len(clpname) > 0:
                        cmd = "f_clipstop:%s"%clpname
                    else:
                        cmd = "f_clipstop"
                if self.wiz_data["action"] == "seek":
                    if len(clpname) > 0:
                        frame = self.wiz_data["frame"]
                        cmd = "f_clipseek:%s:%s"%(clpname, frame)
                    else:
                        self.wiz_error = "Clip name not setted!"
            if cmd != None:
                append_vnss_cmd(self, cmd)
                self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Select an action:", GUILayout.Width(100))
        if GUILayout.Toggle(self.wiz_data["action"] == "play", "Play", GUILayout.Width(80)) and self.wiz_data["action"] != "play":
            self.wiz_data["action"] = "play"
            if synChk:
                self.wiz_error = None
        if GUILayout.Toggle(self.wiz_data["action"] == "pause", "Pause", GUILayout.Width(80)) and self.wiz_data["action"] != "pause":
            self.wiz_data["action"] = "pause"
            if synChk:
                self.wiz_error = None
        if GUILayout.Toggle(self.wiz_data["action"] == "stop", "Stop", GUILayout.Width(80)) and self.wiz_data["action"] != "stop":
            self.wiz_data["action"] = "stop"
            if synChk:
                self.wiz_error = None
        if GUILayout.Toggle(self.wiz_data["action"] == "seek", "Seek", GUILayout.Width(80)) and self.wiz_data["action"] != "seek":
            self.wiz_data["action"] = "seek"
            if synChk:
                self.wiz_error = None
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Target clip name:", GUILayout.Width(100))
        self.wiz_data["clip"] = GUILayout.TextField(self.wiz_data["clip"], GUILayout.Width(100))
        if synChk:
            if GUILayout.Button("<", GUILayout.Width(20)):
                cnlist = sorted(self.game.gdata.kfaManagedClips.keys())
                if (cnlist.count(self.wiz_data["clip"].strip())):
                    cInx = cnlist.index(self.wiz_data["clip"].strip())
                    cInx -= 1
                    cInx %= len(cnlist)
                    self.wiz_data["clip"] = cnlist[cInx]
                else:
                    self.wiz_data["clip"] = cnlist[0]
            if GUILayout.Button(">", GUILayout.Width(20)):
                cnlist = sorted(self.game.gdata.kfaManagedClips.keys())
                if (cnlist.count(self.wiz_data["clip"].strip())):
                    cInx = cnlist.index(self.wiz_data["clip"].strip())
                    cInx += 1
                    cInx %= len(cnlist)
                    self.wiz_data["clip"] = cnlist[cInx]
                else:
                    self.wiz_data["clip"] = cnlist[0]
        if self.wiz_data["action"] != "seek":
            if GUILayout.Button("X", GUILayout.Width(20)):
                self.wiz_data["clip"] = ""
            GUILayout.Label("* Leave blank to operate all clips")
        else:
            GUILayout.Label(", seek to frame No:", GUILayout.Width(120))
            self.wiz_data["frame"] = GUILayout.TextField(self.wiz_data["frame"], GUILayout.Width(50))
        GUILayout.EndHorizontal()
        if self.wiz_data["action"] == "play" and len(self.wiz_data["clip"].strip()) > 0:
            GUILayout.BeginHorizontal()
            GUILayout.Label("Play loop:", GUILayout.Width(80))
            self.wiz_data["loop"] = GUILayout.TextField(self.wiz_data["loop"], GUILayout.Width(40))
            GUILayout.Label(", speed:", GUILayout.Width(60))
            self.wiz_data["speed"] = GUILayout.TextField(self.wiz_data["speed"], GUILayout.Width(40))
            GUILayout.Label("* Leave blank for clip's default")
            GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        # Notification
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        elif self.wiz_data["action"] == "play":
            GUILayout.Label("* Play the specified clip or all clips. When you target one clip, you can control the loop count and play speed too.")
        elif self.wiz_data["action"] == "pause":
            GUILayout.Label("* Pause the specified clip or all clips. Resume from current frame when you play again.")
        elif self.wiz_data["action"] == "stop":
            GUILayout.Label("* Stop the specified clip or all clips. Start from beginning when you play again.")
        elif self.wiz_data["action"] == "seek":
            GUILayout.Label("* Seek to the specified frame of a clip. Start from there when you play it.")
        else:
            self.wiz_error = "Unexpected action!?"
        GUILayout.EndHorizontal()

    elif self.wiz_step == 22:       # ObjCam command
        # list object camera and set synChk
        try:
            from Studio import OCICamera
            ocams =  [cam.name for cam in self.game.studio.dicObjectCtrl.Values if isinstance(cam, OCICamera)]
            ocams.append("")
        except:
            ocams = None
        if ocams == None:
            self.wiz_error = "ERROR: Fail to get OCICamera! Object camera doesn't work!"
            synChk = False
        elif len(ocams) == 1:
            self.wiz_error = "WARNING: No object camera found! Syntax check DISABLED! Set all parameters on your own risk!"
            synChk = False
        else:
            synChk = True
        # header line
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Switch between normal camera and object camera")
        GUILayout.FlexibleSpace()
        if ocams and GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            self.wiz_error = None
            cname = self.wiz_data["name"].strip()
            cmd = "objcam:%s"%(cname)
            append_vnss_cmd(self, cmd)
            self.wiz_step = 0
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        # contents
        GUILayout.BeginHorizontal()
        if synChk:
            GUILayout.Label("Target camera:", GUILayout.Width(100))
            GUILayout.Label("<color=#ff0000>" + self.wiz_data["name"] + "</color>" if self.wiz_data["name"] != "" else "<color=#00ff00>normal camera</color>", GUILayout.Width(150))
            if GUILayout.Button("<", GUILayout.Width(20)):
                cInx = ocams.index(self.wiz_data["name"])
                cInx -= 1
                cInx %= len(ocams)
                self.wiz_data["name"] = ocams[cInx]
            if GUILayout.Button(">", GUILayout.Width(20)):
                cInx = ocams.index(self.wiz_data["name"])
                cInx += 1
                cInx %= len(ocams)
                self.wiz_data["name"] = ocams[cInx]
        elif ocams:
            GUILayout.Label("Target camera:", GUILayout.Width(100))
            self.wiz_data["name"] = GUILayout.TextField(self.wiz_data["name"], GUILayout.Width(150)).strip()
            GUILayout.Label("* Leave blank switch to normal camera")
        GUILayout.EndHorizontal()
        # Notification
        if self.wiz_error:
            GUILayout.Label("<color=#ff0000>" + self.wiz_error + "</color>")
        else:
            GUILayout.Label("* Switch to selected object camera or back to normal camera. Remember when object camera actived, it will overwrite normal camera setting <color=#ff0000>UNTIL</color> you switch back to normal camera.")

    elif self.wiz_step == 23:       # VNText command
        from vntext import get_vntext_manager
        mgr = get_vntext_manager(self.game)
        # header line
        GUILayout.BeginHorizontal()
        GUILayout.Label("Wizard: Manage dynamic vntexts")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>Update</color>", GUILayout.Width(60)):
            if self.wiz_data["action"] == "update":
                cmd = "f_dyntext:::" + mgr.exportDynamicTextSetting()
                remove_vnss_cmd_startswith(self, "f_dyntext:::")
                append_vnss_cmd(self, cmd)
            else:
                remove_vnss_cmd_startswith(self, "f_dyntext:::")
            self.wiz_step = 0
            self.wiz_error = None
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        # contents
        GUILayout.Label("Current has %d dynamic vntexts in the scene"%mgr.managedTextCount)
        GUILayout.BeginHorizontal()
        if GUILayout.Button("<color=#00ff00>Start VNText Editor...</color>"):
            self.vnss_wizard_ui_mode = "vntext"
        if GUILayout.Button("Delete Dynamic VNText Cmd"):
            self.wiz_data["action"] = "delete"
        GUILayout.EndHorizontal()

    elif self.wiz_step == 24:       # Blackrain commands
        GUILayout.BeginHorizontal()
        GUILayout.Label("Blackrain ext: What do you want to do?")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
        GUILayout.EndHorizontal()
        if GUILayout.Button("<color=#00ff00>setvar</color>: set a variable to a number"):
            self.wiz_step = 2401
            self.wiz_data = {"action": "setvar", "title": "set a variable to a number", "desp": "If a var is specified its value is resolved", "ap1": "", "ap2": "", "ap3": None}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>setrandvar</color>: set var to a random number"):
            self.wiz_step = 2402
            self.wiz_data = {"action": "setrandvar", "title": "set var to a random number", "desp": "Create a random integer in range (x,y)", "ap1": "", "ap2": "", "ap3": None}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>setrandsumvar</color>: set var to multiple random numbers summed together"):
            self.wiz_step = 2403
            self.wiz_data = {"action": "setrandsumvar", "title": "set var to multiple random numbers summed together", "desp": "Create a random integer in range (x,y) several times and add them up.", "ap1": "", "ap2": "", "ap3": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>opvar</color>: perform math operation on a variable"):
            self.wiz_step = 2404
            self.wiz_data = {"action": "opvar", "title": "perform math operation on a variable", "desp": "Valid operatior: +, -, *, /, %, ^", "ap1": "", "ap2": "", "ap3": None}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>oprandvar</color>: perform math operation on a variable using a random number"):
            self.wiz_step = 2405
            self.wiz_data = {"action": "oprandvar", "title": "perform math operation on a variable using a random number", "desp": "Valid operatior: +, -, *, /, %, ^", "ap1": "", "ap2": "", "ap3": None}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>nextstatecond</color>: goto next state by condition"):
            self.wiz_step = 2406
            self.wiz_data = {"action": "nextstatecond", "title": "goto next state by condition", "desp": "If condition is true, goto 1st state, otherwise goto 2nd state.\nValid comparison operators: <, >, <=, >=, ==, !=", "ap1": "", "ap2": "", "ap3": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>timernextcond</color>: goto next state after timer by condition"):
            self.wiz_step = 2407
            self.wiz_data = {"action": "timernextcond", "title": "goto next state after timer by condition", "desp": "If condition is true, goto 1st state after timer, else 2nd state.\nValid comparison operators: <, >, <=, >=, ==, !=", "ap1": "", "ap2": "", "ap3": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>addbtncond</color>: custom button goto state by condition"):
            self.wiz_step = 2408
            self.wiz_data = {"action": "addbtncond", "title": "custom button goto state by condition", "desp": "Create button, if condition true, goto 1st state, otherwise 2nd state.\nValid comparison operators: <, >, <=, >=, ==, !=", "ap1": "", "ap2": "", "ap3": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>txtfv</color>: display a formatted string using a variable list"):
            self.wiz_step = 2409
            self.wiz_data = {"action": "txtfv", "title": "display a formatted string using a variable list", "desp": "Set value in a formatted string and display it. Ref to str.format() function for detail.", "ap1": "", "ap2": "", "ap3": ""}
            self.wiz_error = None

    elif self.wiz_step >= 2400 and self.wiz_step <= 2499:       # Blackrain commands detail
        # header line
        GUILayout.BeginHorizontal()
        GUILayout.Label("Blackrain: " + self.wiz_data["title"])
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            cmd = self.wiz_data["action"]
            if self.wiz_data["ap1"] != None: cmd += ":" + self.wiz_data["ap1"]
            if self.wiz_data["ap2"] != None: cmd += ":" + self.wiz_data["ap2"]
            if self.wiz_data["ap3"] != None: cmd += ":" + self.wiz_data["ap3"]
            append_vnss_cmd(self, cmd)
            self.wiz_step = 0
            self.wiz_error = None
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        # contents
        GUILayout.BeginHorizontal()
        if self.wiz_step == 2401:       # setvar
            GUILayout.Label("Var name: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("value: ")
            self.wiz_data["ap2"] = GUILayout.TextField(self.wiz_data["ap2"], GUILayout.Width(100))
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2402:     # setrandvar
            GUILayout.Label("Var name: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(100))
            GUILayout.Space(10)
            r = self.wiz_data["ap2"].split(",")
            if len(r) < 2: r.append("")
            GUILayout.Label("from: ")
            rmin = GUILayout.TextField(r[0], GUILayout.Width(50))
            GUILayout.Space(10)
            GUILayout.Label("to: ")
            rmax = GUILayout.TextField(r[1], GUILayout.Width(50))
            self.wiz_data["ap2"] = rmin.strip() + "," + rmax.strip()
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2403:     # setrandsumvar
            GUILayout.Label("Var name: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(100))
            GUILayout.Space(10)
            r = self.wiz_data["ap2"].split(",")
            if len(r) < 2: r.append("")
            GUILayout.Label("from: ")
            rmin = GUILayout.TextField(r[0], GUILayout.Width(50))
            GUILayout.Space(10)
            GUILayout.Label("to: ")
            rmax = GUILayout.TextField(r[1], GUILayout.Width(50))
            self.wiz_data["ap2"] = rmin.strip() + "," + rmax.strip()
            GUILayout.Space(10)
            GUILayout.Label("times: ")
            self.wiz_data["ap3"] = GUILayout.TextField(self.wiz_data["ap3"], GUILayout.Width(50))
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2404:       # opvar
            GUILayout.Label("Var name: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(100))
            GUILayout.Space(10)
            if len(self.wiz_data["ap2"]) > 0:
                op = self.wiz_data["ap2"][0]
            else:
                op = ""
            if len(self.wiz_data["ap2"]) > 0:
                vl = self.wiz_data["ap2"][1:]
            else:
                vl = ""
            GUILayout.Label("operator: ")
            op = GUILayout.TextField(op, GUILayout.Width(30))
            GUILayout.Space(10)
            GUILayout.Label("value: ")
            vl = GUILayout.TextField(vl, GUILayout.Width(50))
            self.wiz_data["ap2"] = op.strip() + vl.strip()
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2405:     # oprandvar
            GUILayout.Label("Var name: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(100))
            if len(self.wiz_data["ap2"]) > 1:
                op = self.wiz_data["ap2"][0]
                r = self.wiz_data["ap2"][1:].split(",")
                if len(r) < 2: r.append("")
                rmin = r[0]
                rmax = r[1]
            else:
                op = ""
                rmin = ""
                rmax = ""
            GUILayout.Space(10)
            GUILayout.Label("operator: ")
            op = GUILayout.TextField(op, GUILayout.Width(30))
            GUILayout.Space(10)
            GUILayout.Label("from: ")
            rmin = GUILayout.TextField(rmin, GUILayout.Width(50))
            GUILayout.Space(10)
            GUILayout.Label("to: ")
            rmax = GUILayout.TextField(rmax, GUILayout.Width(50))
            self.wiz_data["ap2"] = op.strip() + rmin.strip() + "," + rmax.strip()
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2406:     # nextstatecond
            r = self.wiz_data["ap1"].split(",")
            while len(r) < 3: r.append("")
            GUILayout.Label("Var name: ")
            vn = GUILayout.TextField(r[0], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("comparison: ")
            op = GUILayout.TextField(r[1], GUILayout.Width(30))
            GUILayout.Space(10)
            GUILayout.Label("value: ")
            vl = GUILayout.TextField(r[2], GUILayout.Width(50))
            self.wiz_data["ap1"] = vn + "," + op + "," + vl
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("1st state: ")
            self.wiz_data["ap2"] = GUILayout.TextField(self.wiz_data["ap2"], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("2nd state: ")
            self.wiz_data["ap3"] = GUILayout.TextField(self.wiz_data["ap3"], GUILayout.Width(100))
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2407:     # timernextcond
            r = self.wiz_data["ap1"].split(",")
            while len(r) < 3: r.append("")
            GUILayout.Label("Var name: ")
            vn = GUILayout.TextField(r[0], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("comparison: ")
            op = GUILayout.TextField(r[1], GUILayout.Width(30))
            GUILayout.Space(10)
            GUILayout.Label("value: ")
            vl = GUILayout.TextField(r[2], GUILayout.Width(50))
            self.wiz_data["ap1"] = vn + "," + op + "," + vl
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("timer: ")
            self.wiz_data["ap2"] = GUILayout.TextField(self.wiz_data["ap2"], GUILayout.Width(100))
            GUILayout.Label("sec")
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            r = self.wiz_data["ap3"].split(",")
            if len(r) < 2: r.append("")
            GUILayout.Label("1st state: ")
            s1 = GUILayout.TextField(r[0], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("2nd state: ")
            s2 = GUILayout.TextField(r[1], GUILayout.Width(100))
            self.wiz_data["ap3"] = s1.strip() + "," + s2.strip()
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2408:     # addbtncond
            GUILayout.Label("button texts: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(150))
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            r = self.wiz_data["ap2"].split(",")
            while len(r) < 3: r.append("")
            GUILayout.Label("Var name: ")
            vn = GUILayout.TextField(r[0], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("comparison: ")
            op = GUILayout.TextField(r[1], GUILayout.Width(30))
            GUILayout.Space(10)
            GUILayout.Label("value: ")
            vl = GUILayout.TextField(r[2], GUILayout.Width(50))
            self.wiz_data["ap2"] = vn + "," + op + "," + vl
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            r = self.wiz_data["ap3"].split(",")
            if len(r) < 2: r.append("")
            GUILayout.Label("1st state: ")
            s1 = GUILayout.TextField(r[0], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("2nd state: ")
            s2 = GUILayout.TextField(r[1], GUILayout.Width(100))
            self.wiz_data["ap3"] = s1.strip() + "," + s2.strip()
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2409:     # txtfv
            GUILayout.Label("Who say: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(200))
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("What say: ")
            self.wiz_data["ap3"] = GUILayout.TextField(self.wiz_data["ap3"], GUILayout.Width(400))
            GUILayout.FlexibleSpace()
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Var list: ")
            self.wiz_data["ap2"] = GUILayout.TextField(self.wiz_data["ap2"], GUILayout.Width(200))
            GUILayout.FlexibleSpace()
        else:   # unknown
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        # description
        GUILayout.Label(self.wiz_data["desp"])

    elif self.wiz_step == 25:       # GameUtil commands
        GUILayout.BeginHorizontal()
        GUILayout.Label("Game util ext: What do you want to do?")
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
        GUILayout.EndHorizontal()
        if GUILayout.Button("<color=#00ff00>gskin</color>: select a skin for game"):
            self.wiz_step = 2501
            self.wiz_data = {"action": "gskin", "title": "select a skin for game", "desp": "Set a skin by skin python file name, for example: skin_renpy, skin_renpymini, skin_default, skin_btnonly", "ap1": "", "ap2": None, "ap3": None}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>gskin_setattr</color>: set attribute of current skin"):
            self.wiz_step = 2502
            self.wiz_data = {"action": "gskin_setattr", "title": "set attribute of current skin", "desp": "Set an attribute of skin, refer to skin file's readme for detail of attribute", "ap1": "", "ap2": "", "ap3": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>gpersdata_save</color>: save gpersdata to disk"):
            self.wiz_step = 2503
            self.wiz_data = {"action": "gpersdata_save", "title": "save gpersdata to disk", "desp": "Save all variable in gpersdata onto disk, with [filename].dat. If successed next will goto state1 else state2. If state1 or state2 not set, just goto next state.", "ap1": "", "ap2": "", "ap3": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>gpersdata_load</color>: load gpersdata from disk"):
            self.wiz_step = 2504
            self.wiz_data = {"action": "gpersdata_load", "title": "load gpersdata from disk", "desp": "Load all variable in [filename].dat to gpersdata. If successed next will goto state1 else state2. If state1 or state2 not set, just goto next state.", "ap1": "", "ap2": "", "ap3": ""}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>gpersdata_clear</color>: Clear gpersdata and delete from disk"):
            self.wiz_step = 2505
            self.wiz_data = {"action": "gpersdata_clear", "title": "Clear gpersdata and delete from disk", "desp": "Clear all variable in gpersdata and delete [filename].dat.", "ap1": "", "ap2": None, "ap3": None}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>gpersdata_to_brvars</color>: load var from gpersdata to brVars (Blackrain ext var)"):
            self.wiz_step = 2506
            self.wiz_data = {"action": "gpersdata_to_brvars", "title": "load var from gpersdata to brVars (Blackrain ext var)", "desp": "Load listed vars (seperate by comma) from gpersdata to brVars, if no var listed, just load all.", "ap1": "", "ap2": None, "ap3": None}
            self.wiz_error = None
        if GUILayout.Button("<color=#00ff00>brvars_to_gpersdata</color>: load var from brVars (Blackrain ext var) to gpersdata"):
            self.wiz_step = 2507
            self.wiz_data = {"action": "brvars_to_gpersdata", "title": "load var from brVars (Blackrain ext var) to gpersdata", "desp": "Load listed vars (seperate by comma) from brVars to gpersdata, if no var listed, just load all.", "ap1": "", "ap2": None, "ap3": None}
            self.wiz_error = None

    elif self.wiz_step >= 2500 and self.wiz_step <= 2599:       # game util commands detail
        # header line
        GUILayout.BeginHorizontal()
        GUILayout.Label("Game util: " + self.wiz_data["title"])
        GUILayout.FlexibleSpace()
        if GUILayout.Button("<color=#00ff00>OK</color>", GUILayout.Width(60)):
            cmd = self.wiz_data["action"]
            if self.wiz_data["ap1"] != None: cmd += ":" + self.wiz_data["ap1"]
            if self.wiz_data["ap2"] != None: cmd += ":" + self.wiz_data["ap2"]
            if self.wiz_data["ap3"] != None: cmd += ":" + self.wiz_data["ap3"]
            append_vnss_cmd(self, cmd)
            self.wiz_step = 0
            self.wiz_error = None
        if GUILayout.Button("<color=#ff0000>Cancel</color>", GUILayout.Width(60)):
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        # contents
        GUILayout.BeginHorizontal()
        if self.wiz_step == 2501:       # gskin
            GUILayout.Label("Skin file name: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(150))
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2502:     # gskin_setattr
            GUILayout.Label("Skin attr: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("value: ")
            self.wiz_data["ap3"] = GUILayout.TextField(self.wiz_data["ap3"], GUILayout.Width(100))
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2503 or self.wiz_step == 2504:     # gpersdata_save / gpersdata_load
            GUILayout.Label("filename: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(100))
            GUILayout.Space(10)
            GUILayout.Label("state1: ")
            self.wiz_data["ap2"] = GUILayout.TextField(self.wiz_data["ap2"], GUILayout.Width(50))
            GUILayout.Space(10)
            GUILayout.Label("state2: ")
            self.wiz_data["ap3"] = GUILayout.TextField(self.wiz_data["ap3"], GUILayout.Width(50))
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2505:     # gpersdata_clear
            GUILayout.Label("filename: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(100))
            GUILayout.FlexibleSpace()
        elif self.wiz_step == 2506 or self.wiz_step == 2507:     # gpersdata_to_brvars / brvars_to_gpersdata
            GUILayout.Label("Var list: ")
            self.wiz_data["ap1"] = GUILayout.TextField(self.wiz_data["ap1"], GUILayout.Width(150))
            GUILayout.FlexibleSpace()
        else:   # unknown
            self.wiz_step = 0
            self.wiz_error = None
        GUILayout.EndHorizontal()
        # description
        GUILayout.Label(self.wiz_data["desp"])

    else:
        GUILayout.Label("What?")
        print "Unknown wizard step:", self.wiz_step
        self.wiz_step = 0

def render_vntext_editor(self):
    def backfunc():
        self.vnss_wizard_ui_mode = "main"
    def updfunc():
        from vntext import get_vntext_manager
        mgr = get_vntext_manager(self.game)
        cmd = "f_dyntext:::" + mgr.exportDynamicTextSetting()
        remove_vnss_cmd_startswith(self, "f_dyntext:::")
        append_vnss_cmd(self, cmd)
        self.vnss_wizard_ui_mode = "main"
        self.wiz_step = 0
        self.wiz_error = None
    from vntext import vntxt_GUI
    vntxt_GUI(self.game, backfunc, ("<color=#00ff00>Update</color>", updfunc))

def append_vnss_cmd(self, cmd):
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""

    if len(_sc.cam_addvncmds) > 0 and not _sc.cam_addvncmds.endswith("\n"):
        _sc.cam_addvncmds += "\n"
    
    _sc.cam_addvncmds += cmd

def remove_vnss_cmd_startswith(self, header):
    cmds = self.cam_addvncmds.strip().splitlines()
    for cmd in cmds:
        if cmd.startswith(header):
            cmds.remove(cmd)
    self.cam_addvncmds = "\n".join(cmds)

def analysis_vnss_cmd(cmd):
    cmds = cmd.strip().splitlines()
    acmds = []
    for c in cmds:
        org = c.strip()
        if len(org) == 0:
            continue
        params = org.split(":", 3)
        action = params[0].lower()
        aplen = len(params) - 1
        ap1 = None if aplen <= 0 else params[1]
        ap2 = None if aplen <= 1 else params[2]
        ap3 = None if aplen <= 2 else params[3]
        desp = None
        runable = False
        catelog = "other"
        error = False
        try:
            if action == "addbtn":
                if aplen == 2:
                    desp = "Custom button [%s] jumps to [%s]"%(ap1, ap2)
                else:
                    error = True
            elif action == "nextstate":
                if aplen == 1:
                    desp = "Next button jumps to [%s]"%(ap1)
                else:
                    error = True
            elif action == "timernext":
                if aplen == 2:
                    desp = "Auto jumps to [%s] after [%s] second"%(ap2, ap1)
                elif aplen == 1:
                    desp = "Auto go next after [%s] second"%(ap1)
                else:
                    error = True
            elif action == "addbtnrnd":
                if aplen == 2:
                    desp = "Random button [%s] jumps to [%s]"%(ap1, ap2)
                else:
                    error = True
            elif action == "addbtnms":
                if aplen == 2:
                    desp = "Ministate button [%s] invokes [%s]"%(ap1, ap2)
                else:
                    error = True
            elif action == "showui":
                if aplen == 0:
                    desp = "Show UI"
                else:
                    error = True
            elif action == "hideui":
                if aplen == 0:
                    desp = "Hide UI"
                elif aplen == 1:
                    desp = "Hide UI for [%s] second"%(ap1)
                else:
                    error = True
            elif action == "lockui":
                if aplen == 0:
                    desp = "Lock UI"
                elif aplen == 1:
                    desp = "Lock UI for [%s] second"%(ap1)
                else:
                    error = True
            elif action == "unlockui":
                if aplen == 0:
                    desp = "Unlock UI"
                else:
                    error = True
            elif action == "runms":
                if aplen == 1:
                    desp = "Invoke ministate [%s]"%(ap1)
                else:
                    error = True
            # vnframe ext
            elif action == "synch" or action == "f_synch" or action == "synchr" or action == "f_synchr":
                runable = True
                catelog = "vnframe"
                if aplen == 1:
                    desp = "Sync anime for [%s]"%(ap1) + (" and restart anime" if action.endswith("r") else "")
                elif aplen == 2:
                    desp = "Sync anime for [%s] with [%s]"%(ap1, ap2) + (" and restart anime" if action.endswith("r") else "")
                else:
                    error = True
            elif action == "f_height" or action == "f_breast":
                runable = True
                catelog = "vnframe"
                if aplen == 2:
                    desp = "Set [%s]'s %s = %s"%(ap1, action[2:], ap2)
                else:
                    error = True
            elif action == "f_animclipnum":
                runable = True
                catelog = "vnframe"
                if aplen == 2:
                    desp = "VNFrame: '" + org[0:35] + "...'"
                else:
                    error = True
            elif action == "f_acts" or action == "f_actm" or action == "f_act" or action == "f_anime" or action == "f_actm_j":
                runable = True
                catelog = "vnframe"
                if aplen == 3:
                    desp = "VNFrame: '" + org[0:35] + "...'"
                else:
                    error = True
            # vnanime ext
            elif action == "f_clipplay":
                runable = True
                catelog = "vnanime"
                if aplen >= 1:
                    desp = "VNAnime: Play clip [%s]"%ap1
                else:
                    desp = "VNAnime: Play all clips"
            elif action == "f_clipstop":
                runable = True
                catelog = "vnanime"
                if aplen == 0:
                    desp = "VNAnime: Stop all clips"
                elif aplen == 1:
                    desp = "VNAnime: Stop clip [%s]"%ap1
                else:
                    error = True
            elif action == "f_clippause":
                runable = True
                catelog = "vnanime"
                if aplen == 0:
                    desp = "VNAnime: Pause all clips"
                elif aplen == 1:
                    desp = "VNAnime: Pause clip [%s]"%ap1
                else:
                    error = True
            elif action == "f_clipseek":
                runable = True
                catelog = "vnanime"
                if aplen == 2:
                    desp = "VNAnime: Seek to frame [%s] of clip [%s]"%(ap2, ap1)
                else:
                    error = True
            # objcam ext
            elif action == "objcam":
                runable = True
                catelog = "objcam"
                if aplen == 1:
                    if len(ap1) > 0:
                        desp = "objcam: switch to camera [%s]"%ap1
                    else:
                        desp = "objcam: switch back to normal camera"
                else:
                    error = True
            # vntext ext
            elif action == "f_dyntext":
                runable = True
                catelog = "vntext"
                if aplen == 3:
                    try:
                        sd = eval(ap3)
                        if len(sd):
                            desp = "VNText: setup %d dynamic texts"%len(sd)
                        else:
                            desp = "VNText: clear dynamic texts"
                    except:
                        print "ap3 =", ap3
                        traceback.print_exc()
                        error = True
                else:
                    error = True
            # blackrain ext
            elif action == "txtfv":
                catelog = "blackrain"
                if aplen == 3:
                    desp = "[br] formatted texts"
                else:
                    error = True
            elif action == "nextstatecond":
                catelog = "blackrain"
                if aplen == 3:
                    desp = "[br] next goto [%s] if [%s], else goto [%s]"%(ap2, ap1.replace(",", ""), ap3)
                else:
                    error = True
            elif action == "timernextcond":
                catelog = "blackrain"
                if aplen == 3:
                    desp = "[br] goto [%s] after %ssec if [%s], else goto [%s]"%(ap3.split(",")[0], ap2, ap1.replace(",", ""), ap3.split(",")[1])
                else:
                    error = True
            elif action == "addbtncond":
                catelog = "blackrain"
                if aplen == 3:
                    desp = "[br] button [%s] jump to [%s] if [%s], else to [%s]"%(ap1, ap3.split(",")[0], ap2.replace(",", ""), ap3.split(",")[1])
                else:
                    error = True
            elif action == "setvar":
                catelog = "blackrain"
                if aplen == 2:
                    desp = "[br] set var %s = %s"%(ap1, ap2)
                else:
                    error = True
            elif action == "setrandvar":
                catelog = "blackrain"
                if aplen == 2:
                    desp = "[br] set random var %s = random(%s)"%(ap1, ap2)
                else:
                    error = True
            elif action == "setrandvar":
                catelog = "blackrain"
                if aplen == 2:
                    desp = "[br] set random var %s = random(%s)"%(ap1, ap2)
                else:
                    error = True
            elif action == "setrandsumvar":
                catelog = "blackrain"
                if aplen == 3:
                    desp = "[br] set random var %s = random(%s) x %s"%(ap1, ap2, ap3)
                else:
                    error = True
            elif action == "opvar":
                catelog = "blackrain"
                if aplen == 2:
                    desp = "[br] math operation %s = %s%s"%(ap1, ap1, ap2)
                else:
                    error = True
            elif action == "oprandvar":
                catelog = "blackrain"
                if aplen == 2:
                    desp = "[br] math operation %s = %s%srandom(%s)"%(ap1, ap1, ap2[0], ap2[1:])
                else:
                    error = True
            elif action == "timernext2" or action == "stoptimer" or action == "enablelipsync" or action == "disablelipsync" or action == "printvar":
                catelog = "blackrain"
                desp = "[br] " + action
            # gameutil
            elif action == "gskin":
                catelog = "gameutil"
                if aplen == 1:
                    desp = "Set game skin to [%s]"%ap1
                else:
                    error = True
            elif action == "gskin_setattr":
                catelog = "gameutil"
                if aplen == 3:
                    desp = "Set game skin attribute %s = %s"%(ap1, ap3)
                else:
                    error = True
            elif action == "gpersdata_save":
                catelog = "gameutil"
                if aplen >= 1:
                    desp = "Save game gpersdata to [%s]"%ap1
                else:
                    error = True
            elif action == "gpersdata_load":
                catelog = "gameutil"
                if aplen >= 1:
                    desp = "Load game gpersdata from [%s]"%ap1
                else:
                    error = True
            elif action == "gpersdata_clear":
                catelog = "gameutil"
                if aplen == 1:
                    desp = "Clear game gpersdata [%s]"%ap1
                else:
                    error = True
            elif action == "gpersdata_to_brvars":
                catelog = "gameutil"
                if aplen == 1:
                    desp = "Load vars [%s] from gpersdata to blackrain vars"%ap1
                else:
                    desp = "Load all from gpersdata to blackrain vars"
            elif action == "brvars_to_gpersdata":
                catelog = "gameutil"
                if aplen == 1:
                    desp = "Load vars [%s] from blackrain vars to gpersdata"%ap1
                else:
                    desp = "Load all from blackrain vars to gpersdata"
            # unknown
            else:
                desp = "Unknown command: %s"%org
        except:
            traceback.print_exc()
            error = True
        if error or desp == None:
            desp = action + " command with wrong syntax"
        acmds.append({"desp": desp, "org": org, "runable": runable, "catelog": catelog, "error": error, "action": action, "ap1": ap1, "ap2": ap2, "ap3": ap3, "aplen": aplen})
    return acmds

def vnframe_take_snapshot(self):
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""
    outputScript = {}
    curscn = self.block[self.cur_index]

    # diff actors
    for actId in curscn.actors.keys():
        ofs = curscn.actors[actId]
        if actId == "sys":
            from vnactor import export_sys_status
            nfs = export_sys_status(self.game)
        else:
            nfs = self.game.scenef_get_actor(actId).export_full_status()
        dfs = {}
        for key in nfs.keys():
            if not key in ofs.Keys or ofs[key] != nfs[key]:
                dfs[key] = nfs[key]
        if len(dfs) > 0:
            outputScript[actId] = dfs
    
    # diff props
    for prpId in curscn.props.keys():
        ofs = curscn.props[prpId]
        nfs = self.game.scenef_get_propf(prpId).export_full_status()
        dfs = {}
        for key in nfs.Keys:
            if not key in ofs.Keys or ofs[key] != nfs[key]:
                dfs[key] = nfs[key]
        if len(dfs) > 0:
            outputScript[prpId] = dfs

    #print "outputScript:", outputScript
    return outputScript

def vnframe_manual_start(self, acmd):
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""

    if acmd != None:
        try:
            if acmd["action"] == "f_act":
                oldScript = eval(acmd["ap3"])
            elif acmd["action"] == "f_anime":
                aniScript = eval(acmd["ap3"])
                oldScript = aniScript[0][0]
                self.wiz_temp_vnframe_manual_tgt_anime_duration = aniScript[0][1]
                self.wiz_temp_vnframe_manual_tgt_anime_style = aniScript[0][2]
        except:
            print "Fail to eval vnss cmd:", acmd
            traceback.print_exc()
            return
        self.wiz_temp_vnframe_manual_script = oldScript
        self.wiz_temp_vnframe_manual_tgt_cmd = acmd
    else:
        self.wiz_temp_vnframe_manual_script = vnframe_take_snapshot(self)
        self.wiz_temp_vnframe_manual_tgt_cmd = None

    #if len(self.wiz_data["script"]) == 0:
    #    self.wiz_data["script"] = vnframe_take_snapshot(self)
    self.wiz_temp_vnframe_scl1 = Vector2.zero
    self.wiz_temp_vnframe_scl2 = Vector2.zero
    self.wiz_temp_vnframe_auto_script = vnframe_take_snapshot(self)
    self.wiz_temp_vnframe_target_id = None
    self.wiz_temp_vnframe_target_detail = None

    self.vnss_wizard_ui_mode = "vnframe_manual"

def render_vnframe_manual(self):
    from vnanime import translateAndSortStatusKeys
    from vnactor import export_sys_status
    from vnframe import script2string
    self = self
    """:type self:SceneConsole"""
    _sc = self
    """:type _sc:SceneConsole"""

    # prepare
    game = self.game
    ascript = self.wiz_temp_vnframe_auto_script
    mscript = self.wiz_temp_vnframe_manual_script

    fullw = game.wwidth-30
    idw = 250
    btnstyle = GUIStyle("button")
    btnstyle.fontSize = 14

    def updateManualScript():
        for tid in mscript.keys():
            if tid == "sys":
                curData = export_sys_status(game)
            elif tid in game.scenef_get_all_actors():
                curData = game.scenef_get_actor(tid).export_full_status()
            elif tid in game.scenef_get_all_props():
                curData = game.scenef_get_propf(tid).export_full_status()
            else:
                print "Unexpect target id <%s>"%tid
                del mscript[tid]
                continue

            for prp in mscript[tid]:
                if prp in curData:
                    mscript[tid][prp] = curData[prp]
                else:
                    print "Unexpected property <%s> of <%s>"%(prp, tid)
                    del mscript[tid][prp]

    def clearTempVarAndReturn():
        del self.wiz_temp_vnframe_scl1
        del self.wiz_temp_vnframe_scl2
        del self.wiz_temp_vnframe_auto_script
        del self.wiz_temp_vnframe_manual_script
        del self.wiz_temp_vnframe_target_id
        del self.wiz_temp_vnframe_target_detail
        self.vnss_wizard_ui_mode = "main"

    def debugPrintScript(sc, headerTxt):
        print headerTxt
        for tid in sc.keys():
            print "  " + tid + ":"
            for prp in sc[tid].keys():
                print "    " + prp + ": " + script2string(sc[tid][prp])
        print ""

    # Titles
    GUILayout.Label("Select the actors/props and properties of what you want. Item with <color=#ff0000>" + u"\u2605" + "</color> mark indicates diff detected against base scene.")
    GUILayout.Space(10)
    GUILayout.BeginHorizontal()
    GUILayout.Label("Actors/Props", GUILayout.Width(idw))
    if self.wiz_temp_vnframe_target_id != None and self.wiz_temp_vnframe_target_detail != None:
        GUILayout.Label("Properties of <color=#00ff00>" + self.wiz_temp_vnframe_target_id + "</color>")
    else:
        GUILayout.Label("Properties")
    GUILayout.EndHorizontal()


    # main contants
    GUILayout.BeginHorizontal()
    self.wiz_temp_vnframe_scl1 = GUILayout.BeginScrollView(self.wiz_temp_vnframe_scl1, GUILayout.Width(idw))
    GUILayout.Label("<color=#00ffff>Actors:</color>")
    for aid in game.scenef_get_all_actors():
        actor = game.scenef_get_actor(aid)
        name = aid + ": " + actor.text_name
        osel = aid in mscript and len(mscript[aid]) > 0
        if osel:
            name = "<b>" + name + "</b>"
        if aid in ascript:
            name += " <color=#ff0000>" + u"\u2605" + "</color>" #" <b><color=#ff0000>*</color></b>"
        GUILayout.BeginHorizontal()
        nsel = GUILayout.Toggle(osel, "")
        if osel != nsel:
            if nsel:
                if aid in ascript:
                    mscript[aid] = ascript[aid]
                else:
                    mscript[aid] = {}
            else:
                del mscript[aid]
                self.wiz_temp_vnframe_target_id = None
                self.wiz_temp_vnframe_target_detail = None
        if GUILayout.Button(name):
            if not aid in mscript:
                mscript[aid] = {}
            self.wiz_temp_vnframe_target_id = aid
            self.wiz_temp_vnframe_target_detail = actor.export_full_status()
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()
    GUILayout.Label("<color=#00ffff>Props:</color>")
    for pid in game.scenef_get_all_props():
        prop = game.scenef_get_propf(pid)        
        name = pid + ": " + prop.text_name
        osel = pid in mscript and len(mscript[pid]) > 0
        if osel:
            name = "<b>" + name + "</b>"
        if pid in ascript:
            name += " <color=#ff0000>" + u"\u2605" + "</color>" #" <b><color=#ff0000>*</color></b>"
        GUILayout.BeginHorizontal()
        nsel = GUILayout.Toggle(osel, "")
        if osel != nsel:
            if nsel:
                if pid in ascript:
                    mscript[pid] = ascript[pid]
                else:
                    mscript[pid] = {}
            else:
                del mscript[pid]
                self.wiz_temp_vnframe_target_id = None
                self.wiz_temp_vnframe_target_detail = None
        if GUILayout.Button(name):
            if not pid in mscript:
                mscript[pid] = {}
            self.wiz_temp_vnframe_target_id = pid
            self.wiz_temp_vnframe_target_detail = prop.export_full_status()
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()
    GUILayout.Label("<color=#00ffff>System:</color>")
    sid = "sys"
    name = "sys: Scene environment"
    osel = sid in mscript and len(mscript[sid]) > 0
    if osel:
        name = "<b>" + name + "</b>"
    if sid in ascript:
        name += " <color=#ff0000>" + u"\u2605" + "</color>" #" <b><color=#ff0000>*</color></b>"
    GUILayout.BeginHorizontal()
    nsel = GUILayout.Toggle(osel, "")
    if osel != nsel:
        if nsel:
            if sid in ascript:
                mscript[sid] = ascript[sid]
            else:
                mscript[sid] = {}
        else:
            del mscript[sid]
            self.wiz_temp_vnframe_target_id = None
            self.wiz_temp_vnframe_target_detail = None
    if GUILayout.Button(name):
        if not sid in mscript:
            mscript[sid] = {}
        self.wiz_temp_vnframe_target_id = sid
        self.wiz_temp_vnframe_target_detail = export_sys_status(self.game)
    GUILayout.FlexibleSpace()
    GUILayout.EndHorizontal()
    GUILayout.EndScrollView()

    self.wiz_temp_vnframe_scl2 = GUILayout.BeginScrollView(self.wiz_temp_vnframe_scl2)
    if self.wiz_temp_vnframe_target_id != None and self.wiz_temp_vnframe_target_detail != None:
        sortIds, idDict = translateAndSortStatusKeys(self.wiz_temp_vnframe_target_detail.keys())
        for sid in sortIds:
            name = idDict[sid]
            osel = sid in mscript[self.wiz_temp_vnframe_target_id]
            if osel:
                name = "<b>" + name + "</b>"
            if (self.wiz_temp_vnframe_target_id in ascript) and (sid in ascript[self.wiz_temp_vnframe_target_id]):
                name +=  " <color=#ff0000>" + u"\u2605" + "</color>"
            GUILayout.BeginHorizontal()
            nsel = GUILayout.Toggle(osel, name)
            if osel != nsel:
                if nsel:
                    mscript[self.wiz_temp_vnframe_target_id][sid] = self.wiz_temp_vnframe_target_detail[sid]
                    #print "vnframe manual add: %s[%s] = %s"%(self.wiz_temp_vnframe_target_id, sid, str(self.wiz_temp_vnframe_target_detail[sid]))
                else:
                    del mscript[self.wiz_temp_vnframe_target_id][sid]
            GUILayout.EndHorizontal()
    else:
        GUILayout.BeginHorizontal()
        GUILayout.Label("Select a actor/prop to check detail.")
        GUILayout.FlexibleSpace()
        GUILayout.EndHorizontal()
    GUILayout.EndScrollView()
    GUILayout.EndHorizontal()

    # tail button
    GUILayout.Space(10)
    GUILayout.BeginHorizontal()
    if GUILayout.Button("OK"):
        updateManualScript()
        debugPrintScript(mscript, "VNFrame manual mode output:")
        if self.wiz_temp_vnframe_manual_tgt_cmd:
            if self.wiz_temp_vnframe_manual_tgt_cmd["action"] == "f_act":
                cmd = "f_act:::%s"%script2string(mscript).replace(" ", "").strip()
            else:
                aniScript = ((mscript, self.wiz_temp_vnframe_manual_tgt_anime_duration, self.wiz_temp_vnframe_manual_tgt_anime_style), )
                cmd = "f_anime:::%s"%script2string(aniScript).replace(" ", "").strip()
            remove_vnss_cmd_startswith(self, self.wiz_temp_vnframe_manual_tgt_cmd["org"])
            append_vnss_cmd(self, cmd)
        else:
            self.wiz_data["script"] = mscript
            if len(mscript) > 0:
                self.wiz_error = None
        clearTempVarAndReturn()
    if GUILayout.Button("Rescan Diff"):
        self.wiz_temp_vnframe_auto_script = vnframe_take_snapshot(self)
    if GUILayout.Button("Auto Snapshot"):
        self.wiz_temp_vnframe_manual_script = vnframe_take_snapshot(self)
        self.wiz_temp_vnframe_target_id = None
        self.wiz_temp_vnframe_target_detail = None
    if GUILayout.Button("Cancel"):
        clearTempVarAndReturn()
    GUILayout.EndHorizontal()

def runVNSSExtCmd(game, vncmd):
    try:
        if not vncmd["runable"]:
            return False

        # parse act
        ar = vncmd["org"].split(":", 3)
        act = {}
        act["origintext"] = vncmd["org"]
        act["action"] = ar[0]
        if len(ar) > 1:
            act["actionparam"] = ar[1]
            if len(ar) > 2:
                act["actionparam2"] = ar[2]
                if len(ar) > 3:
                    act["actionparam3"] = ar[3]

        # run vnss
        if vncmd["catelog"] == "vnframe":
            from vnscenescriptext_vnframe12 import custom_action
            return custom_action(game, act)
        if vncmd["catelog"] == "vnanime":
            from vnscenescriptext_vnanime10 import custom_action
            return custom_action(game, act)
        if vncmd["catelog"] == "vntext":
            from vnscenescriptext_vntext10 import custom_action
            return custom_action(game, act)
        if vncmd["catelog"] == "objcam":
            from vnscenescriptext_objcam10 import custom_action
            return custom_action(game, act)
        return False

    except:
        traceback.print_exc()
        return False
