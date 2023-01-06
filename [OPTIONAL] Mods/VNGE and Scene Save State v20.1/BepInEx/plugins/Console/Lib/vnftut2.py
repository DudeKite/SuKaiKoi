#vngame;charastudio;Demos/VNFrame Tutorial 2
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
    game.skin_set_byname("skin_default")

    # enable lip sync provide by vngameengine
    game.isfAutoLipSync = True 
    game.fAutoLipSyncVer = "v11" 
    game.readingSpeed = 12.0
    
    # auto hide and lock style for your game, these are global settings
    game.isHideWindowDuringCameraAnimation = False
    game.isLockWindowDuringSceneAnimation = False
    
    # load scene PNG and then init scene after loaded
    enableQuickReload = False
    game.sceneDir = "wcf\\"
    if enableQuickReload and hasattr(game, "scenePNG") and game.scenePNG == "vnftut.png":
        # skip load png, quick reload
        # all actor/prop status must be reset by script
        init_scene(game)
    else:
        load_and_init_scene(game, "vnftut.png", init_scene)
    
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
        sh.createLocalizeStringOnBuild = False
        sh.masterMode = False
        sh.baseNest = "        " # base nest space of dumpped script
        sh.nestWord = "    " # space inserted when script is nested
        sh.load_python() # load this python file for auto script
        sh.asEnable = True # enable auto script feature
        
        # setup default next button
        game.btnNextText = "Next >>"

        # here game start
        toSeq1(game)

    except Exception as e:
        import traceback
        traceback.print_exc()
        toEnd(game, "init_scene FAILED: "+str(e))

def toSeq1(game):
    game.texts_next([
        #-VNFA:seq:start:1-#
        ["main", "Hi, everyone! Nice to see you again. This time I will introduce the new features in VNFrame3.0. Mainly, the key frame based anime clip!", act, {
            'cam': {'goto_pos': ((0.987, 1.406, 0.135), (0.000, 0.000, -0.880), (-0.800, 193.000, 0.000))},
            'main': {'acc_all': 1, 'anim': (0, 1, 11), 'anim_lp': 0, 'anim_ptn': 0.000, 'anim_spd': 1.000, 'cloth_all': (0, 0, 0, 0, 3, 0, 0, 0), 'cloth_type': 4, 'eyebrow': 0, 'eyes': 0, 'eyes_blink': 1, 'eyes_open': 1.000, 'face_red': 0.000, 'face_to': 3, 'fk_active': (0, 1, 0, 1, 0, 0, 0), 'fk_set': {}, 'hands': (0, 0), 'ik_active': (1, 1, 1, 1, 1), 'ik_set': {}, 'juice': (0, 0, 0, 0, 0), 'kinematic': 0, 'lip_sync': 1, 'look_at_pos': (0.000, 0.000, 0.250), 'look_at_ptn': 1, 'mouth': 0, 'mouth_open': 0.000, 'move_to': (0.903, 0.000, 0.100), 'nip_stand': 0.000, 'rotate_to': (0.000, 355.000, 0.000), 'scale_to': (1.000, 1.000, 1.000), 'son': (0, 1.000), 'tear': 0, 'visible': 1, 'voice_lst': (), 'voice_rpt': 0},
            'led': {'move_to': (0.000, 0.050, 0.000), 'rotate_to': (0.000, 0.000, 0.000), 'scale_to': (0.442, 0.442, 0.442), 'visible': 0},
            'boxmove': {'frame': 0, 'loop': -1, 'play': 0, 'speed': 1.000},
            'boxspin': {'frame': 0, 'loop': -1, 'play': 0, 'speed': 1.000},
            'box': {'move_to': (0.000, 1.000, 0.000), 'rotate_to': (0.000, 0.000, 0.000), 'visible': 1},
        }],
        ["main", "Still, let's use the magic box to do the demo!", act, {
            'cam': {'goto_pos': ((0.411, 1.203, 0.077), (0.000, 0.000, -3.107), (0.750, 179.600, 0.000))},
            'main': {'anim': (0, 2, 6), 'hands': (3, 0)},
        }],
        ["main", "Now, you should see the box starts to move around. It is controlled by a clip. This is a very simple clip, controls only the position property (or 'move_to') of the box.", act, {
            'cam': {'goto_pos': ((0.535, 1.246, 0.210), (0.000, 0.000, -2.658), (-0.250, 187.650, 0.000))},
            'boxmove': {'play': 1},
            'main': {'anim': (0, 1, 24), 'hands': (0, 0)},
        }],
        ["main", "A clip is a set of keyframes. Clip creates a short animation which can be controlled by script. Oh, clip can be long of course, as long as you wish."],
        ["main", "Let try another one. Now the box stop moving and start to spin.", act, {
            'boxmove': {'play': 2},
            'boxspin': {'play': 1},
        }],
        ["main", "It is another simple clip, which controls the box's rotation property (or 'rotate_to'). Both of the two clips I showed you control the box, but they contents keyframes for different properties, so they will not conflict, means they can play at the same time..."],
        ["main", "Like this.", act, {
            'boxmove': {'play': 1},
        }],
        ["main", "Let's use this trick on an actor, myself.", act, {
            'cam': {'goto_pos': ((0.718, 0.320, 0.145), (0.000, 0.000, -2.012), (-1.100, 164.550, 0.000))},
            #'main': {'acc_all': 1, 'anim': (4, 144, 0), 'anim_lp': 0, 'anim_ptn': 0.000, 'anim_spd': 1.000, 'cloth_all': (0, 0, 0, 0, 3, 0, 0, 0), 'eyebrow': 0, 'eyes': 0, 'eyes_blink': 1, 'eyes_open': 1.000, 'face_red': 0.000, 'face_to': 4, 'fk_active': (0, 1, 0, 0, 0, 0, 0), 'fk_set': {1: (-22.625, -34.426, 10.793), 2: (-27.644, 0.000, 0.000)}, 'hands': (3, 7), 'ik_active': (1, 1, 1, 1, 1), 'ik_set': {'cf_j_arm00_L': ((0.076, 0.383, -0.264), ), 'cf_j_arm00_R': ((-0.116, 0.397, -0.238), ), 'cf_j_forearm01_L': ((0.148, 0.137, -0.111), ), 'cf_j_forearm01_R': ((-0.163, 0.129, -0.151), ), 'cf_j_hand_L': ((0.121, 0.051, -0.281), (358.079, 232.257, 24.669)), 'cf_j_hand_R': ((-0.157, 0.016, -0.325), (359.721, 98.042, 7.702)), 'cf_j_hips': ((0.000, 0.337, -0.004), ), 'cf_j_leg01_L': ((0.196, 0.000, -0.035), ), 'cf_j_leg01_R': ((-0.158, 0.000, -0.034), ), 'cf_j_leg03_L': ((0.109, 0.032, 0.307), (55.329, 335.653, 168.008)), 'cf_j_leg03_R': ((-0.075, 0.032, 0.307), (52.393, 18.542, 162.269)), 'cf_j_thigh00_L': ((0.076, 0.336, 0.139), ), 'cf_j_thigh00_R': ((-0.076, 0.342, 0.139), )}, 'juice': (0, 0, 0, 0, 0), 'kinematic': 3, 'lip_sync': 1, 'look_at_pos': (0.000, 0.000, 0.250), 'look_at_ptn': 1, 'mouth': 0, 'mouth_open': 0.000, 'move_to': (0.920, 0.000, 0.000), 'nip_stand': 0.000, 'rotate_to': (0.000, 175.572, 0.000), 'scale_to': (1.000, 1.000, 1.000), 'son': (0, 1.000), 'tear': 0, 'visible': 1, 'voice_lst': (), 'voice_rpt': 0},
            'main': {'acc_all': 1, 'anim': (4, 144, 0), 'face_to': 4, 'fk_active': (0, 1, 0, 0, 1, 1, 0), 'fk_set': {1: (-22.625, -34.426, 10.793), 2: (-27.644, 0.000, 0.000), 22: (-75.715, 9.174, -44.696), 23: (0.000, 0.000, 9.353), 24: (0.000, 0.000, -5.997), 25: (-5.048, 160.353, -160.723), 26: (0.000, -0.002, 14.281), 27: (0.000, -0.001, 11.518), 28: (6.567, -178.934, -159.730), 29: (0.000, 0.000, 11.517), 30: (0.000, 0.000, 16.161), 31: (18.109, -162.864, -160.030), 32: (0.000, 0.000, 10.855), 33: (0.000, 0.000, 10.898), 34: (17.862, -150.091, -163.390), 35: (0.000, -0.001, 13.631), 36: (0.000, 0.002, 12.142), 37: (73.544, 104.780, 76.601), 38: (0.000, 0.000, -9.222), 39: (0.000, 0.000, -9.222), 40: (14.148, 17.048, 7.536), 41: (0.000, 0.002, -3.295), 42: (0.000, 0.001, -1.909), 43: (-6.948, 0.674, 1.239), 44: (0.000, 0.000, -1.761), 45: (0.000, 0.000, -5.705), 46: (-6.654, -15.495, 4.670), 47: (0.000, 0.000, -5.491), 48: (0.000, 0.000, -4.488), 49: (-12.391, -29.294, 8.953), 50: (0.000, 0.000, -3.863), 51: (0.000, 0.000, -2.383)}, 'hands': (3, 7), 'ik_set': {'cf_j_arm00_L': ((0.076, 0.383, -0.264), ), 'cf_j_arm00_R': ((-0.116, 0.397, -0.238), ), 'cf_j_forearm01_L': ((0.148, 0.137, -0.111), ), 'cf_j_forearm01_R': ((-0.163, 0.129, -0.151), ), 'cf_j_hand_L': ((0.121, 0.051, -0.281), (358.079, 232.257, 24.669)), 'cf_j_hand_R': ((-0.157, 0.016, -0.325), (359.721, 98.042, 7.702)), 'cf_j_hips': ((0.000, 0.337, -0.004), ), 'cf_j_leg01_L': ((0.196, 0.000, -0.035), ), 'cf_j_leg01_R': ((-0.158, 0.000, -0.034), ), 'cf_j_leg03_L': ((0.109, 0.032, 0.307), (55.329, 335.653, 168.008)), 'cf_j_leg03_R': ((-0.075, 0.032, 0.307), (52.393, 18.542, 162.269)), 'cf_j_thigh00_L': ((0.076, 0.336, 0.139), ), 'cf_j_thigh00_R': ((-0.076, 0.342, 0.139), )}, 'kinematic': 3, 'move_to': (0.920, 0.000, 0.000), 'rotate_to': (0.000, 175.572, 0.000)},
        }],
        ["main", "I started two clips, which controls the different IK joint of my body, so they can be played at same time and controlled separately. Let's try it!", act, {
            'dogs1': {'frame': 0, 'loop': -1, 'play': 1, 'speed': 1},
            'dogs2': {'frame': 0, 'loop': -1, 'play': 1, 'speed': 1},
        }],
        #-VNFA:seq:end:1-#
    ], toSel1)
    
def toSel1(game):
    kfa_play(game, "dogf")
    game.set_buttons_alt([],("function", toSel1_GUI))
    
def toSel1_GUI(game, info):
    from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
    from vngameengine import VNController
    if not isinstance(game, VNController):
        # maybe a skin since vngame 9.0
        game = game.controller
    fullw = info["fwidth"]
    btnheight = info["btnheight"]
    btnstyle = info["btnstyle"]
    labelstyle = info["labelstyle"]
    
    # UI
    GUILayout.BeginHorizontal()
    dgss1 = game.gdata.kfaManagedClips["dogs1"].speed
    GUILayout.Label("Should speed: %.1f"%dgss1, GUILayout.Width(150))
    if GUILayout.Button("Shake quicker!", GUILayout.Width((fullw-150)/2-4)) and dgss1 < 2:
        game.gdata.kfaManagedClips["dogs1"].speed = dgss1 + 0.3
    if GUILayout.Button("Shake slower!", GUILayout.Width((fullw-150)/2-4)) and dgss1 > 0.4:
        game.gdata.kfaManagedClips["dogs1"].speed = dgss1 - 0.3
    GUILayout.EndHorizontal()

    GUILayout.BeginHorizontal()
    dgss2 = game.gdata.kfaManagedClips["dogs2"].speed
    GUILayout.Label("Hip speed: %.1f"%dgss2, GUILayout.Width(150))
    if GUILayout.Button("Wriggle quicker!", GUILayout.Width((fullw-150)/2-4)) and dgss2 < 2:
        game.gdata.kfaManagedClips["dogs2"].speed = dgss2 + 0.3
    if GUILayout.Button("Wriggle slower!", GUILayout.Width((fullw-150)/2-4)) and dgss2 > 0.4:
        game.gdata.kfaManagedClips["dogs2"].speed = dgss2 - 0.3
    GUILayout.EndHorizontal()
    
    GUILayout.BeginHorizontal()
    if GUILayout.Button("Enough, let's go on.", GUILayout.Width(fullw)):
        kfa_stop(game, "dogs1")
        kfa_stop(game, "dogs2")
        kfa_stop(game, "dogf")
        toSeq2(game)
    GUILayout.EndHorizontal()

def toSeq2(game):
    game.texts_next([
        #-VNFA:seq:start:2-#
        ["main", "All these clips we played are simple. They control only one property of one actor/prop. A clip can be complicated too! You can set all the properties of all actor/prop in one clip if you want.", act, {
            'main': {'anim': (0, 1, 0), 'anim_spd': 1.000, 'hands': (0, 0), 'kinematic': 0, 'rotate_to': (0.000, 355.000, 0.000)},
            'cam': {'goto_pos': ((0.600, 1.018, 0.090), (0.000, 0.000, -3.635), (9.650, 181.100, 0.000))},
            'boxmove': {'frame': 0, 'loop': -1, 'play': 0, 'speed': 1},
            'boxspin': {'frame': 0, 'loop': -1, 'play': 0, 'speed': 1},
        }],
        ["main", "Like this clip. It controls actor fk and camera in one clip.", act, {
            'wave': {'loop': -1, 'play': 1, 'speed': 1.000},
        }],
        ["main", "Let's turn clips for boxes ON!", act, {
            'boxmove': {'loop': -1, 'play': 1, 'speed': 1},
            'boxspin': {'loop': -1, 'play': 1, 'speed': 1},
        }],
        ["main", "Alright, I feel dizzy... Let's stop them all.", anime, (
            {
                'boxmove': {'frame': 0, 'loop': -1, 'play': 0, 'speed': 1},
                'wave': {'frame': 0, 'loop': -1, 'play': 0, 'speed': 1.000},
                'boxspin': {'frame': 0, 'loop': -1, 'play': 0, 'speed': 1},
                'cam': {'goto_pos': ((0.472, 1.061, 0.124), (0.000, 0.000, -4.150), (-0.550, 179.350, 0.000))},
            },
            {
                'main': {'anim': (0, 2, 36), 'hands': (0, 0), 'kinematic': 0, 'anim_spd': 1.000},
            }
        )],
        ["main", "Clip can be start/stop just like game's build-in animation. They do not use timer so you can run many clips at the same time! And wouldn't conflict with script anime."],
        #-VNFA:seq:end:2-#
    ], toSeq3)

def toSeq3(game):
    game.texts_next([
        #-VNFA:seq:start:3-#
        ["main", "Now I will try to explain how to build a clip. VNFrame3.0 provide a new tool to build and manager clips, no coding needed at all. From here, you may need to switch between ScriptHelper and main game, remember the default hotkey is Ctrl-F5.", act, {
            'main': {'anim': (0, 5, 1)},
            'cam': {'goto_pos': ((0.472, 1.061, 0.124), (0.000, 0.000, -4.150), (-0.550, 179.350, 0.000))},
        }],
        ["main", "At first, switch to ScriptHelper you will find a new button [Clip Manager] at the bottom of window. Click to switch to manager tab, and in it you can see three clips on left side, these are the clips used in this demo. And there are play control buttons on right side, you can try them by yourself.", act, {
            'main': {'anim': (0, 0, 9)},
        }],
        ["main", "As you see, every clip has a name. Name of clips serves like tag of actor/prop, they cannot duplicate with others! When you click the [Create] button to build a new clip, the first thing to do is input a name. Now, try the [Create] button and select [Empty Clip], input a valid name and then create it.", act, {
        }],
        ["main", "Now we are in the clip editor UI. In the top of window is the progress bar and play control buttons. And then 5 tab buttons are [Actor/Prop] [Camera] [System] [Clips] and [Setting]. The first 4 tabs are where we create keyframes, for different targets. The last one [Setting] is about this clip, let start from [Setting]. Check it please.", act, {
        }],
        ["main", "[Name] is what you just input. [Priority] is about the update sequence of clips. In previous demo I actived 3 clips but they control different object or different property. If more than 2 clips control the same property of same object, they are conflict. The one with greater priority will be update later, so it will overwrite the one with less priority.", act, {
        }],
        ["main", "[Length] is how many frames in you clip totally. [FPS] is the default frame rate. Oh! It is NOT the actual FPS of the clip anime. It is much more like 'How many frames do you need in 1 second'. The actual FPS depends on your machine power. For example, the 'boxspin' clip's length is 2 and FPS is 1, but it still spins smoothly.", act, {
        }],
        ["main", "If you check the contents of 'boxspin' clip, you will found when the [Length] is 2, there are 3 frames in it: the frame 0, 1 and 2. And frame 0 and 2 are keyframes. Is the empty frame between 0 and 2 necessary? Yes, it is! It tell clip engine to interpolate between frame 0 and 2. The engine will not insert interpolate frame between contiguous keyframes.", act, {
        }],
        ["main", "Back to setting tab, [Speed] is the play speed ratio, you can adjust it at runtime. [Loop] is the loop count. 0 means no loop, -1 means infinite, 1 means loop once (play twice) and so on. Here is the default loop setting, you can set another loop count on play.", act, {
        }],
        ["main", "And the [Content], there are nothing now. After you build some keyframes, you can check here to get a brief about how many keyframes are created for each object. If you changed some setting, use the [Apply] button to make it take effect.", act, {
        }],
        #-VNFA:seq:end:3-#
    ], toSeq4)

def toSeq4(game):
    game.texts_next([
        #-VNFA:seq:start:4-#
        ["main", "Now let's go back to [Actor/Prop] tab. We can create keyframe for actor or prop here. As you know, everything you want to control by vnframe must be TAGGED first. For clips, this principle remains unchanged.", act, {
            'cam': {'goto_pos': ((0.472, 1.061, 0.124), (0.000, 0.000, -4.150), (-0.550, 179.350, 0.000))},
            'main': {'anim': (0, 0, 10)},
        }],
        ["main", "In clip editor, we can select the actor/prop in workspace (the tree view) of studio and build keyframe for it. Try select me in workspace, and there will be a message says '[上杉美沙(main)]: No key frames'. 'main' is the tag for me, and I am ready to build keyframe for. If you select the floor object, you will see a message says it is not tagged yet, and there is a button at bottom-left to help you tag it right now.", act, {
        }],
        ["main", "After tag ready, we can build keyframe. Keyframe is a very common concept in almost all animation soft. If you don't know what it is, google it. You can seek to a frame and then click the [create] button, and the current status of selected actor/prop will be saved into a keyframe.", act, {
        }],
        ["main", "After create a keyframe, the keyframe No. will be listed at left side, and the [Create] button changes to [Update]. It is easy to modify keyframe, just seek to it (by click the keyframe No. in list is the fastest way), change the status of actor/prop, and click the [Update].", act, {
        }],
        ["main", "When you click [Create] or [Update], only the selected properties will be saved. Clip editor let you set which property you want to keyframe, but I recommend include all properties, unless you know what you are doing very clearly. And we can use the optimize function to delete all unused properties automatically, after we are done creating all keyframes.", act, {
        }],
        ["main", "Now you can try it, move things around and create keyframes. If the property you changed between keyframes can be animated, engine will insert interpolate frame for it. Interpolate is controlled by a Bezier curve show at right side, you can set the curve by drag the handle besides [X1,Y1,X2,Y2], and by click the [>>>] button you will found some presets and copy-paste function for curve.", act, {
        }],
        ["main", "If you set a keyframe at #10 and another at #20, the interpolate frames between #10 and #20 are controlled by the curve of keyframe at #20. It also means the curve of the first keyframe is always ignored.", act, {
        }],
        ["main", "There are some function buttons at the bottom of window. [Delete] use to delete one keyframe. [Shift] can shift the keyframe to another frame position, [Copy] can copy a keyframe to clipboard, and then you can use [Paste] to put it at new position. Copy the first keyframe and paste it at the last frame is useful to make a loop animation.", act, {
        }],
        ["main", "Click the [+ More +] button will show some function about all keyframes. You can import/export all keyframes of current selected actor or prop from/to file. The import and export here exclude actor/prop id, so you can export all keyframes from actor A and then import them to actor B.", act, {
        }],
        #-VNFA:seq:end:4-#
    ], toSeq5)

def toSeq5(game):
    game.texts_next([
        #-VNFA:seq:start:5-#
        ["main", "Now, check the [Camera] and [System] tab. They work like [actor/prop] tab, only their tag are reserved so you don't need to select anything. Then the [Clip] tab. You can't select clip in studio's workspace, so you have to select target clip at here to create keyframe for it.", act, {
            'main': {'anim': (0, 0, 13)},
        }],
        ["main", "There are only 4 properties for a clip can be controlled at runtime. [Play] the play status, [Frame] the seek position, [Loop] the loop count, and [Speed] the speed ratio. There is no curve setting because none of the 4 properties can be animated.", act, {
        }],
        ["main", "And not like others, to build clip keyframes you must input the property's value by hand. Not dump from current status. By create keyframe for clip you can sync with another clip. Use it wisely.", act, {
        }],
        ["main", "Finally go back to [Setting] tab. After we done creating our clip, we can save it to file by using the [Export] here. This function will save everything in current clip. [Dump] do the similar work, only difference is it write info into 'dumppython.txt'.", act, {
            'main': {'anim': (0, 0, 14)},
        }],
        ["main", "[Import] load info from file, but if the tag in file not existed in scene, its keyframes will be skipped. [Optimize] can delete unchanged properties. Please, export you work before use optimize! If something goes wrong, you can import it to undo the optimization.", act, {
        }],
        #-VNFA:seq:end:5-#
    ], toSeq6)

def toSeq6(game):
    game.texts_next([
        #-VNFA:seq:start:6-#
        ["main", "After we create clips, we can use them in game. VNFrame3.0 release with an updated auto script template, it supports clip well. This demo is build by the auto script, as you can see, all clip data is written into python file itself and loaded to clip engine at initialization.", act, {
            'main': {'anim': (0, 0, 17)},
            'cam': {'goto_pos': ((0.472, 1.061, 0.124), (0.000, 0.000, -4.150), (-0.550, 179.350, 0.000))},
        }],
        ["main", "In this way, you can control your clip by script directly. And you can modify clips and then hit the [Build Clips] button in clip manager, the updated clip data will be written into python file again after you save the python.", act, {
        }],
        ["main", "If you want to use clip in your old auto script based game, you need migrate your game to new auto script template, by doing following 2 steps: First, build a new game with VNFrame3.0. Next, copy all the toSeqn() functions from old game and overwrite the toSeqn() functions in new game. And then clips should work.", act, {
        }],
        ["main", "And if you are coding by yourself, just refer to this python file about how to use clips. And you can find some useful functions in vnanime.py, too. You can find clip data from exported or dumped file, when auto script disabled, there will be a [Dump Clips] in clip manager which dump all the clips into dumppython.py.", act, {
        }],
        ["main", "Clip can be controlled in act script. The auto dump in ScriptHelper support dump clip status too. In VNFrame3.0, you can choose the targets for dump now. Click the [n objs] button at the middle-top of script builder page, you can set dump targets from all valid actors, props and clips.", act, {
            'main': {'anim': (0, 0, 18)},
        }],
        ["main", "This update is mainly for clips. For example, if you want to dump a script to play the 'boxspin' clip, first you need to start play 'boxspin' in clip manager, and then dump the script with 'boxspin' be set as target. But may be you want to exclude 'box' from dump targets, because it is controlled by clip and we do not intent to control it by script again.", act, {
        }],
        ["main", "There are some limitation on auto dump script to control clip. 1: when clip is play, the frame position info will not be dumped. Because it changes too fast you can't get what you want at dump. 2: the loop dumped is the setting value, not the runtime value. If you need control clip exactly, retouch the script by yourself, or use function call by writing code.", act, {
        }],
        ["main", "Alright, I think I talked too much. It's your time now! Have fun with new feature!", act, {
            'cam': {'goto_pos': ((0.835, 1.272, -0.127), (0.000, 0.000, -1.945), (10.750, 190.350, 0.000))},
            'main': {'anim': (0, 0, 33)},
        }],
        #-VNFA:seq:end:6-#
    ], toSeq7)

def toSeq7(game):
    game.texts_next([
        #-VNFA:seq:empty:7-#
    ], toEnd)
    
#-VNFA:sel:empty:1-#
    
def toEnd(game, text = None):
    if text == None:
        text = "<size=32>THE END</size>"
    game.set_text_s(text)
    if True:
        game.set_buttons(["Show me the demo again.", "Again, how to build a clip?", "Again, how to use clips?", "Understood! Bye bye!"], [toSeq1, toSeq3, toSeq6, clearExit])
    else:
        clearExit(game)

def clearExit(game):
    clear_keyframe_anime(game)
    game.scenePNG = ""
    game.return_to_start_screen_clear()

# Keyframe clips build by clip manager
keyframeClips = [
#-VNFA:KeyFrameClips:start-#
{
    'setting': {
        'name' : 'boxmove',
        'frameLength': 120,
        'frameRate': 30,
        'priority': 100,
        'animeType': 'absolute',
        'loop': -1,
        'speed': 1,
    },
    'props': {
        'box': {
            0 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'move_to': (0.000, 1.000, 0.000)}},
           30 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'move_to': (0.400, 1.000, 0.000)}},
           60 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'move_to': (0.400, 1.400, 0.000)}},
           90 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'move_to': (0.000, 1.400, 0.000)}},
          120 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'move_to': (0.000, 1.000, 0.000)}},
        },
    },
}
,
{
    'setting': {
        'name' : 'boxspin',
        'frameLength': 2,
        'frameRate': 1,
        'priority': 100,
        'animeType': 'absolute',
        'loop': -1,
        'speed': 1,
    },
    'props': {
        'box': {
            0 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'rotate_to': (0.000, 0.000, 0.000)}},
            2 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'rotate_to': (0.000, 359.000, 0.000)}},
        },
    },
}
,
{
    'setting': {
        'name' : 'wave',
        'frameLength': 120,
        'frameRate': 30,
        'priority': 100,
        'animeType': 'absolute',
        'loop': -1,
        'speed': 1,
    },
    'actors': {
        'main': {
            0 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'anim': (1, 3, 14), 'anim_spd': 0.000, 'fk_active': (0, 1, 0, 1, 0, 0, 0), 'fk_set': {0: (0.567, 4.623, -3.622), 1: (6.499, -0.517, 12.268), 2: (-13.914, 0.379, 14.297), 3: (1.337, -0.251, 13.132), 4: (0.668, -0.127, 11.775), 5: (0.000, 0.000, 0.000), 6: (-3.006, -6.753, 19.001), 7: (14.139, 0.000, 0.000), 8: (-14.349, -13.610, -12.108), 9: (-0.403, 0.328, -0.329), 10: (0.452, 7.705, -7.873), 11: (11.439, 0.000, 0.000), 12: (-14.135, 6.184, 10.150), 13: (-2.184, -0.438, 0.425), 14: (-25.171, -13.283, 9.098), 15: (43.213, 10.027, 84.462), 16: (-55.834, -56.373, 56.649), 17: (-9.775, -19.575, 17.201), 18: (-0.819, 11.416, -14.887), 19: (-5.318, 0.480, -27.450), 20: (-42.066, 44.168, -28.450), 21: (-30.199, 1.005, -32.299)}, 'hands': (3, 3), 'ik_active': (1, 1, 1, 1, 1), 'ik_set': {}, 'kinematic': 2}},
           60 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'fk_set': {1: (6.499, -0.517, -12.394), 2: (-13.914, 0.379, -3.989), 3: (1.337, -0.251, -10.381), 4: (0.668, -0.127, -6.727), 15: (43.213, 10.027, 41.497), 16: (-69.204, -26.221, 29.591), 17: (-17.805, 15.374, 8.598), 19: (-5.318, 0.480, -78.064), 20: (-31.811, 62.900, -39.817)}}},
          120 : {'curve': [0.200, 0.800, 0.200, 0.800], 'status': {'fk_set': {1: (6.499, -0.517, 12.268), 2: (-13.914, 0.379, 14.297), 3: (1.337, -0.251, 13.132), 4: (0.668, -0.127, 11.775), 15: (43.213, 10.027, 84.462), 16: (-55.834, -56.373, 56.649), 17: (-9.775, -19.575, 17.201), 19: (-5.318, 0.480, -27.450), 20: (-42.066, 44.168, -28.450)}}},
        },
    },
    'cam': {
            0 : {'curve': [0.200, 0.800, 0.200, 0.800], 'distance': (0.000, 0.000, -3.933), 'fieldOfView': 23.000, 'pos': (0.875, 1.192, 0.003), 'rotate': (-0.550, 185.200, 0.000)},
           30 : {'curve': [0.200, 0.800, 0.200, 0.800], 'distance': (0.000, 0.000, -2.328), 'fieldOfView': 23.000, 'pos': (0.875, 1.382, 0.003), 'rotate': (-0.550, 185.200, 0.000)},
           60 : {'curve': [0.200, 0.800, 0.200, 0.800], 'distance': (0.000, 0.000, -3.933), 'fieldOfView': 23.000, 'pos': (0.875, 1.192, 0.003), 'rotate': (-0.550, 185.200, 0.000)},
           90 : {'curve': [0.200, 0.800, 0.200, 0.800], 'distance': (0.000, 0.000, -2.328), 'fieldOfView': 23.000, 'pos': (0.875, 1.382, 0.003), 'rotate': (-0.550, 185.200, 0.000)},
          120 : {'curve': [0.200, 0.800, 0.200, 0.800], 'distance': (0.000, 0.000, -3.933), 'fieldOfView': 23.000, 'pos': (0.875, 1.192, 0.003), 'rotate': (-0.550, 185.200, 0.000)},
    },
}
,
{
    'setting': {
        'name' : 'dogf',
        'frameLength': 100,
        'frameRate': 30,
        'priority': 100,
        'animeType': 'absolute',
        'loop': -1,
        'speed': 1,
    },
    'actors': {
        'main': {
            0 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'mouth_open': 0.000}},
           55 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'mouth_open': 0.484}},
          100 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'mouth_open': 0.000}},
        },
    },
}
,
{
    'setting': {
        'name' : 'dogs1',
        'frameLength': 90,
        'frameRate': 30,
        'priority': 100,
        'animeType': 'absolute',
        'loop': -1,
        'speed': 0,
    },
    'actors': {
        'main': {
            0 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'fk_set': {1: (-22.558, -35.104, 11.070)}, 'ik_set': {'cf_j_arm00_L': ((0.050, 0.371, -0.264), ), 'cf_j_arm00_R': ((-0.131, 0.415, -0.238), )}}},
           40 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'fk_set': {1: (-24.979, -10.608, 1.068)}, 'ik_set': {'cf_j_arm00_L': ((0.110, 0.393, -0.264), ), 'cf_j_arm00_R': ((-0.075, 0.380, -0.238), )}}},
           90 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'fk_set': {1: (-22.558, -35.104, 11.070)}, 'ik_set': {'cf_j_arm00_L': ((0.050, 0.371, -0.264), ), 'cf_j_arm00_R': ((-0.131, 0.415, -0.238), )}}},
        },
    },
}
,
{
    'setting': {
        'name' : 'dogs2',
        'frameLength': 120,
        'frameRate': 30,
        'priority': 100,
        'animeType': 'absolute',
        'loop': -1,
        'speed': 0,
    },
    'actors': {
        'main': {
            0 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'ik_set': {'cf_j_hips': ((0.067, 0.337, -0.004), ), 'cf_j_thigh00_L': ((0.207, 0.379, 0.139), ), 'cf_j_thigh00_R': ((0.004, 0.279, 0.139), )}}},
           70 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'ik_set': {'cf_j_hips': ((-0.069, 0.337, -0.004), ), 'cf_j_thigh00_L': ((0.110, 0.293, 0.139), ), 'cf_j_thigh00_R': ((-0.212, 0.366, 0.139), )}}},
          120 : {'curve': [0.400, 0.600, 0.000, 1.000], 'status': {'ik_set': {'cf_j_hips': ((0.067, 0.337, -0.004), ), 'cf_j_thigh00_L': ((0.207, 0.379, 0.139), ), 'cf_j_thigh00_R': ((0.004, 0.279, 0.139), )}}},
        },
    },
}
,
#-VNFA:KeyFrameClips:end-#
]
