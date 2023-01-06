#===============================================================================================
# Engine Frame Function
# v1.1
# - Base on vngameengine 7.5
# - Add a new feature Script helper, access from developer console (CTRL-F4) then dump scene
# - Modify some action function to take parameter from auto generated scripts
# - Use Prop class to control item/folder, 'color' action's parameter changed! 
#   IF YOU USED 'color' ACTION, YOU MUST MODIFY THE PARAMETER!
# - Add 'btn_next', 'bg_png', 'fm_png' action function for system
# - register_actor_prop_by_tag() use scenef_register_actorsprops() from vngameengine, old one commented out
# - fake auto lip sync is supported by vngameengine now, so commented out from vnframe
# v1.2
# - Base on vngameengine 7.6
# - Can be toggle by VNFrameDeveloperConsole hotkey (defualt is Ctrl+F5), thank to @keitaro.
#   In this way, you even not need to use init_script_helper(). (init_script_helper also works)
# - sys_btn_next() function change texts on next button temporary. It affects current click and 
#   only current click
# - Optimize the output for IK/FK diff script, remove duplicated bone info.
# - Add a prompt message view for dangerous buttons. 
#   If you don't need it, disable it by set masterMode to True.
# v2.0
# - Move all wrapper function to VNActor.py, because they are game dependance.
# - Add load_and_init_scene() and register_string_resource() to support new feature in ScriptHelper
# - Advanced ScriptHelper:
#   - Improved GUI, add a minimize button on ScriptBuilder screen
#   - Script clips can be update/insert/delete after set into AnimeBuffer, preview will not overwrite old scene now
#   - New SceneHelper screen. Help manage png and python file, create tag, localization, and auto script feature
#   - localize helper and string dictionary helps using UNICODE texts in game
#   - A 'next-only' story can be build by ScriptHelper, without write ANY code. ScriptHelper can generate everything!
# - Add a template file vnftemplate.py, used by auto script feature in ScriptHelper, to create new game automaticlly
# v2.1
# - Bug fix
# - Work with vngameengine v8.1
# - Fix save scene function, support other mod's .extdata now.
# v2.2
# - Bug fix
# - A new utility "Couple Helper" in scene helper page. It helps create H scene quickly.
# v2.3
# - Support "wait_anime" and "wait_voice" to control anime-time
# - Support anime script can use non-range parameter just like act script. 
#   VNFrame will try to build anime from current state to the target state
# - New function addProp() and delProp() can be used to add and delete props at runtime.
# v2.3.2
# - add "game_func" to run game functions
#   example: {'game_func': [(sup_print, "1"), (sup_print, "2")]} or {'game_func': (sup_print, "test1")}
# v2.3.3
# - export sorted script.
# - add a "scriptCopy" function to make a deep copy for script.
# v2.3.4
# - bug fix
# v2.3.5 (Keitaro)
# - change init functions for running with 8.9+ engine (with skin system)
# v2.3.6 (Keitaro)
# - change act function to handle constructions like {actor: params} (no actorid, but actor object itself)
# v2.3.7 (Keitaro)
# - fixed some bug in prop handling
# v2.3.8 (Keitaro)
# - (act function) more correct processing of Prop creation due to v8.10
# v2.3.9 (Keitaro)
# - (act function) call import_status for Prop and Actor instead of direct processing
# v2.4 (countd360)
# - support UTF-8
# - <Create TAG> command in ScriptHelper can use <-propchild:> to tag a light.
# v3.0 (countd360)
# - A new feature: "key frame clips" added!
#   - Create and manage key frame based animation clips in ScriptHelper!
#   - A clip can animate tagged actors and props, camera and system, and sync which another clip.
#   - Several clips can be run in the same time. So you can create one clip for one actor, or
#     even several clips for one actor, and then run them at same time to make an animation.
#   - Clip can be controlled in act script like a game build-in anime. 
#     Clip status can be dumpped by script helper.
# - In script builder can choose which actor/prop/clip you want to dump now.
# - Auto script template update:
#   - Support key frame clips
#   - Support skin selection
#   - Choice to show a "restart" button the end of game
#   - Choice to use quick reload, which restart game without reload the scene file.
# - (act function) call import_status_diff_optimized for Prop and Actor instead of direct processing.
# - [Create Tag] button in scene helper will register the new tagged object to actor/prop automatically.
# v3.1 (countd360)
# - load/save extend data for HoneyStudioNeo
# - interpolate can handle vector3 with tuple/list
# v3.2.1 (Keitaro)
# - templorarily removed UTF-8 header for work with studio without UTF-8 support
# v3.2.2 (Keitaro)
# - fix for using act function without game.gdata.kfaManagedClips
# v3.2.3 (countd360)
# - add a "reset" button in scene helper tab to reset vnanime (maybe temporary) 
# v3.3 (countd360)
# - add a "vnactor setting" button in scene helper tab to set vnactor extend export at runtime. 
# v3.4 (countd360)
# - update tag_select function, support tag a route object
# - act function pick actors/props from game's actor/prop dict first,
#   anime function initialise itself, so vnframe should works without initialize.
# v3.5 (countd360)
# - add util "VNText Editor" and "Anime Info" in scenehelper tag
# v3.5.1 (countd360)
# - util function script2string and scriptCopy support Quaternion type
#===============================================================================================

from UnityEngine import Vector3, Vector2, Mathf, Color, Quaternion
from vngameengine import HSNeoOCI, HSNeoOCIChar, HSNeoOCIProp, HSNeoOCILight, HSNeoOCIItem, HSNeoOCIFolder, HSNeoOCIRoute
from vnactor import cam_act_funcs, sys_act_funcs, char_act_funcs, prop_act_funcs, export_sys_status
from vnactor import get_hanime_group_names, get_hanime_category_names, get_hanime_no_names
from vnactor import sys_wait_anime, sys_wait_voice
from vnactor import load_ini_file, get_ini_options, is_ini_value_true, set_ini_value, get_ini_exportOptionDesp
import copy

_sh = None  # instance of ScriptHelper

# act function
# this function read script and do the works
# script should be dictionary data
def act(game, script):
    # act script must be a dict
    # script: { 'tgt1' : {'tgt_fuc1' : tgt_func1_param, 'tgt_func2' : tgt_func2_param, ... }, 'tgt2' : {...}, ... }
    # tgt can be "cam" for camera, "sys" for system, actor name for actor or prop name for prop
    for tgt in script:
        try:
            # if param is a string
            if isinstance(tgt, basestring):
                # Handle camera
                if tgt == "cam":
                    for f in script[tgt]:
                        if f in cam_act_funcs:
                            cam_act_funcs[f][0](game, script[tgt][f])
                        else:
                            print "act error: unknown function '%s' for 'cam'"%(f)
                # Handle system
                elif tgt == "sys":
                    for f in script[tgt]:
                        if f in sys_act_funcs:
                            sys_act_funcs[f][0](game, script[tgt][f])
                        else:
                            print "act error: unknown function '%s' for 'sys'"%(f)
                # Handle game_func call
                elif tgt == "game_func":
                    funcs = script[tgt]
                    if type(funcs) is list:
                        pass
                    else:
                        funcs = [funcs]
                    for f in funcs:
                        game.call_game_func(f)
                # If this is a character in this scene
                elif tgt in game.scenef_get_all_actors():
                    game.scenef_get_actor(tgt).import_status_diff_optimized(script[tgt])
                elif hasattr(game.scenedata, 'actors') and tgt in game.scenedata.actors:
                    game.scenedata.actors[tgt].import_status_diff_optimized(script[tgt])
                    # for f in script[tgt]:
                    #     if f in char_act_funcs:
                    #         char_act_funcs[f][0](game.scenedata.actors[tgt], script[tgt][f])
                    #     else:
                    #         print "act error: unknown function '%s' for '%s'!"%(f, tgt)
                # If this is a prop in this scene
                elif tgt in game.scenef_get_all_props():
                    game.scenef_get_propf(tgt).import_status_diff_optimized(script[tgt])
                elif hasattr(game.scenedata, 'props') and tgt in game.scenedata.props:
                    game.scenedata.props[tgt].import_status_diff_optimized(script[tgt])
                    # for f in script[tgt]:
                    #     if f in prop_act_funcs:
                    #         prop_act_funcs[f][0](game.scenedata.props[tgt], script[tgt][f])
                    #     else:
                    #         print "act error: unknown function '%s' for '%s'!"%(f, tgt)
                # if this is a clip in the gdata
                elif hasattr(game.gdata, 'kfaManagedClips'):
                    if tgt in game.gdata.kfaManagedClips:
                        game.gdata.kfaManagedClips[tgt].import_status(script[tgt])
                    else:
                        print "act error: unknown target '%s'!" % (tgt)
                # else act can not handle it
                else:
                    print "act error: unknown target '%s'!"%(tgt)
            else:
                from vnanime import KeyFrameClip
                # we pass object with state
                if isinstance(tgt, HSNeoOCIChar):
                    # character
                    actor = tgt.as_actor
                    actor.import_status_diff_optimized(script[tgt])
                elif isinstance(tgt, HSNeoOCIProp):
                    # prop - folder or item
                    obj2 = tgt.as_prop
                    obj2.import_status_diff_optimized(script[tgt])
                elif isinstance(tgt, KeyFrameClip):
                    # keyframe clip
                    tgt.import_status(script[tgt])
                else:
                    print "act error in process tgt='%s' script='%s'" % (tgt, script[tgt]) + " : " + str(e)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print "act error in process tgt='%s' script='%s'"%(tgt, script[tgt]) + " : " + str(e)

# anime function
# this function read script and do animation works by sequence
# script should be tuple data
def anime(game, script):
    # script = (aniScene, aniScene, ... aniScene)
    # aniScene = (actScript, [duration], [style])
    # actScript like the script used by act function
    # if duration and style is obmitted, then aniScene = actScript, and will be pass to act function directly
    if not isinstance(script, tuple):
        print "anime function request tuple as script"
        return

    # init scene anime if not
    init_scene_anime(game)
    
    # check is old animation done
    if game.scnAnimeTID != -1:
        print "Old animation TID = %d is running!"%game.scnAnimeTID
        animeClearner(game)
    
    # save script into list
    game.aniList = []
    game.aniIndex = 0
    for aniScene in script:
        game.aniList.append(aniScene)
    
    # start worker
    #print "scene anime start: %d anime/act to do"%len(script)
    if game.isLockWindowDuringSceneAnimation:
        game.isHideGameButtons = True
    animeWorker(game)
    
def init_scene_anime(game):
    # init variables need for scene anime, do only once
    if hasattr(game, "scnAnimeTID"):
        return
    game.scnAnimeTID = -1  # timer id for scene animation
    game.isLockWindowDuringSceneAnimation = False
    
def animeWorker(game):
    try:
        # take out script
        if game.aniIndex >= len(game.aniList):
            # sync with ScriptHelper?
            game.scnAnimeTID = -1
            if game.isLockWindowDuringSceneAnimation:
                game.isHideGameButtons = False
            #print "scene anime done"
            return
        aniScene = game.aniList[game.aniIndex]
        game.aniIndex += 1
        
        # get info and setup 
        if not isinstance(aniScene, tuple) or len(aniScene) == 1:
            # process act
            if isinstance(aniScene, tuple):
                aniScene = aniScene[0]
            #print "Act"+str(game.aniIndex-1)+": [Non-Anime]"+str(aniScene)
            act(game, aniScene)
            animeWorker(game)   # goto next
            return
        elif len(aniScene) == 2:
            asAct = aniScene[0]
            asDur = aniScene[1]
            asEff = "linear"
        else:
            asAct = aniScene[0]
            asDur = aniScene[1]
            asEff = aniScene[2]
            
        # auto build range param if it is not
        for tgt in asAct.Keys:
            for fnc in asAct[tgt].Keys:
                param = asAct[tgt][fnc]
                try:
                    if isinstance(param, tuple) and len(param) == 2 and paramInterpolater(param[0], param[1], 0.5) != None:
                        isRangeParam = True
                    else:
                        isRangeParam = False
                except Exception:
                    isRangeParam = False
                if not isRangeParam:
                    curParam = currentParamBuilder(game, tgt, fnc)
                    if curParam != None:
                        asAct[tgt][fnc] = (curParam, param)
                        #print "param [%s][%s] is rebuild as range param"%(tgt, fnc)
                        #print curParam
                        #print "to"
                        #print param
                        #print ""
                    else:
                        #print "param [%s][%s] is not a range param"%(tgt, fnc)
                        pass
        
        #print "Act"+str(game.aniIndex-1)+": "+str(asAct)+", Dur: "+str(asDur)+", Eff: "+str(asEff)
        game.curAnimeAct = asAct
        game.curAnimeEff = asEff
        
        # setup timer and go
        game.scnAnimeTID = game.set_timer(asDur, animeWorker, animeUpdater)
        if game.scnAnimeTID == -1:
            print "animeWorker error: run out for timer resource"
            animeClearner(game)
    except Exception as e:
        print "animeWorker error:", str(game.aniList[game.aniIndex-1]), ":", str(e)

def animeClearner(game):
    print "animeClearner: start collapse anime from Act%d"%(game.aniIndex-1)
    # stop scene anime timer if exists
    if game.scnAnimeTID != -1:
        game.clear_timer(game.scnAnimeTID)
    game.scnAnimeTID = -1
    
    # stop cam anime timer if exists
    if game.camAnimeTID != -1:
        game.clear_timer(game.camAnimeTID)
    game.camAnimeTID = -1
    
    # collapse current and rest animes/acts into one act script
    actScript = scriptCollapser(game.aniList)
    print "animeClearner collapsed act: "+script2string(actScript)
    
    # call act to do collapsed script
    act(game, actScript)

def animeUpdater(game, dt, time, duration):
    try:
        # calculate progress
        if time > duration : time = duration
        asProgress = time2progress(time, duration, game.curAnimeEff)
        
        # handle special system command
        if 'sys' in game.curAnimeAct.Keys:
            if 'wait_anime' in game.curAnimeAct['sys']:
                if sys_wait_anime(game, game.curAnimeAct['sys']['wait_anime']):
                    #print "stop anime here time = %f"%time
                    game.clear_timer(game.scnAnimeTID, True)
        if 'sys' in game.curAnimeAct.Keys:
            if 'wait_voice' in game.curAnimeAct['sys']:
                if sys_wait_voice(game, game.curAnimeAct['sys']['wait_voice']):
                    #print "stop by voice at time = %f"%time
                    game.clear_timer(game.scnAnimeTID, True)
                    
        # set script
        actScript = {}
        for tgt in game.curAnimeAct:
            actScript[tgt] = {}
            for fnc in game.curAnimeAct[tgt]:
                rangeParam = game.curAnimeAct[tgt][fnc]
                if isinstance(rangeParam, tuple):
                    actScript[tgt][fnc] = paramInterpolater(rangeParam[0], rangeParam[1], asProgress)
                else:
                    actScript[tgt][fnc] = rangeParam
        
        # send to act
        #print actScript
        act(game, actScript)
        
        # sync with ScriptHelper
        if _sh != None:
            _sh.animeTime = time
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print "animeUpdater error:", str(e)
        
def scriptCollapser(orgList):
    # collapse orgList from colFrom into one act script dict
    #print ">>>>start collapse %d tuple/list"%len(orgList)
    actScript = {}    
    try:
        for i in range(len(orgList)):
            aniScene = orgList[i]
            #print aniScene
            if not isinstance(aniScene, tuple):
                asAct = aniScene
                simpleAct = True
            else:
                asAct = aniScene[0]     # dismiss duration and style
                simpleAct = False
            
            for tgt in asAct:
                if not tgt in actScript:
                    actScript[tgt] = {}
                for f in asAct[tgt]:
                    # take out final param
                    if simpleAct:
                        fp = asAct[tgt][f]      # an act format script
                    elif isinstance(asAct[tgt][f], tuple):
                        fp = asAct[tgt][f][1]   # take the final state as param
                    else:
                        fp = asAct[tgt][f]      # anime format but only have one param

                    # special process for cam
                    if tgt == 'cam':
                        #print ">> cam param : " + str(fp)
                        fp = camParamUnAnimator(f, fp)
                        #print ">> UnAnimate : " + str(fp)
                    
                    # register final param
                    actScript[tgt][f] = fp
    except Exception as e:
        print ">>>>scriptCollapser Error: " + str(e) + "\n"
    #else:
    #    print ">>>>collapse successed: " + str(actScript) + "\n"
    return actScript
    
def camParamUnAnimator(camFunc, camParam):
    # delete cam animation setting from cam act script param
    # WARNING! will delete onCamEnd function if setted!
    if camFunc == 'goto_preset':
        if not isinstance(camParam, tuple):
            return camParam
        else:
            if len(camParam) == 4:
                print "Warning from camParamUnAnimator: cam goto_preset onCamEnd func '%s' will be lost!"%str(camParam[3])
            return camParam[0]
            
    elif camFunc == 'goto_pos':
        if len(camParam) == 6:
            print "Warning from camParamUnAnimator: cam goto_pos onCamEnd func '%s' will be lost!"%str(camParam[5])
        return camParam[:3]
        
    elif camFunc == 'rotate':
        if len(camParam) == 3 and (not isinstance(camParam[0], tuple)):
            return camParam
        else:
            if len(camParam) == 4:
                print "Warning from camParamUnAnimator: cam rotate onCamEnd func '%s' will be lost!"%str(camParam[3])
            return camParam[0]
            
    elif camFunc == 'zoom':
        if not isinstance(camParam, tuple):
            return camParam
        else:
            if len(camParam) == 4:
                print "Warning from camParamUnAnimator: cam zoom onCamEnd func '%s' will be lost!"%str(camParam[3])
            return camParam[0]
            
    else:
        raise Exception("Unknown cam function " + camFunc)

def currentParamBuilder(game, tgt, fnc):
    if tgt == "sys" and fnc in ("wait_anime", "wait_voice"):
        return None # no warning for wait_xxx
    if tgt == "cam" and fnc == "goto_pos":
        caFuncScript = ScriptHelper.get_cam_status()['cam']
    elif tgt == "sys" and fnc in sys_act_funcs.Keys and sys_act_funcs[fnc][1]:
        caFuncScript = export_sys_status(game)
    elif tgt in game.scenef_get_all_actors() and fnc in char_act_funcs.Keys and char_act_funcs[fnc][1]:
        caFuncScript = game.scenef_get_actor(tgt).export_full_status()
    elif hasattr(game.scenedata, "actors") and tgt in game.scenedata.actors and fnc in char_act_funcs.Keys and char_act_funcs[fnc][1]:
        caFuncScript = game.scenedata.actors[tgt].export_full_status()
    elif tgt in game.scenef_get_all_props() and fnc in prop_act_funcs.Keys and prop_act_funcs[fnc][1]:
        caFuncScript = game.scenef_get_propf(tgt).export_full_status()
    elif hasattr(game.scenedata, "props") and tgt in game.scenedata.props and fnc in prop_act_funcs.Keys and prop_act_funcs[fnc][1]:
        caFuncScript = game.scenedata.props[tgt].export_full_status()
    else:
        print "currentParamBuilder error: param of '%s''%s' unknown or can not do animate!"%(tgt, fnc)
        return None
    #print "caFuncScript = " + script2string(caFuncScript)
    if fnc in caFuncScript.Keys:
        return caFuncScript[fnc]
    else:
        print "currentParamBuilder error: '%s' not found in auto build attribute list of '%s'"%(fnc, tgt)
        return None
        
def paramInterpolater(paramFrom, paramTo, progress):
    # calculate new parameter between paramFrom and paramTo by progress
    if paramFrom == None or paramTo == None:
        return None

    elif isinstance(paramFrom, tuple) or isinstance(paramFrom, list):
        # interpolate tuple or list, special case: enable interpolate between Vector3 and tuple(3) or list(3)
        if len(paramFrom) == 3 and isinstance(paramTo, Vector3):
            paramTo = (paramTo.x, paramTo.y, paramTo.z)
        elif (type(paramFrom) != type(paramTo)) or (len(paramFrom) != len(paramTo)): 
            raise Exception("Parameter mismatch %s vs %s! From: "%(str(type(paramFrom)), str(type(paramTo))) + str(paramFrom) + " To: " + str(paramTo))
        updParam = []
        for i in range(len(paramFrom)):
            subParam = paramInterpolater(paramFrom[i], paramTo[i], progress)
            updParam.append(subParam)
        return tuple(updParam)
        
    elif isinstance(paramFrom, dict):
        # interpolate dictionary
        if not isinstance(paramTo, dict): 
            raise Exception("Parameter mismatch %s vs %s! From: "%(str(type(paramFrom)), str(type(paramTo))) + str(paramFrom) + " To: " + str(paramTo))
        updParam = {}
        for ikey in paramFrom.Keys:
            if ikey in paramTo.Keys:
                subParam = paramInterpolater(paramFrom[ikey], paramTo[ikey], progress)
                updParam[ikey] = subParam
        return updParam
        
    elif isinstance(paramFrom, Vector3):
        # interpolate Vector3, special case: enable interpolate between Vector3 and tuple(3) or list(3)
        if (isinstance(paramTo, tuple) or isinstance(paramTo, list)) and len(paramTo) == 3:
            paramTo = Vector3(paramTo[0], paramTo[1], paramTo[2])
        elif not isinstance(paramTo, Vector3): 
            raise Exception("Parameter mismatch %s vs %s! From: "%(str(type(paramFrom)), str(type(paramTo))) + str(paramFrom) + " To: " + str(paramTo))
        return Vector3.Lerp(paramFrom, paramTo, progress)
    
    elif isinstance(paramFrom, Vector2):
        # interpolate Vector2
        if isinstance(paramTo, tuple) and len(paramTo) == 2:
            paramTo = Vector2(paramTo[0], paramTo[1])
        if not isinstance(paramTo, Vector2): 
            raise Exception("Parameter mismatch %s vs %s! From: "%(str(type(paramFrom)), str(type(paramTo))) + str(paramFrom) + " To: " + str(paramTo))
        return Vector2.Lerp(paramFrom, paramTo, progress)
    
    elif isinstance(paramFrom, Color):
        # interpolate Color
        if isinstance(paramTo, tuple) and len(paramTo) == 4:
            paramTo = Color(paramTo[0], paramTo[1], paramTo[2], paramTo[3])
        if not isinstance(paramTo, Color):
            raise Exception("Parameter mismatch %s vs %s! From: "%(str(type(paramFrom)), str(type(paramTo))) + str(paramFrom) + " To: " + str(paramTo))
        return Color.Lerp(paramFrom, paramTo, progress)
        
    else:
        # try to interpolate as float
        updParam = float(progress) * (float(paramTo) - float(paramFrom)) + float(paramFrom)
        return updParam
        
def time2progress(time, duration, style):
    # calculate progress
    if time > duration : time = duration
    progress = time / duration
    if style == "slow-fast":
        progress = Mathf.Pow(progress, 2)
    elif style == "fast-slow":
        progress = 1 - Mathf.Pow(1 - progress, 2)
    elif style == "slow-fast3":
        progress = Mathf.Pow(progress, 3)
    elif style == "fast-slow3":
        progress = 1 - Mathf.Pow(1 - progress, 3)
    elif style == "slow-fast4":
        progress = Mathf.Pow(progress, 4)
    elif style == "fast-slow4":
        progress = 1 - Mathf.Pow(1 - progress, 4)
    else:
        pass
    return progress
        
def register_actor_prop_by_tag(game):
    # the same as register_actor_prop_by_tag - but do it by core engine calls
    from vnactor import ActorHSNeo, ActorPHStudio, ActorCharaStudio, PropHSNeo, PropPHStudio, PropCharaStudio
    game.scenef_register_actorsprops()
    """
    tmpActors = game.scenef_get_all_actors()
    tmpProps = game.scenef_get_all_props()
    game.scenedata.actors = {}
    game.scenedata.props = {}
    if game.isStudioNEO:
        for a in tmpActors.Keys:
            game.scenedata.actors[a] = ActorHSNeo(tmpActors[a].objctrl)
        for p in tmpProps.Keys:
            game.scenedata.props[p] = PropHSNeo(tmpProps[p].objctrl)
    elif game.isPlayHomeStudio:
        for a in tmpActors.Keys:
            game.scenedata.actors[a] = ActorPHStudio(tmpActors[a].objctrl)
        for p in tmpProps.Keys:
            game.scenedata.props[p] = PropPHStudio(tmpProps[p].objctrl)
    elif game.isCharaStudio:
        for a in tmpActors.Keys:
            game.scenedata.actors[a] = ActorCharaStudio(tmpActors[a].objctrl)
        for p in tmpProps.Keys:
            game.scenedata.props[p] = PropCharaStudio(tmpProps[p].objctrl)
    else:
        print "Classic studio not supported!"
    """
    game.scenedata.actors = game.scenef_get_all_actors()
    tmpProps = game.scenef_get_all_props()
    game.scenedata.props = {}
    for p in tmpProps.Keys:
        game.scenedata.props[p] = game.scenef_get_propf(p)

def addProp(no, game=None, id=None):
    # for StudioNeo and PlayhomeStudio, just use 'no' to identify an item,
    # for CharaStudio, 'no' should be (group, category, no) to identify an item.
    from Studio import AddObjectItem
    from vngameengine import get_engine_id
    eid = get_engine_id()
    # add item
    if eid == "neo" or eid == "phstudio":
        ociitem = AddObjectItem.Add(no)
    else:
        ociitem = AddObjectItem.Add(no[0], no[1], no[2])
    # build prop object
    if eid == "neo":
        from vnactor import PropHSNeo
        newprop = PropHSNeo(ociitem)
    elif eid == "phstudio":
        from vnactor import PropPHStudio
        newprop = PropPHStudio(ociitem)
    elif eid == "charastudio":
        from vnactor import PropCharaStudio
        newprop = PropCharaStudio(ociitem)
    else:
        raise Exception("classic studio not supported")
    # register to props if game and id are set
    if game != None and id != None:
        if id == 'cam' or id == 'sys':
            raise Exception("reversed id 'sys' and 'cam' can not be used by user")
        elif id in game.scenedata.props.Keys:
            raise Exception("ID '%s' is already used by prop '%s'"%(id, game.scenedata.props[id].name))
        elif id in game.scenedata.actors.Keys:
            raise Exception("ID '%s' is already used by actor '%s'"%(id, game.scenedata.actors[id].name))
        game.scenedata.props[id] = newprop
    return newprop

def delProp(prop, game=None, id=None):
    from Studio import Studio
    # delete from props
    if game != None and id != None:
        if id in game.scenedata.props.Keys:
            game.scenedata.props.pop(id)
    # delete from studio
    studio = Studio.Instance
    studio.DeleteNode(prop.treeNodeObject)
        
def register_string_resource(game):
    # load string resource dictionary from -strings- folder
    # save game in a global variable for easy access
    game.scenedata.strings = {}
    strFolder = HSNeoOCIFolder.find_single("-strings-")
    if strFolder != None:
        for strTO in strFolder.treeNodeObject.child:
            try:
                #print strTO.textName
                ss = strTO.textName.split(":", 1)
                si = int(ss[0])
                if si in game.scenedata.strings.Keys:
                    print "Duplicated string id = %d: '%s' was overwrited by 's'"%(si, game.scenedata.strings[si], ss[1])
                game.scenedata.strings[si] = ss[1]
            except:
                pass
    print "-- Framework: Load %d string resources"%(len(game.scenedata.strings))

def load_and_init_scene(game, pngFile, initFunc, loadWait = 60):
    game.scenePNG = pngFile
    game.sceneInitFunc = initFunc
    game.load_scene(pngFile)
    game.scnLoadTID = game.set_timer(loadWait, _load_scene_timeout, _load_scene_wait)
    if game.scnLoadTID != -1:
        print "start load scene: " + pngFile
    else:
        game.set_text_s("Fail to load scene because of no more timer available.")
        game.set_buttons_end_game()

def _load_scene_timeout(game):
    # this is called when load scene timeouted
    game.set_text_s("Fail to load scene because of timeout.")
    game.set_buttons_end_game()
    
def _load_scene_wait(game, dt, time, duration):
    # check if scene is loaded
    if game.isFuncLocked == False:
        game.clear_timer(game.scnLoadTID)
        
        # load ext data
        try:
            if game.isStudioNEO:
                from extplugins import HSStudioNEOExtSave
                from os import path
                fullpath = path.join(game.get_scene_dir(), game.sceneDir + game.scenePNG)
                HSSNES = HSStudioNEOExtSave()
                HSSNES.LoadExtData(fullpath)
        except Exception as e:
            # ext data may be not necessary, continue on error
            import traceback
            traceback.print_exc()
            print "Unable to load ext data"

        # call init function
        game.sceneInitFunc(game)
        print "load and init scene done!\n"
    
def ltext(game, index):
    if game == None:
        raise Exception("Unexpected ltext() call (index = %d) when game is None. Do not use this function in other function's default parameter!"%index)
    if not hasattr(game.scenedata, "strings"):
        register_string_resource(game)
    if index in game.scenedata.strings.Keys:
        orgText = game.scenedata.strings[index]
        tgtText = orgText
        tt = orgText.split("#")
        #print "ltext", tt
        for i in range(int((len(tt)-1)/2)):
            vword = tt[i*2+1]
            #print "vword", vword
            if vword in game.registeredChars:
                rep = game.registeredChars[vword][1]
            elif vword in game.scenedata.props.Keys:
                rep = game.scenedata.props[vword].name
            else:
                try:
                    ivword = int(vword)
                    if ivword in game.scenedata.strings.Keys:
                        rep = game.scenedata.strings[ivword]
                    else:
                        rep = None
                except:
                    rep = None
            #print "rep", rep
            if rep != None:
                tgtText = tgtText.replace("#"+vword+"#", rep, 1)
        return tgtText
    else:
        return "Undefined text id = " + str(index)
        
def debug_game_texts_next(game, startfrom, nexttexts, endfunc):
    # collapse all the script before startfrom, and then start at startfrom
    if startfrom >= len(nexttexts):
        print "debug_game_texts_next: startfrom out of range! Jump to end!"
        endfunc(game)
        reutrn
    
    # collapse each skipped step into dict and collect them
    toColList = []
    for i in range(startfrom):
        if len(nexttexts[i]) != 4:
            continue
        if isinstance(nexttexts[i][3], tuple):
            actScript = scriptCollapser(nexttexts[i][3])
        elif isinstance(nexttexts[i][3], dict):
            actScript = nexttexts[i][3]
        else:
            print "Unknown param type: " + str(type(nexttexts[i][3]))
        toColList.append(actScript)
    
    # collapse skipped steps and act it
    actScript = scriptCollapser(toColList)
    if len(actScript) > 0:
        print "All step before step %d was collapsed into"%(startfrom)
        print actScript
        act(game, actScript)
    
    # prepare a new script list
    newScriptList = []
    for i in range(startfrom, len(nexttexts)):
        newScriptList.append(nexttexts[i])
    
    # run new 
    game.texts_next(newScriptList, endfunc)
    
# -------------------------- script helper --------------------------
class ScriptClipInfo():
    def __init__(self):
        # scene
        self.dumpTypeIndex = 0
        self.dumpTgts = None
        self.dumpAsIndex = 0
        self.animeDuration = 1
        self.animeStyle = 0
        self.speakerAlias = ""
        self.dialogue = ""
        # camera
        self.includeCamera = False
        self.animateCamera = False
        self.useCameraTimer = True
        self.cameraDuration = 1
        self.cameraStyle = 0
        # system
        self.hideWindowInAnime = False
        self.hideButtonInAnime = False
        
class ScriptClip():
    def __init__(self):
        self.finalScnStatus = None
        self.finalCamStatus = None
        self.nonAnimeScript = None
        self.animeScript = None
        self.tailScript = None
        self.info = None

class AutoScriptInfo():
    def __init__(self):
        self.gameName = ""
        self.pythonName = ""
        self.sceneDir = ""
        self.scenePNG = ""
        self.enableReload = True
        self.enableQuickReload = False
        self.alwaysHideWindowInCameraAnime = False
        self.alwaysLockWindowInSceneAnime = False
        self.createLocalizeString = False
        self.defaultNextBtnText = "Next >>"
        self.defaultReloadBtnText = "Restart <<"
        self.defaultEndBtnText = "End Game >>"
        self.defaultEndText = "<size=32>THE END</size>"
        self.skinVersion = "skin_renpy"
        self.fakeLipSyncEnable = True
        self.fakeLipSyncVersion = "v11"
        self.fakeLipSyncReadingSpeed = 12.0
        self.masterMode = False
        
class ScriptHelper():

    def __init__(self, tgtGame):
        # const
        self._normalWidth = 500
        self._normalHeight = 265
        self._shrinkWidth = 130
        self._shrinkHeight = 55
        self._animeStyleTexts = ("linear", "slow-fast", "fast-slow", "slow-fast3", "fast-slow3", "slow-fast4", "fast-slow4")
        
        # basic setting
        init_scene_anime(tgtGame)
        self.game = tgtGame
        self.orgWWidth = 0
        self.orgWHeight = 0
        self.orgWindowCallback = None
        self.guiOnShow = False
        self.guiWidth = self._normalWidth
        self.guiHeight = self._normalHeight
        self.guiScreenIndex = 0
        
        # utility setting
        self.baseNest = "        "
        self.nestWord = "    "
        self.masterMode = False
        self.slowMotionRate = 10
        self.createLocalizeStringOnBuild = True

        # script builder setting
        self.curSCInfo = ScriptClipInfo()

        # anime buffer and reference setting
        self.init_anime_buffer(False)
        
        # runtime
        self.dumpClipToFile = False
        self.slowMotion = False
        self.pythonContent = ""
        self.asTemplate = False
        self.asEnable = False
        self.asInfo = AutoScriptInfo()
        
        # some game attribute used by script helper
        if not hasattr(tgtGame, "endNextTextFunc"):
            tgtGame.endNextTextFunc = None
        if not hasattr(tgtGame, "scenePNG"):
            tgtGame.scenePNG = ""
            
    def init_anime_buffer(self, rescan = True):
        # rescan
        if rescan or not hasattr(self.game.scenedata, "actors") or not hasattr(self.game.scenedata, "props"):
            register_actor_prop_by_tag(self.game)
        if rescan or not hasattr(self.game.scenedata, "strings"):
            register_string_resource(self.game)
    
        # reset prev status
        self.prevScnStatus = ScriptHelper.get_scn_status(self.game)
        self.prevCamStatus = ScriptHelper.get_cam_status()
        
        # reset anime buffer
        initSC = ScriptClip()
        initSC.finalScnStatus = self.prevScnStatus
        initSC.finalCamStatus = self.prevCamStatus
        initSC.info = ScriptClipInfo()
        self.animeBuffer = [initSC]
        self.animeBufferIndex = 0
        self.animeTime = 0
        
    def build_script_clip(self, info = None, refIndex = -1, tgtIndex = -1):
        # build script from refIndex clip to tgtIndex clip
        # if info set to None, use self.curSCInfo
        # if refIndex set to -1, diff from setted previous status
        # if tgtIndex set to -1, diff to current scene status
        if info == None:
            info = self.curSCInfo
        if refIndex == -1:
            preScnStatus = self.prevScnStatus
            preCamStatus = self.prevCamStatus
        else:
            preScnStatus = self.animeBuffer[refIndex].finalScnStatus
            preCamStatus = self.animeBuffer[refIndex].finalCamStatus
        if tgtIndex == -1:
            curScnStatus = ScriptHelper.get_scn_status(self.game)
            if info.includeCamera:
                curCamStatus = ScriptHelper.get_cam_status()
            else:
                curCamStatus = self.prevCamStatus
        else:
            curScnStatus = self.animeBuffer[tgtIndex].finalScnStatus
            curCamStatus = self.animeBuffer[tgtIndex].finalCamStatus

        # prepare scene contents
        if info.dumpTypeIndex == 0:
            # dump diff
            scnScript = ScriptHelper.diffSceneWithPrev(curScnStatus, preScnStatus)
        else:
            # dump full
            scnScript = curScnStatus

        # filter target ids
        if info.dumpTgts != None:
            for tgt in scnScript.keys():
                if info.dumpTgts.count(tgt) == 0:
                    scnScript.pop(tgt)
        
        # seperate by anime and non-anime
        dmpAnimeScript = {}
        dmpNonAnimeScript = {}
        dmpTailScript = {}
        if info.dumpAsIndex == 0 or info.animeDuration == 0:
            # no scene anime
            dmpNonAnimeScript.update(scnScript)
        else:
            # check every tgt(actor/prop) for every action, anime or non-anime
            for tgt in scnScript.Keys:
                if tgt in self.game.scenedata.actors:
                    for func in scnScript[tgt].Keys:
                        if func in char_act_funcs:
                            if char_act_funcs[func][1]:
                                if not tgt in dmpAnimeScript:
                                    dmpAnimeScript[tgt] = {}
                                dmpAnimeScript[tgt][func] = scnScript[tgt][func]
                            else:
                                if not tgt in dmpNonAnimeScript:
                                    dmpNonAnimeScript[tgt] = {}
                                dmpNonAnimeScript[tgt][func] = scnScript[tgt][func]
                        else:
                            print "Unexpected actor function '%s'"%(func)
                elif tgt in self.game.scenedata.props:
                    for func in scnScript[tgt].Keys:
                        if func in prop_act_funcs:
                            if prop_act_funcs[func][1]:
                                if not tgt in dmpAnimeScript:
                                    dmpAnimeScript[tgt] = {}
                                dmpAnimeScript[tgt][func] = scnScript[tgt][func]
                            else:
                                if not tgt in dmpNonAnimeScript:
                                    dmpNonAnimeScript[tgt] = {}
                                dmpNonAnimeScript[tgt][func] = scnScript[tgt][func]
                        else:
                            print "Unexpected prop function '%s'"%(func)
                elif tgt in self.game.gdata.kfaManagedClips:
                    from vnanime import clip_act_funcs
                    for func in scnScript[tgt].Keys:
                        if func in clip_act_funcs:
                            if clip_act_funcs[func][1]:
                                if not tgt in dmpAnimeScript:
                                    dmpAnimeScript[tgt] = {}
                                dmpAnimeScript[tgt][func] = scnScript[tgt][func]
                            else:
                                if not tgt in dmpNonAnimeScript:
                                    dmpNonAnimeScript[tgt] = {}
                                dmpNonAnimeScript[tgt][func] = scnScript[tgt][func]
                        else:
                            print "Unexpected clip function '%s'"%(func)
                elif tgt == "sys":
                    for func in scnScript[tgt].Keys:
                        if func in sys_act_funcs:
                            if sys_act_funcs[func][1]:
                                if not tgt in dmpAnimeScript:
                                    dmpAnimeScript[tgt] = {}
                                dmpAnimeScript[tgt][func] = scnScript[tgt][func]
                            else:
                                if not tgt in dmpNonAnimeScript:
                                    dmpNonAnimeScript[tgt] = {}
                                dmpNonAnimeScript[tgt][func] = scnScript[tgt][func]
                        else:
                            print "Unexpected sys function '%s'"%(func)
                else:
                    print "Unexpected alias '%s'"%(tgt)
                    
        # change anime script param to range param
        for tgt in dmpAnimeScript.Keys:
            for func in dmpAnimeScript[tgt].Keys:
                pFrom = preScnStatus[tgt][func]
                pTo = dmpAnimeScript[tgt][func]
                dmpAnimeScript[tgt][func] = (pFrom, pTo)
        
        # prepare camera contents
        if info.includeCamera:
            # dump camera, whatever changed or not
            camScript = {}
            camScript['cam'] = {}
            camScript['cam']['goto_pos'] = curCamStatus['cam']['goto_pos']  # don't know why copy.deepcopy cannot work, so I copy that manually.
            if info.animateCamera and info.useCameraTimer and info.cameraDuration != 0:
                # use camera timer to animate camera, add camera anime setting into camScript
                pList = list(camScript['cam']['goto_pos'])
                pList.append(info.cameraDuration)
                pList.append(self._animeStyleTexts[info.cameraStyle])
                camScript['cam']['goto_pos'] = tuple(pList)
                # merge to non-anime script
                dmpNonAnimeScript.update(camScript)
            elif info.animateCamera and not info.useCameraTimer and info.animeDuration != 0:
                # use scene timer to animate camera, add camera range param into camScript
                pFrom = preCamStatus['cam']['goto_pos']
                pTo = camScript['cam']['goto_pos']
                camScript['cam']['goto_pos'] = (pFrom, pTo)
                # merge to anime script
                dmpAnimeScript.update(camScript)
            else:
                # merge to non-anime script
                dmpNonAnimeScript.update(camScript)
        else:
            pass
            
        # create localize string if needed
        if self.dumpClipToFile and len(info.dialogue) > 0 and self.createLocalizeStringOnBuild:
            self.sd_init()
            newStrId = self.sd_find_or_create(info.dialogue)
            dlgString = "ltext(game, %d)"%newStrId
        else:
            dlgString = '"' + info.dialogue + '"'
            
        # prepare output string
        if info.dumpAsIndex == 0:
            # as new act
            if len(dmpNonAnimeScript) == 0:
                output = self.baseNest + '["%s", %s],\n'%(info.speakerAlias, dlgString)
            else:
                output = self.baseNest + '["%s", %s, act, {\n'%(info.speakerAlias, dlgString)
                for tgt in sorted(dmpNonAnimeScript.keys()):
                    output += self.baseNest + self.nestWord + "'" + tgt + "': " + script2string(dmpNonAnimeScript[tgt]) + ",\n"
                output += self.baseNest + '}],\n'
        elif info.dumpAsIndex == 1:
            # as new anime
            if len(dmpAnimeScript) == 0 and info.animeDuration > 0:
                # add a sys.idle function to anime script if anime duration is setted but no animeable function
                dmpAnimeScript['sys'] = {}
                dmpAnimeScript['sys']['idle'] = (0, 0)
                
            if len(dmpAnimeScript) > 0:
                if info.hideWindowInAnime:
                    # add a sys.visible=0 in non-anime script, and sys.visible=1 in tail
                    if not 'sys' in dmpNonAnimeScript.Keys:
                        dmpNonAnimeScript['sys'] = {}
                    dmpNonAnimeScript['sys']['visible'] = 0
                    dmpTailScript['sys'] = {}
                    dmpTailScript['sys']['visible'] = 1
                elif info.hideButtonInAnime:
                    # add a sys.lock=1 in non-anime script, and sys.lock=0 in tail
                    if not 'sys' in dmpNonAnimeScript.Keys:
                        dmpNonAnimeScript['sys'] = {}
                    dmpNonAnimeScript['sys']['lock'] = 1
                    dmpTailScript['sys'] = {}
                    dmpTailScript['sys']['lock'] = 0
            
            if len(dmpNonAnimeScript) + len(dmpAnimeScript) == 0:
                output = self.baseNest + '["%s", %s],\n'%(info.speakerAlias, dlgString)
            else:
                output = self.baseNest + '["%s", %s, anime, (\n'%(info.speakerAlias, dlgString)
                if len(dmpNonAnimeScript) > 0:
                    output += self.baseNest + self.nestWord + '({\n'
                    for tgt in sorted(dmpNonAnimeScript.keys()):
                        output += self.baseNest + self.nestWord + self.nestWord + "'" + tgt + "': " + script2string(dmpNonAnimeScript[tgt]) + ",\n"
                    output += self.baseNest + self.nestWord + '}),\n'
                if len(dmpAnimeScript) > 0:
                    output += self.baseNest + self.nestWord + '({\n'
                    for tgt in sorted(dmpAnimeScript.keys()):
                        output += self.baseNest + self.nestWord + self.nestWord + "'" + tgt + "': " + script2string(dmpAnimeScript[tgt]) + ",\n"
                    output += self.baseNest + self.nestWord + '}, %.2f, \'%s\'),\n'%(info.animeDuration, self._animeStyleTexts[info.animeStyle])
                if len(dmpTailScript) > 0:
                    output += self.baseNest + self.nestWord + '({\n'
                    for tgt in sorted(dmpTailScript.keys()):
                        output += self.baseNest + self.nestWord + self.nestWord + "'" + tgt + "': " + script2string(dmpTailScript[tgt]) + ",\n"
                    output += self.baseNest + self.nestWord + '}),\n'
                output += self.baseNest + ')],\n'
        else:
            # as sub anime
            if len(info.dialogue) > 0 and self.dumpClipToFile:
                # add a sys.text function to non-anime script if dialogue is setted, not necessary if not need to output to file
                if not 'sys' in dmpNonAnimeScript:
                    dmpNonAnimeScript['sys'] = {}
                dmpNonAnimeScript['sys']['text'] = (info.speakerAlias, dlgString)

            if len(dmpAnimeScript) == 0 and info.animeDuration > 0:
                # add a sys.idle function to anime script if anime duration is setted but no animeable function
                dmpAnimeScript['sys'] = {}
                dmpAnimeScript['sys']['idle'] = (0, 0)

            if len(dmpAnimeScript) > 0:
                if info.hideWindowInAnime:
                    # add a sys.visible=0 in non-anime script, and sys.visible=1 in tail
                    if not 'sys' in dmpNonAnimeScript.Keys:
                        dmpNonAnimeScript['sys'] = {}
                    dmpNonAnimeScript['sys']['visible'] = 0
                    dmpTailScript['sys'] = {}
                    dmpTailScript['sys']['visible'] = 1
                elif info.hideButtonInAnime:
                    # add a sys.lock=1 in non-anime script, and sys.lock=0 in tail
                    if not 'sys' in dmpNonAnimeScript.Keys:
                        dmpNonAnimeScript['sys'] = {}
                    dmpNonAnimeScript['sys']['lock'] = 1
                    dmpTailScript['sys'] = {}
                    dmpTailScript['sys']['lock'] = 0

            if len(dmpNonAnimeScript) + len(dmpAnimeScript) == 0:
                print "Nothing to dump..."
                return
            else:
                output = ""
                if len(dmpNonAnimeScript) > 0:
                    output += self.baseNest + self.nestWord + '({\n'
                    for tgt in sorted(dmpNonAnimeScript.keys()):
                        output += self.baseNest + self.nestWord + self.nestWord + "'" + tgt + "': " + script2string(dmpNonAnimeScript[tgt]) + ",\n"
                    output += self.baseNest + self.nestWord + '}),\n'
                if len(dmpAnimeScript) > 0:
                    output += self.baseNest + self.nestWord + '({\n'
                    for tgt in sorted(dmpAnimeScript.keys()):
                        output += self.baseNest + self.nestWord + self.nestWord + "'" + tgt + "': " + script2string(dmpAnimeScript[tgt]) + ",\n"
                    output += self.baseNest + self.nestWord + '}, %.2f, \'%s\'),\n'%(info.animeDuration, self._animeStyleTexts[info.animeStyle])
                if len(dmpTailScript) > 0:
                    output += self.baseNest + self.nestWord + '({\n'
                    for tgt in sorted(dmpTailScript.keys()):
                        output += self.baseNest + self.nestWord + self.nestWord + "'" + tgt + "': " + script2string(dmpTailScript[tgt]) + ",\n"
                    output += self.baseNest + self.nestWord + '}),\n'
                    
        # save current to previous
        self.set_ref_scene(curScnStatus, curCamStatus)
            
        # output dump to file
        if self.dumpClipToFile:
            try:
                import codecs
                f = codecs.open('dumppython.txt', 'a+', 'utf-8')
                f.write(output)
                f.close()
            except Exception as e:
                print e
                
        # VNSceneScript patch
        import vngameengine
        sshelper = vngameengine.import_or_reload("vnframe_vnscenescripthelper")
        error = sshelper.dumpclip_toscenescript(self,output)
        if error == "":
            # all is ok
            pass
        else:
            # some error show
            pass
        # VNSceneScript patch end
        
        # build script clip
        newSC = ScriptClip()
        newSC.finalScnStatus = curScnStatus
        newSC.finalCamStatus = curCamStatus
        newSC.nonAnimeScript = dmpNonAnimeScript
        newSC.animeScript = dmpAnimeScript
        newSC.tailScript = dmpTailScript
        newSC.info = copy.copy(info)
        return newSC
        
    # script builder and anime buffer
    def append_clip(self):
        newSC = self.build_script_clip()
        self.animeBuffer.append(newSC)
        self.animeBufferIndex = len(self.animeBuffer) - 1
        self.clear_dialogue()
    
    def update_clip(self, useOldInfo = False):
        if self.animeBufferIndex == 0: raise Exception("Invalide operation: try to update init scene!")
        # update current clip
        if useOldInfo:
            updInfo = self.animeBuffer[self.animeBufferIndex].info
        else:
            updInfo = self.curSCInfo
        updSC = self.build_script_clip(updInfo, self.animeBufferIndex - 1)
        self.animeBuffer[self.animeBufferIndex] = updSC
        # update next clip if exist
        if self.animeBufferIndex < len(self.animeBuffer) - 1:
            updNextInfo = self.animeBuffer[self.animeBufferIndex + 1].info
            updNextSc = self.build_script_clip(updNextInfo, self.animeBufferIndex, self.animeBufferIndex + 1)
            self.animeBuffer[self.animeBufferIndex + 1] = updNextSc
        
    def insert_clip(self, useOldInfo = False):
        if self.animeBufferIndex == 0: raise Exception("Invalide operation: try to insert init scene!")
        # check time status
        if self.animeBuffer[self.animeBufferIndex].info.dumpAsIndex != 0:
            print "TODO: calculate insert anime progress at %.2f/%.2f"%(self.animeTime, self.animeBuffer[self.animeBufferIndex].info.animeDuration)
        else:
            print "current is a actiong."
        # create a new clip
        if useOldInfo:
            newInfo = self.animeBuffer[self.animeBufferIndex].info
        else:
            newInfo = self.curSCInfo
        newSC = self.build_script_clip(newInfo, self.animeBufferIndex - 1)
        self.animeBuffer.insert(self.animeBufferIndex, newSC)
        # update next clip
        updNextInfo = self.animeBuffer[self.animeBufferIndex + 1].info
        updNextSc = self.build_script_clip(updNextInfo, self.animeBufferIndex, self.animeBufferIndex + 1)
        self.animeBuffer[self.animeBufferIndex + 1] = updNextSc
        
    def delete_clip(self, rollBack = False):
        # if set rollBack, delete will set the the init status of current clip and delete current clip and all following clips
        if self.animeBufferIndex == 0: raise Exception("Invalide operation: try to delete init scene!")
        if rollBack or self.animeBufferIndex == len(self.animeBuffer) - 1:
            if self.animeBufferIndex > 0:
                self.animeBuffer = self.animeBuffer[:self.animeBufferIndex]
                self.animeBufferIndex -= 1
            self.prevScnStatus = self.animeBuffer[self.animeBufferIndex].finalScnStatus
            self.prevCamStatus = self.animeBuffer[self.animeBufferIndex].finalCamStatus
        else:
            #print "delete clip at", self.animeBufferIndex
            updInfo = self.animeBuffer[self.animeBufferIndex + 1].info
            updSc = self.build_script_clip(updInfo, self.animeBufferIndex - 1, self.animeBufferIndex + 1)
            self.animeBuffer.pop(self.animeBufferIndex)
            self.animeBuffer[self.animeBufferIndex] = updSc
        
    def set_ref_scene(self, scnStatus = None, camStatus = None):
        # set default
        if scnStatus == None:
            scnStatus = ScriptHelper.get_scn_status(self.game)
        if camStatus == None:
            camStatus = ScriptHelper.get_cam_status()
        # save to prev
        self.prevScnStatus = scnStatus
        self.prevCamStatus = camStatus
    
    def restore_scene_status(self, tgtSceneStatus):
        curScn = ScriptHelper.get_scn_status(self.game)
        difSpt = ScriptHelper.diffSceneWithPrev(tgtSceneStatus, curScn)
        #print "restore scene:", script2string(difSpt)
        act(self.game, difSpt)
        
    def restore_camera_status(self, tgtCameraStatus):
        act(self.game, tgtCameraStatus)
    
    def play_anime_clip(self, mode):
        # stop cam anime timer if exists
        if self.game.camAnimeTID != -1:
            self.game.clear_timer(self.game.camAnimeTID)
        self.game.camAnimeTID = -1
        
        if self.animeBufferIndex == 0:
            prevSC = self.animeBuffer[0]
            currSC = self.animeBuffer[0]
        else:
            prevSC = self.animeBuffer[self.animeBufferIndex-1]
            currSC = self.animeBuffer[self.animeBufferIndex]
        
        if mode == "tostart":
            # just restore init status = prev final status
            self.restore_scene_status(prevSC.finalScnStatus)
            if currSC.info.includeCamera:
                self.restore_camera_status(prevSC.finalCamStatus)
            self.animeTime = 0
        elif mode == "toend":
            # just restore final status
            self.restore_scene_status(currSC.finalScnStatus)
            if currSC.info.includeCamera:
                self.restore_camera_status(currSC.finalCamStatus)
            self.animeTime = currSC.info.animeDuration
        elif mode == "play" or mode == "play_and_next":
            if self.animeBufferIndex == 0:
                # restore init status only
                self.restore_scene_status(prevSC.finalScnStatus)
                self.restore_camera_status(prevSC.finalCamStatus)
            else:
                # restore prev status
                self.restore_scene_status(prevSC.finalScnStatus)
                if currSC.info.includeCamera:
                    self.restore_camera_status(prevSC.finalCamStatus)
                # play non-anime scipte then anime scipte
                if len(currSC.nonAnimeScript) > 0:
                    # non-anime script can be act 
                    act(self.game, currSC.nonAnimeScript)
                if len(currSC.animeScript) > 0:
                    # anime script must turn to tuple before pass to anime
                    if self.slowMotion:
                        aniDur = currSC.info.animeDuration * self.slowMotionRate
                    else:
                        aniDur = currSC.info.animeDuration
                    aniScript = (currSC.animeScript, aniDur, self._animeStyleTexts[currSC.info.animeStyle])
                    aniScript = (aniScript,)
                    anime(self.game, aniScript)
                if len(currSC.tailScript) > 0:
                    # tail script can be act, it will be acted soon but not after anime done TODO?
                    act(self.game, currSC.tailScript)
                    
            if mode == "play_and_next" and self.animeBufferIndex < len(self.animeBuffer) - 1:
                self.animeBufferIndex += 1
        elif mode == "stop":
            if self.game.scnAnimeTID != -1:
                self.game.clear_timer(self.game.scnAnimeTID)
                self.game.scnAnimeTID = -1
            if self.slowMotion:
                self.animeTime /= self.slowMotionRate
        elif mode == "toposition":
            asProgress = time2progress(self.animeTime, currSC.info.animeDuration, self._animeStyleTexts[currSC.info.animeStyle])
            #print "play anime at %.2f/%.2f, progress %.3f"%(self.animeTime, currSC.info.animeDuration, asProgress)
            # set script
            actScript = {}
            for char in currSC.animeScript:
                actScript[char] = {}
                for f in currSC.animeScript[char]:
                    rangeParam = currSC.animeScript[char][f]
                    if isinstance(rangeParam, tuple):
                        actScript[char][f] = paramInterpolater(rangeParam[0], rangeParam[1], asProgress)
                    else:
                        actScript[char][f] = rangeParam
            act(self.game, actScript)
        else:
            print "Unknown play mode:", mode
        
    def build_anime(self):
        # output anime to file
        allAnimeScript = self.output_anime_clips()
        # format the output string
        #output = script2string(allAnimeScript)
        output = ""
        for ntScript in allAnimeScript:
            # each next text script
            if len(ntScript) == 2:
                output += self.baseNest + '["%s", %s],\n'%(ntScript[0], ntScript[1] if ntScript[1].startswith("ltext(") else '"' + ntScript[1] + '"')
            elif ntScript[2] == act:
                output += self.baseNest + '["%s", %s, act, {\n'%(ntScript[0], ntScript[1] if ntScript[1].startswith("ltext(") else '"' + ntScript[1] + '"')
                for tgt in ntScript[3].Keys:
                    output += self.baseNest + self.nestWord + "'" + tgt + "': " + script2string(ntScript[3][tgt]) + ",\n"
                output += self.baseNest + "}],\n"
            elif ntScript[2] == anime:
                output += self.baseNest + '["%s", %s, anime, (\n'%(ntScript[0], ntScript[1] if ntScript[1].startswith("ltext(") else '"' + ntScript[1] + '"')
                for subScript in ntScript[3]:
                    if len(subScript) == 1:
                        output += self.baseNest + self.nestWord + '({\n'
                        for tgt in subScript[0].Keys:
                            output += self.baseNest + self.nestWord + self.nestWord + "'" + tgt + "': " + script2string(subScript[0][tgt]) + ",\n"
                        output += self.baseNest + self.nestWord + '}),\n'
                    else:
                        output += self.baseNest + self.nestWord + '({\n'
                        for tgt in subScript[0].Keys:
                            output += self.baseNest + self.nestWord + self.nestWord + "'" + tgt + "': " + script2string(subScript[0][tgt]) + ",\n"
                        output += self.baseNest + self.nestWord + '}, %.2f, \'%s\'),\n'%(subScript[1], subScript[2])
                output += self.baseNest + ')],\n'
            else:
                raise Exception("build_anime exception: Unknown ntScript format")
        # write to python or dump file
        if self.asTemplate and self.asEnable:
            return self.as_add_seq(output)
        else:
            if len(self.baseNest) >= len(self.nestWord):
                preNest = self.baseNest[:len(self.baseNest)-len(self.nestWord)]
            else:
                preNest = ""
            output = preNest + "[\n" + output + preNest + "]\n"
            try:
                import codecs
                f = codecs.open('dumppython.txt', 'a+', 'utf-8')
                f.write(output)
                f.write("\n")
                f.close()
                return "All script clips in anime buffer were dumped into dumppython.txt"
            except Exception as e:
                return "Write to dumppython.txt failed: " + str(e)
            
    def preview_anime_in_game(self, fromIndex = 0):
        # preview anime in game, set from clip index or from start
        # prepare preview scene
        if fromIndex == 0:
            prevSC = self.animeBuffer[0]
        else:
            prevSC = self.animeBuffer[fromIndex-1]
        self._previewStartScn = prevSC.finalScnStatus
        self._previewStartCam = prevSC.finalCamStatus
        self._previewFromIndex = fromIndex
        # backup old scene contents
        self._previewBackupNextTexts = self.game.nextTexts
        self._previewBackupEndNextTextFunc = self.game.endNextTextFunc
        self._previewBackupCurCharText = self.game.curCharText
        self._previewBackupVnText = self.game.vnText
        # start
        self._preview_anime_start()
        
    def _preview_anime_start(self):
        self.restore_scene_status(self._previewStartScn)
        self.restore_camera_status(self._previewStartCam)
        previewScript = self.output_anime_clips(self._previewFromIndex, False)
        scriptHelperGUIClose()
        self.game.texts_next(previewScript, self._preview_anime_end_choice)
        
    def _preview_anime_end_choice(self, game):
        scriptHelperGUIStart(game)
        scriptHelperGUIMessage("Preview is over", (("Again", _sh._preview_anime_start), ("Back to ScriptHelper", _sh._preview_anime_end, False), ("Back to Scene", _sh._preview_anime_end, True)))
        
    def _preview_anime_end(self, toScene):
        self.game.nextTexts = self._previewBackupNextTexts
        self.game.endNextTextFunc = self._previewBackupEndNextTextFunc
        self.game.set_text(self._previewBackupCurCharText, self._previewBackupVnText)
        if toScene:
            scriptHelperGUIClose()
    
    def output_anime_clips(self, fromIndex = 0, forDump = True):
        # merge all buffered anime clips to one list
        aoc = []
        lastClipType = None
        for i in range(fromIndex, len(self.animeBuffer)):
            clp = self.animeBuffer[i]
            clpInfo = clp.info
            if i == 0:
                # TODO: dump init status 
                continue
                
            # create localize string if needed
            if forDump and len(clpInfo.dialogue) > 0 and self.createLocalizeStringOnBuild:
                self.sd_init()
                newStrId = self.sd_find_or_create(clpInfo.dialogue)
                dlgString = "ltext(game, %d)"%newStrId
            else:
                dlgString = clpInfo.dialogue
            
            # choice dump type
            if clpInfo.dumpAsIndex == 0:
                # as a new act
                actScript = clp.nonAnimeScript
                if len(actScript) > 0:
                    ntScript = [clpInfo.speakerAlias, dlgString, act, actScript]
                    lastClipType = 0
                else:
                    ntScript = [clpInfo.speakerAlias, dlgString]
                    lastClipType = None
                aoc.append(ntScript)
                
            elif clpInfo.dumpAsIndex == 1 or (clpInfo.dumpAsIndex == 2 and lastClipType != 1):
                # as a new anime
                anmScript = []
                if len(clp.nonAnimeScript) > 0:
                    anmScript.append((clp.nonAnimeScript,))
                if len(clp.animeScript) > 0:
                    optScript = ScriptHelper.optimizeAnimeScript(clp.animeScript)
                    anmScript.append((optScript, clpInfo.animeDuration, self._animeStyleTexts[clpInfo.animeStyle]))
                if len(clp.tailScript) > 0:
                    anmScript.append((clp.tailScript,))
                anmScript = tuple(anmScript)
                if len(anmScript) > 0:
                    ntScript = [clpInfo.speakerAlias, dlgString, anime, anmScript]
                    lastClipType = 1
                else:
                    ntScript = [clpInfo.speakerAlias, dlgString]
                    lastClipType = 0
                aoc.append(ntScript)
                
            elif clpInfo.dumpAsIndex == 2 and lastClipType == 1:
                # as a sub anime
                anmScript = list(aoc[-1][3])
                if len(clpInfo.dialogue) > 0:
                    if not 'sys' in clp.nonAnimeScript:
                        clp.nonAnimeScript['sys'] = {}
                    clp.nonAnimeScript['sys']['text'] = (clpInfo.speakerAlias, dlgString)
                if len(clp.nonAnimeScript) > 0:
                    anmScript.append((clp.nonAnimeScript,))
                if len(clp.animeScript) > 0:
                    optScript = ScriptHelper.optimizeAnimeScript(clp.animeScript)
                    anmScript.append((optScript, clpInfo.animeDuration, self._animeStyleTexts[clpInfo.animeStyle]))
                if len(clp.tailScript) > 0:
                    anmScript.append((clp.tailScript,))
                anmScript = tuple(anmScript)
                aoc[-1][3] = anmScript
                lastClipType = 1
                
            else:
                raise Exception("Unexpected dump type %d and last dump type %d"%(clpInfo.dumpAsIndex, lastClipType))
                
        return aoc
        
    # scene helper
    def reload_scene(self):
        from os import path
        checkext = path.splitext(self.game.scenePNG)
        if checkext[1].lower() != ".png": self.game.scenePNG += ".png"
        fpath = path.join(self.game.get_scene_dir(), self.game.sceneDir + self.game.scenePNG)
        if path.isfile(fpath):
            print "Try reload " + self.game.sceneDir + self.game.scenePNG
            load_and_init_scene(self.game, self.game.scenePNG, self.init_anime_buffer)
        else:
            scriptHelperGUIMessage("File '%s' does not existed!"%fpath, ("OK",))
    
    def save_scene(self, showMessage = True):
        import os, shutil
        from UnityEngine import Application
        from Studio import Studio
        try:
            studio = Studio.Instance
            scene_dir = self.game.get_scene_dir()
            oldSceneFiles = os.listdir(scene_dir)
            studio.SaveScene()
            newSceneFiles = os.listdir(scene_dir)
            newFiles = []
            for sf in newSceneFiles:
                if not sf in oldSceneFiles:
                    #print "new save scene:", sf
                    newFiles.append(sf)
            if len(newFiles) == 0:
                raise Exception("Can not found new saved file...")
                
            checkext = os.path.splitext(self.game.scenePNG)
            if checkext[1].lower() != ".png": self.game.scenePNG += ".png"
            pngFile = None
            nonpngs = []
            for newFile in newFiles:
                if os.path.splitext(newFile)[1].lower() != ".png":
                    nonpngs.append(newFile)
                    continue
                else:
                    pngFile = newFile
                srcfile = os.path.join(scene_dir, newFile)
                dstfile = os.path.join(scene_dir, self.game.sceneDir, self.game.scenePNG)
                if os.path.isfile(dstfile):
                    bckfile = dstfile + ".bak"
                    shutil.move(dstfile, bckfile)
                shutil.move(srcfile, dstfile)
                
                # save ext data
                try:
                    if self.game.isStudioNEO:
                        from extplugins import HSStudioNEOExtSave
                        HSSNES = HSStudioNEOExtSave()
                        HSSNES.SaveExtData(dstfile)
                except Exception as e:
                    # ext data may be not necessary, continue on error
                    import traceback
                    traceback.print_exc()
                    print "[NOT IMPORTANT] Unable to save ext data"
                        
                # OK message
                msg = "Scene file '%s' saved!"%os.path.join(self.game.sceneDir, self.game.scenePNG)
            if pngFile == None:
                raise Exception("Can not found new saved PNG file...")
            else:
                oldPngNameNoExt = os.path.splitext(pngFile)[0]
                newPngNameNoExt = os.path.splitext(self.game.scenePNG)[0]
            for nonpng in nonpngs:
                if nonpng.startswith(oldPngNameNoExt):
                    srcfile = os.path.join(scene_dir, nonpng)
                    dstfile = os.path.join(scene_dir, self.game.sceneDir, nonpng.replace(oldPngNameNoExt, newPngNameNoExt))
                    print "save non-png file:", srcfile, "->", dstfile
                    if os.path.isfile(dstfile):
                        bckfile = dstfile + ".bak"
                        shutil.move(dstfile, bckfile)
                    shutil.move(srcfile, dstfile)
                else:
                    msg += "\nUnknown Non-PNG file detected: " + nonpng
        except Exception as e:
            msg = "Save Scene Failed: " + str(e)
            if not showMessage:
                raise Exception(msg)
        if showMessage:
            scriptHelperGUIMessage(msg)
        return msg
    
    def load_python(self, filename = ""):
        from os import path

        try:
            import codecs
            if filename == "" : filename = self.game.current_game
            pyPathname = path.join(self.game.pygamepath, filename)
            if not pyPathname.lower().endswith(".py") : pyPathname += ".py"
            
            #self.pythonContent = self.game.file_get_content(pyPathname)
            if path.exists(pyPathname):
                fp = codecs.open(pyPathname, "r", 'utf-8')
                self.pythonContent = fp.read()
                fp.close()
            else:
                raise Exception("file <%s> not found."%pyPathname)
                
            if len(self.pythonContent.strip()) == 0:
                self.asTemplate = False
                raise Exception("Empty python content")
            else:
                self.asTemplate = self.pythonContent.find("#-VNFA:BuildFromAutoScriptTemplate-#") > 0
                print "load python: %s (%dbytes), Template = %s"%(pyPathname, len(self.pythonContent), str(self.asTemplate))
        except Exception as e:
            self.pythonContent == ""
            print "load python failed:", e
    
    def save_python(self, showMessage = True):
        import shutil

        from os import path
        fp = None
        try:
            import codecs
            dstfile = path.join(self.game.pygamepath, self.game.current_game + ".py")
            if path.isfile(dstfile):
                bckfile = dstfile + ".bak"
                shutil.move(dstfile, bckfile)
            fp = codecs.open(dstfile, "w", 'utf-8')
            fp.write(self.pythonContent)
            fp.close()
            msg = "Python file '%s' saved!"%(self.game.current_game + ".py")
        except Exception as e:
            if fp != None: fp.close()
            msg = "Save Python Failed: " + str(e)
            if not showMessage:
                raise Exception(msg)
        if showMessage:
            scriptHelperGUIMessage(msg)
        return msg
    
    def tag_select(self):
        try:
            sel = HSNeoOCI.create_from_selected()
        except:
            sel = None
        if sel != None:
            for akey in self.game.scenedata.actors.Keys:
                if self.game.scenedata.actors[akey].objctrl == sel.objctrl:
                    scriptHelperGUIMessage("Selected character is already tagged as '%s'."%akey)
                    return
            for pkey in self.game.scenedata.props.Keys:
                if self.game.scenedata.props[pkey].objctrl == sel.objctrl:
                    scriptHelperGUIMessage("Selected item/folder is already tagged as '%s'."%pkey)
                    return
        if isinstance(sel, HSNeoOCIProp):
            scriptHelperGUIMessage("Tag '" + sel.text_name + "' as a prop:", (("Tag It", _sh._tag_select_do, sel), "Cancel"), {"ID": ["", "txt", 60, 60]})
        elif isinstance(sel, HSNeoOCIChar):
            scriptHelperGUIMessage("Tag '" + sel.text_name + "' as an actor:", (("Tag She/Him", _sh._tag_select_do, sel), "Cancel"), {"ID": ["", "txt", 60, 60], "Color": ["ffffff", "txt", 60, 60, "*Color of title, RRGGBB in Hex"], "Title": ["", "txt", 60, 60, "*Omit it to use char's own name"]})
        else:
            scriptHelperGUIMessage("Nothing selected or unknown object.\nSelect a character or an item/folder/route to add tag to.")
            
    def _tag_select_do(self, param):
        try:
            tagId = self.msgParam["ID"][0].strip()
            self._tag_check_id(tagId)
            if isinstance(param, HSNeoOCIChar):
                tagText = "-actor:" + tagId + ":" + self.msgParam["Color"][0]
                if self.msgParam["Title"][0].strip() != "":
                    tagText += ":" + self.msgParam["Title"][0]
                tagFolder = HSNeoOCIFolder.add(tagText)
                tagFolder.set_pos((param.pos.x, param.pos.y, param.pos.z))
                tagFolder.set_parent_treenodeobject(param.treeNodeObject.child[0].child[0])
            elif isinstance(param, HSNeoOCILight):
                tagText = "-propchild:" + tagId
                tagFolder = HSNeoOCIFolder.add(tagText)
                tagFolder.set_pos((param.pos.x, param.pos.y, param.pos.z))
                param.set_parent(tagFolder)
            elif isinstance(param, HSNeoOCIRoute):
                tagText = "-propgrandpa:" + tagId
                tagFolder = HSNeoOCIFolder.add(tagText)
                tagFolder.set_pos((param.pos.x, param.pos.y, param.pos.z))
                tagFolder.set_parent_treenodeobject(param.treeNodeObject.child[0])
            else:
                tagText = "-prop:" + tagId
                tagFolder = HSNeoOCIFolder.add(tagText)
                tagFolder.set_pos((param.pos.x, param.pos.y, param.pos.z))
                tagFolder.set_parent(param)
            register_actor_prop_by_tag(self.game)
        except Exception, e:
            scriptHelperGUIMessage("Fail to create TAG for %s: %s"%(param.text_name, str(e)), 3 if self.masterMode else ("OK",))
        
    def _tag_check_id(self, tagId):
        if len(tagId) == 0:
            raise Exception("Null ID")
        if tagId.isunicode():
            raise Exception("ID can not use UNICODE text")
        if tagId in self.game.scenedata.actors.Keys:
            raise Exception("ID '%s' is already used by an actor id"%tagId)
        if tagId in self.game.scenedata.props.Keys:
            raise Exception("ID '%s' is already used by a prop id"%tagId)
        if tagId in self.game.gdata.kfaManagedClips.Keys:
            raise Exception("ID '%s' is already used by a clip name"%tagId)
        if tagId == "sys":
            raise Exception("ID 'sys' is reserved for system")
        if tagId == "cam":
            raise Exception("ID 'cam' is reserved for camera")
        
    def sd_init(self):
        if not hasattr(self.game.scenedata, "strings"):
            register_string_resource(self.game)
        if hasattr(self, "sdSearchKeyword"):
            return
        self.sdSearchKeyword = ""
        self.sd_search()
        self.sdModifiedList = []
        
    def sd_search(self):
        self.sdSearchResult = []
        try:
            searchAsKey = int(self.sdSearchKeyword)
            if searchAsKey in self.game.scenedata.strings.Keys:
                self.sdSearchResult.append(searchAsKey)
        except:
            pass
        for key in self.game.scenedata.strings:
            if self.game.scenedata.strings[key].find(self.sdSearchKeyword) != -1 and not key in self.sdSearchResult:
                self.sdSearchResult.append(key)
        if len(self.sdSearchResult) > 0:
            self.sdIndex = 0
        else:
            self.sdIndex = -1
            
    def sd_new(self, id, text = ""):
        try:
            newID = int(id)
        except:
            newID = -1
        newID = self.sd_new_id(newID)
        self.game.scenedata.strings[newID] = text
        self.sdModifiedList.append(newID)
        self.sdSearchKeyword = str(newID)
        self.sd_search()
        return newID
        
    def sd_apply(self, id = -1):
        try:
            id = int(id)
            if id == -1:
                toApply = self.sdModifiedList
            elif id in self.game.scenedata.strings.Keys:
                toApply = [id]
            else:
                raise Exception("id %d is not in strings dictionary."%id)
            applied = []
            
            pFld = HSNeoOCIFolder.find_single("-strings-")
            if pFld == None:
                pFld = HSNeoOCIFolder.add("-strings-")
            for ta in toApply:
                tgtFlds = HSNeoOCIFolder.find_all_startswith(str(ta)+":")
                found = False
                for tgtFld in tgtFlds:
                    if tgtFld.treeNodeObject.parent == pFld.treeNodeObject:
                        tgtFld.name = str(ta) + ":" + self.game.scenedata.strings[ta]
                        applied.append(ta)
                        found = True
                        break
                if not found:
                    newFld = HSNeoOCIFolder.add(str(ta) + ":" + self.game.scenedata.strings[ta])
                    newFld.set_parent(pFld)
                    applied.append(ta)
            if len(applied) > 0:
                for ta in applied:
                    self.sdModifiedList.remove(ta)
                return "%d strings applied to -strings- folder. Save the scene!"%len(applied)
            else:
                return "No string applied!"
        except Exception as e:
            return "Apply string failed: " + str(e)
    
    def sd_find_or_create(self, text):
        # search for existed string
        for strId in self.game.scenedata.strings.Keys:
            if self.game.scenedata.strings[strId] == text:
                return strId
        # no match. create one
        strId = self.sd_new(-1, text)
        self.sd_apply(strId)
        return strId
    
    def sd_revert(self):
        register_string_resource(self.game)
        self.sdModifiedList = []
        self.sd_search()
        
    def sd_new_id(self, id):
        if id == -1 or id in _sh.game.scenedata.strings.Keys:
            idx = _sh.game.scenedata.strings.keys()
            idx.sort()
            if len(idx) > 0:
                return idx[-1] + 1
            else:
                return 1
        else:
            return id
        
    def sd_is_modified(self, id):
        try:
            id = int(id)
            return id in self.sdModifiedList
        except:
            return False
            
    def lh_init(self):
        self.sd_init()
        if self.pythonContent == "":
            self.load_python()
        if hasattr(self, "lhPrevVnText"):
            return
        self.lhPrevVnText = ""
        self.lhOrgTextType = "Unknown"
        self.lhOrgInput = ""
        self.lhTgtID = ""
        self.lhTgtInput = ""
        self.lhModifiedList = {}
    
    def lh_check_orgInput(self):
        pt = self.lhOrgInput.replace('\n', '\\n')
        ct = self.pythonContent.count('"' + pt + '"')
        if ct > 0:
            self.lhOrgTextType = '"PlainText" c=%d'%ct
            self.lh_set_id(-1)
            return
        ct = self.pythonContent.count("'" + pt + "'")
        if ct > 0:
            self.lhOrgTextType = "'PlainText' c=%d"%ct
            self.lh_set_id(-1)
            return
        for si in self.game.scenedata.strings.Keys:
            if self.lhOrgInput == self.game.scenedata.strings[si] or self.lhOrgInput == ltext(self.game, si):
                self.lhOrgInput = self.game.scenedata.strings[si]
                self.lhOrgTextType = "ltext id=%d"%si
                self.lh_set_id(si)
                return
        self.lhOrgTextType = "Unknown"
        
    def lh_set_id(self, id, offset = 0):
        try:
            id = int(id)
        except:
            id = -1
        if id in _sh.game.scenedata.strings.Keys:
            if offset != 0:
                ididxs = _sh.game.scenedata.strings.keys()
                ididxs.sort()
                ididx = ididxs.index(id)
                ididx = (ididx + offset) % len(ididxs)
                id = ididxs[ididx]
            self.lhTgtID = str(id)
            self.lhTgtInput = _sh.game.scenedata.strings[id]
            idModify = True
        elif offset != 0 and len(_sh.game.scenedata.strings) > 0:
            ididxs = _sh.game.scenedata.strings.keys()
            ididxs.sort()
            id = ididxs[0]
            self.lhTgtID = str(id)
            self.lhTgtInput = _sh.game.scenedata.strings[id]
            idModify = True
        else:
            self.lhTgtID = str(self.sd_new_id(id))
            self.lhTgtInput = ""
            idModify = False
        if idModify:
            self.lh_modify()
            
    def lh_update_tgtInput(self):
        try:
            id = int(self.lhTgtID)
        except:
            id = -1
        if not id in _sh.game.scenedata.strings.Keys:
            id = self.sd_new_id(id)
            self.lhTgtID = str(id)
        self.game.scenedata.strings[id] = self.lhTgtInput
        if not id in self.sdModifiedList:
            self.sdModifiedList.append(id)
            self.lh_modify()
    
    def lh_build_replace_source(self):
        if self.lhOrgTextType.startswith('"PlainText"'):
            return '"' + self.lhOrgInput + '"'
        elif self.lhOrgTextType.startswith("'PlainText'"):
            return "'" + self.lhOrgInput + "'"
        elif self.lhOrgTextType.startswith("ltext"):
            return "ltext(game, %s)"%(self.lhOrgTextType[9:])
        else:
            raise Exception("Unable to build replace source from unknown type")
    
    def lh_modify(self):
        rplSrcText = self.lh_build_replace_source()
        rplTgtText = "ltext(game, %s)"%(self.lhTgtID)
        if rplSrcText == rplTgtText:
            if rplSrcText in self.lhModifiedList.Keys:
                self.lhModifiedList.pop(rplSrcText)
        else:
            self.lhModifiedList[rplSrcText] = rplTgtText
        #print "lh_modify src: " + rplSrcText
        #print "lh_modify tgt: " + rplTgtText
        #print "lhModifiedList :" + str(self.lhModifiedList)
        #print "sdModifiedList :" + str(self.sdModifiedList)
        #print ""
        pass
    
    def lh_apply(self, id = -1):
        if id == -1:
            repLst = self.lhModifiedList.keys()
        else:
            id = int(id)
            repSrc = self.lh_build_replace_source()
            if repSrc in self.lhModifiedList:
                repLst = [repSrc]
            else:
                repLst = []
        for repSrc in repLst:
            repTgt = self.lhModifiedList.pop(repSrc)
            #print "replace [" + rplSrcText + "] to [" + rplTgtText + "]"
            if repSrc[0] == "'" or repSrc[0] == '"':
                repSrc = repSrc.replace("\n", "\\n")
            self.pythonContent = self.pythonContent.replace(repSrc, repTgt)
        if len(repLst) > 0:
            msg = "%d plain-text or ltext in python file is replaced. Save the python!"%len(repLst)
        else:
            msg = "No python text replaced."
        if id == -1 or id in self.sdModifiedList:
            msg += "\n" + self.sd_apply(id)
        return msg
        
    def lh_revert(self):
        self.sd_revert()
        self.load_python()
        self.lhModifiedList = {}
        self.lh_check_orgInput()
        
    def lh_is_modified(self, id):
        if self.sd_is_modified(id):
            return True
        else:
            rplSrcText = self.lh_build_replace_source()
            return rplSrcText in self.lhModifiedList.Keys
            
    def ch_init(self):
        if hasattr(self, "ch_sel_group"):
            return
        self.ch_base_actor = None
        self.ch_base_speed = None
        self.ch_base_pattern = None
        self.ch_partner_actor = None
        self.ch_partner_actor_sex = ()
        self.ch_ext_actor = []
        self.ch_set_ext_actor = False
        self.ch_sel_group = 0
        self.ch_sel_category = 0
        self.ch_sel_no = 0
        self.ch_gp_sclpos = Vector2(0, 0)
        self.ch_ct_sclpos = Vector2(0, 0)
        self.ch_no_sclpos = Vector2(0, 0)
        self.ch_group_texts = get_hanime_group_names(self.game)
        self.ch_category_texts = get_hanime_category_names(self.game, self.ch_sel_group)
        self.ch_no_texts = get_hanime_no_names(self.game, self.ch_sel_group, self.ch_sel_category)
    
    def ch_select_actor(self, aIndex):
        try:
            sel = HSNeoOCI.create_from_selected()
        except:
            sel = None
        if not isinstance(sel, HSNeoOCIChar):
            scriptHelperGUIMessage("Nothing selected or unknown object.\nSelect a character then click the select button.")
            return
        selactor = sel.as_actor
        if aIndex == 0:
            self.ch_base_actor = selactor
            self.ch_base_speed = selactor.get_anime_speed()
            self.ch_base_pattern = selactor.get_anime_pattern()
            self.ch_partner_actor_sex = selactor.h_partner(self.ch_sel_group, self.ch_sel_category)
            self.ch_check_partner()
        elif aIndex == 1:
            if self.ch_partner_actor_sex[0] != -1 and self.ch_partner_actor_sex[0] != selactor.sex:
                scriptHelperGUIMessage("Partner actor must be a %s"%("female" if self.ch_partner_actor_sex[0] else "male"))
            elif self.ch_base_actor.treeNodeObject == selactor.treeNodeObject:
                scriptHelperGUIMessage("%s is already setted as base actor"%(selactor.text_name))
            else:
                self.ch_partner_actor = selactor
        else:
            if self.ch_partner_actor_sex[aIndex-1] != -1 and self.ch_partner_actor_sex[aIndex-1] != selactor.sex:
                scriptHelperGUIMessage("Extra actor %d must be a %s"%(aIndex-1, "female" if self.ch_partner_actor_sex[aIndex-1] else "male"))
            elif self.ch_base_actor.treeNodeObject == selactor.treeNodeObject:
                scriptHelperGUIMessage("%s is already setted as base actor"%(selactor.text_name))
            elif self.ch_partner_actor.treeNodeObject != None and self.ch_partner_actor.treeNodeObject == selactor.treeNodeObject:
                scriptHelperGUIMessage("%s is already setted as parnter actor"%(selactor.text_name))
            else:
                self.ch_ext_actor[aIndex-2] = selactor
        
    def ch_check_partner(self):
        if self.ch_partner_actor != None:
            if self.ch_partner_actor.treeNodeObject == self.ch_base_actor.treeNodeObject:
                self.ch_partner_actor = None
            elif self.ch_partner_actor_sex[0] != -1 and self.ch_partner_actor_sex[0] != self.ch_partner_actor.sex:
                self.ch_partner_actor = None
        new_ext_actor = []
        for i in range(len(self.ch_partner_actor_sex) - 1):
            if len(self.ch_ext_actor) > i and self.ch_ext_actor[i] != None:
                ext_act = self.ch_ext_actor[i]
                if ext_act.treeNodeObject == self.ch_base_actor.treeNodeObject:
                    ext_act = None
                elif self.ch_partner_actor_sex[i+1] != -1 and self.ch_partner_actor_sex[i+1] != ext_act.sex:
                    ext_act = None
                new_ext_actor.append(ext_act)
            else:
                new_ext_actor.append(None)
        self.ch_ext_actor = new_ext_actor
        if len(self.ch_ext_actor) <= 1:
            self.ch_set_ext_actor = False
    
    def ch_change_group(self, newGroup):
        self.ch_sel_group = newGroup
        self.ch_sel_category = 0
        self.ch_sel_no = 0
        self.ch_category_texts = get_hanime_category_names(self.game, self.ch_sel_group)
        self.ch_no_texts = get_hanime_no_names(self.game, self.ch_sel_group, self.ch_sel_category)
        if self.ch_base_actor != None: 
            self.ch_partner_actor_sex = self.ch_base_actor.h_partner(self.ch_sel_group, self.ch_sel_category)
            self.ch_check_partner()
        
    def ch_change_category(self, newCat):
        self.ch_sel_category = newCat
        self.ch_sel_no = 0
        self.ch_no_texts = get_hanime_no_names(self.game, self.ch_sel_group, self.ch_sel_category)
        if self.ch_base_actor != None: 
            self.ch_partner_actor_sex = self.ch_base_actor.h_partner(self.ch_sel_group, self.ch_sel_category)
            self.ch_check_partner()
    
    def ch_update_speed(self, speed):
        self.ch_base_actor.set_anime_speed(speed)
        self.ch_base_speed = self.ch_base_actor.get_anime_speed()
        if self.ch_partner_actor != None:
            self.ch_partner_actor.set_anime_speed(speed)
        for extActor in self.ch_ext_actor:
            if extActor != None:
                extActor.set_anime_speed(speed)

    def ch_update_pattern(self, pattern):
        self.ch_base_actor.set_anime_pattern(pattern)
        self.ch_base_pattern = self.ch_base_actor.get_anime_pattern()
        if self.ch_partner_actor != None:
            self.ch_partner_actor.set_anime_pattern(pattern)
        for extActor in self.ch_ext_actor:
            if extActor != None:
                extActor.set_anime_pattern(pattern)
            
    def ch_start(self):
        hasExt = False
        for ext in self.ch_ext_actor:
            if ext != None:
                hasExt = True
                break
        if self.ch_base_actor != None and self.ch_partner_actor != None:
            print "start h_with (%d, %d, %d) as %s > %s > %s"%(self.ch_sel_group, self.ch_sel_category, self.ch_sel_no, self.ch_group_texts[self.ch_sel_group], self.ch_category_texts[self.ch_sel_category], self.ch_no_texts[self.ch_sel_no])
            if hasExt:
                self.ch_base_actor.h_with(self.ch_partner_actor, self.ch_sel_group, self.ch_sel_category, self.ch_sel_no, tuple(self.ch_ext_actor))
            else:
                self.ch_base_actor.h_with(self.ch_partner_actor, self.ch_sel_group, self.ch_sel_category, self.ch_sel_no)
            
    def ch_restart(self):
        if self.ch_base_actor != None:
            self.ch_base_actor.restart_anime()
        if self.ch_partner_actor != None:
            self.ch_partner_actor.restart_anime()
        for extActor in self.ch_ext_actor:
            if extActor != None:
                extActor.restart_anime()
        
    def ch_actor_name(self, index):
        if index == 0 and self.ch_base_actor != None:
            return self.ch_base_actor.text_name
        elif index == 1 and self.ch_partner_actor != None:
            return self.ch_partner_actor.text_name
        elif index > 1 and self.ch_ext_actor[index-2] != None:
            return self.ch_ext_actor[index - 2].text_name
        else:
            return "click to set"
            
    def ch_get_overall_anime_option_visible(self):
        chAllActors = [self.ch_base_actor, self.ch_partner_actor]
        chAllActors.extend(self.ch_ext_actor)
        for chActor in chAllActors:
            if chActor != None and chActor.get_anime_option_visible():
                return True
        return False
        
    def ch_set_overall_anime_option_visible(self, visible):
        chAllActors = [self.ch_base_actor, self.ch_partner_actor]
        chAllActors.extend(self.ch_ext_actor)
        for chActor in chAllActors:
            if chActor != None:
                chActor.set_anime_option_visible(visible)

    def ch_get_overall_shoes(self):
        chAllActors = [self.ch_base_actor, self.ch_partner_actor]
        chAllActors.extend(self.ch_ext_actor)
        for chActor in chAllActors:
            if chActor != None and chActor.get_cloth()[-1] == 0:
                return True
        return False
        
    def ch_set_overall_shoes(self, shoes):
        chAllActors = [self.ch_base_actor, self.ch_partner_actor]
        chAllActors.extend(self.ch_ext_actor)
        for chActor in chAllActors:
            if chActor != None:
                allcloth = list(chActor.get_cloth())
                allcloth[-1] = 0 if shoes else 2
                chActor.set_cloth(tuple(allcloth))

    def as_create_new(self):
        import shutil
        from os import path
        try:
            # check asInfo
            if len(self.asInfo.gameName) == 0 or len(self.asInfo.pythonName) == 0 or len(self.asInfo.sceneDir) == 0 or len(self.asInfo.scenePNG) == 0:
                raise Exception("Some basic infomation missed!")
            if self.asInfo.gameName.isunicode() or self.asInfo.pythonName.isunicode() or self.asInfo.sceneDir.isunicode() or self.asInfo.scenePNG.isunicode():
                raise Exception("Game name/scene dir/scene png/python file settings can not use UNICODE texts")
            # prepare basic infomation
            gameTitleLine = "#vngame;%s;%s"%(self.game.engine_name, self.asInfo.gameName)
            if self.asInfo.pythonName.lower().endswith(".py"): 
                aelf.asInfo.pythonName = self.asInfo.pythonName[:-3]
            if self.asInfo.sceneDir[-1] != "\\" and self.asInfo.sceneDir[-1] != "/":
                self.asInfo.sceneDir += "\\"
            if not self.asInfo.scenePNG.lower().endswith(".png"): 
                self.asInfo.scenePNG += ".png"
            if self.asInfo.createLocalizeString:
                self.sd_init()
                strId = self.sd_find_or_create(self.asInfo.defaultNextBtnText)
                defaultNextBtn = "ltext(game, %d)"%strId
                strId = self.sd_find_or_create(self.asInfo.defaultReloadBtnText)
                defaultReloadBtn = "ltext(game, %d)"%strId
                strId = self.sd_find_or_create(self.asInfo.defaultEndBtnText)
                defaultEndBtn = "ltext(game, %d)"%strId
                strId = self.sd_find_or_create(self.asInfo.defaultEndText)
                defaultEnd = "ltext(game, %d)"%strId
            else:
                defaultNextBtn = '"' + self.asInfo.defaultNextBtnText + '"'
                defaultReloadBtn = '"' + self.asInfo.defaultReloadBtnText + '"'
                defaultEndBtn = '"' + self.asInfo.defaultEndBtnText + '"'
                defaultEnd = '"' + self.asInfo.defaultEndText + '"'
            # read template and apply setting
            self.load_python("vnftemplate.py")
            self.pythonContent = self.pythonContent.replace("#-VNFA:GameTitle-#", gameTitleLine)
            self.pythonContent = self.pythonContent.replace("#-VNFA:SceneDir-#", '"' + self.asInfo.sceneDir.replace('\\', '\\\\') + '"')
            self.pythonContent = self.pythonContent.replace("#-VNFA:ScenePNG-#", '"' + self.asInfo.scenePNG + '"')
            self.pythonContent = self.pythonContent.replace("#-VNFA:EnableReload-#", str(self.asInfo.enableReload))
            self.pythonContent = self.pythonContent.replace("#-VNFA:EnableQuickReload-#", str(self.asInfo.enableQuickReload))
            self.pythonContent = self.pythonContent.replace("#-VNFA:HideWindow-#", str(self.asInfo.alwaysHideWindowInCameraAnime))
            self.game.isHideWindowDuringCameraAnimation = self.asInfo.alwaysHideWindowInCameraAnime
            self.pythonContent = self.pythonContent.replace("#-VNFA:LockWindow-#", str(self.asInfo.alwaysLockWindowInSceneAnime))
            self.game.isLockWindowDuringSceneAnimation = self.asInfo.alwaysLockWindowInSceneAnime
            self.pythonContent = self.pythonContent.replace("#-VNFA:SkinVersion-#", '"' + self.asInfo.skinVersion + '"')
            self.pythonContent = self.pythonContent.replace("#-VNFA:FakeLipSyncEnable-#", str(self.asInfo.fakeLipSyncEnable))
            self.game.isfAutoLipSync = self.asInfo.fakeLipSyncEnable
            self.pythonContent = self.pythonContent.replace("#-VNFA:FakeLipSyncVersion-#", '"' + self.asInfo.fakeLipSyncVersion + '"')
            self.game.fAutoLipSyncVer = self.asInfo.fakeLipSyncVersion
            self.pythonContent = self.pythonContent.replace("#-VNFA:FakeLipSyncReadingSpeed-#", str(self.asInfo.fakeLipSyncReadingSpeed))
            self.game.readingSpeed = self.asInfo.fakeLipSyncReadingSpeed
            self.pythonContent = self.pythonContent.replace("#-VNFA:DefaultNextText-#", defaultNextBtn)
            self.game.btnNextText = self.asInfo.defaultNextBtnText
            self.pythonContent = self.pythonContent.replace("#-VNFA:CreateString-#", str(self.asInfo.createLocalizeString))
            self.createLocalizeStringOnBuild = self.asInfo.createLocalizeString
            self.pythonContent = self.pythonContent.replace("#-VNFA:MasterMode-#", str(self.asInfo.masterMode))
            self.masterMode = self.asInfo.masterMode
            self.pythonContent = self.pythonContent.replace("#-VNFA:DefaultEndText-#", defaultEnd)
            self.pythonContent = self.pythonContent.replace("#-VNFA:DefaultRestartButton-#", defaultReloadBtn)
            self.pythonContent = self.pythonContent.replace("#-VNFA:DefaultEndButton-#", defaultEndBtn)
            # save python file
            self.game.current_game = self.asInfo.pythonName
            pyMsg = self.save_python(False)
            # Save scene PNG
            self.game.sceneDir = self.asInfo.sceneDir
            self.game.scenePNG = self.asInfo.scenePNG
            pngMsg = self.save_scene(False)
            # report
            msg = "New game <%s> for %s created!\n"%(self.asInfo.gameName, self.game.engine_name)
            msg += pyMsg + "\n"
            msg += pngMsg + "\n"
        except Exception as e:
            msg = "Fail to create new auto script: " + str(e)
        return msg
        
    def as_add_seq(self, scrString):
        try:
            if len(self.pythonContent) == 0:
                self.load_python()
            if not self.asTemplate: 
                raise Exception("Python contents error, or not a template script")
            # search for insert position
            spos = self.pythonContent.find("#-VNFA:seq:empty:")
            if spos == -1:
                raise "Can not find insert anchor start position!"
            epos = self.pythonContent.find("-#", spos + 17)
            if epos == -1:
                raise "Can not find insert anchor end position!"
            rplAnchor = self.pythonContent[spos : epos + 2]
            seqNo = int(self.pythonContent[spos + 17 : epos])
            seqNext = seqNo + 1
            #print "replace anchor = %s, no = %d"%(rplAnchor, seqNo)
            # new sequence
            newSeq = "#-VNFA:seq:start:%d-#\n"%(seqNo)
            newSeq += scrString
            newSeq += "        #-VNFA:seq:end:%d-#\n"%(seqNo)
            newSeq += "    ], toSeq%d)\n"%(seqNext)
            newSeq += "\n"
            newSeq += "def toSeq%d(game):\n"%(seqNext)
            newSeq += "    game.texts_next([\n"
            newSeq += "        #-VNFA:seq:empty:%d-#"%(seqNext)
            #print newSeq
            self.pythonContent = self.pythonContent.replace(rplAnchor, newSeq)
            return "All script clips in anime buffer were build into <color=#ff0000>toSeq%d()</color> function of current python contents.\nSave the python to save your work!"%seqNo
        except Exception as e:
            return "Add seq failed: " + str(e)
    
    def as_load(self):
        import ast
        try:
            if len(self.pythonContent) == 0:
                self.load_python()
            if not self.asTemplate:
                raise Exception("Python contents error, or not a template script")
            # search for insert position
            searchStartPos = 0
            while True:
                sspos = self.pythonContent.find("#-VNFA:seq:start:", searchStartPos)
                if sspos == -1:
                    break
                sepos = self.pythonContent.find("-#", sspos + 17)
                if sepos == -1:
                    raise Exception("Can not find start anchor end position!")
                seqNo = int(self.pythonContent[sspos + 17 : sepos])
                staAnchor = self.pythonContent[sspos : sepos + 2]
                endAnchor = "#-VNFA:seq:end:%d-#"%seqNo
                espos = self.pythonContent.find(endAnchor, sepos + 2)
                if espos == -1:
                    raise Exception("Can not find end anchor %s pair with start anchor %s!"%(endAnchor, staAnchor))
                searchStartPos = espos + len(endAnchor)
                print "found anchor pair %d"%seqNo
                
                scriptTexts = "[" + self.pythonContent[sepos + 2 : espos] + "]"
                game = self.game
                def ltext(game, no):
                    return "ltext(game, %d)"%no
                script = eval(scriptTexts)
                #print scriptTexts
                print script
                print script2string(script)

        except Exception as e:
            print "as_load failed: " + str(e)
    
    def as_rebuild_clips(self, clipString):
        try:
            if len(self.pythonContent) == 0:
                self.load_python()
            if not self.asTemplate: 
                raise Exception("Python contents error, or not a template script")
            # search for insert position
            spos = self.pythonContent.find("#-VNFA:KeyFrameClips:start-#")
            if spos == -1:
                raise Exception("Can not find keyframe clips insert anchor start position!")
            spos += len("#-VNFA:KeyFrameClips:start-#")
            epos = self.pythonContent.find("#-VNFA:KeyFrameClips:end-#")
            if epos == -1:
                raise Exception("Can not find keyframe clips insert anchor end position!")
            if spos > epos:
                raise Exception("Keyframe clips insert anchor start/end position mismatch!")
            # insert all
            self.pythonContent = self.pythonContent[:spos] + "\n" + clipString + self.pythonContent[epos:]
            return "All keyframe clips in keyframe clip manager were build into current python contents.\nSave the python to save your work!"
        except Exception as e:
            return "Add seq failed: " + str(e)

    # utilities
    def shrink_mode(self, shrink):
        from UnityEngine import Screen, Rect
        self.guiWidth = self.game.wwidth = self._shrinkWidth if shrink else self._normalWidth
        self.guiHeight = self.game.wheight = self._shrinkHeight if shrink else self._normalHeight
        self.game.windowRect = Rect(Screen.width / 2 - self.game.wwidth / 2, Screen.height - self.game.wheight - 10, self.game.wwidth, self.game.wheight)
    
    def clear_dialogue(self):        
        # clear dialogue
        self.curSCInfo.dialogue = ""
    
    def get_next_speaker(self, curSpeakAlias, next):
        # next from unknown speaker
        if curSpeakAlias != 's' and (not curSpeakAlias in self.game.scenedata.actors.Keys):
            return 's'
            
        # next from s or actor
        if curSpeakAlias == 's':
            if len(self.game.scenedata.actors) > 0:
                if next:
                    return self.game.scenedata.actors.Keys[0]
                else:
                    return self.game.scenedata.actors.Keys[-1]
            else:
                return 's'
        else:
            nextIndex = self.game.scenedata.actors.Keys.IndexOf(curSpeakAlias)
            if next:
                nextIndex += 1
            else:
                nextIndex -= 1
            if nextIndex in range(len(self.game.scenedata.actors)):
                return self.game.scenedata.actors.Keys[nextIndex]
            else:
                return 's'
    
    @staticmethod
    def diffSceneWithPrev(curScn, preScn):
        ds = {}
        for tgt in curScn.Keys:
            if tgt in preScn.Keys:
                for actFunc in curScn[tgt].Keys:
                    if (not actFunc in preScn[tgt].Keys) or (curScn[tgt][actFunc] != preScn[tgt][actFunc]):
                        if not tgt in ds.Keys:
                            ds[tgt] = {}
                        ds[tgt][actFunc] = curScn[tgt][actFunc]
            else:
                ds[tgt] = scriptCopy(curScn[tgt])
        return ds
        
    @staticmethod
    def optimizeAnimeScript(orgScript):
        optScript = {}
        try:
            for tgt in orgScript.Keys:
                optScript[tgt] = {}
                for actFunc in orgScript[tgt].Keys:
                    if (actFunc == "ik_set" or actFunc == "fk_set") and isinstance(orgScript[tgt][actFunc][0], dict):
                        # skip duplicated bone info
                        optFrom = {}
                        optTo = {}
                        for bi in orgScript[tgt][actFunc][0].Keys:
                            if orgScript[tgt][actFunc][0][bi] != orgScript[tgt][actFunc][1][bi]:
                                optFrom[bi] = orgScript[tgt][actFunc][0][bi]
                                optTo[bi] = orgScript[tgt][actFunc][1][bi]
                        optScript[tgt][actFunc] = (optFrom, optTo)
                    else:
                        optScript[tgt][actFunc] = orgScript[tgt][actFunc]
        except Exception as e:
            print "optimizeAnimeScript error:", e
        return optScript
        
    @staticmethod
    def get_cam_status():
        from Studio import Studio
        cdata = Studio.Instance.cameraCtrl.cameraData
        camDic = {}
        camDic['cam'] = {}
        camDic['cam']['goto_pos'] = (cdata.pos, cdata.distance, cdata.rotate)
        #print ("# other one: 'cam': {'goto_pos': ((%.3f, %.3f, %.3f), (%.3f, %.3f, %.3f), (%.3f, %.3f, %.3f))}"%(cdata.pos.x, cdata.pos.y, cdata.pos.z, cdata.distance.x, cdata.distance.y, cdata.distance.z, cdata.rotate.x, cdata.rotate.y, cdata.rotate.z))
        return camDic
    
    @staticmethod
    def get_scn_status(game):
        fs = {}
        if hasattr(game.scenedata, "actors"):
            for actorAlias in game.scenedata.actors.Keys:
                fs[actorAlias] = game.scenedata.actors[actorAlias].export_full_status()
        if hasattr(game.scenedata, "props"):
            for propAlias in game.scenedata.props.Keys:
                fs[propAlias] = game.scenedata.props[propAlias].export_full_status()
        if hasattr(game.gdata, "kfaManagedClips"):
            for clipName in game.gdata.kfaManagedClips.Keys:
                fs[clipName] = game.gdata.kfaManagedClips[clipName].export_full_status()
        fs['sys'] = export_sys_status(game)
        return fs

# global functions for ScriptHelper
def init_script_helper(game):
    global _sh
    game.onDumpSceneOverride = scriptHelperGUIStart
    _sh = ScriptHelper(game)
    return _sh
    
def toggle_devconsole(game):
    global _sh
    # initialize if not
    if _sh == None:
        _sh = ScriptHelper(game)
    # toggle script helper guiOnShow
    if _sh.guiOnShow:
        scriptHelperGUIClose()
    else:
        scriptHelperGUIStart(game)

# ----- some wraps for skin -----
def scriptHelperGUIStart(game):
    global _sh
    # register actor/prop if not
    if not hasattr(game.scenedata, "actors") or not hasattr(game.scenedata, "props"):
        register_actor_prop_by_tag(game)
    # init anime clip if not
    from vnanime import check_keyframe_anime, init_keyframe_anime
    if not check_keyframe_anime(game):
        init_keyframe_anime(game)

    _sh.game_skin_saved = game.skin
    _sh.guiOnShow = True
    scriptHelperGUIToSceen(_sh.guiScreenIndex) # to set game.windowName

    from skin_customwindow import SkinCustomWindow
    skin = SkinCustomWindow()
    skin.funcSetup = scriptHelperSkinSetup
    skin.funcWindowGUI = scriptHelperSkinWindowGUI
    game.skin_set(skin)

def scriptHelperSkinSetup(game):
    from UnityEngine import GUI, Screen, Rect
    game.wwidth = _sh.guiWidth
    game.wheight = _sh.guiHeight
    game.windowRect = Rect (Screen.width / 2 - game.wwidth / 2, Screen.height - game.wheight - 10, game.wwidth, game.wheight)
    #game.windowCallback = GUI.WindowFunction(scriptHelperWindowGUI)
    game.windowStyle = game.windowStyleDefault

def scriptHelperSkinWindowGUI(game,windowid):
    scriptHelperWindowGUI(windowid)

def scriptHelperGUIClose(toDevConsole = False):
    global _sh
    from UnityEngine import Screen, Rect
    _sh.guiOnShow = False
    _sh.game.windowName = ""
    _sh.game.isShowDevConsole = toDevConsole

    _sh.game.skin_set(_sh.game_skin_saved)

# ----- end wraps for skin ------

def scriptHelperGUIToSceen(toScreen):
    global _sh
    validScreen = {
        0: "Script Builder",
        0.1: "Script Builder",
        1: "Anime Buffer",
        2: "Key Frame Animation Clip Manager",
        3: "Scene Helper",
        10: "String Dictionary",
        11: "Localize Helper",
        12: "Couple Helper",
        13: "Couple Helper -adjust-",
        14: "VNActor Export Setting",
        15: "VNText Editor",
        16: "Anime Info",
        20: "New Game Wizard 1/2",
        21: "New Game Wizard 2/2",
        31: "Select Dump Target"
    }
    if toScreen in validScreen.Keys:
        _sh.guiScreenIndex = toScreen
        _sh.game.windowName = validScreen[toScreen]
    else:
        print "Invalid screen index:", toScreen
    
def scriptHelperGUIMessage(msg, action = 2, param = None):
    global _sh
    #print "scriptHelperGUIMessage from", _sh.guiScreenIndex, "\nmsg:", msg, "action:", action, "param:", param
    _sh.prevMsgGuiScreenIndex = _sh.guiScreenIndex
    _sh.msgTexts = msg
    _sh.msgParam = param
    if isinstance(action, tuple):
        _sh.msgAction = action
        _sh.guiScreenIndex = 99
    else:
        _sh.msgAction = None
        tid = _sh.game.set_timer(float(action), scriptHelperGUIMessageRtn)
        if tid != -1:
            _sh.guiScreenIndex = 99
        else:
            print "run out of timer"
            
def scriptHelperGUIMessageRtn(game = None):
    global _sh
    #print "scriptHelperGUIMessageRtn to", _sh.prevMsgGuiScreenIndex
    _sh.guiScreenIndex = _sh.prevMsgGuiScreenIndex
    
def scriptHelperWindowGUI(windowid):
    global _sh
    import UnityEngine
    from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
    from UnityEngine import Event, EventType, WaitForSeconds, GameObject
    from System import String, Array
    
    try:
        fullw = _sh.game.wwidth-30
        
        customButton = GUIStyle("button")
        customButton.fontSize = 14
        
        dumpTgtTexts = Array[String](("Diff", "All"))
        dumpAsTexts = Array[String](("new act", "new anime", "sub anime"))
        aniStyleTexts = Array[String](("Linear", "S-F", "F-S", "S-F3", "F-S3", "S-F4", "F-S4"))
        
        GUILayout.BeginVertical(GUILayout.Width(fullw))
        
        if _sh.guiScreenIndex == 0:     # screen No.0: Script Builder
        
            # dump scene setting
            GUILayout.BeginHorizontal()
            GUILayout.Label("Dump", GUILayout.Width(35))
            dumpTgtTexts[_sh.curSCInfo.dumpTypeIndex] = "<color=#00ffff>" + dumpTgtTexts[_sh.curSCInfo.dumpTypeIndex] + "</color>"
            _sh.curSCInfo.dumpTypeIndex = GUILayout.SelectionGrid(_sh.curSCInfo.dumpTypeIndex, dumpTgtTexts, 2, GUILayout.Width(80))
            GUILayout.Label("of", GUILayout.Width(15))
            if GUILayout.Button("<color=#00ffff>%s</color>"%("ALL objs" if _sh.curSCInfo.dumpTgts == None else "%d objs"%len(_sh.curSCInfo.dumpTgts)), GUILayout.Width(71)):
                scriptHelperGUIToSceen(31)
            GUILayout.Label("as", GUILayout.Width(15))
            dumpAsTexts[_sh.curSCInfo.dumpAsIndex] = "<color=#00ffff>" + dumpAsTexts[_sh.curSCInfo.dumpAsIndex] + "</color>"
            _sh.curSCInfo.dumpAsIndex = GUILayout.SelectionGrid(_sh.curSCInfo.dumpAsIndex, dumpAsTexts, 3, GUILayout.Width(230))
            GUILayout.EndHorizontal()
            
            # speaker/dialogue setting
            GUILayout.BeginHorizontal()
            if GUILayout.Button("<", GUILayout.Width(20)):
                _sh.curSCInfo.speakerAlias = _sh.get_next_speaker(_sh.curSCInfo.speakerAlias, False)
            if GUILayout.Button(">", GUILayout.Width(20)):
                _sh.curSCInfo.speakerAlias = _sh.get_next_speaker(_sh.curSCInfo.speakerAlias, True)
            _sh.curSCInfo.speakerAlias = GUILayout.TextField(_sh.curSCInfo.speakerAlias, GUILayout.Width(50))
            GUILayout.Label("says:", GUILayout.Width(35))
            _sh.curSCInfo.dialogue = GUILayout.TextField(_sh.curSCInfo.dialogue, GUILayout.Width(286))
            if GUILayout.Button("Clear", GUILayout.Width(45)):
                _sh.clear_dialogue()
            GUILayout.EndHorizontal()
                
            # scene anime detail
            if _sh.curSCInfo.dumpAsIndex != 0:
                GUILayout.BeginHorizontal()
                GUILayout.Label("Anime Duration:", GUILayout.Width(110))
                if GUILayout.Button("-1s", GUILayout.Width(50)):
                    _sh.curSCInfo.animeDuration -= 1
                if GUILayout.Button("-0.1s", GUILayout.Width(50)):
                    _sh.curSCInfo.animeDuration -= 0.1
                if _sh.curSCInfo.animeDuration < 0:
                    _sh.curSCInfo.animeDuration = 0
                durStr = GUILayout.TextField(str(_sh.curSCInfo.animeDuration), 10, GUILayout.Width(50))
                try:
                    _sh.curSCInfo.animeDuration = float(durStr)
                except ValueError:
                    print "invalid input in 'anime duration': %s, float expected."%durStr
                if GUILayout.Button("+0.1s", GUILayout.Width(50)):
                    _sh.curSCInfo.animeDuration += 0.1
                if GUILayout.Button("+1s", GUILayout.Width(50)):
                    _sh.curSCInfo.animeDuration += 1
                GUILayout.EndHorizontal()

                GUILayout.BeginHorizontal()
                GUILayout.Label("Anime Style:", GUILayout.Width(110))
                _sh.curSCInfo.animeStyle = GUILayout.SelectionGrid(_sh.curSCInfo.animeStyle, aniStyleTexts, 7)
                GUILayout.EndHorizontal()
            
            # camera anime setting
            GUILayout.BeginHorizontal()
            _sh.curSCInfo.includeCamera = GUILayout.Toggle(_sh.curSCInfo.includeCamera, "Include Camera", GUILayout.Width(fullw/3-2))
            if _sh.curSCInfo.includeCamera:
                _sh.curSCInfo.animateCamera = GUILayout.Toggle(_sh.curSCInfo.animateCamera, "Camera Anime", GUILayout.Width(fullw/3-2))
                if _sh.curSCInfo.animateCamera:
                    _sh.curSCInfo.useCameraTimer = GUILayout.Toggle(_sh.curSCInfo.useCameraTimer, "Use Camera Timer", GUILayout.Width(fullw/3-2)) or _sh.curSCInfo.dumpAsIndex == 0
            GUILayout.EndHorizontal()

            # camera anime detail
            if _sh.curSCInfo.includeCamera and _sh.curSCInfo.animateCamera and _sh.curSCInfo.useCameraTimer:
                GUILayout.BeginHorizontal()
                GUILayout.Label("Camera Duration:", GUILayout.Width(110))
                if GUILayout.Button("-1s", GUILayout.Width(50)):
                    _sh.curSCInfo.cameraDuration -= 1
                if GUILayout.Button("-0.1s", GUILayout.Width(50)):
                    _sh.curSCInfo.cameraDuration -= 0.1
                if _sh.curSCInfo.cameraDuration < 0:
                    _sh.curSCInfo.cameraDuration = 0
                durStr = GUILayout.TextField(str(_sh.curSCInfo.cameraDuration), 10, GUILayout.Width(50))
                try:
                    _sh.curSCInfo.cameraDuration = float(durStr)
                except ValueError:
                    print "invalid input in 'anime duration': %s, float expected."%durStr
                if GUILayout.Button("+0.1s", GUILayout.Width(50)):
                    _sh.curSCInfo.cameraDuration += 0.1
                if GUILayout.Button("+1s", GUILayout.Width(50)):
                    _sh.curSCInfo.cameraDuration += 1
                GUILayout.EndHorizontal()

                GUILayout.BeginHorizontal()
                GUILayout.Label("Camera Style:", GUILayout.Width(110))
                _sh.curSCInfo.cameraStyle = GUILayout.SelectionGrid(_sh.curSCInfo.cameraStyle, aniStyleTexts, 7)
                GUILayout.EndHorizontal()
                
            # clip setting
            GUILayout.BeginHorizontal()
            _sh.dumpClipToFile = GUILayout.Toggle(_sh.dumpClipToFile, "To file", GUILayout.Width(70))
            if _sh.curSCInfo.dumpAsIndex != 0:
                _sh.curSCInfo.hideWindowInAnime = GUILayout.Toggle(_sh.curSCInfo.hideWindowInAnime, "Hide window in anime", GUILayout.Width(150))
                if not _sh.curSCInfo.hideWindowInAnime:
                    _sh.curSCInfo.hideButtonInAnime = GUILayout.Toggle(_sh.curSCInfo.hideButtonInAnime, "Hide button in anime", GUILayout.Width(150))
            GUILayout.EndHorizontal()

            # VNSceneScript patch
            import vnframe_vnscenescripthelper # no reload due to performance issues
            vnframe_vnscenescripthelper.sshelper_onelineinterface(_sh)
            # VNSceneScript patch end
            
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("-", customButton, GUILayout.Width(20), GUILayout.Height(24)):
                _sh.shrink_mode(True)
                scriptHelperGUIToSceen(0.1)
            if GUILayout.Button("<color=#ff6666ff>%s</color>"%("Dump" if _sh.dumpClipToFile else "Build"), customButton, GUILayout.Width(100-24), GUILayout.Height(24)):
                _sh.append_clip()
                scriptHelperGUIMessage("Script%s added into anime buffer."%(" Dumped and " if _sh.dumpClipToFile else ""))
            if GUILayout.Button("Anime Buffer", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(1)
            if GUILayout.Button("Clip Manager", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(2)
            if GUILayout.Button("Scene Helper", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            if GUILayout.Button("Back", customButton, GUILayout.Width(50), GUILayout.Height(24)):
                scriptHelperGUIClose()
            GUILayout.EndHorizontal()
            
        elif _sh.guiScreenIndex == 0.1: # screen No.0.1: Script Builder shunk mode
            # Tail button
            GUILayout.BeginHorizontal()
            if GUILayout.Button("+", customButton, GUILayout.Width(20)):
                _sh.shrink_mode(False)
                scriptHelperGUIToSceen(0)
            if GUILayout.Button("<color=#ff6666ff>%s</color>"%("Dump Script" if _sh.dumpClipToFile else "Build Script")):
                _sh.append_clip()
                scriptHelperGUIMessage("Script%s added into anime buffer."%(" Dumped and " if _sh.dumpClipToFile else ""))
            GUILayout.EndHorizontal()
            
        elif _sh.guiScreenIndex == 1:   # screen No.1: Anime Buffer
            animeStopped = _sh.game.scnAnimeTID == -1
        
            # replay control
            GUILayout.BeginHorizontal()
            if GUILayout.Button("<", GUILayout.Width(20)):
                if _sh.animeBufferIndex > 1:
                    _sh.animeBufferIndex -= 1
            GUILayout.Label("%d/%d"%(_sh.animeBufferIndex, len(_sh.animeBuffer)-1), GUILayout.Width(40))
            if GUILayout.Button(">", GUILayout.Width(20)):
                if _sh.animeBufferIndex < len(_sh.animeBuffer) - 1:
                    _sh.animeBufferIndex += 1
            if GUILayout.Button("%s"%("Replay" if animeStopped else "Stop"), GUILayout.Width(70)):
                _sh.play_anime_clip("play" if animeStopped else "stop")
            if GUILayout.Button("To Start"):
                _sh.play_anime_clip("tostart")
            if GUILayout.Button("To End"):
                _sh.play_anime_clip("toend")
            if GUILayout.Button("Play & Next"):
                _sh.play_anime_clip("play_and_next")
            _sh.slowMotion = GUILayout.Toggle(_sh.slowMotion, "Slow Motion")
            GUILayout.EndHorizontal()
            
            if _sh.animeBufferIndex != 0:
                cInfo = _sh.animeBuffer[_sh.animeBufferIndex].info
                # anime speaker/dialogue info
                GUILayout.BeginHorizontal()
                if GUILayout.Button("<", GUILayout.Width(20)):
                    cInfo.speakerAlias = _sh.get_next_speaker(cInfo.speakerAlias, False)
                if GUILayout.Button(">", GUILayout.Width(20)):
                    cInfo.speakerAlias = _sh.get_next_speaker(cInfo.speakerAlias, True)
                cInfo.speakerAlias = GUILayout.TextField(cInfo.speakerAlias, GUILayout.Width(50))
                GUILayout.Label("says:", GUILayout.Width(35))
                cInfo.dialogue = GUILayout.TextField(cInfo.dialogue, GUILayout.Width(286))
                if GUILayout.Button("Clear", GUILayout.Width(45)):
                    cInfo.dialogue = ""
                GUILayout.EndHorizontal()
                
                # anime clip info and progress control
                if cInfo.dumpAsIndex != 0:
                    GUILayout.BeginHorizontal()
                    GUILayout.Label("Anime Duration:", GUILayout.Width(110))
                    if GUILayout.Button("-1s", GUILayout.Width(50)):
                        cInfo.animeDuration -= 1
                    if GUILayout.Button("-0.1s", GUILayout.Width(50)):
                        cInfo.animeDuration -= 0.1
                    if cInfo.animeDuration < 0:
                        cInfo.animeDuration = 0
                    durStr = GUILayout.TextField(str(cInfo.animeDuration), 10, GUILayout.Width(50))
                    try:
                        cInfo.animeDuration = float(durStr)
                    except ValueError:
                        print "invalid input in 'anime duration': %s, float expected."%durStr
                    if GUILayout.Button("+0.1s", GUILayout.Width(50)):
                        cInfo.animeDuration += 0.1
                    if GUILayout.Button("+1s", GUILayout.Width(50)):
                        cInfo.animeDuration += 1
                    subAnimeSet = GUILayout.Toggle(cInfo.dumpAsIndex == 2, "sub-anime")
                    cInfo.dumpAsIndex = 2 if subAnimeSet else 1
                    GUILayout.EndHorizontal()

                    GUILayout.BeginHorizontal()
                    GUILayout.Label("Anime Style:", GUILayout.Width(110))
                    cInfo.animeStyle = GUILayout.SelectionGrid(cInfo.animeStyle, aniStyleTexts, 7)
                    GUILayout.EndHorizontal()
                    
                    GUILayout.BeginHorizontal()
                    animeBigStep = cInfo.animeDuration / 10
                    animeLittleStep = cInfo.animeDuration / 100
                    if animeStopped and _sh.animeTime > cInfo.animeDuration:
                        _sh.animeTime = cInfo.animeDuration
                    animeTimePrev = float(_sh.animeTime)
                    if GUILayout.Button("<<", GUILayout.Width(25)) and animeStopped:
                        if _sh.animeTime > animeBigStep:
                            _sh.animeTime -= animeBigStep
                        else:
                            _sh.animeTime = 0
                    if GUILayout.Button("<", GUILayout.Width(20)) and animeStopped:
                        if _sh.animeTime > animeLittleStep:
                            _sh.animeTime -= animeLittleStep
                        else:
                            _sh.animeTime = 0
                    if animeStopped:
                        _sh.animeTime = GUILayout.HorizontalSlider(_sh.animeTime, 0, cInfo.animeDuration)
                    else:
                        if _sh.slowMotion:
                            aniDur = cInfo.animeDuration * _sh.slowMotionRate
                        else:
                            aniDur = cInfo.animeDuration
                        GUILayout.HorizontalSlider(_sh.animeTime, 0, aniDur)
                    if GUILayout.Button(">", GUILayout.Width(20)) and animeStopped:
                        if _sh.animeTime < cInfo.animeDuration - animeLittleStep:
                            _sh.animeTime += animeLittleStep
                        else:
                            _sh.animeTime = cInfo.animeDuration
                    if GUILayout.Button(">>", GUILayout.Width(25)) and animeStopped:
                        if _sh.animeTime < cInfo.animeDuration - animeBigStep:
                            _sh.animeTime += animeBigStep
                        else:
                            _sh.animeTime = cInfo.animeDuration
                    if animeStopped and (animeTimePrev - _sh.animeTime > 0.001 or animeTimePrev - _sh.animeTime < -0.001):
                        #print "anime time from", animeTimePrev, "to", _sh.animeTime
                        _sh.play_anime_clip("toposition")
                    GUILayout.EndHorizontal()
                else:
                    GUILayout.BeginHorizontal()
                    GUILayout.Label("*This clip has no scene anime script")
                    GUILayout.EndHorizontal()
            else:
                GUILayout.BeginHorizontal()
                GUILayout.Label("*No anime clip in buffer, use Script Builder first")
                GUILayout.EndHorizontal()

            # anime clip edit control
            if _sh.animeBufferIndex > 0:
                GUILayout.BeginHorizontal()
                if GUILayout.Button("Update", GUILayout.Width(fullw/3-2)):
                    if _sh.masterMode:
                       _sh.update_clip()
                    else:
                        scriptHelperGUIMessage("Update clip #%d to current scene status. And update next clip (if existed) to start from current scene. Click [Update] button to update with clip's current anime/camera settings. Or if you want new camera/scene settings, set in <b>Script Builder</b> and then click [Rebuild] button. Next clip (if existed) always be updated with its own camera/scene setting."%(_sh.animeBufferIndex), (("Update", _sh.update_clip, True), ("Rebuild", _sh.update_clip, False), "Cancel"))
                if GUILayout.Button("Insert", GUILayout.Width(fullw/3-2)):
                    if _sh.masterMode:
                       _sh.insert_clip()
                    else:
                        scriptHelperGUIMessage("Insert a clip at #%d, move current clip to next and update it to start from current status. Click [Insert] button to insert clip with current clip's anime/carema settings. Or you can set new camera/scene settings in <b>Script Builder</b>, and  then click [Build & Insert]."%(_sh.animeBufferIndex), (("Insert", _sh.insert_clip, True), ("Build & Insert", _sh.insert_clip, False), "Cancel"))
                if GUILayout.Button("Delete", GUILayout.Width(fullw/3-2)):
                    if _sh.masterMode:
                        _sh.delete_clip()
                    else:
                        scriptHelperGUIMessage("Use [Delete] button to delete current clip, and next clip (if existed) will be update to start from previous end state. Or [Roll back] button to delete not only current scene but also following clips, and set previous end state as the reference state.", (("Delete", _sh.delete_clip, False), ("Roll back", _sh.delete_clip, True), "Cancel"))
                GUILayout.EndHorizontal()
            
            # advanced control
            GUILayout.BeginHorizontal()
            if GUILayout.Button("Preview", GUILayout.Width(fullw/3-2)):
                if _sh.animeBufferIndex > 0:
                    if _sh.masterMode:
                        _sh.preview_anime_in_game(_sh.animeBufferIndex)
                    else:
                        scriptHelperGUIMessage("Preview the anime in game. Choice preview from beginning, or from current script clip.", (("Preview All", _sh.preview_anime_in_game), ("Preview From #%d"%(_sh.animeBufferIndex), _sh.preview_anime_in_game, _sh.animeBufferIndex), "Cancel"))
                else:
                    scriptHelperGUIMessage("No anime clip in buffer to preview, use Script Builder first.")
            if GUILayout.Button("Ref to current", GUILayout.Width(fullw/3-2)):
                if _sh.masterMode:
                    _sh.set_ref_scene()
                    scriptHelperGUIMessage("Reference set to current scene.")
                else:
                    scriptHelperGUIMessage("Set reference to current scene, so next builded script will take diff from current status. Reference status will not effect existed anime clips.", (("Set as Ref", _sh.set_ref_scene), "Cancel"))
            if GUILayout.Button("Rescan & Reset", GUILayout.Width(fullw/3-2)):
                if _sh.masterMode:
                    _sh.init_anime_buffer()
                    scriptHelperGUIMessage("All TAGs rescaned and anime buffer resetted.")
                else:
                    scriptHelperGUIMessage("Rescan the TAGs in the scene and reset anime buffer, set reference at the same time. Use this function when you want to start from beginning. All unsaved work lost!", (("Rescan & Reset", _sh.init_anime_buffer), "Cancel"))
            GUILayout.EndHorizontal()
            
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("Script Builder", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(0)
            if GUILayout.Button("<color=#ff6666ff>%s</color>"%("Build Anime" if _sh.asTemplate and _sh.asEnable else "Dump Anime"), customButton, GUILayout.Width(100), GUILayout.Height(24)):
                if len(_sh.animeBuffer) > 1:
                    msg = _sh.build_anime()
                    scriptHelperGUIMessage(msg)
                else:
                    scriptHelperGUIMessage("No anime clip in buffer to dump, use script builder first.")
            if GUILayout.Button("Clip Manager", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(2)
            if GUILayout.Button("Scene Helper", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            if GUILayout.Button("Back", customButton, GUILayout.Width(50), GUILayout.Height(24)):
                scriptHelperGUIClose()
            GUILayout.EndHorizontal()
        
        elif _sh.guiScreenIndex == 2:   # Screen No.2: Key Frame Animation Clip Manager
            from vnanime import kfam_GUI
            kfam_GUI(_sh)

        elif _sh.guiScreenIndex == 3:   # screen No.3: Scene Helper

            # scene file
            GUILayout.BeginHorizontal()
            GUILayout.Label("Scene File: (*for non-vnframe game, scene info may be wrong!)")
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("PNG:", GUILayout.Width(40))
            oldPngPathName = _sh.game.sceneDir + _sh.game.scenePNG
            newPngPathName = GUILayout.TextField(oldPngPathName, GUILayout.Width(120))
            if oldPngPathName != newPngPathName:
                from os import path
                pathname = path.split(newPngPathName)
                if pathname[0] != "":
                    _sh.game.sceneDir = pathname[0] + "\\"
                else:
                    _sh.game.sceneDir = ""
                _sh.game.scenePNG = pathname[1]
            if GUILayout.Button("Create TAG", GUILayout.Width(100)):
                _sh.tag_select()
            if len(_sh.game.scenePNG.strip()) > 0 and GUILayout.Button("Reload Scene", GUILayout.Width(100)):
                if _sh.masterMode:
                    _sh.reload_scene()
                else:
                    scriptHelperGUIMessage("Reload png file '%s' will revert all unsaved changes and reset anime buffer. Are you sure?"%newPngPathName, (("Reload", _sh.reload_scene), "Cancel"))
            if len(_sh.game.scenePNG.strip()) > 0 and GUILayout.Button("Save Scene", GUILayout.Width(100)):
                if _sh.masterMode:
                    _sh.save_scene()
                else:
                    scriptHelperGUIMessage("Save current scene and overwrite old scene file?\n(Old scene will be backuped to .bak file)", (("Save", _sh.save_scene), "Cancel"))
            GUILayout.EndHorizontal()
            # python file
            GUILayout.BeginHorizontal()
            if len(_sh.pythonContent) > 0:
                if _sh.asTemplate:
                    pyInfo = "[Loaded][AutoScript]"
                else:
                    pyInfo = "[Loaded]"
            else:
                pyInfo = "[N/A]"
            GUILayout.Label("Python script: " + pyInfo)
            if _sh.asTemplate:
                _sh.asEnable = GUILayout.Toggle(_sh.asEnable, "Enable Auto Script", GUILayout.Width(130))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("PY:", GUILayout.Width(40))
            _sh.game.current_game = GUILayout.TextField(_sh.game.current_game, GUILayout.Width(120))
            if GUILayout.Button("New Python", GUILayout.Width(100)):
                _sh.asInfo.pythonName = _sh.game.current_game
                _sh.asInfo.sceneDir = _sh.game.sceneDir
                _sh.asInfo.scenePNG = _sh.game.scenePNG
                scriptHelperGUIToSceen(20)
            if len(_sh.game.current_game) > 0 and GUILayout.Button(" Load Python " if _sh.pythonContent == "" else "Revert Python", GUILayout.Width(100)):
                if _sh.masterMode or _sh.pythonContent == "":
                    _sh.load_python()
                else:
                    scriptHelperGUIMessage("Revert python script to last saved status?\nUnsaved auto script or localization works will be lost!", (("Revert", _sh.load_python), "Cancel"))
            if len(_sh.game.current_game) > 0 and _sh.pythonContent != "" and GUILayout.Button("Save Python", GUILayout.Width(100)):
                if _sh.masterMode:
                    _sh.save_python()
                else:
                    scriptHelperGUIMessage("Save current python script and overwrite old python file?\n(Old python will be backuped to .bak file)", (("Save", _sh.save_python), "Cancel"))
            GUILayout.EndHorizontal()
            # localization
            GUILayout.BeginHorizontal()
            GUILayout.Label("Utilities:")
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("String Dictionary", GUILayout.Width(fullw/3-2)):
                _sh.sd_init()
                scriptHelperGUIToSceen(10)
            if GUILayout.Button("Localize Helper", GUILayout.Width(fullw/3-2)):
                _sh.lh_init()
                scriptHelperGUIToSceen(11)
            if GUILayout.Button("Couple Helper", GUILayout.Width(fullw/3-2)):
                _sh.ch_init()
                scriptHelperGUIToSceen(12)
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("VNActor Setting", GUILayout.Width(fullw/3-2)):
                scriptHelperGUIToSceen(14)
            if GUILayout.Button("VNText Editor", GUILayout.Width(fullw/3-2)):
                scriptHelperGUIToSceen(15)
            if GUILayout.Button("Char Anime Info", GUILayout.Width(fullw/3-2)):
                scriptHelperGUIToSceen(16)
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            _sh.createLocalizeStringOnBuild = GUILayout.Toggle(_sh.createLocalizeStringOnBuild, "Create localize string on script clip building.")
            GUILayout.EndHorizontal()
                        
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("Script Builder", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(0)
            if GUILayout.Button("Anime Buffer", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(1)
            if GUILayout.Button("Clip Manager", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                scriptHelperGUIToSceen(2)
            if GUILayout.Button("<color=#ff6666ff>Reset</color>", customButton, GUILayout.Width(100), GUILayout.Height(24)):
                from vnanime import init_keyframe_anime
                scriptHelperGUIMessage("Reset the keyframe clips, all unsaved work lost!", (("Reset keyframe clips", init_keyframe_anime, _sh.game), "Cancel"))
            if GUILayout.Button("Back", customButton, GUILayout.Width(50), GUILayout.Height(24)):
                scriptHelperGUIClose()
            GUILayout.EndHorizontal()

        elif _sh.guiScreenIndex == 10:  # Screen No.10: string dictionary
            
            # search
            GUILayout.BeginHorizontal()
            GUILayout.Label("Search:", GUILayout.Width(50))
            prevSearch = _sh.sdSearchKeyword
            _sh.sdSearchKeyword = GUILayout.TextField(_sh.sdSearchKeyword, GUILayout.Width(60))
            if GUILayout.Button("Clear", GUILayout.Width(40)):
                _sh.sdSearchKeyword = ""
            if _sh.sdSearchKeyword != prevSearch:
                _sh.sd_search()
            GUILayout.Label("Found:", GUILayout.Width(50))
            if len(_sh.sdSearchResult) > 0 and GUILayout.Button("<", GUILayout.Width(20)):
                if _sh.sdIndex == 0:
                    _sh.sdIndex = len(_sh.sdSearchResult) - 1
                else:
                    _sh.sdIndex -= 1
            GUILayout.Label("%d/%d"%(_sh.sdIndex + 1, len(_sh.sdSearchResult)), GUILayout.Width(50))
            if len(_sh.sdSearchResult) > 0 and GUILayout.Button(">", GUILayout.Width(20)):
                if _sh.sdIndex == len(_sh.sdSearchResult) - 1:
                    _sh.sdIndex = 0
                else:
                    _sh.sdIndex += 1
            if _sh.sdIndex >= 0:
                GUILayout.Label("ID = %d"%(_sh.sdSearchResult[_sh.sdIndex]))
                if _sh.sd_is_modified(_sh.sdSearchResult[_sh.sdIndex]) and GUILayout.Button("Apply"):
                    resMsg = _sh.sd_apply(_sh.sdSearchResult[_sh.sdIndex])
                    if _sh.masterMode:
                        scriptHelperGUIMessage(resMsg)
                    else:
                        scriptHelperGUIMessage(resMsg, ("OK",))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            if _sh.sdIndex >= 0:
                prevTexts = _sh.game.scenedata.strings[_sh.sdSearchResult[_sh.sdIndex]]
            else:
                prevTexts = ""
            inputTexts = GUILayout.TextArea(prevTexts, GUILayout.Width(fullw))
            if prevTexts != inputTexts and _sh.sdIndex >= 0:
                _sh.game.scenedata.strings[_sh.sdSearchResult[_sh.sdIndex]] = inputTexts
                if not _sh.sd_is_modified(_sh.sdSearchResult[_sh.sdIndex]):
                    _sh.sdModifiedList.append(_sh.sdSearchResult[_sh.sdIndex])
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Totally %d strings in dictionary, %d modified."%(len(_sh.game.scenedata.strings), len(_sh.sdModifiedList)))
            GUILayout.EndHorizontal()
            
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("New", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                _sh.sd_new(_sh.sdSearchKeyword)
            if GUILayout.Button("Apply All", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                resMsg = _sh.sd_apply()
                if _sh.masterMode:
                    scriptHelperGUIMessage(resMsg)
                else:
                    scriptHelperGUIMessage(resMsg, ("OK",))
            if GUILayout.Button("Revert All", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                if _sh.masterMode:
                    _sh.sd_revert()
                else:
                    scriptHelperGUIMessage("Revert to last applied status? All non-applied changes will be lost.", (("Revert", _sh.sd_revert), "Cancel"))
            if GUILayout.Button("Back", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            GUILayout.EndHorizontal()
        
        elif _sh.guiScreenIndex == 11:  # Screen No.11: localize helper
            # Org
            GUILayout.BeginHorizontal()
            GUILayout.Label("Original texts: %s"%(_sh.lhOrgTextType))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            if _sh.game.vnText != _sh.lhPrevVnText:
                _sh.lhOrgInput = _sh.lhPrevVnText = _sh.game.vnText
                _sh.lhTgtInput = ""
                _sh.lh_check_orgInput()
            usrOrgInput = GUILayout.TextArea(_sh.lhOrgInput, GUILayout.Width(fullw))
            if usrOrgInput != _sh.lhOrgInput:
                _sh.lhOrgInput = usrOrgInput
                _sh.lh_check_orgInput()
            GUILayout.EndHorizontal()
            
            # Tgt
            if _sh.lhOrgTextType[1:10] == "PlainText" or _sh.lhOrgTextType[:5] == "ltext":
                GUILayout.BeginHorizontal()
                GUILayout.Label("Select ID:", GUILayout.Width(70))
                if GUILayout.Button("<", GUILayout.Width(20)):
                    _sh.lh_set_id(_sh.lhTgtID, -1)
                usrTgtIndex = GUILayout.TextField(_sh.lhTgtID, GUILayout.Width(50))
                if usrTgtIndex != _sh.lhTgtID:
                    _sh.lh_set_id(usrTgtIndex)
                if GUILayout.Button(">", GUILayout.Width(20)):
                    _sh.lh_set_id(_sh.lhTgtID, +1)
                if GUILayout.Button("New", GUILayout.Width(50)):
                    _sh.lh_set_id(-1)
                if _sh.lh_is_modified(_sh.lhTgtID) and GUILayout.Button("Apply", GUILayout.Width(50)):
                    resMsg = _sh.lh_apply(_sh.lhTgtID)
                    if _sh.masterMode:
                        scriptHelperGUIMessage(resMsg)
                    else:
                        scriptHelperGUIMessage(resMsg, ("OK",))
                GUILayout.EndHorizontal()
                GUILayout.BeginHorizontal()
                usrTgtInput = GUILayout.TextArea(_sh.lhTgtInput, GUILayout.Width(fullw))
                if usrTgtInput != _sh.lhTgtInput:
                    _sh.lhTgtInput = usrTgtInput
                    _sh.lh_update_tgtInput()
                GUILayout.EndHorizontal()
            else:
                GUILayout.BeginHorizontal()
                GUILayout.Label("Unable to localize unknown string. Try input the plain text manually.")
                GUILayout.EndHorizontal()
            
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("Apply All", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                resMsg = _sh.lh_apply(-1)
                if _sh.masterMode:
                    scriptHelperGUIMessage(resMsg)
                else:
                    scriptHelperGUIMessage(resMsg, ("OK",))
            if GUILayout.Button("Revert All", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                if _sh.masterMode:
                    _sh.lh_revert()
                else:
                    scriptHelperGUIMessage("Revert to last applied status? All non-applied changes will be lost.", (("Revert", _sh.lh_revert), "Cancel"))
            if GUILayout.Button("Back", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            if GUILayout.Button("Back to Scene", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                scriptHelperGUIClose()
            GUILayout.EndHorizontal()
        
        elif _sh.guiScreenIndex == 12:  # Screen No.12: Couple helper
            # Actor select
            GUILayout.BeginHorizontal()
            if not _sh.ch_set_ext_actor:
                GUILayout.Label("Base Actor:", GUILayout.Width(70))
                if GUILayout.Button(_sh.ch_actor_name(0), GUILayout.Width(150)):
                    _sh.ch_select_actor(0)
                if len(_sh.ch_partner_actor_sex) > 0:
                    GUILayout.Label("Partner:", GUILayout.Width(50))
                    if GUILayout.Button(_sh.ch_actor_name(1), GUILayout.Width(150)):
                        _sh.ch_select_actor(1)
                if len(_sh.ch_partner_actor_sex) > 1:
                    if GUILayout.Button(">>", GUILayout.Width(30)):
                        _sh.ch_set_ext_actor = True
            else:
                if GUILayout.Button("<<", GUILayout.Width(30)):
                    _sh.ch_set_ext_actor = False
                for i in range(len(_sh.ch_partner_actor_sex)-1):
                    GUILayout.Label("Ext%d:"%(i+1), GUILayout.Width(40))
                    if GUILayout.Button(_sh.ch_actor_name(i+2), GUILayout.Width(100)):
                        _sh.ch_select_actor(i+2)
            GUILayout.EndHorizontal()
            
            # Speed and pattern
            GUILayout.BeginHorizontal()
            if _sh.ch_base_speed != None and _sh.ch_base_pattern != None:
                # Spd
                GUILayout.Label("Spd:", GUILayout.Width(30))
                newSpd = GUILayout.HorizontalSlider(_sh.ch_base_speed, 0, 3, GUILayout.Width(95))
                newSpdTxt = GUILayout.TextField("%.2f"%(newSpd), GUILayout.Width(30))
                try:
                    newSpd = float(newSpdTxt)
                    if newSpd != _sh.ch_base_speed:
                        _sh.ch_update_speed(newSpd)
                except:
                    pass
                # ptn
                if isinstance(_sh.ch_base_pattern, Vector2):
                    GUILayout.Label("Ptn:", GUILayout.Width(30))
                    newPtn1 = GUILayout.HorizontalSlider(_sh.ch_base_pattern.x, -1, 1, GUILayout.Width(95))
                    newPtnTxt1 = GUILayout.TextField("%.2f"%(newPtn1), GUILayout.Width(30))
                    newPtn2 = GUILayout.HorizontalSlider(_sh.ch_base_pattern.y, -1, 1, GUILayout.Width(95))
                    newPtnTxt2 = GUILayout.TextField("%.2f"%(newPtn2), GUILayout.Width(30))
                    try:
                        newPtn = Vector2(float(newPtn1), float(newPtn2))
                        if newPtn != _sh.ch_base_pattern:
                            _sh.ch_update_pattern(newPtn)
                    except:
                        pass
                else:
                    GUILayout.Label("Ptn:", GUILayout.Width(30))
                    newPtn = GUILayout.HorizontalSlider(_sh.ch_base_pattern, -1, 1, GUILayout.Width(95))
                    newPtnTxt = GUILayout.TextField("%.2f"%(newPtn), GUILayout.Width(30))
                    try:
                        newPtn = float(newPtnTxt)
                        if newPtn != _sh.ch_base_pattern:
                            _sh.ch_update_pattern(newPtn)
                    except:
                        pass
            else:
                GUILayout.Label("*Select an actor first")
            GUILayout.EndHorizontal()
            
            # Motion select
            GUILayout.BeginHorizontal()
            _sh.ch_gp_sclpos = GUILayout.BeginScrollView(_sh.ch_gp_sclpos, GUILayout.Width(100), GUILayout.Height(150))
            newGroup = GUILayout.SelectionGrid(_sh.ch_sel_group, Array[String](_sh.ch_group_texts), 1)
            if newGroup != _sh.ch_sel_group:
                _sh.ch_change_group(newGroup)
            GUILayout.EndScrollView()
            _sh.ch_ct_sclpos = GUILayout.BeginScrollView(_sh.ch_ct_sclpos, GUILayout.Width(190), GUILayout.Height(150))
            newCat = GUILayout.SelectionGrid(_sh.ch_sel_category, Array[String](_sh.ch_category_texts), 1)
            if newCat != _sh.ch_sel_category:
                _sh.ch_change_category(newCat)
            GUILayout.EndScrollView()
            _sh.ch_no_sclpos = GUILayout.BeginScrollView(_sh.ch_no_sclpos, GUILayout.Width(190), GUILayout.Height(150))
            newNo = GUILayout.SelectionGrid(_sh.ch_sel_no, Array[String](_sh.ch_no_texts), 1)
            if newNo != _sh.ch_sel_no:
                _sh.ch_sel_no = newNo
            GUILayout.EndScrollView()
            GUILayout.EndHorizontal()
            
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if _sh.ch_base_actor == None or _sh.ch_partner_actor == None:
                if GUILayout.Button("Help", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                    scriptHelperGUIMessage("Set base actor and partner to make them couple! Partner char will be move to base char. And anime speed, anime pattern will be synchronized too.\nSelect a charater in studio and press <b>'click to set'</b> button to set actor.", ("OK",))
                if GUILayout.Button("", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                    pass
                if GUILayout.Button("", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                    pass
            else:
                if GUILayout.Button("Start", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                    _sh.ch_start()
                if GUILayout.Button("Restart", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                    _sh.ch_restart()
                if GUILayout.Button("Adjust", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                    scriptHelperGUIToSceen(13)
            if GUILayout.Button("Back", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            GUILayout.EndHorizontal()
            
        elif _sh.guiScreenIndex == 13:  # Screen No.13: Couple helper - Adjust
            GUILayout.BeginHorizontal()
            GUILayout.Label("", GUILayout.Width(130))
            GUILayout.Label("Param1", GUILayout.Width(170))
            GUILayout.Label("Param2", GUILayout.Width(160))
            GUILayout.EndHorizontal()
            chAllActors = [_sh.ch_base_actor, _sh.ch_partner_actor]
            chAllActors.extend(_sh.ch_ext_actor)
            for i in range(len(chAllActors)):
                chActor = chAllActors[i]
                if chActor != None and chActor.isHAnime:
                    GUILayout.BeginHorizontal()
                    GUILayout.Label(_sh.ch_actor_name(i), GUILayout.Width(120))
                    oldParam = chActor.get_anime_option_param()
                    newParam1 = oldParam[0]
                    if GUILayout.Button("<", GUILayout.Width(20)):
                        if newParam1 > 0.1:
                            newParam1 -= 0.1
                        else:
                            newParam1 = 0
                    newParam1 = GUILayout.HorizontalSlider(newParam1, 0, 1, GUILayout.Width(90))
                    if GUILayout.Button(">", GUILayout.Width(20)):
                        if newParam1 < 0.9:
                            newParam1 += 0.1
                        else:
                            newParam1 = 1
                    GUILayout.Label("%.2f"%newParam1, GUILayout.Width(30))
                    newParam2 = oldParam[1]
                    if GUILayout.Button("<", GUILayout.Width(20)):
                        if newParam2 > 0.1:
                            newParam2 -= 0.1
                        else:
                            newParam2 = 0
                    newParam2 = GUILayout.HorizontalSlider(newParam2, 0, 1, GUILayout.Width(90))
                    if GUILayout.Button(">", GUILayout.Width(20)):
                        if newParam2 < 0.9:
                            newParam2 += 0.1
                        else:
                            newParam2 = 1
                    GUILayout.Label("%.2f"%newParam2, GUILayout.Width(30))
                    if newParam1 != oldParam[0] or newParam2 != oldParam[1]:
                        chActor.set_anime_option_param((newParam1, newParam2))
                    GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            allOption = _sh.ch_get_overall_anime_option_visible()
            newAllOption = GUILayout.Toggle(allOption, "Anime option item visible")
            if allOption != newAllOption:
                _sh.ch_set_overall_anime_option_visible(newAllOption)
            allShoes = _sh.ch_get_overall_shoes()
            newAllShoes = GUILayout.Toggle(allShoes, "Wear shoes")
            if allShoes != newAllShoes:
                _sh.ch_set_overall_shoes(newAllShoes)
            GUILayout.EndHorizontal()
        
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("Help", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                scriptHelperGUIMessage("Adjust anime option param to fix anime position mismatch.\nParam1 almost about height, Param2 almost about breast.\nIf the female wears high-heel, y position may be offseted. You need to take off it or adjust y position by youself.", ("OK",))
            if GUILayout.Button("", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                pass
            if GUILayout.Button("", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                pass
            if GUILayout.Button("Back", customButton, GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(12)
            GUILayout.EndHorizontal()
            
        elif _sh.guiScreenIndex == 14:  # Screen No.14: VNActor Setting
            # option list
            GUILayout.Label("Check the extend data you want to export with VNActor:")
            if not hasattr(_sh, "guiScrollPos14"):
                _sh.guiScrollPos14 = Vector2.zero
            _sh.guiScrollPos14 = GUILayout.BeginScrollView(_sh.guiScrollPos14, GUILayout.Height(170))
            for optname in get_ini_options():
                optdesp = get_ini_exportOptionDesp(optname)
                if optdesp == None:
                    optdesp = "<color=#00ff00>" + optname + "</color>"
                else:
                    optdesp = "<color=#00ff00>" + optname + "</color>: " + optdesp
                optold = is_ini_value_true(optname)
                optnew = GUILayout.Toggle(optold, optdesp)
                if optold != optnew:
                    set_ini_value(optname, optnew)
            GUILayout.EndScrollView()
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("OK", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            if GUILayout.Button("Readme", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                from vngameengine import get_engine_id
                msg = "VNActor extend export settings, which are wrtten in vnactor.ini file, can be modified here in run time. These settings affect the behavior of other components that depends on vnactor (such as VNFrame, VNAnime and SceneSaveState).\nTo keep you setting permanently, please edit them in vnactor.ini under <color=#00ff00>[" + get_engine_id() + "]</color> category and then click <Reload>."
                scriptHelperGUIMessage(msg, ("OK",))
            if GUILayout.Button("Reload", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                load_ini_file(True)
            GUILayout.EndHorizontal()

        elif _sh.guiScreenIndex == 15:  # Screen No.15: VNText Setting
            def backfunc():
                scriptHelperGUIToSceen(3)
            from vntext import vntxt_GUI
            vntxt_GUI(_sh.game, backfunc)

        elif _sh.guiScreenIndex == 16:  # Screen No.16: Anime Info
            from vnactor import Actor, Prop
            def getCurSelected(game):
                try:
                    sel = HSNeoOCI.create_from_selected()
                except:
                    return (None, None)
                if isinstance(sel, HSNeoOCIChar):
                    for actorId in game.scenef_get_all_actors().keys():
                        if game.scenef_get_actor(actorId).objctrl == sel.objctrl:
                            return (actorId, game.scenef_get_actor(actorId))
                    return (None, sel.as_actor)
                if isinstance(sel, HSNeoOCIProp):
                    for propId in game.scenef_get_all_props().keys():
                        if game.scenef_get_propf(propId).objctrl == sel.objctrl:
                            return (propId, game.scenef_get_propf(propId))
                    return (None, sel.as_prop)
                return (None, None)

            # print info
            (tid, obj) = getCurSelected(_sh.game)
            GUILayout.Label("Select a character to check anime info:")
            if obj and isinstance(obj, Actor):
                if tid:
                    tids = "(<color=#00ff00>%s</color>)"%tid
                else:
                    tids = "No registed"
                GUILayout.Label("Current select actor: %s %s"%(obj.text_name, tids))
                info, info2 = obj.get_anime_info_text()
                GUILayout.Label("  " + info)
                GUILayout.Label("  " + info2)
            elif obj and isinstance(obj, Prop):
                if tid:
                    tids = "(<color=#00ff00>%s</color>)"%tid
                else:
                    tids = "No registed"
                GUILayout.Label("Current select prop: %s %s"%(obj.text_name, tids))

            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                pass
            if GUILayout.Button("", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                pass
            if GUILayout.Button("Back", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            GUILayout.EndHorizontal()

        elif _sh.guiScreenIndex == 20:  # Screen No.20: New auto script wizard, basic setting
            GUILayout.BeginHorizontal()
            GUILayout.Label("Setup a new auto script game:")
            GUILayout.EndHorizontal()
            # python info
            GUILayout.BeginHorizontal()
            GUILayout.Label("Game name:", GUILayout.Width(100))
            _sh.asInfo.gameName = GUILayout.TextField(_sh.asInfo.gameName, GUILayout.Width(120))
            GUILayout.Label("Python file:", GUILayout.Width(100))
            _sh.asInfo.pythonName = GUILayout.TextField(_sh.asInfo.pythonName, GUILayout.Width(120))
            GUILayout.EndHorizontal()
            # Scene PNG info
            GUILayout.BeginHorizontal()
            GUILayout.Label("Scene folder:", GUILayout.Width(100))
            _sh.asInfo.sceneDir = GUILayout.TextField(_sh.asInfo.sceneDir, GUILayout.Width(120))
            GUILayout.Label("PNG file:", GUILayout.Width(100))
            _sh.asInfo.scenePNG = GUILayout.TextField(_sh.asInfo.scenePNG, GUILayout.Width(120))
            GUILayout.EndHorizontal()
            # Settings
            GUILayout.BeginHorizontal()
            _sh.asInfo.enableReload = GUILayout.Toggle(_sh.asInfo.enableReload, "Enable reload button at end of the game.")
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            _sh.asInfo.enableQuickReload = GUILayout.Toggle(_sh.asInfo.enableQuickReload, "Enable quick reload (Scene sould be initialized by script).")
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            _sh.asInfo.alwaysHideWindowInCameraAnime = GUILayout.Toggle(_sh.asInfo.alwaysHideWindowInCameraAnime, "Always hide window when camera anime is playing.")
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            _sh.asInfo.alwaysLockWindowInSceneAnime = GUILayout.Toggle(_sh.asInfo.alwaysLockWindowInSceneAnime, "Always hide buttons when scene anime is playing.")
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            _sh.asInfo.createLocalizeString = GUILayout.Toggle(_sh.asInfo.createLocalizeString, "Create localize string in scene file.")
            GUILayout.EndHorizontal()
            #GUILayout.BeginHorizontal()
            #_sh.asInfo.masterMode = GUILayout.Toggle(_sh.asInfo.masterMode, "I have mastered the ScriptHelper, so no prompt message needed!")
            #GUILayout.EndHorizontal()
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("Create New!", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                msg = _sh.as_create_new()
                scriptHelperGUIToSceen(3)
                scriptHelperGUIMessage(msg, ("OK",))
            if GUILayout.Button("More settings", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(21)
            if GUILayout.Button("Cancel", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            GUILayout.EndHorizontal()

        elif _sh.guiScreenIndex == 21:  # Screen No.21: New auto script wizard, more setting
            GUILayout.BeginHorizontal()
            GUILayout.Label("Setup a new auto script game: - More Settings -")
            GUILayout.EndHorizontal()
            # settings
            GUILayout.BeginHorizontal()
            GUILayout.Label("UI Skin:", GUILayout.Width(60))
            skinVersionTexts = Array[String](("skin_default", "skin_renpy"))
            skinVerIndex = Array.IndexOf(skinVersionTexts, _sh.asInfo.skinVersion)            
            skinVerIndex = GUILayout.SelectionGrid(skinVerIndex, skinVersionTexts, len(skinVersionTexts))
            _sh.asInfo.skinVersion = skinVersionTexts[skinVerIndex]
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Lip sync:", GUILayout.Width(60))
            _sh.asInfo.fakeLipSyncEnable = GUILayout.Toggle(_sh.asInfo.fakeLipSyncEnable, "Enable", GUILayout.Width(110))
            GUILayout.Label("Version:", GUILayout.Width(50))
            flsVersionTexts = Array[String](("v10", "v11"))            
            flsVerIndex = Array.IndexOf(flsVersionTexts, _sh.asInfo.fakeLipSyncVersion)
            flsVerIndex = GUILayout.SelectionGrid(flsVerIndex, flsVersionTexts, len(flsVersionTexts), GUILayout.Width(80))
            _sh.asInfo.fakeLipSyncVersion = flsVersionTexts[flsVerIndex]
            GUILayout.Label("Speed:", GUILayout.Width(45))
            rspd = GUILayout.TextField(str(_sh.asInfo.fakeLipSyncReadingSpeed), GUILayout.Width(40))
            try:
                _sh.asInfo.fakeLipSyncReadingSpeed = float(rspd)
            except:
                pass
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Default 'next' button text:", GUILayout.Width(170))
            _sh.asInfo.defaultNextBtnText = GUILayout.TextField(_sh.asInfo.defaultNextBtnText, GUILayout.Width(200))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Default 'reload' button text:", GUILayout.Width(170))
            _sh.asInfo.defaultReloadBtnText = GUILayout.TextField(_sh.asInfo.defaultReloadBtnText, GUILayout.Width(200))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Default 'end' button text:", GUILayout.Width(170))
            _sh.asInfo.defaultEndBtnText = GUILayout.TextField(_sh.asInfo.defaultEndBtnText, GUILayout.Width(200))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            GUILayout.Label("Default end scene text:", GUILayout.Width(170))
            _sh.asInfo.defaultEndText = GUILayout.TextField(_sh.asInfo.defaultEndText, GUILayout.Width(200))
            GUILayout.EndHorizontal()

            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("Create New!", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                msg = _sh.as_create_new()
                scriptHelperGUIToSceen(3)
                scriptHelperGUIMessage(msg, ("OK",))
            if GUILayout.Button("Basic settings", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(20)
            if GUILayout.Button("Cancel", GUILayout.Width(fullw/3-2), GUILayout.Height(24)):
                scriptHelperGUIToSceen(3)
            GUILayout.EndHorizontal()
        
        elif _sh.guiScreenIndex == 31:  # Screen No.31: Select dump target
            # Data
            sheight = 150
            sd = _sh.game.scenedata
            if not hasattr(sd, "localTgts"):
                sd.dtsActorPos = Vector2.zero
                sd.dtsPropPos = Vector2.zero
                sd.dtsClipPos = Vector2.zero
                if _sh.curSCInfo.dumpTgts != None:
                    sd.localTgts = copy.copy(_sh.curSCInfo.dumpTgts)
                else:
                    sd.localTgts = ["sys",]
                    for aid in sd.actors.keys():
                        sd.localTgts.append(aid)
                    for pid in sd.props.keys():
                        sd.localTgts.append(pid)
                    for cid in _sh.game.gdata.kfaManagedClips.keys():
                        sd.localTgts.append(cid)
            def checkId(tgtId):
                return sd.localTgts.count(tgtId) == 1
            def toggleId(tgtId, check):
                if checkId(tgtId) and not check:
                    sd.localTgts.remove(tgtId)
                if not checkId(tgtId) and check:
                    sd.localTgts.append(tgtId)
            def quitTgtSelect():
                del(sd.localTgts)
                scriptHelperGUIToSceen(0)
            # Title
            GUILayout.BeginHorizontal()
            GUILayout.Label("Select target objects to be dump into script:")
            GUILayout.EndHorizontal()
            # Actors, Props, Clips
            GUILayout.BeginHorizontal()
            GUILayout.BeginVertical(GUILayout.Width(180), GUILayout.Height(sheight))   # Actors
            GUILayout.Label("Actors:")
            sd.dtsActorPos = GUILayout.BeginScrollView(sd.dtsActorPos)
            if len(sd.actors):
                for aid in sd.actors.keys():
                    chk = GUILayout.Toggle(checkId(aid), "%s (%s)"%(sd.actors[aid].text_name, aid))
                    toggleId(aid, chk)
            else:
                GUILayout.Label("Not found")
            GUILayout.EndScrollView()
            GUILayout.EndVertical()
            GUILayout.BeginVertical(GUILayout.Width(180), GUILayout.Height(sheight))   # Props
            GUILayout.Label("Props:")
            sd.dtsPropPos = GUILayout.BeginScrollView(sd.dtsPropPos)
            if len(sd.props):
                for pid in sd.props.keys():
                    chk = GUILayout.Toggle(checkId(pid), "%s (%s)"%(sd.props[pid].text_name, pid))
                    toggleId(pid, chk)
            else:
                GUILayout.Label("Not found")
            GUILayout.EndScrollView()
            GUILayout.EndVertical()
            GUILayout.BeginVertical(GUILayout.Width(100), GUILayout.Height(sheight))   # Clips
            GUILayout.Label("Clips:")
            sd.dtsClipPos = GUILayout.BeginScrollView(sd.dtsClipPos)
            if len(_sh.game.gdata.kfaManagedClips):
                for cid in _sh.game.gdata.kfaManagedClips.keys():
                    chk = GUILayout.Toggle(checkId(cid), "%s"%(cid))
                    toggleId(cid, chk)
            else:
                GUILayout.Label("Not found")
            GUILayout.EndScrollView()
            GUILayout.EndVertical()
            GUILayout.EndHorizontal()
            # System
            GUILayout.BeginHorizontal()
            chk = GUILayout.Toggle(checkId("sys"), "Dump system settings. (such as map, bgm...)")
            toggleId("sys", chk)
            GUILayout.EndHorizontal()
            # Tail button
            GUILayout.FlexibleSpace()
            GUILayout.BeginHorizontal()
            if GUILayout.Button("Select (%d)"%len(sd.localTgts), GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                _sh.curSCInfo.dumpTgts = copy.copy(sd.localTgts)
                quitTgtSelect()
            if GUILayout.Button("All", GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                _sh.curSCInfo.dumpTgts = None
                quitTgtSelect()
            if GUILayout.Button("None", GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                sd.localTgts = []
            if GUILayout.Button("Back", GUILayout.Width(fullw/4-2), GUILayout.Height(24)):
                quitTgtSelect()
            GUILayout.EndHorizontal()

        elif _sh.guiScreenIndex == 99:
            # Screen No.99: Message Screen
            style = GUIStyle("label")
            style.richText = True
            style.fontSize = 18
            style.wordWrap = True
            
            # Message Texts
            GUILayout.BeginHorizontal()
            GUILayout.Label(_sh.msgTexts, style, GUILayout.Width(fullw))
            GUILayout.EndHorizontal()
            
            # Message Params
            if _sh.msgParam != None and isinstance(_sh.msgParam, dict):
                for pkey in _sh.msgParam:
                    keyName = pkey
                    value = _sh.msgParam[pkey][0]
                    valueType = _sh.msgParam[pkey][1]
                    keyWidth = _sh.msgParam[pkey][2]
                    valueWidth = _sh.msgParam[pkey][3]
                    if len(_sh.msgParam[pkey]) > 4:
                        comment = _sh.msgParam[pkey][4]
                    else:
                        comment = ""
                    if valueType == "txt":
                        GUILayout.BeginHorizontal()
                        GUILayout.Label(keyName, GUILayout.Width(keyWidth))
                        _sh.msgParam[pkey][0] = GUILayout.TextField(_sh.msgParam[pkey][0], GUILayout.Width(valueWidth))
                        GUILayout.Label(comment)
                        GUILayout.EndHorizontal()
                    else:
                        print "unsupported key type:", valueType
            
            # Tail button
            GUILayout.FlexibleSpace()
            if _sh.msgAction != None:
                GUILayout.BeginHorizontal()
                for ma in _sh.msgAction:
                    if isinstance(ma, tuple) and len(ma) > 1:
                        maText = str(ma[0])
                        maFunc = ma[1]
                        maParam = None if len(ma) == 2 else ma[2]
                    else:
                        maText = str(ma)
                        maFunc = None
                        maParam = None
                    if _sh.msgAction == None: break # prevent _sh.msgAction overwrite
                    if GUILayout.Button(maText, customButton, GUILayout.Width(fullw/len(_sh.msgAction)-2), GUILayout.Height(32)):
                        scriptHelperGUIMessageRtn(_sh.game)
                        if maFunc != None:
                            if maParam != None:
                                maFunc(maParam)
                            else:
                                maFunc()
                GUILayout.EndHorizontal()
            
        else:
            raise Exception("Unexpected guiScreenIndex = "+str(_sh.guiScreenIndex))
        
        GUILayout.EndVertical()
        GUI.DragWindow()
    except Exception as e:
        import traceback
        print "scriptHelperWindowGUI Exception:"
        traceback.print_exc()
        scriptHelperGUIClose()
        _sh.game.show_blocking_message_time("Script helper error: "+str(e))

def script2string(script):
    from UnityEngine import Vector3
    from System import Single, Byte
    if isinstance(script, list):
        ret = "["
        for subElm in script:
            ret += script2string(subElm) + ", "
        if len(ret) > 1:
            ret = ret[:len(ret)-2]
        ret += "]"
        return ret
    elif isinstance(script, tuple):
        ret = "("
        for subElm in script:
            ret += script2string(subElm) + ", "
        if len(script) > 1:
            ret = ret[:len(ret)-2]
        ret += ")"
        return ret
    elif isinstance(script, dict):
        ret = "{"
        for subKey in sorted(script.keys()):
            ret += script2string(subKey) + ": "
            ret += script2string(script[subKey]) + ", "
        if len(ret) > 1:
            ret = ret[:len(ret)-2]
        ret += "}"
        return ret
    elif isinstance(script, Vector3):
        #ret = "Vector3(%.3f, %.3f, %.3f)"%(script.x, script.y, script.z)
        ret = "(%.3f, %.3f, %.3f)"%(script.x, script.y, script.z)
        return ret
    elif isinstance(script, Vector2):
        ret = "(%.3f, %.3f)"%(script.x, script.y)
        return ret
    elif isinstance(script, Color):
        ret = "(%.2f, %.2f, %.2f, %.2f)"%(script.r, script.g, script.b, script.a)
        return ret
    elif isinstance(script, Quaternion):
        ret = "(%.3f, %.3f, %.3f, %.3f)"%(script.x, script.y, script.z, script.w)
        return ret
    elif isinstance(script, str):
        if script.startswith("ltext(") and script.endswith(")"):    # special for ltext() function
            return script
        else:
            return "'" + script + "'"
    elif isinstance(script, float) or isinstance(script, Single):        
        return "%.3f"%script
    elif isinstance(script, bool):
        if script:
            return '1'
        else:
            return '0'
    elif isinstance(script, int) or isinstance(script, Byte):
        return str(script)
    elif script == act:
        return 'act'
    elif script == anime:
        return 'anime'
    elif script == None:
        return 'None'
    else:
        raise Exception("script2string: Unknown type " + str(type(script)) +  " of " + str(script))

def scriptCopy(script):
    if isinstance(script, list):
        ret = []
        for subElm in script:
            ret.append(scriptCopy(subElm))
        return ret
    elif isinstance(script, tuple):
        ret = []
        for subElm in script:
            ret.append(scriptCopy(subElm))
        return tuple(ret)
    elif isinstance(script, dict):
        ret = {}
        for subKey in script.keys():
            ret[subKey] = scriptCopy(script[subKey])
        return ret
    elif isinstance(script, Vector3):
        ret = Vector3(script.x, script.y, script.z)
        return ret
    elif isinstance(script, Vector2):
        ret = Vector2(script.x, script.y)
        return ret
    elif isinstance(script, Color):
        ret = Color(script.r, script.g, script.b, script.a)
        return ret
    elif isinstance(script, Quaternion):
        ret = Quaternion(script.x, script.y, script.z, script.w)
        return ret
    else:
        return script


