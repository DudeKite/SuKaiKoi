"""
VNGE CustomWindow skin
1.0

you must set
- funcSetup (optionally)
- funcWindowGUI (must!)
before call game.set_skin(skin) call
"""

from vngameengine import *

import UnityEngine
#import GameCursor, CameraControl
from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Mathf, Time
import System

def get_skin():
    return SkinCustomWindow()

class SkinCustomWindow(SkinBase):
    def __init__(self):
        SkinBase.__init__(self);
        self.name = "skin_customwindow"

        self.isCustomFuncWindowGUI = True

        self.funcSetup = None
        self.funcWindowGUI = None

    def setup(self,controller):
        self.controller = controller

        controller.call_game_func(self.funcSetup)

    def customWindowGUI(self, windowid):
        if self.funcWindowGUI:
            self.funcWindowGUI(self.controller, windowid)

