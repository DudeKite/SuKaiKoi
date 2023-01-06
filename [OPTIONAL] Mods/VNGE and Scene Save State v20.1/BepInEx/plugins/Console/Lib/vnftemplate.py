#-VNFA:GameTitle-#
# -*- coding: UTF-8 -*-
#-VNFA:BuildFromAutoScriptTemplate-#
# UTF-8 encode is supported now! ^o^

from vnactor import *
from vnframe import *
from vnanime import *

def start(game):
    # use importOrReload to keep vnactor and vnframe updated
    # it is useful if you want to modify vnactor or vnframe script
    from vngameengine import importOrReload
    importOrReload("vnactor")
    importOrReload("vnframe")
    importOrReload("vnanime")
    importOrReload("extplugins")
    
    # enable scene anime function provide by vnframe
    init_scene_anime(game)
    # enable key frame anime function provide by vnanime
    init_keyframe_anime(game)

    # select a skin
    game.skin_set_byname(#-VNFA:SkinVersion-#)

    # enable lip sync provide by vngameengine
    game.isfAutoLipSync = #-VNFA:FakeLipSyncEnable-# 
    game.fAutoLipSyncVer = #-VNFA:FakeLipSyncVersion-# 
    game.readingSpeed = #-VNFA:FakeLipSyncReadingSpeed-#
    
    # auto hide and lock style for your game, these are global settings
    game.isHideWindowDuringCameraAnimation = #-VNFA:HideWindow-#
    game.isLockWindowDuringSceneAnimation = #-VNFA:LockWindow-#
    
    # load scene PNG and then init scene after loaded
    enableQuickReload = #-VNFA:EnableQuickReload-#
    game.sceneDir = #-VNFA:SceneDir-#
    if enableQuickReload and hasattr(game, "scenePNG") and game.scenePNG == #-VNFA:ScenePNG-#:
        # skip load png, quick reload
        # all actor/prop status must be reset by script
        init_scene(game)
    else:
        load_and_init_scene(game, #-VNFA:ScenePNG-#, init_scene)
    
def init_scene(game):
    try:
        # show our game window
        game.visible = 1
        game.isHideGameButtons = 0
        
        # load actor/prop/string from scene by "tag folder", must be called after scene is loaded
        register_actor_prop_by_tag(game)
        register_string_resource(game)
        
        # import clips, after actor/prop registered
        for clip in keyframeClips:
            kfa_import(game, clip)

        # init script helper, must be called after actor/prop registered
        sh = init_script_helper(game)
        sh.createLocalizeStringOnBuild = #-VNFA:CreateString-#
        sh.masterMode = #-VNFA:MasterMode-#
        sh.baseNest = "        " # base nest space of dumpped script
        sh.nestWord = "    " # space inserted when script is nested
        sh.load_python() # load this python file for auto script
        sh.asEnable = True # enable auto script feature
        
        # setup default next button
        game.btnNextText = #-VNFA:DefaultNextText-#

        # here game start
        toSeq1(game)

    except Exception as e:
        import traceback
        traceback.print_exc()
        toEnd(game, "init_scene FAILED: "+str(e))

def toSeq1(game):
    game.texts_next([
        #-VNFA:seq:empty:1-#
    ], toEnd)
    
#-VNFA:sel:empty:1-#
    
def toEnd(game, text = None):
    if text == None:
        text = #-VNFA:DefaultEndText-#
    game.set_text_s(text)
    if #-VNFA:EnableReload-#:
        game.set_buttons([#-VNFA:DefaultRestartButton-#, #-VNFA:DefaultEndButton-#], [start, clearExit])
    else:
        clearExit(game)

def clearExit(game):
    clear_keyframe_anime(game)
    game.scenePNG = ""
    game.return_to_start_screen_clear()

# Keyframe clips build by clip manager
keyframeClips = [
#-VNFA:KeyFrameClips:start-#
#-VNFA:KeyFrameClips:end-#
]
