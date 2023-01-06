#===============================================================================================
# Key frame based animator framework
# v1.0 (countd360)
# v1.1 (countd360)
# - fix an optimize bug
# v1.1.2 (countd360)
# - fix ClipKeyFrame load issue.
# v1.1.3 (countd360)
# - Remove utf-8 dependence.
# v1.2 (countd360)
# - Export clips into scene, so clips can be save with PNG file.
# - Auto and manual load in-scene clips.
# - Stop update clip aftet last keyframe.
# v1.3 (countd360)
# - A new clip optimization UI
# - Clips sorted by priority first and then by clip's name
# - Status list of actor/prop/system can be sorted/translated/colored by setting in vnactor.ini
# - Adjust of curve data applied automatically, no 'update' button click needed.
# v1.3.1 (Joan)
# - includes Joan fix for VideoExport plugin
# v1.4 (countd360)
# - fix anime speed save bug
# - fix seek bar time display bug
# - work with vnactor v3.9 
# v1.5 (countd360)
# - update to new event_reg_listener/event_unreg_listener function
# - fix copy/parse keyframe when playing bug
# v1.5.1 (countd360)
# - fix AIPE support bug
# v1.6 (countd360)
# - support auto run when scene loaded/imported
# - merge clips into one "-keyframeclips" folder when imported
# - optimized setting export to scene
# v1.6.1 (countd360)
# - fix error message on load ext file fail.
#===============================================================================================
import time
import math
import traceback
import copy
from os import path
from UnityEngine import Vector2, Vector3, Color
from vngameengine import HSNeoOCI, HSNeoOCIChar, HSNeoOCIProp, HSNeoOCIFolder
from vnactor import cam_act_funcs, sys_act_funcs, char_act_funcs, prop_act_funcs, export_sys_status
from vnframe import act, paramInterpolater, register_actor_prop_by_tag, scriptHelperGUIToSceen, scriptHelperGUIMessage, scriptHelperGUIClose, script2string, scriptCopy

# system functions
def init_keyframe_anime(game):
    if not check_keyframe_anime(game):
        # clean up hook
        game.event_unreg_listener("update", update_keyframe_anime, "vnanime_update")
        # register update function
        game.event_reg_listener("update", update_keyframe_anime, "vnanime_update")
    # new clips
    game.gdata.kfaManagedClips = {}
    game.gdata.kfaSortedClips = []
    # delete manager temp data
    if hasattr(game.scenedata, "kfamSelectedClipIndex"):
        del game.scenedata.kfamSelectedClipIndex
    # try import from scene
    importAllClipsFromScene(game)
    
def clear_keyframe_anime(game):
    game.event_unreg_listener("update", update_keyframe_anime, "vnanime_update")
    if check_keyframe_anime(game):
        game.gdata.kfaManagedClips = None
        game.gdata.kfaSortedClips = None
        
def check_keyframe_anime(game):
    return hasattr(game.gdata, "kfaManagedClips") and game.gdata.kfaManagedClips != None

def update_keyframe_anime(game, evid, param):
    for clip in game.gdata.kfaSortedClips:
        clip.update(game)

def merge_imported_clips(game):
    clipbases = HSNeoOCIFolder.find_all_startswith("-keyframeclips:")
    if len(clipbases) <= 1:
        # no need to merge
        return
    # run register
    register_actor_prop_by_tag(game)
    # build base info
    baseFld = clipbases[0]
    clipids = []
    for clpFld in baseFld.treeNodeObject.child:
        cspt = clpFld.textName.split(":")
        if len(cspt) != 3 or cspt[0] != "-clip":
            continue
        cid = cspt[1]
        clipids.append(cid)
    # merge imported info
    for i in range(1, len(clipbases)):
        impBaseFld = clipbases[i]
        for clpFld in impBaseFld.treeNodeObject.child:
            cspt = clpFld.textName.split(":")
            if len(cspt) != 3 or cspt[0] != "-clip":
                continue
            cid = cspt[1]
            try:
                if cid in clipids:
                    # need rename
                    while cid in clipids:
                        cid += "_import"
                    clpScp = eval(clpFld.child[0].textName)
                    tempClp = KeyFrameClip(game, clpScp)
                    tempClp.name = cid
                    clpSetting = tempClp.exportSettingForScene()
                    print "VNAnime Info: import and renamed clip:%s"%cid
                else:
                    # just move
                    clpSetting = clpFld.child[0].textName
                    print "VNAnime Info: import clip:%s"%cid
                clpFld = HSNeoOCIFolder.add("-clip:%s:0"%cid)
                clpFld.set_parent(baseFld)
                clpData = HSNeoOCIFolder.add(clpSetting)
                clpData.set_parent(clpFld)
            except Exception as e:
                print "Error in import %s: %s"%(cspt[1], str(e))
        # remove imported clip base
        impBaseFld.delete()

def start_autorun_clips(game):
    for clip in game.gdata.kfaSortedClips:
        if clip.autorun:
            clip.play()
        
# clip control functions
def kfa_register(game, clip):
    try:
        game.gdata.kfaManagedClips[clip.name] = clip
        game.gdata.kfaSortedClips = game.gdata.kfaManagedClips.values()
        game.gdata.kfaSortedClips.sort(key=KeyFrameClip.sortByPriority)
    except Exception as e:
        traceback.print_exc()
        print "Fail to register clip:", e

def kfa_import(game, clipScript):
    try:
        newClip = KeyFrameClip(game, clipScript)
        game.gdata.kfaManagedClips[newClip.name] = newClip
        game.gdata.kfaSortedClips = game.gdata.kfaManagedClips.values()
        game.gdata.kfaSortedClips.sort(key=KeyFrameClip.sortByPriority)
    except Exception as e:
        traceback.print_exc()
        print "Fail to import clip:", e

def kfa_remove(game, clipName):
    try:
        clip = game.gdata.kfaManagedClips.pop(clipName)
        game.gdata.kfaSortedClips = game.gdata.kfaManagedClips.values()
        game.gdata.kfaSortedClips.sort(key=KeyFrameClip.sortByPriority)
    except Exception as e:
        traceback.print_exc()
        print "Fail to remove clip:", e

def kfa_rename(game, oldName, newName):
    try:
        clip = game.gdata.kfaManagedClips.pop(oldName)
        game.gdata.kfaManagedClips[newName] = clip
        clip.name = newName
    except Exception as e:
        traceback.print_exc()
        print "Fail to rename clip <%s> to <%s>: %s"%(oldName, newName, str(e))

def kfa_resort(game, clipName, priority):
    try:
        clip = game.gdata.kfaManagedClips[clipName]
        clip.priority = priority
        game.gdata.kfaSortedClips.sort(key=KeyFrameClip.sortByPriority)
    except Exception as e:
        traceback.print_exc()
        print "Fail to resort clip <%s>: %s"%(clipName, str(e))

def kfa_retype(game, clipName, animeType):
    try:
        clip = game.gdata.kfaManagedClips[clipName]
        #
        clip.animeType = animeType
    except Exception as e:
        traceback.print_exc()
        print "Fail to resort clip <%s>: %s"%(clipName, str(e))
    
def kfa_play(game, clipName, forceLoop=None):
    try:
        game.gdata.kfaManagedClips[clipName].play(forceLoop)
    except Exception as e:
        traceback.print_exc()
        print "Fail to play clip <%s>: %s"%(clipName, str(e))

def kfa_playAll(game):
    for clip in game.gdata.kfaSortedClips:
        clip.play()
        
def kfa_pause(game, clipName):
    try:
        game.gdata.kfaManagedClips[clipName].pause()
    except Exception as e:
        traceback.print_exc()
        print "Fail to pause clip <%s>: %s"%(clipName, str(e))
        
def kfa_pauseAll(game):
    for clip in game.gdata.kfaSortedClips:
        clip.pause()
    
def kfa_stop(game, clipName):
    try:
        game.gdata.kfaManagedClips[clipName].stop()
    except Exception as e:
        traceback.print_exc()
        print "Fail to stop clip <%s>: %s"%(clipName, str(e))
        
def kfa_stopAll(game):
    for clip in game.gdata.kfaSortedClips:
        clip.stop()
        
def kfa_seek(game, clipName, frameNo):
    try:
        game.gdata.kfaManagedClips[clipName].seek(frameNo)
    except Exception as e:
        traceback.print_exc()
        print "Fail to seek clip <%s> to %d: %s"%(clipName, frameNo, str(e))

def kfa_rewindAll(game):
    for clip in game.gdata.kfaSortedClips:
        clip.seek(0)


# math work
def cbi_s(p1, p2, t):
    a = 1 - 3*p2 + 3*p1
    b = 3*(p2 - 2*p1)
    c = 3*(p1)
    return a*t*t*t + b*t*t + c*t

def root3(x):
    if x < 0:
        y = math.pow(-x, 0.3333333333333333333)
        return -y
    else:
        y = math.pow(x, 0.3333333333333333333)
        return y
    
def cbi_ts(p1, p2, y):
    a = 1 - 3*p2 + 3*p1
    b = 3*(p2 - 2*p1)
    c = 3*(p1)
    d = - y
    #y = a*t*t*t + b*t*t + c*t + d
    #print ("a=", a, "b=", b, "c=", c, "d=", d)
    if a == 0:
        if b == 0:
            #print ("linear function")
            return y
        else:
            #print ("square function")
            D = c*c - 4*b*d
            if D < 0:
                print ("FAIL to solve square: D < 0!? %f %f %f"%(b, c, d))
                return 0
            else:
                X1 = (-c + math.sqrt(D))/(2*b)
                X2 = (-c - math.sqrt(D))/(2*b)
                if X1 >= 0 and X1 <= 1:
                    return X1
                elif X2 >= 0 and X2 <= 1:
                    return X2
                else:
                    print ("FAIL to solve square: %f %f"%(X1, X2))
                    return X2
    A = b*b - 3*a*c
    B = b*c - 9*a*d
    C = c*c - 3*b*d
    D = B*B - 4*A*C
    #print ("A=", A, "B=", B, "C=", C, "D=", D)
    if A == 0 and B == 0:
        X = -b/(3*a)
        #print ("ptn1:", X)
        return X
    if D > 0:
        Y1 = A*b + 3*a*(-B + math.sqrt(D))/2
        Y2 = A*b + 3*a*(-B - math.sqrt(D))/2
        X = (-b - (root3(Y1) + root3(Y2)))/(3*a)
        #print ("ptn2:", X)
        return X
    if D == 0:
        K = B/A
        X1 = -b/a + K
        X2 = X3 = -K/2
        #print ("ptn3:",X1,X2,X3)
        if X1 >= 0 and X1 <= 1:
            return X1
        elif X2 >= 0 and X2 <= 1:
            return X2
        elif X3 >= 0 and X3 <= 1:
            return X3
        else:
            print("FAIL to solve ptn3: (%f, %f, %f)"%(X1,X2,X3))
            return X3
    if D < 0:
        T = (2*A*b - 3*a*B)/(2*math.sqrt(A*A*A))
        theta = math.acos(T)/3
        X1 = (-b - 2*math.sqrt(A)*math.cos(theta))/(3*a)
        X2 = (-b + math.sqrt(A)*(math.cos(theta) + 1.732*math.sin(theta)))/(3*a)
        X3 = (-b + math.sqrt(A)*(math.cos(theta) - 1.732*math.sin(theta)))/(3*a)
        #print ("ptn4:",X1,X2,X3)
        if X1 >= 0 and X1 <= 1:
            return X1
        elif X2 >= 0 and X2 <= 1:
            return X2
        elif X3 >= 0 and X3 <= 1:
            return X3
        else:
            print("FAIL to solve ptn4: (%f, %f, %f)"%(X1,X2,X3))
            return X3
            
def cubicBezierInterpolate(p1x, p2x, p1y, p2y, x):
    t = cbi_ts(p1x, p2x, x)
    y = cbi_s(p1y, p2y, t)
    return y
    
    
# support classes
class KeyFrame():
    def __init__(self):
        self.frameNo = 0
        self.targetID = ""
        
    def applyFrame(self, game):
        raise Exception("not implemented")
        
    def createInterFrameTo(self, toFrame, newFrameNo):
        raise Exception("not implemented")
        
    def dumpContent(self):
        raise Exception("not implemented")
        
    def importContent(self, content):
        raise Exception("not implemented")
        
    def copyContent(self, fromKey):
        raise Exception("not implemented")
    
    def copy(self):
        raise Exception("not implemented")

    def optimizeWith(self, fromFrame, toFrame, effectToFrame):
        raise Exception("not implemented")
    
    @staticmethod
    def sortByFrameNo(keyframe):
        return keyframe.frameNo
        
    @staticmethod
    def alignDataType(targetData, refData):
        if isinstance(targetData, dict) and isinstance(refData, dict):
            for key in targetData.keys():
                if refData.has_key(key):
                    targetData[key] = KeyFrame.alignDataType(targetData[key], refData[key])
                else:
                    #print "alignDataType warning: key '%s' in targetData not found in reference data"%str(key)
                    pass
            return targetData
        if isinstance(targetData, list) and isinstance(refData, list):
            if len(targetData) != len(refData):
                print "alignDataType warning: targetData list size(%d) not march reference list size(%d)"%(len(targetData), len(refData))
            for i in range(len(targetData)):
                if i < len(refData):
                    targetData[i] = KeyFrame.alignDataType(targetData[i], refData[i])
            return targetData
        if isinstance(targetData, tuple) and isinstance(refData, tuple):
            if len(targetData) != len(refData):
                print "alignDataType warning: targetData list size(%d) not march reference list size(%d)"%(len(targetData), len(refData))
            targetData = list(targetData)
            for i in range(len(targetData)):
                if i < len(refData):
                    targetData[i] = KeyFrame.alignDataType(targetData[i], refData[i])
            return tuple(targetData)
        if isinstance(targetData, tuple) and len(targetData) == 3 and isinstance(refData, Vector3):
            return Vector3(targetData[0], targetData[1], targetData[2])
        if isinstance(targetData, tuple) and len(targetData) == 2 and isinstance(refData, Vector2):
            return Vector2(targetData[0], targetData[1])
        if isinstance(targetData, tuple) and len(targetData) == 4 and isinstance(refData, Color):
            return Color(targetData[0], targetData[1], targetData[2], targetData[3])
        return targetData        
        
class CameraKeyFrame(KeyFrame):
    def __init__(self, frameNo, curve):
        # common
        self.frameNo = frameNo
        self.targetID = "cam"
        
        # save current camera
        from Studio import Studio
        studio = Studio.Instance
        c = studio.cameraCtrl
        cdata = c.cameraData
        self.pos = cdata.pos
        self.distance = cdata.distance
        self.rotate = cdata.rotate
        self.fieldOfView = c.fieldOfView
        
        # default interpolate curve, format [x1, x2, y1, y2]
        self.curve = curve
        
    def applyFrame(self, game):
        from Studio import Studio
        studio = Studio.Instance
        c = studio.cameraCtrl
        cdata = c.cameraData
        cdata.pos = self.pos
        cdata.distance = self.distance
        cdata.rotate = self.rotate
        c.fieldOfView = self.fieldOfView
        
    def createInterFrameTo(self, toFrame, newFrameNo):
        if self.frameNo + 1 == toFrame.frameNo:
            # do not interpolate between two adjacent key frame
            return self
        # get interpolate progress
        progress = float(newFrameNo - self.frameNo) / float(toFrame.frameNo - self.frameNo)
        
        # cubic Bezier interpolate
        pcv = cubicBezierInterpolate(toFrame.curve[0], toFrame.curve[1], toFrame.curve[2], toFrame.curve[3], progress)

        # interpolate and create new frame
        nf = CameraKeyFrame(newFrameNo, None)
        nf.pos = Vector3.Lerp(self.pos, toFrame.pos, pcv)
        nf.distance = Vector3.Lerp(self.distance, toFrame.distance, pcv)
        nf.rotate = Vector3.Lerp(self.rotate, toFrame.rotate, pcv)
        nf.fieldOfView = self.fieldOfView + (toFrame.fieldOfView - self.fieldOfView) * pcv
        #print "interpolate cam frame[%f]: pos=(%.2f, %.2f, %.2f), rot=(%.1f, %.1f, %.1f), dis=%.2f, fov=%.1f"%(nf.frameNo, nf.pos.x, nf.pos.y, nf.pos.z, nf.rotate.x, nf.rotate.y, nf.rotate.z, nf.distance.z, nf.fieldOfView)
        return nf
        
    def dumpContent(self):
        dumpDict = {"pos": self.pos, "distance": self.distance, "rotate": self.rotate, "fieldOfView": self.fieldOfView,
                    "curve": self.curve,
                   }
        return script2string(dumpDict)
        
    def importContent(self, content):
        self.pos = Vector3(content["pos"][0], content["pos"][1], content["pos"][2])
        self.distance = Vector3(content["distance"][0], content["distance"][1], content["distance"][2])
        self.rotate = Vector3(content["rotate"][0], content["rotate"][1], content["rotate"][2])
        self.fieldOfView = content["fieldOfView"]
        self.curve = content["curve"]
        
    def copyContent(self, fromKey):
        self.pos = scriptCopy(fromKey.pos)
        self.distance = scriptCopy(fromKey.distance)
        self.rotate = scriptCopy(fromKey.rotate)
        self.fieldOfView = scriptCopy(fromKey.fieldOfView)
        self.curve = scriptCopy(fromKey.curve)
        
    def copy(self):
        nf = CameraKeyFrame(self.frameNo, None)
        nf.copyContent(self)
        return nf

    def optimizeWith(self, fromFrame, toFrame, effectToFrame):
        pass    # can not optimize camera
        
class ActorKeyFrame(KeyFrame):
    def __init__(self, frameNo, actorId, status, curve):
        # common
        self.frameNo = frameNo
        self.targetID = actorId
        
        # save actor status
        self.status = status
        
        # default interpolate curve, format [x1, x2, y1, y2]
        self.curve = curve
        
    def applyFrame(self, game):
        #print "ActorKeyFrame: apply frame %d"%self.frameNo
        curStatus = game.scenedata.actors[self.targetID].export_full_status()
        dfs = {}
        for key in self.status.keys():
            if not key in curStatus.keys() or curStatus[key] != self.status[key]:
                dfs[key] = self.status[key]
        act(game, {self.targetID : dfs})
        
    def createInterFrameTo(self, toFrame, newFrameNo):
        #print "ActorKeyFrame: create frame %f"%newFrameNo
        if self.frameNo + 1 == toFrame.frameNo:
            # do not interpolate between two adjacent key frame
            return self
        # get interpolate progress
        progress = float(newFrameNo - self.frameNo) / float(toFrame.frameNo - self.frameNo)
        
        # cubic Bezier interpolate
        cbiProgress = cubicBezierInterpolate(toFrame.curve[0], toFrame.curve[1], toFrame.curve[2], toFrame.curve[3], progress)

        dfs = {}
        for ak in self.status.keys():
            if not char_act_funcs[ak][1] or not ak in toFrame.status.keys() or toFrame.status[ak] == self.status[ak]:
                dfs[ak] = self.status[ak]
            else:
                dfs[ak] = paramInterpolater(self.status[ak], toFrame.status[ak], cbiProgress)
        nf = ActorKeyFrame(newFrameNo, self.targetID, dfs, None)
        return nf
        
    def dumpContent(self):
        dumpDict = {'status': self.status, 'curve': self.curve}
        return script2string(dumpDict)
        
    def importContent(self, content):
        self.status = content["status"]
        self.curve = content["curve"]
        
    def copyContent(self, fromKey):
        self.status = scriptCopy(fromKey.status)
        self.curve = scriptCopy(fromKey.curve)

    def copy(self):
        nf = ActorKeyFrame(self.frameNo, self.targetID, None, None)
        nf.copyContent(self)
        return nf

    def optimizeWith(self, fromFrame, toFrame, effectToFrame):
        for st in self.status.keys():
            if (not toFrame.status.has_key(st) or self.status[st] == toFrame.status[st]) and (fromFrame == None or not fromFrame.status.has_key(st) or self.status[st] == fromFrame.status[st]):
                # remove from self
                self.status.pop(st)
            else:   # special care for ik_set and fk_set
                if (st == "ik_set" or st == "fk_set") and isinstance(self.status[st], dict):
                    # delete duplicated bone info
                    for bi in self.status[st].keys():
                        if (not toFrame.status.has_key(st) or not toFrame.status[st].has_key(bi) or self.status[st][bi] == toFrame.status[st][bi]) and (fromFrame == None or not fromFrame.status.has_key(st) or not fromFrame.status[st].has_key(bi) or self.status[st][bi] == fromFrame.status[st][bi]):
                            self.status[st].pop(bi)
        if effectToFrame:
            for st in toFrame.status.keys():
                if not self.status.has_key(st) or self.status[st] == toFrame.status[st]:
                    toFrame.status.pop(st)
                else:   # special care for ik_set and fk_set
                    if (st == "ik_set" or st == "fk_set") and isinstance(toFrame.status[st], dict):
                        # delete duplicated bone info
                        for bi in toFrame.status[st].keys():
                            if not self.status[st].has_key(bi) or self.status[st][bi] == toFrame.status[st][bi]:
                                toFrame.status[st].pop(bi)

class PropKeyFrame(KeyFrame):
    def __init__(self, frameNo, propId, propStatus, curve):
        # common
        self.frameNo = frameNo
        self.targetID = propId
        
        # save actor status
        self.status = propStatus
        
        # default interpolate curve, format [x1, x2, y1, y2], not necessary for non-key-frame
        self.curve = curve
        
    def applyFrame(self, game):
        #print "PropKeyFrame: apply frame %d"%self.frameNo
        curStatus = game.scenedata.props[self.targetID].export_full_status()
        dfs = {}
        for key in self.status.keys():
            if not key in curStatus.keys() or curStatus[key] != self.status[key]:
                dfs[key] = self.status[key]
        act(game, {self.targetID : dfs})
        
    def createInterFrameTo(self, toFrame, newFrameNo):
        #print "PropKeyFrame: create frame %f"%newFrameNo
        if self.frameNo + 1 == toFrame.frameNo:
            # do not interpolate between two adjacent key frame
            return self
        # get interpolate progress
        progress = float(newFrameNo - self.frameNo) / float(toFrame.frameNo - self.frameNo)

        # cubic Bezier interpolate
        cbiProgress = cubicBezierInterpolate(toFrame.curve[0], toFrame.curve[1], toFrame.curve[2], toFrame.curve[3], progress)
        
        dfs = {}
        for ak in self.status.keys():
            if not prop_act_funcs[ak][1] or not ak in toFrame.status.keys() or toFrame.status[ak] == self.status[ak]:
                dfs[ak] = self.status[ak]
            else:
                dfs[ak] = paramInterpolater(self.status[ak], toFrame.status[ak], cbiProgress)
        nf = PropKeyFrame(newFrameNo, self.targetID, dfs, None)
        return nf
        
    def dumpContent(self):
        dumpDict = {'status': self.status, 'curve': self.curve}
        return script2string(dumpDict)
        
    def importContent(self, content):
        self.status = content["status"]
        self.curve = content["curve"]
        
    def copyContent(self, fromKey):
        self.status = scriptCopy(fromKey.status)
        self.curve = scriptCopy(fromKey.curve)

    def copy(self):
        nf = PropKeyFrame(self.frameNo, self.targetID, None, None)
        nf.copyContent(self)
        return nf

    def optimizeWith(self, fromFrame, toFrame, effectToFrame):
        for st in self.status.keys():
            if (not toFrame.status.has_key(st) or self.status[st] == toFrame.status[st]) and (fromFrame == None or not fromFrame.status.has_key(st) or self.status[st] == fromFrame.status[st]):
                # remove from self
                self.status.pop(st)
        if effectToFrame:
            for st in toFrame.status.keys():
                if not self.status.has_key(st) or self.status[st] == toFrame.status[st]:
                    toFrame.status.pop(st)

class SystemKeyFrame(KeyFrame):
    def __init__(self, frameNo, sysStatus, curve):
        # common
        self.frameNo = frameNo
        self.targetID = "sys"
        
        # save actor status
        self.status = sysStatus
        
        # default interpolate curve, format [x1, x2, y1, y2], not necessary for non-key-frame
        self.curve = curve

    def applyFrame(self, game):
        #print "SystemKeyFrame: apply frame %d"%self.frameNo
        curStatus = export_sys_status(game)
        dfs = {}
        for key in self.status.keys():
            if not key in curStatus.keys() or curStatus[key] != self.status[key]:
                dfs[key] = self.status[key]
        act(game, {self.targetID : dfs})
        
    def createInterFrameTo(self, toFrame, newFrameNo):
        #print "SystemKeyFrame: create frame %f"%newFrameNo
        if self.frameNo + 1 == toFrame.frameNo:
            # do not interpolate between two adjacent key frame
            return self
        # get interpolate progress
        progress = float(newFrameNo - self.frameNo) / float(toFrame.frameNo - self.frameNo)

        # cubic Bezier interpolate
        cbiProgress = cubicBezierInterpolate(toFrame.curve[0], toFrame.curve[1], toFrame.curve[2], toFrame.curve[3], progress)
        
        dfs = {}
        for ak in self.status.keys():
            if not sys_act_funcs[ak][1] or not ak in toFrame.status.keys() or toFrame.status[ak] == self.status[ak]:
                dfs[ak] = self.status[ak]
            else:
                dfs[ak] = paramInterpolater(self.status[ak], toFrame.status[ak], cbiProgress)
        nf = SystemKeyFrame(newFrameNo, dfs, None)
        return nf
        
    def dumpContent(self):
        dumpDict = {'status': self.status, 'curve': self.curve}
        return script2string(dumpDict)
        
    def importContent(self, content):
        self.status = content["status"]
        self.curve = content["curve"]
        
    def copyContent(self, fromKey):
        self.status = scriptCopy(fromKey.status)
        self.curve = scriptCopy(fromKey.curve)

    def copy(self):
        nf = SystemKeyFrame(self.frameNo, None, None)
        nf.copyContent(self)
        return nf

    def optimizeWith(self, fromFrame, toFrame, effectToFrame):
        for st in self.status.keys():
            if (not toFrame.status.has_key(st) or self.status[st] == toFrame.status[st]) and (fromFrame == None or not fromFrame.status.has_key(st) or self.status[st] == fromFrame.status[st]):
                # remove from self
                self.status.pop(st)
        if effectToFrame:
            for st in toFrame.status.keys():
                if not self.status.has_key(st) or self.status[st] == toFrame.status[st]:
                    toFrame.status.pop(st)

class ClipKeyFrame(KeyFrame):
    def __init__(self, frameNo, clipId, clipStatus):
        # common
        self.frameNo = frameNo
        self.targetID = clipId
        
        # save clip status
        self.status = clipStatus
                
    def applyFrame(self, game):
        #print "ClipKeyFrame: apply frame %d"%self.frameNo
        if game.gdata.kfaManagedClips.has_key(self.targetID):
            game.gdata.kfaManagedClips[self.targetID].import_status(self.status)
        
    def createInterFrameTo(self, toFrame, newFrameNo):
        #print "ClipKeyFrame: create frame %f"%newFrameNo
        if self.frameNo + 1 == toFrame.frameNo:
            # do not interpolate between two adjacent key frame
            return self
        if int(newFrameNo) == self.frameNo:
            return self
        else:
            return None
        
    def dumpContent(self):
        dumpDict = {'status': self.status}
        return script2string(dumpDict)
        
    def importContent(self, content):
        self.status = content["status"]
        
    def copyContent(self, fromKey):
        self.status = scriptCopy(fromKey.status)

    def copy(self):
        nf = ClipKeyFrame(self.frameNo, self.targetID, None)
        nf.copyContent(self)
        return nf

    def optimizeWith(self, fromFrame, toFrame, effectToFrame):
        pass    # do not optimize clip keyframe

class KeyFrameClip():
    def __init__(self, game, clipScript):
        # init runtime
        self.game = game
        self.isPlaying = False
        self.curFrame = 0
        self.clipboard = None
        # setting
        self.name = ""
        self.frameLength = 300
        self.frameRate = 30
        self.priority = 100
        self.animeType = "absolute"
        self.loop = -1
        self.speed = 1
        # key frames
        self.keyframes = {}
        # new setting
        self.autorun = False    # from ver1.6
        self.version = 1
        self.syncActorAnime = False # not supported yet
        # import settings & keyframe or an empty one
        if clipScript:
            self.importSetting(clipScript)

    @property
    def lastFrameNo(self):  # the last frame no of all keyframes
        lfn = 0
        for kfs in self.keyframes.values():
            if kfs[-1].frameNo > lfn:
                lfn = kfs[-1].frameNo
        return lfn

    def copy(self, newName):
        newClip = KeyFrameClip(self.game, None)
        # setting
        newClip.name = newName  # copy except name
        newClip.frameLength = self.frameLength
        newClip.frameRate = self.frameRate
        newClip.priority = self.priority
        newClip.animeType = self.animeType
        newClip.loop = self.loop
        newClip.speed = self.speed
        newClip.autorun = self.autorun
        # key frames
        newClip.keyframes = scriptCopy(self.keyframes)
        # return
        return newClip

    def importSetting(self, clipScript, tgtId=None):
        if tgtId:
            if tgtId == "cam":
                self.keyframes["cam"] = []
                for frameNo in clipScript.keys():
                    frm = CameraKeyFrame(frameNo, None)
                    frm.importContent(clipScript[frameNo])
                    self.keyframes["cam"].append(frm)
                if len(self.keyframes["cam"]):
                    self.keyframes["cam"].sort(key=KeyFrame.sortByFrameNo)
                else:
                    self.keyframes.pop("cam")
            elif tgtId == "sys":
                refScript = export_sys_status(self.game)
                self.keyframes["sys"] = []
                for frameNo in clipScript.keys():
                    frm = SystemKeyFrame(frameNo, None, None)
                    frm.importContent(clipScript[frameNo])
                    frm.status = KeyFrame.alignDataType(frm.status, refScript)
                    self.keyframes["sys"].append(frm)
                if len(self.keyframes["sys"]):
                    self.keyframes["sys"].sort(key=KeyFrame.sortByFrameNo)
                else:
                    self.keyframes.pop("sys")
            elif self.game.scenedata.actors.has_key(tgtId):
                refScript = self.game.scenedata.actors[tgtId].export_full_status()
                self.keyframes[tgtId] = []
                for frameNo in clipScript.keys():
                    frm = ActorKeyFrame(frameNo, tgtId, None, None)
                    frm.importContent(clipScript[frameNo])
                    frm.status = KeyFrame.alignDataType(frm.status, refScript)
                    self.keyframes[tgtId].append(frm)
                if len(self.keyframes[tgtId]):
                    self.keyframes[tgtId].sort(key=KeyFrame.sortByFrameNo)
                else:
                    self.keyframes.pop(tgtId)
            elif self.game.scenedata.props.has_key(tgtId):
                refScript = self.game.scenedata.props[tgtId].export_full_status()
                self.keyframes[tgtId] = []
                for frameNo in clipScript.keys():
                    frm = PropKeyFrame(frameNo, tgtId, None, None)
                    frm.importContent(clipScript[frameNo])
                    frm.status = KeyFrame.alignDataType(frm.status, refScript)
                    self.keyframes[tgtId].append(frm)
                if len(self.keyframes[tgtId]):
                    self.keyframes[tgtId].sort(key=KeyFrame.sortByFrameNo)
                else:
                    self.keyframes.pop(tgtId)
            elif self.game.gdata.kfaManagedClips.has_key(tgtId):
                self.keyframes[tgtId] = []
                for frameNo in clipScript.keys():
                    frm = ClipKeyFrame(frameNo, tgtId, None)
                    frm.importContent(clipScript[frameNo])
                    self.keyframes[tgtId].append(frm)
                if len(self.keyframes[tgtId]):
                    self.keyframes[tgtId].sort(key=KeyFrame.sortByFrameNo)
                else:
                    self.keyframes.pop(tgtId)
            else:
                raise Exception("Unknown target ID <%s>"%tgtId)
        else:
            # setting
            self.name = clipScript["setting"]["name"]
            self.frameLength = clipScript["setting"]["frameLength"]
            self.frameRate = clipScript["setting"]["frameRate"]
            self.priority = clipScript["setting"]["priority"]
            self.animeType = clipScript["setting"]["animeType"]
            self.loop = clipScript["setting"]["loop"]
            self.speed = clipScript["setting"]["speed"]
            # from v1.6
            if "autorun" in clipScript["setting"]:
                self.autorun = clipScript["setting"]["autorun"]
            
            # key frames
            self.keyframes = {}
            # actors
            if clipScript.has_key("actors"):
                for actkey in clipScript["actors"].keys():
                    if not self.game.scenedata.actors.has_key(actkey):
                        continue
                    refScript = self.game.scenedata.actors[actkey].export_full_status()
                    self.keyframes[actkey] = []
                    for frameNo in clipScript["actors"][actkey].keys():
                        frm = ActorKeyFrame(frameNo, actkey, None, None)
                        frm.importContent(clipScript["actors"][actkey][frameNo])
                        frm.status = KeyFrame.alignDataType(frm.status, refScript)
                        self.keyframes[actkey].append(frm)
                    if len(self.keyframes[actkey]):
                        self.keyframes[actkey].sort(key=KeyFrame.sortByFrameNo)
                    else:
                        self.keyframes.pop(actkey)
            if clipScript.has_key("props"):
                for prokey in clipScript["props"].keys():
                    if not self.game.scenedata.props.has_key(prokey):
                        continue
                    refScript = self.game.scenedata.props[prokey].export_full_status()
                    self.keyframes[prokey] = []
                    for frameNo in clipScript["props"][prokey].keys():
                        frm = PropKeyFrame(frameNo, prokey, None, None)
                        frm.importContent(clipScript["props"][prokey][frameNo])
                        frm.status = KeyFrame.alignDataType(frm.status, refScript)
                        self.keyframes[prokey].append(frm)
                    if len(self.keyframes[prokey]):
                        self.keyframes[prokey].sort(key=KeyFrame.sortByFrameNo)
                    else:
                        self.keyframes.pop(prokey)
            if clipScript.has_key("clips"):
                for clpkey in clipScript["clips"].keys():
                    self.keyframes[clpkey] = []
                    for frameNo in clipScript["clips"][clpkey].keys():
                        frm = ClipKeyFrame(frameNo, clpkey, None)
                        frm.importContent(clipScript["clips"][clpkey][frameNo])
                        self.keyframes[clpkey].append(frm)
                    if len(self.keyframes[clpkey]):
                        self.keyframes[clpkey].sort(key=KeyFrame.sortByFrameNo)
                    else:
                        self.keyframes.pop(clpkey)
            if clipScript.has_key("cam"):
                self.keyframes["cam"] = []
                for frameNo in clipScript["cam"].keys():
                    frm = CameraKeyFrame(frameNo, None)
                    frm.importContent(clipScript["cam"][frameNo])
                    self.keyframes["cam"].append(frm)
                if len(self.keyframes["cam"]):
                    self.keyframes["cam"].sort(key=KeyFrame.sortByFrameNo)
                else:
                    self.keyframes.pop("cam")
            if clipScript.has_key("sys"):
                refScript = export_sys_status(self.game)
                self.keyframes["sys"] = []
                for frameNo in clipScript["sys"].keys():
                    frm = SystemKeyFrame(frameNo, None, None)
                    frm.importContent(clipScript["sys"][frameNo])
                    frm.status = KeyFrame.alignDataType(frm.status, refScript)
                    self.keyframes["sys"].append(frm)
                if len(self.keyframes["sys"]):
                    self.keyframes["sys"].sort(key=KeyFrame.sortByFrameNo)
                else:
                    self.keyframes.pop("sys")

    def exportSetting(self, tgtId=None):
        if tgtId:
            output = "{\n"
            for frm in self.keyframes[tgtId]:
                output += "    %5d : %s,\n"%(frm.frameNo, frm.dumpContent())
            output += "}"
        else:
            output = "{\n"
            # save setting
            output += "    'setting': {\n"
            output += "        'name' : '%s',\n"%self.name
            output += "        'frameLength': %d,\n"%self.frameLength
            output += "        'frameRate': %d,\n"%self.frameRate
            output += "        'priority': %d,\n"%self.priority
            output += "        'animeType': '%s',\n"%self.animeType
            output += "        'loop': %d,\n"%self.loop
            output += "        'speed': %.2f,\n"%self.speed
            output += "        'autorun': %s,\n"%self.autorun
            output += "    },\n"
            # save actors
            actKeys = [tgt for tgt in self.keyframes.Keys if self.game.scenedata.actors.has_key(tgt)]
            if len(actKeys) > 0:
                output += "    'actors': {\n"
                for tgt in actKeys:
                    output += "        '%s': {\n"%tgt
                    for frm in self.keyframes[tgt]:
                        output += "        %5d : %s,\n"%(frm.frameNo, frm.dumpContent())
                    output += "        },\n"
                output += "    },\n"
            # save props
            proKeys = [tgt for tgt in self.keyframes.Keys if self.game.scenedata.props.has_key(tgt)]
            if len(proKeys) > 0:
                output += "    'props': {\n"
                for tgt in proKeys:
                    output += "        '%s': {\n"%tgt
                    for frm in self.keyframes[tgt]:
                        output += "        %5d : %s,\n"%(frm.frameNo, frm.dumpContent())
                    output += "        },\n"
                output += "    },\n"
            # save clips
            clpKeys = [tgt for tgt in self.keyframes.Keys if self.game.gdata.kfaManagedClips.has_key(tgt)]
            if len(clpKeys) > 0:
                output += "    'clips': {\n"
                for tgt in clpKeys:
                    output += "        '%s': {\n"%tgt
                    for frm in self.keyframes[tgt]:
                        output += "        %5d : %s,\n"%(frm.frameNo, frm.dumpContent())
                    output += "        },\n"
                output += "    },\n"
            # save camera
            if self.keyframes.has_key("cam"):
                output += "    'cam': {\n"
                for frm in self.keyframes["cam"]:
                    output += "        %5d : %s,\n"%(frm.frameNo, frm.dumpContent())
                output += "    },\n"
            # save system
            if self.keyframes.has_key("sys"):
                output += "    'sys': {\n"
                for frm in self.keyframes["sys"]:
                    output += "        %5d : %s,\n"%(frm.frameNo, frm.dumpContent())
                output += "    },\n"
            output += "}\n"
        # export
        return output

    def exportSettingForScene(self, tgtId=None):
        if tgtId:
            output = "{"
            for frm in self.keyframes[tgtId]:
                output += "%5d:%s,"%(frm.frameNo, frm.dumpContent())
            output += "}"
        else:
            output = "{"
            # save setting
            output += "'setting':{"
            output += "'name':'%s',"%self.name
            output += "'frameLength':%d,"%self.frameLength
            output += "'frameRate':%d,"%self.frameRate
            output += "'priority':%d,"%self.priority
            output += "'animeType':'%s',"%self.animeType
            output += "'loop':%d,"%self.loop
            output += "'speed':%.2f,"%self.speed
            output += "'autorun':%s,"%self.autorun
            output += "},"
            # save actors
            actKeys = [tgt for tgt in self.keyframes.Keys if self.game.scenedata.actors.has_key(tgt)]
            if len(actKeys) > 0:
                output += "'actors':{"
                for tgt in actKeys:
                    output += "'%s':{"%tgt
                    for frm in self.keyframes[tgt]:
                        output += "%5d:%s,"%(frm.frameNo, frm.dumpContent())
                    output += "},"
                output += "},"
            # save props
            proKeys = [tgt for tgt in self.keyframes.Keys if self.game.scenedata.props.has_key(tgt)]
            if len(proKeys) > 0:
                output += "'props':{"
                for tgt in proKeys:
                    output += "'%s':{"%tgt
                    for frm in self.keyframes[tgt]:
                        output += "%5d:%s,"%(frm.frameNo, frm.dumpContent())
                    output += "},"
                output += "},"
            # save clips
            clpKeys = [tgt for tgt in self.keyframes.Keys if self.game.gdata.kfaManagedClips.has_key(tgt)]
            if len(clpKeys) > 0:
                output += "'clips':{"
                for tgt in clpKeys:
                    output += "'%s':{"%tgt
                    for frm in self.keyframes[tgt]:
                        output += "%5d:%s,"%(frm.frameNo, frm.dumpContent())
                    output += "},"
                output += "},"
            # save camera
            if self.keyframes.has_key("cam"):
                output += "'cam':{"
                for frm in self.keyframes["cam"]:
                    output += "%5d:%s,"%(frm.frameNo, frm.dumpContent())
                output += "},"
            # save system
            if self.keyframes.has_key("sys"):
                output += "'sys':{"
                for frm in self.keyframes["sys"]:
                    output += "%5d:%s,"%(frm.frameNo, frm.dumpContent())
                output += "},"
            output += "}"
        # export
        return output        

    def import_status(self, script):
        if script.has_key("frame") and script["frame"] != self.curFrame:
            self.seek(script["frame"])
        if script.has_key("loop") and script["loop"] != self.loop:
            self.loop = script["loop"]
            self.playLoop = script["loop"]
        if script.has_key("speed") and script["speed"] != self.speed:
            self.speed = script["speed"]
        if script.has_key("play"):
            if script["play"] == 0 and self.isPlaying:
                self.stop()
            if script["play"] == 1 and not self.isPlaying:
                self.play()
            if script["play"] == 2 and self.isPlaying:
                self.pause()

    def export_full_status(self):
        fs = {}
        if self.isPlaying:
            fs["play"] = 1      # play
            # do not export frame when play
        elif self.curFrame == 0:
            fs["play"] = 0      # stop
            fs["frame"] = self.curFrame
        else:
            fs["play"] = 2      # pause
            fs["frame"] = self.curFrame
        fs["loop"] = self.loop
        fs["speed"] = self.speed
        return fs

    def optimizeKeyFrames(self, includeFirst):
        for frms in self.keyframes.values():
            if includeFirst:
                tgtIdx = range(0, len(frms) - 1)
            else:
                tgtIdx = range(1, len(frms) - 1)
            for idx in tgtIdx:
                fromFrame = None if idx == 0 else frms[idx-1]
                frms[idx].optimizeWith(fromFrame, frms[idx+1], idx == tgtIdx[-1])

    def clearUnchangedStatus(self, tgtId=None):
        def doClrUchSt(tgtKeyframes):
            print "clear unchanged status for", tgtKeyframes[0].targetID
            for st in tgtKeyframes[0].status.keys():
                unchanged = True
                for i in range(1, len(tgtKeyframes)):
                    if not tgtKeyframes[i].status.has_key(st) or tgtKeyframes[0].status[st] != tgtKeyframes[i].status[st]:
                        unchanged = False
                        break
                if unchanged:
                    print " delete status:", st
                    for kf in tgtKeyframes:
                        kf.status.pop(st)
        # clear target clip or every clip
        if tgtId == None:
            for tgtId in self.keyframes.keys():
                if len(self.keyframes[tgtId]) > 1:
                    tgtkfs = self.keyframes[tgtId]
                    if isinstance(tgtkfs[0], ActorKeyFrame) or isinstance(tgtkfs[0], PropKeyFrame) or isinstance(tgtkfs[0], SystemKeyFrame):
                        doClrUchSt(tgtkfs)
        else:
            if self.keyframes.has_key(tgtId) and len(self.keyframes[tgtId]) > 1:
                doClrUchSt(self.keyframes[tgtId])

    def checkUnchangedStatus(self, tgtId):
        # check
        if not self.keyframes.has_key(tgtId):
            return None     # unknown ID
        tgtkfs = self.keyframes[tgtId]
        if len(tgtkfs) == 0:
            return None     # no data at all
        if len(tgtkfs) == 1:
            return ()       # not enough data for check
        if isinstance(tgtkfs[0], ActorKeyFrame) or isinstance(tgtkfs[0], PropKeyFrame) or isinstance(tgtkfs[0], SystemKeyFrame):
            ucList = []
            for st in tgtkfs[0].status.keys():
                unchanged = True
                for i in range(1, len(tgtkfs)):
                    if not tgtkfs[i].status.has_key(st) or tgtkfs[0].status[st] != tgtkfs[i].status[st]:
                        unchanged = False
                        break
                if unchanged:
                    ucList.append(st)
            return tuple(ucList)    # list of unchanged status
        else:
            return None     # camera and clip keyframe exclude

    def clearSpecifiedStatus(self, tgtId, delList, keep1st):
        # delete status in list
        tgtkfs = self.keyframes[tgtId]
        for i in range(1 if keep1st else 0, len(tgtkfs)):
            for st in delList:
                tgtkfs[i].status.pop(st)

    # play control
    def play(self, forceLoop=None):
        if forceLoop:
            self.playLoop = forceLoop
        else:
            self.playLoop = self.loop
        self.isPlaying = True
        if self.syncActorAnime:
            self.syncActor(False)
        
    def pause(self):
        self.isPlaying = False
        if self.syncActorAnime:
            self.syncActor(False)
        
    def stop(self):
        self.isPlaying = False
        self.curFrame = 0
        if self.syncActorAnime:
            self.syncActor(False)
        
    def seek(self, frameNo, apply=True):
        self.curFrame = frameNo if frameNo <= self.frameLength else frameNo % self.frameLength
        if apply:
            self.applyFrames()
            if self.syncActorAnime:
                self.syncActor(True)
        
    def update(self, game):
        from UnityEngine import Time
        if self.isPlaying:
            deltaTime = Time.deltaTime
            self.curFrame += deltaTime * self.frameRate * self.speed
            if self.curFrame > self.frameLength:
                if self.playLoop != 0:
                    self.curFrame -= self.frameLength
                    if self.playLoop > 0: self.playLoop -= 1
                else:
                    self.curFrame = self.frameLength
                    self.isPlaying = False
            #print " clip [%s] playing: dt=%f, curFrame=%f"%(self.name, deltaTime, self.curFrame)
            try:
                self.applyFrames()
            except Exception as e:
                self.isPlaying = False  # stop on exception
                traceback.print_exc()
                print "update keyframe anime Error:", e
            
    def applyFrames(self):
        for tgtId in self.keyframes.keys():
            frame = self.getCurFrame(tgtId)
            if frame:
                frame.applyFrame(self.game)
                    
    def getCurFrame(self, tgtId):
        tgtKeyFrames = self.keyframes[tgtId]
        tgtKeys = [i.frameNo for i in tgtKeyFrames]
        if tgtKeys == None or len(tgtKeys) == 0:
            return None
        if self.curFrame < tgtKeys[0]:
            return None
        if self.curFrame >= tgtKeys[-1]+1:
            return None
        if self.curFrame >= tgtKeys[-1]:
            return tgtKeyFrames[-1]
        #if self.curFrame > self.cameraKeyFrames[self.fsIndex].frameNo and self.curFrame < self.cameraKeyFrames[self.fsIndex+1].frameNo:
        #    return self.createInterFrame()
        for i in range(len(tgtKeys)):
            if self.curFrame == tgtKeys[i]:
                #self.fsIndex = i
                return tgtKeyFrames[i]
            elif self.curFrame < tgtKeys[i+1]:
                #self.fsIndex = i
                return tgtKeyFrames[i].createInterFrameTo(tgtKeyFrames[i+1], self.curFrame)
    
    def syncActor(self, seek):
        actKeys = [tgt for tgt in self.keyframes.Keys if self.game.scenedata.actors.has_key(tgt)]
        for actId in actKeys:
            actor = self.game.scenedata.actors[actId]
            if self.isPlaying:
                actor.set_anime_speed(1)
                #print "sync Actor %s's anime speed to %f"%(actId, 1)
            else:
                actor.set_anime_speed(0)
                #print "sync Actor %s's anime speed to %f"%(actId, 0)
            if seek:
                if self.curFrame == 0:
                    actor.restart_anime()
                    #print "syncActor restart anime"
                else:
                    ani = actor.get_animate()
                    nt = float(self.curFrame) / self.frameLength
                    actor.animate(ani[0], ani[1], ani[2], nt, 1)
                    #print "syncActor force animate update: %f"%(nt)

    # edit function
    def updateKeyFrame(self, keyFrame):
        # update keyframes dictionary
        if not self.keyframes.has_key(keyFrame.targetID):
            self.keyframes[keyFrame.targetID] = []
        # check if existed
        existKeys = tuple(i.frameNo for i in self.keyframes[keyFrame.targetID])
        exist = existKeys.count(keyFrame.frameNo)
        if exist == 0:
            # append new keyframe
            self.keyframes[keyFrame.targetID].append(keyFrame)
            self.keyframes[keyFrame.targetID].sort(key=KeyFrame.sortByFrameNo)
        elif exist == 1:
            # replace old keyframe
            idx = existKeys.index(keyFrame.frameNo)
            self.keyframes[keyFrame.targetID][idx] = keyFrame
        else:
            raise Exception("Duplicated keyframes at %d for id:<%s>"%(keyFrame.frameNo, keyFrame.targetID))
        
    def shiftKeyFrame(self, tgtId, shift, includeFollower):
        print "Shift key frame for %s at %d by %d, includeFollower = %s"%(tgtId, self.curFrame, shift, includeFollower)
        # check
        if shift == 0:
            return
        # shift frames
        for kf in self.keyframes[tgtId]:
            if kf.frameNo == self.curFrame or (includeFollower and kf.frameNo > self.curFrame):
                kf.frameNo += shift
        
    def deleteKeyFrame(self, tgtId):
        print "delete a key frame for %s at %d"%(tgtId, self.curFrame)
        existKeys = tuple(i.frameNo for i in self.keyframes[tgtId])
        idx = existKeys.index(self.curFrame)
        self.keyframes[tgtId].pop(idx)
        if len(self.keyframes[tgtId]) == 0:
            self.keyframes.pop(tgtId)
        
    def copyKeyFrame(self, tgtId):
        print "copy a key frame for %s at %d to clipboard"%(tgtId, self.curFrame)
        existKeys = tuple(i.frameNo for i in self.keyframes[tgtId])
        idx = existKeys.index(self.curFrame)
        self.clipboard = self.keyframes[tgtId][idx].copy()

    def canPasteKeyFrame(self, tgtId):
        if self.clipboard == None:
            return False
        if self.clipboard.targetID == tgtId:
            # same tgtId
            return True
        elif self.game.scenedata.actors.has_key(self.clipboard.targetID) and self.game.scenedata.actors.has_key(tgtId):
            # actor -> actor
            if type(self.game.scenedata.actors[self.clipboard.targetID].objctrl) == type(self.game.scenedata.actors[tgtId].objctrl):
                return True
            else:
                return False
        elif self.game.scenedata.props.has_key(self.clipboard.targetID) and self.game.scenedata.props.has_key(tgtId):
            # prop -> prop
            if type(self.game.scenedata.props[self.clipboard.targetID].objctrl) == type(self.game.scenedata.props[tgtId].objctrl):
                return True
            else:
                return False
        else:
            return False
        
    def pasteKeyFrame(self, tgtId):
        if tgtId == "cam":
            nf = CameraKeyFrame(self.curFrame, None)
            nf.copyContent(self.clipboard)
        elif tgtId == "sys":
            nf = SystemKeyFrame(self.curFrame, None, None)
            nf.copyContent(self.clipboard)
        elif tgtId in self.game.scenedata.actors:
            nf = ActorKeyFrame(self.curFrame, tgtId, None, None)
            nf.copyContent(self.clipboard)
        elif tgtId in self.game.scenedata.props:
            nf = PropKeyFrame(self.curFrame, tgtId, None, None)
            nf.copyContent(self.clipboard)
        elif tgtId in self.game.gdata.kfaManagedClips:
            nf = ClipKeyFrame(self.curFrame, tgtId, None)
            nf.copyContent(self.clipboard)
        else:
            raise Exception("Unexpected target id '%s' to paste key frame!"%tgtId)
        self.updateKeyFrame(nf)

    @staticmethod
    def sortByPriority(keyframeClip):
        return (keyframeClip.priority, keyframeClip.name)

# script wrapper function
# not supported, just for anime/non-anime check
clip_act_funcs = {
    'play': ("clip_play", False),
    'frame': ("clip_seek", False),
    'loop': ("clip_loop", False),
    'speed': ("clip_speed", True),
}

# GUI function
def kfam_GUI(sh):
    game = sh.game
    if not hasattr(game.scenedata, "kfaGuiFunction"):
        changeGuiScreen(sh, kfam_GUI_manager)
    game.scenedata.kfaGuiFunction(sh)

def changeGuiScreen(sh, newGuiScreen, targetClip=None):
    if newGuiScreen == kfam_GUI_manager:
        sh.game.scenedata.kfamOnModifyClip = None
        sh.game.windowName = "Key Frame Animation Clip Manager"
    elif newGuiScreen == kfam_GUI_create_clip:
        sh.game.scenedata.kfamOnModifyClip = targetClip
        sh.game.scenedata.kfamCreateType = 0
        sh.game.scenedata.kfamCreateName = ""
        sh.game.scenedata.kfamCreateFile = ""
        sh.game.scenedata.kfamImportClipName = True
        sh.game.windowName = "Create new key frame animation clip"
    elif newGuiScreen == kfam_GUI_modify_clip:
        sh.game.scenedata.kfamOnModifyClip = targetClip
        sh.game.scenedata.kfamModifyTabIndex = -1
        sh.game.windowName = "Editing clip [<b><color=#ff0000>%s</color></b>]"%targetClip.name
    else:
        raise Exception("Unknown KeyFrameAnime GUI Function")
    # change
    sh.game.scenedata.kfaGuiFunction = newGuiScreen

def outputAllClipsToScene(game):
    # shortcuts
    sClips = game.gdata.kfaSortedClips
    # delete "-keyframeclips:" folder if existed
    flds = game.scene_get_all_folders()
    for fld in flds:
        if fld.name.startswith("-keyframeclips:"):
            fld.delete()
            break
    # create "-keyframeclips:" folder
    clpBaseFld = HSNeoOCIFolder.add("-keyframeclips:v1")
    # build output for all managered clips
    for clip in sClips:
        clpFld = HSNeoOCIFolder.add("-clip:%s:0"%clip.name)
        clpFld.set_parent(clpBaseFld)
        output = clip.exportSettingForScene()
        clpData = HSNeoOCIFolder.add(output)
        clpData.set_parent(clpFld)
    scriptHelperGUIMessage("All keyframe clips in keyframe clip manager were export into <color=#ffff00>-keyframeclips:v1</color> folder. <color=#ff0000>Save your scene to save your work!</color>")

def importAllClipsFromScene(game, baseFld=None):
    # try to found base folder if not setted
    if baseFld == None:
        flds = game.scene_get_all_folders()
        for fld in flds:
            if fld.name.startswith("-keyframeclips:"):
                baseFld = fld
                break
    if baseFld == None:
        return
    # update regist tag
    register_actor_prop_by_tag(game)
    # load all clips
    for clpFld in baseFld.treeNodeObject.child:
        clpFldTxt = clpFld.textName
        if clpFldTxt.startswith("-clip:"):
            try:
                clpScp = eval(clpFld.child[0].textName)
                kfa_import(game, clpScp)
            except Exception as e:
                print "Error in load %s: %s"%(clpFldTxt, str(e))

def outputAllClipsToExtFile(sh):
    # shortcuts
    sClips = sh.game.gdata.kfaSortedClips
    # build output for all managered clips
    output = ""
    for clip in sClips:
        output += clip.exportSetting()
        output += ",\n"
    # dump or save to python
    if sh.asTemplate and sh.asEnable:
        msg = sh.as_rebuild_clips(output)
        scriptHelperGUIMessage(msg, ("OK",))
    else:
        if saveStringToFile("dumppython.txt", output, append=True):
            scriptHelperGUIMessage("All keyframe clips in keyframe clip manager were dumpped into <color=#ffff00>dumppython.txt</color>.")

def selectTaggedActorOrProp(game):
    try:
        sel = HSNeoOCI.create_from_selected()
    except:
        return (None, None)
    if isinstance(sel, HSNeoOCIChar):
        for actorId in game.scenedata.actors.keys():
            if game.scenedata.actors[actorId].objctrl == sel.objctrl:
                return (actorId, game.scenedata.actors[actorId])
        return (None, sel.as_actor)
    if isinstance(sel, HSNeoOCIProp):
        for propId in game.scenedata.props.keys():
            if game.scenedata.props[propId].objctrl == sel.objctrl:
                return (propId, game.scenedata.props[propId])
        return (None, sel.as_prop)
    return (None, None)

def drawCurve(texture, curveData):
    from System import Array
    from UnityEngine import Color, Color32
    w = texture.width
    h = texture.height
    #print "Update curve:", curveData
    # build canvas
    canvasCols = []
    for y in range(h):
        for x in range(w):
            if x == 0 or y == 0 or x == 99 or y == 99:
                canvasCols.append(Color.white)
            else:
                canvasCols.append(Color(0, 0, 0, 0))
    # funcs
    def point(x, y, color):
        if x < 0: x = 0
        if x > w-1: x = w-1
        if y < 0: y = 0
        if y > h-1: y = h-1
        idx = int(y*w+x)
        canvasCols[idx] = color
    def handle(x, y, color):
        point(x-1, y-1, color)
        point(x, y-1, color)
        point(x+1, y-1, color)
        point(x-1, y, color)
        point(x, y, color)
        point(x+1, y, color)
        point(x-1, y+1, color)
        point(x, y+1, color)
        point(x+1, y+1, color)
    # draw cuvre
    for x in range(1, w-1):
        y = cubicBezierInterpolate(curveData[0], curveData[1], curveData[2], curveData[3], float(x)/w)
        y = round(y*h)
        point(x, y, Color.yellow)
    # draw handle
    h1x = round(w*curveData[0])
    h2x = round(w*curveData[1])
    h1y = round(h*curveData[2])
    h2y = round(h*curveData[3])
    handle(h1x, h1y, Color.cyan)
    handle(h2x, h2y, Color.magenta)
    # done
    texture.SetPixels(Array[Color](canvasCols))
    texture.Apply()

def saveStringToFile(filename, outputString, append=False, backup=True):
    import shutil
    import codecs
    fp = None
    try:
        if not append and backup and path.isfile(filename):
            bckfile = filename + ".bak"
            shutil.move(filename, bckfile)
        fp = codecs.open(filename, 'a+' if append else 'w', 'utf-8')
        fp.write(outputString)
        fp.close()
        return True
    except Exception as e:
        if fp != None: fp.close()
        msg = "Save file '%s' failed: '%s'"%(filename, str(e))
        scriptHelperGUIMessage(msg)
        return False

def loadScriptFromFile(filename):
    import codecs
    fp = None
    try:
        fp = codecs.open(filename, "r", 'utf-8')
        fileContent = fp.read()
        fp.close()
        fileScript = eval(fileContent)
        return fileScript
    except Exception as e:
        if fp != None: fp.close()
        msg = "Load file '%s' failed: '%s'"%(filename, str(e))
        raise Exception(msg)

def translateAndSortStatusKeys(orgStatusKeys):
    from vnactor import get_ini_translation
    forSort = []
    stDict = {}
    for st in orgStatusKeys:
        tst = get_ini_translation(st)
        try:
            tsts = tst.split(":")
            snum = int(tsts[0])
            stxt = tsts[1]
            scolor = "ffffff" if len(tsts) < 3 else tsts[2]
        except:
            snum = 99999
            stxt = st
            scolor = "ffffff"
        forSort.append((snum, stxt, st))
        stDict[st] = "<color=#%s>%s</color>"%(scolor, stxt)
    forSort.sort(key=lambda x:(x[0], x[1]))
    oslist = [i[2] for i in forSort]
    return oslist, stDict

def startFileBrower(sh, startPath=None, extFilter=None, openSave="open", title=None, onOk=None, onCancel=None):
    from UnityEngine import Application
    game = sh.game
    # list all drivers
    game.scenedata.fb_drivers = []
    for drv in range(65, 91):
        vol = chr(drv) + ':\\'
        if path.isdir(vol):
            game.scenedata.fb_drivers.append(vol)
    # check start path
    if startPath != None and path.exists(startPath):
        game.scenedata.fb_cur_input = path.realpath(startPath)
    elif not hasattr(game.scenedata, "fb_cur_input"):
        game.scenedata.fb_cur_input = path.realpath(path.join(Application.dataPath, '..'))
    # setup
    game.scenedata.fb_ext_filter = None if extFilter == None else (extFilter if isinstance(extFilter, list) or isinstance(extFilter, tuple) else [extFilter])
    game.scenedata.fb_open_save = openSave
    game.scenedata.fb_title = "Select a file to %s:"%openSave if title == None else title
    game.scenedata.fb_scroll_pos = Vector2.zero    
    game.scenedata.fb_selected_file = None
    game.scenedata.fb_on_ok = onOk
    game.scenedata.fb_on_cancel = onCancel
    # goto file browser
    game.scenedata.fb_previous_gui_function = sh.game.scenedata.kfaGuiFunction
    game.scenedata.kfaGuiFunction = util_GUI_file_browser

def util_GUI_file_browser(sh):
    from UnityEngine import GUI, GUILayout, GUIStyle, GUIContent, GUIUtility, Screen, Rect, Vector3, Input, KeyCode, TextAnchor
    fullw = sh.game.wwidth-30
    btnstyle = GUIStyle("button")
    btnstyle.fontSize = 14
    fbStyle = GUIStyle("button")
    fbStyle.alignment = TextAnchor.MiddleLeft
    
    # shortcuts
    game = sh.game
    
    # path info
    from os import listdir
    if path.isfile(game.scenedata.fb_cur_input):
        game.scenedata.fb_cur_input = path.realpath(game.scenedata.fb_cur_input)
        curPath = path.split(game.scenedata.fb_cur_input)[0]        
    elif path.isdir(game.scenedata.fb_cur_input):
        if not game.scenedata.fb_cur_input.endswith("\\"):
            game.scenedata.fb_cur_input += "\\"
        curPath = game.scenedata.fb_cur_input
    else:
        curPath = path.split(game.scenedata.fb_cur_input)[0]
        if not path.isdir(curPath):
            curPath = game.pygamepath
            game.scenedata.fb_cur_input = curPath
    #print "info: fb_cur_input:", game.scenedata.fb_cur_input, "curPath:", curPath
    if game.scenedata.fb_cur_input == "":
        subfiles = game.scenedata.fb_drivers
    else:
        subfiles = listdir(curPath)
    
    # title
    GUILayout.BeginHorizontal()
    GUILayout.Label(game.scenedata.fb_title, GUILayout.Width(fullw))
    GUILayout.EndHorizontal()

    # file indicator
    GUILayout.BeginHorizontal()
    if GUILayout.Button("^", GUILayout.Width(20)):
        if curPath in game.scenedata.fb_drivers or curPath == "":
            game.scenedata.fb_cur_input = ""
        else:
            game.scenedata.fb_cur_input = path.realpath(path.join(curPath, '..'))
    if game.scenedata.fb_open_save == "save":
        game.scenedata.fb_cur_input = GUILayout.TextField(game.scenedata.fb_cur_input, GUILayout.Width(fullw - 22))
    else:
        GUILayout.TextField(game.scenedata.fb_cur_input, GUILayout.Width(fullw - 22))
    GUILayout.EndHorizontal()
    
    # file/folder selector
    GUILayout.BeginHorizontal()
    game.scenedata.fb_scroll_pos = GUILayout.BeginScrollView(game.scenedata.fb_scroll_pos, GUILayout.Width(fullw), GUILayout.Height(150))
    for f in subfiles:
        if not path.isfile(path.join(curPath, f)):
            if GUILayout.Button("<color=#6edb00>[" + f + "]</color>", fbStyle):
                game.scenedata.fb_cur_input = path.realpath(path.join(curPath, f))
    for f in subfiles:
        if not path.isfile(path.join(curPath, f)):
            continue
        if game.scenedata.fb_ext_filter != None:
            filter = [flt.lower() for flt in game.scenedata.fb_ext_filter]
            fext = path.splitext(f)[1].lower()
            if not fext in filter:
                continue
        if GUILayout.Button(f, fbStyle):
            game.scenedata.fb_cur_input = path.realpath(path.join(curPath, f))
    GUILayout.EndScrollView()
    GUILayout.EndHorizontal()
    
    # Control buttons
    btnW = fullw / 2 - 4
    GUILayout.FlexibleSpace()
    GUILayout.BeginHorizontal()
    if GUILayout.Button("OK", btnstyle, GUILayout.Width(btnW)):
        game.scenedata.fb_selected_file = game.scenedata.fb_cur_input
        if game.scenedata.fb_open_save == "save" and game.scenedata.fb_ext_filter and len(game.scenedata.fb_ext_filter) == 1 and not game.scenedata.fb_selected_file.lower().endswith(game.scenedata.fb_ext_filter[0].lower()):
            game.scenedata.fb_selected_file += game.scenedata.fb_ext_filter[0]
        game.scenedata.kfaGuiFunction = game.scenedata.fb_previous_gui_function
        if game.scenedata.fb_on_ok != None:
            game.scenedata.fb_on_ok(game, game.scenedata.fb_selected_file)
    if GUILayout.Button("Cancel", btnstyle, GUILayout.Width(btnW)):
        game.scenedata.fb_selected_file = None
        game.scenedata.kfaGuiFunction = game.scenedata.fb_previous_gui_function
        if game.scenedata.fb_on_cancel != None:
            game.scenedata.fb_on_cancel(game)
    GUILayout.EndHorizontal()

def startManualOptimize(sh):
    game = sh.game
    sd = game.scenedata
    clip = sd.kfamOnModifyClip
    # list up keyframe tgt
    sd.mo_target_ids = {}
    sd.mo_target_sts = {}
    sd.mo_keep1st = {}
    #sd.mo_cleanIKFK = {}
    for kfId in clip.keyframes.keys():
        st = clip.checkUnchangedStatus(kfId)
        if st != None and len(st) != 0:
            sd.mo_target_ids[kfId] = True
            sd.mo_keep1st[kfId] = False
            #sd.mo_cleanIKFK[kfId] = False
            stdict = {}
            for s in st:
                stdict[s] = False
            sd.mo_target_sts[kfId] = stdict
    sd.mo_target_sclpos = Vector2.zero
    sd.mo_status_sclpos = Vector2.zero
    sd.mo_cur_tid = None if len(sd.mo_target_ids) == 0 else sd.mo_target_ids.keys()[0]
    # goto optimize GUI
    game.scenedata.fb_previous_gui_function = sh.game.scenedata.kfaGuiFunction
    game.scenedata.kfaGuiFunction = util_GUI_manual_optimize

def util_GUI_manual_optimize(sh):
    from UnityEngine import GUI, GUILayout, GUIStyle
    from System import String, Array
    fullw = sh.game.wwidth-30
    btnstyle = GUIStyle("button")
    btnstyle.fontSize = 14

    # shortcuts
    game = sh.game
    sd = game.scenedata
    clip = sd.kfamOnModifyClip

    if sd.mo_cur_tid != None:
        GUILayout.BeginHorizontal()
        GUILayout.Label("Select and clear unchanged status to optimzie clip:")
        GUILayout.EndHorizontal()

        GUILayout.BeginHorizontal()
        # left panel: target list
        GUILayout.BeginVertical(GUILayout.Width(150))
        sd.mo_target_sclpos = GUILayout.BeginScrollView(sd.mo_target_sclpos, GUILayout.Width(150), GUILayout.Height(170))
        for tid in sd.mo_target_ids.keys():
            GUILayout.BeginHorizontal()
            sd.mo_target_ids[tid] = GUILayout.Toggle(sd.mo_target_ids[tid], " ", GUILayout.Width(15))
            if GUILayout.Button(tid if tid != sd.mo_cur_tid else "<color=#00ff00>" + tid + "</color>"):
                sd.mo_cur_tid = tid
            GUILayout.EndHorizontal()
        GUILayout.EndScrollView()
        GUILayout.EndVertical()

        # mid panel: status list
        GUILayout.Space(10)
        sd.mo_status_sclpos = GUILayout.BeginScrollView(sd.mo_status_sclpos, GUILayout.Width(150), GUILayout.Height(170))
        sortIds, idDict = translateAndSortStatusKeys(sd.mo_target_sts[sd.mo_cur_tid].keys())
        for sid in sortIds:
            sd.mo_target_sts[sd.mo_cur_tid][sid] = GUILayout.Toggle(sd.mo_target_sts[sd.mo_cur_tid][sid], idDict[sid])
        GUILayout.EndScrollView()

        # right panel: infos
        GUILayout.Space(10)
        GUILayout.BeginVertical(GUILayout.Width(fullw - 20 - 300))
        if sd.mo_cur_tid in sd.actors:
            cName = "<color=#ff0000>%s</color>"%sd.actors[sd.mo_cur_tid].text_name
        elif sd.mo_cur_tid in sd.props:
            cName = "<color=#00ff00>%s</color>"%sd.props[sd.mo_cur_tid].text_name
        elif sd.mo_cur_tid == "sys":
            cName = "<color=#ffff00>System</color>"
        else:
            cName = "<color=#ff0000>Unknown!?</color>"
        if sd.mo_target_ids[sd.mo_cur_tid]:
            GUILayout.Label("<color=#00ff00>%d</color> unchanged status detected for %s, <color=#ff0000>%d</color> status are selected to delete."%(len(sd.mo_target_sts[sd.mo_cur_tid]), cName, sd.mo_target_sts[sd.mo_cur_tid].values().count(True)))
            GUILayout.BeginHorizontal()
            if GUILayout.Button("All", GUILayout.Width((fullw - 20 - 300)/2-2)):
                for sid in sd.mo_target_sts[sd.mo_cur_tid]:
                    sd.mo_target_sts[sd.mo_cur_tid][sid] = True
            if GUILayout.Button("None", GUILayout.Width((fullw - 20 - 300)/2-2)):
                for sid in sd.mo_target_sts[sd.mo_cur_tid]:
                    sd.mo_target_sts[sd.mo_cur_tid][sid] = False
            GUILayout.EndHorizontal()
            sd.mo_keep1st[sd.mo_cur_tid] = GUILayout.Toggle(sd.mo_keep1st[sd.mo_cur_tid], "Keep first keyframe")
            #if clip.keyframes[sd.mo_cur_tid][0].status.has_key("ik_set") or clip.keyframes[sd.mo_cur_tid][0].status.has_key("fk_set"):
            #    sd.mo_cleanIKFK[sd.mo_cur_tid] = GUILayout.Toggle(sd.mo_cleanIKFK[sd.mo_cur_tid], "Clean unchanged IK/FK nodes")
        else:
            GUILayout.Label("%s excluded from clean-up optimization."%(cName))
        GUILayout.EndVertical()
        GUILayout.EndHorizontal()

        # tail button
        GUILayout.FlexibleSpace()
        GUILayout.BeginHorizontal()
        if GUILayout.Button("<color=#ff6666>Do cleanup</color>", btnstyle, GUILayout.Height(24), GUILayout.Width(fullw/2-4)):
            for tid in sd.mo_target_ids.keys():
                if sd.mo_target_ids[tid]:
                    delList = []
                    for st in sd.mo_target_sts[tid].keys():
                        if sd.mo_target_sts[tid][st]:
                            delList.append(st)
                    print "For %s delete:"%tid, delList
                    clip.clearSpecifiedStatus(tid, delList, sd.mo_keep1st[tid])
            game.scenedata.kfaGuiFunction = game.scenedata.fb_previous_gui_function
        if GUILayout.Button("Cancel", btnstyle, GUILayout.Height(24), GUILayout.Width(fullw/2-4)):
            game.scenedata.kfaGuiFunction = game.scenedata.fb_previous_gui_function
        GUILayout.EndHorizontal()

    else:
        # nothing to optimize
        GUILayout.BeginHorizontal()
        GUILayout.Label("Nothing to optimzie!")
        GUILayout.EndHorizontal()

        GUILayout.FlexibleSpace()
        GUILayout.BeginHorizontal()
        if GUILayout.Button("Cancel", btnstyle, GUILayout.Height(24), GUILayout.Width(fullw)):
            game.scenedata.kfaGuiFunction = game.scenedata.fb_previous_gui_function
        GUILayout.EndHorizontal()

def kfam_GUI_manager(sh):
    from UnityEngine import GUI, GUILayout, GUIStyle
    from System import String, Array
    fullw = sh.game.wwidth-30
    btnstyle = GUIStyle("button")
    btnstyle.fontSize = 14
    
    # shortcuts
    game = sh.game
    sd = game.scenedata
    mClips = game.gdata.kfaManagedClips
    sClips = game.gdata.kfaSortedClips

    # auto load from scene
    clpBaseFld = None
    flds = sh.game.scene_get_all_folders()
    for fld in flds:
        if fld.name.startswith("-keyframeclips:"):
            clpBaseFld = fld
            break
    if clpBaseFld and len(mClips) == 0:
        scriptHelperGUIMessage("Auto load clips from scene...")
        importAllClipsFromScene(game, clpBaseFld)
    
    # setting for clips
    if not hasattr(sd, "kfamSelectedClipIndex"):
        sd.kfamSelectedClipIndex = -1
        sd.kfamScrollPos = Vector2.zero
        sd.kfamTempName = ""
        sd.kfamCheckStatus = {}
    clipNameList = []
    for clip in sClips:
        if clip.isPlaying:
            n = "<color=#00ff00>" + clip.name + "</color>"
        else:
            n = "<color=#ffffff>" + clip.name + "</color>"
        if not sd.kfamCheckStatus.has_key(clip.name):
            sd.kfamCheckStatus[clip.name] = False
        if sd.kfamCheckStatus[clip.name]:
            n = "<b>" + n + "</b>"
        if clip.animeType == "relative":
            n = "<i>" + n + "</i>"
        clipNameList.append(n)
    #clipNameList.reverse()
    for clipName in sd.kfamCheckStatus.keys():
        if not mClips.has_key(clipName):
            sd.kfamCheckStatus.pop(clipName)
    checkedCount = sd.kfamCheckStatus.values().count(True)
    
    # clip manager UI
    GUILayout.BeginHorizontal()
    # left panel
    GUILayout.BeginVertical(GUILayout.Width(100))
    sd.kfamScrollPos = GUILayout.BeginScrollView(sd.kfamScrollPos, GUILayout.Width(100-4), GUILayout.Height(200))
    selectedClip = GUILayout.SelectionGrid(sd.kfamSelectedClipIndex, Array[String](tuple(clipNameList)), 1)
    if selectedClip != sd.kfamSelectedClipIndex:
        sd.kfamSelectedClipIndex = selectedClip
        sd.kfamTempName = sClips[selectedClip].name
        sd.kfamTempPriority = "%d"%sClips[selectedClip].priority
        sd.kfamTempType = sClips[selectedClip].animeType
        sd.kfamTempLength = "%d"%sClips[selectedClip].frameLength
        sd.kfamTempFPS = "%d"%sClips[selectedClip].frameRate
        sd.kfamTempSpeed = "%.2f"%sClips[selectedClip].speed
        sd.kfamTempLoop = "%d"%sClips[selectedClip].loop
        sd.kfamTempAutorun = sClips[selectedClip].autorun
    GUILayout.EndScrollView()
    GUILayout.EndVertical()
    # right panel
    if sd.kfamSelectedClipIndex != -1:
        clip = sClips[sd.kfamSelectedClipIndex]
    else:
        clip = None
    GUILayout.BeginVertical(GUILayout.Width(fullw-100))
    if clip:
        # setting
        GUILayout.BeginHorizontal()
        GUILayout.Label("Clip <<color=#00ffff>%s</color>> settings:"%clip.name, GUILayout.Width(200))
        sd.kfamCheckStatus[clip.name] = GUILayout.Toggle(sd.kfamCheckStatus[clip.name], "<color=#ff0000><b>Selected</b></color>" if sd.kfamCheckStatus[clip.name] else "Select", GUILayout.Width(80))
        settingModified = sd.kfamTempName != clip.name or sd.kfamTempPriority != "%d"%clip.priority or sd.kfamTempType != clip.animeType or sd.kfamTempLength != "%d"%clip.frameLength or sd.kfamTempFPS != "%d"%clip.frameRate or sd.kfamTempSpeed != "%.2f"%clip.speed or sd.kfamTempLoop != "%d"%clip.loop or sd.kfamTempAutorun != clip.autorun
        if settingModified and GUILayout.Button("<color=#ff0000>Apply</color>"):
            try:
                oldName = clip.name
                name = sd.kfamTempName.strip()
                if len(name) == 0:
                    raise Exception("Clip name can not be empty!")
                if name != clip.name and mClips.has_key(name):
                    raise Exception("Clip name dupulicated!")
                priority = int(sd.kfamTempPriority)
                frameLength = int(sd.kfamTempLength)
                if frameLength < clip.lastFrameNo:
                    raise Exception("Clip's length must be equal or greater than last key frame No. #%d!"%clip.lastFrameNo)
                frameRate = int(sd.kfamTempFPS)
                speed = float(sd.kfamTempSpeed)
                loop = int(sd.kfamTempLoop)
                if name != clip.name:
                    kfa_rename(game, oldName, name)
                if priority != clip.priority:
                    kfa_resort(game, name, priority)
                    sd.kfamSelectedClipIndex = -1
                if sd.kfamTempType != clip.animeType:
                    kfa_retype(game, name, sd.kfamTempType)
                clip.frameLength = frameLength
                clip.frameRate = frameRate
                clip.speed = speed
                clip.loop = loop
                clip.autorun = sd.kfamTempAutorun
            except Exception as e:
                scriptHelperGUIMessage("Apply setting failed: " + str(e))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Name:", GUILayout.Width(50))
        sd.kfamTempName = GUILayout.TextField(sd.kfamTempName, GUILayout.Width(80))
        GUILayout.Space(5)
        GUILayout.Label("Priority:", GUILayout.Width(50))
        sd.kfamTempPriority = GUILayout.TextField(sd.kfamTempPriority, GUILayout.Width(35))
        GUILayout.Space(5)
        sd.kfamTempAutorun = GUILayout.Toggle(sd.kfamTempAutorun, "Auto run on load")
        #GUILayout.Label("Type:", GUILayout.Width(40))
        #if GUILayout.Button(sd.kfamTempType if sd.kfamTempType == "absolute" else "<i>" + sd.kfamTempType + "</i>"):
        #    if sd.kfamTempType == "absolute":
        #        sd.kfamTempType = "relative"
        #    else:
        #        sd.kfamTempType = "absolute"
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Length:", GUILayout.Width(50))
        sd.kfamTempLength = GUILayout.TextField(sd.kfamTempLength, GUILayout.Width(50))
        GUILayout.Space(5)
        GUILayout.Label("FPS:", GUILayout.Width(35))
        sd.kfamTempFPS = GUILayout.TextField(sd.kfamTempFPS, GUILayout.Width(25))
        GUILayout.Space(5)
        GUILayout.Label("Speed:", GUILayout.Width(50))
        sd.kfamTempSpeed = GUILayout.TextField(sd.kfamTempSpeed, GUILayout.Width(35))
        GUILayout.Space(5)
        GUILayout.Label("Loop:", GUILayout.Width(35))
        sd.kfamTempLoop = GUILayout.TextField(sd.kfamTempLoop, GUILayout.Width(35))
        GUILayout.EndHorizontal()
        # play control
        GUILayout.BeginHorizontal()
        newframe = GUILayout.HorizontalSlider(clip.curFrame, 0, clip.frameLength, GUILayout.Width(fullw-100))
        if not clip.isPlaying and int(newframe) != int(clip.curFrame):
            clip.seek(int(newframe))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        if GUILayout.Button("||" if clip.isPlaying else u'\u25b6', GUILayout.Width(23)):
            if clip.isPlaying:
                clip.pause()
            else:
                clip.play()
        if GUILayout.Button(u'\u25a0', GUILayout.Width(23)):
            clip.stop()
        if GUILayout.Button("|<", GUILayout.Width(23)):
            clip.seek(0)
        if GUILayout.Button("<<", GUILayout.Width(23)):
            newframe = 0 if clip.curFrame <  clip.frameRate else clip.curFrame -  clip.frameRate
            clip.seek(newframe)
        if GUILayout.Button("<", GUILayout.Width(23)):
            newframe = 0 if clip.curFrame < 1 else clip.curFrame - 1
            clip.seek(newframe)
        GUILayout.Label("%d/%d %.1f/%.1fs"%(clip.curFrame, clip.frameLength, clip.curFrame/clip.frameRate, clip.frameLength/clip.frameRate))
        if GUILayout.Button(">", GUILayout.Width(23)):
            newframe = clip.frameLength if clip.curFrame + 1 >= clip.frameLength else clip.curFrame + 1
            clip.seek(newframe)
        if GUILayout.Button(">>", GUILayout.Width(23)):
            newframe = clip.frameLength if clip.curFrame + clip.frameRate >= clip.frameLength else clip.curFrame +  clip.frameRate
            clip.seek(newframe)
        if GUILayout.Button(">|", GUILayout.Width(23)):
            clip.seek(clip.frameLength)
        GUILayout.EndHorizontal()
    else:
        GUILayout.BeginHorizontal()
        GUILayout.Label("Select a clip to edit")
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("")
        GUILayout.EndHorizontal()
    # all play control
    GUILayout.BeginHorizontal()
    GUILayout.Label("Sync play control:")
    GUILayout.EndHorizontal()
    GUILayout.BeginHorizontal()
    GUILayout.Label("Play All:")
    if GUILayout.Button(u'\u25b6', GUILayout.Width(25)):
        kfa_playAll(game)
    if GUILayout.Button("||", GUILayout.Width(25)):
        kfa_pauseAll(game)
    if GUILayout.Button(u'\u25a0', GUILayout.Width(25)):
        kfa_stopAll(game)
    if GUILayout.Button("|<", GUILayout.Width(25)):
        kfa_rewindAll(game)
    GUILayout.Label("", GUILayout.Width(10))
    GUILayout.Label("Play Select:")
    if GUILayout.Button(u'\u25b6', GUILayout.Width(25)):
        for clipName in sd.kfamCheckStatus.keys():
            if sd.kfamCheckStatus[clipName]:
                kfa_play(game, clipName)
    if GUILayout.Button("||", GUILayout.Width(25)):
        for clipName in sd.kfamCheckStatus.keys():
            if sd.kfamCheckStatus[clipName]:
                kfa_pause(game, clipName)
    if GUILayout.Button(u'\u25a0', GUILayout.Width(25)):
        for clipName in sd.kfamCheckStatus.keys():
            if sd.kfamCheckStatus[clipName]:
                kfa_stop(game, clipName)
    if GUILayout.Button("|<", GUILayout.Width(25)):
        for clipName in sd.kfamCheckStatus.keys():
            if sd.kfamCheckStatus[clipName]:
                kfa_seek(game, clipName, 0)
    GUILayout.EndHorizontal()
    GUILayout.FlexibleSpace()
    GUILayout.BeginHorizontal()
    if GUILayout.Button("Create", btnstyle, GUILayout.Width(70)):
        changeGuiScreen(sh, kfam_GUI_create_clip, clip)
    if clip and GUILayout.Button("Modify" if clip else "", btnstyle, GUILayout.Width(70)):
        changeGuiScreen(sh, kfam_GUI_modify_clip, clip)
    if clip and GUILayout.Button("Delete" if clip else "", btnstyle, GUILayout.Width(70)):
        def onDeleteClip():
            kfa_remove(game, clip.name)
            sd.kfamSelectedClipIndex = -1
        scriptHelperGUIMessage("Are you sure to delete the clip <%s>?"%clip.name, (("Yes, Delete it!", onDeleteClip), "Cancel"))
    if checkedCount > 1 and GUILayout.Button("Merge", btnstyle, GUILayout.Width(70)):
        scriptHelperGUIMessage("Not supported yet :)")
    if clpBaseFld and GUILayout.Button("Reload", btnstyle, GUILayout.Width(70)):
        scriptHelperGUIMessage("Are you sure to reload all the clips from the scene?", (("Yes, Reload them!", importAllClipsFromScene, game), "Cancel"))
    GUILayout.EndHorizontal()
    GUILayout.EndVertical() # right panel
    GUILayout.EndHorizontal() # all ui

    # Control buttons
    GUILayout.FlexibleSpace()
    GUILayout.BeginHorizontal()
    if GUILayout.Button("Script Builder", btnstyle, GUILayout.Width(100), GUILayout.Height(24)):
        scriptHelperGUIToSceen(0)
    if GUILayout.Button("Anime Buffer", btnstyle, GUILayout.Width(100), GUILayout.Height(24)):
        scriptHelperGUIToSceen(1)
    if GUILayout.Button("<color=#ff6666ff>Export Clips</color>", btnstyle, GUILayout.Width(100), GUILayout.Height(24)):
        scriptHelperGUIMessage("Where do you want to export the key frame anime clips?\n* To Scene: Export clip data into scene, it will be saved with PNG.\n* To Ext File: Export clip data into py file or dump file.", (("To Scene", outputAllClipsToScene, sh.game) , ("To Ext File", outputAllClipsToExtFile, sh), "Cancel"))
    if GUILayout.Button("Scene Helper", btnstyle, GUILayout.Width(100), GUILayout.Height(24)):
        scriptHelperGUIToSceen(3)
    if GUILayout.Button("Back", btnstyle, GUILayout.Width(50), GUILayout.Height(24)):
        scriptHelperGUIClose()
    GUILayout.EndHorizontal()

def kfam_GUI_create_clip(sh):
    from UnityEngine import GUI, GUILayout, GUIStyle
    from System import String, Array
    fullw = sh.game.wwidth-30
    btnstyle = GUIStyle("button")
    btnstyle.fontSize = 14
    
    # shortcuts
    game = sh.game
    sd = game.scenedata
    clip = sd.kfamOnModifyClip
    mClips = game.gdata.kfaManagedClips
    sClips = game.gdata.kfaSortedClips

    # type
    GUILayout.BeginHorizontal()
    createTypes = ["Empty Clip", "Copy <%s>"%clip.name if clip else "<color=#555555>Copy</color>", "Import File"]
    createTypes[sd.kfamCreateType] = "<color=#00ffff>" + createTypes[sd.kfamCreateType] + "</color>"
    GUILayout.Label("Create:", GUILayout.Width(80))
    sel = GUILayout.SelectionGrid(sd.kfamCreateType, Array[String](createTypes), 3)
    if sel != sd.kfamCreateType:
        if clip == None and sel == 1:
            scriptHelperGUIMessage("Select a clip in manager then click the <create> button to create a copy.")
        else:
            sd.kfamCreateType = sel
    GUILayout.EndHorizontal()
    # name
    GUILayout.BeginHorizontal()
    GUILayout.Label("Clip Name:", GUILayout.Width(80))
    if sd.kfamCreateType != 2 or not sd.kfamImportClipName:
        sd.kfamCreateName = GUILayout.TextField(sd.kfamCreateName, GUILayout.Width(120))
    if sd.kfamCreateType == 2:
        sd.kfamImportClipName = GUILayout.Toggle(sd.kfamImportClipName, "Import clip's name")
    GUILayout.EndHorizontal()
    # file
    if sd.kfamCreateType == 2:
        GUILayout.BeginHorizontal()
        GUILayout.Label("File Name:", GUILayout.Width(80))
        sd.kfamCreateFile = GUILayout.TextField(sd.kfamCreateFile, GUILayout.Width(350))
        if GUILayout.Button("..."):
            def onSetImportClip(game, filename):
                sd.kfamCreateFile = filename
            stPath = path.join(game.pygamepath, "animeclips/")
            startFileBrower(sh, startPath=stPath, extFilter=".txt", openSave="open", title="Select a clip file to import:", onOk=onSetImportClip, onCancel=None)
        GUILayout.EndHorizontal()

    # Control buttons
    GUILayout.FlexibleSpace()
    GUILayout.BeginHorizontal()
    if GUILayout.Button("Create", btnstyle, GUILayout.Width(fullw/2-2)):
        try:
            # if import
            if sd.kfamCreateType == 2:
                clipScript = loadScriptFromFile(sd.kfamCreateFile)
                if sd.kfamImportClipName:
                    sd.kfamCreateName = clipScript["setting"]["name"]
            # check name
            sd.kfamCreateName = sd.kfamCreateName.strip()
            if len(sd.kfamCreateName) == 0:
                raise Exception("Empty clip name!")
            if sd.kfamCreateName == "cam" or sd.kfamCreateName == "sys":
                raise Exception("Reserved name as 'cam' and 'sys' can not be used as clip name!")
            if sd.actors.has_key(sd.kfamCreateName):
                raise Exception("<%s> is already registed as a actor's id!"%sd.kfamCreateName)
            if sd.props.has_key(sd.kfamCreateName):
                raise Exception("<%s> is already registed as a prop's id!"%sd.kfamCreateName)
            if mClips.has_key(sd.kfamCreateName):
                raise Exception("<%s> is already registed as a clip's name!"%sd.kfamCreateName)
            # create clip
            if sd.kfamCreateType == 0:
                newClip = KeyFrameClip(game, None)
                newClip.name = sd.kfamCreateName
            elif sd.kfamCreateType == 1:
                newClip = clip.copy(sd.kfamCreateName)
            elif sd.kfamCreateType == 2:
                newClip = KeyFrameClip(game, clipScript)
                if not sd.kfamImportClipName:
                    newClip.name = sd.kfamCreateName
            else:
                raise Exception("Unexpected Create Type!?")
            # register
            kfa_register(game, newClip)
            changeGuiScreen(sh, kfam_GUI_modify_clip, newClip)
        except Exception as e:
            scriptHelperGUIMessage("Create Clip Failed: " + str(e))
    if GUILayout.Button("Cancel", btnstyle, GUILayout.Width(fullw/2-2)):
        changeGuiScreen(sh, kfam_GUI_manager)
    GUILayout.EndHorizontal()

def kfam_GUI_modify_clip(sh):
    from UnityEngine import GUI, GUILayout, GUIStyle, Rect, Texture2D, Color, Color32, TextureFormat, RectOffset
    from System import String, Array
    fullw = sh.game.wwidth-30
    btnstyle = GUIStyle("button")
    btnstyle.fontSize = 14
    slableStyle = GUIStyle("Label")
    slableStyle.fontSize = 11
    sslableStyle = GUIStyle()
    sslableStyle.fontSize = 9
    cbwidth = fullw/6-3
    
    # shortcuts
    game = sh.game
    sd = game.scenedata
    clip = sd.kfamOnModifyClip
    mClips = game.gdata.kfaManagedClips
    sClips = game.gdata.kfaSortedClips

    # setting for modify
    if sd.kfamModifyTabIndex == -1:
        # on enter screen
        sd.kfamModifyTabIndex = 0
        sd.kfamTempName = clip.name
        sd.kfamTempPriority = "%d"%clip.priority
        sd.kfamTempType = clip.animeType
        sd.kfamTempLength = "%d"%clip.frameLength
        sd.kfamTempFPS = "%d"%clip.frameRate
        sd.kfamTempSpeed = "%.2f"%clip.speed
        sd.kfamTempLoop = "%d"%clip.loop
        sd.kfamTempAutorun = clip.autorun
        sd.kfLastOnEditId = None
        sd.kfLastOnEditFrame = -1
        sd.kfScrollPos = Vector2.zero
        sd.stScrollPos = Vector2.zero
        sd.kfSelectIndex = -1
        sd.clSelectIndex = -1
        sd.kfCurveTexture = Texture2D(100, 100, TextureFormat.RGBA32, False)
        sd.kfCurveRedraw = True
        sd.uiMore = False
        sd.uiPreset = False
        sd.uiShift = False

    def moreAction(objname):
        btnRect = Rect(fullw-100+15, 120, 100, 20)
        if GUI.Button(btnRect, "Import"):
            def onImportKeyframe(game, filename):
                try:
                    clipScript = loadScriptFromFile(filename)
                    clip.importSetting(clipScript, tgtId)
                    scriptHelperGUIMessage("Keyframes loaded.")
                except Exception as e:
                    scriptHelperGUIMessage("Fail to import setting: %s"%str(e), ("OK",))
            stPath = path.join(game.pygamepath, "keyframes/")
            startFileBrower(sh, startPath=stPath, extFilter=".txt", openSave="open", title="Select a keyframe file to import:", onOk=onImportKeyframe, onCancel=None)
        btnRect = Rect(fullw-100+15, 120+22, 100, 20)
        if len(tgtKeyframes) > 0 and GUI.Button(btnRect, "Export"):
            def onExportKeyframe(game, filename):
                try:
                    if saveStringToFile(filename, clip.exportSetting(tgtId), append=False, backup=False):
                        scriptHelperGUIMessage("All keyframes of %s(%s) were saved into <%s>."%(objname, tgtId, filename), ("OK",))
                except Exception as e:
                    scriptHelperGUIMessage("Fail to export setting: %s"%str(e), ("OK",))
            stPath = path.join(game.pygamepath, "keyframes/")
            startFileBrower(sh, startPath=stPath, extFilter=".txt", openSave="save", title="Export keyframes to:", onOk=onExportKeyframe, onCancel=None)
        btnRect = Rect(fullw-100+15, 120+22+22, 100, 20)
        if len(tgtKeyframes) > 0 and GUI.Button(btnRect, "Remove All"):
            scriptHelperGUIMessage("Delete <color=#ff0000>ALL</color> key frames for %s(%s)?"%(objname, tgtId), (("Sure, DELETE ALL!", clip.keyframes.pop, tgtId), "Cancel"))
        btnRect = Rect(fullw-100+15, 120+22+22+22, 100, 20)
        if len(tgtKeyframes) > 1 and (selectedTab == 0 or selectedTab == 2) and GUI.Button(btnRect, "Optimize"):
            scriptHelperGUIMessage("Clear <color=#ff0000>ALL unchanged status</color> in key frames for %s(%s)? Use the optimize command in <setting> tab if you want to choice which to clear."%(objname, tgtId), (("Sure, clean up!", clip.clearUnchangedStatus, tgtKeyframes[0].targetID), "Cancel"))

    def curveAndMoreAction(objname):
        # Curve Setting
        GUILayout.BeginVertical()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Curve:", GUILayout.Width(60))
        if GUILayout.Button("<<<" if sd.uiPreset else ">>>", GUILayout.Width(40)):
            sd.uiPreset = not sd.uiPreset
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("<color=#00ffff>X1:</color>", slableStyle, GUILayout.Width(25))
        newX1 = GUILayout.HorizontalSlider(sd.kfCurveData[0], 0.00, 1, GUILayout.Width(75))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("<color=#00ffff>Y1:</color>", slableStyle, GUILayout.Width(25))
        newY1 = GUILayout.HorizontalSlider(sd.kfCurveData[2], 0.00, 1, GUILayout.Width(75))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("<color=#ff00ff>X2:</color>", slableStyle, GUILayout.Width(25))
        newX2 = GUILayout.HorizontalSlider(sd.kfCurveData[1], 0.00, 1, GUILayout.Width(75))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("<color=#f00fff>Y2:</color>", slableStyle, GUILayout.Width(25))
        newY2 = GUILayout.HorizontalSlider(sd.kfCurveData[3], 0.00, 1, GUILayout.Width(75))
        GUILayout.EndHorizontal()
        GUILayout.EndVertical()
        if newX1 != sd.kfCurveData[0] or newX2 != sd.kfCurveData[1] or newY1 != sd.kfCurveData[2] or newY2 != sd.kfCurveData[3]:
            sd.kfCurveData[0] = newX1
            sd.kfCurveData[1] = newX2
            sd.kfCurveData[2] = newY1
            sd.kfCurveData[3] = newY2
            sd.kfCurveRedraw = True

        # Curve Graph or more operation buttons
        if sd.uiMore:
            sd.uiPreset = False
            moreAction(objname)
        elif sd.uiPreset:
            sd.uiMore = False
            btnRect = Rect(fullw-100+15, 120, 100, 20)
            if GUI.Button(btnRect, "Linear"):
                sd.kfCurveData = [0.2, 0.8, 0.2, 0.8]
                sd.kfCurveRedraw = True
                sd.uiPreset = False
            btnRect = Rect(fullw-100+15, 120+22, 50, 20)
            if GUI.Button(btnRect, "F-S"):
                sd.kfCurveData = [0.1, 0.6, 0.4, 0.9]
                sd.kfCurveRedraw = True
                sd.uiPreset = False
            btnRect = Rect(fullw-50+15, 120+22, 50, 20)
            if GUI.Button(btnRect, "S-F"):
                sd.kfCurveData = [0.4, 0.9, 0.1, 0.6]
                sd.kfCurveRedraw = True
                sd.uiPreset = False
            btnRect = Rect(fullw-100+15, 120+22+22, 50, 20)
            if GUI.Button(btnRect, "F-S2"):
                sd.kfCurveData = [0.0, 0.5, 0.5, 1.0]
                sd.kfCurveRedraw = True
                sd.uiPreset = False
            btnRect = Rect(fullw-50+15, 120+22+22, 50, 20)
            if GUI.Button(btnRect, "S-F2"):
                sd.kfCurveData = [0.5, 1.0, 0.0, 0.5]
                sd.kfCurveRedraw = True
                sd.uiPreset = False
            btnRect = Rect(fullw-100+15, 120+22+22+22, 50, 20)
            if GUI.Button(btnRect, "F-S-F"):
                sd.kfCurveData = [0.0, 1.0, 0.4, 0.6]
                sd.kfCurveRedraw = True
                sd.uiPreset = False
            btnRect = Rect(fullw-50+15, 120+22+22+22, 50, 20)
            if GUI.Button(btnRect, "S-F-S"):
                sd.kfCurveData = [0.4, 0.6, 0.0, 1.0]
                sd.kfCurveRedraw = True
                sd.uiPreset = False
            btnRect = Rect(fullw-100+15, 120+22+22+22+22, 50, 20)
            if GUI.Button(btnRect, "Copy"):
                sd.kfCurveDataCopy = copy.copy(sd.kfCurveData)
                sd.uiPreset = False
            btnRect = Rect(fullw-50+15, 120+22+22+22+22, 50, 20)
            if GUI.Button(btnRect, "Paste"):
                if hasattr(sd, "kfCurveDataCopy"):
                    sd.kfCurveData = copy.copy(sd.kfCurveDataCopy)
                    sd.kfCurveRedraw = True
                else:
                    scriptHelperGUIMessage("Copy a curve data first.")
                sd.uiPreset = False
        else:
            curveRect = Rect(fullw-100+15, 120, 100, 100)
            if sd.kfCurveRedraw and not clip.isPlaying:
                drawCurve(sd.kfCurveTexture, sd.kfCurveData)
                sd.kfCurveRedraw = False
                # auto update curve setting
                if selectedTab == 0:    # actor/prop
                    (tgtId, tgtObj) = selectTaggedActorOrProp(game)
                    if tgtId and tgtObj and clip.keyframes.has_key(tgtId):
                        for kf in clip.keyframes[tgtId]:
                            if kf.frameNo == curFrame:
                                kf.curve = copy.copy(sd.kfCurveData)
                                break
                elif selectedTab == 1:  # camera
                    if clip.keyframes.has_key("cam"):
                        for kf in clip.keyframes["cam"]:
                            if kf.frameNo == curFrame:
                                kf.curve = copy.copy(sd.kfCurveData)
                elif selectedTab == 2:  # system
                    if clip.keyframes.has_key("sys"):
                        for kf in clip.keyframes["sys"]:
                            if kf.frameNo == curFrame:
                                kf.curve = copy.copy(sd.kfCurveData)
                else:   # no curve for clip or setting
                    pass
            GUI.DrawTexture(curveRect, sd.kfCurveTexture)
            labelRect = Rect(fullw-100+15, 220+1, 100, 20)
            GUI.Label(labelRect, "<color=#00ffff>(%.2f,%.2f)</color>  <color=#f00fff>(%.2f,%.2f)</color>"%(newX1, newY1, newX2, newY2), sslableStyle)
        
    # play control
    GUILayout.BeginHorizontal()
    newframe = GUILayout.HorizontalSlider(clip.curFrame, 0, clip.frameLength, GUILayout.Width(fullw))
    if not clip.isPlaying and int(newframe) != int(clip.curFrame):
        clip.seek(int(newframe))
    GUILayout.EndHorizontal()
    GUILayout.BeginHorizontal()
    if GUILayout.Button("||" if clip.isPlaying else u'\u25b6', GUILayout.Width(23)):
        if clip.isPlaying:
            clip.pause()
        else:
            clip.play()
    if GUILayout.Button(u'\u25a0', GUILayout.Width(23)):
        clip.stop()
    if GUILayout.Button("|<", GUILayout.Width(23)):
        clip.seek(0)
    if GUILayout.Button("<<", GUILayout.Width(23)):
        newframe = 0 if clip.curFrame < clip.frameRate else clip.curFrame -  clip.frameRate
        clip.seek(newframe)
    if GUILayout.Button("<", GUILayout.Width(23)):
        newframe = 0 if clip.curFrame < 1 else clip.curFrame - 1
        clip.seek(newframe)
    GUILayout.Label("%d/%d %.2fs/%.2fs"%(clip.curFrame, clip.frameLength, clip.curFrame/float(clip.frameRate), clip.frameLength/float(clip.frameRate)))
    if GUILayout.Button(">", GUILayout.Width(23)):
        newframe = clip.frameLength if clip.curFrame + 1 >= clip.frameLength else clip.curFrame + 1
        clip.seek(newframe)
    if GUILayout.Button(">>", GUILayout.Width(23)):
        newframe = clip.frameLength if clip.curFrame + clip.frameRate >= clip.frameLength else clip.curFrame +  clip.frameRate
        clip.seek(newframe)
    if GUILayout.Button(">|", GUILayout.Width(23)):
        clip.seek(clip.frameLength)
    GUILayout.EndHorizontal()

    # edit tabs
    GUILayout.BeginHorizontal()
    tabs = ["Actor/Prop", "Camera", "System", "Clip", "Setting"]
    if sd.kfamModifyTabIndex >= 0:
        tabs[sd.kfamModifyTabIndex] = "<color=#00ffff>" + tabs[sd.kfamModifyTabIndex] + "</color>"
    selectedTab = GUILayout.SelectionGrid(sd.kfamModifyTabIndex, Array[String](tabs), 5)
    if selectedTab != sd.kfamModifyTabIndex:
        # on tab change
        sd.kfamModifyTabIndex = selectedTab
        sd.kfLastOnEditId = None
        sd.kfLastOnEditFrame = -1
        sd.kfScrollPos = Vector2.zero
        sd.stScrollPos = Vector2.zero
        sd.kfSelectIndex = -1
        sd.clSelectIndex = -1
        sd.kfCurveRedraw = True
        sd.uiMore = False
        sd.uiPreset = False
        sd.uiShift = False
    GUILayout.EndHorizontal()

    # tab area
    if selectedTab == 0:    # actor/prop
        (tgtId, tgtObj) = selectTaggedActorOrProp(game)
        GUILayout.BeginHorizontal() # start actor/prop tab
        if tgtObj:
            if tgtId:
                pass
            else:
                GUILayout.Label("Selected object <%s> is not tagged yet."%tgtObj.text_name)
        else:
            GUILayout.Label("Selected an object to create animation.")
        # edit selected
        if tgtObj and tgtId:
            # prepare data
            tgtKeyframes = [] if not clip.keyframes.has_key(tgtId) else clip.keyframes[tgtId]
            tgtKeyframeNoList = [kf.frameNo for kf in tgtKeyframes]
            curStatus = tgtObj.export_full_status()
            curFrame = int(clip.curFrame)
            statusKeyList, statusKeyTranslateDict = translateAndSortStatusKeys(curStatus.keys())
            isKey = tgtKeyframeNoList.count(curFrame) > 0
            if isKey:
                keyIndex = tgtKeyframeNoList.index(curFrame)
            if sd.kfLastOnEditId != tgtId or sd.kfLastOnEditFrame != curFrame:
                # on actor/prop change or frame change
                sd.kfLastOnEditId = tgtId
                sd.kfLastOnEditFrame = curFrame
                sd.kfCurveRedraw = True
                sd.uiMore = False
                sd.uiPreset = False
                if isKey:
                    sd.kfSelectIndex = keyIndex
                    sd.kfCurveData = copy.copy(tgtKeyframes[keyIndex].curve)
                else:
                    sd.uiShift = False
                    sd.kfSelectIndex = -1
                    if not hasattr(sd, "kfCurveData"):
                        sd.kfCurveData = [0.2, 0.8, 0.2, 0.8]
                if not hasattr(sd, "apStatusSelection"):
                    sd.apStatusSelection = {}
                for st in statusKeyList:
                    if isKey:
                        sd.apStatusSelection[st] = tgtKeyframes[keyIndex].status.has_key(st)
                    elif not sd.apStatusSelection.has_key(st):
                        sd.apStatusSelection[st] = True
                for st in sd.apStatusSelection.keys():
                    if not st in statusKeyList:
                        sd.apStatusSelection.pop(st)

            # char name and key frame prompt
            if len(tgtKeyframes) > 0:
                stsMsg = "%d key frames"%len(tgtKeyframes)
                if isKey:
                    stsMsg += "<color=#ff0000> [KeyFrame]</color>"
            else:
                stsMsg = "No key frames"
            GUILayout.Label("[%s (%s)]: %s"%(tgtObj.text_name, tgtId, stsMsg), GUILayout.Width(fullw-100-4))
            if GUILayout.Button("- Hide -" if sd.uiMore else "+ More +", GUILayout.Width(100)):
                sd.uiMore = not sd.uiMore
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()

            # keyframe scroll list
            sd.kfScrollPos = GUILayout.BeginScrollView(sd.kfScrollPos, GUILayout.Width(80), GUILayout.Height(115))
            newKeyFrameIdx = GUILayout.SelectionGrid(sd.kfSelectIndex, Array[String](tuple(str(n) for n in tgtKeyframeNoList)), 1)
            if newKeyFrameIdx != sd.kfSelectIndex:
                clip.seek(tgtKeyframes[newKeyFrameIdx].frameNo)
            GUILayout.EndScrollView()

            # status scroll list
            sd.stScrollPos = GUILayout.BeginScrollView(sd.stScrollPos, GUILayout.Width(180), GUILayout.Height(115))
            GUILayout.BeginHorizontal()
            if GUILayout.Button("All"):
                for st in statusKeyList:
                    sd.apStatusSelection[st] = True
            if GUILayout.Button("None"):
                for st in statusKeyList:
                    sd.apStatusSelection[st] = False
            if GUILayout.Button("Ref"):
                prevKey = [kfn for kfn in tgtKeyframeNoList if kfn <= curFrame]
                if len(prevKey) > 0:
                    pi = tgtKeyframeNoList.index(prevKey[-1])
                    refStatus = tgtKeyframes[pi].status
                    for st in statusKeyList:
                        sd.apStatusSelection[st] = refStatus.has_key(st)
                else:
                    for st in statusKeyList:
                        sd.apStatusSelection[st] = True
            if GUILayout.Button("Diff"):
                prevKey = [kfn for kfn in tgtKeyframeNoList if kfn <= curFrame]
                if len(prevKey) > 0:
                    pi = tgtKeyframeNoList.index(prevKey[-1])
                    refStatus = tgtKeyframes[pi].status
                    for st in statusKeyList:
                        sd.apStatusSelection[st] = refStatus.has_key(st) and refStatus[st] != curStatus[st]
                else:
                    for st in statusKeyList:
                        sd.apStatusSelection[st] = True
            GUILayout.EndHorizontal()
            for st in statusKeyList:
                if sd.apStatusSelection[st]:
                    sd.apStatusSelection[st] = GUILayout.Toggle(sd.apStatusSelection[st], statusKeyTranslateDict[st])
            for st in statusKeyList:
                if not sd.apStatusSelection[st]:
                    sd.apStatusSelection[st] = GUILayout.Toggle(sd.apStatusSelection[st], statusKeyTranslateDict[st])
            GUILayout.EndScrollView()

            # Curve Setting
            curveAndMoreAction(tgtObj.text_name)

        GUILayout.EndHorizontal()   # end actor/prop tab

    elif selectedTab == 1:  # camera
        GUILayout.BeginHorizontal() # start camera tab
        tgtId = "cam"
        tgtObj = "Camera"
        # prepare data
        from Studio import Studio
        studio = Studio.Instance
        c = studio.cameraCtrl
        cdata = c.cameraData
        tgtKeyframes = [] if not clip.keyframes.has_key(tgtId) else clip.keyframes[tgtId]
        tgtKeyframeNoList = [kf.frameNo for kf in tgtKeyframes]
        curFrame = int(clip.curFrame)
        isKey = tgtKeyframeNoList.count(curFrame) > 0
        if isKey:
            keyIndex = tgtKeyframeNoList.index(curFrame)
        if sd.kfLastOnEditFrame != curFrame:
            # on frame change
            sd.kfLastOnEditFrame = curFrame
            sd.kfCurveRedraw = True
            sd.uiMore = False
            sd.uiPreset = False
            if isKey:
                sd.kfSelectIndex = keyIndex
                sd.kfCurveData = copy.copy(tgtKeyframes[keyIndex].curve)
            else:
                sd.uiShift = False
                sd.kfSelectIndex = -1
                if not hasattr(sd, "kfCurveData"):
                    sd.kfCurveData = [0.2, 0.8, 0.2, 0.8]

        # char name and key frame prompt
        if len(tgtKeyframes) > 0:
            stsMsg = "%d key frames"%len(tgtKeyframes)
            if isKey:
                stsMsg += "<color=#ff0000> [KeyFrame]</color>"
        else:
            stsMsg = "No key frames"
        GUILayout.Label("[%s]: %s"%(tgtObj, stsMsg), GUILayout.Width(fullw-100-4))
        if GUILayout.Button("- Hide -" if sd.uiMore else "+ More +", GUILayout.Width(100)):
            sd.uiMore = not sd.uiMore
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()

        # keyframe scroll list
        sd.kfScrollPos = GUILayout.BeginScrollView(sd.kfScrollPos, GUILayout.Width(80), GUILayout.Height(115))
        newKeyFrameIdx = GUILayout.SelectionGrid(sd.kfSelectIndex, Array[String](tuple(str(n) for n in tgtKeyframeNoList)), 1)
        if newKeyFrameIdx != sd.kfSelectIndex:
            clip.seek(tgtKeyframes[newKeyFrameIdx].frameNo)
        GUILayout.EndScrollView()

        # camera status
        GUILayout.BeginVertical(GUILayout.Width(180), GUILayout.Height(115))
        GUILayout.BeginHorizontal()
        GUILayout.Label("Pos: %.1f, %.1f, %.1f"%(cdata.pos.x, cdata.pos.y, cdata.pos.z))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Rot: %.1f, %.1f, %.1f"%(cdata.rotate.x, cdata.rotate.y, cdata.rotate.z))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Distance: %.1f"%(cdata.distance.z))
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("FieldOfView: %.1f"%(c.fieldOfView))
        if GUILayout.Button("<", GUILayout.Width(18)):
            c.fieldOfView -= 1
        if GUILayout.Button(">", GUILayout.Width(18)):
            c.fieldOfView += 1
        GUILayout.EndHorizontal()
        GUILayout.EndVertical()

        # curve
        curveAndMoreAction(tgtObj)

        GUILayout.EndHorizontal()   # end camera tab

    elif selectedTab == 2:  # system
        GUILayout.BeginHorizontal() # start system tab
        tgtId = "sys"
        tgtObj = "System"
        # prepare data
        tgtKeyframes = [] if not clip.keyframes.has_key(tgtId) else clip.keyframes[tgtId]
        tgtKeyframeNoList = [kf.frameNo for kf in tgtKeyframes]
        curStatus = export_sys_status(game)
        curFrame = int(clip.curFrame)
        statusKeyList, statusKeyTranslateDict = translateAndSortStatusKeys(curStatus.keys())
        isKey = tgtKeyframeNoList.count(curFrame) > 0
        if isKey:
            keyIndex = tgtKeyframeNoList.index(curFrame)
        if sd.kfLastOnEditFrame != curFrame:
            # on frame change
            sd.kfLastOnEditFrame = curFrame
            sd.kfCurveRedraw = True
            sd.uiMore = False
            sd.uiPreset = False
            if isKey:
                sd.kfSelectIndex = keyIndex
                sd.kfCurveData = copy.copy(tgtKeyframes[keyIndex].curve)
            else:
                sd.uiShift = False
                sd.kfSelectIndex = -1
                if not hasattr(sd, "kfCurveData"):
                    sd.kfCurveData = [0.2, 0.8, 0.2, 0.8]
            if not hasattr(sd, "apStatusSelection"):
                sd.apStatusSelection = {}
            for st in statusKeyList:
                if isKey:
                    sd.apStatusSelection[st] = tgtKeyframes[keyIndex].status.has_key(st)
                elif not sd.apStatusSelection.has_key(st):
                    sd.apStatusSelection[st] = True
            for st in sd.apStatusSelection.keys():
                if not st in statusKeyList:
                    sd.apStatusSelection.pop(st)

        # char name and key frame prompt
        if len(tgtKeyframes) > 0:
            stsMsg = "%d key frames"%len(tgtKeyframes)
            if isKey:
                stsMsg += "<color=#ff0000> [KeyFrame]</color>"
        else:
            stsMsg = "No key frames"
        GUILayout.Label("[%s]: %s"%(tgtObj, stsMsg), GUILayout.Width(fullw-100-4))
        if GUILayout.Button("- Hide -" if sd.uiMore else "+ More +", GUILayout.Width(100)):
            sd.uiMore = not sd.uiMore
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()

        # keyframe scroll list
        sd.kfScrollPos = GUILayout.BeginScrollView(sd.kfScrollPos, GUILayout.Width(80), GUILayout.Height(115))
        newKeyFrameIdx = GUILayout.SelectionGrid(sd.kfSelectIndex, Array[String](tuple(str(n) for n in tgtKeyframeNoList)), 1)
        if newKeyFrameIdx != sd.kfSelectIndex:
            clip.seek(tgtKeyframes[newKeyFrameIdx].frameNo)
        GUILayout.EndScrollView()

        # status scroll list
        sd.stScrollPos = GUILayout.BeginScrollView(sd.stScrollPos, GUILayout.Width(180), GUILayout.Height(115))
        GUILayout.BeginHorizontal()
        if GUILayout.Button("All"):
            for st in statusKeyList:
                sd.apStatusSelection[st] = True
        if GUILayout.Button("None"):
            for st in statusKeyList:
                sd.apStatusSelection[st] = False
        if GUILayout.Button("Ref"):
            prevKey = [kfn for kfn in tgtKeyframeNoList if kfn <= curFrame]
            if len(prevKey) > 0:
                pi = tgtKeyframeNoList.index(prevKey[-1])
                refStatus = tgtKeyframes[pi].status
                for st in statusKeyList:
                    sd.apStatusSelection[st] = refStatus.has_key(st)
            else:
                for st in statusKeyList:
                    sd.apStatusSelection[st] = True
        if GUILayout.Button("Diff"):
            prevKey = [kfn for kfn in tgtKeyframeNoList if kfn <= curFrame]
            if len(prevKey) > 0:
                pi = tgtKeyframeNoList.index(prevKey[-1])
                refStatus = tgtKeyframes[pi].status
                for st in statusKeyList:
                    sd.apStatusSelection[st] = refStatus.has_key(st) and refStatus[st] != curStatus[st]
            else:
                for st in statusKeyList:
                    sd.apStatusSelection[st] = True
        GUILayout.EndHorizontal()
        for st in statusKeyList:
            if sd.apStatusSelection[st]:
                sd.apStatusSelection[st] = GUILayout.Toggle(sd.apStatusSelection[st], statusKeyTranslateDict[st])
        for st in statusKeyList:
            if not sd.apStatusSelection[st]:
                sd.apStatusSelection[st] = GUILayout.Toggle(sd.apStatusSelection[st], statusKeyTranslateDict[st])
        GUILayout.EndScrollView()

        # Curve Setting
        curveAndMoreAction(tgtObj)

        GUILayout.EndHorizontal()   # end actor/prop tab
    
    elif selectedTab == 3:  # clips
        GUILayout.BeginHorizontal() # start clip tab
        # clip scroll list
        clipNames = [c.name for c in sClips if c != clip]
        clipListNames = []
        for cn in clipNames:
            if clip.keyframes.has_key(cn):
                clipListNames.append("<color=#00ffff>" + cn + "</color>")
            else:
                clipListNames.append(cn)
        sd.stScrollPos = GUILayout.BeginScrollView(sd.stScrollPos, GUILayout.Width(100), GUILayout.Height(130))
        newClipIdx = GUILayout.SelectionGrid(sd.clSelectIndex, Array[String](tuple(clipListNames)), 1)
        if newClipIdx != sd.clSelectIndex:
            # on clip change
            sd.clSelectIndex = newClipIdx
            sd.kfLastOnEditFrame = -1   # force reset curframe info
            sd.clstPlay = 0
            sd.clstFrame = "0"
            sd.clstLoop = "-1"
            sd.clstSpeed = "1"
        if len(clipNames) == 0:
            sd.clSelectIndex = -1
        GUILayout.EndScrollView()
        if sd.clSelectIndex == -1:
            tgtId = None
            tgtObj = None
        else:
            tgtId = clipNames[sd.clSelectIndex]
            tgtObj = mClips[tgtId]

        # edit selected
        if tgtObj and tgtId:
            # prepare data
            tgtKeyframes = [] if not clip.keyframes.has_key(tgtId) else clip.keyframes[tgtId]
            tgtKeyframeNoList = [kf.frameNo for kf in tgtKeyframes]
            curFrame = int(clip.curFrame)
            statusKeyList = ("play", "frame", "loop", "speed")
            isKey = tgtKeyframeNoList.count(curFrame) > 0
            if isKey:
                keyIndex = tgtKeyframeNoList.index(curFrame)
            if sd.kfLastOnEditFrame != curFrame:
                # on frame change
                sd.kfLastOnEditFrame = curFrame
                if isKey:
                    sd.kfSelectIndex = keyIndex
                    if tgtKeyframes[keyIndex].status.has_key('play'):
                        sd.clstPlay = tgtKeyframes[keyIndex].status['play']
                    if tgtKeyframes[keyIndex].status.has_key('frame'):
                        sd.clstFrame = "%d"%tgtKeyframes[keyIndex].status['frame']
                    if tgtKeyframes[keyIndex].status.has_key('loop'):
                        sd.clstLoop = "%d"%tgtKeyframes[keyIndex].status['loop']
                    if tgtKeyframes[keyIndex].status.has_key('speed'):
                        sd.clstSpeed = "%.2f"%tgtKeyframes[keyIndex].status['speed']
                else:
                    sd.kfSelectIndex = -1
                if not hasattr(sd, "apStatusSelection"):
                    sd.apStatusSelection = {}
                for st in statusKeyList:
                    if isKey:
                        sd.apStatusSelection[st] = tgtKeyframes[keyIndex].status.has_key(st)
                    elif not sd.apStatusSelection.has_key(st):
                        sd.apStatusSelection[st] = False
                for st in sd.apStatusSelection.keys():
                    if not st in statusKeyList:
                        sd.apStatusSelection.pop(st)

            # clip name and key frame prompt
            GUILayout.BeginVertical() 
            if len(tgtKeyframes) > 0:
                stsMsg = "%d key frames"%len(tgtKeyframes)
                if isKey:
                    stsMsg += "<color=#ff0000> [KeyFrame]</color>"
            else:
                stsMsg = "No key frames"
            GUILayout.BeginHorizontal()
            GUILayout.Label("[Clip %s]: %s"%(tgtId, stsMsg), GUILayout.Width(fullw-100-4-100))
            if GUILayout.Button("- Hide -" if sd.uiMore else "+ More +", GUILayout.Width(100)):
                sd.uiMore = not sd.uiMore
            GUILayout.EndHorizontal()

            # keyframe scroll list
            GUILayout.BeginHorizontal()
            sd.kfScrollPos = GUILayout.BeginScrollView(sd.kfScrollPos, GUILayout.Width(80), GUILayout.Height(95))
            newKeyFrameIdx = GUILayout.SelectionGrid(sd.kfSelectIndex, Array[String](tuple(str(n) for n in tgtKeyframeNoList)), 1)
            if newKeyFrameIdx != sd.kfSelectIndex:
                clip.seek(tgtKeyframes[newKeyFrameIdx].frameNo)
            GUILayout.EndScrollView()

            GUILayout.BeginVertical()
            GUILayout.BeginHorizontal()
            sd.apStatusSelection['play'] = GUILayout.Toggle(sd.apStatusSelection['play'], "Play:", GUILayout.Width(60))
            if sd.clstPlay == 0:
                playbtn = "<color=#ff0000>Stop</color>"
            elif sd.clstPlay == 1:
                playbtn = "<color=#00ff00>Play</color>"
            else:
                playbtn = "<color=#ffff00>Pause</color>"
            if sd.apStatusSelection['play'] and GUILayout.Button(playbtn, GUILayout.Width(60)):
                sd.clstPlay += 1
                sd.clstPlay %= 3
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            sd.apStatusSelection['frame'] = GUILayout.Toggle(sd.apStatusSelection['frame'], "Frame:", GUILayout.Width(60))
            if sd.apStatusSelection['frame']:
                sd.clstFrame = GUILayout.TextField(sd.clstFrame, GUILayout.Width(60))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            sd.apStatusSelection['loop'] = GUILayout.Toggle(sd.apStatusSelection['loop'], "Loop:", GUILayout.Width(60))
            if sd.apStatusSelection['loop']:
                sd.clstLoop = GUILayout.TextField(sd.clstLoop, GUILayout.Width(60))
            GUILayout.EndHorizontal()
            GUILayout.BeginHorizontal()
            sd.apStatusSelection['speed'] = GUILayout.Toggle(sd.apStatusSelection['speed'], "Speed:", GUILayout.Width(60))
            if sd.apStatusSelection['speed']:
                sd.clstSpeed = GUILayout.TextField(sd.clstSpeed, GUILayout.Width(60))
            GUILayout.EndHorizontal()
            GUILayout.EndVertical()
            GUILayout.EndHorizontal()
            GUILayout.EndVertical()

            # more button
            if sd.uiMore:
                sd.uiPreset = False
                moreAction(tgtId)

        else:
            GUILayout.Label("Selected an clip to create animation.")

        GUILayout.EndHorizontal()   # end clip tab

    else:   # settings
        GUILayout.BeginHorizontal()
        GUILayout.Label("Name:", GUILayout.Width(50))
        sd.kfamTempName = GUILayout.TextField(sd.kfamTempName, GUILayout.Width(100))
        GUILayout.Space(5)
        GUILayout.Label("Priority:", GUILayout.Width(55))
        sd.kfamTempPriority = GUILayout.TextField(sd.kfamTempPriority, GUILayout.Width(40))
        GUILayout.Space(5)
        sd.kfamTempAutorun = GUILayout.Toggle(sd.kfamTempAutorun, "Auto run on load")
        #GUILayout.Label("Type:", GUILayout.Width(40))
        #if GUILayout.Button(sd.kfamTempType if sd.kfamTempType == "absolute" else "<i>" + sd.kfamTempType + "</i>", GUILayout.Width(100)):
        #    if sd.kfamTempType == "absolute":
        #        sd.kfamTempType = "relative"
        #    else:
        #        sd.kfamTempType = "absolute"
        GUILayout.EndHorizontal()
        GUILayout.BeginHorizontal()
        GUILayout.Label("Length:", GUILayout.Width(50))
        sd.kfamTempLength = GUILayout.TextField(sd.kfamTempLength, GUILayout.Width(60))
        GUILayout.Space(5)
        GUILayout.Label("FPS:", GUILayout.Width(45))
        sd.kfamTempFPS = GUILayout.TextField(sd.kfamTempFPS, GUILayout.Width(35))
        GUILayout.Space(5)
        GUILayout.Label("Speed:", GUILayout.Width(50))
        sd.kfamTempSpeed = GUILayout.TextField(sd.kfamTempSpeed, GUILayout.Width(45))
        GUILayout.Space(5)
        GUILayout.Label("Loop:", GUILayout.Width(50))
        sd.kfamTempLoop = GUILayout.TextField(sd.kfamTempLoop, GUILayout.Width(40))
        GUILayout.EndHorizontal()
        # content list
        GUILayout.BeginHorizontal()
        GUILayout.Label("Content:", GUILayout.Width(60))
        sd.kfScrollPos = GUILayout.BeginScrollView(sd.kfScrollPos, GUILayout.Height(80))
        for kfId in clip.keyframes.keys():
            GUILayout.BeginHorizontal()
            if kfId in sd.actors:
                cName = "<color=#ff0000>Actor</color>:" + sd.actors[kfId].text_name + "(" + kfId + ")"
            elif kfId in sd.props:
                cName = "<color=#00ff00>Prop</color>:" + sd.props[kfId].text_name + "(" + kfId + ")"
            elif kfId in mClips:
                cName = "<color=#00ffff>Clip</color>:" + mClips[kfId].name
            elif kfId == "cam":
                cName = "<color=#ffff00>Camera</color>"
            elif kfId == "sys":
                cName = "<color=#ffff00>System</color>"
            else:
                cName = "<color=#ff0000>Unknown!?</color>"
            cKfCount = len(clip.keyframes[kfId])
            if cKfCount:
                cKfMin = clip.keyframes[kfId][0].frameNo
                cKfMax = clip.keyframes[kfId][-1].frameNo
                info = "%s with %d keyframes from %d to %d"%(cName, cKfCount, cKfMin, cKfMax)
            else:
                info = "%s with no keyframe"%(cName)
            GUILayout.Label(info)
            GUILayout.EndHorizontal()
        GUILayout.EndScrollView()
        GUILayout.EndHorizontal()

    # Control buttons
    GUILayout.FlexibleSpace()
    if selectedTab in {0, 1, 2, 3}: # for keyframe
        GUILayout.BeginHorizontal()
        if not sd.uiShift:
            # normal mode
            if tgtObj:
                if tgtId:
                    if GUILayout.Button("Create" if not isKey else "Update", btnstyle, GUILayout.Width(cbwidth)):
                        try:
                            if selectedTab == 0:    # actor/prop
                                # check
                                saveStKey = [i for i in sd.apStatusSelection.keys() if sd.apStatusSelection[i]]
                                if len(saveStKey) == 0:
                                    raise Exception("No property selected!")
                                saveStatus = {}
                                for sk in saveStKey:
                                    saveStatus[sk] = curStatus[sk]
                                # build
                                from vnactor import Actor, Prop
                                if isinstance(tgtObj, Actor):
                                    newkf = ActorKeyFrame(curFrame, tgtId, saveStatus, sd.kfCurveData)
                                elif isinstance(tgtObj, Prop):
                                    newkf = PropKeyFrame(curFrame, tgtId, saveStatus, sd.kfCurveData)
                                else:
                                    print "tgtObj", tgtObj
                                    print "tgtId", tgtId
                                    raise Exception("Unknown target type: " + str(type(tgtObj)))
                            elif selectedTab == 1:  # camera
                                newkf = CameraKeyFrame(curFrame, sd.kfCurveData)
                            elif selectedTab == 2:  # system
                                # check
                                saveStKey = [i for i in sd.apStatusSelection.keys() if sd.apStatusSelection[i]]
                                if len(saveStKey) == 0:
                                    raise Exception("No property selected!")
                                saveStatus = {}
                                for sk in saveStKey:
                                    saveStatus[sk] = curStatus[sk]
                                newkf = SystemKeyFrame(curFrame, saveStatus, sd.kfCurveData)
                            elif selectedTab == 3:  # clip
                                # check
                                saveStKey = [i for i in sd.apStatusSelection.keys() if sd.apStatusSelection[i]]
                                if len(saveStKey) == 0:
                                    raise Exception("No property selected!")
                                # convert
                                saveStatus = {}
                                if sd.apStatusSelection['play']:
                                    saveStatus['play'] = sd.clstPlay
                                if sd.apStatusSelection['frame']:
                                    saveStatus['frame'] = int(sd.clstFrame)
                                if sd.apStatusSelection['loop']:
                                    saveStatus['loop'] = int(sd.clstLoop)
                                if sd.apStatusSelection['speed']:
                                    saveStatus['speed'] = float(sd.clstSpeed)
                                newkf = ClipKeyFrame(curFrame, tgtId, saveStatus)
                            else:
                                raise Exception("Unknown keyframe type")
                            # create/update
                            if not isKey or sh.masterMode:
                                clip.updateKeyFrame(newkf)
                            else:
                                def toClipboard():
                                    clip.clipboard = newkf
                                scriptHelperGUIMessage("Update key frame at <color=#ff0000>#%d</color> with current status?\nUpdate will overwrite the old status of current keyframe. If you want to make a new keyframe with current status, select [To Clipboard] and then paste on target frame later."%(curFrame), (("Update", clip.updateKeyFrame, newkf), ("To Clipboard", toClipboard), "Cancel"))
                        except Exception as e:
                            scriptHelperGUIMessage(str(e))
                else:
                    if GUILayout.Button("Tag it", btnstyle, GUILayout.Width(cbwidth)):
                        sh.tag_select()
            else:
                GUILayout.Button("", btnstyle, GUILayout.Width(cbwidth))
            if clip.isPlaying:
                GUILayout.Button(" ", btnstyle, GUILayout.Width(cbwidth))
                GUILayout.Button(" ", btnstyle, GUILayout.Width(cbwidth))
                GUILayout.Button(" ", btnstyle, GUILayout.Width(cbwidth))
                GUILayout.Button(" ", btnstyle, GUILayout.Width(cbwidth))
            else:
                if GUILayout.Button("Delete" if tgtId and isKey else "", btnstyle, GUILayout.Width(cbwidth)) and tgtId and isKey:
                    def onDeleteKeyframe():
                        clip.deleteKeyFrame(tgtId)
                        sd.kfSelectIndex = -1
                    scriptHelperGUIMessage("Delete key frame at #%d?"%(curFrame), (("Delete", onDeleteKeyframe), "Cancel"))
                if GUILayout.Button("Shift" if tgtId and isKey else "", btnstyle, GUILayout.Width(cbwidth)) and tgtId and isKey:
                    if not hasattr(sd, "shiftFollowers"):
                        sd.shiftFollowers = False
                    sd.shiftInput = "0"
                    sd.uiShift = True
                if GUILayout.Button("Copy" if tgtId and isKey else "", btnstyle, GUILayout.Width(cbwidth)) and tgtId and isKey:
                    scriptHelperGUIMessage("Keyframe at frame %d was copied into the clipboard."%(curFrame))
                    clip.copyKeyFrame(tgtId)
                if GUILayout.Button("Paste" if tgtId and clip.canPasteKeyFrame(tgtId) else "", btnstyle, GUILayout.Width(cbwidth)) and tgtId and clip.canPasteKeyFrame(tgtId):
                    clip.pasteKeyFrame(tgtId)
                    clip.applyFrames()
            if GUILayout.Button("Back", btnstyle, GUILayout.Width(cbwidth)):
                changeGuiScreen(sh, kfam_GUI_manager)
        else:
            # shift mode
            if keyIndex == 0:
                sfMin = -curFrame
            else:
                sfMin = tgtKeyframeNoList[keyIndex - 1] - curFrame + 1
            if sd.shiftFollowers or curFrame == tgtKeyframeNoList[-1]:
                sfMax = clip.frameLength - tgtKeyframeNoList[-1]
            else:
                sfMax = tgtKeyframeNoList[keyIndex + 1] - curFrame - 1
            # shift UI
            GUILayout.Label("Shift (%d - %d)"%(sfMin, sfMax), GUILayout.Width(110))
            sd.shiftInput = GUILayout.TextField(sd.shiftInput, GUILayout.Width(40))
            GUILayout.Label("frames", GUILayout.Width(40))
            sd.shiftFollowers = GUILayout.Toggle(sd.shiftFollowers, "with followers", GUILayout.Width(110))
            if GUILayout.Button("Apply", btnstyle, GUILayout.Width(cbwidth)):
                try:
                    sfNum = int(sd.shiftInput)
                    if sfNum > sfMax:
                        raise Exception("Shift step is too big. (Max = %d)"%sfMax)
                    if sfNum < sfMin:
                        raise Exception("Shift step is too small. (Min = %d)"%sfMin)
                    clip.shiftKeyFrame(tgtId, sfNum, sd.shiftFollowers)
                    clip.seek(curFrame + sfNum)
                    sd.uiShift = False
                except Exception as e:
                    scriptHelperGUIMessage("Shift keyframe failed: " + str(e))
            if GUILayout.Button("Cancel", btnstyle, GUILayout.Width(cbwidth)):
                sd.uiShift = False
        GUILayout.EndHorizontal()
    else:   # for setting
        GUILayout.BeginHorizontal()
        settingModified = sd.kfamTempName != clip.name or sd.kfamTempPriority != "%d"%clip.priority or sd.kfamTempType != clip.animeType or sd.kfamTempLength != "%d"%clip.frameLength or sd.kfamTempFPS != "%d"%clip.frameRate or sd.kfamTempSpeed != "%.2f"%clip.speed or sd.kfamTempLoop != "%d"%clip.loop or sd.kfamTempAutorun != clip.autorun
        if GUILayout.Button("Apply" if settingModified else "", btnstyle, GUILayout.Width(cbwidth)) and settingModified:
            try:
                oldName = clip.name
                name = sd.kfamTempName.strip()
                if len(name) == 0:
                    raise Exception("Clip name can not be empty!")
                if name != clip.name and mClips.has_key(name):
                    raise Exception("Clip name dupulicated!")
                priority = int(sd.kfamTempPriority)
                frameLength = int(sd.kfamTempLength)
                if frameLength < clip.lastFrameNo:
                    raise Exception("Clip's length must be equal or greater than last key frame No. #%d!"%clip.lastFrameNo)
                frameRate = int(sd.kfamTempFPS)
                speed = float(sd.kfamTempSpeed)
                loop = int(sd.kfamTempLoop)
                if name != clip.name:
                    kfa_rename(game, oldName, name)
                if priority != clip.priority:
                    kfa_resort(game, name, priority)
                    sd.kfamSelectedClipIndex = -1
                if sd.kfamTempType != clip.animeType:
                    kfa_retype(game, name, sd.kfamTempType)
                clip.frameLength = frameLength
                clip.frameRate = frameRate
                clip.speed = speed
                clip.loop = loop
                clip.autorun = sd.kfamTempAutorun
            except Exception as e:
                scriptHelperGUIMessage("Apply setting failed: " + str(e))
        if GUILayout.Button("Import", btnstyle, GUILayout.Width(cbwidth)):
            def onImportClip(game, filename):
                try:
                    clipScript = loadScriptFromFile(filename)
                    oldName = clip.name
                    oldPriority = clip.priority
                    oldAnimeType = clip.animeType
                    clip.importSetting(clipScript)
                    clip.name = oldName # do not change clip name when import
                    if oldPriority != clip.priority:
                        kfa_resort(game, clip.name, clip.priority)
                        sd.kfamSelectedClipIndex = -1
                    if sd.kfamTempType != clip.animeType:
                        kfa_retype(game, clip.name, clip.animeType)
                    scriptHelperGUIMessage("Key frame anime clip loaded.")
                except Exception as e:
                    scriptHelperGUIMessage("Fail to import setting: %s"%str(e), ("OK",))
            stPath = path.join(game.pygamepath, "animeclips/")
            startFileBrower(sh, startPath=stPath, extFilter=".txt", openSave="open", title="Select a clip file to import:", onOk=onImportClip, onCancel=None)
        if GUILayout.Button("Export", btnstyle, GUILayout.Width(cbwidth)):
            def onExportClip(game, filename):
                if saveStringToFile(filename, clip.exportSetting(), append=False, backup=True):
                    scriptHelperGUIMessage("All clip settings and keyframes were saved into <%s>."%filename, ("OK",))
            stPath = path.join(game.pygamepath, "animeclips/")
            startFileBrower(sh, startPath=stPath, extFilter=".txt", openSave="save", title="Export current clip to:", onOk=onExportClip, onCancel=None)
        if GUILayout.Button("Dump", btnstyle, GUILayout.Width(cbwidth)):
            if saveStringToFile('dumppython.txt', clip.exportSetting(), append=True):
                scriptHelperGUIMessage("All clip settings and keyframes were dumpped into <dumppython.txt>.")
        if GUILayout.Button("Optimize", btnstyle, GUILayout.Width(cbwidth)):
            scriptHelperGUIMessage("Optimize keyframes for all contents. The optimization will delete unchanged status to make the output shorter and clear, and better for performence.\n'Manual': Choice to delete status stay unchanged in all keyframes.\n'Deep': Delete status unchanged between keyframes.\n'Deep -1st': Run deep clear except for the first keyframe.\n<color=#ff0000>Save you work before do this action if you are not sure!</color>",
                                    (("Manual", startManualOptimize, sh), ("Deep", clip.optimizeKeyFrames, True), ("Deep -1st", clip.optimizeKeyFrames, False), "Cancel"))
        if GUILayout.Button("Back", btnstyle, GUILayout.Width(cbwidth)):
            changeGuiScreen(sh, kfam_GUI_manager)
        GUILayout.EndHorizontal()
    


