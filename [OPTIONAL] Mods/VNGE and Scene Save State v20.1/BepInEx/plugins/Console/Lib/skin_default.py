"""
VNGE default skin
1.1

Changelog:
1.1
- fix send game param (instead of skin) when CustomGUI option is using
"""

from vngameengine import *

import UnityEngine
#import GameCursor, CameraControl
from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Mathf, Time
import System

def get_skin():
    return SkinDefault()

class SkinDefault(SkinBase):
    def __init__(self):
        SkinBase.__init__(self);
        self.name = "skin_default"

        self.wwidth = 500
        self.wheight = 230

        self.labelFontSize = 16
        self.buttonFontSize = 16
        self.buttonHeight = 30

    def setup(self,controller):
        #super(SkinDefault, self).setup(controller)
        self.controller = controller

        controller.wwidth = self.wwidth
        controller.wheight = self.wheight

        controller.windowName = ''
        controller.windowRect = Rect(Screen.width / 2 - controller.wwidth / 2, Screen.height - controller.wheight - 10, controller.wwidth,
                                     controller.wheight)

        self.controller.windowStyle = self.controller.windowStyleDefault


    def render_main(self,text_author,text,btnsTexts,btnsActions,btnStyle):
        # --------- calculate actual author ------------
        char0 = text_author.split("//")[0]

        if char0 in self.controller.registeredChars:
            charinfo = self.controller.registeredChars[char0]
        else:
            charinfo = ("ffffff", char0)


        # --------- render ---------------
        fullw = self.wwidth - 30
        GUILayout.BeginVertical(GUILayout.Width(fullw))
        style = GUIStyle("label")
        style.richText = True
        style.fontSize = self.labelFontSize
        style.wordWrap = True

        customButton = GUIStyle("button")
        customButton.fontSize = self.buttonFontSize

        if (charinfo[1] != ""):
            GUILayout.Label("<color=#%sff><b>%s</b></color>" % (charinfo[0], charinfo[1]), style,
                            GUILayout.Width(fullw))

        if self.controller.engineOptions["usetranslator"] == "1" and self.controller.engineOptions["translatetexts"] == "1":
            GUILayout.Label(translateText(text), style, GUILayout.Width(fullw))
        else:
            GUILayout.Label(text, style, GUILayout.Width(fullw))

        GUILayout.FlexibleSpace()

        if isinstance(btnStyle, tuple):
            # tuple is specific action
            if btnStyle[0] == "function":
                try:
                    btnStyle[1](self.controller,
                                           {'fwidth': fullw, 'btnheight': self.buttonHeight, 'btnstyle': customButton,
                                            'labelstyle': style})
                except Exception, e:
                    print "Error in call custom GUI buttons: " + str(e)

        else:
            if not self.controller.isHideGameButtons:
                if btnStyle == "compact":
                    GUILayout.BeginHorizontal()

                for i in range(len(btnsTexts)):
                    restext = btnsTexts[i]
                    if self.controller.engineOptions["usetranslator"] == "1" and self.controller.engineOptions["translatebuttons"] == "1":
                        restext = translateText(restext)

                    fintext = restext
                    if self.controller.get_ini_option("usekeysforbuttons") == "1":
                        if len(self.controller.arKeyKodes) > i:
                            fintext = (self.controller.arKeyKodes[i]).upper() + ": " + fintext

                    if btnStyle == "normal":
                        if GUILayout.Button(fintext, customButton,
                                            GUILayout.Width(fullw), GUILayout.Height(self.buttonHeight)):
                            self.controller.call_game_func(btnsActions[i])

                    if btnStyle == "compact":
                        if GUILayout.Button(fintext, customButton,
                                            GUILayout.Width(fullw / 2 - 2), GUILayout.Height(self.buttonHeight)):
                            self.controller.call_game_func(btnsActions[i])
                        if (i % 2) == 1:
                            GUILayout.EndHorizontal()
                            GUILayout.BeginHorizontal()
                        # pass
                if btnStyle == "compact":
                    GUILayout.EndHorizontal()

        GUILayout.EndVertical()
        GUI.DragWindow()

    def render_system(self,sys_text):
        fullw = self.wwidth - 30
        GUILayout.BeginVertical(GUILayout.Width(fullw))
        style = GUIStyle("label")
        style.richText = True
        style.fontSize = self.labelFontSize
        style.wordWrap = True

        GUILayout.Label(sys_text, style, GUILayout.Width(fullw))

        GUILayout.EndVertical()
        GUI.DragWindow()

    def render_dev_console(self):
        # require implement only in SkinDefault
        fullw = self.wwidth - 30
        GUILayout.BeginVertical(GUILayout.Width(fullw))
        # guistyle1 = GUIStyle;
        # guistyle1.wordwrap = True;
        # GUILayout.Label("my test text bla-bla-bla ake a repeating button. The button returns true as long as the user holds down the mo", guistyle1, GUILayout.Width(260))
        style = GUIStyle("label")
        style.richText = True
        style.fontSize = self.labelFontSize
        style.wordWrap = True

        customButton = GUIStyle("button")
        customButton.fontSize = self.buttonFontSize

        #GUILayout.Label(sys_text, style, GUILayout.Width(fullw))
        GUILayout.Label("<color=#ffaaaaff><b>Developer console</b></color>", style, GUILayout.Width(fullw))
        GUILayout.FlexibleSpace()
        GUILayout.BeginHorizontal();
        if GUILayout.Button("Dump camera", customButton,
                            GUILayout.Width(fullw / 2 - 2), GUILayout.Height(self.buttonHeight)):
            self.controller.dump_camera()
        if GUILayout.Button("Dump scene", customButton,
                            GUILayout.Width(fullw / 2 - 2), GUILayout.Height(self.buttonHeight)):
            self.controller.dump_scene()
        GUILayout.EndHorizontal();
        GUILayout.BeginHorizontal();
        if GUILayout.Button("List chars > console ", customButton,
                            GUILayout.Width(fullw), GUILayout.Height(self.buttonHeight)):
            self.controller.debug_print_all_chars()
        GUILayout.EndHorizontal();
        if not self.controller.isClassicStudio:
            GUILayout.BeginHorizontal();
            if GUILayout.Button("Dump selected item/folder tree", customButton,
                                GUILayout.Width(fullw), GUILayout.Height(self.buttonHeight)):
                dump_selected_item_tree()
                self.controller.show_blocking_message_time("Tree dumped!")
            GUILayout.EndHorizontal();
            GUILayout.BeginHorizontal();
            if GUILayout.Button("VNFrame scene dump", customButton,
                                GUILayout.Width(fullw / 2 - 2), GUILayout.Height(self.buttonHeight)):
                self.controller.dump_scene_vnframe()
                # self.show_blocking_message_time("VNFrame scene dumped!")

            if GUILayout.Button("VNFActor select dump", customButton,
                                GUILayout.Width(fullw / 2 - 2), GUILayout.Height(self.buttonHeight)):
                self.controller.dump_selected_vnframe()

            GUILayout.EndHorizontal();

        GUILayout.EndVertical()
        GUI.DragWindow()