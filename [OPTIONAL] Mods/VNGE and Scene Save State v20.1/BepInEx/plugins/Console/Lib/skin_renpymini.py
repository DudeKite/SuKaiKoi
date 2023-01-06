"""
VNGE RenPy Mini like skin
1.0

1.0
- initial in VNGE 14.5
"""

from vngameengine import *

import UnityEngine
#import GameCursor, CameraControl
from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Mathf, Time
import System

def get_skin():
    return SkinRenPyMini()

class SkinRenPyMini(SkinBase):
    def __init__(self):
        SkinBase.__init__(self);
        self.name = "skin_renpymini"

        self.contentHeight = 0.15
        #self.wheight = Screen.height / 4
        self.contentWidthProp = 0.7

        self.calcWindowProp = Screen.width / 1920

        self.labelFontSize = 28
        self.buttonFontSize = 20
        self.buttonHeight = 36

        self.maxButtonsNormal = 3
        self.maxButtonsCompact = 6
        #boxstyle = GUIStyle("box");
        #boxstyle.
        self.isEndButton = False
        self.endButtonTxt = ">>"
        self.endButtonCall = None

    def setup(self,controller):
        #super(SkinDefault, self).setup(controller)


        self.controller = controller

        self.wwidth = Screen.width
        self.wheight = Screen.height * self.contentHeight

        controller.wwidth = self.wwidth
        controller.wheight = self.wheight

        controller.windowName = ''
        controller.windowRect = Rect(Screen.width / 2 - controller.wwidth / 2, Screen.height - controller.wheight, controller.wwidth,
                                     controller.wheight)

        #GUI.skin.panel.onActive.textColor
        style = GUIStyle("label")
        self.controller.windowStyle = style

        #style.
        #GUI.skin.window = style

        #GUI.backgroundColor.a = 0.7

    def ren_start(self):
        # this is an ugly way to draw gray alpha background
        GUI.Box(Rect(-10, 0, self.wwidth + 10, self.wheight + 5), "")
        GUI.Box(Rect(-10, 0, self.wwidth + 10, self.wheight + 5), "")
        GUI.Box(Rect(-10, 0, self.wwidth + 10, self.wheight + 5), "")

        GUILayout.BeginHorizontal(GUILayout.Width(self.wwidth))

        GUILayout.Space(self.wwidth * (1-self.contentWidthProp) / 2)

    def ren_end(self):
        if not self.isEndButton:
            GUILayout.Space(self.wwidth * (1-self.contentWidthProp) / 2)
        else:

            GUILayout.BeginVertical()
            #GUILayout.FlexibleSpace()
            GUILayout.Space(20)
            GUILayout.BeginHorizontal()
            GUILayout.FlexibleSpace()
            if GUILayout.Button(self.endButtonTxt):
                #print "AAAA!"
                self.controller.call_game_func(self.endButtonCall)
            GUILayout.Space(20)
            GUILayout.EndHorizontal()
            GUILayout.Space(20)
            GUILayout.EndVertical()

        GUILayout.EndHorizontal()
        #GUI.DragWindow()

    def render_main(self,text_author,text,btnsTexts,btnsActions,btnStyle):

        #stylebox = GUIStyle("box")
        #stylebox.border = 0
        #GUI.Box(Rect(0, 0, Screen.width / 7, Screen.height / 1), "");
        self.ren_start()

        # --------- calculate actual author ------------
        char0 = text_author.split("//")[0]

        if char0 in self.controller.registeredChars:
            charinfo = self.controller.registeredChars[char0]
        else:
            charinfo = ("ffffff", char0)


        # --------- render ---------------
        fullw = self.wwidth * self.contentWidthProp
        fullw0 = self.wwidth * (self.contentWidthProp - 0.2)
        fullw1 = self.wwidth * 0.2

        #GUILayout.BeginVertical("box1", GUILayout.Width(fullw), GUILayout.Height(self.wheight))
        #GUILayout.BeginVertical("box1", GUILayout.Width(fullw), GUILayout.Height(self.wheight))
        if isinstance(btnStyle, tuple): # custom gui buttons - to fullw
            GUILayout.BeginVertical(GUILayout.Width(fullw), GUILayout.Height(self.wheight))
        else:
            GUILayout.BeginVertical(GUILayout.Width(fullw0), GUILayout.Height(self.wheight))

        GUILayout.Space(10)

        # ---- preparing styles ----------
        style = GUIStyle("label")
        style.richText = True
        style.fontSize = self.labelFontSize
        style.wordWrap = True

        customButton = GUIStyle("button")
        customButton.fontSize = self.buttonFontSize

        # ----------- render ---------
        if isinstance(btnStyle, tuple):
            # -------- custom render -----------
            # tuple is specific action
            if btnStyle[0] == "function":
                try:

                    btnStyle[1](self.controller,
                                           {'fwidth': fullw, 'btnheight': self.buttonHeight, 'btnstyle': customButton,
                                            'labelstyle': style})
                except Exception, e:
                    print "Error in call custom GUI buttons: " + str(e)

        else:
            # --------- normal render ----------

            #GUILayout.BeginHorizontal()

            if (charinfo[1] != ""):
                GUILayout.Label("<color=#%sff><b>%s</b></color>" % (charinfo[0], charinfo[1]), style,
                                GUILayout.Width(fullw0))
                GUILayout.Space(0)

            # -- special processing for translation --
            if self.controller.engineOptions["usetranslator"] == "1" and self.controller.engineOptions["translatetexts"] == "1":
                GUILayout.Label(translateText(text), style, GUILayout.Width(fullw0))
            else:
                GUILayout.Label(text, style, GUILayout.Width(fullw0))

            #GUILayout.FlexibleSpace()
            GUILayout.EndVertical()

            GUILayout.BeginVertical(GUILayout.Width(fullw1), GUILayout.Height(self.wheight))
            GUILayout.FlexibleSpace()
            # ---- show buttons ---
            if not self.controller.isHideGameButtons:


                if btnStyle == "compact":
                    GUILayout.BeginHorizontal()

                isOneButton = False

                for i in range(len(btnsTexts)):
                    # preparing button texts
                    restext = btnsTexts[i]
                    if self.controller.engineOptions["usetranslator"] == "1" and self.controller.engineOptions["translatebuttons"] == "1":
                        restext = translateText(restext)

                    fintext = restext
                    if self.controller.get_ini_option("usekeysforbuttons") == "1":
                        if len(self.controller.arKeyKodes) > i:
                            fintext = (self.controller.arKeyKodes[i]).upper() + ": " + fintext

                    # render button
                    if btnStyle == "normal":
                        if len(btnsTexts) > 1:
                            if GUILayout.Button(fintext, customButton,
                                                GUILayout.Width(fullw1), GUILayout.Height(self.buttonHeight)):
                                self.controller.call_game_func(btnsActions[i])
                        else:
                            # special case for 1 button
                            isOneButton = True
                            GUILayout.BeginHorizontal()
                            GUILayout.FlexibleSpace()

                            customButton.fontSize *= 1.2
                            if GUILayout.Button(fintext, customButton,
                                                GUILayout.Width(fullw1), GUILayout.Height(self.buttonHeight*1.4)):
                                self.controller.call_game_func(btnsActions[i])


                            GUILayout.EndHorizontal()

                    if btnStyle == "compact":
                        if GUILayout.Button(fintext, customButton,
                                            GUILayout.Width(fullw1 / 2 - 2), GUILayout.Height(self.buttonHeight)):
                            self.controller.call_game_func(btnsActions[i])
                        if (i % 2) == 1:
                            GUILayout.EndHorizontal()
                            GUILayout.BeginHorizontal()
                        # pass
                if btnStyle == "compact":
                    GUILayout.EndHorizontal()

        GUILayout.Space(16)
        GUILayout.EndVertical()



        self.ren_end()

    def render_system(self,sys_text):
        self.ren_start()

        fullw = self.wwidth * self.contentWidthProp

        GUILayout.BeginVertical(GUILayout.Width(fullw))
        style = GUIStyle("label")
        style.richText = True
        style.fontSize = self.labelFontSize
        style.wordWrap = True

        GUILayout.Label(sys_text, style, GUILayout.Width(fullw))
        GUILayout.EndVertical()

        self.ren_end()

