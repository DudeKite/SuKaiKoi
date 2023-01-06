# External Plugin Functions 
# Module for calling functions from native plugins in "/Plugins" folder
# v3.8
#
# Changelog:
# 1.1
# - static method "exists" in ExtPlugin - crossplatform
# 2.0 (VNGE 11.0)
# - NEO: HSStudioNEOAddon, HSStudioNEOExtSave
# - PH: PHSAddon
# - KK: KKPE (beta support
# 2.1
# - NEO: HSStudioNEOExtSave - functions ExtDataGet, ExtDataSet (get/set full plugin data in string)
# - All: GetPrivate function - grant access to private fields
# 2.2
# - NEO: HSStudioNEOAddon - Add some function to support play MMD
# - KK: KKVMDPlayPlugin - a plugin to support play MMD
# 2.3 (VNGE 11.7)
# - NEO: HSPENeo plugin (works with HSPE 2.8.0+)
# 2.4 (VNGE 11.8)
# - CharaStudio: KKPE plugin support
# Warning: this work only with internal beta KKPE version! Don't use it for now!
# 2.5 (VNGE 12.0)
# - CharaStudio: Screencap plugin support
# 2.6 (VNGE 12.5)
# - All: has_plugin support function
# 2.7 (VNGE 13.9)
# - NeoV2 (AI): AIPE plugin support
# 2.8 (VNGE 14.1)
# - All: calculating plugin folder (easy switch between Bep4 and Bep5)
# 2.9 (VNGE 15.0)
# - Support for NodeConstraints plugin
# 3.0 (VNGE 16.0)
# - Support AIVMDPlugin
# - Support DHH_AI
# 3.1
# - changed logic for Exists check. Allow load plugins from subfolders in Bep5.
# 3.2 (VNGE 16.8)
# - Update AIVMDPlugin to support AIVMDPlayer too
# - Support AI_FKIK
# - Add: CallPrivateStatic function
# 3.3 (VNGE 16.9)
# - ExtensibleSaveFormat and AI_ExtensibleSaveFormat mod (for AI and KK). Support for OnSceneLoad, Import, Save events
# - HSExtSave mod (for HS). Support for OnSceneLoad, Import, Save events
# 3.4 (VNGE 17.5)
# - AI_ExtensibleSaveFormat also load HS2_ExtensibleSaveFormat
# - AI_ExtensibleSaveFormat's Helper function for save/load extend data 
# 3.5 (VNGE 17.7)
# - support HS2PE
# 3.6
# - support HS2VmdPlayPlugin
# - some new function for KKVmdPlayPlugin
# - ExtensibleSaveFormat's Helper function for save/load extend data
# 3.7 (VNGE 18.0)
# - support ILLAPI (KKAPI, HS2API etc.)
# 3.8 (VNGE 18.2) (countd360)
# - support NodesConstraints 1.2.0 again
# - support HS2VmdPlayPlugin 0.3.x
# 3.9
# - refactored ExtensibleSaveFormat to one class
# - support HS2_FKIK
# 3.10
# - fix NodesConstraints 1.2.0 support bug

# Use "dotPeek" to decompile native plugin dlls to understand how they work.
# Download link: https://www.jetbrains.com/decompiler/download/

# Adding your own class/function:
#   - Create a class extended from ExtPlugin 
#   - Use plugin name as class name for minimal confusion
#   - Create functions to call native plugin functions
#   - Do not create code that affects other functions if possible

import clr
import os
from vngameengine import get_engine_id, HSNeoOCIChar

pluginsDetection = {}

class ExtPlugin(): # v1.0
    def __init__(self, name = None):
        self.isDetected = False
        self.name = name
        #print "ExtPlugin:", name
        self.initFlag()

    @staticmethod
    def calc_plugin_dir():
        from UnityEngine import Application
        from os import path
        rootfolder = path.realpath(path.join(Application.dataPath, '..'))

        # os.path.splitext(__file__)[0] + '.ini'
        pydirname = path.dirname(__file__)
        pluginpath = path.realpath(path.join(pydirname, '..', '..'))
        return path.relpath(pluginpath, rootfolder)

    @staticmethod
    def exists(name):
        # usually check IPA folder
        # plgdir = os.path.join(os.getcwd(), "Plugins/")
        #
        # if get_engine_id() == "charastudio":
        #     # in CharaStudio check BepInEx folder
        #     plgdir = os.path.join(os.getcwd(), "BepInEx/")
        #
        # if get_engine_id() == "neov2":
        #     # in StudioNeoV2 check BepInEx/plugins folder
        #     plgdir = os.path.join(os.getcwd(), "BepInEx/Plugins/")

        # ------------ old check - using DLL file path ---------------------
        # plgdir = ExtPlugin.calc_plugin_dir()
        # return os.path.isfile(plgdir + "/" + name + ".dll")

        # new check
        global pluginsDetection
        if name in pluginsDetection:
            #print "Cached explugin check for ", name
            pass
        else:
            try:
                clr.AddReference(name)
                pluginsDetection[name] = True
            except Exception, e:
                pluginsDetection[name] = False

        return pluginsDetection[name]
    # init flags
    def initFlag(self):
        #plgdir = os.path.join(os.getcwd(), "Plugins/")
        if ExtPlugin.exists(self.name):
            self.isDetected = True
            clr.AddReference(self.name)
            #print self.name + ".dll detected."
        else:
            self.isDetected = False
            print self.name + ".dll not found."

# ::::::::::: StudioNeo ::::::::::: 

# --- HSStudioNeoAddon --- 
class HSStudioNEOAddon(ExtPlugin):
    def __init__(self):
        #super(HSStudioNEOAddon, self).__init__("HSStudioNEOAddon") #can't get it to work
        ExtPlugin.__init__(self, "HSStudioNEOAddon")
        if self.isDetected:
            from HSStudioNEOAddon import BaseMgr, HSVMDAnimationMgr
            self.vmdMgr = BaseMgr[HSVMDAnimationMgr].Instance

    # Activate simulataneous FK/IK (char: HSNeoOCIChar, OCIChar)
    def activateFKIK(self, char):
        from Studio import OCIChar
        if self.isDetected == True and not char == None:
            from HSStudioNEOAddon import FKIKAssist
            if isinstance(char, HSNeoOCIChar):
                FKIKAssist.FKIKAssistMgr.ActivateFKIK(char.objctrl)
            elif isinstance(char, OCIChar): #might be redundant, not sure
                FKIKAssist.FKIKAssistMgr.ActivateFKIK(char)

    # MMD play ALL
    def MMDPlayAll(self):
        if self.isDetected:
            self.vmdMgr.PlayAll()
            
    # MMD Pause ALL
    def MMDPauseAll(self):
        if self.isDetected:
            self.vmdMgr.PauseAll()

    # MMD play ALL
    def MMDStopAll(self):
        if self.isDetected:
            self.vmdMgr.StopAll()
    
    # MMD set anime position
    def MMDSetAnimPositionAll(self, time):
        if self.isDetected:
            self.vmdMgr.PlayAll()
            self.vmdMgr.PauseAll()
            for vc in self.vmdMgr.controllers:
                vc.SetAnimPosition(time)
            self.vmdMgr.SoundMgr.AnimePosition = time
                
    # MMD get controller for char
    def MMDGetCharVmdController(self, char):
        from Studio import OCIChar
        if self.isDetected and char:
            if isinstance(char, HSNeoOCIChar):
                tgtOCIChar = char.objctrl
            elif isinstance(char, OCIChar): #might be redundant, not sure
                tgtOCIChar = char
            else:
                return None
            for vc in self.vmdMgr.controllers:
                if vc.studioChara == tgtOCIChar:
                    return vc
        return None
        
    # MMD export setting for char
    def MMDExportCharVmdSetting(self, char):
        vc = self.MMDGetCharVmdController(char)
        if vc and vc.VMDAnimEnabled:
            exset = {}
            exset["VMDAnimEnabled"] = "1"
            exset["lastLoadedVMD"] = vc.lastLoadedVMD if vc.lastLoadedVMD else ""
            exset["speed"] = str(vc.speed)
            exset["Loop"] = "1" if vc.Loop else "0"
            exset["centerBasePos"] = "(%.3f, %.3f, %.3f)"%(vc.centerBasePos.x, vc.centerBasePos.y, vc.centerBasePos.z)
            return exset
        else:
            return None
            
    # MMD import setting for char
    def MMDImportCharVmdSetting(self, char, imSet):
        vc = self.MMDGetCharVmdController(char)
        if vc == None:
            return
        # TODO: load settings
        
# --- HSStudioNEOExtSave ---
class HSStudioNEOExtSave(ExtPlugin):
    def __init__(self):
        #super(HSStudioNEOExtSave, self).__init__("HSStudioNEOExtSave") #can't get it to work
        ExtPlugin.__init__(self, "HSStudioNEOExtSave")
        
    # Save ext data
    def SaveExtData(self, filePath):
        from HSStudioNEOExtSave import StudioNEOExtendSaveMgr
        StudioNEOExtendSaveMgr.Instance.SaveExtData(filePath)
        
    # Load ext data
    def LoadExtData(self, filePath):
        from HSStudioNEOExtSave import StudioNEOExtendSaveMgr
        StudioNEOExtendSaveMgr.Instance.LoadExtData(filePath)
        StudioNEOExtendSaveMgr.Instance.LoadExtDataRaw(filePath)

    def ExtDataGet(self):
        import clr
        clr.AddReference("System.Xml")

        from HSStudioNEOExtSave import StudioNEOExtendSaveMgr
        #handlers = StudioNEOExtendSaveMgr.Instance.GetField("handlers", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.FlattenHierarchy)
        handlers = GetPrivate(StudioNEOExtendSaveMgr.Instance, "handlers")

        from System.Xml import XmlDocument

        if len(handlers) > 0:
            xmlDocument = XmlDocument()
            newChild = xmlDocument.CreateXmlDeclaration("1.0", "utf-8", None)
            xmlDocument.AppendChild(newChild)
            xmlElement = xmlDocument.CreateElement("ExtSave")
            xmlDocument.AppendChild(xmlElement)
            for handler in handlers:
                try:
                    handler.OnSave(xmlElement)
                except Exception, e:
                    print "Error in ExtSave handler save:", e

            #return xmlDocument.ToString()
            from System.IO import StringWriter
            #from System.Xml import XmlTextWriter

            stringWriter = StringWriter()
            xmlDocument.Save(stringWriter)
            return stringWriter.ToString()

        return ""

    def ExtDataSet(self, datastring):
        import clr
        clr.AddReference("System.Xml")

        from HSStudioNEOExtSave import StudioNEOExtendSaveMgr
        # handlers = StudioNEOExtendSaveMgr.Instance.GetField("handlers", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.FlattenHierarchy)
        handlers = GetPrivate(StudioNEOExtendSaveMgr.Instance, "handlers")

        from System.Xml import XmlDocument

        if len(handlers) > 0:
            xmlDocument = XmlDocument()
            xmlDocument.LoadXml(datastring)
            documentElement = xmlDocument.DocumentElement
            for handler in handlers:
                try:
                    handler.OnLoad(documentElement)
                except Exception, e:
                    print "Error in ExtSave handler load:", e

class HSPENeo(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "HSPENeo")

    def GetCharaSettingsText(self,ocichar):
        import clr
        clr.AddReference("System.Xml")

        from System.IO import StringWriter
        from System.Xml import XmlTextWriter

        stringWriter = StringWriter()
        xmlTextWriter = XmlTextWriter(stringWriter)

        from HSPE import MainWindow

        from UnityEngine import GameObject
        from HSPE import PoseController

        xmlTextWriter.WriteStartElement("characterInfo")
        ocichar.charInfo.gameObject.GetComponent(PoseController).SaveXml(xmlTextWriter)
        xmlTextWriter.WriteEndElement()

        return stringWriter.ToString()

    def SetCharaSettingsText(self,ocichar,text):
        import clr
        clr.AddReference("System.Xml")

        from System.IO import StringWriter
        from System.Xml import XmlDocument

        xmlDocument = XmlDocument()
        xmlDocument.LoadXml(text)
        node = xmlDocument.FirstChild

        from HSPE import MainWindow

        from UnityEngine import GameObject
        from HSPE import PoseController

        ocichar.charInfo.gameObject.GetComponent(PoseController).ScheduleLoad(node, None)


# ::::::::::: PlayHome Studio :::::::::::
class PHSAddon(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "PHSAddon")
        # support class instance from plugin
        if self.isDetected:
            from PHSAddon import BaseMgr, HSVMDAnimationMgr, ExtMP3
            self.vmdMgr = BaseMgr[HSVMDAnimationMgr].Instance
            self.mp3player = ExtMP3.MP3Player

    # Activate simulataneous FK/IK (char: HSNeoOCIChar, OCIChar)
    def activateFKIK(self, char):
        from Studio import OCIChar
        if self.isDetected == True and not char == None:
            from PHSAddon import FKIKAssist
            if isinstance(char, HSNeoOCIChar):
                try:
                    FKIKAssist.FKIKAssistMgr.ActivateFKIK(char.objctrl)
                except SystemError as e:
                    #print e
                    pass
            elif isinstance(char, OCIChar): #might be redundant, not sure
                try:
                    FKIKAssist.FKIKAssistMgr.ActivateFKIK(char)
                except SystemError as e:
                    #print e
                    pass
    
    # MMD play ALL
    def MMDPlayAll(self):
        if self.isDetected:
            self.vmdMgr.PlayAll()
            self.mp3player.Play()
            
    # MMD Pause ALL
    def MMDPauseAll(self):
        if self.isDetected:
            self.vmdMgr.PauseAll()
            self.mp3player.Pause()

    # MMD play ALL
    def MMDStopAll(self):
        if self.isDetected:
            self.vmdMgr.StopAll()
            self.mp3player.Stop()
    
    # MMD set anime position
    def MMDSetAnimPositionAll(self, time):
        if self.isDetected:
            self.vmdMgr.PlayAll()
            self.vmdMgr.PauseAll()
            for vc in self.vmdMgr.controllers:
                vc.SetAnimPosition(time)
            #self.mp3player.Seek(time)
            from System import Single
            #p = Array[Single]([time])
            CallPrivateStatic(self.mp3player, "Seek", [Single(time)])
                
    # MMD get controller for char
    def MMDGetCharVmdController(self, char):
        from Studio import OCIChar
        if self.isDetected and char:
            if isinstance(char, HSNeoOCIChar):
                tgtOCIChar = char.objctrl
            elif isinstance(char, OCIChar): #might be redundant, not sure
                tgtOCIChar = char
            else:
                return None
            for vc in self.vmdMgr.controllers:
                if vc.studioChara == tgtOCIChar:
                    return vc
        return None
        
    # MMD export setting for char
    def MMDExportCharVmdSetting(self, char):
        vc = self.MMDGetCharVmdController(char)
        if vc and vc.VMDAnimEnabled:
            exset = {}
            exset["VMDAnimEnabled"] = "1"
            exset["lastLoadedVMD"] = vc.lastLoadedVMD if vc.lastLoadedVMD else ""
            exset["lastLipPath"] = vc.lastLipPath if vc.lastLipPath else ""
            exset["isLipSync"] = "1" if vc.isLipSync else "0"
            exset["speed"] = str(vc.speed)
            exset["Loop"] = "1" if vc.Loop else "0"
            exset["centerBasePos"] = "(%.3f, %.3f, %.3f)"%(vc.centerBasePos.x, vc.centerBasePos.y, vc.centerBasePos.z)
            exset["hipPositionAdjust"] = "(%.3f, %.3f, %.3f)"%(vc.hipPositionAdjust.x, vc.hipPositionAdjust.y, vc.hipPositionAdjust.z)
            return exset
        else:
            return None
            
    # MMD import setting for char
    def MMDImportCharVmdSetting(self, char, imSet):
        vc = self.MMDGetCharVmdController(char)
        if vc == None:
            return
        if imSet.has_key("isLipSync"):
            vc.SetLipSyn(imSet["isLipSync"] == "1")
        # is the other settings necessary?        
        
# ::::::::::: CharaStudio ::::::::::: 
class KKPE(ExtPlugin):
    def __init__(self):
        #super(HSStudioNEOAddon, self).__init__("HSStudioNEOAddon") #can't get it to work
        ExtPlugin.__init__(self, "KKPE")

    def GetCharaSettingsText(self,ocichar):
        import clr
        clr.AddReference("System.Xml")

        from System.IO import StringWriter
        from System.Xml import XmlTextWriter



        stringWriter = StringWriter()
        xmlTextWriter = XmlTextWriter(stringWriter)

        from HSPE import MainWindow

        from UnityEngine import GameObject
        from HSPE import PoseController
        # print self.studio.m_BackgroundCtrl.Load(ffile)
        # for obj in GameObject.FindObjectOfType(BackgroundCtrl):

        #obj = GameObject.FindObjectOfType(MainWindow)

        #obj.SaveChara(ocichar,xmlTextWriter)
        xmlTextWriter.WriteStartElement("characterInfo")
        ocichar.charInfo.gameObject.GetComponent(PoseController).SaveXml(xmlTextWriter)
        xmlTextWriter.WriteEndElement()

        return stringWriter.ToString()

    def SetCharaSettingsText(self,ocichar,text):
        import clr
        clr.AddReference("System.Xml")

        from System.IO import StringWriter
        from System.Xml import XmlDocument

        xmlDocument = XmlDocument()
        xmlDocument.LoadXml(text)
        node = xmlDocument.FirstChild

        from HSPE import MainWindow

        from UnityEngine import GameObject
        from HSPE import PoseController

        ocichar.charInfo.gameObject.GetComponent(PoseController).ScheduleLoad(node, None)
        # print self.studio.m_BackgroundCtrl.Load(ffile)
        # for obj in GameObject.FindObjectOfType(BackgroundCtrl):

        # obj = GameObject.FindObjectOfType(MainWindow)

        # obj.SaveChara(ocichar,xmlTextWriter)
        # xmlTextWriter.WriteStartElement("characterInfo")
        # ocichar.charInfo.gameObject.GetComponent(PoseController).SaveXml(xmlTextWriter)
        # xmlTextWriter.WriteEndElement()
        #
        # return stringWriter.ToString()


class ScreencapPlugin(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "Screencap")

    def TakeCharScreenshot(self):
        from Screencap import ScreenshotManager
        from Studio import Studio
        studio = Studio.Instance

        studio.StartCoroutine(
            CallPrivate(ScreenshotManager.Instance, "TakeCharScreenshot", []))  # this take screenshot without UI

    def TakeScreenshot(self):
        from Screencap import ScreenshotManager
        from Studio import Studio
        studio = Studio.Instance

        CallPrivate(ScreenshotManager.Instance, "TakeScreenshot", []) # this take screenshot with UI


class KKVMDPlayPlugin(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "KKVMDPlayPlugin")
        # support class instance from plugin
        if self.isDetected:
            from KKVMDPlayPlugin import VMDAnimationMgr
            self.vmdMgr = VMDAnimationMgr.Instance
            self.cameraMgr = self.vmdMgr.CameraMgr
            self.audioMgr = self.vmdMgr.SoundMgr

    # MMD play ALL
    def MMDPlayAll(self):
        if self.isDetected:
            self.vmdMgr.PlayAll()
            
    # MMD Pause ALL
    def MMDPauseAll(self):
        if self.isDetected:
            self.vmdMgr.PauseAll()

    # MMD play ALL
    def MMDStopAll(self):
        if self.isDetected:
            self.vmdMgr.StopAll()
    
    # MMD set anime position
    def MMDSetAnimPositionAll(self, time):
        if self.isDetected:
            self.vmdMgr.PlayAll()
            self.vmdMgr.PauseAll()
            for vc in self.vmdMgr.controllers:
                vc.SetAnimPosition(time)
            self.cameraMgr.AnimePosition = time
            self.audioMgr.AnimePosition = time
                
    # MMD get controller for char
    def MMDGetCharVmdController(self, char):
        from Studio import OCIChar
        if self.isDetected and char:
            if isinstance(char, HSNeoOCIChar):
                tgtChara = char.objctrl.charInfo
            elif isinstance(char, OCIChar): #might be redundant, not sure
                tgtChara = char.charInfo
            else:
                return None
            for vc in self.vmdMgr.controllers:
                if vc.chara == tgtChara:
                    return vc
        return None
        
    # MMD export setting for char
    def MMDExportCharVmdSetting(self, char):
        vc = self.MMDGetCharVmdController(char)
        if vc and vc.VMDAnimEnabled:
            exset = {}
            exset["VMDAnimEnabled"] = "1"
            exset["lastLoadedVMD"] = vc.lastLoadedVMD if vc.lastLoadedVMD else ""
            #exset["isLipSync"] = "1" if vc.isLipSync else "0"
            #exset["speed"] = str(vc.speed)
            #exset["Loop"] = "1" if vc.Loop else "0"
            return exset
        else:
            return None
            
    # MMD import setting for char
    def MMDImportCharVmdSetting(self, char, imSet):
        vc = self.MMDGetCharVmdController(char)
        if vc == None:
            return
        if imSet.has_key("isLipSync"):
            vc.SetLipSyn(imSet["isLipSync"] == "1")
        # is the other settings necessary?     

    # MMD get controller infomation
    def MMDGetAllVmdController(self):
        if not self.isDetected:
            return None
        vcs = []
        for vc in self.vmdMgr.controllers:
            vcs.append(vc)
        return tuple(vcs)

    def MMDGetVmdInfo(self, ctrl):
        info = {}
        try:
            # version 0.1.x
            clip = ctrl.animationForVMD.clip
            info["Loaded"] = clip != None
            info["ChaControl"] = ctrl.chara
            info["FilePath"] = ctrl.lastLoadedVMD
            info["Length"] = 0 if clip == None else ctrl.animationForVMD.clip.length
            info["Frames"] = 0 if clip == None else int(ctrl.animationForVMD.clip.length * 30.0)
            #info["BoneNameMap"] = ctrl.boneNameMap
            #info["BoneAdjustMap"] = ctrl.boneAdjust
        except:
            # version 0.3.x
            state = ctrl.GetModelAnimationState()
            info["Loaded"] = state != None
            info["ChaControl"] = ctrl.chara
            info["FilePath"] = ctrl.lastLoadedVMD
            info["Length"] = 0 if state == None else state.length
            info["Frames"] = 0 if state == None else int(state.length * 30.0)
            #info["BoneNameMap"] = ctrl.boneNameMap
            #info["BoneAdjustMap"] = ctrl.boneAdjust
        return info

    def MMDGetCameraInfo(self):
        if not self.isDetected:
            return None
        info = {}
        info["Loaded"] = False
        if self.cameraMgr.AnimeLength > 0 and self.cameraMgr.cameraVMDFilePath != None:
            info["Loaded"] = True
            info["Enabled"] = self.cameraMgr.CameraEnabled
            info["FilePath"] = self.cameraMgr.cameraVMDFilePath
            info["Length"] = self.cameraMgr.AnimeLength
        return info

    def MMDGetSoundInfo(self):
        if not self.isDetected:
            return None
        info = {}
        info["Loaded"] = False
        if self.audioMgr.currentAudioClip != None:
            info["Loaded"] = True
            info["FilePath"] = self.audioMgr.audioFilePath
            info["Length"] = self.audioMgr.SoundLength
        return info

    # control and sync
    def MMDPlayVmd(self, ctrl):
        ctrl.Play()

    def MMDPauseVmd(self, ctrl):
        ctrl.Pause()

    def MMDStopVmd(self, ctrl):
        ctrl.Stop()

    def MMDSyncVmd(self, ctrl, time):
        ctrl.SetAnimPosition(time)

    def MMDPlayCamera(self):
        if self.isDetected:
            self.cameraMgr.Play()

    def MMDPauseCamera(self):
        if self.isDetected:
            self.cameraMgr.Pause()

    def MMDStopCamera(self):
        if self.isDetected:
            self.cameraMgr.Stop()

    def MMDSyncCamera(self, time):
        if self.isDetected:
            self.cameraMgr.AnimePosition = time

    def MMDPlaySound(self):
        if self.isDetected:
            self.audioMgr.PlaySound()

    def MMDPauseSound(self):
        if self.isDetected:
            self.audioMgr.PauseSound()

    def MMDStopSound(self):
        if self.isDetected:
            self.audioMgr.StopSound()

    def MMDSyncSound(self, time):
        if self.isDetected:
            self.audioMgr.AnimePosition = time


# ::::::::::: StudioNeoV2 (AI/HS2) ::::::::::: 
class AIPE(ExtPlugin):
    def __init__(self):
        #ExtPlugin.__init__(self, "AIPE")
        if ExtPlugin.exists("AIPE"):
            ExtPlugin.__init__(self, "AIPE")
        elif ExtPlugin.exists("HS2PE"):
            ExtPlugin.__init__(self, "HS2PE")

    def GetCharaSettingsText(self, ocichar):
        import clr
        clr.AddReference("System.Xml")

        from System.IO import StringWriter
        from System.Xml import XmlTextWriter

        stringWriter = StringWriter()
        xmlTextWriter = XmlTextWriter(stringWriter)

        from UnityEngine import GameObject
        from HSPE import PoseController

        xmlTextWriter.WriteStartElement("characterInfo")
        ocichar.charInfo.gameObject.GetComponent(PoseController).SaveXml(xmlTextWriter)
        xmlTextWriter.WriteEndElement()

        return stringWriter.ToString()

    def SetCharaSettingsText(self,ocichar, text):
        import clr
        clr.AddReference("System.Xml")

        from System.IO import StringWriter
        from System.Xml import XmlDocument

        xmlDocument = XmlDocument()
        xmlDocument.LoadXml(text)
        node = xmlDocument.FirstChild

        from UnityEngine import GameObject
        from HSPE import PoseController

        ocichar.charInfo.gameObject.GetComponent(PoseController).ScheduleLoad(node, None)

class AIVMDPlugin(ExtPlugin):
    def __init__(self):
        self.isDetected = False
        self.name = ""
        # try load AIVMDPlugin from maki3d, as manager1
        if ExtPlugin.exists("AIVMDPlugin"):
            self.isDetected1 = True
            self.name = "AIVMDPlugin"
            clr.AddReference("AIVMDPlugin")
            from AIVMDPlugin import VMDMotionManager
            self.vmdMgr1 = VMDMotionManager.Instance
            self.audioMgr1 = self.vmdMgr1.AudioManager
            self.cameraMgr1 = self.vmdMgr1.CameraManager
        else:
            self.isDetected1 = False
        # try load AIVMDPlayer from craft6, as manager2
        if ExtPlugin.exists("AIVMDPlayer"):
            self.isDetected2 = True
            self.name = "AIVMDPlugin"
            clr.AddReference("AIVMDPlayer")
            from AIVMDPlayer import VMDAnimationMgr
            self.vmdMgr2 = VMDAnimationMgr.Instance
            self.audioMgr2 = self.vmdMgr2.SoundMgr
            self.cameraMgr2 = self.vmdMgr2.CameraMgr
        else:
            self.isDetected2 = False
        # if found any one
        self.isDetected = self.isDetected1 or self.isDetected2

    # MMD play ALL
    def MMDPlayAll(self):
        if self.isDetected1:
            self.vmdMgr1.playAll()
        if self.isDetected2:
            self.vmdMgr2.PlayAll()
            
    # MMD Pause ALL
    def MMDPauseAll(self):
        if self.isDetected1:
            self.vmdMgr1.pauseAll()
        if self.isDetected2:
            self.vmdMgr2.PauseAll()

    # MMD play ALL
    def MMDStopAll(self):
        if self.isDetected1:
            self.vmdMgr1.stopAll()
        if self.isDetected2:
            self.vmdMgr2.StopAll()
    
    # MMD set anime position
    def MMDSetAnimPositionAll(self, time):
        if self.isDetected1:
            self.vmdMgr1.playAll()
            self.vmdMgr1.pauseAll()
            for vc in self.vmdMgr1.controllers:
                vc.SetAnimPosition(time)
            self.audioMgr1.AnimePosition = time
            self.cameraMgr1.AnimePosition = time
        if self.isDetected2:
            self.vmdMgr2.PlayAll()
            self.vmdMgr2.PauseAll()
            for vc in self.vmdMgr2.controllers:
                vc.SetAnimPosition(time)
            self.audioMgr2.AnimePosition = time
            self.cameraMgr2.AnimePosition = time
                
    # MMD get controller for char
    def MMDGetCharVmdController(self, char):
        from Studio import OCIChar
        if isinstance(char, HSNeoOCIChar):
            tgtChara = char.objctrl.charInfo
        elif isinstance(char, OCIChar): #might be redundant, not sure
            tgtChara = char.charInfo
        else:
            return None
        if self.isDetected1:
            for vc in self.vmdMgr1.controllers:
                if vc.chara == tgtChara:
                    return vc
        if self.isDetected2:
            for vc in self.vmdMgr2.controllers:
                if vc.chara == tgtChara:
                    return vc
        return None

    # MMD export setting for char
    def MMDExportCharVmdSetting(self, char):
        vc = self.MMDGetCharVmdController(char)
        if vc and vc.VMDAnimEnabled:
            exset = {}
            exset["VMDAnimEnabled"] = "1"
            exset["lastLoadedVMD"] = vc.lastLoadedVMD if vc.lastLoadedVMD else ""
            #exset["isLipSync"] = "1" if vc.isLipSync else "0"
            #exset["speed"] = str(vc.speed)
            #exset["Loop"] = "1" if vc.Loop else "0"
            return exset
        else:
            return None

    # MMD import setting for char
    def MMDImportCharVmdSetting(self, char, imSet):
        vc = self.MMDGetCharVmdController(char)
        if vc == None:
            return
        #if imSet.has_key("isLipSync"):
        #    vc.SetLipSyn(imSet["isLipSync"] == "1")
        # is the other settings necessary?     

    # MMD get all controller
    def MMDGetAllVmdController(self):
        if not self.isDetected:
            return None
        vcs = []
        if self.isDetected1:
            for vc in self.vmdMgr1.controllers:
                vcs.append(vc)
        if self.isDetected2:
            for vc in self.vmdMgr2.controllers:
                vcs.append(vc)
        return tuple(vcs)
    
    def MMDPlayVmd(self, ctrl):
        ctrl.Play()

    def MMDPauseVmd(self, ctrl):
        ctrl.Pause()

    def MMDStopVmd(self, ctrl):
        ctrl.Stop()

    def MMDSyncVmd(self, ctrl, time):
        ctrl.SetAnimPosition(time)

    def MMDGetVmdInfo(self, ctrl):
        info = {}
        clip = ctrl.animationForVMD.clip
        info["Loaded"] = clip != None
        info["ChaControl"] = ctrl.chara
        info["FilePath"] = ctrl.lastLoadedVMD
        info["Length"] = 0 if clip == None else ctrl.animationForVMD.clip.length
        info["Frames"] = 0 if clip == None else int(ctrl.animationForVMD.clip.length * 30.0)
        #info["BoneNameMap"] = ctrl.boneNameMap
        #info["BoneAdjustMap"] = ctrl.boneAdjust
        return info

    def MMDPlaySound(self):
        if self.isDetected1:
            self.audioMgr1.playSound()
        if self.isDetected2:
            self.audioMgr2.PlaySound()

    def MMDPauseSound(self):
        if self.isDetected1:
            self.audioMgr1.pauseSound()
        if self.isDetected2:
            self.audioMgr2.PauseSound()

    def MMDStopSound(self):
        if self.isDetected1:
            self.audioMgr1.stopSound()
        if self.isDetected2:
            self.audioMgr2.StopSound()

    def MMDSyncSound(self, time):
        if self.isDetected1:
            self.audioMgr1.AnimePosition = time
        if self.isDetected2:
            self.audioMgr2.AnimePosition = time

    def MMDGetSoundInfo(self):
        if not self.isDetected:
            return None
        info = {}
        info["Loaded"] = False
        if self.isDetected1 and self.audioMgr1.currentAudioClip != None:
            info["Loaded"] = True
            info["FilePath"] = self.audioMgr1.AudioFilePath
            info["Length"] = self.audioMgr1.SoundLength
        if self.isDetected2 and self.audioMgr2.currentAudioClip != None:
            info["Loaded"] = True
            info["FilePath"] = self.audioMgr2.audioFilePath
            info["Length"] = self.audioMgr2.SoundLength
        return info

    def MMDSetSound(self, pathname):
        if self.isDetected2:
            return self.audioMgr2.SetSoundClip(pathname)
        return False

    def MMDPlayCamera(self):
        if self.isDetected1:
            self.cameraMgr1.play()
        if self.isDetected2:
            self.cameraMgr2.Play()

    def MMDPauseCamera(self):
        if self.isDetected1:
            self.cameraMgr1.pause()
        if self.isDetected2:
            self.cameraMgr2.Pause()

    def MMDStopCamera(self):
        if self.isDetected1:
            self.cameraMgr1.stop()
        if self.isDetected2:
            self.cameraMgr2.Stop()

    def MMDSyncCamera(self, time):
        if self.isDetected1:
            self.cameraMgr1.AnimePosition = time
        if self.isDetected2:
            self.cameraMgr2.AnimePosition = time

    def MMDGetCameraInfo(self):
        if not self.isDetected:
            return None
        info = {}
        info["Loaded"] = False
        if self.isDetected1 and self.cameraMgr1.AnimeLength > 0 and self.cameraMgr1.cameraVMDFilePath != None:
            info["Loaded"] = True
            info["Enabled"] = self.cameraMgr1.CameraEnabled
            info["FilePath"] = self.cameraMgr1.cameraVMDFilePath
            info["Length"] = self.cameraMgr1.AnimeLength
        if self.isDetected2 and self.cameraMgr2.AnimeLength > 0 and self.cameraMgr2.cameraVMDFilePath != None:
            info["Loaded"] = True
            info["Enabled"] = self.cameraMgr2.CameraEnabled
            info["FilePath"] = self.cameraMgr2.cameraVMDFilePath
            info["Length"] = self.cameraMgr2.AnimeLength
        return info

class HS2VMDPlayPlugin(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "HS2_VMDPlayPlugin")
        # support class instance from plugin
        if self.isDetected:
            from HS2VMDPlayPlugin import VMDAnimationMgr
            self.vmdMgr = VMDAnimationMgr.Instance
            self.cameraMgr = self.vmdMgr.CameraMgr
            self.audioMgr = self.vmdMgr.SoundMgr

    # MMD play ALL
    def MMDPlayAll(self):
        if self.isDetected:
            self.vmdMgr.PlayAll()
            
    # MMD Pause ALL
    def MMDPauseAll(self):
        if self.isDetected:
            self.vmdMgr.PauseAll()

    # MMD play ALL
    def MMDStopAll(self):
        if self.isDetected:
            self.vmdMgr.StopAll()
    
    # MMD set anime position
    def MMDSetAnimPositionAll(self, time):
        if self.isDetected:
            self.vmdMgr.PlayAll()
            self.vmdMgr.PauseAll()
            for vc in self.vmdMgr.controllers:
                vc.SetAnimPosition(time)
            self.cameraMgr.AnimePosition = time
            self.audioMgr.AnimePosition = time
                
    # MMD get controller for char
    def MMDGetCharVmdController(self, char):
        from Studio import OCIChar
        if self.isDetected and char:
            if isinstance(char, HSNeoOCIChar):
                tgtChara = char.objctrl.charInfo
            elif isinstance(char, OCIChar): #might be redundant, not sure
                tgtChara = char.charInfo
            else:
                return None
            for vc in self.vmdMgr.controllers:
                if vc.chara == tgtChara:
                    return vc
        return None
        
    # MMD export setting for char
    def MMDExportCharVmdSetting(self, char):
        vc = self.MMDGetCharVmdController(char)
        if vc and vc.VMDAnimEnabled:
            exset = {}
            exset["VMDAnimEnabled"] = "1"
            exset["lastLoadedVMD"] = vc.lastLoadedVMD if vc.lastLoadedVMD else ""
            #exset["isLipSync"] = "1" if vc.isLipSync else "0"
            #exset["speed"] = str(vc.speed)
            #exset["Loop"] = "1" if vc.Loop else "0"
            return exset
        else:
            return None
            
    # MMD import setting for char
    def MMDImportCharVmdSetting(self, char, imSet):
        vc = self.MMDGetCharVmdController(char)
        if vc == None:
            return
        if imSet.has_key("isLipSync"):
            vc.SetLipSyn(imSet["isLipSync"] == "1")
        # is the other settings necessary?     

    # MMD get controller infomation
    def MMDGetAllVmdController(self):
        if not self.isDetected:
            return None
        vcs = []
        for vc in self.vmdMgr.controllers:
            vcs.append(vc)
        return tuple(vcs)

    def MMDGetVmdInfo(self, ctrl):
        info = {}
        state = ctrl.GetModelAnimationState()
        info["Loaded"] = state != None
        info["ChaControl"] = ctrl.chara
        info["FilePath"] = ctrl.lastLoadedVMD
        info["Length"] = 0 if state == None else state.length
        info["Frames"] = 0 if state == None else int(state.length * 30.0)
        #info["BoneNameMap"] = ctrl.boneNameMap
        #info["BoneAdjustMap"] = ctrl.boneAdjust
        return info

    def MMDGetCameraInfo(self):
        if not self.isDetected:
            return None
        info = {}
        info["Loaded"] = False
        if self.cameraMgr.AnimeLength > 0 and self.cameraMgr.cameraVMDFilePath != None:
            info["Loaded"] = True
            info["Enabled"] = self.cameraMgr.CameraEnabled
            info["FilePath"] = self.cameraMgr.cameraVMDFilePath
            info["Length"] = self.cameraMgr.AnimeLength
        return info

    def MMDGetSoundInfo(self):
        if not self.isDetected:
            return None
        info = {}
        info["Loaded"] = False
        if self.audioMgr.currentAudioClip != None:
            info["Loaded"] = True
            info["FilePath"] = self.audioMgr.audioFilePath
            info["Length"] = self.audioMgr.SoundLength
        return info

    # control and sync
    def MMDPlayVmd(self, ctrl):
        ctrl.Play()

    def MMDPauseVmd(self, ctrl):
        ctrl.Pause()

    def MMDStopVmd(self, ctrl):
        ctrl.Stop()

    def MMDSyncVmd(self, ctrl, time):
        ctrl.SetAnimPosition(time)

    def MMDPlayCamera(self):
        if self.isDetected:
            self.cameraMgr.Play()

    def MMDPauseCamera(self):
        if self.isDetected:
            self.cameraMgr.Pause()

    def MMDStopCamera(self):
        if self.isDetected:
            self.cameraMgr.Stop()

    def MMDSyncCamera(self, time):
        if self.isDetected:
            self.cameraMgr.AnimePosition = time

    def MMDPlaySound(self):
        if self.isDetected:
            self.audioMgr.PlaySound()

    def MMDPauseSound(self):
        if self.isDetected:
            self.audioMgr.PauseSound()

    def MMDStopSound(self):
        if self.isDetected:
            self.audioMgr.StopSound()

    def MMDSyncSound(self, time):
        if self.isDetected:
            self.audioMgr.AnimePosition = time

class DHH_AI(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "DHH_AI4")
        if self.isDetected:
            from DHH_AI4 import DHH_Main
            from os import path
            self.dhh_main = DHH_Main.instance
            self.dhh_path = path.realpath(GetPrivate(self.dhh_main, "path"))
            self.dhh_tempfile = path.join(self.dhh_path, "VNGETemp")
            self.delTempFiles()

    def getEnable(self):
        if self.isDetected:
            return GetPrivate(self.dhh_main, "GraphicEnable")

    def setEnable(self, enable):
        if self.isDetected:
            self.dhh_main.SetEnable(enable)

    def exportGraphSetting(self):
        if self.isDetected:
            self.delTempFiles()
            idx = 0
            while (True):
                indexedFile = self.dhh_tempfile + str(idx)
                if not os.path.exists(indexedFile):
                    break
                else:
                    idx += 1
            CallPrivate(self.dhh_main, "SaveGraphicSetting", [indexedFile])
            fp = open(indexedFile, "r")
            settxt = fp.read()
            fp.close()
            return settxt
        else:
            return None

    def importGraphSetting(self, setting):
        if self.isDetected:
            self.delTempFiles()
            idx = 0
            while (True):
                try:
                    indexedFile = self.dhh_tempfile + str(idx)
                    fp = open(indexedFile, "w")
                    fp.write(setting)
                    fp.flush()
                    fp.close()
                    break
                except:
                    idx += 1
            # LoadGraphicSetting didn't close file stream...
            CallPrivate(self.dhh_main, "LoadGraphicSetting", [indexedFile])

    def delTempFiles(self):
        if self.isDetected:
            import os
            tempfiles = []
            for f in os.listdir(self.dhh_path):
                if f.startswith("VNGETemp"):
                    tempfiles.append(os.path.join(self.dhh_path, f))
            for f in tempfiles:
                try:
                    os.remove(f)
                except:
                    pass

class AI_FKIK(ExtPlugin):
    def __init__(self):
        if ExtPlugin.exists("AI_FKIK"):
            ExtPlugin.__init__(self, "AI_FKIK")
        elif ExtPlugin.exists("HS2_FKIK"):
            ExtPlugin.__init__(self, "HS2_FKIK")
        else:
            self.isDetected = False
        #ExtPlugin.__init__(self, "AI_FKIK")

    # Activate simulataneous FK/IK (char: HSNeoOCIChar, OCIChar)
    def activateFKIK(self, char):
        from Studio import OCIChar
        if self.isDetected == True and not char == None:
            from KK_Plugins import FKIK
            if isinstance(char, HSNeoOCIChar):
                FKIK.EnableFKIK(char.objctrl)
            elif isinstance(char, OCIChar): #might be redundant, not sure
                FKIK.EnableFKIK(char)


class CharaAnime(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "CharaAnime")
        if self.isDetected:
            from CharaAnime import CharaAnimeMgr, GizmosManager
            self.Manager = CharaAnimeMgr.Instance
            self.GizmosMgr = GizmosManager.Instance

# ::::::::::: NodesConstraints (HS,KK) :::::::::::
class NodesConstraints(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "NodesConstraints")

    def GetSysSettingsText(self):
        import clr
        clr.AddReference("System.Xml")

        from System.IO import StringWriter
        from System.Xml import XmlTextWriter, XmlDocument

        stringWriter = StringWriter()
        xmlTextWriter = XmlTextWriter(stringWriter)

        xmlTextWriter.WriteStartElement("nodescon")
        #ocichar.charInfo.gameObject.GetComponent(PoseController).SaveXml(xmlTextWriter)
        #from Studio import Studio
        from NodesConstraints import NodesConstraints
        #studio = Studio.Instance
        nodescon = GetPrivateStatic(NodesConstraints, "_self")
        try:
            CallPrivate(nodescon,"SaveSceneGeneric",[xmlTextWriter])
        except:
            CallPrivate(nodescon, "OnSceneSave", ["dummy path", xmlTextWriter])

        xmlTextWriter.WriteEndElement()

        #return stringWriter.ToString()
        settingData = stringWriter.ToString()
        try:
            # load contents of setting data
            xDoc = XmlDocument()
            xDoc.LoadXml(settingData)

            # get the sorted list of all objects in studio
            from Studio import Studio
            studio = Studio.Instance
            silist = sorted(list(studio.dicObjectCtrl.Keys))
            
            # find each setting and adjust
            xRoot = xDoc.FirstChild
            if xRoot.Name != "nodescon":
                print "NodesConstraints Error: unexpected root node, should be 'nodescon'."
                raise Exception()
            if not xRoot.HasChildNodes or xRoot.FirstChild.Name != "constraints":
                print "NodesConstraints Error: miss container node 'constraints'"
                raise Exception()
            for nc in xRoot.FirstChild.ChildNodes:
                if nc.Name == "constraint":
                    pidx = int(nc.GetAttribute("parentObjectIndex"))
                    cidx = int(nc.GetAttribute("childObjectIndex"))
                    pid = silist[pidx]
                    cid = silist[cidx]
                    #print "constraint setting: %d(%d) -> %d(%d)"%(pidx, pid, cidx, cid)
                    nc.SetAttribute("parentObjectID", str(pid))
                    nc.SetAttribute("childObjectID", str(cid))
                else:
                    print "NodesConstraints Warning: unknown setting node '%s'"%nc.Name
            # export again
            stringWriter2 = StringWriter()
            xmlTextWriter2 = XmlTextWriter(stringWriter2)
            xDoc.WriteContentTo(xmlTextWriter2)
            settingData = stringWriter2.ToString()
        except:
            pass
        return settingData

    def SetSysSettingsText(self, text):
        import clr
        clr.AddReference("System.Xml")

        from System.IO import StringWriter
        from System.Xml import XmlDocument

        xmlDocument = XmlDocument()
        xmlDocument.LoadXml(text)
        node = xmlDocument.FirstChild

        # re-calcuate object index base on the id
        try:
            # get the sorted list of all objects in studio
            from Studio import Studio
            studio = Studio.Instance
            silist = sorted(list(studio.dicObjectCtrl.Keys))

            if node.Name != "nodescon":
                print "NodesConstraints Error: unexpected root node, should be 'nodescon'."
                raise Exception()
            if not node.HasChildNodes or node.FirstChild.Name != "constraints":
                print "NodesConstraints Error: miss container node 'constraints'"
                raise Exception()
            for nc in node.FirstChild.ChildNodes:
                if nc.Name == "constraint":
                    pid = int(nc.GetAttribute("parentObjectID"))
                    cid = int(nc.GetAttribute("childObjectID"))
                    pidx = silist.index(pid)
                    cidx = silist.index(cid)
                    #print "constraint setting: %d(%d) -> %d(%d)"%(pidx, pid, cidx, cid)
                    nc.SetAttribute("parentObjectIndex", str(pidx))
                    nc.SetAttribute("childObjectIndex", str(cidx))
                else:
                    print "NodesConstraints Warning: unknown setting node '%s'"%nc.Name
        except:
            pass

        from NodesConstraints import NodesConstraints
        #studio = Studio.Instance
        nodescon = GetPrivateStatic(NodesConstraints, "_self")
        #print node
        self.ClearConstrains()

        try:
            CallPrivate(nodescon, "LoadSceneGeneric", [node.FirstChild,-1])
        except:
            CallPrivate(nodescon, "OnSceneLoad", ["dummy path", node])

    def ClearConstrains(self):
        from NodesConstraints import NodesConstraints
        #studio = Studio.Instance
        nodescon = GetPrivateStatic(NodesConstraints, "_self")

        constrains = GetPrivate(nodescon,"_constraints")
        for i in range(len(constrains)):
            CallPrivate(nodescon,"RemoveConstraintAt",[0])
        #ocichar.charInfo.gameObject.GetComponent(PoseController).ScheduleLoad(node, None)

# ::::::::::: ExtensibleSaveFormat (KK Bep5, AI) :::::::::::
class ExtensibleSaveFormat(ExtPlugin):
    def __init__(self):
        if ExtPlugin.exists("AI_ExtensibleSaveFormat"):
            ExtPlugin.__init__(self, "AI_ExtensibleSaveFormat")
        elif ExtPlugin.exists("HS2_ExtensibleSaveFormat"):
            ExtPlugin.__init__(self, "HS2_ExtensibleSaveFormat")
        elif ExtPlugin.exists("ExtensibleSaveFormat"):
            ExtPlugin.__init__(self, "ExtensibleSaveFormat")
        #elif ExtPlugin.exists("PH_ExtensibleSaveFormat"): # no, PH version doesn't suport studio save/load events
        #    ExtPlugin.__init__(self, "PH_ExtensibleSaveFormat")
        else:
            self.isDetected = False
        if self.isDetected:
            from ExtensibleSaveFormat import PluginData
            self.extSaveData = PluginData()
        else:
            self.extSaveData = None

    def reg_scene_being_loaded(self,callback):
        from ExtensibleSaveFormat import ExtendedSave
        ExtendedSave.SceneBeingLoaded += callback

    def reg_scene_being_saved(self,callback):
        from ExtensibleSaveFormat import ExtendedSave
        ExtendedSave.SceneBeingSaved += callback

    def reg_scene_being_imported(self,callback):
        from ExtensibleSaveFormat import ExtendedSave
        ExtendedSave.SceneBeingImported += callback

    def setExtendSaveData(self, key, data):
        if self.isDetected and self.extSaveData:
            self.extSaveData.data[key] = data

    def getExtendSaveData(self, key):
        if self.isDetected and self.extSaveData and self.extSaveData.data.ContainsKey(key):
            return self.extSaveData.data[key]
        else:
            return None

    def delExtendSaveData(self, key):
        if self.isDetected and self.extSaveData and self.extSaveData.data.ContainsKey(key):
            self.extSaveData.data.Remove(key)

    def newExtendSaveData(self, key):
        if self.isDetected:
            from ExtensibleSaveFormat import PluginData
            self.extSaveData = PluginData()

    def setExtendSaveVersion(self, ver):
        if self.isDetected and self.extSaveData:
            self.extSaveData.version = ver

    def getExtendSaveVersion(self):
        if self.isDetected and self.extSaveData:
            return self.extSaveData.version

    def saveExtendSaveData(self, id):
        from ExtensibleSaveFormat import ExtendedSave
        if self.isDetected:
            ExtendedSave.SetSceneExtendedDataById(id, self.extSaveData)

    def loadExtendSaveData(self, id):
        from ExtensibleSaveFormat import ExtendedSave, PluginData
        if self.isDetected:
            self.extSaveData = ExtendedSave.GetSceneExtendedDataById(id)
            if not self.extSaveData:
                self.extSaveData = PluginData()
            return self.extSaveData
        else:
            return None

class AI_ExtensibleSaveFormat(ExtensibleSaveFormat): # the same ExtensibleSaveFormat
    pass

# ::::::::::: Common class for KK_API, HS2_API etc, :::::::::::
class ILLAPI(ExtPlugin):
    def __init__(self):
        if ExtPlugin.exists("KKAPI"):
            ExtPlugin.__init__(self, "KKAPI")
        elif ExtPlugin.exists("HS2API"):
            ExtPlugin.__init__(self, "HS2API")
        elif ExtPlugin.exists("AIAPI"):
            ExtPlugin.__init__(self, "AIAPI")
        else:
            self.isDetected = False

    def Utilities_Extensions(self):
        from KKAPI.Utilities import Extensions
        return Extensions

    def Studio_StudioAPI(self):
        from KKAPI.Studio import StudioAPI
        return StudioAPI

# ::::::::::: ExtensibleSaveFormat (KK Bep5, AI) :::::::::::
class HSExtSave(ExtPlugin):
    def __init__(self):
        ExtPlugin.__init__(self, "HSExtSave")

    def reg_all_scene(self, id, callback_load, callback_import, callback_save):
        from HSExtSave import HSExtSave
        HSExtSave.RegisterHandler(id, None, None, callback_load,callback_import,callback_save,None,None)

# support functions
def has_plugin(pluginname):
    return ExtPlugin.exists(pluginname)

def GetPrivate(self, name):
    from System.Reflection import BindingFlags
    type = self.GetType()
    typefield = type.GetField(name, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.FlattenHierarchy)
    return typefield.GetValue(self)

def CallPrivate(self, name, p):
    from System.Reflection import BindingFlags
    bindflgs = BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.FlattenHierarchy
    try:
        method = self.GetType().GetMethod(name, bindflgs)
    except:
        # try fix Ambiguous match
        types = tuple((pm.GetType() for pm in p))
        method = self.GetType().GetMethod(name, bindflgs, None, types, None)

    from System import Array
    ar = tuple(p)

    return method.Invoke(self, ar)

def GetPrivateStatic(type, name):
    #return type.__dict__(name)
    from System.Reflection import BindingFlags
    #type = self.GetType()
    #typeof()
    import clr
    #clr.GetClrType(str)
    typefield = clr.GetClrType(type).GetField(name, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.FlattenHierarchy  | BindingFlags.Static)
    return typefield.GetValue(None)

def CallPrivateStatic(type, name, p):
    from System.Reflection import BindingFlags
    import clr
    method = clr.GetClrType(type).GetMethod(name, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.FlattenHierarchy  | BindingFlags.Static)
    
    from System import Array
    ar = tuple(p)
    return method.Invoke(type, ar)
