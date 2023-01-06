"""
PoseSaveState for All engines (Implemented in SceneSaveState as "Pose Library")
Based on PoseConsole for HS StudioNeo (Implemented in SceneConsole as "Pose Library") (by @chickenmanX)
v3.0
Plugin for management of pose library

2.0
- changed PoseConsoleUIData to direct use folders
- fixed bug with tx names
- moved folders to sss/fposes, sss/mposes
- change logic to use classes
- add faces save/load
2.1
- fix bug: empty Tags during save will lead to Base tag, not error
- X buttons for text fields during save
2.2
- Fix bug with no MFaces tab
3.0
- Support save: FStatus, MStatus, Left hand, Right hand
"""
from vngameengine import HSNeoOCIFolder, HSNeoOCI
from vnactor import *
from Studio import OICharInfo
from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Vector2, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject
from System import String, Array

from System import Single, Byte
from json import encoder
import json
from array import array
#import extplugins
#[116,153 except 122,123]
#Instance of pose console
_pc = None

# :::::::::: JSON Derulo ::::::::::::
encoder.FLOAT_REPR = lambda o: format(o, '.3f')
from libjsoncoder import *

# :::::::::: Main console ::::::::::::
def start(game):
    toggle_pose_console(game)

class PoseConsoleUIData():
    def __init__(self, basefold = None, groupose_flag = False):
        self.toolbarInt = 0
        self.basefold = basefold

        # --- Load screen --- 
        self.ldscrollPos = Vector2(0,0)
        self.ldtagscrollpos = Vector2(0,0)
        self.ldgrpscrollpos = Vector2(0,0)
        
        self.ldsearchstr = ""
        self.ldbyTag = False
        self.ldbyGrp = False

        self.ldTags = []
        self.ldTagsBckup = []
        self.ldTagTgl = []
        self.ldGroup = ""
        
        # --- Save screen ---
        self.svscrollPos = Vector2(0,0)
        self.svtagscrollpos = Vector2(0,0)
        self.svgrpscrollpos = Vector2(0,0)
        self.svsearchstr = ""
        self.svtagstr = ""
        self.svgrpstr = ""   
        self.svTagTgl = []
        
        # --- Replace screen --- 
        self.rep_scrollPos = Vector2(0,0)
        self.rep_tagscrollpos = Vector2(0,0)
        self.rep_grpscrollpos = Vector2(0,0)
        self.rep_searchstr = ""
        self.rep_tagstr = ""
        self.rep_grpstr = ""   
        self.rep_TagTgl = []
        
        self.loaded_pose = None # pose key from load scren
        self.rep_do_init = False
        self.rep_do = False
        
        # --- Lib --- 
        self.taglib = []
        self.lib = {"None":{},}
        self.y_offset = 0
        
        # --- Pose fetch ---
        self.getAllPoses()
        self.getAllTags()
        self.getTagIndex()

        # --- Color data ---
        self.nortgcol = "#f9f9f9"
        self.sptgcol = "#42d4f4" 
        
    def getAllPoses(self):
        import os

        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        


            
        basefolder_path = os.path.join(script_dir, self.basefold)
        itemlist = os.listdir(basefolder_path)

        #poselib = {}
        #print itemlist
        ext = ".txt"
        for item in itemlist:
            if os.path.isdir(basefolder_path+item):
                if not item in self.lib.Keys:
                    self.lib[item] = {}
                sub_fld_path = os.path.join(basefolder_path,(item+"/"))
                filelist = os.listdir(sub_fld_path)
                for file in filelist:
                    if ext in file:
                        #posename = file.strip('.txt')
                        posename = file[0:-4]
                        file_path = sub_fld_path+file
                        
                        f = open(file_path)
                        self.lib[item][posename] = json.loads(f.read(), object_hook = sceneDecoder)
                        f.close()
            elif ext in item:
                posename = item[0:-4]
                file_path = os.path.join(basefolder_path, item)
                
                f = open(file_path)
                self.lib["None"][posename] = json.loads(f.read(), object_hook = sceneDecoder)
                f.close()
    
    def getAllTags(self):
        #taglib = []
        for grp in self.lib.values():
            for pose in grp.Keys:
                if not grp[pose]["tags"] == [""]:
                    tags = grp[pose]["tags"]
                    self.taglib = addItems(tags, self.taglib)
        # Something Heels/flats on top
        #ntaglib = ["Heels","Flats"]
        #ntaglib = ["Heels", "Flats"]
        ntaglib = ["Base", "Sexy"]
        #ntaglib = []
        for tg in self.taglib:
            if not tg.lower() == "base" and not tg.lower() == "sexy" :
                ntaglib.append(tg)
        
        self.taglib = ntaglib
            #return self.taglib
      
    
    def getTagIndex(self):
        self.ldTagTgl = []
        self.svTagTgl = []
        self.rep_TagTgl = []
            
        for i in range (0,len(self.taglib)):
            self.ldTagTgl.append(False)
            self.svTagTgl.append(False)
            self.rep_TagTgl.append(False)
            
    def getRepTagIndex(self):
        self.rep_TagTgl = []
        for i in range (0,len(self.taglib)):
            self.rep_TagTgl.append(False)
            

    # base function to override
    def savePoseData(self, name, tags, group, offset_flag = False, rep_loaded = False):
        return None

    #Save Pose
    def savePose(self, name, tags, group, offset_flag = False, rep_loaded = False):

        data = self.savePoseData(name, tags, group, offset_flag , rep_loaded)

        if data == None:
            return None

        import os


                    
        tags = tags.replace(" ","")

        # avoid bugs if str is empty
        if tags == "":
            tags = "Base,"

        if tags[-1] == ",":
            tags = tags[0:-1]
        tags = tags.split(",")

        #dict = {"pose" : pose, "tags" : tags, "group" : group}
        dict = {"pose" : data, "tags" : tags}
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in


        folder_path = os.path.join(script_dir,self.basefold)

        #Group (make folder)
        if not group == "":
            folder_path = os.path.join(folder_path,(group + "/"))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

        file_path = os.path.join(folder_path, (str(name)+".txt"))

        # If replace
        if rep_loaded == True:
            if not str(self.loaded_pose[0]) == str(name):
                old_file_path = folder_path + str(self.loaded_pose[0]) + ".txt"
                abs_old_file_path = os.path.join(script_dir, old_file_path)
                os.rename(abs_old_file_path,file_path)

        f=open(file_path,"w")
        f.write(json.dumps(dict, cls = SceneEncoder))#, indent = 4, separators = (","," : ")))
        f.close()
        #toSelect(game)

        #Add pose to PoseLib
        if rep_loaded == True:
            loaded_name = self.loaded_pose[0]
            loaded_grp = self.loaded_pose[1]
            self.lib[loaded_grp].pop(loaded_name)
        if group == "":
            self.lib["None"][name] = dict
        elif group not in self.lib.Keys:
            self.lib[group] = {}
            self.lib[group][name] = dict
        else:
            self.lib[group][name] = dict
        self.getAllTags()
        self.getTagIndex()
        
    def checkTags(self, grp, name):
        if (set(list(map(lambda x: x.lower(),self.ldTags))) <= set(list(map(lambda x: x.lower(),self.lib[grp][name]["tags"])))):
            return True
        else:
            return False

    def prepReplace(self, pose_name, grp_name):
        self.loaded_pose = (pose_name, grp_name)
        self.rep_do_init = True

    def replaceInit(self):
        if self.rep_do_init == True:
            pose_name = self.loaded_pose[0]
            grp_name = self.loaded_pose[1]
            if isinstance(self.loaded_pose,tuple):
                self.rep_searchstr = pose_name
                if grp_name == "None":
                    self.rep_grpstr = ""
                else:
                    self.rep_grpstr = grp_name    
                
                self.getRepTagIndex()
                tags = self.lib[grp_name][pose_name]["tags"]
                if len(tags) > 0:
                    for tag in tags:
                        for i in range(0,len(self.taglib)):
                            if tag.lower() == self.taglib[i].lower():
                                self.rep_TagTgl[i] = True
                            #else:
                                #self.rep_TagTgl[i] = False
                self.rep_do = True
                self.rep_do_init = False

    def applyState(self, state):
        applyStateNormal(state)

class UIDataPoses(PoseConsoleUIData):
    def savePoseData(self, name, tags, group, offset_flag = False, rep_loaded = False):
        char = get_selected_objs(_pc.game)
        if not char == None:
            char = char[0]
            state = char.export_full_status()

            pose = {}
            poseKeys = ["kinematic", "anim", "anim_spd", "anim_ptn", "anim_lp", "ik_active",
                        "ik_set", "fk_active", "face_to", "rotate_to", "hands"]
            if state["face_to"] == 4:
                poseKeys.append("face_to_full")

            # --- Creating dictionary ---
            for key in poseKeys:
                if key in state:
                    pose[key] = state[key]

            if offset_flag == True:
                pose["y_offset"] = state["move_to"][1]
                # Y offset backup
                if char.sex == 1:
                    self.y_offset = state["move_to"][1]

            # Exclude head fk nodes
            pose["fk_set"] = excludeFK(state["fk_set"])

            return pose

        return None


class UIDataFPoses(UIDataPoses):
    def __init__(self):
        PoseConsoleUIData.__init__(self, "sss/fposes/")

class UIDataMPoses(UIDataPoses):
    def __init__(self):
        PoseConsoleUIData.__init__(self, "sss/mposes/")

class UIDataFaces(PoseConsoleUIData):
    def savePoseData(self, name, tags, group, offset_flag = False, rep_loaded = False):
        char = get_selected_objs(_pc.game)
        if not char == None:
            char = char[0]
            state = char.export_full_status()

            pose = {}
            poseKeys = ["eyes", "eyes_blink", "eyes_open", "face_red", "look_at_pos", "look_at_ptn",
                        "mouth", "mouth_open", "tear"]
            if _pc.game.isCharaStudio:
                poseKeys.append("eyebrow")

            # --- Creating dictionary ---
            for key in poseKeys:
                if key in state:
                    pose[key] = state[key]
            return pose

        return None

class UIDataFFaces(UIDataFaces):
    def __init__(self):
        PoseConsoleUIData.__init__(self, "sss/ffaces/")

class UIDataMFaces(UIDataFaces):
    def __init__(self):
        PoseConsoleUIData.__init__(self, "sss/mfaces/")

class UIDataStatus(PoseConsoleUIData):
    def savePoseData(self, name, tags, group, offset_flag = False, rep_loaded = False):
        char = get_selected_objs(_pc.game)
        if not char == None:
            char = char[0]
            state = char.export_full_status()

            del state["visible"]
            del state["rotate_to"]
            del state["move_to"]
            del state["scale_to"]
            return state

        return None



    def applyState(self, state):
        applyStateNormalDiffOpt(state)

class UIDataFStatus(UIDataStatus):
    def __init__(self):
        PoseConsoleUIData.__init__(self, "sss/fstatus/")

class UIDataMStatus(UIDataStatus):
    def __init__(self):
        PoseConsoleUIData.__init__(self, "sss/mstatus/")

class UIDataHands(PoseConsoleUIData):
    def savePoseData(self, name, tags, group, offset_flag = False, rep_loaded = False):
        char = get_selected_objs(_pc.game)
        if not char == None:
            char = char[0]
            state = char.export_full_status()

            pose = {}
            poseKeys = ["kinematic", "hands", "fk_set", "fk_active", "ik_active", "ik_set"]

            # --- Creating dictionary ---
            for key in poseKeys:
                if key in state:
                    pose[key] = state[key]
            return pose

        return None

    def applyState(self, state):
        global _pc
        char = get_selected_objs(_pc.game)
        if not char == None:
            char = char[0]
            self.applyStateChar(char,state)

    def applyStateChar(self, char, state):
        global _pc
        kin = char.get_kinematic()
        if kin == 2 or kin == 3:
            # ok
            self.applyStateChar2(char,state)
        else:
            _pc.show_blocking_message_time_pc("Load works only if char in FK or FK&IK state")

    def applyStateChar2(self, char, state):
        pass

class UIDataLHand(UIDataHands):
    def __init__(self):
        PoseConsoleUIData.__init__(self, "sss/lhand/")
    # def applyState(self, state):
    #     applyStateLHand(state)

    def applyStateChar2(self, char, state):
        do_exist = False

        lhand_keys = [i for i in range(37,52)]
        #if lhand_keys <= state["fk_set"].keys():
        lhand_fk = {}
        for i in lhand_keys:
            if i in state["fk_set"].keys():
                lhand_fk[i] = state["fk_set"][i]
                do_exist = True
        if do_exist == True:
            char.set_FK_active(group = 5, active = 1)
            char.import_fk_bone_info(lhand_fk)

class UIDataRHand(UIDataHands):
    def __init__(self):
        PoseConsoleUIData.__init__(self, "sss/rhand/")
    # def applyState(self, state):
    #     applyStateRHand(state)

    def applyStateChar2(self, char, state):
        do_exist = False

        rhand_keys = [i for i in range(22,37)]
        #if rhand_keys <= state["fk_set"].keys():
        rhand_fk = {}
        for i in rhand_keys:
            if i in state["fk_set"].keys():
                rhand_fk[i] = state["fk_set"][i]
                do_exist = True
        if do_exist == True:
            char.set_FK_active(group = 4, active = 1)
            char.import_fk_bone_info(rhand_fk)

class PoseConsole():
    def __init__(self,game):
        # --- Some constants/strings ---
        self._normalwidth = 500
        self._normalheight = 350
        #self.drag_rect = Rect(0, 0, 10000, 50)
        self.options = Array[String](("Load screen","Save screen","Replace"))
        self.hoptions = Array[String](("Load screen","Save screen")) 
        
        # --- Basic settings ---
        self.game = game
        self.originalwindowwidth = 0
        self.originalwindowheight = 0
        self.originalWindowCallback = None
        self.guiOnShow = False
        self.windowwidth = self._normalwidth
        self.windowheight = self._normalheight
        self.windowindex = 0
        
        # --- Colors ---
        self.col_grp = "#f442dc"
        self.col_pmatch = "#f9f9f9" #"#42f4f4"
        self.col_match = "#f4424e"
        self.col_loaded = self.col_match
        
        # --- Init UI data ---
        #self.fconsole = PoseConsoleUIData(basefold="sss/fposes/")
        #self.mconsole = PoseConsoleUIData(basefold="sss/mposes/")
        self.fconsole = UIDataFPoses()
        self.mconsole = UIDataMPoses()

        self.ffaces = UIDataFFaces()
        self.mfaces = UIDataMFaces()

        self.fstatus = UIDataFStatus()
        self.mstatus = UIDataMStatus()

        self.lhand = UIDataLHand()
        self.rhand = UIDataRHand()

        # blocking message
        self.funcLockedText = "..."
        self.isFuncLocked = False

    # Blocking message functions
    def show_blocking_message(self, text="..."):
        self.funcLockedText = text
        self.isFuncLocked = True

    def hide_blocking_message(self, game=None):
        self.isFuncLocked = False

    def show_blocking_message_time_pc(self, text="...", duration=3):
        self.show_blocking_message(text)
        self.game.set_timer(duration, self.hide_blocking_message)

    #self.hconsole = HandConsoleUIData()
        
        # --- Additional modifiers ---
        #self.fk_exc = self.init_fkexclude()
        
    # def init_fkexclude(self):
    #     a = []
    #     for i in range(116,154):
    #         if not i == 122 and not i == 123:
    #             a.append(i)
    #     return (a)
        
# lib must be list      
def addItems(items, lib):
    for item in items:
        if item.lower() not in list(map(lambda x:x.lower(),lib)):
            lib.append(item)
    return lib
        
def init_from_sc(game):
    global _pc
    if _pc == None:
        _pc = PoseConsole(game)
    return _pc
        
def toggle_pose_console(game):
    global _pc
    if _pc == None:
        _pc = PoseConsole(game)
        
    if _pc.guiOnShow:
        poseConsoleGUIClose()
    else:
        poseConsoleGUIStart(game)

        
def poseConsoleGUIStart(game):
    global _pc

    _pc.game_skin_saved = game.skin

    from skin_customwindow import SkinCustomWindow
    skin = SkinCustomWindow()
    skin.funcSetup = poseConsoleSkinSetup
    skin.funcWindowGUI = poseConsoleSkinWindowGUI
    game.skin_set(skin)

    _pc.guiOnShow = True
    

def poseConsoleSkinSetup(game):
    setWindowName(_pc.windowindex)
    from UnityEngine import GUI, Screen, Rect
    game.wwidth = _pc.windowwidth
    game.wheight = _pc.windowheight
    #game.windowRect = Rect (Screen.width / 2 - game.wwidth / 2, Screen.height - game.wheight - 10, game.wwidth, game.wheight)
    game.windowRect = Rect(Screen.width / 2 - game.wwidth * 1.5, Screen.height - game.wheight - 500, game.wwidth - 50,
                           game.wheight + 200)
    #game.windowCallback = GUI.WindowFunction(scriptHelperWindowGUI)
    game.windowStyle = game.windowStyleDefault

def poseConsoleSkinWindowGUI(game,windowid):
    poseConsoleWindowFunc(windowid)

def poseConsoleGUIClose():
    global _pc

    _pc.guiOnShow = False
    _pc.game.windowName = ""

    _pc.game.skin_set(_pc.game_skin_saved)


# def setWindowName(index):
#     global _pc
#     names = {
#         0 : "FPoses",
#         1 : "MPoses",
#         2 : "FFaces",
#         3 : "MFaces"
#     }
#
#     if index in names.Keys:
#         _pc.windowindex = index
#         _pc.game.windowName = names[index]
#     else:
#         print "Invalid index:", index

def setWindowName(index):
    _pc.windowindex = index

def poseConsoleWindowFunc(windowid):
    global _pc
    #options = Array[String](("Load screen","Save screen","Replace"))
    try:
        poseConsoleUIFuncs()
    except Exception as e:
        import traceback
        print "PoseConsoleWindowGUI Exception:"
        traceback.print_exc()
        poseConsoleGUIClose()
        _pc.game.show_blocking_message_time("Pose console error: "+str(e))

def poseRenderButtons():
    GUILayout.BeginVertical()
    if GUILayout.Button("FPoses"):
        setWindowName(0)
    if GUILayout.Button("MPoses"):
        setWindowName(1)
    GUILayout.EndVertical()

    GUILayout.BeginVertical()
    if GUILayout.Button("FFaces"):
        setWindowName(2)
    if GUILayout.Button("MFaces"):
        setWindowName(3)
    GUILayout.EndVertical()

    GUILayout.BeginVertical()
    if GUILayout.Button("FStatus"):
        setWindowName(4)
    if GUILayout.Button("MStatus"):
        setWindowName(5)
    GUILayout.EndVertical()

    GUILayout.BeginVertical()
    if GUILayout.Button("Left hand"):
        setWindowName(6)
    if GUILayout.Button("Right hand"):
        setWindowName(7)
    GUILayout.EndVertical()

def poseConsoleUIFuncs():
    global _pc

    # global msg
    if _pc.isFuncLocked == True:
        GUILayout.BeginVertical()
        GUILayout.Space(10)
        GUILayout.BeginHorizontal()
        GUILayout.Space(10)
        GUILayout.Label("<size=20>"+_pc.funcLockedText+"</size>")
        # GUILayout.Label(_sc.funcLockedText)
        GUILayout.Space(10)
        GUILayout.EndHorizontal()
        GUILayout.Space(10)
        GUILayout.EndVertical()
        return

    options = _pc.options
    hoptions = _pc.hoptions
    
    GUILayout.BeginVertical()
    if _pc.windowindex == 0: #FPoses
        _pc.fconsole.toolbarInt = GUILayout.Toolbar(_pc.fconsole.toolbarInt,options)
        if _pc.fconsole.toolbarInt == 0: #Load
            _pc.fconsole = poseConsoleLoadWindow(_pc.fconsole)
        elif _pc.fconsole.toolbarInt == 1: #Save
            _pc.fconsole = poseConsoleSaveWindow(_pc.fconsole)
        elif _pc.fconsole.toolbarInt == 2: #Replace
            _pc.fconsole = poseConsoleReplaceWindow(_pc.fconsole)
            
        GUILayout.BeginHorizontal()
        poseRenderButtons()
        #if GUILayout.Button("Close window",GUILayout.Width(120)):
            #poseConsoleGUIClose()  
            #toggle_pose_console(_pc.game)
        # elif GUILayout.Button("Hands"):
        #     setWindowName(2)
        GUILayout.EndHorizontal()
         
        
    elif _pc.windowindex == 1: #MPoses
        _pc.mconsole.toolbarInt = GUILayout.Toolbar(_pc.mconsole.toolbarInt,options)
        if _pc.mconsole.toolbarInt == 0: #Load
            _pc.mconsole = poseConsoleLoadWindow(_pc.mconsole)
        elif _pc.mconsole.toolbarInt == 1: #Save
            _pc.mconsole = poseConsoleSaveWindow(_pc.mconsole)
        elif _pc.mconsole.toolbarInt == 2: #Replace
            _pc.mconsole = poseConsoleReplaceWindow(_pc.mconsole)
        
        GUILayout.BeginHorizontal()
        poseRenderButtons()
        # elif GUILayout.Button("Hands"):
        #     setWindowName(2)
        #if GUILayout.Button("Close window",GUILayout.Width(120)):
            #GUILayout.Label("Go to SceneConsole tab and close...")
            #poseConsoleGUIClose()    
        GUILayout.EndHorizontal()

    elif _pc.windowindex == 2:  # FFaces
        _pc.ffaces.toolbarInt = GUILayout.Toolbar(_pc.ffaces.toolbarInt, options)
        if _pc.ffaces.toolbarInt == 0:  # Load
            _pc.ffaces = poseConsoleLoadWindow(_pc.ffaces)
        elif _pc.ffaces.toolbarInt == 1:  # Save
            _pc.ffaces = poseConsoleSaveWindow(_pc.ffaces)
        elif _pc.ffaces.toolbarInt == 2:  # Replace
            _pc.ffaces = poseConsoleReplaceWindow(_pc.ffaces)

        GUILayout.BeginHorizontal()
        poseRenderButtons()
        GUILayout.EndHorizontal()

    elif _pc.windowindex == 3:  # MFaces
        _pc.mfaces.toolbarInt = GUILayout.Toolbar(_pc.mfaces.toolbarInt, options)
        if _pc.mfaces.toolbarInt == 0:  # Load
            _pc.mfaces = poseConsoleLoadWindow(_pc.mfaces)
        elif _pc.mfaces.toolbarInt == 1:  # Save
            _pc.mfaces = poseConsoleSaveWindow(_pc.mfaces)
        elif _pc.mfaces.toolbarInt == 2:  # Replace
            _pc.mfaces = poseConsoleReplaceWindow(_pc.mfaces)

        GUILayout.BeginHorizontal()
        poseRenderButtons()
        GUILayout.EndHorizontal()

    elif _pc.windowindex == 4:  # FStatus
        _pc.fstatus.toolbarInt = GUILayout.Toolbar(_pc.fstatus.toolbarInt, options)
        if _pc.fstatus.toolbarInt == 0:  # Load
            _pc.fstatus = poseConsoleLoadWindow(_pc.fstatus)
        elif _pc.fstatus.toolbarInt == 1:  # Save
            _pc.fstatus = poseConsoleSaveWindow(_pc.fstatus)
        elif _pc.fstatus.toolbarInt == 2:  # Replace
            _pc.fstatus = poseConsoleReplaceWindow(_pc.fstatus)

        GUILayout.BeginHorizontal()
        poseRenderButtons()
        GUILayout.EndHorizontal()

    elif _pc.windowindex == 5:  # MStatus
        _pc.mstatus.toolbarInt = GUILayout.Toolbar(_pc.mstatus.toolbarInt, options)
        if _pc.mstatus.toolbarInt == 0:  # Load
            _pc.mstatus = poseConsoleLoadWindow(_pc.mstatus)
        elif _pc.mstatus.toolbarInt == 1:  # Save
            _pc.mstatus = poseConsoleSaveWindow(_pc.mstatus)
        elif _pc.mstatus.toolbarInt == 2:  # Replace
            _pc.mstatus = poseConsoleReplaceWindow(_pc.mstatus)

        GUILayout.BeginHorizontal()
        poseRenderButtons()
        GUILayout.EndHorizontal()

    elif _pc.windowindex == 6:  # LHand
        _pc.lhand.toolbarInt = GUILayout.Toolbar(_pc.lhand.toolbarInt, options)
        if _pc.lhand.toolbarInt == 0:  # Load
            _pc.lhand = poseConsoleLoadWindow(_pc.lhand)
        elif _pc.lhand.toolbarInt == 1:  # Save
            _pc.lhand = poseConsoleSaveWindow(_pc.lhand)
        elif _pc.lhand.toolbarInt == 2:  # Replace
            _pc.lhand = poseConsoleReplaceWindow(_pc.lhand)

        GUILayout.BeginHorizontal()
        poseRenderButtons()
        GUILayout.EndHorizontal()

    elif _pc.windowindex == 7:  # RHand
        _pc.rhand.toolbarInt = GUILayout.Toolbar(_pc.rhand.toolbarInt, options)
        if _pc.rhand.toolbarInt == 0:  # Load
            _pc.rhand = poseConsoleLoadWindow(_pc.rhand)
        elif _pc.rhand.toolbarInt == 1:  # Save
            _pc.rhand = poseConsoleSaveWindow(_pc.rhand)
        elif _pc.rhand.toolbarInt == 2:  # Replace
            _pc.rhand = poseConsoleReplaceWindow(_pc.rhand)

        GUILayout.BeginHorizontal()
        poseRenderButtons()
        GUILayout.EndHorizontal()

    GUILayout.EndVertical()
    GUI.DragWindow()

def poseConsoleLoadWindow(console):
    global _pc
    
    #if _pc.windowindex == 0:
    if isinstance(console.loaded_pose,tuple):    
        GUILayout.Label("Search by:                                    <color=#ffbb99>(Last loaded: %s)</color>"%(console.loaded_pose[0]))
    else:
        GUILayout.Label("Search by:")
    GUILayout.BeginHorizontal()
    console.ldsearchstr = GUILayout.TextField(console.ldsearchstr,GUILayout.Width(200))
      
    console.ldbyTag = GUILayout.Toggle(console.ldbyTag,"Tag:",GUILayout.Width(120))
    console.ldbyGrp = GUILayout.Toggle(console.ldbyGrp,"Group: "+console.ldGroup,GUILayout.Width(160))
    GUILayout.EndHorizontal()
        
    GUILayout.BeginHorizontal()
            
    console.ldscrollPos = GUILayout.BeginScrollView(console.ldscrollPos,GUILayout.Width(200)) #,GUILayout.Width(250),GUILayout.Height(300))
    if console.ldGroup == "": 
        for grp in console.lib.Keys:
            if grp == "None":
                grp_name = ""
            else:
                grp_name = grp
            for name in sorted(console.lib[grp]):
                if name.lower().startswith(console.ldsearchstr.lower()) and console.checkTags(grp, name):
                    if GUILayout.Button("%s  <color=%s><b>%s</b></color>"%(name,_pc.col_grp,grp_name)):
                        console.applyState(console.lib[grp][name]["pose"])
                        console.prepReplace(name,grp) #Replace prep
                elif console.ldsearchstr == "" and console.checkTags(grp, name):
                    if GUILayout.Button("%s  <color=%s><b>%s</b></color>"%(name,_pc.col_grp,grp_name)):
                        console.applyState(console.lib[grp][name]["pose"])
                        console.prepReplace(name,grp)
    else:
        grp = console.ldGroup
        if grp == "None":
            grp_name = ""
        else:
            grp_name = grp
        for name in sorted(console.lib[grp]):
            if name.lower().startswith(console.ldsearchstr.lower()) and console.checkTags(grp, name):
                if GUILayout.Button("%s  <color=%s><b>%s</b></color>"%(name,_pc.col_grp,grp_name)):
                    console.applyState(console.lib[grp][name]["pose"])
                    console.prepReplace(name,grp)
            elif console.ldsearchstr == "" and console.checkTags(grp, name):
                if GUILayout.Button("%s  <color=%s><b>%s</b></color>"%(name,_pc.col_grp,grp_name)):
                    console.applyState(console.lib[grp][name]["pose"])
                    console.prepReplace(name,grp)
    GUILayout.EndScrollView()
           
    # If "Tags" toggle is on
    if console.ldbyTag == True:
        console.ldTags = console.ldTagsBckup
        console.ldtagscrollpos = GUILayout.BeginScrollView(console.ldtagscrollpos)
        for i in range (0,len(console.taglib)):
            if i == 0 or i == 1: col = console.sptgcol
            else: col = console.nortgcol 
            console.ldTagTgl[i] = GUILayout.Toggle(console.ldTagTgl[i],"<color=%s>%s</color>"%(col,console.taglib[i]))
            
            if (console.ldTagTgl[i] == True) and console.ldTags.count(console.taglib[i]) == 0:
                console.ldTags.append(console.taglib[i])
            elif (console.ldTagTgl[i] == False) and console.ldTags.count(console.taglib[i]) == 1:
                console.ldTags.remove(console.taglib[i])
        GUILayout.EndScrollView()
        console.ldTagsBckup = console.ldTags
            
    elif console.ldbyTag == False:
        console.ldTags = []
           
    # If "Groups" toggle is on
    if console.ldbyGrp == True:
        console.ldgrpscrollpos = GUILayout.BeginScrollView(console.ldgrpscrollpos)  
        if GUILayout.Button("None"):
            console.ldGroup = "None"
        for grp in console.lib.Keys:
            if not grp == "None": 
                if GUILayout.Button(grp):
                    console.ldGroup = grp
        GUILayout.EndScrollView()
    elif console.ldbyGrp == False:
        console.ldGroup = ""
    GUILayout.EndHorizontal()    
    #if GUILayout.Button("Save"):
        #savePose(console.ldsearchstr)          

    return console
    
def poseConsoleSaveWindow(console):
    global _pc
        
    #if _pc.windowindex == 0:
    GUILayout.Label("Save as:")
        
    GUILayout.BeginHorizontal()
    GUILayout.Label("Name:",GUILayout.Width(60))
    console.svsearchstr = GUILayout.TextField(console.svsearchstr,GUILayout.Width(230))
    if GUILayout.Button("X", GUILayout.Width(20)):
        console.svsearchstr = ""
    if GUILayout.Button("Save"):
        console.savePose(console.svsearchstr,console.svtagstr,console.svgrpstr)
    GUILayout.EndHorizontal()
      
    GUILayout.BeginHorizontal()
    GUILayout.Label("with Tags:",GUILayout.Width(60))
    console.svtagstr = GUILayout.TextField(console.svtagstr,GUILayout.Width(230))
    if GUILayout.Button("X", GUILayout.Width(20)):
        console.svtagstr = ""
    if GUILayout.Button("Save w/ y-offset"):
        console.savePose(console.svsearchstr,console.svtagstr,console.svgrpstr,offset_flag = True)
    GUILayout.EndHorizontal()

    GUILayout.BeginHorizontal()
    GUILayout.Label("in Group:",GUILayout.Width(60))
    console.svgrpstr = GUILayout.TextField(console.svgrpstr,GUILayout.Width(230))
    if GUILayout.Button("X", GUILayout.Width(20)):
        console.svgrpstr = ""
    GUILayout.EndHorizontal()

    GUILayout.BeginHorizontal()
      
    GUILayout.BeginVertical()
    GUILayout.Label("",GUILayout.Width(80)) #<b>Files:</b>
    console.svscrollPos = GUILayout.BeginScrollView(console.svscrollPos,GUILayout.Width(170)) #,GUILayout.Width(250),GUILayout.Height(300))
    for grp in console.lib.Keys:
        if grp == "None":
            for name in sorted(console.lib[grp]):
                if console.svsearchstr.lower() == name.lower():
                    GUILayout.Label("<color=%s><b>%s</b></color>"%(_pc.col_match,name))
                elif name.lower().startswith(console.svsearchstr.lower()):
                    GUILayout.Label("<color=%s>%s</color>"%(_pc.col_pmatch,name))
        else:
            for name in sorted(console.lib[grp]):
                if console.svsearchstr.lower() == name.lower():
                    GUILayout.Label("<color=%s><b>%s</b></color> <color=%s><b>(%s)</b></color>"%(_pc.col_match,name,_pc.col_grp,grp))
                elif name.lower().startswith(console.svsearchstr.lower()):
                    GUILayout.Label("<color=%s>%s</color><color=%s>(%s)</color>"%(_pc.col_pmatch,name,_pc.col_grp,grp))
    GUILayout.EndScrollView()
    GUILayout.EndVertical()
        
    GUILayout.BeginVertical()
    # Tags
    GUILayout.Label("Tags:",GUILayout.Width(120))
    console.svtagscrollpos = GUILayout.BeginScrollView(console.svtagscrollpos)
    for i in range (0,len(console.taglib)):
        if i == 0 or i == 1: col = console.sptgcol
        else: col = console.nortgcol
        console.svTagTgl[i] = GUILayout.Toggle(console.svTagTgl[i],"<color=%s>%s</color>"%(col,console.taglib[i]))
        """
        # Add tag to textfield
        if (console.svTagTgl[i] == True):
            if console.svtagstr == "":
                console.svtagstr = console.taglib[i]
            elif console.taglib[i] not in console.svtagstr:
                console.svtagstr = console.svtagstr + ", " + console.taglib[i]
        # Remove tag from textfield
        elif (", "+console.taglib[i]) in console.svtagstr:
            console.svtagstr = console.svtagstr.replace((", "+console.taglib[i]),"")
        elif (console.taglib[i]+", ") in console.svtagstr:
            console.svtagstr = console.svtagstr.replace((console.taglib[i]+", "),"")  
        elif (","+console.taglib[i]) in console.svtagstr:
            console.svtagstr = console.svtagstr.replace((","+console.taglib[i]),"")    
        elif (console.taglib[i]+",") in console.svtagstr:
            console.svtagstr = console.svtagstr.replace((console.taglib[i]+","),"")
        elif console.taglib[i] == console.svtagstr:
            console.svtagstr = console.svtagstr.replace(console.taglib[i],"")
        """    
        # Add tag to textfield
        if (console.svTagTgl[i] == True):
            if console.svtagstr == "":
                console.svtagstr = console.taglib[i] + ", "
            elif console.taglib[i] not in console.svtagstr:
                if console.svtagstr.strip()[-1] == ",":
                    console.svtagstr = console.svtagstr + console.taglib[i] + ", "
                else:
                    console.svtagstr = console.svtagstr + ", " + console.taglib[i] + ", "
        # Remove tag from textfield
        elif (", "+console.taglib[i]+", ") in console.svtagstr:
            console.svtagstr = console.svtagstr.replace((console.taglib[i])+", ","")
        elif (", "+console.taglib[i]+",") in console.svtagstr:
            console.svtagstr = console.svtagstr.replace((console.taglib[i])+",","")
        elif console.svtagstr == console.taglib[i] + ", ":
            console.svtagstr = console.svtagstr.replace(console.taglib[i] + ", ","")     
        elif console.svtagstr == console.taglib[i] + ",":
            console.svtagstr = console.svtagstr.replace(console.taglib[i] + ",","")      
        elif console.svtagstr == console.taglib[i]:
            console.svtagstr = console.svtagstr.replace(console.taglib[i],"") 
        elif len(console.svtagstr) > len(console.taglib[i]) + 2:
            if console.svtagstr[0:len(console.taglib[i])+2] == console.taglib[i] + ", ":
                console.svtagstr = console.svtagstr.replace(console.taglib[i] + ", ","")   
            elif console.svtagstr[0:len(console.taglib[i])+1] == console.taglib[i] + ",":
                console.svtagstr = console.svtagstr.replace(console.taglib[i] + ",","")            
    GUILayout.EndScrollView()
    if GUILayout.Button("Clear tags"):
        for i in range(0,len(console.svTagTgl)):
            console.svTagTgl[i] = False
        #for tgl in console.svTagTgl:
            #tgl = False
        console.svtagstr = ""
    GUILayout.EndVertical()
    GUILayout.BeginVertical()
    # Groups
    GUILayout.Label("Groups:",GUILayout.Width(130))
    console.svgrpscrollpos = GUILayout.BeginScrollView(console.svgrpscrollpos) 
    if GUILayout.Button("None"):
        console.svgrpstr = ""
    for grp in console.lib.Keys:
        if not grp == "None":
            if GUILayout.Button(grp):
                console.svgrpstr = grp
    GUILayout.EndScrollView()
    GUILayout.EndVertical()

    GUILayout.EndHorizontal()
                
        
    
    return console

def poseConsoleReplaceWindow(console):
    global _pc

    
    if not console.loaded_pose == None:
        console.replaceInit()
            
        #if _pc.windowindex == 0:
        GUILayout.Label('Replace last loaded "<color=%s><b>%s</b></color>" with current pose:'%(_pc.col_loaded,console.loaded_pose[0]))
            
        GUILayout.BeginHorizontal()
        GUILayout.Label("Name:",GUILayout.Width(60))
        console.rep_searchstr = GUILayout.TextField(console.rep_searchstr,GUILayout.Width(220))
        if GUILayout.Button("Replace"):
            console.savePose(console.rep_searchstr,console.rep_tagstr,console.rep_grpstr, rep_loaded = console.rep_do)
        GUILayout.EndHorizontal()
          
        GUILayout.BeginHorizontal()
        GUILayout.Label("with Tags:",GUILayout.Width(60))
        console.rep_tagstr = GUILayout.TextField(console.rep_tagstr,GUILayout.Width(220))
        if GUILayout.Button("Replace w/ y-offset"):
            console.savePose(console.rep_searchstr,console.rep_tagstr,console.rep_grpstr,offset_flag = True, rep_loaded = console.rep_do)
        GUILayout.EndHorizontal()
    
        GUILayout.BeginHorizontal()
        GUILayout.Label("in Group:",GUILayout.Width(60))
        console.rep_grpstr = GUILayout.TextField(console.rep_grpstr,GUILayout.Width(220))
        GUILayout.EndHorizontal()
    
        GUILayout.BeginHorizontal()
          
        GUILayout.BeginVertical()
        GUILayout.Label("Files:",GUILayout.Width(80))
        console.rep_scrollPos = GUILayout.BeginScrollView(console.rep_scrollPos,GUILayout.Width(120)) #,GUILayout.Width(250),GUILayout.Height(300))
        for grp in console.lib.Keys:
            if grp == "None":
                for name in sorted(console.lib[grp]):
                    if console.rep_searchstr.lower() == name.lower():
                        GUILayout.Label("<color=%s><b>%s</b></color>"%(_pc.col_match,name))
                    elif name.lower().startswith(console.rep_searchstr.lower()):
                        GUILayout.Label("<color=%s><b>%s</b></color>"%(_pc.col_pmatch,name))
            else:
                for name in sorted(console.lib[grp]):
                    if console.rep_searchstr.lower() == name.lower():
                        GUILayout.Label("<color=%s><b>%s</b></color> <color=%s><b>(%s)</b></color>"%(_pc.col_match,name,_pc.col_grp,grp))
                    elif name.lower().startswith(console.rep_searchstr.lower()):
                        GUILayout.Label("<color=%s><b>%s</b></color><color=%s><b>(%s)</b></color>"%(_pc.col_pmatch,name,_pc.col_grp,grp))
        GUILayout.EndScrollView()
        GUILayout.EndVertical()
            
        GUILayout.BeginVertical()
        # Tags
        GUILayout.Label("Tags:",GUILayout.Width(120))
        console.rep_tagscrollpos = GUILayout.BeginScrollView(console.rep_tagscrollpos)
        for i in range (0,len(console.taglib)):
            if i == 0 or i == 1: col = console.sptgcol
            else: col = console.nortgcol
            console.rep_TagTgl[i] = GUILayout.Toggle(console.rep_TagTgl[i],"<color=%s>%s</color>"%(col,console.taglib[i]))
            # Add tag to textfield
            if (console.rep_TagTgl[i] == True):
                if console.rep_tagstr == "":
                    console.rep_tagstr = console.taglib[i] + ", "
                elif console.taglib[i] not in console.rep_tagstr:
                    if console.rep_tagstr.strip()[-1] == ",":
                        console.rep_tagstr = console.rep_tagstr + console.taglib[i] + ", "
                    else:
                        console.rep_tagstr = console.rep_tagstr + ", " + console.taglib[i] + ", "
            # Remove tag from textfield
            elif (", "+console.taglib[i]+", ") in console.rep_tagstr:
                console.rep_tagstr = console.rep_tagstr.replace((console.taglib[i])+", ","")
            elif (", "+console.taglib[i]+",") in console.rep_tagstr:
                console.rep_tagstr = console.rep_tagstr.replace((console.taglib[i])+",","")
            elif console.rep_tagstr == console.taglib[i] + ", ":
                console.rep_tagstr = console.rep_tagstr.replace(console.taglib[i] + ", ","")     
            elif console.rep_tagstr == console.taglib[i] + ",":
                console.rep_tagstr = console.rep_tagstr.replace(console.taglib[i] + ",","")      
            elif console.rep_tagstr == console.taglib[i]:
                console.rep_tagstr = console.rep_tagstr.replace(console.taglib[i],"") 
            elif len(console.rep_tagstr) > len(console.taglib[i]) + 2:
                if console.rep_tagstr[0:len(console.taglib[i])+2] == console.taglib[i] + ", ":
                    console.rep_tagstr = console.rep_tagstr.replace(console.taglib[i] + ", ","")   
                elif console.rep_tagstr[0:len(console.taglib[i])+1] == console.taglib[i] + ",":
                    console.rep_tagstr = console.rep_tagstr.replace(console.taglib[i] + ",","")     
        GUILayout.EndScrollView()
        if GUILayout.Button("Clear tags"):
            for i in range(0,len(console.rep_TagTgl)):
                console.rep_TagTgl[i] = False
            #for tgl in console.rep_TagTgl:
                #tgl = False
            console.rep_tagstr = ""
        GUILayout.EndVertical()
        GUILayout.BeginVertical()
        # Groups
        GUILayout.Label("Groups:",GUILayout.Width(160))
        console.rep_grpscrollpos = GUILayout.BeginScrollView(console.rep_grpscrollpos) 
        if GUILayout.Button("None"):
            console.svgrpstr = ""
        for grp in console.lib.Keys:
            if not grp == "None":
                if GUILayout.Button(grp):
                    console.svgrpstr = grp
        GUILayout.EndScrollView()
        GUILayout.EndVertical()
    
        GUILayout.EndHorizontal()
    
    else:
        GUILayout.FlexibleSpace()
        GUILayout.BeginHorizontal()
        GUILayout.FlexibleSpace()    
        GUILayout.Label("Load a pose first!")
        GUILayout.FlexibleSpace()  
        GUILayout.EndHorizontal()
        GUILayout.FlexibleSpace()                
            
        
    return console

# Get selection
def get_selected_objs(game):
    mtreeman = game.studio.treeNodeCtrl
    ar = []
    for node in mtreeman.selectNodes:
        ochar = HSNeoOCI.create_from_treenode(node)
        #if 'oiCharInfo' in dir(ochar):
        if "as_actor" in dir(ochar):
        #if isinstance(ochar,OCIChar):
            ar.append(ochar.as_actor)
        
        """
        if isinstance(ochar,HSNeoOCIChar):
            ar.append(ActorSC(ochar.objctrl))
            #print "actor"
        else:
            ar.append(ochar.objctrl)
            #print "item"
        """

    if len(ar) == 0:
        return None
    return ar
    
# def applyState(state):
#     # if is_hsadvneo():
#     #     applyStateHSNeoAdv(state)
#     # else:
#     applyStateCross(state)


def applyStateNormal(state):
    global _pc
    char = get_selected_objs(_pc.game)
    if not char == None:
        char = char[0]
        if "move_to" in state:
            del state["move_to"]
        if "rotate_to" in state:
            del state["rotate_to"]
        if "scale_to" in state:
            del state["scale_to"]

        char.import_status(state)

def applyStateNormalDiffOpt(state):
    global _pc
    char = get_selected_objs(_pc.game)
    if not char == None:
        char = char[0]
        if "move_to" in state:
            del state["move_to"]
        if "rotate_to" in state:
            del state["rotate_to"]
        if "scale_to" in state:
            del state["scale_to"]

        char.import_status_diff_optimized(state)

# --- old functions from SceneConsole to apply hands --

# def applyStateLHand(state):
#     global _pc
#     char = get_selected_objs(_pc.game)
#     if not char == None:
#         char = char[0]
#
#         char.set_kinematic(state["kinematic"])
#         if state["kinematic"] == 0 or state["kinematic"] == 1:
#             cur_lhand = char.get_hand_ptn()
#             new_lhand = (state["hands"][0],cur_lhand[1])
#             char.set_hand_ptn(new_lhand)
#         if state["kinematic"] == 2 or state["kinematic"] == 3:
#             do_exist = False
#             lhand_keys = [i for i in range(37,52)]
#             #if lhand_keys <= state["fk_set"].keys():
#             lhand_fk = {}
#             for i in lhand_keys:
#                 if i in state["fk_set"].keys():
#                     lhand_fk[i] = state["fk_set"][i]
#                     do_exist = True
#             if do_exist == True:
#                 char.set_FK_active(group = 5, active = 1)
#                 char.import_fk_bone_info(lhand_fk)
#
#
# def applyStateRHand(state):
#     global _pc
#     char = get_selected_objs(_pc.game)
#     if not char == None:
#         char = char[0]
#
#         char.set_kinematic(state["kinematic"])
#         if state["kinematic"] == 0 or state["kinematic"] == 1:
#             cur_rhand = char.get_hand_ptn()
#             new_rhand = (state["hands"][1],cur_rhand[0])
#             char.set_hand_ptn(new_rhand)
#         if state["kinematic"] == 2 or state["kinematic"] == 3:
#             do_exist = False
#             rhand_keys = [i for i in range(22,37)]
#             #if rhand_keys <= state["fk_set"].keys():
#             rhand_fk = {}
#             for i in rhand_keys:
#                 if i in state["fk_set"].keys():
#                     rhand_fk[i] = state["fk_set"][i]
#                     do_exist = True
#             if do_exist == True:
#                 char.set_FK_active(group = 4, active = 1)
#                 char.import_fk_bone_info(rhand_fk)

            # def applyStateCross(state, apply = None):
#     global _pc
#     char = get_selected_objs(_pc.game)
#     if not char == None:
#         char = char[0]
#         if apply == None:
#             apply = ["pose"]
#
#         if isinstance(apply, list):
#             # print "list"
#             if "move_to" in state:
#                 del state["move_to"]
#             if "rotate_to" in state:
#                 del state["rotate_to"]
#             if "scale_to" in state:
#                 del state["scale_to"]
#
#             char.import_status(state)

def excludeFK(dicFK, exc = None):
    # no correction for now
    return dicFK

    #
    correctedDicFK = {}
    if exc == None:
        global _pc
        exc = _pc.fk_exc
    for tgt in dicFK:
        if int(tgt) not in exc: 
            #rot = Vector3(float(dicFK[tgt][0]),float(dicFK[tgt][1]),float(dicFK[tgt][2]))
            correctedDicFK[tgt] = dicFK[tgt]
    
    return correctedDicFK   
    
def cleanKeys(dct):
    ndct = {}
    for key in dct.keys():
        ndct[int(key)] = dct[key]
    return ndct

# keitaro crossplatform elements
def is_hsadvneo():
    import extplugins
    return extplugins.ExtPlugin.exists("HSStudioNEOAddon")
