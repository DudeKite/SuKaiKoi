"""
vn game engine - specific for Playhome Studio
"""
import vngameengine
import UnityEngine
from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Mathf, Time
import System  
from WindowsInput import InputSimulator
from WindowsInput import VirtualKeyCode 
import unity_util      
from vngameengine import VNNeoController

def vngame_window_phstudio(vnButtonsStart, vnButtonsActionsStart):
    import unity_util

    unity_util.clean_behaviors()

    class PHStudioController(VNNeoController):
        def __init__(self):
            self.engine_name = "phstudio"
            self.pygamepath = self.calc_py_path()
            self._vnButtons = vnButtonsStart
            self._vnButtonsActions = vnButtonsActionsStart
            VNNeoController.__init__(self)

        # --- support functions ----
        def load_scene(self, file):
            self._load_scene_before(file)

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

        def get_scene_dir(self):
            from UnityEngine import Application
            from os import path
            return path.realpath(path.join(Application.dataPath, '..', 'UserData', 'studio', 'scene'))

        def scene_set_bg_png(self, filepng):
            ffile = "..\\studio\\scene\\" + self.sceneDir + filepng
            self.scene_set_bg_png_orig(ffile)

        # --- support functions ----
        def init_saveload_events(self):
            pass
            # ph studio ExtensibleSaveFormat doesn't support scene load/save events now

            # import extplugins
            # extSave = extplugins.ExtensibleSaveFormat()
            # if extSave.isDetected:
            #     extSave.reg_scene_being_loaded(self._event_scene_loaded)
            #     extSave.reg_scene_being_imported(self._event_scene_imported)
            #     extSave.reg_scene_being_saved(self._event_scene_saved)
            #     self.isSceneEventsSupported = True
            #     self.isSceneDataSaveSupported = True
            # else:
            #     self.errSceneEvents = "ExtensibleSaveFormat.dll not found"
            # return

    game = unity_util.create_gui_behavior(PHStudioController)
    return game