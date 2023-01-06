"""
vn game engine - specific for Studio
"""
import vngameengine
import UnityEngine
import GameCursor, CameraControl
from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Mathf, Time
import System  
from WindowsInput import InputSimulator
from WindowsInput import VirtualKeyCode 
import unity_util      
from vngameengine import VNController

class StudioController(VNController):
    def __init__(self):
        self.engine_name = "studio"
        self.pygamepath = "Plugins\\Console\\Lib"
        VNController.__init__(self)

    @property
    def studio(self):
        from Manager import Studio
        studio = Studio.Instance
        return studio

    def move_camera_direct(self, pos=None, distance=None, rotate=None, fov=23.0):
        studio = self.studio
        if pos:
            #if isinstance(pos, Vector3):
            studio.CameraCtrl.TargetPos = pos
        if distance:
            #if isinstance(distance, Vector3):
            studio.CameraCtrl.CameraDir = distance
        if rotate:
            #if isinstance(rotate, Vector3):
            studio.CameraCtrl.CameraAngle = rotate

    def dump_camera(self):
        import hs
        f = open('dumppython.txt', 'a+')
        import sys
        tmp = sys.stdout
        sys.stdout = f
        print("---DUMP! Camera Studio----")
        hs.HSCamera.dump()
        print("")
        sys.stdout = tmp
        f.close()
        self.show_blocking_message_time("Camera position dumped! (Studio)")

    def dump_scene(self):
        import hs
        f = open('dumppython.txt', 'a+')
        import sys
        tmp = sys.stdout
        sys.stdout = f
        print("---DUMP! Scene Studio----")
        hs.dump_scene()
        print("")
        sys.stdout = tmp
        f.close()
        self.show_blocking_message_time("Scene dumped! (Studio)")

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
        import hs
        hs.load_scene(self.sceneDir + file)

        self.isFuncLocked = False

    def get_scene_dir(self):
        from UnityEngine import Application
        from os import path
        return path.realpath(path.join(Application.dataPath, '..', 'UserData', 'Studio'))

    def to_camera(self, camnum):
        self.studio.studioUICamera.CameraLoadState(camnum - 1)

    def change_female_num_animation(self, num, clipName, assetbundle="", animation=""):
        import hs
        hsfem = hs.get_female_by_num(num)  # getting Female
        if assetbundle != "":
            hsfem.load_animation(assetbundle, animation)
        hsfem.play_animation_clip(clipName)

    def change_male_num_animation(self, num, clipName, assetbundle="", animation=""):
        import hs
        hsfem = hs.get_male_by_num(num)  # getting Male
        if assetbundle != "":
            hsfem.load_animation(assetbundle, animation)
        hsfem.play_animation_clip(clipName)

    def get_female_by_num(self, num):
        import hs
        hsfem = hs.get_female_by_num(num)  # getting Female
        return hsfem

    def get_male_by_num(self, num):
        import hs
        hsfem = hs.get_male_by_num(num)  # getting Male
        return hsfem

    def get_camera_num(self, camnum):
        if camnum == 0:
            c = self.studio.CameraCtrl
            return self.camparams2vec(c.TargetPos, c.CameraDir, c.CameraAngle, 23.0)
        else:
            c = self.studio.studioUICamera.cameraSaveStatuses[camnum - 1]
            return self.camparams2vec(c.pos, c.dir, c.ang, c.fov)

    def reset(self):
        self._unload_scene_before()
        import hs
        hs.reset()

    def scene_get_all_females(self):
        from Manager import Studio
        studio = Studio.Instance
        i = 0
        ar = []
        for c in studio.femaleList:
            ar.append(self.get_female_by_num(i))
            i += 1
        return ar

    def scene_get_all_males(self):
        from Manager import Studio
        studio = Studio.Instance
        i = 0
        ar = []
        for c in studio.maleList:
            ar.append(self.get_male_by_num(i))
            i += 1
        return ar

    def scene_set_bg_no(self,no):
        uiBGChanger = self.studio.uiBGChanger
        uiBGChanger.ChangeBackgroundMode(True)
        uiBGChanger.SetBackgroundNo(no)

    def scene_set_bg_png(self,filepng):
        uiBGChanger = self.studio.uiBGChanger
        uiBGChanger.ChangeBackgroundMode(True)
        #uiBGChanger.SetBackgroundNo(5)
        ffile = self.get_scene_dir() + "\\"+self.sceneDir+filepng
        #print ffile
        import PngAssist
        sprite = PngAssist.LoadSpriteFromFile(ffile);
        uiBGChanger.bgImage.sprite = sprite;
        #print "2"



def vngame_window_studio(vnButtonsStart, vnButtonsActionsStart):
    import unity_util

    unity_util.clean_behaviors()

    class StudioControllerEnd(StudioController):
        def __init__(self):
            self._vnButtons = vnButtonsStart
            self._vnButtonsActions = vnButtonsActionsStart
            StudioController.__init__(self)

    game = unity_util.create_gui_behavior(StudioControllerEnd)
    return game
