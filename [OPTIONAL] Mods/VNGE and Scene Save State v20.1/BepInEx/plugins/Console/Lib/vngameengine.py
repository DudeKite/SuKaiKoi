"""
vn game engine for Honey Select Studio / NEO / PlayHomeStudio / CharaStudio / AI-Shoujo by Keitaro-kun
VNActor, VNFrame, VNAnime, VNText and other cool stuff by countd360
"""
vnge_version = "20.1"
"""
Key shorcuts:
- Ctrl+F8 - show/hide main window
- Ctrl+F3 - return to title screen
For developers:
- Ctrl+F4 - toggle developer console
- Ctrl+F1 - reloading and restarting vn game engine
- Ctrl+Alt+F4 - dump camera state (saved in dumppython.txt)
- Ctrl+Alt+F5 - dump scene state (saved in dumppython.txt)
---------
Changelog in vngameengine_changelog.txt
---------
For cool developers:
- main game classes are located in vngameengine.py

"game" is an instance of one of classes, depending on engine, where we run game

There are several classes:
- BaseController - just for window instantion
- VNController(BaseController) - for main vn game engine. Contains functions for buttons, timers, main window, etc.
- StudioController(VNController) - controller for Studio. Contains scene loading, move between chars etc. - placed in vngameenginestudio.py
- VNNeoController(VNController) - base controller for all NEO-based engines - line NEO, PlayHome Studio (perspectively), CharaStudio in Koikatsu. Contains move between cameras, animation between them and so on.
- NeoController(VNNeoController) - controller for NEO. Contains specific scene loading.
- CharaStudioController(VNNeoController) - controller for CharaStudio. Contains specific scene loading.
- PHStudioController(VNNeoController) - controller for PlayHomeStudio. placed in vngameenginephstudio.py

All examples usually can be found at this places:
- maingamedemo.py
- simplegamedemoadv.py
- techdemo.py
"""
def importOrReload(module_name): return import_or_reload(module_name)

def import_or_reload(module_name):
    import sys

    if module_name in sys.modules:
        reload(sys.modules[module_name])
    else:
        __import__(module_name)

    if module_name in sys.modules:
        return sys.modules[module_name]
    return None


def get_engine_id():
    from UnityEngine import Application
    dpath = Application.dataPath
    ar = dpath.split("/")
    gameId = ar[len(ar)-1]
    if (gameId == "HoneyStudio_32_Data") or (gameId == "HoneyStudio_64_Data"):
        return "studio"
    if (gameId == "StudioNEO_32_Data") or (gameId == "StudioNEO_64_Data"):
        return "neo"
    if (gameId == "PlayHomeStudio32bit_Data") or (gameId == "PlayHomeStudio64bit_Data"):
        return "phstudio"
    if (gameId == "CharaStudio_Data"):
        return "charastudio"
    if (gameId == "StudioNEOV2_Data"):
        return "neov2"
    return ""

def vngame_window_autogames_uni():
    global vnge_version
    from UnityEngine import Application
    dpath = Application.dataPath
    ar = dpath.split("/")
    gameId = ar[len(ar)-1]
    if (gameId == "HoneyStudio_32_Data") or (gameId == "HoneyStudio_64_Data"):
        print "VNGE", vnge_version, "starting..."
        vngame_window_studio(["autogames"], [])
        print "VNGE", vnge_version, "inited!"
        return True
    if (gameId == "StudioNEO_32_Data") or (gameId == "StudioNEO_64_Data"):
        print "VNGE",vnge_version,"starting..."
        vngame_window_neo(["autogames"], [])
        print "VNGE", vnge_version, "inited!"
        return True
    if (gameId == "PlayHomeStudio32bit_Data") or (gameId == "PlayHomeStudio64bit_Data"):
        print "VNGE", vnge_version, "starting..."
        vngame_window_phstudio(["autogames"], [])
        print "VNGE", vnge_version, "inited!"
        return True
    if (gameId == "CharaStudio_Data"):
        print "VNGE", vnge_version, "starting..."
        vngame_window_charastudio(["autogames"], [])
        print "VNGE", vnge_version, "inited!"
        return True
    if (gameId == "StudioNEOV2_Data"):
        print "VNGE", vnge_version, "starting..."
        vngame_window_neov2(["autogames"], [])
        print "VNGE", vnge_version, "inited!"
        return True
    print("VN Game engine is not for this EXE file")
    return False

inited = False
def vngame_window_autogames_uni_1init():
    global inited
    if not inited:
        inited = True
        vngame_window_autogames_uni()

def parseKeyCode(s):
    from System import Enum
    from UnityEngine import KeyCode
    try:
        if s:
            ctrl, alt, shift = False, False, False
            keys = s.lower().split('+')
            shift = 'shift' in keys
            ctrl = 'ctrl' in keys or 'control' in keys
            alt = 'alt' in keys or 'meta' in keys
            code = Enum.Parse(KeyCode, keys[-1:][0], True)
            return (s, code, ctrl, alt, shift)
    except:
        pass
    return (s, KeyCode.None, False, False, False)


def reloadKeyCodes():
    global _keycodes
    _keycodes = {}

bepInExLoggingConsole = ""

def parseBepInExIniFile():
    global bepInExLoggingConsole
    try:
        import ConfigParser, sys, os.path
        config = ConfigParser.RawConfigParser()
        import codecs
        with codecs.open('BepInEx/config/BepInEx.cfg', 'r', encoding='utf-8') as f:
            config.readfp(f)

        #print "ok!"
        bepInExLoggingConsole = config.get('Logging.Console', 'Enabled').lower()


    #config.read('BepInEx/config/BepInEx.cfg')
    # for k, v in config.items('Logging.Console'):
    #     if k == "Enabled":
    #         #bepInExLoggingConsole = v
    #         print v
    except Exception, e:
        print("VNGE Error parseBepInExIniFile: " + str(e))

def parseIniFile():
    global _keycodes
    global _engineoptions
    try:
        _keycodes
    except NameError:
        _keycodes = {}
    try:
        _engineoptions
    except NameError:
        _engineoptions = {}
    try:
        import ConfigParser, sys, os.path
        config = ConfigParser.SafeConfigParser()
        config.read(os.path.splitext(__file__)[0] + '.ini')
        for k, v in config.items('Shortcuts'):
            _keycodes[k.lower()] = parseKeyCode(v)
        for k, v in config.items('Options'):
            _engineoptions[k.lower()] = v
    except Exception, e:
        print("Error: " + str(e))
    if not _keycodes.get('hide', None):
        _keycodes['hide'] = ('Ctrl+F8', KeyCode.F8, True, False, False)

def getKeyCodes():
    global _keycodes
    return _keycodes

def checkKeyCode(iniparam):
    global _keycodes
    try: # disabling due to performance issues
        iniparam = iniparam.lower()
        import unity_util
        from UnityEngine import Input, KeyCode
        if iniparam in _keycodes:
            (_, icode, ictrl, ialt, ishift) = _keycodes[iniparam]
            if Input.GetKeyDown(icode):
                # unity sucks for checking meta keys
                ctrl, alt, shift = unity_util.metakey_state()
                if ctrl == ictrl and alt == ialt and shift == ishift:
                    return True
        else:
            return False
    except Exception, e:
        pass
    return False

def getEngineOptions():
    global _engineoptions
    return _engineoptions

def translateText(value):
    if not value: return value

    global _translateHookChanged
    try:
        _translateHookChanged
    except NameError:
        _translateHookChanged = None
    if not _translateHookChanged:
        try:
            import clr
            clr.AddReference('XUnity.AutoTranslator.Plugin.Core')
            from XUnity.AutoTranslator.Plugin.Core import AutoTranslationPlugin
            _translateHookChanged = AutoTranslationPlugin.Current.Hook_TextChanged
            print "AutoTranslator enabled!!"
        except Exception, e:
            _translateHookChanged = lambda x: x
            print "AutoTranslator disabled or not found"
            #print("Error in AutoTranslator: " + str(e))
    from UnityEngine import GUIContent
    if isinstance(value, GUIContent):
        if not value.text: return value
        _translateHookChanged(value)
        return value
    else:
        content = GUIContent(str(value))
        _translateHookChanged(content)
        return content.text

class GData():
    def __init__(self):
        pass

class BaseController():
    def __init__(self):
        from UnityEngine import Screen, Rect
        
        self.gameObject = None # will be assigned if exists as member
        self.component = None # will be assigned if exists as member
        self.counter = 1
        self.show_buttons = False
        self.visible = True
        self.style = None
        self.cameraControl = None
        self.windowRect = Rect (Screen.width / 2 - 50, Screen.height / 2 - 50, 400, 400)
        self.isMouseInWindow =False
        self.windowDraggable = True
        self.lastCameraState = True
        self.gameCursor = None
        self.windowName = "Window"
        # loading options
        parseIniFile()
        self.engineOptions = getEngineOptions()
        #print self.engineOptions

    def EnableCamera(self, value):
        if self.lastCameraState != value:
            self.lastCameraState = value
            if self.cameraControl:
                self.cameraControl.enabled = value
            self.gameCursor.enabled = value
        
    def ResetWindow(self, windowid):
        from UnityEngine import GUI, GUIUtility
        from UnityEngine import Event, EventType
        #Workaround mouse/camera issues when dragging window
        if GUIUtility.hotControl == 0:
            self.EnableCamera(True)
        if Event.current.type == EventType.MouseDown:
            GUI.FocusControl("")
            GUI.FocusWindow(windowid)
            self.EnableCamera(False)
        
    def Start(self):
        try:
            import UnityEngine
            import GameCursor, CameraControl
            from UnityEngine import GameObject



            #self.useGUILayout = True

            if self.isClassicStudio:
                if self.cameraControl == None:
                    self.cameraControl = GameObject.Find('StudioCamera/Main Camera').GetComponent[CameraControl]()
            #if GameObject.Find("EventSystem") == None:
            #self.Instantiate(self.cameraControl);
            if self.gameCursor == None:
                self.gameCursor = UnityEngine.Object.FindObjectOfType[GameCursor]()
        except Exception, e:
            print "VNGE: passable error in Start: ", e
            pass
        
    def OnGUI(self):
        from UnityEngine import GUI
        if not self.visible: return
        self.windowRect = GUI.Window(0, self.windowRect, self.windowCallback, self.windowName)
    
    def Update(self):
        import unity_util
        from UnityEngine import Input, KeyCode
        # Update is called less so better place to check keystate

        if checkKeyCode('hide'):
            self.visible = not self.visible
        """
        if Input.GetKeyDown(KeyCode.F8):
            # unity sucks for checking meta keys
            ctrl, alt, shift = unity_util.metakey_state()
            if ctrl and not alt and not shift:
                self.visible = not self.visible
        """


class SkinBase:
    def __init__(self):
        self.isCustomFuncWindowGUI = False

        self.maxButtonsNormal = 5
        self.maxButtonsCompact = 8
        pass

    def setup(self,controller):
        """:type controller:VNController"""
        pass

    def customWindowGUI(self, windowid):
        pass

    def render_system(self,sys_text):
        pass

    def render_main(self,text_author,text,btnsTexts,btnsActions,btnStyle):
        pass

    def render_dev_console(self):
        print "Skin Dev Console not implemented"
                
import UnityEngine
#import GameCursor, CameraControl
from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Mathf, Time
import System  
from WindowsInput import InputSimulator
from WindowsInput import VirtualKeyCode 
import unity_util             
class VNController(BaseController):
    def __init__(self):
        BaseController.__init__(self)


        
        self.arKeyKodes = getEngineOptions()['keysforbuttons'].split(',')
        self.vnButtonsStyle = "normal"

        self.visible = self.engineOptions["starthidden"] == "0"


        # self.wwidth = 500
        # self.wheight = 230
        #
        # self.windowName = ''
        # self.windowRect = Rect (Screen.width / 2 - self.wwidth / 2, Screen.height - self.wheight - 10, self.wwidth, self.wheight)
        #self.skin_panel_unity = CloneSkin(GUI.)
        self.windowStyle = None
        self.windowStyleDefault = GUIStyle("window")


        self.skin_set_byname("skin_default")
        self.skin_default = self.skin

        # try connect to save/load events
        self.isSceneEventsSupported = False
        self.isSceneDataSaveSupported = False
        self.errSceneEvents = ""
        self.init_saveload_events()


        global vnge_version
        self._vnText = "Welcome to <b>VN Game engine "+vnge_version+"</b>!\n"

        try:
            import testutf8
            self._vnText = self._vnText
            self._vnText += "\n"
        except Exception, e:
            self._vnText += "<color=red>WRN!</color> You have a problems with UTF-8 libs! See website.\n"
            print "VNGE: problems with UTF-8 libs detected"

        if not self.isSceneEventsSupported:
            self._vnText += "<color=red>WRN!</color> No handle save/load scene events. "+self.errSceneEvents+"\n"

        self._vnText += "- "+getKeyCodes()['hide'][0]+" to show/hide this window\n" \
                       "- "+getKeyCodes()['reset'][0]+" to return to this main screen (more in INI file)"
        #self._vnButtons = ["Start >"]
        #self._vnButtonsActions = [self.StartAct]
        
        self.registeredChars = {}
        self.register_char("s", "ff5555", "")
        self.curCharText = "s"
        self.curCharFull = "s"
        
        self.nextTexts = [[]]
        

        

        self.updFunc = None
        self.updFuncParam = ""
        
        self.timers = [-1,-1,-1,-1,-1,-1,-1,-1]
        self.timersFuncUpd = [None,None,None,None,None,None,None,None]
        self.timersFuncEnd = [None,None,None,None,None,None,None,None]
        self.timersDuration = [0,0,0,0,0,0,0,0]

        self.isTitleScreen = True
        # preprocessing start options
        if self._vnButtons[0] == "autogames":
            #self._vnButtons = []
            #self._vnButtonsActions = []
            #self.prepare_auto_games()
            #self._vnButtons = ["All games list >>", "(hide this window)"]
            self._vnButtons = [color_text_green("All games >>"),
                               "Simple novels >>",
                               "VN Scenes >>",
                               color_text_yellowlight("DEV: ")+"Clip Man / VNText",
                               color_text_yellowlight("DEV: ")+"SceneSaveState (SSS)",
                               color_text_gray("hide this window")]
            self._vnButtonsActions = [self.prepare_auto_games,
                                      (self.game_start_fromfile, "simplenovelmanager"),
                                      (self.game_start_fromfile, "simplevnscenesmanager"),
                                      self._sup_toggle_vnframe_console,
                                      (self.game_start_fromfile, "scenesavestate"),
                                      self._sup_hide_window]
            self.vnButtonsStyle = "compact"


        self._vnStButtons = self._vnButtons
        self._vnStButtonsActions = self._vnButtonsActions
        self._vnStText = self._vnText

        self.maxBtnsBeforeSeparator = 5
        self._btnSepCounter = 0
        self._arBtnsTextFull = []
        self._arBtnsActsFull = []

        self.gdata = GData()
        self.scenedata = GData()
        self.gpersdata = {}

        self._scenef_actors = {}  # for actors
        self._scenef_props = {}  # for props

        self.current_game = ""

        self._eventListenerDic = {}

        self.isfAutoLipSync = False
        self.fAutoLipSyncVer = "v10"

        self.isSceneAutorunAnimDisabled = False

        self.init_start_params()

        #RawMakeToolbarButton(self)
        # import extplugins
        # illapi = extplugins.ILLAPI()
        # if illapi.isDetected:
        #     illapi.Studio_StudioAPI().StudioLoadedChanged += self.studio_loaded_changed
        #self.set_timer(4,self.studio_after_loaded_changed)

        # autoloading feature

        self.windowCallback = GUI.WindowFunction(self.FuncWindowGUI)

        self.init_autorun_mods()

    # def studio_after_loaded_changed(self,p1="",p2=""):
    #
    #     print p1,p2,"studio loaded!"
    #     RawMakeToolbarButton(self)

    def init_saveload_events(self):
        return

    # templates for scene loaded calls
    def _event_scene_loaded(self,p1,p2=None):
        self.lastSceneLoadedFile = p1
        print "VNGE event: scene_loaded"
        self.event_dispatch("scene_loaded",p1)
        self.set_timer(1,self._event_scene_loaded_after)

    def _event_scene_saved(self,p1,p2=None):
        self.lastSceneSavedFile = p1
        print "VNGE event: scene_saved"
        self.event_dispatch("scene_saved",p1)

    def _event_scene_imported(self,p1,p2=None):
        self.lastSceneImportedFile = p1
        print "VNGE event: scene_imported"
        self.event_dispatch("scene_imported",p1)
        self.set_timer(1,self._event_scene_imported_after)

    def _event_scene_loaded_after(self, game):
        self.event_dispatch("scene_loaded_after",self.lastSceneLoadedFile)
        self.event_dispatch("scene_loaded_after2",self.lastSceneLoadedFile)

    def _event_scene_imported_after(self, game):
        self.event_dispatch("scene_imported_after",self.lastSceneImportedFile)
        self.event_dispatch("scene_imported_after2",self.lastSceneImportedFile)


    # autorun staff
    def init_autorun_mods(game):
        from os import listdir
        from os.path import isfile, join
        mypath = game.pygamepath
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        for fil in onlyfiles:
            # print fil[:-3]
            if fil.startswith("autorun_") and fil.endswith(".py"):
                modfile = fil[:-3]
                print "VNGE found autorun mod: "+modfile
                game.init_autorun_mod(modfile)

    def init_autorun_mod(game,modname):

        try:
            mod = import_or_reload(modname)
        except Exception,e:
            print "VNGE autorun mod {0} can't load error: {1}".format(modname, str(e))
            return False
        try:
            mod.start_autorun(game)
        except Exception, e:
            print "VNGE autorun mod {0} can't start mod error: {1}".format(modname, str(e))
            return False

        return True


    def init_start_params(self):
        self.isShowDevConsole = False

        self.isSceneAutorunAnimDisabled = False

        # menu
        self._menuStack = []
        self.menu_result = None

        self.isHideGameButtons = False
        self.onSetTextCallback = None
        self.camAnimeTID = -1  # timer id for camera animation
        self.onDumpSceneOverride = None

        self.isHideWindowDuringCameraAnimation = False

        self.isFuncLocked = False
        self.funcLockedText = "SYSTEM: Unknown default lock"

        # some settings - may be localized
        self.btnNextText = "Next >"
        #self.autostart = False
        #self.isDevDumpButtons = False - no use
        self.sceneDir = ""

        self.gdata = GData()
        self.gpersdata = {}
        self.scenedata = GData()

        self._scenef_actors = {}  # for actors
        self._scenef_props = {}  # for props

        self.current_game = ""

        # lip sync
        self.isfAutoLipSync = False
        self.fAutoLipSyncVer = "v10"

        self.readingChar = None
        self.readingSpeed = 12.0
        self.readingProgress = 0
        self.lipAnimeTID = -1  # timer id for lip sync animation

        # self._eventListenerDic = {}

        # advanced clean, keep persistent stuff
        for eventid in self._eventListenerDic:
            newlis = []
            for evt in self._eventListenerDic[eventid]:
                if evt[2]: # if persistent
                    newlis.append(evt)
            self._eventListenerDic[eventid] = newlis

        self.windowStyle = self.windowStyleDefault
        self.skin_set(self.skin_default)


    def _sup_hide_window(self,game):
        self.hide_window()
    
    def FuncWindowGUI(self,windowid):
        if self.isClassicStudio:
            #self.ResetWindow(windowid) #required for dragging - not work in NEO!!!
            pass

        if self.skin.isCustomFuncWindowGUI: # skin has it's own WindowGUI func
            self.skin.customWindowGUI(windowid)
            return

        if not self.isFuncLocked:
            if not self.isShowDevConsole:
                try:
                    self.skin.render_main(self.curCharFull,self.vnText,self.vnButtons,self._vnButtonsActions,self.vnButtonsStyle)
                except Exception, e:
                    print "Error in skin.render_main, ", str(e)

            else: # show dev console
                try:
                    self.skin.render_dev_console()
                except Exception, e:
                    print "Error in skin.render_dev_console, ", str(e)
        else: # render system message
            self.skin.render_system(self.funcLockedText)




    def dump_camera(self):
        self.show_blocking_message_time("ERROR: Not implemented")

    def dump_scene(self):
        self.show_blocking_message_time("ERROR: Not implemented")

    def dump_scene_vnframe(self):
        self.show_blocking_message_time("ERROR: Not implemented")

    def Start(self):
        BaseController.Start(self)

        if get_engine_id() != "studio": # if not old Studio
            try:
                # make button using KKAPI
                IllApiMakeToolbarButton(self)
            except Exception, e:
                #  if failed - make it raw
                RawMakeToolbarButton(self)
        
    def OnGUI(self):
        #r = self.windowRect
        #self.windowRect = Rect(r.x, r.y, r.width, 70 if self.show_buttons else 50)

        #if self.windowStyle:
        #    GUI.skin.window = self.windowStyle
        #BaseController.OnGUI(self)
        from UnityEngine import GUI
        if not self.visible: return
        self.windowRect = GUI.Window(0, self.windowRect, self.windowCallback, self.windowName, self.windowStyle)

        # for ui drag
        from UnityEngine import Event, Input, KeyCode
        from Studio import Studio
        self.isMouseInWindow = self.windowRect.Contains(Event.current.mousePosition)

        def vngeNoCtrlConition():
            orgCondition = Studio.Instance.workInfo.useAlt and not Input.GetKey(KeyCode.LeftAlt) and not Input.GetKey(KeyCode.RightAlt)
            return (self.isMouseInWindow and self.visible and self.windowDraggable) or orgCondition
        if self.isMouseInWindow:
            Studio.Instance.cameraCtrl.noCtrlCondition = vngeNoCtrlConition

    def Update(self):
        BaseController.Update(self)
        if self.updFunc != None:
            func = self.updFunc
            self.updFunc = None
            func(self.updFuncParam)
        for i in range(len(self.timers)):
            if(self.timers[i] > 0):
                self.timers[i] -= Time.deltaTime
                if self.timersFuncUpd[i] != None:
                    self.timersFuncUpd[i](self, Time.deltaTime, self.timersDuration[i] - self.timers[i], self.timersDuration[i])
                if self.timers[i] <= 0 and self.timersFuncEnd[i] != None:
                    self.call_game_func(self.timersFuncEnd[i])
        self.UpdateKeyChecks()
        self.event_dispatch("update", None)

    def _sup_toggle_vnframe_console(self,game=""):
        try:
            import vnframe
            vnframe.toggle_devconsole(self)
        except Exception, e:
            self.show_blocking_message_time("Error: can't start VNFrame developer console: %s"%(str(e)))

    def UpdateKeyChecks(self):

        if checkKeyCode('reset'):
            self.return_to_start_screen_clear()
        if checkKeyCode('ReloadCurrentGame'):
            if self.current_game != "":
                self.game_start_fromfile(self,self.current_game)
        if checkKeyCode('VNFrameDeveloperConsole'):
            self._sup_toggle_vnframe_console()

        if self.get_ini_option("usekeysforbuttons") == "1":
            if self.visible and not self.isFuncLocked and not self.isHideGameButtons:
                for i in range(len(self.arKeyKodes)):
                    if Input.GetKeyDown(self.arKeyKodes[i]):
                        #self._vnButtonsActions[i](self)
                        self.call_game_func(self._vnButtonsActions[i])
        # running games from INI
        self._util_upd_check_and_start_game("game1")
        self._util_upd_check_and_start_game("game2")
        self._util_upd_check_and_start_game("game3")
        self._util_upd_check_and_start_game("game4")
        self._util_upd_check_and_start_game("game5")
        self._util_upd_check_and_start_game("game6")
        self._util_upd_check_and_start_game("game7")
        self._util_upd_check_and_start_game("game8")
        self._util_upd_check_and_start_game("game9")
        self._util_upd_check_and_start_game("game10")
        if checkKeyCode('developerconsole'):
            if self.isShowDevConsole:
                # restoring old window
                self.isShowDevConsole = False
                self.skin_set(self.skin_saved)
            else:
                # set default skin and set console flag to show
                # console must be rendered only in default skin
                self.skin_saved = self.skin
                self.skin_set(self.skin_default)
                self.isShowDevConsole = True

        if checkKeyCode('dumpcamera'):
            self.dump_camera()
        if checkKeyCode('dumpscene'):
            self.dump_scene()


        if checkKeyCode('reloadvnengine'):
            # reload engine
            print "Try reloading engine..."
            try:
                import sys
                reload(sys.modules['vngameengine'])
                sys.modules['vngameengine'].vngame_window_autogames_uni()
                print "Reloading engine success!"
            except Exception, e:
                print("Error in reloading game engine")

    def _util_upd_check_and_start_game(self, gamekey):
        if gamekey in self.engineOptions:
            if self.engineOptions[gamekey] != "":
                if checkKeyCode(gamekey):
                    self.game_start_fromfile(self,self.engineOptions[gamekey])

    def get_ini_option(self,option):
        option = option.lower()
        if option in self.engineOptions:
            return self.engineOptions[option]
        return None

    def return_to_start_screen_clear(self):
        self.clear_timers()
        #self.reset() # before init_start_params to call before_scene_unload event
        self._unload_scene_before() # simulate unloading scene to finish all unneeded features
        # no resetting scene!
        self.init_start_params()
        self.return_to_start_screen()


    def set_timer(self, duration, timerFuncEnd, timerFuncUpd = None):
        # print "Start set_timer!"
        for i in range(len(self.timers)):
            if self.timers[i] <= 0:
                # print "Found timer!"
                self.timers[i] = duration
                self.timersDuration[i] = duration
                self.timersFuncEnd[i] = timerFuncEnd
                self.timersFuncUpd[i] = timerFuncUpd
                # print "New Timer ID =", str(i)
                return i
        return -1  # no more timer valid

    def clear_timer(self, index, runEndFunc=False):
        if runEndFunc and self.timersFuncEnd[index] != None:
            self.timersFuncEnd[index](self)
        self.timers[index] = -1
        self.timersDuration[index] = 0
        self.timersFuncEnd[index] = None
        self.timersFuncUpd[index] = None

    def return_to_start_screen(self):
        self.skin_set_byname("skin_default")
        self.set_text("s", self._vnStText)
        self.set_buttons(self._vnStButtons, self._vnStButtonsActions, "compact")
        self.isTitleScreen = True
    
    def clear_timers(self): # not calling end function
        for i in range(len(self.timers)):
            if self.timers[i] >= 0:
                self.timers[i] = -1
                self.timersFuncEnd[i] = None
    
    @property
    def vnText(self):
        return self._vnText
    
    @vnText.setter
    def vnText(self,value):
        self._vnText = value
        #self.OnGUI(self)
    
    @property
    def vnButtons(self):
        return self._vnButtons
    
    @vnButtons.setter
    def vnButtons(self,value):
        self._vnButtons = value
        #self.OnGUI(self)
    
    # ---- external game functions ---------
    def set_buttons(self, arButTexts, arButActions, style = "normal"):
        self.vnButtonsStyle = style

        if style == "normal":
            self.maxBtnsBeforeSeparator = self.skin.maxButtonsNormal
        if style == "compact":
            self.maxBtnsBeforeSeparator = self.skin.maxButtonsCompact

        if len(arButTexts) <= self.maxBtnsBeforeSeparator:
            # normal case, not so much btns
            self._btnSepCounter = 0
            self.vnButtons = arButTexts
            self._vnButtonsActions = arButActions
        else:
            self._btnSepCounter = 0
            self._arBtnsTextFull = arButTexts
            self._arBtnsActsFull = arButActions
            self._btnCallSepCounter(self,0)
        #self.OnGUI(self)

    def _btnCallFull(self,game,param):
        self.call_game_func(self._arBtnsActsFull[param])

    def _btnCallSepCounter(self,game,param):
        # wrapping over list
        if param > len(self._arBtnsTextFull)-1:
            param = 0
        # get sublist
        endindex = param+self.maxBtnsBeforeSeparator - 1
        if endindex > len(self._arBtnsTextFull):
            endindex = len(self._arBtnsTextFull)
        ar1 = self._arBtnsTextFull[param:endindex]
        #print param
        #print endindex
        #print ar1

        ar2 = []
        for i in range(len(ar1)):
            ar2.append((self._btnCallFull, param+i))
        # add button to move forward
        ar1.append(">>")
        ar2.append((self._btnCallSepCounter,param+self.maxBtnsBeforeSeparator-1))
        # setting buttons
        self.set_buttons(ar1, ar2, self.vnButtonsStyle)

    def set_buttons_alt(self, arButTextsActions, style = "normal"):
        ar1 = []
        ar2 = []
        for i in range(len(arButTextsActions)):
            if (i % 2) == 0:
                ar1.append(arButTextsActions[i])
            else:
                ar2.append(arButTextsActions[i])
        self.set_buttons(ar1,ar2,style)

    def set_buttons_end_game(self):
        self.set_buttons(["End Game & Return >>"], [self._onEndGame])

    def _onEndGame(self,game):
        self.return_to_start_screen_clear()
    """
    def add_buttons(self, arButTexts, arButActions):
        a1 = self.vnButtons
        a2 = self.vnButtonsActions
        a1 = a1+arButTexts
        a2 = a2+arButActions
        self.set_buttons(a1,a2)
    """

    def set_text(self, char, text):
        char0 = char.split("//")[0]

        self.curCharText = char0
        self.curCharFull = char
        if text.startswith("!"):
            self.vnText = text[1:]
        else:
            self.vnText = text
        #self.OnGUI(self)
        if self.onSetTextCallback != None:
            self.onSetTextCallback(self,char,text)
        self.event_dispatch("set_text",(char,text))

    def set_text_s(self,text):
        self.set_text("s", text)
    
    def register_char(self, name, color, showname):
        self.registeredChars[name] = [color, showname]
    
    def texts_next(self, nexttexts, endfunc):
        self.nextTexts = nexttexts
        self.endNextTextFunc = endfunc
        self.NextText(self)
        
    def NextText(self, game):
        if(len(self.nextTexts) > 0):
            self.set_text(self.nextTexts[0][0],self.nextTexts[0][1])
            self.set_buttons([self.btnNextText],[self.NextText])
            if(len(self.nextTexts[0]) > 2):
                func = self.nextTexts[0][2]
                func(self,self.nextTexts[0][3])
            self.nextTexts.pop(0)
        else:
            self.endNextTextFunc(self)
    
    def show_window(self):
        self.visible = True
        
    def hide_window(self):
        self.visible = False

    def toggle_window(self,p1="",p2=""):
        self.visible = not self.visible

    def toggle_window_to(self,p1):
        self.visible = p1
    
    def show_blocking_message(self, text = "..."):
        self.funcLockedText = text
        self.isFuncLocked = True
        
    def hide_blocking_message(self,game=None):
        self.isFuncLocked = False

    def show_blocking_message_time(self, text = "...", duration = 3):
        self.show_blocking_message(text)
        self.set_timer(duration, self.hide_blocking_message)
        
        
    # simulating key presses
    def anim_sim_zoom_in(self,duration):
        InputSimulator.SimulateKeyDown(VirtualKeyCode.UP)
        self.set_timer(duration,self._anim_sim_zoom_in_end)

    def _anim_sim_zoom_in_end(self,game):
        InputSimulator.SimulateKeyUp(VirtualKeyCode.UP)
        
    def anim_sim_zoom_out(self,duration):
        InputSimulator.SimulateKeyDown(VirtualKeyCode.DOWN)
        self.set_timer(duration,self._anim_sim_zoom_out_end)

    def _anim_sim_zoom_out_end(self,game):
        InputSimulator.SimulateKeyUp(VirtualKeyCode.DOWN)
        
    # reseting scene - must be overrided by engine
    def reset(self):
        return
    
    def call_game_func(self,param):
        try:
            #print param
            if param == None:
                return

            if isinstance(param,tuple):
                if len(param) == 2: # (?, ?)
                    if isinstance(param[0],list): # ([func] param)
                        param[0](param[1])
                    else:
                        param[0](self,param[1]) # (func param)
                    return
            elif isinstance(param,list): # [func]
                    #print "new call"
                    param[0]()
            else:
                # default - call func(game)
                param(self)
        except Exception, e:
            import traceback
            traceback.print_exc()
            print "Error in call_game_func: "+str(e)


    def load_scene(self, file):
        """Load scene from file"""
        self.show_blocking_message_time("ERROR: load_scene was not implemented")

    def get_scene_dir(self):
        """Return dir, where engine saves scenes"""
        # must be implemented in child
        return ""

    def get_camera_num(self, camnum):
        self.show_blocking_message_time("ERROR: get_camera_num was not implemented")
        return self.camparams2vec((0,0,0), (0,0,0), (0,0,0))

    def anim_to_camera_num(self, duration, camnum, style="linear", onCameraEnd=None):
        """
        Made animation movement to camera with some number
        :param float duration: Duration of animation in seconds
        :param int camnum: Camera number to animate from current position
        :param * style: may be an object or string. String can be linear,slow-fast,fast-slow,slow-fast3,fast-slow3,slow-fast4,fast-slow4. Object may vary
        :param Callable onCameraEnd: function that wil called after animation end
        """
        #self.show_blocking_message_time("ERROR: anim_to_camera_num was not implemented")
        self.anim_to_camera_obj(duration,self.get_camera_num(camnum),style,onCameraEnd)

    def scene_get_all_females(self):
        return []

    def scene_get_all_males(self):
        return []

    def debug_print_all_chars(self):
        fems = self.scene_get_all_females()
        print("-- Female scene chars: --")
        for i in range(len(fems)):
            print "%s: %s" % (str(i), fems[i].text_name)
        fems = self.scene_get_all_males()
        print("-- Male scene chars: --")
        for i in range(len(fems)):
            print "%s: %s"%(str(i),fems[i].text_name)
        self.show_blocking_message_time("Debug: list of chars printed in console!")

    # ---------- menu functions -------------------------
    def run_menu(self,menufunc,menuparam,onEndFunc):
        self._menuStack.append(onEndFunc)
        menufunc(self,menuparam)

    def menu_finish(self,result):
        self.menu_result = result
        endFunc = self._menuStack.pop()
        self.call_game_func(endFunc)

    # ---------- checking for engine types --------------
    @property
    def isClassicStudio(self):
        return self.engine_name == "studio"
        
    @property
    def isStudioNEO(self):
        return self.engine_name == "neo"

    @property
    def isNEOV2(self):
        return self.engine_name == "neov2"

    @property
    def isCharaStudio(self):
        return self.engine_name == "charastudio"

    @property
    def isPlayHomeStudio(self):
        return self.engine_name == "phstudio"

    # -------- other ----------
    def scene_set_bg_png(self, filepng):
        self.show_blocking_message_time("ERROR: scene_set_bg_png was not implemented")

    # ---------- cameras ----------
    def move_camera(self, pos=None, distance=None, rotate=None, fov=23.0):
        #self.show_blocking_message_time("ERROR: move_camera was not implemented")
        camobj = self.camparams2vec(pos,distance,rotate,fov)
        self.move_camera_obj(camobj)

    def move_camera_obj(self,camobj):
        camv = self.cam2vec(camobj)
        self.move_camera_direct(camv["pos"], camv["distance"], camv["rotate"], camv["fov"])

    def camparams2vec(self, pos, distance, rotate, fov=23.0):
        obj = {}
        if pos:
            if isinstance(pos, tuple) and len(pos) == 3:
                pos = Vector3(pos[0], pos[1], pos[2])
            if isinstance(pos, Vector3):
                obj["pos"] = pos
        if distance:
            if isinstance(distance, tuple) and len(distance) == 3:
                distance = Vector3(distance[0], distance[1], distance[2])
            if isinstance(distance, Vector3):
                obj["distance"] = distance
        if rotate:
            if isinstance(rotate, tuple) and len(rotate) == 3:
                rotate = Vector3(rotate[0], rotate[1], rotate[2])
            if isinstance(rotate, Vector3):
                obj["rotate"] = rotate
        obj["fov"] = fov
        return obj

    def cam2vec(self,camobj):
        return self.camparams2vec(camobj["pos"], camobj["distance"], camobj["rotate"], camobj["fov"])

    def move_camera_direct(self, pos=None, distance=None, rotate=None, fov=23.0):
        # expecting only Vectors3
        self.show_blocking_message_time("ERROR: move_camera_direct was not implemented")

    def anim_to_camera(self, duration, pos=None, distance=None, rotate=None, fov=23.0, style="linear", onCameraEnd=None):
        camobj = self.camparams2vec(pos,distance,rotate,fov)
        self.anim_to_camera_obj(duration,camobj,style,onCameraEnd)

    def anim_to_camera_obj(self, duration, camobj, style="linear",
                           onCameraEnd=None):
        self._anim_to_camera_savecurrentpos()
        # print "Anim to cam 1"
        # print "Anim to cam 2"
        camobjv = self.cam2vec(camobj)
        self.camTPos = camobjv["pos"]
        self.camTDir = camobjv["distance"]
        self.camTAngle = camobjv["rotate"]
        self.camTFOV = camobjv["fov"]

        if isinstance(style, str):
            self.camAnimStyle = style
            self.camAnimFullStyle = None
        else:
            self.camAnimStyle = style["style"]
            self.camAnimFullStyle = style
            if 'add_distance_target_camera' in self.camAnimFullStyle:
                self.camTDir = Vector3(self.camTDir.x, self.camTDir.y,
                                       self.camTDir.z + self.camAnimFullStyle["add_distance_target_camera"])

        # camera animation one timer only
        if self.camAnimeTID != -1:
            self.clear_timer(self.camAnimeTID)
        self.camAnimeTID = self.set_timer(duration, self._anim_to_cam_end, self._anim_to_cam_upd)

        self._onCameraEnd = onCameraEnd

        if self.isHideWindowDuringCameraAnimation:
            self.hide_window()

    def _anim_to_cam_upd(self, game, dt, time, duration):

        camProgress = time / duration

        if self.camAnimStyle == "linear":
            camProgress = time / duration
        if self.camAnimStyle == "slow-fast":
            camProgress = Mathf.Pow(camProgress, 2)
        if self.camAnimStyle == "fast-slow":
            camProgress = 1 - Mathf.Pow(1 - camProgress, 2)
        if self.camAnimStyle == "slow-fast3":
            camProgress = Mathf.Pow(camProgress, 3)
        if self.camAnimStyle == "fast-slow3":
            camProgress = 1 - Mathf.Pow(1 - camProgress, 3)
        if self.camAnimStyle == "slow-fast4":
            camProgress = Mathf.Pow(camProgress, 4)
        if self.camAnimStyle == "fast-slow4":
            camProgress = 1 - Mathf.Pow(1 - camProgress, 4)


        TPos = self.camTPos
        TDir = self.camTDir
        TAngle = self.camTAngle

        if self.camAnimFullStyle != None:
            if 'target_camera_zooming_in' in self.camAnimFullStyle:
                TDir = Vector3(TDir.x, TDir.y,
                               TDir.z - self.camAnimFullStyle["target_camera_zooming_in"] * (1 - time / duration))
            if 'target_camera_rotating_z' in self.camAnimFullStyle:
                TAngle = Vector3(TAngle.x,
                                 TAngle.y,
                                 TAngle.z + self.camAnimFullStyle["target_camera_rotating_z"] * (1 - time / duration))
            if 'target_camera_rotating_x' in self.camAnimFullStyle:
                TAngle = Vector3(TAngle.x + self.camAnimFullStyle["target_camera_rotating_x"] * (1 - time / duration),
                                 TAngle.y,
                                 TAngle.z )
            if 'target_camera_rotating_y' in self.camAnimFullStyle:
                TAngle = Vector3(TAngle.x,
                                 TAngle.y + self.camAnimFullStyle["target_camera_rotating_y"] * (1 - time / duration),
                                 TAngle.z)
            if 'target_camera_posing_y' in self.camAnimFullStyle:
                TPos = Vector3(TPos.x,
                               TPos.y + self.camAnimFullStyle["target_camera_posing_y"] * (1 - time / duration),
                               TPos.z)
                # TDir.z = TDir.z + self.camAnimFullStyle["move_distance"] * time / duration
                # TDir.z = TDir.z + (-20)
                # print "z: %s"%(str(TDir.z))

        pos = Vector3.Lerp(self.camSPos, TPos, camProgress)
        distance = Vector3.Lerp(self.camSDir, TDir, camProgress)
        rotate = Vector3.Slerp(self.camSAngle, TAngle, camProgress)
        fov = Mathf.Lerp(self.camSFOV, self.camTFOV, camProgress)
        #print fov, self.camSFOV, self.camTFOV, camProgress
        self.move_camera_direct(pos, distance, rotate, fov)

    def _anim_to_cam_end(self, game):
        # game.set_text("Anim camera end!")
        # print "Anim camera end!"
        if self.isHideWindowDuringCameraAnimation:
            self.show_window()
        self.camAnimeTID = -1
        self.call_game_func(self._onCameraEnd)
        return

    def _anim_to_camera_savecurrentpos(self):
        camobj = self.get_camera_num(0)
        self.camSPos = camobj["pos"]
        self.camSDir = camobj["distance"]
        self.camSAngle = camobj["rotate"]
        self.camSFOV = camobj["fov"]

    def vec3(self,x,y,z):
        return Vector3(x,y,z)

    # ---- automaking list of games -----
    def prepare_auto_games(self,game):
        self.isTitleScreen = False
        self.prepare_auto_games_prefix(game,"")

    def prepare_auto_games_prefix(self,game,prefix):
        from os import listdir
        from os.path import isfile, join
        mypath = self.pygamepath
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        arTx = []
        arTx2 = []
        arAc = []

        for fil in onlyfiles:
            #print fil[:-3]
            if fil.endswith(".py"):
                firstline = self.file_get_firstline(mypath+"\\"+fil)
                #print firstline
                ar = firstline.split(";")
                # checking header
                if len(ar) >= 3:
                    if ar[0] == "#vngame":
                        if (ar[1] == "all") or (ar[1] == self.engine_name):
                            # found game!
                            #print "-- Found game! --"
                            gamename = ar[2]
                            if gamename[-1] == "\n":
                                gamename = gamename[:-1]

                            # Add game or folder if prefix matches. Unless the name already exists.
                            # (An empty prefix will match all games)
                            if gamename.startswith(prefix):
                                # Remove prefix from gamename
                                if len(prefix) > 0:
                                    gamename = gamename[len(prefix):]
                                # If gamename looks like a folder, just keep the foldername
                                if '/' in gamename:
                                    gamename = gamename.split("/")[0]
                                    gamename = gamename + "/"
                                if not gamename in arTx2:
                                    arTx2.append(gamename)
                                    if '/' in gamename:
                                        arTx.append("<color=#aaaaaaff>"+gamename[:-1]+ " ></color>")
                                        arAc.append((self.prepare_auto_games_prefix, prefix + gamename))
                                    else:
                                        arTx.append(gamename)
                                        arAc.append((self.game_start_fromfile, fil[:-3]))

        # IF we have a prefix, add button to go back one level
        if len(prefix) > 0:
            parent = "/".join(prefix.split("/")[:-2]) # Get parent-prefix
            # Add a / but only if the prefix we want to go to is non-empty
            if parent:
                parent = parent + "/"
            arTx.append("<< Back")
            arAc.append((self.prepare_auto_games_prefix, parent))

        self.set_text_s("Available games:")
        self.set_buttons(arTx,arAc)


    def game_start_fromfile(self,game,gamefilestr):
        oldcurrentgame = self.current_game
        print "-- Importing and starting game: %s --"%(gamefilestr)
        try:
            self.current_game = gamefilestr
            if gamefilestr != "scenesavestate": # special case for scene save state
                importOrReload(gamefilestr)
            else:
                print "running scenesavestate..."
                import scenesavestate
            import sys
            sys.modules[gamefilestr].start(self)
            self.isTitleScreen = False
        except Exception, e:
            print("Error in game loading: " + str(e))
            import traceback
            print "details:"
            traceback.print_exc()

            self.show_blocking_message_time("ERROR: can't load or start game '%s'"%(gamefilestr))
            self.current_game = oldcurrentgame

        #__import__(gamefilestr).start(self)


    def file_get_firstline(self,filename):
        import os
        if os.path.exists(filename):
            fp = open(filename, "r")
            content = fp.readline()
            fp.close()
            return content
        return ""

    def file_get_firstline_utf8(self,filename):
        import os
        import codecs
        if os.path.exists(filename):
            fp = codecs.open(filename, "r", encoding="utf-8")
            content = fp.readline()
            fp.close()
            return content
        return ""

    def file_get_content(self,filename):
        import os
        if os.path.exists(filename):
            fp = open(filename, "r")
            content = fp.read()
            fp.close()
            return content
        return ""

    def file_get_content_utf8(self,filename):
        import os
        import codecs
        if os.path.exists(filename):
            fp = codecs.open(filename, "r", encoding="utf-8")
            content = fp.read()
            fp.close()
            return content
        return ""


    # ------------ event system -----------
    def event_reg_listener(self,eventid,func,funcid="_unnamed", persistent = False):
        self._event_create_lisarray_ifneeded(eventid)
        self._eventListenerDic[eventid].append((func, funcid, persistent))

    def _event_create_lisarray_ifneeded(self,eventid):
        if eventid in self._eventListenerDic:
            return
        else:
            self._eventListenerDic[eventid] = []

    def event_unreg_listener(self,eventid,func,funcid="_unnamed"):
        ret = False
        if eventid in self._eventListenerDic:
            for evt in self._eventListenerDic[eventid]:
                if evt[1] == "_unnamed":
                    # old logic
                    if evt[0] == func:
                        self._eventListenerDic[eventid].remove(evt)
                        ret = True
                else:
                    # new logic
                    if evt[1] == funcid:
                        self._eventListenerDic[eventid].remove(evt)
                        ret = True
        return ret

    def event_dispatch(self,eventid,param):
        if eventid in self._eventListenerDic:
            for evt in self._eventListenerDic[eventid]:
                func = evt[0]
                func(self,eventid,param)

    def event_is_reg_funcid(self,eventid,funcid):
        if eventid in self._eventListenerDic:
            for evt in self._eventListenerDic[eventid]:
                if evt[1] == funcid:
                    return True
        return False

    def _load_scene_before(self,file):
        self._unload_scene_before()
        self.event_dispatch("before_scene_load", file)

    def _unload_scene_before(self):
        self.event_dispatch("before_scene_unload", None)
        self.scenedata = GData()

    # -------- game persistent data ----------
    def gpersdata_getfilename(self, fname=None):
        from os import path
        if fname == None: 
            fname = self.current_game + "_p"
        fname = fname.lower()
        if not fname.endswith(".dat"):
            fname += ".dat"
        dstfile = path.join(self.pygamepath, "Gpdata", fname)
        return dstfile

    def gpersdata_exists(self, fname=None):
        dstfile = self.gpersdata_getfilename(fname)
        from os import path
        return path.isfile(dstfile)

    def gpersdata_load(self, fname=None):
        loaded = False
        try:
            dstfile = self.gpersdata_getfilename(fname)
            if self.gpersdata_exists(fname):
                with open(dstfile, "r") as f2:
                    import pickle
                    self.gpersdata = pickle.load(f2)
                    f2.close()
                msg = "gpersdata loaded!"
                loaded = True
            else:
                msg = "gpersdata <%s> not exists!"%dstfile
        except Exception as e:
            msg = "gpersdata load Failed: " + str(e)
        # game.show_blocking_message_time(msg)
        print msg
        return loaded

    def gpersdata_save(self, fname=None):
        try:
            dstfile = self.gpersdata_getfilename(fname)
            with open(dstfile, "w") as f:
                import pickle
                pickle.dump(self.gpersdata, f)
                f.close()
            print "gpersdata saved into <%s>"%dstfile
            return True
        except Exception as e:
            msg = "gpersdata save Failed: " + str(e)
            print msg
            return False
        # game.show_blocking_message_time(msg)


    def gpersdata_set(self,param,val):
        self.gpersdata[param] = val
        return self.gpersdata_save()

    def gpersdata_get(self,param):
        if param in self.gpersdata:
            return self.gpersdata[param]
        else:
            return None

    def gpersdata_clear(self, fname=None):
        import os
        try:
            dstfile = self.gpersdata_getfilename(fname)
            os.remove(dstfile)
            self.gpersdata = {}
            msg = "gpersdata cleared!"
        except Exception as e:
            msg = "gpersdata clear Failed: " + str(e)
        print msg

    # ---------- checkpoints --------
    def checkpoint_set_list(self,type,arr):
        if not hasattr(self.gdata, '_check_list'):
            self.gdata._check_list = {}

        self.gdata._check_list[type] = arr

    def checkpoint_save(self,type,checkId):
        arr = self.checkpoint_loadall(type)
        if checkId in arr:
            pass
            return ""
        else:
            arr.append(checkId)
            return self.gpersdata_set("_checkpoints_"+type, arr)

    def checkpoint_loadall(self,type):
        res = self.gpersdata_get("_checkpoints_"+type)
        if res == None:
            return []
        else:
            return res

    def checkpoint_clean(self,type):
        self.gpersdata_set("_checkpoints_" + type, [])

    def checkpoint_goto(self,type,checkId):
        arr = self.gdata._check_list[type]
        for checkpoint in arr:
            if checkpoint[0] == checkId:
                self.call_game_func(checkpoint[1])
                return True
        return False

    def checkpoint_has_one(self,type):
        return len(self.checkpoint_loadall(type)) > 0

    def checkpoint_goto_latest(self,type):
        arr = self.checkpoint_loadall(type)
        if len(arr) > 0:
            return self.checkpoint_goto(type,arr[-1])
        return False

    def checkpoint_rendergotomenu(self,type,showall=True):
        btns = []
        arr = self.gdata._check_list[type]
        arrpassed = self.checkpoint_loadall(type)
        for checkpoint in arr:
            checkId = checkpoint[0]
            if checkId in arrpassed:
                btns += [checkpoint[2][0],(self._checkpoint_goto_menu,(type,checkId))]
            else:
                if showall:
                    txt = '<color=#{1}ff>{0}</color>'.format(checkpoint[2][0], '666666')
                    btns += [txt, None]
        return btns

    def _checkpoint_goto_menu(self,game,param):
        self.checkpoint_goto(param[0],param[1])

    # --------- skin system ------------
    def skin_set(self, skin):
        self.skin = skin
        self.skin.setup(self)

    def skin_set_byname(self,skinname):
        try:
            mod = import_or_reload(skinname)
            skin = mod.get_skin()
            self.skin_set(skin)
        except Exception, e:
            print "Error loading skin ", skinname, ", error: ", e

    def skin_get_current(self):
        return self.skin

def vngame_window_studio(vnButtonsStart, vnButtonsActionsStart):
    import vngameenginestudio
    game = vngameenginestudio.vngame_window_studio(vnButtonsStart, vnButtonsActionsStart)
    return game

class HSNeoOCI(object):    
    def __init__(self, objctrl):
        self.objctrl = objctrl
        return
    
    #changed by chickenman
    @staticmethod
    def create_from(objctrl):
        from Studio import OCIFolder, OCIChar, Studio, OCIItem, OCILight
        if isinstance(objctrl,OCIFolder):
            return HSNeoOCIFolder(objctrl)
        if isinstance(objctrl,OCIChar):
            return HSNeoOCIChar(objctrl)
        if isinstance(objctrl,OCIItem):
            return HSNeoOCIItem(objctrl)
        if isinstance(objctrl,OCILight):
            return HSNeoOCILight(objctrl)
        try:
            from Studio import OCIRoute
            if isinstance(objctrl, OCIRoute):
                return HSNeoOCIRoute(objctrl)
        except:
            pass
        return HSNeoOCI(objctrl)


    @staticmethod
    def create_from_treenode(treenode):
        if treenode == None:
            return None

        from Studio import OCIFolder, OCIChar, Studio
        studio = Studio.Instance
        """ :type : dummyneoclasses.Studio"""

        dobjctrl = studio.dicInfo
        obj = dobjctrl[treenode]
        if obj != None:
            return HSNeoOCI.create_from(obj)
        return None

    @staticmethod
    def create_from_selected():
        from Studio import OCIFolder, OCIChar, Studio
        studio = Studio.Instance
        """ :type : dummyneoclasses.Studio"""
        return HSNeoOCI.create_from_treenode(studio.treeNodeCtrl.selectNode)

    @property
    def visible_treenode(self):
        return self.objctrl.treeNodeObject.visible

    @visible_treenode.setter
    def visible_treenode(self,value):
        if self.objctrl.treeNodeObject.visible != value:
            self.objctrl.treeNodeObject.SetVisible(value)

    @property
    def treeNodeObject(self):
        obj = self.objctrl.treeNodeObject
        """ :type : dummyneoclasses.TreeNodeObject"""

        return obj

    def set_parent_treenodeobject(self,parentTreeNode):
        from Studio import Studio
        studio = Studio.Instance
        studio.treeNodeCtrl.SetParent(self.treeNodeObject, parentTreeNode)

    def set_parent(self,parent):
        self.set_parent_treenodeobject(parent.treeNodeObject)

    def delete(self):
        from Studio import Studio
        studio = Studio.Instance
        """ :type : dummyneoclasses.Studio"""
        studio.treeNodeCtrl.DeleteNode(self.treeNodeObject)

    @property
    def text_name(self):
        return self.objctrl.treeNodeObject.textName

class HSNeoOCIProp(HSNeoOCI):

    globalPropClass = None

    @property
    def as_prop(self):
        from vnactor import Prop,PropHSNeo,PropCharaStudio,PropPHStudio,PropNeoV2
        # we are Prop already
        if isinstance(self, Prop):
            return self

        # in case we want special class handling
        if HSNeoOCIProp.globalPropClass:
            return HSNeoOCIProp.globalPropClass(self.objctrl)

        # make prop depending on engine
        enid = get_engine_id()
        obj = None
        if enid == "neo":
            obj = PropHSNeo(self.objctrl)
        if enid == "phstudio":
            obj = PropPHStudio(self.objctrl)
        if enid == "charastudio":
            obj = PropCharaStudio(self.objctrl)
        if enid == "neov2":
            obj = PropNeoV2(self.objctrl)

        return obj

class HSNeoOCIFolder(HSNeoOCIProp):
    @staticmethod
    def add(name = None):
        from Studio import AddObjectFolder
        fold = AddObjectFolder.Add()
        obj = HSNeoOCIFolder(fold)
        if name != None:
            obj.name = name
        return obj

    @staticmethod
    def find_all(name=None):
        from Studio import OCIFolder, Studio
        studio = Studio.Instance
        """ :type : dummyneoclasses.Studio"""
        ar = []
        dobjctrl = studio.dicInfo
        for key in dobjctrl.Keys:  # key is TreeNodeObject
            objctrl = dobjctrl[key]
            if isinstance(objctrl, OCIFolder):
                txt = objctrl.name
                # ar.append((objctrl.name, objctrl, key))
                if txt == name:
                    ar.append(HSNeoOCIFolder(objctrl))
                    # this will process for all folders we found

        return ar

    @staticmethod
    def find_single(name=None):
        ar = HSNeoOCIFolder.find_all(name)
        obj = None
        """ :type : HSNeoOCIFolder"""
        if len(ar) > 0:
            obj = ar[0]
        return obj

    @staticmethod
    def find_all_startswith(name=None):
        from Studio import OCIFolder, Studio
        studio = Studio.Instance
        """ :type : dummyneoclasses.Studio"""
        ar = []
        dobjctrl = studio.dicInfo
        for key in dobjctrl.Keys:  # key is TreeNodeObject
            objctrl = dobjctrl[key]
            if isinstance(objctrl, OCIFolder):
                txt = objctrl.name
                """ :type txt: string """
                if txt.startswith(name):
                    ar.append(HSNeoOCIFolder(objctrl))
                    # this will process for all folders we found

        return ar

    @staticmethod
    def find_single_startswith(name=None):
        ar = HSNeoOCIFolder.find_all_startswith(name)
        obj = None
        """ :type : HSNeoOCIFolder"""
        if len(ar) > 0:
            obj = ar[0]
        return obj

    @property
    def name(self):
        return self.objctrl.name

    @name.setter
    def name(self,value):
        self.objctrl.name = value

    def delete_all_children(self):
        ar = self.treeNodeObject.child
        ar2 = []
        for treeobj in ar:
            ar2.append(HSNeoOCI.create_from_treenode(treeobj))

        for obj in ar2:
            obj.delete()

    @property
    def pos(self):
        return self.objctrl.objectInfo.changeAmount.pos

    @property
    def rot(self):
        return self.objctrl.objectInfo.changeAmount.rot

    def set_pos(self, param):
        # param = (pos_x, pos_y, pos_z)
        item = self.objctrl
        ncp = Vector3(param[0], param[1], param[2])
        item.objectInfo.changeAmount.pos = ncp

    def set_rot(self, param):
        # param = (rot_x, rot_y, rot_z)
        try:
            item = self.objctrl
            nrt = Vector3(param[0], param[1], param[2])
            item.objectInfo.changeAmount.rot = nrt
        except Exception, e:
            print "Error in set_rot %s"%(str(e))

class HSNeoOCIItem(HSNeoOCIProp):
    def __init__(self, objctrl):
        self.objctrl = objctrl
        """ :type : dummyneoclasses.OCIItem"""
        return

    @staticmethod
    def add_item(no):
        from Studio import AddObjectItem
        objctrl = AddObjectItem.Add(no)
        return HSNeoOCIItem(objctrl)

    def pos_add(self, param):
        # param = (pos_delta_x, pos_delta_y, pos_delta_z)
        item = self.objctrl
        cp = item.objectInfo.changeAmount.pos
        ncp = Vector3(cp.x + param[0], cp.y + param[1], cp.z + param[2])
        item.objectInfo.changeAmount.pos = ncp

    def set_pos(self, param):
        # param = (pos_x, pos_y, pos_z)
        item = self.objctrl
        ncp = Vector3(param[0], param[1], param[2])
        item.objectInfo.changeAmount.pos = ncp

    def rot_add(self, param):
        # param = (rot_delta_x, rot_delta_y, rot_delta_z)
        item = self.objctrl
        rt = item.objectInfo.changeAmount.rot
        nrt = Vector3(rt.x + param[0], rt.y + param[1], rt.z + param[2])
        item.objectInfo.changeAmount.rot = nrt

    def set_rot(self, param):
        # param = (rot_x, rot_y, rot_z)
        item = self.objctrl
        nrt = Vector3(param[0], param[1], param[2])
        item.objectInfo.changeAmount.rot = nrt

    def scale_add(self, param):
        # param = (scale_x, scale_y, scale_z) or scale
        item = self.objctrl
        from Studio import OCIItem
        if isinstance(item, OCIItem):
            # for item only, folder can not set scale
            rt = item.itemInfo.changeAmount.scale
            nrt = Vector3(rt.x + param[0], rt.y + param[1], rt.z + param[2])
            item.itemInfo.changeAmount.scale = nrt

    def set_scale(self, param):
        # param = (scale_x, scale_y, scale_z) or scale
        item = self.objctrl
        from Studio import OCIItem
        if isinstance(item, OCIItem):
            # for item only, folder can not set scale
            if isinstance(param, tuple):
                nsl = Vector3(param[0], param[1], param[2])
            else:
                nsl = Vector3(param, param, param)
            item.itemInfo.changeAmount.scale = nsl

    @property
    def pos(self):
        return self.objctrl.itemInfo.changeAmount.pos

    @property
    def rot(self):
        return self.objctrl.itemInfo.changeAmount.rot

    @property
    def scale(self):
        return self.objctrl.itemInfo.changeAmount.scale

    @property
    def no(self):
        return self.objctrl.itemInfo.no

#changed by chickenman
class HSNeoOCILight(HSNeoOCIProp):
    def __init__(self, objctrl):
        self.objctrl = objctrl
        """ :type : dummyneoclasses.OCILight"""
        return
    
    @staticmethod
    def add_light(no): #no:0~8
        from Studio import AddObjectLight
        objctrl = AddObjectLight.Add(no)
        return HSNeoOCILight(objctrl)
    
    def pos_add(self, param):
        # param = (pos_delta_x, pos_delta_y, pos_delta_z)
        item = self.objctrl
        cp = item.objectInfo.changeAmount.pos
        ncp = Vector3(cp.x + param[0], cp.y + param[1], cp.z + param[2])
        item.objectInfo.changeAmount.pos = ncp

    def set_pos(self, param):
        # param = (pos_x, pos_y, pos_z)
        item = self.objctrl
        ncp = Vector3(param[0], param[1], param[2])
        item.objectInfo.changeAmount.pos = ncp

    def rot_add(self, param):
        # param = (rot_delta_x, rot_delta_y, rot_delta_z)
        item = self.objctrl
        rt = item.objectInfo.changeAmount.rot
        nrt = Vector3(rt.x + param[0], rt.y + param[1], rt.z + param[2])
        item.objectInfo.changeAmount.rot = nrt

    def set_rot(self, param):
        # param = (rot_x, rot_y, rot_z)
        item = self.objctrl
        nrt = Vector3(param[0], param[1], param[2])
        item.objectInfo.changeAmount.rot = nrt
    
    @property
    def enable(self):
        return self.objctrl.lightInfo.enable
    
    @property
    def type(self):
        return self.objctrl.lightType
    
    @property
    def no(self):
        return self.objctrl.lightInfo.no
    
    @property
    def pos(self):
        return self.objctrl.objectInfo.changeAmount.pos

    @property
    def rot(self):
        return self.objctrl.objectInfo.changeAmount.rot

class HSNeoOCIRoute(HSNeoOCIProp):
    # Route only for KK and AI
    def __init__(self, objctrl):
        self.objctrl = objctrl
        """ :type : dummyneoclasses.OCILight"""
        return

    @property
    def pos(self):
        return self.objctrl.objectInfo.changeAmount.pos

    @property
    def rot(self):
        return self.objctrl.objectInfo.changeAmount.rot

class HSNeoOCIChar(HSNeoOCI):
    globalActorClass = None

    def __init__(self, objctrl):
        self.objctrl = objctrl
        """ :type : dummyneoclasses.OCIChar"""
        return

    @staticmethod
    def add_female(path):
        from Studio import AddObjectFemale
        objctrl = AddObjectFemale.Add(path)
        return HSNeoOCIChar(objctrl)

    @staticmethod
    def add_male(path):
        from Studio import AddObjectMale
        objctrl = AddObjectMale.Add(path)
        return HSNeoOCIChar(objctrl)

    @property
    def as_actor(self):
        from vnactor import Actor,ActorHSNeo,ActorPHStudio,ActorCharaStudio,ActorNeoV2
        if isinstance(self,Actor):
            return self

        if HSNeoOCIChar.globalActorClass:
            return HSNeoOCIChar.globalActorClass(self.objctrl)

        enid = get_engine_id()
        obj = None
        if enid == "neo":
            obj = ActorHSNeo(self.objctrl)
        if enid == "phstudio":
            obj = ActorPHStudio(self.objctrl)
        if enid == "charastudio":
            obj = ActorCharaStudio(self.objctrl)
        if enid == "neov2":
            obj = ActorNeoV2(self.objctrl)

        return obj

    @property
    def charInfo(self):
        return self.objctrl.charInfo

    @property
    def oiCharInfo(self):
        return self.objctrl.oiCharInfo
        
    @property
    def pos(self):
        return self.charInfo.transform.localPosition
        
    @property
    def rot(self):
        return self.charInfo.transform.localRotation.eulerAngles
   
    @property
    def scale(self):
        return self.charInfo.transform.localScale   

    @property
    def look_eyes_ptn(self):
        try:
            return self.objctrl.charInfo.GetLookEyesPtn()
        except Exception, e:
            print str(e)
        return ""

    @look_eyes_ptn.setter
    def look_eyes_ptn(self,value):
        self.objctrl.charInfo.ChangeLookEyesPtn(value)

    @property
    def look_neck_ptn(self):
        try:
            return self.objctrl.charInfo.GetLookNeckPtn()
        except Exception, e:
            print str(e)
        return ""

    @look_neck_ptn.setter
    def look_neck_ptn(self, value):
        self.objctrl.charInfo.ChangeLookNeckPtn(value)

    @property
    def mouth_ptn(self):
        try:
            return self.objctrl.charInfo.GetMouthPtn()
        except Exception, e:
            print str(e)
        return ""

    @mouth_ptn.setter
    def mouth_ptn(self, value):
        self.objctrl.charInfo.ChangeMouthPtn(value)

    @property
    def mouth_openmax(self):
        try:
            return self.objctrl.charInfo.GetMouthOpenMax()
        except Exception, e:
            print str(e)
        return ""

    @mouth_openmax.setter
    def mouth_openmax(self, value):
        self.objctrl.charInfo.ChangeMouthOpenMax(value)

    @property
    def eyes_ptn(self):
        try:
            return self.objctrl.charInfo.GetEyesPtn()
        except Exception, e:
            print str(e)
        return ""

    @eyes_ptn.setter
    def eyes_ptn(self, value):
        self.objctrl.charInfo.ChangeEyesPtn(value)

    @property
    def eyes_openmax(self):
        try:
            return self.objctrl.charInfo.GetEyesOpenMax()
        except Exception, e:
            print str(e)
        return ""

    @eyes_openmax.setter
    def eyes_openmax(self, value):
        self.objctrl.charInfo.ChangeEyesOpenMax(value)

    @property
    def eyebrow_ptn(self):
        try:
            return self.objctrl.charInfo.GetEyebrowPtn()
        except Exception, e:
            print str(e)
        return ""

    @eyebrow_ptn.setter
    def eyebrow_ptn(self, value):
        self.objctrl.charInfo.ChangeEyebrowPtn(value)

    @property
    def tears_level(self):
        try:
            return self.objctrl.GetTearsLv()
        except Exception, e:
            print str(e)
        return ""

    @tears_level.setter
    def tears_level(self, value):
        self.objctrl.SetTearsLv(value)

    def move(self, pos=None, rot=None, scale=None):
        #if not self.stChara: return False
        
        from UnityEngine import Vector3
        if pos:
            if isinstance(pos, tuple) and len(pos) == 3:
                pos = Vector3(pos[0], pos[1], pos[2])
            #self.stChara.objCtrl.transform.localPosition = pos
            #self.charInfo.SetPosition(pos);
            self.charInfo.transform.localPosition = pos
            
        if rot:
            if isinstance(rot, tuple) and len(rot) == 3:
                rot = Vector3(rot[0], rot[1], rot[2])
            #self.charInfo.SetRotation(rot)
            self.charInfo.transform.localRotation.eulerAngles = rot
            
        if scale:
            if isinstance(scale, tuple) and len(scale) == 3:
                scale = Vector3(pos[0], pos[1], pos[2])
            #self.stChara.objCtrl.transform.localPosition = pos
            #self.objctrl.charInfo.chaBody.objAnim.transform.localScale = localScale; 
            self.charInfo.transform.localScale = scale
            
        return True

    
    def animate(self,group,category,no,animePattern,animeSpeed):
        #print "1"
        try:
            self.oiCharInfo.animePattern = animePattern
        except Exception, e:
            # passing for PlayHome Studio - it has another pattern
            pass
        #print "2"
        #
        self.objctrl.LoadAnime(group, category, no, animeSpeed);
        #print "3"
        self.objctrl.animeSpeed = animeSpeed
        #self.charInfo.chaBody.animBody.speed = animeSpeed
        #print "4"
        #self.charInfo.chaBody.animBody.speed = animeSpeed
        #print "5"
        #self.objctrl.RestartAnime()
        #print "6"

    def animate2(self,group,category,no,animeSpeed):
        self.objctrl.LoadAnime(group, category, no);
        self.objctrl.animeSpeed = animeSpeed

    def restart_anime(self):
        self.objctrl.RestartAnime()

    #def animate2(self,category,group,no,animePattern,animeSpeed):
    # debug purpose - load info from dictionary
    def animate_some_info(self,group,category,no,animePattern,animeSpeed):
        #from Studio import Info
        #Info.Instance.LoadExcelData()
        
        print "21"
        #print str(Info.Instance.dicFemaleAnimeLoadInfo)
        dic0 = Info.Instance.dicFemaleAnimeLoadInfo
        for key in dic0.Keys:
            print key
        d1 = dic0[category]
        print str(d1)
        d2 = d1[group]
        print str(d2)
        animeLoadInfo = d2[no]
        print str(animeLoadInfo)
        print "%s %s %s"%(animeLoadInfo.bundlePath, animeLoadInfo.fileName, animeLoadInfo.clip)
        
        
    def female_all_clothes_state(self,state):
        self.objctrl.SetClothesStateAll(state)

        
    def dump_obj(self):
        #print "objctrlchar.move(pos=%s, rot=%s)"%(str(self.charInfo.GetPosition()), str(self.charInfo.GetRotation()))
        try:
            print "objctrlchar.move(pos=%s, rot=%s, scale=%s)"%(str(self.charInfo.transform.localPosition), str(self.charInfo.transform.localRotation.eulerAngles), str(self.charInfo.transform.localScale))
            print "objctrlchar.animate(%s, %s, %s, %s, %s)"%(str(self.oiCharInfo.animeInfo.group), str(self.oiCharInfo.animeInfo.category), str(self.oiCharInfo.animeInfo.no), str(self.oiCharInfo.animePattern), str(self.oiCharInfo.animeSpeed))
            #print "objctrlchar.tears_level = %s" % (str(self.tears_level))
        except Exception, e:
            print "# oops, error happened %s"%str(e)
        return


        
class VNNeoController(VNController): # for all engines, who derived NEO engine
    def __init__(self):
        VNController.__init__(self)

    def calc_py_path(self):
        from UnityEngine import Application
        from os import path
        rootfolder = path.realpath(path.join(Application.dataPath, '..'))

        # os.path.splitext(__file__)[0] + '.ini'
        pydirname = path.dirname(__file__)
        return path.relpath(pydirname, rootfolder)

        
    def to_camera(self,camnum):
        if self.isCharaStudio:
            # old code simulating key press
            ar = [VirtualKeyCode.VK_1,VirtualKeyCode.VK_2,VirtualKeyCode.VK_3,VirtualKeyCode.VK_4,VirtualKeyCode.VK_5,VirtualKeyCode.VK_6,VirtualKeyCode.VK_7,VirtualKeyCode.VK_8,VirtualKeyCode.VK_9,VirtualKeyCode.VK_0]
            InputSimulator.SimulateKeyPress(ar[camnum-1])
            # enable it due to fucking reason - in CharaStudio camera not always setting at correct position
        else:
            from Studio import Studio
            studio = Studio.Instance
            si = studio.sceneInfo
            cdatas = si.cameraData

            c = studio.cameraCtrl
            cdata = c.cameraData
            cdata.Copy(cdatas[camnum-1])
        """
        camobj = self.get_camera_num(camnum)
        self.move_camera_obj(camobj)
        """
    def move_camera_direct(self, pos=None, distance=None, rotate=None, fov=None):
        c = self.studio.cameraCtrl
        cdata = c.cameraData
        if pos:
            cdata.pos = pos
        if distance:
            cdata.distance = distance
        if rotate:
            cdata.rotate = rotate

        if fov:
            if c.fieldOfView != fov:
                c.fieldOfView = fov

    def hsneo_dump_camera(self):
        #import hs
        f = open('dumppython.txt', 'a+')
        import sys
        tmp = sys.stdout
        sys.stdout = f
        print("---DUMP! Camera----")
        #hs.HSCamera.dump()
        self.hsneo_dump_camera2()
        print("")
        sys.stdout = tmp
        f.close()
        self.show_blocking_message_time("Camera position dumped!")

    def hsneo_dump_camera2(self):
        from Studio import Studio
        studio = Studio.Instance
        c = studio.cameraCtrl
        cdata = c.cameraData
        print("game.move_camera(pos=%s, distance=%s, rotate=%s)"%(str(cdata.pos), str(cdata.distance), str(cdata.rotate)))
        print("# for VN Scene Script %s"%self.camera_calcstr_for_vnscene())
        print ("# other one: 'cam': {'goto_pos': ((%.3f, %.3f, %.3f), (%.3f, %.3f, %.3f), (%.3f, %.3f, %.3f))}, "%(cdata.pos.x, cdata.pos.y, cdata.pos.z, cdata.distance.x, cdata.distance.y, cdata.distance.z, cdata.rotate.x, cdata.rotate.y, cdata.rotate.z))

    def camera_calcstr_for_vnscene(self):
        st = 0

        if hasattr(self,"scLastRunnedState"):
            st = self.scLastRunnedState

        from Studio import Studio
        studio = Studio.Instance
        c = studio.cameraCtrl
        cdata = c.cameraData

        s1 = "%s,%s,%s,23.0"%(str(cdata.pos), str(cdata.distance), str(cdata.rotate))

        return "a:%s:camo:%s"%(str(st),s1.replace("(","").replace(")","").replace(" ",""))

    def dump_camera(self):
        self.hsneo_dump_camera()

    def dump_scene_vnframe(self):
        import vnframe
        import vnactor

        output = ""

        self.scenef_register_actorsprops()

        actors = self.scenef_get_all_actors()
        try:
            for id in actors:
                actor = self.scenef_get_actor(id)
                status = actor.export_full_status()
                output += ("'%s': " % id)+vnframe.script2string(status) + ",\n"
        except Exception as e:
            print "Error in status: ", e
            game.show_blocking_message_time("Error during dump actor %s!"%id)
            return

        props = self.scenef_get_all_props()
        try:
            for id in props:
                prop = self.scenef_get_propf(id)
                status = prop.export_full_status()
                output += ("'%s': " % id)+vnframe.script2string(status) + ",\n"
        except Exception as e:
            print "Error in status: ", e
            game.show_blocking_message_time("Error during dump prop %s!"%id)
            return

        output += "'sys': "+vnframe.script2string(vnactor.export_sys_status(self)) + ",\n"

        c = self.studio.cameraCtrl
        cdata = c.cameraData
        output += "'cam': {'goto_pos': ((%.3f, %.3f, %.3f), (%.3f, %.3f, %.3f), (%.3f, %.3f, %.3f))}\n" % (
            cdata.pos.x, cdata.pos.y, cdata.pos.z, cdata.distance.x, cdata.distance.y, cdata.distance.z, cdata.rotate.x,
            cdata.rotate.y, cdata.rotate.z)

        output = "{\n"+output+"}\n"

        try:
            f = open('dumppython.txt', 'a+')
            #f.write("import vnframe\nvnframe.act({\n")
            f.write(output)
            #f.write("})\n")
            f.write("\n")
            f.close()
        except Exception as e:
            print e

        #self.scenef_clean_actorsprops()

        self.show_blocking_message_time("VNFrame Scene dumped!")

    def dump_selected_vnframe(self):
        import vnframe
        import vnactor

        output = ""

        try:
            fem = HSNeoOCI.create_from_selected()
            actor = fem.as_actor
            status = actor.export_full_status()
            output += vnframe.script2string({'selected': status}) + "\n"
        except Exception as e:
            print "Error in status: ", e
            game.show_blocking_message_time("Error during dump actor %s!"%id)
            return

        try:
            f = open('dumppython.txt', 'a+')
            #f.write("import vnframe\nvnframe.act({\n")
            f.write(output)
            #f.write("})\n")
            f.write("\n")
            f.close()
        except Exception as e:
            print e

        #self.scenef_clean_actorsprops()

        self.show_blocking_message_time("VNFrame selected dumped!")

    def get_camera_num(self, camnum):
        studio = self.studio
        si = studio.sceneInfo
        cdatas = si.cameraData

        if camnum == 0:  # 0 camera is current camera. It may be interested due to some reasons
            c = studio.cameraCtrl
            cdata = c.cameraData
        else:
            cdata = cdatas[camnum - 1]

        camobj = self.camparams2vec(cdata.pos,cdata.distance,cdata.rotate,cdata.parse)
        #print camobj
        return camobj

    def reset(self):
        self._unload_scene_before()
        self.studio.InitScene(False)
    
    @property
    def studio(self):
        from Studio import Studio
        studio = Studio.Instance
        """ :type : dummyneoclasses.Studio"""
        return studio

    @property
    def studio_scene(self):
        return self.studio.sceneInfo

    def hsneo_dump_scene(self):
        f = open('dumppython.txt', 'a+')
        import sys
        tmp = sys.stdout
        sys.stdout = f
        print("---DUMP! Scene----")
        self.hsneo_dump_scene2()
        print("")
        sys.stdout = tmp
        f.close()
        
    def hsneo_dump_scene2(self):
        #print("Dumping scene 1!")
        from Studio import OCIChar
        #si = self.studio_scene
        dobjctrl = self.studio.dicObjectCtrl
        #print("Dumping scene 2!")
        print("# we are not dumping objects because of number... but you can enable it in code of hsneo_dump_scene2")
        for key in dobjctrl.Keys:
            objctrl = dobjctrl[key]
            #print(key)
            if isinstance(objctrl, OCIChar):
                print("objctrlchar = game.get_objctrl_num_tochar(%s) # char name %s, animid=%s"%(key, to_roman_file(objctrl.treeNodeObject.textName), to_roman_file(objctrl.charAnimeCtrl.name)))
                #print("objctrlchar = game.get_objctrl_num_tochar(%s) # char name" % (key))
                # objctrl.charAnimeCtrl.name
                pctrl = HSNeoOCIChar(objctrl)
                pctrl.dump_obj()
            else:
                #uncomment here to dump not only chars in scene
                #print("objctrl = game.get_objctrl_num(%s)"%(key))
                objctrl = objctrl
            #print key
        #print("Dumping scene End!")
        self.show_blocking_message_time("Scene dumped!")

    def dump_scene(self):
        if self.onDumpSceneOverride != None:
            self.onDumpSceneOverride(self)
        else:
            self.hsneo_dump_scene()

    def get_objctrl_num(self,num): # return ObjectCtrlInfo object from dicObjectCtrl
        #si = self.studio_scene
        #dobj = si.dicObject
        dobjctrl = self.studio.dicObjectCtrl
        return dobjctrl[num]
    
    def get_objctrl_num_tochar(self,num): # return HSNeoOCIChar by num
        return HSNeoOCIChar(self.get_objctrl_num(num))

    def scene_get_all_females(self):
        from Studio import OCIChar
        from Studio import OCICharFemale
        from Studio import OCICharMale
        ar = []
        dobjctrl = self.studio.dicObjectCtrl
        for key in dobjctrl.Keys:
            objctrl = dobjctrl[key]
            if isinstance(objctrl, OCICharFemale):
                pctrl = HSNeoOCIChar(objctrl)
                ar.append(pctrl)
        return ar

    def scene_get_all_males(self):
        from Studio import OCIChar
        from Studio import OCICharFemale
        from Studio import OCICharMale
        ar = []
        dobjctrl = self.studio.dicObjectCtrl
        for key in dobjctrl.Keys:
            objctrl = dobjctrl[key]
            if isinstance(objctrl, OCICharMale):
                pctrl = HSNeoOCIChar(objctrl)
                ar.append(pctrl)
        return ar

    def scene_get_all_items_raw(self):
        from Studio import OCIItem
        ar = []
        dobjctrl = self.studio.dicObjectCtrl
        for key in dobjctrl.Keys:
            objctrl = dobjctrl[key]
            if isinstance(objctrl, OCIItem):
                pctrl = objctrl
                ar.append(pctrl)
        return ar

    def scene_get_all_items(self):
        from Studio import OCIItem
        ar = []
        dobjctrl = self.studio.dicObjectCtrl
        for key in dobjctrl.Keys:
            objctrl = dobjctrl[key]
            if isinstance(objctrl, OCIItem):
                pctrl = objctrl
                ar.append(HSNeoOCIItem(pctrl))
        return ar

    def scene_get_all_folders_raw(self):
        from Studio import OCIFolder
        ar = []
        dobjctrl = self.studio.dicObjectCtrl
        for key in dobjctrl.Keys:
            objctrl = dobjctrl[key]
            if isinstance(objctrl, OCIFolder):
                pctrl = objctrl
                ar.append(pctrl)
        return ar

    def scene_get_all_folders(self):
        from Studio import OCIFolder
        ar = []
        dobjctrl = self.studio.dicObjectCtrl
        for key in dobjctrl.Keys:
            objctrl = dobjctrl[key]
            if isinstance(objctrl, OCIFolder):
                pctrl = objctrl
                ar.append(HSNeoOCIFolder(pctrl))
        return ar


    def scene_set_bg_png(self,filepng):
        #uiBGChanger = self.studio.uiBGChanger
        #uiBGChanger.ChangeBackgroundMode(True)
        #uiBGChanger.SetBackgroundNo(5)
        #ffile = self.get_scene_dir() + "\\"+self.sceneDir+filepng
        ffile = "..\\Studio\\scene\\" + self.sceneDir + filepng
        print self.studio.m_BackgroundCtrl.Load(ffile)
        """
        print ffile
        import PngAssist
        #sprite = PngAssist.LoadSpriteFromFile(ffile);
        #uiBGChanger.bgImage.sprite = sprite;
        #print "2"
        #
        texture = PngAssist.LoadTexture(ffile)
        material = self.studio.m_BackgroundCtrl.meshRenderer.material;
        material.SetTexture("_MainTex", texture);
        self.studio.m_BackgroundCtrl.meshRenderer.material = material;
        self.studio.m_BackgroundCtrl.isVisible = True
        print "2"
        """

    def vnscenescript_run_current(self,onEnd,startState = 0):
        #print "Run current!"
        module = import_or_reload("vnscenescript")
        self.run_menu(module.start_menu,{'mode': 'view', 'startState': startState},onEnd)

    def vnscenescript_run_filescene(self,file,onEnd):
        self.runScAct = onEnd
        self.load_scene(file)
        self.set_text_s("...")
        self.set_buttons_alt([])
        self.set_timer(0.5,self._vnscenescript_run_filescene)

    def _vnscenescript_run_filescene(self, game):
        self.set_timer(0.5, self._vnscenescript_run_filescene2)

    def _vnscenescript_run_filescene2(self,game):
        self.vnscenescript_run_current(self.runScAct)

    def scene_get_bg_png_orig(self):
        return self.studio.sceneInfo.background

    def scene_set_bg_png_orig(self, filepng):
        if self.scene_get_bg_png_orig() != filepng:
            # return self.studio.sceneInfo.background
            from Studio import BackgroundCtrl
            from UnityEngine import GameObject
            # print self.studio.m_BackgroundCtrl.Load(ffile)
            # for obj in GameObject.FindObjectOfType(BackgroundCtrl):
            obj = GameObject.FindObjectOfType(BackgroundCtrl)
            return obj.Load(filepng)
            # print self.studio.m_BackgroundCtrl.Load(ffile)
        return True

    # -------- scene with framework ------------
    def scenef_register_actorsprops(self):
        print "-- Framework: register actors and props start --"
        game = self
        # search for tag folder (-actor:,-prop:,-dlgFolder-) and load them into game automaticlly
        # so this function must be called AFTER SCENE HAD BE LOADED!!

        game._scenef_actors = {}
        game._scenef_props = {}

        # get all from scene
        folders = game.scene_get_all_folders_raw()  # get list<OCIFolder> of folders in scene,

        # load actors and props from -actor:/-prop: tag folder attach on char/item
        for fld in folders:
            ftn = fld.name
            if ftn.startswith("-actor:"):
                # analysis actor tag
                tagElements = ftn[7:].strip().split(":")
                if len(tagElements) == 1:
                    actorAlias = tagElements[0]
                    # actorColor = "ffffff"
                    actorColor = None
                    actorTitle = None
                elif len(tagElements) == 2:
                    actorAlias = tagElements[0]
                    actorColor = tagElements[1]
                    actorTitle = None
                else:
                    actorAlias = tagElements[0]
                    actorColor = tagElements[1]
                    actorTitle = tagElements[2]
                # register actor
                try:
                    hsociChar = HSNeoOCI.create_from_treenode(fld.treeNodeObject.parent.parent.parent)
                    if isinstance(hsociChar, HSNeoOCIChar):
                        from vnactor import *
                        if actorTitle == None: actorTitle = hsociChar.text_name

                        #game._scenef_actors[actorAlias] = Actor(hsociChar.objctrl)
                        #adapted to multiple frameworks in 2.0
                        game._scenef_actors[actorAlias] = hsociChar.as_actor

                        if actorColor != None:
                            game.register_char(actorAlias, actorColor, actorTitle)
                        print "Registered actor: '" + to_roman(actorAlias) + "' as " + to_roman(actorTitle) + " (#" + str(actorColor) + ")"
                    else:
                        print "Error in register char tag (not correct child) <" + to_roman(ftn) + ">"
                except Exception as e:
                    print "error in register char tag <" + to_roman(ftn) + ">: " + str(e)
                    continue
            elif ftn.startswith("-prop:"):
                # analysis props tag
                propAlias = ftn[6:].strip()
                # register props
                hsobj = HSNeoOCI.create_from_treenode(fld.treeNodeObject.parent)
                game._scenef_props[propAlias] = hsobj
                print "Registered prop: '" + to_roman(propAlias) + "' as " + to_roman(hsobj.text_name)
            elif ftn.startswith("-propchild:"):
                # analysis props tag
                propAlias = ftn[11:].strip()
                # register props
                hsobj = HSNeoOCI.create_from_treenode(fld.treeNodeObject.child[0])
                game._scenef_props[propAlias] = hsobj
                print "Registered prop: '" + to_roman(propAlias) + "' as " + to_roman(hsobj.text_name)
            elif ftn.startswith("-propgrandpa:"):
                # analysis props tag
                propAlias = ftn[13:].strip()
                # register props
                hsobj = HSNeoOCI.create_from_treenode(fld.treeNodeObject.parent.parent)
                game._scenef_props[propAlias] = hsobj
                print "Registered prop: '" + to_roman(propAlias) + "' as " + to_roman(hsobj.text_name)

        print "-- Framework: register actors and props end --"

    def scenef_get_all_actors(self):
        return self._scenef_actors

    def scenef_get_all_props(self):
        return self._scenef_props

    def scenef_get_prop(self,id):
        if id in self.scenef_get_all_props():
            obj = self.scenef_get_all_props()[id]
            """ :type : HSNeoOCI"""
            return obj
        return None

    def scenef_get_propf(self,id):
        if id in self.scenef_get_all_props():
            from vnactor import *
            obj = self.scenef_get_all_props()[id]
            """ :type : HSNeoOCIProp"""

            return obj.as_prop
        return None

    def scenef_get_actor(self,id):
        if id in self.scenef_get_all_actors():
            obj = self.scenef_get_all_actors()[id]
            """ :type : vnactor.Actor"""
            return obj
        return None

    def scenef_reg_actor(self,id,actor):
        self._scenef_actors[id] = actor

    def scenef_reg_prop(self,id,prop):
        self._scenef_props[id] = prop

    def scenef_clean_actorsprops(self):
        self._scenef_actors = {}
        self._scenef_props = {}

    # ---- lip sync -------
    def set_text(self, char, text):
        VNController.set_text(self,char,text)
        if self.isfAutoLipSync:
            try:
                self._flipsync_text_handler(char,text)
            except Exception, e:
                print "Error in flipsync: "+str(e)

    def _flipsync_text_handler(self, char, text):
        import vngelipsync
        vngelipsync.flipsync_text_handler(self,char,text)

    def fake_lipsync_stop(self):
        import vngelipsync
        vngelipsync.fake_lipsync_stop(self)

    # --------- sync_h ---------
    def sync_h(self,female,male):
        factor = female.as_actor
        """ :type : vnactor.Actor"""
        mactor = male.as_actor
        """ :type : vnactor.Actor"""

        anime_option_param = (factor.height, factor.breast)

        # if factor.isHAnime:
        factor.set_anime_option_param(anime_option_param)
        # if mactor.isHAnime:
        mactor.set_anime_option_param(anime_option_param)

    # --------- save/load inside scene PNG -----------
    def dataPNG_save(self,id,strdata,strversion):
        if self.isSceneDataSaveSupported:
            #if not self.isStudioNEO:
                # classic ExtPlugins
                from extplugins import ExtensibleSaveFormat
                extsave = ExtensibleSaveFormat()
                extsave.loadExtendSaveData(id)
                #data = extsave.getExtendSaveData("main")
                extsave.setExtendSaveData("main",strdata)
                extsave.setExtendSaveData("version",strversion)

                extsave.saveExtendSaveData(id)
                return True


        return False

    def dataPNG_load(self,id): # return pair MainStrData, Version
        dummy = (None,None)

        try:
            if self.isSceneDataSaveSupported:
                from extplugins import ExtensibleSaveFormat
                extsave = ExtensibleSaveFormat()
                extsave.loadExtendSaveData(id)
                data = extsave.getExtendSaveData("main")
                version = extsave.getExtendSaveData("version")
                return (data,version)
        except:
            pass

        return dummy



def vngame_window_neo(vnButtonsStart, vnButtonsActionsStart):
    import unity_util

    unity_util.clean_behaviors()
    class NeoController(VNNeoController):
        def __init__(self):
            self.engine_name = "neo"
            self.pygamepath = "Plugins\\Console\\Lib"
            self._vnButtons = vnButtonsStart
            self._vnButtonsActions = vnButtonsActionsStart
            self.dataPNGarray = {}
            VNNeoController.__init__(self)
    
        # --- support functions ----
        def init_saveload_events(self):
            import extplugins
            extSave = extplugins.HSExtSave()
            if extSave.isDetected:
                extSave.reg_all_scene("vngeDefault", self._event_scene_loadedHS,self._event_scene_imported,self._event_scene_savedHS)
                self.isSceneEventsSupported = True
                self.isSceneDataSaveSupported = True
            else:
                self.errSceneEvents = "HSExtSave.dll not found"
            return

        def _event_scene_savedHS(self,p1,p2=""):
            import base64

            #from vnactor import bytearray_to_str64,str_to_bytearray
            #self.dataPNGarray = {"vngetest":("1","2")}
            self.dataPNGarray = {}

            xmlWriter = p2
            xmlWriter.WriteStartElement("defVNGE")

            self._event_scene_saved(p1,p2)
            #print self.dataPNGarray
            #print p1,p2
            # saving data in scene if necessary
            for key in self.dataPNGarray:
                print "xmlwrite...",self.dataPNGarray[key]
                xmlWriter.WriteStartElement("vngedata")
                xmlWriter.WriteAttributeString("key", key);
                xmlWriter.WriteAttributeString("version", self.dataPNGarray[key][1]);
                str64 = base64.b64encode(bytes(self.dataPNGarray[key][0], 'utf-8'))
                #str64 = bytearray_tostr64(str_to_bytearray(self.dataPNGarray[key][0]))
                #print str64
                xmlWriter.WriteString(str64)
                xmlWriter.WriteEndElement()

            xmlWriter.WriteEndElement()


        def _event_scene_loadedHS(self,p1,p2=""):
            import base64
            #print p1,p2
            self.dataPNGarray = {}
            try:
                if p2 != None:
                    for node in p2.FirstChild.ChildNodes:
                        if node.Name == "vngedata":
                            key = node.GetAttribute("key")
                            version = node.GetAttribute("version")
                            text = node.InnerText
                            self.dataPNGarray[key] = (base64.b64decode(text),version)
                        else:
                            print "VNGE Load from HSExtSave Unknown name:", node.Name
            except Exception, e:
                print "VNGE:_event_scene_loadedHS error", e

            #print "VNGE ExtSave XML data: ", self.dataPNGarray

            self._event_scene_loaded(p1,p2)

        def load_scene(self,file):
            self._load_scene_before(file)

            self.funcLockedText = "Loading scene..."
            self.isFuncLocked = True
            
            self.updFuncParam = file
            self.updFunc = self.load_scene2 # load scene on after one Update cycle
            
        def load_scene2(self,file):
            self.updFunc = self.load_scene_immediately # load scene on next Update cycle
        
        def load_scene_immediately(self,file):
            from Studio import Studio
            studio = Studio.Instance
            from os import path
            #return path.join(get_scene_dir(),file)
            studio.LoadScene(path.join(self.get_scene_dir(),self.sceneDir+file))
            
            self.isFuncLocked = False

        def get_scene_dir(self):
            from UnityEngine import Application
            from os import path
            return path.realpath(path.join(Application.dataPath,'..','UserData','studioneo','scene'))



        def scene_set_bg_png(self, filepng):
            ffile = "..\\studioneo\\scene\\" + self.sceneDir + filepng
            #print self.studio.m_BackgroundCtrl.Load(ffile)
            self.scene_set_bg_png_orig(ffile)

        # --------- save/load inside scene PNG -----------
        def dataPNG_save(self,id,strdata,strversion):
            if self.isSceneDataSaveSupported:
                # special case for StudioNEO
                self.dataPNGarray[id] = (strdata,strversion)

            return False

        def dataPNG_load(self,id): # return pair MainStrData, Version
            dummy = (None,None)

            try:
                if id in self.dataPNGarray:
                    return self.dataPNGarray[id]
            except:
                pass

            return dummy

        # def Update(self):
        #     VNNeoController.Update(self)
        #     print "Upd!"

        # def OnDestroy(self):
        #     print "OnDestroy NEO!"
        #     import coroutine
        #     coroutine.start_new_coroutine(vngame_window_autogames_uni, (), None)


    game = unity_util.create_gui_behavior(NeoController)
    return game



def vngame_window_phstudio(vnButtonsStart, vnButtonsActionsStart):
    import vngameenginephstudio
    game = vngameenginephstudio.vngame_window_phstudio(vnButtonsStart, vnButtonsActionsStart)
    return game

def vngame_window_charastudio(vnButtonsStart, vnButtonsActionsStart):
    import unity_util

    unity_util.clean_behaviors()
    class CharaStudioController(VNNeoController):
        def __init__(self):
            self.engine_name = "charastudio"
            self.pygamepath = self.calc_py_path() #"BepInEx\\Console\\Lib"
            self._vnButtons = vnButtonsStart
            self._vnButtonsActions = vnButtonsActionsStart
            VNNeoController.__init__(self)
            
        # --- support functions ----
        def init_saveload_events(self):
            import extplugins
            extSave = extplugins.ExtensibleSaveFormat()
            if extSave.isDetected:
                extSave.reg_scene_being_loaded(self._event_scene_loaded)
                extSave.reg_scene_being_imported(self._event_scene_imported)
                extSave.reg_scene_being_saved(self._event_scene_saved)
                self.isSceneEventsSupported = True
                self.isSceneDataSaveSupported = True
            else:
                self.errSceneEvents = "ExtensibleSaveFormat.dll not found"
            return



        def load_scene(self,file):
            self._load_scene_before(file)

            from Studio import Studio
            studio = Studio.Instance
            self.change_map_to(-1) # unload map before loading - due to stability issues
            #studio.InitScene(False) # or init scene to false
            self.updFuncParam = file
            self.updFunc = self.load_scene2 # load scene on next Update cycle
            
            self.funcLockedText = "Loading scene..."
            self.isFuncLocked = True
            
            #self.saveTChar = 
            
        def load_scene2(self,file):
            self.updFunc = self.load_scene3 # load scene on next Update cycle
            
        def load_scene3(self,file):
            self.updFunc = self.load_scene_immediately # load scene on next Update cycle
            
        def load_scene_immediately(self,file):
            from Studio import Studio
            studio = Studio.Instance
            from os import path
            #return path.join(get_scene_dir(),file)
            
            fpath = path.join(self.get_scene_dir(),self.sceneDir+file)
            studio.LoadScene(fpath) # not always loading map. Can't say, what to do. So we must unload map before LoadScene
            #self.change_map_to(-1)
            #self.change_map_to(studio.sceneInfo.map)
            
            #self.updFunc = self.testupdfunc
            
            # -------- this loading scene certainly work, but show scene unimmersive, step-by-step -----------
            #studio.StartCoroutine(studio.LoadSceneCoroutine(fpath))
            self.isFuncLocked = False
    
        def get_scene_dir(self):
            from UnityEngine import Application
            from os import path
            return path.realpath(path.join(Application.dataPath,'..','UserData','Studio','scene'))        
            
        def change_map_to(self,mapnum):
            from Studio import Studio
            studio = Studio.Instance
            studio.AddMap(mapnum,True,False,False)

        def scene_set_bg_png(self, filepng):
            """
            try:
                ffile = "..\\studio\\scene\\" + self.sceneDir + filepng
                print ffile
                from Studio import BackgroundCtrl
                from UnityEngine import GameObject
                #print self.studio.m_BackgroundCtrl.Load(ffile)
                #for obj in GameObject.FindObjectOfType(BackgroundCtrl):
                obj = GameObject.FindObjectOfType(BackgroundCtrl)
                print obj.Load(ffile)
            except Exception, e:
                print("Error: " + str(e))
            """
            ffile = "..\\studio\\scene\\" + self.sceneDir + filepng
            self.scene_set_bg_png_orig(ffile)

        def scene_get_framefile(self):
            return self.studio_scene.frame

        def scene_set_framefile(self,ffile):
            from Studio import FrameCtrl
            from UnityEngine import GameObject
            obj = GameObject.FindObjectOfType(FrameCtrl)
            return obj.Load(ffile)

    game = unity_util.create_gui_behavior(CharaStudioController)
    return game


def vngame_window_neov2(vnButtonsStart, vnButtonsActionsStart):
    import unity_util

    unity_util.clean_behaviors()

    class NeoV2Controller(VNNeoController):
        def __init__(self):
            self.engine_name = "neov2"
            self.pygamepath = self.calc_py_path() # "Bepinex\\plugins\\Console\\Lib"
            self._vnButtons = vnButtonsStart
            self._vnButtonsActions = vnButtonsActionsStart
            VNNeoController.__init__(self)

        # --- support functions ----
        def init_saveload_events(self):
            import extplugins
            extSave = extplugins.AI_ExtensibleSaveFormat()
            if extSave.isDetected:
                extSave.reg_scene_being_loaded(self._event_scene_loaded)
                extSave.reg_scene_being_imported(self._event_scene_imported)
                extSave.reg_scene_being_saved(self._event_scene_saved)
                self.isSceneEventsSupported = True
                self.isSceneDataSaveSupported = True
            else:
                self.errSceneEvents = "AI_ExtensibleSaveFormat.dll not found"
            return

        def load_scene(self, file):
            self._load_scene_before(file)

            self.change_map_to(-1) # unload map before loading - due to stability issues
            
            self.funcLockedText = "Loading scene..."
            self.isFuncLocked = True

            self.updFuncParam = file
            self.updFunc = self.load_scene2  # load scene on after one Update cycle

        def load_scene2(self, file):
            self.updFunc = self.load_scene_immediately  # load scene on next Update cycle

        def load_scene_immediately(self, file):
            from Studio import Studio
            studio = Studio.Instance
            from os import path
            # return path.join(get_scene_dir(),file)
            studio.LoadScene(path.join(self.get_scene_dir(), self.sceneDir + file))

            self.isFuncLocked = False

        def change_map_to(self,mapnum):
            from Studio import Studio
            studio = Studio.Instance
            studio.AddMap(mapnum,True,False,False)

        def get_scene_dir(self):
            from UnityEngine import Application
            from os import path
            return path.realpath(path.join(Application.dataPath, '..', 'UserData', 'Studio', 'scene'))

        def scene_set_bg_png(self, filepng):
            ffile = "..\\studio\\scene\\" + self.sceneDir + filepng
            # print self.studio.m_BackgroundCtrl.Load(ffile)
            self.scene_set_bg_png_orig(ffile)

        def scene_get_framefile(self):
            return self.studio_scene.frame

        def scene_set_framefile(self,ffile):
            from Studio import FrameCtrl
            from UnityEngine import GameObject
            obj = GameObject.FindObjectOfType(FrameCtrl)
            return obj.Load(ffile)



    game = unity_util.create_gui_behavior(NeoV2Controller)
    return game

# ---------------- --- dumping item tree -----------------

def dump_selected_item_tree():
    item = HSNeoOCI.create_from_selected()
    f = open("dump_selected_items.txt", 'w')
    _dump_item_tree(f,item,0)
    f.close()

def _dump_item_tree(f,item,level):
    txt1 = ""
    if isinstance(item,HSNeoOCIItem):
        addparams = "";
        try:
            tmp = (", 'anSp': {0}").format(item.objctrl.animeSpeed)
            addparams += tmp
        except Exception:
            pass
        txt1 = "{"+"'no': {0}, 'prs': ({1},{2},{3})".format(item.no,item.pos,item.rot,item.scale)
        txt1 += addparams
    if isinstance(item, HSNeoOCIFolder):
        value = item.name
        if not only_roman_chars(value):
            value = "nonlatinname"
        txt1 = "{" + "'no': 'fold', 'name': '{2}', 'pr': ({0},{1})".format(item.pos, item.rot, value)

    if item.treeNodeObject.childCount > 0:
        txt1 += ", 'ch': ["
        _print_dump(f,txt1,level)

        # print all child
        for childt in item.treeNodeObject.child:
            child = HSNeoOCI.create_from_treenode(childt)
            _dump_item_tree(f,child,level+1)

        _print_dump(f,"]},",level)
    else:
        _print_dump(f, txt1+"}", level)

def _print_dump(f,txt,level):
    #print(" "*level*4+txt)
    f.write(" "*level*4+txt+"\n")

def load_item_tree(obj,itemparenttobj):
    if isinstance(obj["no"],str):
        item = HSNeoOCIFolder.add(obj["name"])
        if itemparenttobj != None:
            item.set_parent_treenodeobject(itemparenttobj)
        item.set_pos(obj["pr"][0])
        item.set_rot(obj["pr"][1])
    else:
        item = HSNeoOCIItem.add_item(obj["no"])
        if itemparenttobj != None:
            item.set_parent_treenodeobject(itemparenttobj)
        item.set_pos(obj["prs"][0])
        item.set_rot(obj["prs"][1])
        item.set_scale(obj["prs"][2])
        if 'anSp' in obj:
            item.objctrl.animeSpeed = float(obj["anSp"])

    if 'ch' in obj:
        for objch in obj["ch"]:
            load_item_tree(objch,item.treeNodeObject)

    return item

def only_roman_chars(s):
    try:
        s.encode("ascii")
        return True
    except Exception, e:
        return False

def to_roman(s):
    # potentially convert all symbols to latin
    # but now only return s
    # this is used in console, so we don't always convert it to latin
    return s

def to_roman_file(s):
    # when we write to file, we want always be latin
    if only_roman_chars(s):
        return s
    return "nonlatin"

import random
rng=random.WichmannHill()
# to correct distribution
# see https://github.com/IronLanguages/ironpython2/issues/231 for details

def random_randint(a,b):
    # seems to be an error in IronPython random.randint, so we use our realization
    #import random
    res = rng.randint(a,b+1)
    if res > b:
        return rng.randint(a,b)
    return res

def random_choice(ar):
    try:
        item = random_randint(0,len(ar)-1)
        #print "random_choice: ",item
        res = ar[item]
        return res
    except Exception, e:
        print "Error in random_choice, %s " % str(e)
        pass
    return ar[0]

def CloneSkin(skin):
    newskin = GUISkin()
    props = newskin.GetType().GetProperties(BindingFlags.Public | BindingFlags.Instance| BindingFlags.SetProperty)
    for prop in [x.Name for x in props]:
        try:
            setattr(newskin, prop, getattr(skin, prop))
        except:
            pass
    return newskin

def console_show(visible):
    import ctypes
    # crt_win_hwid = ctypes.windll.user32.FindWindowA(0, 'Unity Console')
    crt_win_hwid = ctypes.windll.kernel32.GetConsoleWindow()
    #game.show_blocking_message_time(str(crt_win_hwid))
    if visible:
        ctypes.windll.user32.ShowWindow(crt_win_hwid, 1)
    else:
        ctypes.windll.user32.ShowWindow(crt_win_hwid, 0)

# -- studio_wait_for_load trick - for NEO and Old Studio--
def studio_wait_for_load():
    print "VNGE studio_wait_for_load..."
    parseIniFile()
    option = getEngineOptions()
    if "hideconsoleafterstart" in option:
        if option["hideconsoleafterstart"] == "1":
            console_show(False)
        if option["hideconsoleafterstart"] == "2":
            global bepInExLoggingConsole
            parseBepInExIniFile()
            #print "BepConOpt: ",bepInExLoggingConsole
            if bepInExLoggingConsole == "true":
                pass
            elif bepInExLoggingConsole == "false":
                console_show(False)
            else:
                print "VNGE can't detect BepInEx console settings"
                pass


    if get_engine_id() == "":
        print "VN Game Engine not for this EXE file"
        return
    from UnityEngine.SceneManagement import SceneManager
    #print "SceneManager: ",SceneManager.GetActiveScene().name
    from System.Threading import Thread

    # we wait for 300 seconds before scene will set to Studio - and run after that
    for i in range(0,300):
        Thread.Sleep(1000)


        #print "!!"
        #print "SceneManager: ", i, SceneManager.GetActiveScene().name
        if SceneManager.GetActiveScene().name.lower() == "studio":
            vngame_window_autogames_uni_1init()
            return

    print "Studio loads more than 300 seconds... seems to be an error."
    return
    #yield WaitForSeconds(8)
    #print "SceneManager3: ", i,  SceneManager.GetActiveScene().name
    #import coroutine
    #coroutine.start_new_coroutine(neo_preload2, (), None)

# -- studio_wait_for_load trick - for NEO and Old Studio--
# def studio_wait_for_load2():
#     if get_engine_id() == "":
#         print "VN Game Engine not for this EXE file"
#         return
#     from UnityEngine.SceneManagement import SceneManager
#     #print "SceneManager: ",SceneManager.GetActiveScene().name
#     from System.Threading import Thread
#
#     # we wait for 300 seconds before scene will set to Studio - and run after that
#     for i in range(0,300):
#         Thread.Sleep(1000)
#
#
#         #print "!!"
#         #print "SceneManager: ", i, SceneManager.GetActiveScene().name
#         if SceneManager.GetActiveScene().name.lower() == "studio":
#             vngame_window_autogames_uni_1init()
#             return
#
#     print "Studio loads more than 300 seconds... seems to be an error."
#     return
#     #yield WaitForSeconds(8)
#     #print "SceneManager3: ", i,  SceneManager.GetActiveScene().name
#     #import coroutine
#     #coroutine.start_new_coroutine(neo_preload2, (), None)

# -------- color text --------------

def color_text(text,color):
    return '<color=#{1}ff>{0}</color>'.format(text,color)

def color_text_green(text):
    return color_text(text,"aaffaa")

def color_text_red(text):
    return color_text(text,"ffaaaa")

def color_text_yellowlight(text):
    return color_text(text, "f8e473")

def color_text_gray(text):
    return color_text(text, "999999")

# routine for making toolbar button
def ActuallyRemoveAllListeners(evt):
    evt.RemoveAllListeners()
    i = 0
    while i <  evt.GetPersistentEventCount():
        evt.SetPersistentListenerState(i, 0)
        i += 1

def GetIconTex():
    import os.path
    from UnityEngine import GameObject, Object, RectTransform, Vector2, Color, Texture2D, Rect, Sprite
    from System.IO import File
    from UnityEngine import TextureFormat

    iconTex = Texture2D(2,2,TextureFormat.ARGB32,False)
    bytes = File.ReadAllBytes(os.path.splitext(__file__)[0] + '.png')
    #print bytes
    #iconTex.LoadImage(game.file_get_content_utf8("toolbar-icon.png"))
    #iconTex.LoadImage(bytes)
    try:
        from UnityEngine import ImageConversion
        ImageConversion.LoadImage(iconTex, bytes)
    except Exception, e:
        iconTex.LoadImage(bytes)

    return iconTex


def RawMakeToolbarButton(game):
    print "VNGE try make Raw toolbar button..."

    from UnityEngine import GameObject, Object, RectTransform, Vector2, Color, Texture2D, Rect, Sprite
    from UnityEngine.UI import Button

    # import extplugins
    # illapi = extplugins.ILLAPI()

    #from KKAPI.Utilities import Extensions

    existingRt = GameObject.Find("StudioScene/Canvas System Menu/01_Button/Button Center").GetComponent[RectTransform]();

    _searchToolbarButton = Object.Instantiate(existingRt.gameObject, existingRt.parent);
    copyRt = _searchToolbarButton.GetComponent[RectTransform]();
    copyRt.localScale = existingRt.localScale;
    copyRt.anchoredPosition = existingRt.anchoredPosition + Vector2(0, 160);

    #iconTex = Utils.LoadTexture(ResourceUtils.GetEmbeddedResource("toolbar-icon.png"));
    # iconTex = Texture2D(2,2,TextureFormat.ARGB32,False)
    # bytes = File.ReadAllBytes("BepInEx/plugins/Console/Lib/vnge-toolbar-icon.png");
    # #print bytes
    # #iconTex.LoadImage(game.file_get_content_utf8("toolbar-icon.png"))
    # #iconTex.LoadImage(bytes)
    # ImageConversion.LoadImage(iconTex, bytes)
    iconSprite = Sprite.Create(GetIconTex(), Rect(0, 0, 32, 32), Vector2(16, 16));

    copyBtn = copyRt.GetComponent[Button]();
    #copyBtn.onClick.RemoveAllListeners();
    #copyBtn.onClick.ActuallyRemoveAllListeners();
    #illapi.Utilities_Extensions().ActuallyRemoveAllListeners(copyBtn.onClick);
    ActuallyRemoveAllListeners(copyBtn.onClick)

    copyBtn.onClick.AddListener(game.toggle_window)
    #copyBtn.get_onClick().ActuallyRemoveAllListeners();
    # copyBtn.onClick.AddListener(() => Visible = !Visible);

    _toolbarIcon = copyBtn.image;
    _toolbarIcon.sprite = iconSprite;
    _toolbarIcon.color = Color.white;
    print "VNGE - Raw toolbar button done!"

def IllApiMakeToolbarButton(game):
    import extplugins
    illapi = extplugins.ILLAPI()

    from KKAPI.Studio.UI import CustomToolbarButtons
    # oldvisible = game.visible
    # game.visible = not game.visible
    CustomToolbarButtons.AddLeftToolbarToggle(GetIconTex(),game.visible,game.toggle_window_to)
    print "VNGE: Toolbar Button made by Ill API"