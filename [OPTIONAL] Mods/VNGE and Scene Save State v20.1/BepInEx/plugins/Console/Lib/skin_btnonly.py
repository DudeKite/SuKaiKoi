
"""
VNSS button only skin
NO TEXT MESSAGE WINDOW, BUTTONS ONLY!
V1.0

Default button show at left-bottom conner on screen.
Custom buttons show at mid of screen.

Some usable setting:
buttonSetDir: "h" to arrange button in horizontal, "v" to arrange in vertical
maxButtonsInSet: if button number is bigger than this setting, they will be arranged in matrix

LOG:
v1.0
    - initial in VNGE 16.0
"""

from vngameengine import *

import UnityEngine
#import GameCursor, CameraControl
from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Mathf, Time
from System import String, Array

def get_skin():
    return SkinButtonOnly()

class SkinButtonOnly(SkinBase):
    def __init__(self):
        SkinBase.__init__(self)
        self.name = "skin_btnonly"

        self.contentHeight = 0.33
        self.contentWidthProp = 0.7

        self.minDefBtnWidth = 150
        self.minBtnWidth = 200
        self.maxBtnWidth = 400

        self.labelFontSize = 28
        self.buttonFontSize = 20
        self.buttonHeight = 36

        self.buttonSetDir = "h"
        self.maxButtonsInSet = 5

        # end button
        self.isEndButton = False
        self.endButtonTxt = "QUIT"
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


    def render_main(self,text_author,text,btnsTexts,btnsActions,btnStyle):

        def prepareButtonText(idx):
            restext = btnsTexts[idx]
            # translate
            if self.controller.engineOptions["usetranslator"] == "1" and self.controller.engineOptions["translatebuttons"] == "1":
                restext = translateText(restext)
            # add shortcut
            fintext = restext
            if self.controller.get_ini_option("usekeysforbuttons") == "1":
                if len(self.controller.arKeyKodes) > idx:
                    fintext = (self.controller.arKeyKodes[idx]).upper() + ": " + fintext
            # done
            return fintext

        # --------- render ---------------
        fullw = self.wwidth * self.contentWidthProp
        margin = self.wwidth * (1 - self.contentWidthProp) / 2

        # ---- preparing styles ----------
        customButton = GUIStyle("button")
        customButton.fontSize = self.buttonFontSize

        # ----------- render ---------
        if isinstance(btnStyle, tuple):
            # -------- custom render -----------
            # tuple is specific action
            GUILayout.BeginHorizontal()
            GUILayout.FlexibleSpace()
            GUILayout.Label("Custom render is not supported in this skin!!")
            GUILayout.FlexibleSpace()
            GUILayout.EndVertical()

        else:
            # --------- normal render ----------
    
            # ---- show buttons ---
            if not self.controller.isHideGameButtons:
                #print btnsTexts[0], self.controller.btnNextText

                if len(btnsTexts) == 1 and btnStyle == "normal":
                    # normal single button => the default one
                    GUILayout.BeginVertical()
                    GUILayout.FlexibleSpace()

                    # end button
                    if self.isEndButton: 
                        GUILayout.BeginHorizontal()
                        GUILayout.FlexibleSpace()
                        if GUILayout.Button(self.endButtonTxt):
                            self.controller.call_game_func(self.endButtonCall)
                        GUILayout.Space(20)
                        GUILayout.EndHorizontal()

                    # render button
                    GUILayout.BeginHorizontal()
                    GUILayout.FlexibleSpace()
                    if GUILayout.Button(prepareButtonText(0), customButton, GUILayout.MinWidth(self.minDefBtnWidth), GUILayout.Height(self.buttonHeight)):
                        self.controller.call_game_func(btnsActions[0])
                    GUILayout.Space(20)
                    GUILayout.EndHorizontal()

                    GUILayout.Space(20)
                    GUILayout.EndVertical()

                elif len(btnsTexts) > self.maxButtonsInSet:
                    # button matrix
                    row = len(btnsTexts) / self.maxButtonsInSet
                    if (len(btnsTexts) % self.maxButtonsInSet) > 0:
                        row += 1
                    col = self.maxButtonsInSet

                    arrangedTexts = [prepareButtonText(i) for i in range(len(btnsTexts))]

                    gridMaxWidth = self.maxBtnWidth * col + 5 * (col - 1)
                    gridMinWidth = self.minBtnWidth * col + 5 * (col - 1)
                    gridHeight = self.buttonHeight * row + 5 * (row - 1)
                        
                    if not hasattr(self, "tempGridSel"):
                        self.tempGridSel = -1
                    
                    GUILayout.BeginHorizontal()
                    GUILayout.Space(margin)
                    GUILayout.FlexibleSpace()
                    sel = GUILayout.SelectionGrid(self.tempGridSel, Array[String](arrangedTexts), self.maxButtonsInSet, customButton, GUILayout.MinWidth(gridMinWidth), GUILayout.MaxWidth(gridMaxWidth), GUILayout.Height(gridHeight))
                    if sel != self.tempGridSel:
                        del self.tempGridSel
                        self.controller.call_game_func(btnsActions[sel])
                    GUILayout.FlexibleSpace()
                    GUILayout.Space(margin)
                    GUILayout.EndHorizontal()
                    
                    GUILayout.FlexibleSpace()
                    
                    # end button
                    if self.isEndButton: 
                        GUILayout.BeginHorizontal()
                        GUILayout.FlexibleSpace()
                        if GUILayout.Button(self.endButtonTxt):
                            self.controller.call_game_func(self.endButtonCall)
                        GUILayout.Space(20)
                        GUILayout.EndHorizontal()
                        GUILayout.Space(20)
                    
                elif self.buttonSetDir == "v":
                    # button in column
                    for i in range(len(btnsTexts)):
                        # render button
                        GUILayout.BeginHorizontal()
                        GUILayout.Space(margin)
                        GUILayout.FlexibleSpace()
                        if GUILayout.Button(prepareButtonText(i), customButton, GUILayout.MinWidth(self.minBtnWidth), GUILayout.MaxWidth(self.maxBtnWidth), GUILayout.Height(self.buttonHeight)):
                            self.controller.call_game_func(btnsActions[i])
                        GUILayout.FlexibleSpace()
                        GUILayout.Space(margin)
                        GUILayout.EndHorizontal()

                    GUILayout.FlexibleSpace()

                    # end button
                    if self.isEndButton: 
                        GUILayout.BeginHorizontal()
                        GUILayout.FlexibleSpace()
                        if GUILayout.Button(self.endButtonTxt):
                            self.controller.call_game_func(self.endButtonCall)
                        GUILayout.Space(20)
                        GUILayout.EndHorizontal()
                        GUILayout.Space(20)

                elif self.buttonSetDir == "h":
                    # button in row
                    GUILayout.BeginHorizontal()
                    GUILayout.Space(margin)
                    GUILayout.FlexibleSpace()
                    for i in range(len(btnsTexts)):
                        # render button
                        if GUILayout.Button(prepareButtonText(i), customButton, GUILayout.MinWidth(self.minBtnWidth), GUILayout.MaxWidth(self.maxBtnWidth), GUILayout.Height(self.buttonHeight)):
                            self.controller.call_game_func(btnsActions[i])
                    GUILayout.FlexibleSpace()
                    GUILayout.Space(margin)
                    GUILayout.EndHorizontal()

                    GUILayout.FlexibleSpace()

                    # end button
                    if self.isEndButton: 
                        GUILayout.BeginHorizontal()
                        GUILayout.FlexibleSpace()
                        if GUILayout.Button(self.endButtonTxt):
                            self.controller.call_game_func(self.endButtonCall)
                        GUILayout.Space(20)
                        GUILayout.EndHorizontal()
                        GUILayout.Space(20)

        #GUI.DragWindow()



    def render_system(self,sys_text):
        fullw = self.wwidth * self.contentWidthProp

        GUILayout.BeginVertical(GUILayout.Width(fullw))
        style = GUIStyle("label")
        style.richText = True
        style.fontSize = self.labelFontSize
        style.wordWrap = True

        GUILayout.Label(sys_text, style, GUILayout.Width(fullw))
        GUILayout.EndVertical()



