#===============================================================================================
# Help Classes
# v1.1 from @countd360
#  - Add class Prop to control props
# v1.2 
#  - Add new parameter pattern for set_cloth, set_accessory, set_FK_active and set_IK_active,
#    so they can take the return value of get functions as parameter directly
#  - Modify input parameter for set_son() and set_hand_ptn(), so they can take the return value 
#    of get function as parameter directly
#  - Change the output range of IK/FK rotation vector from 0~360 to -180~180, it helps on IK/FK anime
# v2.0
#  - Support PlayHome studio and HoneySelect studio NEO now!
#  - New classes ActorHSNeo/ActorPHStudio/ActorCharaStudio and PropHSNeo/PropPHStudio/PropCharaStudio for different engine
#  - All wrapper functions move from vnframe to vnactor, because they are game dependance as Actor/Prop
#  - New function for actor: set/get_anime_forceloop, set/get_all_voice, set/get_voice_repeat. Almost all settings is supported now!
#  - New function for prop: set/get_anime_speed for Prop (thanks to @Keitaro)
#  - New function for system: export_sys_status() for VNFrame to control studio bgm/env/wav/map
# v2.1
#  - Bug fix
# v2.2
#  - Bug fix
#  - Simple color attrbute of male character supported. 
#  - export_full_status() export different data for male and female
#  - load_clothes_file() added. Which allows you change coordinate by load a coordinate file. Set file by absolute path!
#  - Some function added for 'Couple Helper' of VNFrame.
# v2.3
#  - new property 'isAnimeOver' for Actor. animate() can set if force load anime. h_with() will sync anime force-loop option
#  - some new sys function: 'skip', 'branch', 'set_vari' can be used to control the flow in texts_next(). 
#    'wait_anime' and 'wait_voice' can be used in anime script to control wait time by anime or voice play.
# v2.3.1 (Keitaro)
#  - save neck params when position Fixed (NEO engine) - 'face_to_full' param
# v2.3.3
#  - support FK animation for FK item. 
# v2.3.4
#  - bug fix
# v2.3.9 (Keitaro)
# - import_status for Prop and Actor
# v2.3.10 (chickenman, Keitaro)
# - added support for OCILight as Prop (NEO tested)
# - import_status_diff_optimized for Actor
# - prop functions for Light (NEO tested)
# v2.4 (countd360)
# - support FK&IK mode in NEO and Playhome. Need extplugins and plugin mod. (thanks to @chickenman)
# - prop functions for Light extends to Playhome (need PHIBL.dll to create light) and KoiKatsu. 
# v3.0 (countd360)
# - import_status_diff_optimized for Prop
# v3.1.1 (Keitaro)
# - ActorCharaStudio - options for save/load KKPE data if KKPE plugin exists (set_kkpedata, get_kkpedata). Not included in export_full_status because of size. Also not full work before Joan make changes to KKPE (work only once)
# v3.1.3 (countd360)
# - ActorCharaStudio - set_kinematic(3) now actives IK&FK mode
# v3.2 (beta) (Keitaro)
# - Support for add data from external plugins to export_full using options from vnactor.ini
# - NEO: support save/load HSNeoExtSave (HSStudioNEOAddon.dll) plugin data in "sys"
# v3.2.1 (Keitaro)
# - Error wrapping in face_to_full call
# v3.3 (Keitaro)
# - NEO: HSPENeo plugin support (actor get_hspedata, set_hspedata, export_full)
# v3.4 (Keitaro)
# - CharaStudio: KKPE plugin support (actor get_kkpedata, set_kkpedata, export_full)
# Warning: this work only with beta KKPE version! Don't use it for now!
# v3.5 (Keitaro)
# - support functions - bytearray_to_str64 and str64_to_bytearray
# - CharaStudio: save neck params when position Fixed - 'face_to_full2' param (optimized version to use str64)
# - NEO: save neck params to str when position Fixed - 'face_to_full2' param (optimized version to use str64)
# - CharaStudio: ready for KKPE 1.2.0+, use ExportChara_KKPE=1 in vnactor.ini
# - CharaStudio: error handling for FK set
# - CharaStudio, NEO: export cur clothes, use ExportChara_CurClothesCoord=1 in vnactor.ini (for NEO may be buggy)
# 3.5.1 (countd360)
# - fix char_anime() function, can take force load param, fit with vnactor.animate()
# 3.6 (countd360)
# - fix light color support for CharaStudio
# - load status translate strings for vnactor.ini
# v3.6.1 (Keitaro)
# - CharaStudio: export normalizedTime if anime speed == 0.0
# Allow save characters in middle of animation
# v3.7 (Keitaro)
# - support for NeoV2 (AI-Shoujo)
# v3.7.1 (Countd360)
# - improved support for NeoV2 (AI-Shoujo)
# v3.7.2 (Keitaro)
# - support for shoes (CharaStudio)
# v3.8 (Keitaro)
# - support for body shapes (CharaStudio, NEO, AIShoujo)
# v3.9 (Countd360)
# - support for body and face shapes (all engine)
# - support char light (or camera light) in system export (all engine)
# - support export anime aux param, set it in ini file (all engine)
# - new property "animeLength", to get length of actor's anime (all engine)
# - add some function to support change export setting in runtime
# - fix skin wet import bug (AIShoujo)
# v3.10 (Keitaro)
# - support for Nodes Constraints plugin (Neo,KK)
# v3.11 (Keitaro)
# - support for set_curcloth_coordinate_no_accessory (KK) - load clothes without accs
# v4.0 (Countd360)
# - support almost all properties for item in KK and AI
# - support route object for KK and AI
# - add function for object camera
# - support DHH extern plugin setting for AI
# - bug fix for color and char_eyes_look
# v4.0.1 (Keitaro)
# - KK: function coordinate_type_int_to_enum. Fix bug for clothes track and copy/paste
# v4.1 (Countd360)
# - add get_anime_info_text/height.setter/breast.setter function for very engine
# - (AI) when set kinematic to 3, use AI_FKIK.dll first if exist
# - add set_camera_data/get_camera_data function
# - delete unnecessary ;
# v4.1.1 (Countd360)
# - patch for HoneySelect2
#===============================================================================================

# init stuff for diff plugins


from UnityEngine import Vector3, Vector2, Color
from vngameengine import HSNeoOCIChar, HSNeoOCI

# init stuff for diff plugins
import extplugins
plugin_aipe = extplugins.AIPE()

#===============================================================================================
class Actor(HSNeoOCIChar):
    @property
    def sex(self):
        # get sex: 0-male, 1-female
        raise Exception("Actor.sex not implemented")
    
    @property
    def height(self):
        # get height: not implemented
        return 0.5
        
    @property
    def breast(self):
        # get breast: not implemented
        return 0.5
        
    @property
    def visible(self):
        # get visible status
        return self.objctrl.treeNodeObject.visible
        
    @visible.setter
    def visible(self, value):
        # value: 0(hide)/1(visible)
        self.objctrl.treeNodeObject.visible = value
        
    @property
    def isVoicePlay(self):
        # get voice play status
        return self.objctrl.voiceCtrl.isPlay
        
    @property
    def isAnimeOver(self):
        # get if anime played once. 
        # note, anime may still playing because of it is looping anime or force-loop sets true
        # for those non-looping anime, it may be stopped after played once if force-loop not set.
        return self.objctrl.charAnimeCtrl.normalizedTime >= 1
        
    @property
    def isHAnime(self):
        # get isHAnime status, use by anime option param
        return self.objctrl.isHAnime
        
    @property
    def animeLength(self):
        # get current anime length in (second, frame, fps) format
        cis = self.objctrl.charAnimeCtrl.animator.GetCurrentAnimatorClipInfo(0)
        clip = cis[0].clip
        return (clip.length, int(round(clip.length * clip.frameRate)), clip.frameRate)

    @property
    def pos(self):
        return self.objctrl.oiCharInfo.changeAmount.pos
        
    @property
    def rot(self):
        return self.objctrl.oiCharInfo.changeAmount.rot
   
    @property
    def scale(self):
        return self.objctrl.oiCharInfo.changeAmount.scale

    def move(self, pos=None, rot=None, scale=None):
        if pos:
            if isinstance(pos, tuple) and len(pos) == 3:
                pos = Vector3(pos[0], pos[1], pos[2])
            self.objctrl.oiCharInfo.changeAmount.pos = pos
            
        if rot:
            if isinstance(rot, tuple) and len(rot) == 3:
                rot = Vector3(rot[0], rot[1], rot[2])
            self.objctrl.oiCharInfo.changeAmount.rot = rot
            
        if scale:
            if isinstance(scale, tuple) and len(scale) == 3:
                scale = Vector3(scale[0], scale[1], scale[2])
            self.objctrl.oiCharInfo.changeAmount.scale = scale

    def animate(self, group, category, no, normalizedTime = -1, force = 0):
        # group, category, no: key to anime clip, dump from scene please
        # normalizedTime: start time? 0~1?
        # force reload: true/false

        # check if no normalized time passed to function
        noNormalizedTime = (normalizedTime == -1)
        if noNormalizedTime:
            normalizedTime = 0

        curAnime = self.get_animate()
        if force \
                or curAnime[0] != group or curAnime[1] != category or curAnime[2] != no\
                or (self.get_anime_speed() == 0.0 and not noNormalizedTime and self.objctrl.charAnimeCtrl.normalizedTime != normalizedTime):
            self.objctrl.LoadAnime(group, category, no, normalizedTime)
        
    def get_animate(self):
        # return (group, category, no) in tuple
        aniInfo = []
        aniInfo.append(self.objctrl.oiCharInfo.animeInfo.group)
        aniInfo.append(self.objctrl.oiCharInfo.animeInfo.category)
        aniInfo.append(self.objctrl.oiCharInfo.animeInfo.no)
        if self.get_anime_speed() == 0.0:
            aniInfo.append(self.objctrl.charAnimeCtrl.normalizedTime)

        return tuple(aniInfo)
        
    def restart_anime(self):
        # restart current anime
        self.objctrl.RestartAnime()
        
    def set_anime_speed(self, speed):
        # speed: 0~3
        self.objctrl.animeSpeed = speed
        
    def get_anime_speed(self):
        # return anime speed
        return self.objctrl.animeSpeed

    def set_anime_pattern(self, pattern):
        # pattern: 0~1
        self.objctrl.animePattern = pattern
        
    def get_anime_pattern(self):
        # return anime pattern
        return self.objctrl.animePattern
        
    def set_anime_option_param(self, option):
        # option: (param1, param2)
        self.objctrl.animeOptionParam1 = option[0]
        self.objctrl.animeOptionParam2 = option[1]
        
    def get_anime_option_param(self):
        # return anime option param
        return (self.objctrl.animeOptionParam1, self.objctrl.animeOptionParam2)
        
    def set_anime_option_visible(self, visible):
        # visible: true/false
        self.objctrl.optionItemCtrl.visible = visible
        
    def get_anime_option_visible(self):
        # return anime option visible
        return self.objctrl.optionItemCtrl.visible
        
    def set_anime_forceloop(self, loop):
        # loop: 0(false)/1(true)
        self.objctrl.charAnimeCtrl.isForceLoop = bool(loop)
        
    def get_anime_forceloop(self):
        # return anime force loop status    
        return self.objctrl.charAnimeCtrl.isForceLoop
                
    def set_cloth(self, clothIndex, clothState=None):
        # set cloth will be different between engine
        raise Exception("Actor.set_cloth not implemented")
    
    def get_cloth(self):
        # get cloth will be different between engine
        raise Exception("Actor.get_cloth not implemented")
        
    def set_accessory(self, accIndex, accShow=None):
        # set accessory will be different between engine
        raise Exception("Actor.set_accessory not implemented")
        
    def get_accessory(self):
        # get accessory will be different between engine
        raise Exception("Actor.get_accessory not implemented")
        
    def set_juice(self, juices):
        # set juice will be different between engine
        raise Exception("Actor.set_juice not implemented")
        
    def get_juice(self):
        # get juice will be different between engine
        raise Exception("Actor.get_juice not implemented")
    
    def set_tear(self, level):
        # level: tears level 0,1,2,3 or 0~1
        self.objctrl.SetTearsLv(level)
    
    def get_tear(self):
        # return tear level
        return self.objctrl.GetTearsLv()
    
    def set_facered(self, level):
        # level: face red level 0~1
        self.objctrl.SetHohoAkaRate(level)
    
    def get_facered(self):
        # return face red level
        return self.objctrl.GetHohoAkaRate()
    
    def set_nipple_stand(self, level):
        # level: nipple stand level 0~1
        self.objctrl.SetNipStand(level)
        
    def get_nipple_stand(self):
        # return nipple stand level
        return self.objctrl.oiCharInfo.nipple
        
    def set_son(self, sonState):
        # son visible: 0(False)/1(True)
        if self.sex == 0:
            self.objctrl.SetVisibleSon(bool(sonState))
        
    def get_son(self):
        # return son visible
        return self.objctrl.oiCharInfo.visibleSon
        
    def set_simple(self, simpleState):
        # simple = one color, for male only: 1(true)/0(false)
        if self.sex == 0:
            self.objctrl.SetVisibleSimple(bool(simpleState))
        
    def get_simple(self):
        # return simple state, simple color) in tuple
        return self.objctrl.oiCharInfo.visibleSimple
        
    def set_simple_color(self, simpleColor):
        # simple color, for male only
        if self.sex == 0:
            self.objctrl.SetSimpleColor(tuple4_2_color(simpleColor))
    
    def get_simple_color(self):
        # get simple color
        return self.objctrl.oiCharInfo.simpleColor.rgbaDiffuse
        
    def set_look_eye(self, ptn_dir):
        # ptn_dir: 0: front, 1: camera, 2: hide from camera, 3: fix, 4: operate, or use Vector3 or tuple(3) to set a direction
        # when ptn_dir is Vector3 or (x, y, z), +x look right, -x look left, +y look up, -y look down
        if ptn_dir in range(0, 5):
            self.objctrl.ChangeLookEyesPtn(ptn_dir)
        else:
            if isinstance(ptn_dir, tuple) and len(ptn_dir) == 3:
                ptn_dir = Vector3(ptn_dir[0], ptn_dir[1], ptn_dir[2])
            self.objctrl.ChangeLookEyesPtn(4)
            self.objctrl.lookAtInfo.target.localPosition = ptn_dir
            #self.objctrl.ChangeLookEyesPtn(3)
    
    def get_look_eye(self):
        # return look eye ptn or look eye pos when ptn == 4
        ptn = self.get_look_eye_ptn()
        if ptn == 4:
            return self.get_look_eye_pos()
        else:
            return ptn
            
    def set_look_eye_ptn(self, ptn):
        # eye look at pattern: 0: front, 1: camera, 2: hide from camera, 3: fix, 4: operate
        self.objctrl.ChangeLookEyesPtn(ptn)

    def get_look_eye_ptn(self):
        # get look eye pattern will be different between engine
        raise Exception("Actor.get_look_eye_ptn not implemented")
        
    def set_look_eye_pos(self, pos):
        # set eye look at position: Vector3 or (x, y, z)
        if isinstance(pos, tuple):
            pos = Vector3(pos[0], pos[1], pos[2])
        self.objctrl.lookAtInfo.target.localPosition = pos
    
    def get_look_eye_pos(self):
        # return eye look at position: (x, y, z) as Vector3
        return self.objctrl.lookAtInfo.target.localPosition
    
    def set_look_neck(self, ptn):
        # ptn for CharaStudio: 0: front, 1: camera, 2: hide from camera, 3: by anime, 4: fix
        # ptn for PHStudio: 0: front, 1: camera, 2: by anime, 3: fix
        self.objctrl.ChangeLookNeckPtn(ptn)
        
    def get_look_neck(self):
        # get look neck pattern will be different between engine
        raise Exception("Actor.get_look_neck not implemented")
        
    def set_eyes_ptn(self, ptn):
        # ptn: 0 to 39
        self.objctrl.charInfo.ChangeEyesPtn(ptn)

    def get_eyes_ptn(self):
        # return eyes pattern
        return self.objctrl.charInfo.GetEyesPtn()
        
    def set_eyes_open(self, open):
        # open: 0~1
        self.objctrl.ChangeEyesOpen(open)
        
    def get_eyes_open(self):
        # return eyes open
        return self.objctrl.charInfo.fileStatus.eyesOpenMax
        
    def set_eyes_blink(self, flag):
        # flag: 0(false)/1(True)
        self.objctrl.ChangeBlink(flag)
        
    def get_eyes_blink(self):
        # return eyes blink flag
        return self.objctrl.charInfo.GetEyesBlinkFlag()
        
    def set_mouth_ptn(self, ptn):
        # ptn: 0 to x (depend on engine)
        self.objctrl.charInfo.ChangeMouthPtn(ptn)
        
    def get_mouth_ptn(self):
        # return mouth pattern
        return self.objctrl.charInfo.GetMouthPtn()
    
    def set_mouth_open(self, open):
        # open: 0~1
        self.objctrl.ChangeMouthOpen(open)
        
    def get_mouth_open(self):
        # return mouth open
        return self.objctrl.oiCharInfo.mouthOpen
        
    def set_lip_sync(self, flag):
        # flag: 0/1. 
        # this is the lip sync option for voice play, not for VNGameEngine
        self.objctrl.ChangeLipSync(flag)
        
    def get_lip_sync(self):
        # return lip sync status
        return self.oiCharInfo.lipSync
        
    def set_hand_ptn(self, ptn):
        # ptn: (left hand ptn, right hand ptn)
        self.objctrl.ChangeHandAnime(0, ptn[0])
        self.objctrl.ChangeHandAnime(1, ptn[1])
        
    def get_hand_ptn(self):
        # return (lptn, rptn) in tuple
        return tuple(self.objctrl.oiCharInfo.handPtn)
        
    def add_voice(self, group, category, no):
        # group, category, no: index of voice
        # refer to objctrl.charInfo.charFile.parameter.personality? aggressive? diligence?
        self.objctrl.AddVoice(group, category, no)
        
    def del_voice(self, index):
        # delete voice by index
        self.objctrl.DeleteVoice(index)

    def del_all_voice(self):
        # stop and delete all voice
        if self.isVoicePlay:
            self.stop_voice()
        self.objctrl.DeleteAllVoice()
        
    def set_voice_lst(self, voiceList, autoplay = True):
        # set a list of voice, load and play it
        # voiceList: tuple of voice: ((group, category, no), (group, category, no), ...)
        # autoplay: play voice
        self.del_all_voice()
        for v in voiceList:
            self.add_voice(v[0], v[1], v[2])
        if autoplay:
            self.play_voice()
        
    def get_voice_lst(self):
        # return a tuple of current loaded voice: ((group, category, no), (group, category, no), ...)
        vlist = []
        for v in self.objctrl.voiceCtrl.list:
            vi = (v.group, v.category, v.no)
            vlist.append(vi)
        return tuple(vlist)
        
    def set_voice_repeat(self, repeat):
        # set voice repeat: 0: no repeat, 1: repeat selected one, 2: repeat all
        from Studio import VoiceCtrl
        if repeat == 2:
            self.objctrl.voiceCtrl.repeat = VoiceCtrl.Repeat.All
        elif repeat == 1:
            self.objctrl.voiceCtrl.repeat = VoiceCtrl.Repeat.Select
        else:
            self.objctrl.voiceCtrl.repeat = VoiceCtrl.Repeat.None
        
    def get_voice_repeat(self):
        # return the status of voice repeat setting: 0: no repeat, 1: repeat selected one, 2: repeat all
        from Studio import VoiceCtrl
        if self.objctrl.voiceCtrl.repeat == VoiceCtrl.Repeat.All:
            return 2
        elif self.objctrl.voiceCtrl.repeat == VoiceCtrl.Repeat.Select:
            return 1
        else:
            return 0
        
    def play_voice(self, index = 0):
        # index = which voice to play
        if self.isVoicePlay:
            self.stop_voice()
        self.objctrl.PlayVoice(index)
    
    def stop_voice(self):
        # stop play voice
        self.objctrl.StopVoice()
                
    def set_kinematic(self, mode, force = 0):
        # mode: 0-none, 1-IK, 2-FK, 3-IK&FK(need plugin)
        raise Exception("Actor.set_kinematic not implemented")
            
    def get_kinematic(self):
        # return current kinematice mode: 0-none, 1-IK, 2-FK, 3-IK&FK
        kmode = 0
        if self.objctrl.oiCharInfo.enableIK:
            kmode += 1
        if self.objctrl.oiCharInfo.enableFK:
            kmode += 2
        return kmode
            
    def set_FK_active(self, group, active = None, force = 0):
        # param pattern 1: set one group
        # group: FK group: 0=hair, 1=neck, 2=Breast, 3=body, 4=right hand, 5=left hand, 6=skirt
        # active: 0/1
        # force: 0/1
        # param pattern 2: set all group
        # group: FK group 0/1 in tuple (hair, neck, Breast, body, right hand, left hand, skirt)
        # active: must be None
        # force: 0/1
        # param pattern 3: set all group to same state
        # group: 0/1 for all FK group
        # active: must be None
        # force: 0/1

        from Studio import OIBoneInfo
        bis = (OIBoneInfo.BoneGroup.Hair, OIBoneInfo.BoneGroup.Neck, OIBoneInfo.BoneGroup.Breast, OIBoneInfo.BoneGroup.Body, OIBoneInfo.BoneGroup.RightHand, OIBoneInfo.BoneGroup.LeftHand, OIBoneInfo.BoneGroup.Skirt)
        if active != None:
            try:
                self.objctrl.ActiveFK(bis[group], active, force)
            except Exception, e:
                print "Error in FK activate, group %s, err: %s" % (str(group),str(e))

        elif isinstance(group, tuple):
            for i in range(len(group) if len(group) <= 7 else 7):
                self.objctrl.ActiveFK(bis[i], group[i], force)
        else:
            for i in range(7):
                self.objctrl.ActiveFK(bis[i], group, force)

    def get_FK_active(self):
        # return active status for FK part, (hair, neck, Breast, body, right hand, left hand, skirt) in tuple
        return tuple(self.objctrl.oiCharInfo.activeFK)
        
    def export_fk_bone_info(self, activedOnly = 1):
        # export a dic contents FK bone info
        biDic = {}
        for i in range(len(self.objctrl.listBones)):
            binfo = self.objctrl.listBones[i]
            if (not activedOnly) or binfo.active:
                #posClone = Vector3(binfo.posision.x, binfo.posision.y, binfo.posision.z)
                rot = binfo.boneInfo.changeAmount.rot
                rotClone = Vector3(rot.x if rot.x <= 180 else rot.x - 360, rot.y if rot.y <= 180 else rot.y - 360, rot.z if rot.z <= 180 else rot.z - 360)
                #abDic[binfo.boneID] = (posClone, rotClone)
                biDic[i] = rotClone
        #print "exported", len(biDic), "bones"
        return biDic
        
    def import_fk_bone_info(self, biDic):
        # import fk bone info from dic
        for i in range(len(self.objctrl.listBones)):
            binfo = self.objctrl.listBones[i]
            if i in biDic:
                #binfo.boneInfo.changeAmount.pos = biDic[binfo.boneID][0]
                if biDic[i] is Vector3:
                    binfo.boneInfo.changeAmount.rot = biDic[i]
                else:
                    binfo.boneInfo.changeAmount.rot = Vector3(biDic[i][0], biDic[i][1], biDic[i][2])
        
    def set_IK_active(self, group, active = None, force = 0):
        # param pattern 1: set one group
        # group: IK group: 0=body, 1=right leg, 2=left leg, 3=right arm, 4=left arm
        # active: 0/1
        # force: 0/1
        # param pattern 2: set all group
        # group: IK group 0/1 in tuple (body, right leg, left leg, right arm, left arm)
        # active: must be None
        # force: 0/1
        # param pattern 3: set all group to same state
        # group: 0/1 for all IK group
        # active: must be None
        # force: 0/1
        from Studio import OIBoneInfo
        bis = (OIBoneInfo.BoneGroup.Body, OIBoneInfo.BoneGroup.RightLeg, OIBoneInfo.BoneGroup.LeftLeg, OIBoneInfo.BoneGroup.RightArm, OIBoneInfo.BoneGroup.LeftArm)
        if active != None:
            self.objctrl.ActiveIK(bis[group], active, force)
        elif isinstance(group, tuple):
            for i in range(len(group) if len(group) <= 5 else 5):
                self.objctrl.ActiveIK(bis[i], group[i], force)
        else:
            for i in range(5):
                self.objctrl.ActiveIK(bis[i], group, force)
    
    def get_IK_active(self):
        # return active status for IK part, (body, right leg, left leg, right arm, left arm) in tuple
        return tuple(self.objctrl.oiCharInfo.activeIK)
        
    def export_ik_target_info(self, activedOnly = 1):
        # export a dic contents IK target info
        itDic = {}
        for itInfo in self.objctrl.listIKTarget:
            if (not activedOnly) or itInfo.active:
                tgtName = itInfo.boneObject.name
                pos = itInfo.targetInfo.changeAmount.pos
                posClone = Vector3(pos.x, pos.y, pos.z)
                if "_Hand_" in tgtName or "_Foot01_" in tgtName:
                    rot = itInfo.targetInfo.changeAmount.rot
                    rotClone = Vector3(rot.x, rot.y, rot.z)
                    #rotClone = Vector3(rot.x if rot.x <= 180 else rot.x - 360, rot.y if rot.y <= 180 else rot.y - 360, rot.z if rot.z <= 180 else rot.z - 360)
                    itDic[tgtName]= (posClone, rotClone)
                else:
                    itDic[tgtName]= (posClone, )
        #print "exported", len(itDic), "IK Targets"
        return itDic
        
    def import_ik_target_info(self, itDic):
        # import IK target info from dic 
        for ikTgt in self.objctrl.listIKTarget:
            ikTgName = ikTgt.boneObject.name
            if ikTgName in itDic:
                if isinstance(itDic[ikTgName][0], Vector3):
                    ikTgt.targetInfo.changeAmount.pos = itDic[ikTgName][0]
                else:
                    ikTgt.targetInfo.changeAmount.pos = Vector3(itDic[ikTgName][0][0], itDic[ikTgName][0][1], itDic[ikTgName][0][2])
                if ("_Hand_" in ikTgName or "_Foot01_" in ikTgName) and len(itDic[ikTgName]) == 2:
                    if isinstance(itDic[ikTgName][1], Vector3):
                        ikTgt.targetInfo.changeAmount.rot = itDic[ikTgName][1]
                    else:
                        ikTgt.targetInfo.changeAmount.rot = Vector3(itDic[ikTgName][1][0], itDic[ikTgName][1][1], itDic[ikTgName][1][2])

    def import_status(self, status):
        for f in status:
            if f in char_act_funcs:
                char_act_funcs[f][0](self, status[f])
            else:
                print "act error: unknown function '%s' for actor!" % (f)

    def import_status_diff_optimized(self, status):
        ofs = self.export_full_status()
        dfs = {}
        for key in status.Keys:
            if not key in ofs.Keys or ofs[key] != status[key]:
                dfs[key] = status[key]
        #return dfs
        #print "Optimized import status diff, ", dfs
        self.import_status(dfs)                                                   
    
    def export_full_status(self):
        # export a dict contains all actor status, different between engine
        raise Exception("Actor.export_full_status is not implemented")
        
    def export_diff_status(self, diff):
        # export a dict contains diff from another status
        ofs = self.export_full_status()
        dfs = {}
        for key in ofs.Keys:
            if not key in diff.Keys or ofs[key] != diff[key]:
                dfs[key] = ofs[key]
        return dfs
        
    def load_clothes_file(self, file):
        # load a clothes file
        self.objctrl.LoadClothesFile(file)

    # body sliders
    # see sceneutils.py for realization of this props
    def get_body_shape(self, p1):
        return 0

    def set_body_shape(self, p1, p2):
        pass

    def get_body_shapes_all(self):
        ct = self.get_body_shapes_count()
        res = []
        for i in range(ct):
            res.append(self.get_body_shape(i))
        return res

    def get_body_shape_names(self):
        return ()

    def get_body_shapes_count(self):
        return 0

    def set_body_shapes_all(self, arr):
        for i in range(len(arr)):
            self.set_body_shape(i, arr[i])

    # face sliders
    def get_face_shape(self, p1):
        return 0
    
    def set_face_shape(self, p1, p2):
        pass

    def get_face_shapes_all(self):
        ct = self.get_face_shapes_count()
        res = []
        for i in range(ct):
            res.append(self.get_face_shape(i))
        return res

    def get_face_shape_names(self):
        return ()

    def get_face_shapes_count(self):
        return 0

    def set_face_shapes_all(self, arr):
        for i in range(len(arr)):
            self.set_face_shape(i, arr[i])

class ActorHSNeo(Actor):
    @property
    def sex(self):
        # get sex: 0-male, 1-female
        return self.objctrl.charInfo.Sex

    @property
    def height(self):
        # get height:
        return self.objctrl.oiCharInfo.charFile.femaleCustomInfo.shapeValueBody[0]

    @height.setter
    def height(self, value):
        # set height
        self.set_body_shape(0, value)

    @property
    def breast(self):
        # get breast:
        return self.objctrl.oiCharInfo.charFile.femaleCustomInfo.shapeValueBody[1]
        
    @breast.setter
    def breast(self, value):
        # set breast
        self.set_body_shape(1, value)

    def set_coordinate_type(self, type):
        # type: 0-normal, 1-room, 2-swim
        from CharDefine import CoordinateType
        if type == 0:
            type = CoordinateType.type00
        elif type == 1:
            type = CoordinateType.type01
        else:
            type = CoordinateType.type02
        self.objctrl.SetCoordinateInfo(type)
        
    def get_coordinate_type(self):
        # return coordinate type
        from CharDefine import CoordinateType
        if self.objctrl.charFileInfoStatus.coordinateType == CoordinateType.type00:
            return 0
        elif self.objctrl.charFileInfoStatus.coordinateType == CoordinateType.type01:
            return 1
        else:
            return 2
        
    def set_cloth(self, clothIndex, clothState=None):
        # param format 1: set one cloth
        # clothIndex: 0-top, 1-bottom, 2-bra, 3-shorts, 4-swim-up, 5-swim-down, 6-swim-top, 7-swim-bottom, 8-grove, 9-panst, 10-sock, 11-shoes
        # clothState: 0-put on, 1-half off, 2-off 
        # param format 2: set all clothes, like the return value of get_cloth()
        # clothIndex: state for (top, bottom, bra, shorts, swim-up, swim-down, swim-top, swim-bottom, grove, panst, sock, shoes) in tuple
        # clothState: must be None
        # param format 3: set all cloth to same state
        # clothIndex: state of all clothes
        # clothState: must be None
        if clothState != None:
            self.objctrl.SetClothesState(clothIndex, clothState)
        elif isinstance(clothIndex, tuple):
            for i in range(len(clothIndex) if len(clothIndex) <= 12 else 12):
                self.objctrl.SetClothesState(i, clothIndex[i])
        else:
            #self.objctrl.SetClothesStateAll(clothIndex) # this function may crash the game
            for i in range(12):
                self.objctrl.SetClothesState(i, clothIndex)
    
    def get_cloth(self):
        # return state index of (top, bottom, bra, shorts, swim-up, swim-down, swim-top, swim-bottom, grove, panst, sock, shoes) in tuple
        return tuple(self.objctrl.charFileInfoStatus.clothesState)

    def set_accessory(self, accIndex, accShow=None):
        # param format 1: set one accessory
        # accIndex: 0~9
        # accShow: 0(hide)/1(visible)
        # param format 2: set all accessory, like the return value of get_accessory()
        # accIndex: 0/1 for each acessories in tuple(10)
        # accShow: must be None
        # param format 3: hide/show all accessory
        # accIndex: 0/1 for all
        # accShow: must be None
        if accShow != None:
            self.objctrl.ShowAccessory(accIndex, accShow)
        elif isinstance(accIndex, tuple):
            for i in range(len(accIndex) if len(accIndex) <= 10 else 10):
                self.objctrl.ShowAccessory(i, accIndex[i])
        else:
            for i in range(10):
                self.objctrl.ShowAccessory(i, accIndex)
        
    def get_accessory(self):
        # return accessory state on/off in tuple(10)
        return tuple(self.objctrl.charFileInfoStatus.showAccessory)
        
    def set_juice(self, juices):
        # juices: level on (face, FrontUp, BackUp, FrontDown, BackDown) when 0-none, 1-few, 2-lots
        # use self.objctrl.SetSiruFlags in console will cause the the game crash, but seems ok in frame
        from CharDefine import SiruParts
        self.objctrl.SetSiruFlags(SiruParts.SiruKao, juices[0])
        self.objctrl.SetSiruFlags(SiruParts.SiruFrontUp, juices[1])
        self.objctrl.SetSiruFlags(SiruParts.SiruBackUp, juices[2])
        self.objctrl.SetSiruFlags(SiruParts.SiruFrontDown, juices[3])
        self.objctrl.SetSiruFlags(SiruParts.SiruBackDown, juices[4])
        
    def get_juice(self):
        # return juice level of (face, FrontUp, BackUp, FrontDown, BackDown) in tuple
        from CharDefine import SiruParts
        jInfo = []
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruKao))
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruFrontUp))
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruBackUp))
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruFrontDown))
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruBackDown))
        return tuple(jInfo)

    def set_tuya(self, level):
        # level: tuya 0~1
        self.objctrl.SetTuyaRate(level)
        
    def get_tuya(self):
        # return tuya rate
        return self.objctrl.oiCharInfo.skinRate

    def get_look_eye_ptn(self):
        # return eye look at pattern: 0: front, 1: camera, 2: hide from camera, 3: fix, 4: operate
        return self.objctrl.charFileInfoStatus.eyesLookPtn

    def get_look_neck(self):
        # return neck look pattern: 0: front, 1: camera, 2: by anime, 3: fix
        return self.objctrl.charFileInfoStatus.neckLookPtn
        
    # keitaro 2.3.1
    def get_look_neck_full(self):
        # needed only to save Fixed state
        if self.get_look_neck() == 4:
            from System.IO import MemoryStream, BinaryWriter
            memoryStream = MemoryStream()
            binaryWriter = BinaryWriter(memoryStream)
            self.objctrl.neckLookCtrl.SaveNeckLookCtrl(binaryWriter)
            binaryWriter.Close()
            memoryStream.Close()
            return tuple(bytearray_to_list(memoryStream.ToArray()))
        else:
            return ()

    def set_look_neck_full(self, arrstatetuple):
        # needed only to set Fixed state
        if len(arrstatetuple) > 0:  # if non-fixed-state - move to it!
            self.set_look_neck(4)

        if self.get_look_neck() == 4:
            lst = list(arrstatetuple)
            # print lst
            arrstate = list_to_bytearray(lst)
            # print arrstate
            from System.IO import MemoryStream, BinaryWriter, BinaryReader
            binaryReader = BinaryReader(MemoryStream(arrstate))
            self.objctrl.neckLookCtrl.LoadNeckLookCtrl(binaryReader)

    def get_look_neck_full2(self):
        # needed only to save Fixed state
        if self.get_look_neck() == 4:
            from System.IO import MemoryStream, BinaryWriter
            memoryStream = MemoryStream()
            binaryWriter = BinaryWriter(memoryStream)
            self.objctrl.neckLookCtrl.SaveNeckLookCtrl(binaryWriter)
            binaryWriter.Close()
            memoryStream.Close()
            return bytearray_to_str64(memoryStream.ToArray())
        else:
            return ''

    def set_look_neck_full2(self, str64):
        # needed only to set Fixed state
        if len(str64) > 0:  # if non-fixed-state - move to it!
            self.set_look_neck(4)

        if self.get_look_neck() == 4:
            # print lst
            arrstate = str64_to_bytearray(str64)
            # print arrstate
            from System.IO import MemoryStream, BinaryWriter, BinaryReader
            binaryReader = BinaryReader(MemoryStream(arrstate))
            self.objctrl.neckLookCtrl.LoadNeckLookCtrl(binaryReader)

    def get_curcloth_coordinate(self):
        from System.IO import MemoryStream, BinaryWriter
        chaFile = self.objctrl.charInfo.chaFile
        memoryStream = MemoryStream()
        binaryWriter = BinaryWriter(memoryStream)
        chaFile.clothesInfo.Save(binaryWriter)
        binaryWriter.Close()
        memoryStream.Close()
        return bytearray_to_str64(memoryStream.ToArray())

    def set_curcloth_coordinate(self,str64):
        from System.IO import MemoryStream, BinaryWriter
        bytes = str64_to_bytearray(str64)
        #import ChaFileDefine
        charInfo = self.objctrl.charInfo
        try:
            charInfo.chaFile.clothesInfo.Load(MemoryStream(bytes), True)
            #charInfo.chaFile.SetCoordinateInfo(coordinateType)
            charInfo.Reload(False, True, True)
            if (charInfo.Sex == 1):  # only female
                charInfo.UpdateBustSoftnessAndGravity()

        except Exception, e:
            print "Exception in set_curcloth_coordinate, %s" % ( str(e))

    def get_eyes_open(self):
        # return eyes open
        return self.objctrl.charFileInfoStatus.eyesOpenMax

    def get_eyes_blink(self):
        # return eyes blink flag
        return self.objctrl.charFileInfoStatus.eyesBlink
        
    def set_kinematic(self, mode, force = 0):
        # mode: 0-none, 1-IK, 2-FK, 3-IK&FK(need plugin)
        from Studio import OICharInfo
        if mode == 3:
            try:
                from extplugins import HSStudioNEOAddon
                hsa = HSStudioNEOAddon()
                hsa.activateFKIK(self)
            except Exception as e:
                print "Fail to set IK&FK:", e
        elif mode == 2:
            if self.objctrl.oiCharInfo.enableIK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, 0, force)
            if not self.objctrl.oiCharInfo.enableFK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, 1, force)
        elif mode == 1:
            if self.objctrl.oiCharInfo.enableFK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, 0, force)
            if not self.objctrl.oiCharInfo.enableIK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, 1, force)
        else:
            if self.objctrl.oiCharInfo.enableIK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, 0, force)
            if self.objctrl.oiCharInfo.enableFK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, 0, force)

    def get_hspedata(self):
        import extplugins
        if extplugins.ExtPlugin.exists("HSPENeo"):
            return extplugins.HSPENeo().GetCharaSettingsText(self.objctrl)

        return ""

    def set_hspedata(self, hspedata):
        #print "in hspedata"
        if hspedata != "":
            import extplugins
            if extplugins.ExtPlugin.exists("HSPENeo"):
                #print "import hspedata"
                extplugins.HSPENeo().SetCharaSettingsText(self.objctrl, hspedata)
                #print "import hspedata2"

    def get_body_shape(self, p1):
        return self.objctrl.charBody.charCustom.GetShapeBodyValue(p1)

    def set_body_shape(self, p1, p2):
        self.objctrl.charBody.charCustom.SetShapeBodyValue(p1, p2)

    def get_body_shapes_all(self):
        if self.sex == 0:
            return tuple(self.objctrl.oiCharInfo.charFile.maleCustomInfo.shapeValueBody)
        else:
            return tuple(self.objctrl.oiCharInfo.charFile.femaleCustomInfo.shapeValueBody)

    def get_body_shape_names(self):
        import CharDefine
        if self.sex == 0:
            return CharDefine.cm_bodyshapename
        else:
            return CharDefine.cf_bodyshapename

    def get_body_shapes_count(self):
        return len(self.get_body_shapes_all())

    def get_face_shape(self, p1):
        return self.objctrl.charBody.charCustom.GetShapeFaceValue(p1)

    def set_face_shape(self, p1, p2):
        self.objctrl.charBody.charCustom.SetShapeFaceValue(p1, p2)

    def get_face_shapes_all(self):
        if self.sex == 0:
            return tuple(self.objctrl.oiCharInfo.charFile.maleCustomInfo.shapeValueFace)
        else:
            return tuple(self.objctrl.oiCharInfo.charFile.femaleCustomInfo.shapeValueFace)

    def get_face_shape_names(self):
        import CharDefine
        if self.sex == 0:
            return CharDefine.cm_headshapename
        else:
            return CharDefine.cf_headshapename

    def get_face_shapes_count(self):
        return len(self.get_face_shapes_all())

    def export_full_status(self):
        # export a dict contains all actor status
        fs = {}
        fs["visible"] = self.visible
        fs["move_to"] = self.pos
        fs["rotate_to"] = self.rot
        fs["scale_to"] = self.scale
        fs["anim"] = self.get_animate()
        fs["anim_spd"] = self.get_anime_speed()
        fs["anim_ptn"] = self.get_anime_pattern()
        fs["anim_lp"] = self.get_anime_forceloop()
        fs["cloth_type"] = self.get_coordinate_type()
        fs["cloth_all"] = self.get_cloth()
        fs["acc_all"] = self.get_accessory()
        if self.sex == 1:
            fs["juice"] = self.get_juice()
            fs["tear"] = self.get_tear()
            fs["face_red"] = self.get_facered()
            fs["nip_stand"] = self.get_nipple_stand()
            fs["skin_tuya"] = self.get_tuya()
        else:
            fs["son"] = self.get_son()
            fs["simple"] = self.get_simple()
            fs["simple_color"] = self.get_simple_color()
        fs["look_at_ptn"] = self.get_look_eye_ptn()
        fs["look_at_pos"] = self.get_look_eye_pos()
        fs["face_to"] = self.get_look_neck()
        fs["face_to_full2"] = self.get_look_neck_full2()
        fs["eyes"] = self.get_eyes_ptn()
        fs["eyes_open"] = self.get_eyes_open()
        fs["eyes_blink"] = self.get_eyes_blink()
        fs["mouth"] = self.get_mouth_ptn()
        fs["mouth_open"] = self.get_mouth_open()
        fs["lip_sync"] = self.get_lip_sync()
        fs["hands"] = self.get_hand_ptn()
        fs["kinematic"] = self.get_kinematic()
        fs["fk_active"] = self.get_FK_active()
        fs["fk_set"] = self.export_fk_bone_info()
        fs["ik_active"] = self.get_IK_active()
        fs["ik_set"] = self.export_ik_target_info()
        fs["voice_lst"] = self.get_voice_lst()
        fs["voice_rpt"] = self.get_voice_repeat()

        # ext data, enable by ini setting
        if is_ini_value_true("ExportChara_CurClothesCoord"):
            fs["ext_curclothcoord"] = self.get_curcloth_coordinate()
        if is_ini_value_true("ExportChara_BodyShapes"):
            fs["ext_bodyshapes"] = self.get_body_shapes_all()
        if is_ini_value_true("ExportChara_FaceShapes"):
            fs["ext_faceshapes"] = self.get_face_shapes_all()
        if is_ini_value_true("ExportChara_AnimeAuxParam"):
            fs["anim_optprm"] = self.get_anime_option_param()

        # plugin data, enable by ini setting
        try:
            import extplugins
            if extplugins.ExtPlugin.exists("HSPENeo"):
                if is_ini_value_true("ExportChara_HSPENeo"):
                    fs["pl_hspedata"] = self.get_hspedata()
        except Exception, e:
            print "Error during get hspedata"
            pass

        return fs

    def h_partner(self, hType=0, hPosition=0):
        # return partner sex for current h
        if hType != 4:
            if self.sex == 0:
                return (1,)
            else:
                return (0,)
        else:
            #print "htype = 4: multi, hPosition =", hPosition
            if hPosition in range(0, 4):
                if self.sex == 0:
                    return (1, 0)
                else:
                    return (0, 0)
            elif hPosition in range(4, 12):
                if self.sex == 0:
                    return (1, 1)
                else:
                    return (0, 1)
            else:
                if self.sex == 0:
                    return (1, 1)
                else:
                    return (1,)
        
    def h_with(self, partner, hType=0, hPosition=0, hStage=0, extActors=()):
        # partner: another actor as sex partner
        # hType: 1-11
        # hPosition:?
        # hStage:?
        # extActors = (Actor1, Actor2, Actor3)
        # sync with partner
        if self.pos != partner.pos or self.rot != partner.rot or self.scale != partner.scale:
            partner.move(pos=self.pos, rot=self.rot, scale=self.scale)
        if self.get_anime_speed() != partner.get_anime_speed():
            partner.set_anime_speed(self.get_anime_speed())
        if self.get_anime_pattern() != partner.get_anime_pattern():
            partner.set_anime_pattern(self.get_anime_pattern())
        if self.get_anime_forceloop() != partner.get_anime_forceloop():
            partner.set_anime_forceloop(self.get_anime_forceloop())
        for extActor in extActors:
            if extActor == None:
                continue
            #print "get ext actor " + extActor.text_name
            if self.pos != extActor.pos or self.rot != extActor.rot or self.scale != extActor.scale:
                extActor.move(pos=self.pos, rot=self.rot, scale=self.scale)
            if self.get_anime_speed() != extActor.get_anime_speed():
                extActor.set_anime_speed(self.get_anime_speed())
            if self.get_anime_pattern() != extActor.get_anime_pattern():
                extActor.set_anime_pattern(self.get_anime_pattern())
            if self.get_anime_forceloop() != extActor.get_anime_forceloop():
                extActor.set_anime_forceloop(self.get_anime_forceloop())
        # decide sex role
        if self.sex == 0:
            mactor = self
            factor = partner
        else:
            mactor = partner
            factor = self
        # show son if not
        if mactor.sex == 0 and not mactor.get_son():
            mactor.set_son(1)
        for extActor in extActors:
            if extActor != None and extActor.sex == 0 and not extActor.get_son():
                extActor.set_son(1)
        # load anime
        from Studio import Info
        info = Info.Instance
        gcDic = info.dicFAGroupCategory
        aDic = info.dicFemaleAnimeLoadInfo
        gp = range(3, 9)[hType]
        validCategoryKey = list(gcDic[gp].dicCategory.Keys)
        if not hPosition in range(len(validCategoryKey)):
            print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
            return
        cat = validCategoryKey[hPosition]
        validNoKey = list(aDic[gp][cat].Keys)
        if not hStage in range(len(validNoKey)):
            print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
            return
        no = validNoKey[hStage]
        if gp != 7:
            #print "do %s > %s > %s"%(gcDic[gp].name, gcDic[gp].dicCategory[cat], aDic[gp][cat][no].name)
            #print "mactor.animate(%d, %d, %d)"%(gp, cat, no)
            #print "factor.animate(%d, %d, %d)"%(gp, cat, no)
            mactor.animate(gp, cat, no)
            factor.animate(gp, cat, no)
        else:
            if cat in range(130, 134):
                mactor.animate(gp, cat, no)
                factor.animate(gp, cat, no)
                if len(extActors) > 0 and extActors[0] != None:
                    extActors[0].animate(gp, cat+24, no)
            elif cat in range(134, 138):
                mactor.animate(gp, cat, no)
                factor.animate(gp, cat, no)
                if len(extActors) > 0 and extActors[0] != None:
                    extActors[0].animate(gp, cat+24, no)
            elif cat in range(158, 162):
                mactor.animate(gp, cat-24, no)
                factor.animate(gp, cat, no)
                if len(extActors) > 0 and extActors[0] != None:
                    extActors[0].animate(gp, cat-24, no)
            elif cat == 138 or cat == 139:
                mactor.animate(gp, cat+24, no)
                factor.animate(gp, cat, no)
            else:
                mactor.animate(gp, cat-24, no)
                factor.animate(gp, cat, no)
        # auto adjust anime param
        #print "factor(%s): height=%.2f breast=%.2f"%(factor.text_name, factor.height, factor.breast)
        anime_option_param = (factor.height, factor.breast)
        if mactor.isHAnime:
            mactor.set_anime_option_param(anime_option_param)
        for extActor in extActors:
            if extActor != None and extActor.isHAnime:
                extActor.set_anime_option_param(anime_option_param)
    
    def get_anime_info_text(self):
        info = "Anime Pattern: "
        from Studio import Info
        gcDic = Info.Instance.dicFAGroupCategory
        dic = Info.Instance.dicFemaleAnimeLoadInfo
        chAniInfo = self.objctrl.oiCharInfo.animeInfo
        info += "[%d]<color=#ff0000>%s</color>"%(chAniInfo.group, gcDic[chAniInfo.group].name)
        info += " >> "
        info += "[%d]<color=#ffff00>%s</color>"%(chAniInfo.category, gcDic[chAniInfo.group].dicCategory[chAniInfo.category])
        info += " >> "
        info += "[%d]<color=#00ff00>%s</color>"%(chAniInfo.no, dic[chAniInfo.group][chAniInfo.category][chAniInfo.no].name)

        cis = self.objctrl.charAnimeCtrl.animator.GetCurrentAnimatorClipInfo(0)
        clip = cis[0].clip
        info2 = "Anime Length: org = %.2f sec (%d frames)"%(clip.length, clip.length * clip.frameRate)
        spd = self.get_anime_speed()
        if spd > 0:
            info2 += ", cur = %.2f sec (@ %.2fx speed)"%(clip.length / spd, spd)

        return info, info2
            
    @staticmethod
    def get_hanime_group_names():
        from Studio import Info
        info = Info.Instance
        gcDic = info.dicFAGroupCategory
        return tuple(gcDic[i].name for i in range(3, 9))
        
    @staticmethod
    def get_hanime_category_names(group):
        from Studio import Info
        info = Info.Instance
        group = range(3, 9)[group]
        cDic = info.dicFAGroupCategory[group].dicCategory
        return tuple(cDic.Values)
    
    @staticmethod
    def get_hanime_no_names(group, category):
        from Studio import Info
        info = Info.Instance
        nDic = info.dicFemaleAnimeLoadInfo
        group = range(3, 9)[group]
        category = tuple(info.dicFAGroupCategory[group].dicCategory.Keys)[category]
        nName = []
        for n in nDic[group][category].Keys:
            nName.append(nDic[group][category][n].name)
        return tuple(nName)

class ActorPHStudio(Actor):
    @property
    def sex(self):
        # get sex: 0-male, 1-female
        return self.objctrl.charInfo.sex
        
    @property
    def height(self):
        # get height:
        return self.objctrl.oiCharInfo.charFile.body.shapeVals[0]

    @height.setter
    def height(self, value):
        # set height
        self.set_body_shape(0, value)

    @property
    def breast(self):
        # get breast:
        return self.objctrl.oiCharInfo.charFile.body.shapeVals[1]
        
    @breast.setter
    def breast(self, value):
        # set breast
        self.set_body_shape(1, value)

    def set_anime_pattern(self, pattern):
        # pattern: Vector2(-1~1, -1~1) or tuple
        if isinstance(pattern, tuple):
            pattern = Vector2(pattern[0], pattern[1])
        self.objctrl.animePattern = pattern

    def set_cloth(self, clothIndex, clothState=None):
        # param format 1: set one cloth
        # clothIndex: 0-top, 1-bottom, 2-bra, 3-shorts, 4-swim-up, 5-swim-down, 6-swim-top, 7-swim-bottom, 8-grove, 9-panst, 10-sock, 11-shoes
        # clothState: 0-put on, 1-half off, 2-off 
        # param format 2: set all clothes, like the return value of get_cloth()
        # clothIndex: state for (top, bottom, bra, shorts, swim-up, swim-down, swim-top, swim-bottom, grove, panst, sock, shoes) in tuple
        # clothState: must be None
        # param format 3: set all cloth to same state
        # clothIndex: state of all clothes
        # clothState: must be None
        if clothState != None:
            self.objctrl.SetClothesState(clothIndex, clothState)
        elif isinstance(clothIndex, tuple):
            for i in range(len(clothIndex) if len(clothIndex) <= 12 else 12):
                self.objctrl.SetClothesState(i, clothIndex[i])
        else:
            #self.objctrl.SetClothesStateAll(clothIndex) # this function may crash the game
            for i in range(12):
                self.objctrl.SetClothesState(i, clothIndex)
    
    def get_cloth(self):
        # return state index of (top, bottom, bra, shorts, swim-up, swim-down, swim-top, swim-bottom, grove, panst, sock, shoes) in tuple
        return tuple(self.objctrl.charStatus.clothesState)
        
    def set_accessory(self, accIndex, accShow=None):
        # param format 1: set one accessory
        # accIndex: 0~9
        # accShow: 0(hide)/1(visible)
        # param format 2: set all accessory, like the return value of get_accessory()
        # accIndex: 0/1 for each acessories in tuple(10)
        # accShow: must be None
        # param format 3: hide/show all accessory
        # accIndex: 0/1 for all
        # accShow: must be None
        if accShow != None:
            self.objctrl.ShowAccessory(accIndex, accShow)
        elif isinstance(accIndex, tuple):
            for i in range(len(accIndex) if len(accIndex) <= 10 else 10):
                self.objctrl.ShowAccessory(i, accIndex[i])
        else:
            for i in range(10):
                self.objctrl.ShowAccessory(i, accIndex)
        
    def get_accessory(self):
        # return accessory state on/off in tuple(10)
        return tuple(self.objctrl.charStatus.showAccessory)
        
    def set_juice(self, juices):
        # juices: level on (face, FrontUp, BackUp, FrontDown, BackDown) when 0-none, 1-few, 2-lots
        # use self.objctrl.SetSiruFlags in console will cause the the game crash, but seems ok in frame
        from SEXY import CharDefine
        self.objctrl.SetSiruFlags(CharDefine.SiruParts.SiruKao, juices[0])
        self.objctrl.SetSiruFlags(CharDefine.SiruParts.SiruFrontUp, juices[1])
        self.objctrl.SetSiruFlags(CharDefine.SiruParts.SiruBackUp, juices[2])
        self.objctrl.SetSiruFlags(CharDefine.SiruParts.SiruFrontDown, juices[3])
        self.objctrl.SetSiruFlags(CharDefine.SiruParts.SiruBackDown, juices[4])
        
    def get_juice(self):
        # return juice level of (face, FrontUp, BackUp, FrontDown, BackDown) in tuple
        from SEXY import CharDefine
        jInfo = []
        jInfo.append(self.objctrl.GetSiruFlags(CharDefine.SiruParts.SiruKao))
        jInfo.append(self.objctrl.GetSiruFlags(CharDefine.SiruParts.SiruFrontUp))
        jInfo.append(self.objctrl.GetSiruFlags(CharDefine.SiruParts.SiruBackUp))
        jInfo.append(self.objctrl.GetSiruFlags(CharDefine.SiruParts.SiruFrontDown))
        jInfo.append(self.objctrl.GetSiruFlags(CharDefine.SiruParts.SiruBackDown))
        return tuple(jInfo)

    def set_tuya(self, level):
        # level: tuya 0~1
        self.objctrl.SetTuyaRate(level)
        
    def get_tuya(self):
        # return tuya rate
        return self.objctrl.oiCharInfo.skinRate
        
    def set_face_option(self, index):
        # index: 0-None, 1-ball, 2-tape
        self.objctrl.ChangeFaceOption(index)

    def get_face_option(self):
        # return face option
        return self.objctrl.oiCharInfo.faceOption
        
    def get_simple_color(self):
        # return simple color
        simpleColor = self.objctrl.oiCharInfo.simpleColor
        return simpleColor

    def get_look_eye_ptn(self):
        # return eye look at pattern: 0: front, 1: camera, 2: hide from camera, 3: fix, 4: operate
        return self.objctrl.charStatus.eyesLookPtn

    def get_look_neck(self):
        # return neck look pattern: 0: front, 1: camera, 2: by anime, 3: fix
        return self.objctrl.charStatus.neckLookPtn

    def set_kinematic(self, mode, force = 0):
        # mode: 0-none, 1-IK, 2-FK, 3-IK&FK(need plugin)
        from Studio import OICharInfo
        if mode == 3:
            try:
                from extplugins import PHSAddon
                pha = PHSAddon()
                pha.activateFKIK(self)
            except Exception as e:
                print "Fail to set IK&FK:", e
        elif mode == 2:
            if self.objctrl.oiCharInfo.enableIK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, 0, force)
            if not self.objctrl.oiCharInfo.enableFK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, 1, force)
        elif mode == 1:
            if self.objctrl.oiCharInfo.enableFK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, 0, force)
            if not self.objctrl.oiCharInfo.enableIK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, 1, force)
        else:
            if self.objctrl.oiCharInfo.enableIK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, 0, force)
            if self.objctrl.oiCharInfo.enableFK:
                self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, 0, force)

    def get_body_shape(self, p1):
        return self.charInfo.GetShapeBodyValue(p1)

    def set_body_shape(self, p1, p2):
        self.charInfo.human.body.SetShape(p1, p2)

    def get_body_shapes_all(self):
        if self.sex == 0:
            return tuple(self.objctrl.oiCharInfo.charFile.body.shapeVals)[:21]
        else:
            return tuple(self.objctrl.oiCharInfo.charFile.body.shapeVals)

    def get_body_shape_names(self):
        from SEXY import CharDefine
        if self.sex == 0:
            return CharDefine.cm_bodyshapename
        else:
            return CharDefine.cf_bodyshapename

    def get_body_shapes_count(self):
        return len(self.get_body_shapes_all())

    def get_face_shape(self, p1):
        return self.get_face_shapes_all()[p1]

    def set_face_shape(self, p1, p2):
        self.charInfo.human.head.SetShape(p1, p2)

    def get_face_shapes_all(self):
        return tuple(self.objctrl.oiCharInfo.charFile.head.shapeVals)

    def get_face_shape_names(self):
        from SEXY import CharDefine
        if self.sex == 0:
            return CharDefine.cm_headshapename
        else:
            return CharDefine.cf_headshapename

    def get_face_shapes_count(self):
        return len(self.get_face_shapes_all())

    def export_full_status(self):
        # export a dict contains all actor status
        fs = {}
        fs["visible"] = self.visible
        fs["move_to"] = self.pos
        fs["rotate_to"] = self.rot
        fs["scale_to"] = self.scale
        fs["anim"] = self.get_animate()
        fs["anim_spd"] = self.get_anime_speed()
        fs["anim_ptn"] = self.get_anime_pattern()
        fs["anim_lp"] = self.get_anime_forceloop()
        fs["cloth_all"] = self.get_cloth()
        fs["acc_all"] = self.get_accessory()
        if self.sex == 1:
            fs["juice"] = self.get_juice()
            fs["tear"] = self.get_tear()
            fs["face_red"] = self.get_facered()
            fs["nip_stand"] = self.get_nipple_stand()
            fs["skin_tuya"] = self.get_tuya()
            fs["face_opt"] = self.get_face_option()
        else:
            fs["son"] = self.get_son()
            fs["simple"] = self.get_simple()
            fs["simple_color"] = self.get_simple_color()
        fs["look_at_ptn"] = self.get_look_eye_ptn()
        fs["look_at_pos"] = self.get_look_eye_pos()
        fs["face_to"] = self.get_look_neck()
        #fs["face_to_full"] = self.get_look_neck_full()
        fs["eyes"] = self.get_eyes_ptn()
        fs["eyes_open"] = self.get_eyes_open()
        fs["eyes_blink"] = self.get_eyes_blink()
        fs["mouth"] = self.get_mouth_ptn()
        fs["mouth_open"] = self.get_mouth_open()
        fs["lip_sync"] = self.get_lip_sync()
        fs["hands"] = self.get_hand_ptn()
        fs["kinematic"] = self.get_kinematic()
        fs["fk_active"] = self.get_FK_active()
        fs["fk_set"] = self.export_fk_bone_info()
        fs["ik_active"] = self.get_IK_active()
        fs["ik_set"] = self.export_ik_target_info()
        fs["voice_lst"] = self.get_voice_lst()
        fs["voice_rpt"] = self.get_voice_repeat()

        # ext data, enable by ini setting
        if is_ini_value_true("ExportChara_BodyShapes"):
            fs["ext_bodyshapes"] = self.get_body_shapes_all()
        if is_ini_value_true("ExportChara_FaceShapes"):
            fs["ext_faceshapes"] = self.get_face_shapes_all()
        if is_ini_value_true("ExportChara_AnimeAuxParam"):
            fs["anim_optprm"] = self.get_anime_option_param()

        return fs

    def h_partner(self, hType=0, hPosition=0):
        # return partner sex for current h
        if hType != 9:
            if self.sex == 0:
                return (1,)
            else:
                return (0,)
        else:
            #print "hType = 9, hPosition =", hPosition
            if hPosition in range(0, 3):
                if self.sex == 0:
                    return (1, 0)
                else:
                    return (0, 0)
            elif hPosition in range(3, 7):
                if self.sex == 0:
                    return (1, 0, 0)
                else:
                    return (0, 0, 0)
            elif hPosition in range(7, 10):
                if self.sex == 0:
                    return (1, 0, 0, 0)
                else:
                    return (0, 0, 0, 0)
            else:
                if self.sex == 0:
                    return (1, 1)
                else:
                    return (0, 1)
        
    def h_with(self, partner, hType=0, hPosition=0, hStage=0, extActors=()):
        # partner: another actor as sex partner
        # hType: 1-11
        # hPosition:?
        # hStage:?
        # extActor = (Actor1, Actor2, Actor3) or None
        # sync with partner
        if self.pos != partner.pos or self.rot != partner.rot or self.scale != partner.scale:
            partner.move(pos=self.pos, rot=self.rot, scale=self.scale)
        if self.get_anime_speed() != partner.get_anime_speed():
            partner.set_anime_speed(self.get_anime_speed())
        if self.get_anime_pattern() != partner.get_anime_pattern():
            partner.set_anime_pattern(self.get_anime_pattern())
        if self.get_anime_forceloop() != partner.get_anime_forceloop():
            partner.set_anime_forceloop(self.get_anime_forceloop())
        for extActor in extActors:
            if extActor == None:
                continue
            #print "get ext actor " + extActor.text_name
            if self.pos != extActor.pos or self.rot != extActor.rot or self.scale != extActor.scale:
                extActor.move(pos=self.pos, rot=self.rot, scale=self.scale)
            if self.get_anime_speed() != extActor.get_anime_speed():
                extActor.set_anime_speed(self.get_anime_speed())
            if self.get_anime_pattern() != extActor.get_anime_pattern():
                extActor.set_anime_pattern(self.get_anime_pattern())
            if self.get_anime_forceloop() != extActor.get_anime_forceloop():
                extActor.set_anime_forceloop(self.get_anime_forceloop())
        # decide sex role
        if self.sex == 0:
            mactor = self
            factor = partner
        else:
            mactor = partner
            factor = self
        # show son if not
        if mactor.sex == 0 and not mactor.get_son():
            mactor.set_son(1)
        for extActor in extActors:
            if extActor != None and extActor.sex == 0 and not extActor.get_son():
                extActor.set_son(1)
        # load anime
        from Studio import Info
        info = Info.Instance
        gcDic = info.dicFAGroupCategory
        aDic = info.dicFemaleAnimeLoadInfo
        gp = range(1, 12)[hType]
        validCategoryKey = list(gcDic[gp].dicCategory.Keys)
        if not hPosition in range(len(validCategoryKey)):
            print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
            return
        cat = validCategoryKey[hPosition]
        validNoKey = list(aDic[gp][cat].Keys)
        if not hStage in range(len(validNoKey)):
            print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
            return
        no = validNoKey[hStage]
        #print "h with: (%d, %d, %d) => anime: (%d, %d, %d) = %s > %s > %s"%(hType, hPosition, hStage, gp, cat, no, gcDic[gp].name, gcDic[gp].dicCategory[cat], aDic[gp][cat][no].name)
        if gp != 10:
            #print "do %s > %s > %s"%(gcDic[gp].name, gcDic[gp].dicCategory[cat], aDic[gp][cat][no].name)
            #print "mactor.animate(%d, %d, %d)"%(gp, cat, no)
            #print "factor.animate(%d, %d, %d)"%(gp, cat, no)
            mactor.animate(gp, cat, no)
            factor.animate(gp, cat, no)
        else:
            if cat in (300, 303, 306):
                factor.animate(gp, cat, no)
                mactor.animate(gp, cat+1, no)
                if len(extActors) > 0 and extActors[0] != None:
                    extActors[0].animate(gp, cat+2, no)
            elif cat in (309, 313, 317, 321):
                factor.animate(gp, cat, no)
                mactor.animate(gp, cat+1, no)
                if len(extActors) > 0 and extActors[0] != None:
                    extActors[0].animate(gp, cat+2, no)
                if len(extActors) > 1 and extActors[1] != None:
                    extActors[1].animate(gp, cat+3, no)
            elif cat in (325, 330, 335):
                factor.animate(gp, cat, no)
                mactor.animate(gp, cat+1, no)
                if len(extActors) > 0 and extActors[0] != None:
                    extActors[0].animate(gp, cat+2, no)
                if len(extActors) > 1 and extActors[1] != None:
                    extActors[1].animate(gp, cat+3, no)
                if len(extActors) > 2 and extActors[2] != None:
                    extActors[2].animate(gp, cat+4, no)
            elif cat in (340, 343):
                factor.animate(gp, cat, no)
                mactor.animate(gp, cat+2, no)
                if len(extActors) > 0 and extActors[0] != None:
                    extActors[0].animate(gp, cat+1, no)
            elif cat in (341, 344):
                factor.animate(gp, cat, no)
                mactor.animate(gp, cat+1, no)
                if len(extActors) > 0 and extActors[0] != None:
                    extActors[0].animate(gp, cat-1, no)
            else:
                print "Unknown category", cat, "in group 10 (multi H)"
        # auto adjust anime param
        #print "factor(%s): height=%.2f breast=%.2f"%(factor.text_name, factor.height, factor.breast)
        anime_option_param = (factor.height, factor.breast)
        if mactor.isHAnime:
            mactor.set_anime_option_param(anime_option_param)
        for extActor in extActors:
            if extActor != None and extActor.isHAnime:
                extActor.set_anime_option_param(anime_option_param)

    def get_anime_info_text(self):
        info = "Anime Pattern: "
        from Studio import Info
        gcDic = Info.Instance.dicFAGroupCategory
        dic = Info.Instance.dicFemaleAnimeLoadInfo
        chAniInfo = self.objctrl.oiCharInfo.animeInfo
        info += "[%d]<color=#ff0000>%s</color>"%(chAniInfo.group, gcDic[chAniInfo.group].name)
        info += " >> "
        info += "[%d]<color=#ffff00>%s</color>"%(chAniInfo.category, gcDic[chAniInfo.group].dicCategory[chAniInfo.category])
        info += " >> "
        info += "[%d]<color=#00ff00>%s</color>"%(chAniInfo.no, dic[chAniInfo.group][chAniInfo.category][chAniInfo.no].name)

        cis = self.objctrl.charAnimeCtrl.animator.GetCurrentAnimatorClipInfo(0)
        clip = cis[0].clip
        info2 = "Anime Length: org = %.2f sec (%d frames)"%(clip.length, clip.length * clip.frameRate)
        spd = self.get_anime_speed()
        if spd > 0:
            info2 += ", cur = %.2f sec (@ %.2fx speed)"%(clip.length / spd, spd)

        return info, info2
            
    @staticmethod
    def get_hanime_group_names():
        from Studio import Info
        info = Info.Instance
        gcDic = info.dicFAGroupCategory
        return tuple(gcDic[i].name for i in range(1, 12))
        
    @staticmethod
    def get_hanime_category_names(group):
        from Studio import Info
        info = Info.Instance
        group = range(1, 12)[group]
        cDic = info.dicFAGroupCategory[group].dicCategory
        return tuple(cDic.Values)
    
    @staticmethod
    def get_hanime_no_names(group, category):
        from Studio import Info
        info = Info.Instance
        nDic = info.dicFemaleAnimeLoadInfo
        group = range(1, 12)[group]
        category = tuple(info.dicFAGroupCategory[group].dicCategory.Keys)[category]
        nName = []
        for n in nDic[group][category].Keys:
            nName.append(nDic[group][category][n].name)
        return tuple(nName)

class ActorCharaStudio(Actor):
    @property
    def sex(self):
        # get sex: 0-male, 1-female
        return self.objctrl.sex

    @property
    def height(self):
        # get height:
        return self.objctrl.oiCharInfo.charFile.custom.body.shapeValueBody[0]
        
    @height.setter
    def height(self, value):
        # set height
        self.set_body_shape(0, value)

    @property
    def breast(self):
        # get breast:
        return self.objctrl.oiCharInfo.charFile.custom.body.shapeValueBody[4]

    @breast.setter
    def breast(self, value):
        # set breast
        self.set_body_shape(4, value)

    def coordinate_type_int_to_enum(self, type):
        import ChaFileDefine
        if type == 0:
            type = ChaFileDefine.CoordinateType.School01
        elif type == 1:
            type = ChaFileDefine.CoordinateType.School02
        elif type == 2:
            type = ChaFileDefine.CoordinateType.Gym
        elif type == 3:
            type = ChaFileDefine.CoordinateType.Swim
        elif type == 4:
            type = ChaFileDefine.CoordinateType.Club
        elif type == 5:
            type = ChaFileDefine.CoordinateType.Plain
        else:
            type = ChaFileDefine.CoordinateType.Pajamas
        return type

    def set_coordinate_type(self, type):
        # type: 0-School01, 1-School02, 2-Gym, 3-Swim, 4-Club, 5-Plain, 6-Pajamas
        type = self.coordinate_type_int_to_enum(type)
        #print "Dont use it in console!"
        #print "self.objctrl.charInfo.ChangeCoordinateType(%s, True) is OK"%(str(type))
        #print "But self.objctrl.charInfo.Reload(0, 0, 0, 0) will clash the game"
        self.objctrl.charInfo.ChangeCoordinateTypeAndReload(type)
        
    def get_coordinate_type(self):
        # return coordinate type
        return self.objctrl.charInfo.fileStatus.coordinateType
    
    def set_shoes_type(self, type):
        # type: 0-indoor, 1-outdoor
        self.objctrl.SetShoesType(type)
        
    def get_shoes_type(self):
        # return shoes type
        return self.objctrl.charFileStatus.shoesType
    
    def set_cloth(self, clothIndex, clothState=None):
        # param format 1: set one cloth
        # clothIndex: 0-top, 1-bottom, 2-bra, 3-shorts, 4-grove!!, 5-panst!!, 6-sock, 7-shoes
        # clothState: 0-put on, 1-half off 1, 2-half off 2, 3-off 
        # param format 2: set all clothes, like the return value of get_cloth()
        # clothIndex: state for (top, bottom, bra, shorts, grove, panst, sock, shoes) in tuple
        # clothState: must be None
        # param format 3: set all cloth to same state
        # clothIndex: state of all clothes
        # clothState: must be None
        if clothState != None:
            self.objctrl.SetClothesState(clothIndex, clothState)
        elif isinstance(clothIndex, tuple):
            for i in range(len(clothIndex) if len(clothIndex) <= 8 else 8):
                self.objctrl.SetClothesState(i, clothIndex[i])
        else:
            self.objctrl.SetClothesStateAll(clothIndex)
    
    def get_cloth(self):
        # return state index of (top, bottom, bra, shorts, grove, panst, sock, shoes) in tuple
        # NOTE: self.objctrl.charFileStatus.clothesState return list[9] with 2 shoes
        return tuple(self.objctrl.charFileStatus.clothesState[:8])
        
    def set_accessory(self, accIndex, accShow=None):
        # param format 1: set one accessory
        # accIndex: 0~19
        # accShow: 0(hide)/1(visible)
        # param format 2: set all accessory, like the return value of get_accessory()
        # accIndex: 0/1 for each acessories in tuple(20)
        # accShow: must be None
        # param format 3: hide/show all accessory
        # accIndex: 0/1 for all
        # accShow: must be None
        if accShow != None:
            self.objctrl.ShowAccessory(accIndex, accShow)
        elif isinstance(accIndex, tuple):
            for i in range(len(accIndex) if len(accIndex) <= 20 else 20):
                self.objctrl.ShowAccessory(i, accIndex[i])
        else:
            for i in range(20):
                self.objctrl.ShowAccessory(i, accIndex)
        
    def get_accessory(self):
        # return accessory state on/off in tuple(20)
        return tuple(self.objctrl.charFileStatus.showAccessory)
        
    def set_juice(self, juices):
        # juices: level on (face, FrontUp, BackUp, FrontDown, BackDown) when 0-none, 1-few, 2-lots
        import ChaFileDefine
        self.objctrl.SetSiruFlags(ChaFileDefine.SiruParts.SiruKao, juices[0])
        self.objctrl.SetSiruFlags(ChaFileDefine.SiruParts.SiruFrontUp, juices[1])
        self.objctrl.SetSiruFlags(ChaFileDefine.SiruParts.SiruBackUp, juices[2])
        self.objctrl.SetSiruFlags(ChaFileDefine.SiruParts.SiruFrontDown, juices[3])
        self.objctrl.SetSiruFlags(ChaFileDefine.SiruParts.SiruBackDown, juices[4])
        
    def get_juice(self):
        # return juice level of (face, FrontUp, BackUp, FrontDown, BackDown) in tuple
        import ChaFileDefine
        jInfo = []
        jInfo.append(self.objctrl.GetSiruFlags(ChaFileDefine.SiruParts.SiruKao))
        jInfo.append(self.objctrl.GetSiruFlags(ChaFileDefine.SiruParts.SiruFrontUp))
        jInfo.append(self.objctrl.GetSiruFlags(ChaFileDefine.SiruParts.SiruBackUp))
        jInfo.append(self.objctrl.GetSiruFlags(ChaFileDefine.SiruParts.SiruFrontDown))
        jInfo.append(self.objctrl.GetSiruFlags(ChaFileDefine.SiruParts.SiruBackDown))
        return tuple(jInfo)

    def set_son(self, sonState):
        # sonState: (0(False)/1(True), length(0~3))
        self.objctrl.SetVisibleSon(bool(sonState[0]))
        self.objctrl.SetSonLength(sonState[1])
        
    def get_son(self):
        # return son (visible, length) in tuple
        sInfo = []
        sInfo.append(self.objctrl.oiCharInfo.visibleSon)
        sInfo.append(self.objctrl.oiCharInfo.sonLength)
        return tuple(sInfo)

    def get_simple_color(self):
        # return simple color
        simpleColor = self.objctrl.oiCharInfo.simpleColor
        return simpleColor

    def get_look_eye_ptn(self):
        # return eye look at pattern: 0: front, 1: camera, 2: hide from camera, 3: fix, 4: operate
        return self.objctrl.charInfo.GetLookEyesPtn()

    def get_look_neck(self):
        # return neck look pattern: 0: front, 1: camera, 2: hide from camera, 3: by anime, 4: fix
        return self.objctrl.charInfo.GetLookNeckPtn()

    def set_eyebrow_ptn(self, ptn):
        # ptn: 0 to 16
        self.objctrl.charInfo.ChangeEyebrowPtn(ptn)
        
    def get_eyebrow_ptn(self):
        # return eyebrow pattern
        return self.objctrl.charInfo.GetEyebrowPtn()

    def get_kkpedata(self):

        import extplugins
        if extplugins.ExtPlugin.exists("KKPE"):
            return extplugins.KKPE().GetCharaSettingsText(self.objctrl)

        return ""

    def set_kkpedata(self,kkpedata):
        #print "in kkpedata"
        if kkpedata != "":
            import extplugins
            if extplugins.ExtPlugin.exists("KKPE"):
                #print "import kkpedata"
                extplugins.KKPE().SetCharaSettingsText(self.objctrl,kkpedata)
                #print "import kkpedata2"

    def set_kinematic(self, mode, force = 0):
        # mode: 0-none, 1-IK, 2-FK, 3-IK&FK
        from Studio import OICharInfo, OIBoneInfo, FKCtrl
        if mode == 3:
            # enable IK
            self.objctrl.finalIK.enabled = True
            self.objctrl.oiCharInfo.enableIK = True
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.Body, self.objctrl.oiCharInfo.activeIK[0], True)
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.RightLeg, self.objctrl.oiCharInfo.activeIK[1], True)
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.LeftLeg, self.objctrl.oiCharInfo.activeIK[2], True)
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.RightArm, self.objctrl.oiCharInfo.activeIK[3], True)
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.LeftArm, self.objctrl.oiCharInfo.activeIK[4], True)
            # enable FK, disable "body" because it should be controlled by IK
            self.objctrl.oiCharInfo.activeFK[3] = False
            self.objctrl.fkCtrl.enabled = True
            self.objctrl.oiCharInfo.enableFK = True
            for i in range(len(FKCtrl.parts)):
                try:
                    self.objctrl.ActiveFK(FKCtrl.parts[i], self.objctrl.oiCharInfo.activeFK[i], True)
                except Exception as e:
                    print "Error set kinematic to 3(IK&FK), when ActiveFK[%d: %s]. Error message = %s, Exception type = %s"%(i, str(FKCtrl.parts[i]), str(e), str(type(e)))
            # call ActiveKinematicMode to set pvCopy?
            self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, True, False)
            """
            if not self.objctrl.oiCharInfo.enableIK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, 1, force)
                except Exception:
                    print "Error set kinematic to 3(IK&FK), when set IK"
            if not self.objctrl.oiCharInfo.enableFK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, 1, force)
                except Exception:
                    print "Error set kinematic to 3(IK&FK), when set FK"
            """
        elif mode == 2:
            if self.objctrl.oiCharInfo.enableIK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, False, force)
                except Exception:
                    print "Error set kinematic to 2(FK), when clear IK"
            if not self.objctrl.oiCharInfo.enableFK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, True, force)
                except Exception:
                    print "Error set kinematic to 2(FK), when set FK"
        elif mode == 1:
            if self.objctrl.oiCharInfo.enableFK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, False, force)
                except Exception:
                    print "Error set kinematic to 1(IK), when clear FK"
            if not self.objctrl.oiCharInfo.enableIK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, True, force)
                except Exception:
                    print "Error set kinematic to 1(IK), when set IK"
        else:
            if self.objctrl.oiCharInfo.enableIK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, False, force)
                except Exception:
                    print "Error set kinematic to 0(None), when clear IK"
            if self.objctrl.oiCharInfo.enableFK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, False, force)
                except Exception:
                    print "Error set kinematic to 0(None), when clear FK"
                
    def export_fk_bone_info(self, activedOnly = 1):
        # export a dic contents FK bone info
        biDic = {}
        for binfo in self.objctrl.listBones:
            if (not activedOnly) or binfo.active:
                #posClone = Vector3(binfo.posision.x, binfo.posision.y, binfo.posision.z)
                rot = binfo.boneInfo.changeAmount.rot
                rotClone = Vector3(rot.x if rot.x <= 180 else rot.x - 360, rot.y if rot.y <= 180 else rot.y - 360, rot.z if rot.z <= 180 else rot.z - 360)
                #abDic[binfo.boneID] = (posClone, rotClone)
                biDic[binfo.boneID] = rotClone
        #print "exported", len(biDic), "bones"
        return biDic
        
    def import_fk_bone_info(self, biDic):
        # import fk bone info from dic
        for binfo in self.objctrl.listBones:
            if binfo.boneID in biDic:
                if isinstance(biDic[binfo.boneID], Vector3):
                    binfo.boneInfo.changeAmount.rot = biDic[binfo.boneID]
                else:
                    binfo.boneInfo.changeAmount.rot = Vector3(biDic[binfo.boneID][0], biDic[binfo.boneID][1], biDic[binfo.boneID][2])
        
    def export_ik_target_info(self, activedOnly = 1):
        # export a dic contents IK target info
        itDic = {}
        for itInfo in self.objctrl.listIKTarget:
            if (not activedOnly) or itInfo.active:
                tgtName = itInfo.boneObject.name
                pos = itInfo.targetInfo.changeAmount.pos
                posClone = Vector3(pos.x, pos.y, pos.z)
                if "_hand_" in tgtName or "_leg03_" in tgtName:
                    rot = itInfo.targetInfo.changeAmount.rot
                    rotClone = Vector3(rot.x, rot.y, rot.z)
                    #rotClone = Vector3(rot.x if rot.x <= 180 else rot.x - 360, rot.y if rot.y <= 180 else rot.y - 360, rot.z if rot.z <= 180 else rot.z - 360)
                    itDic[tgtName]= (posClone, rotClone)
                else:
                    itDic[tgtName]= (posClone,)
        #print "exported", len(itDic), "IK Targets"
        return itDic
        
    def import_ik_target_info(self, itDic):
        # import IK target info from dic 
        for ikTgt in self.objctrl.listIKTarget:
            ikTgName = ikTgt.boneObject.name
            if ikTgName in itDic:
                if isinstance(itDic[ikTgName][0], Vector3):
                    ikTgt.targetInfo.changeAmount.pos = itDic[ikTgName][0]
                else:
                    ikTgt.targetInfo.changeAmount.pos = Vector3(itDic[ikTgName][0][0], itDic[ikTgName][0][1], itDic[ikTgName][0][2])
                if ("_hand_" in ikTgName or "_leg03_" in ikTgName) and len(itDic[ikTgName]) == 2:
                    if isinstance(itDic[ikTgName][1], Vector3):
                        ikTgt.targetInfo.changeAmount.rot = itDic[ikTgName][1]
                    else:
                        ikTgt.targetInfo.changeAmount.rot = Vector3(itDic[ikTgName][1][0], itDic[ikTgName][1][1], itDic[ikTgName][1][2])

    def get_look_neck_full2(self):
        # needed only to save Fixed state
        if self.get_look_neck() == 4:
            from System.IO import MemoryStream, BinaryWriter
            memoryStream = MemoryStream()
            binaryWriter = BinaryWriter(memoryStream)
            self.objctrl.neckLookCtrl.SaveNeckLookCtrl(binaryWriter)
            binaryWriter.Close()
            memoryStream.Close()
            return bytearray_to_str64(memoryStream.ToArray())
        else:
            return ''

    def set_look_neck_full2(self, str64):
        # needed only to set Fixed state
        if len(str64) > 0: # if non-fixed-state - move to it!
            self.set_look_neck(4)

        if self.get_look_neck() == 4:

            # print lst
            arrstate = str64_to_bytearray(str64)
            # print arrstate
            from System.IO import MemoryStream, BinaryWriter, BinaryReader
            binaryReader = BinaryReader(MemoryStream(arrstate))
            self.objctrl.neckLookCtrl.LoadNeckLookCtrl(binaryReader)

    def get_curcloth_coordinate(self):
        bytes = self.objctrl.charInfo.nowCoordinate.SaveBytes()
        return bytearray_to_str64(bytes)

    def set_curcloth_coordinate(self,str64):
        bytes = str64_to_bytearray(str64)
        import ChaFileDefine
        try:
            self.objctrl.charInfo.nowCoordinate.LoadBytes(bytes, ChaFileDefine.ChaFileCoordinateVersion)
            #self.objctrl.charInfo.Reload()
            #self.objctrl.charInfo.AssignCoordinate(ChaFileDefine.CoordinateType[self.objctrl.charInfo.fileStatus.coordinateType])
            self.objctrl.charInfo.AssignCoordinate(self.coordinate_type_int_to_enum(self.objctrl.charInfo.fileStatus.coordinateType))
            self.objctrl.charInfo.Reload(False,True,True,True)
        except Exception, e:
            print "Exception in set_curcloth_coordinate, %s" % ( str(e))

    def set_curcloth_coordinate_no_accessory(self,str64):
        bytes = str64_to_bytearray(str64)
        import ChaFileDefine
        import ChaFileAccessory
        import MessagePack.MessagePackSerializer as MessagePackSerializer
        try:
            nowCoord = self.objctrl.charInfo.nowCoordinate
            array2 = MessagePackSerializer.Serialize(nowCoord.accessory)
            nowCoord.LoadBytes(bytes, ChaFileDefine.ChaFileCoordinateVersion)
            #self.objctrl.charInfo.Reload()
            #self.objctrl.charInfo.AssignCoordinate(ChaFileDefine.CoordinateType[self.objctrl.charInfo.fileStatus.coordinateType])
            nowCoord.accessory = MessagePackSerializer.Deserialize[ChaFileAccessory](array2)
            self.objctrl.charInfo.AssignCoordinate(self.coordinate_type_int_to_enum(self.objctrl.charInfo.fileStatus.coordinateType))
            #self.objctrl.charInfo.AssignCoordinate(0)
            self.objctrl.charInfo.Reload(False,True,True,True)
        except Exception, e:
            print "Exception in set_curcloth_coordinate_no_accessory, %s" % ( str(e))

    def get_body_shape(self, p1):
        return self.charInfo.GetShapeBodyValue(p1)

    def set_body_shape(self, p1, p2):
        self.charInfo.SetShapeBodyValue(p1, p2)

    def get_body_shapes_all(self):
        return tuple(self.objctrl.oiCharInfo.charFile.custom.body.shapeValueBody)

    def get_body_shape_names(self):
        import ChaFileDefine
        return ChaFileDefine.cf_bodyshapename

    def get_body_shapes_count(self):
        return len(self.get_body_shapes_all())

    def get_face_shape(self, p1):
        return self.charInfo.GetShapeFaceValue(p1)

    def set_face_shape(self, p1, p2):
        self.charInfo.SetShapeFaceValue(p1, p2)

    def get_face_shapes_all(self):
        return tuple(self.objctrl.oiCharInfo.charFile.custom.face.shapeValueFace)

    def get_face_shape_names(self):
        import ChaFileDefine
        return ChaFileDefine.cf_headshapename

    def get_face_shapes_count(self):
        return len(self.get_face_shapes_all())

    def export_full_status(self):
        # export a dict contains all actor status
        fs = {}
        fs["visible"] = self.visible
        fs["move_to"] = self.pos
        fs["rotate_to"] = self.rot
        fs["scale_to"] = self.scale
        fs["anim"] = self.get_animate()
        fs["anim_spd"] = self.get_anime_speed()
        fs["anim_ptn"] = self.get_anime_pattern()
        fs["anim_lp"] = self.get_anime_forceloop()
        fs["cloth_type"] = self.get_coordinate_type()
        fs["cloth_all"] = self.get_cloth()
        fs["acc_all"] = self.get_accessory()
        if self.sex == 1:
            fs["juice"] = self.get_juice()
            fs["nip_stand"] = self.get_nipple_stand()
        else:
            fs["simple"] = self.get_simple()
            fs["simple_color"] = self.get_simple_color()
        fs["tear"] = self.get_tear()
        fs["face_red"] = self.get_facered()
        fs["son"] = self.get_son()
        fs["look_at_ptn"] = self.get_look_eye_ptn()
        fs["look_at_pos"] = self.get_look_eye_pos()
        fs["face_to"] = self.get_look_neck()
        #fs["face_to_full"] = self.get_look_neck_full()
        fs["face_to_full2"] = self.get_look_neck_full2()
        fs["eyebrow"] = self.get_eyebrow_ptn()
        fs["eyes"] = self.get_eyes_ptn()
        fs["eyes_open"] = self.get_eyes_open()
        fs["eyes_blink"] = self.get_eyes_blink()
        fs["mouth"] = self.get_mouth_ptn()
        fs["mouth_open"] = self.get_mouth_open()
        fs["lip_sync"] = self.get_lip_sync()
        fs["hands"] = self.get_hand_ptn()
        fs["kinematic"] = self.get_kinematic()
        fs["fk_active"] = self.get_FK_active()
        fs["fk_set"] = self.export_fk_bone_info()
        fs["ik_active"] = self.get_IK_active()
        fs["ik_set"] = self.export_ik_target_info()
        fs["voice_lst"] = self.get_voice_lst()
        fs["voice_rpt"] = self.get_voice_repeat()
        fs["shoes"] = self.get_shoes_type()

        # ext data, enable by ini setting
        if is_ini_value_true("ExportChara_CurClothesCoord"):
            fs["ext_curclothcoord"] = self.get_curcloth_coordinate()
        if is_ini_value_true("ExportChara_CurClothesCoordNoAcc"):
            fs["ext_curclothcoordnoacc"] = self.get_curcloth_coordinate()
        if is_ini_value_true("ExportChara_BodyShapes"):
            fs["ext_bodyshapes"] = self.get_body_shapes_all()
        if is_ini_value_true("ExportChara_FaceShapes"):
            fs["ext_faceshapes"] = self.get_face_shapes_all()
        if is_ini_value_true("ExportChara_AnimeAuxParam"):
            fs["anim_optprm"] = self.get_anime_option_param()

        import extplugins

        # plugin data, enable by ini setting
        try:
            if extplugins.ExtPlugin.exists("KKPE"):
                if is_ini_value_true("ExportChara_KKPE"):
                    fs["pl_kkpedata"] = self.get_kkpedata()
        except Exception, e:
            print "Error during get kkpedata"
            pass

        return fs

    def h_partner(self, hType=0, hPosition=0):
        # return tuple of valid partner for current actor
        # 0: male, 1: female, -1: both
        return (-1,)
    
    def h_with(self, partner, hType=0, hPosition=0, hStage=0, extActors=()):
        # partner: another actor as sex partner
        # hType: 0-serve, 1-insert, 2-yuri
        # hPosition:
        # hStage:
        # extActors: always (), no multi h in koikatu now
        # sync with partner
        if self.pos != partner.pos or self.rot != partner.rot or self.scale != partner.scale:
            partner.move(pos=self.pos, rot=self.rot, scale=self.scale)
        if self.get_anime_speed() != partner.get_anime_speed():
            partner.set_anime_speed(self.get_anime_speed())
        if self.get_anime_pattern() != partner.get_anime_pattern():
            partner.set_anime_pattern(self.get_anime_pattern())
        if self.get_anime_forceloop() != partner.get_anime_forceloop():
            partner.set_anime_forceloop(self.get_anime_forceloop())
        # decide sex role
        if self.sex == 0:
            mactor = self
            factor = partner
        else:
            mactor = partner
            factor = self
        # show son for male
        mss = mactor.get_son()
        if not mss[0] and mactor.sex == 0:
            mactor.set_son((True, mss[1]))
        # load anime
        from Studio import Info
        info = Info.Instance
        gcDic = info.dicAGroupCategory
        aDic = info.dicAnimeLoadInfo
        if hType == 0:
            # serve
            validCategoryKey = list(gcDic[3].dicCategory.Keys)
            if not hPosition in range(len(validCategoryKey)):
                print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
                return
            validNoKey = list(aDic[3][validCategoryKey[hPosition]].Keys)
            if not hStage in range(len(validNoKey)):
                print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
                return
            #print "a.animate(3, %d, %d)"%(validCategoryKey[hPosition], validNoKey[hStage])
            #print "b.animate(2, %d, %d)"%(validCategoryKey[hPosition], validNoKey[hStage])
            mactor.animate(3, validCategoryKey[hPosition], validNoKey[hStage])
            factor.animate(2, validCategoryKey[hPosition], validNoKey[hStage])
        elif hType == 1:
            # insert
            validCategoryKey = list(gcDic[5].dicCategory.Keys)
            if not hPosition in range(len(validCategoryKey)):
                print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
                return
            validNoKey = list(aDic[5][validCategoryKey[hPosition]].Keys)
            if not hStage in range(len(validNoKey)):
                print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
                return
            #print "a.animate(5, %d, %d)"%(validCategoryKey[hPosition], validNoKey[hStage])
            #print "b.animate(4, %d, %d)"%(validCategoryKey[hPosition], validNoKey[hStage])
            mactor.animate(5, validCategoryKey[hPosition], validNoKey[hStage])
            factor.animate(4, validCategoryKey[hPosition], validNoKey[hStage])
        else:
            # yuri
            validCategoryKey = [179, 181, 183]
            if not hPosition in range(len(validCategoryKey)):
                print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
                return
            validNoKey = list(aDic[9][validCategoryKey[hPosition]].Keys)
            if not hStage in range(len(validNoKey)):
                print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
                return
            #print "a.animate(9, %d, %d)"%(validCategoryKey[hPosition], validNoKey[hStage])
            #print "b.animate(9, %d, %d)"%(validCategoryKey[hPosition]+1, validNoKey[hStage])
            mactor.animate(9, validCategoryKey[hPosition], validNoKey[hStage])
            factor.animate(9, validCategoryKey[hPosition]+1, validNoKey[hStage])
        # auto adjust anime param
        print "factor(%s): height=%.2f breast=%.2f"%(factor.text_name, factor.height, factor.breast)
        anime_option_param = (factor.height, factor.breast)
        if factor.isHAnime:
            factor.set_anime_option_param(anime_option_param)
        if mactor.isHAnime:
            mactor.set_anime_option_param(anime_option_param)
        for extActor in extActors:
            if extActor != None and extActor.isHAnime:
                extActor.set_anime_option_param(anime_option_param)

    def get_anime_info_text(self):
        info = "Anime Pattern: "
        from Studio import Info
        gcDic = Info.Instance.dicAGroupCategory
        dic = Info.Instance.dicAnimeLoadInfo
        chAniInfo = self.objctrl.oiCharInfo.animeInfo
        info += "[%d]<color=#ff0000>%s</color>"%(chAniInfo.group, gcDic[chAniInfo.group].name)
        info += " >> "
        info += "[%d]<color=#ffff00>%s</color>"%(chAniInfo.category, gcDic[chAniInfo.group].dicCategory[chAniInfo.category])
        info += " >> "
        info += "[%d]<color=#00ff00>%s</color>"%(chAniInfo.no, dic[chAniInfo.group][chAniInfo.category][chAniInfo.no].name)

        cis = self.objctrl.charAnimeCtrl.animator.GetCurrentAnimatorClipInfo(0)
        clip = cis[0].clip
        info2 = "Anime Length: org = %.2f sec (%d frames)"%(clip.length, clip.length * clip.frameRate)
        spd = self.get_anime_speed()
        if spd > 0:
            info2 += ", cur = %.2f sec (@ %.2fx speed)"%(clip.length / spd, spd)

        return info, info2

    @staticmethod
    def get_hanime_group_names():
        from Studio import Info
        info = Info.Instance
        gcDic = info.dicAGroupCategory
        return (gcDic[3].name[1:], gcDic[5].name[1:], gcDic[9].name)
        
    @staticmethod
    def get_hanime_category_names(group):
        from Studio import Info
        info = Info.Instance
        group = (3, 5, 9)[group]
        cDic = info.dicAGroupCategory[group].dicCategory
        if group == 9:
            return (cDic[179][:-1], cDic[181][:-1], cDic[183][:-1])
        else:
            return tuple(cDic.Values)
    
    @staticmethod
    def get_hanime_no_names(group, category):
        from Studio import Info
        info = Info.Instance
        nDic = info.dicAnimeLoadInfo
        group = (3, 5, 9)[group]
        category = tuple(info.dicAGroupCategory[group].dicCategory.Keys)[category]
        nName = []
        for n in nDic[group][category].Keys:
            nName.append(nDic[group][category][n].name)
        return tuple(nName)

class ActorNeoV2(Actor):
    @property
    def sex(self):
        # get sex: 0-male, 1-female
        return self.objctrl.sex

    @property
    def height(self):
        # get height:
        return self.objctrl.oiCharInfo.charFile.custom.body.shapeValueBody[0]

    @height.setter
    def height(self, value):
        # set height
        self.set_body_shape(0, value)

    @property
    def breast(self):
        # get breast:
        return self.objctrl.oiCharInfo.charFile.custom.body.shapeValueBody[1]
        
    @breast.setter
    def breast(self, value):
        # set breast
        self.set_body_shape(1, value)

    def set_cloth(self, clothIndex, clothState=None):
        # param format 1: set one cloth
        # clothIndex: 0-top, 1-bottom, 2-bra, 3-shorts, 4-grove!!, 5-panst!!, 6-sock, 7-shoes
        # clothState: 0-put on, 1-half off 1, 2--off 
        # param format 2: set all clothes, like the return value of get_cloth()
        # clothIndex: state for (top, bottom, bra, shorts, grove, panst, sock, shoes) in tuple
        # clothState: must be None
        # param format 3: set all cloth to same state
        # clothIndex: state of all clothes
        # clothState: must be None
        if clothState != None:
            self.objctrl.SetClothesState(clothIndex, clothState)
        elif isinstance(clothIndex, tuple):
            for i in range(len(clothIndex) if len(clothIndex) <= 8 else 8):
                self.objctrl.SetClothesState(i, clothIndex[i])
        else:
            self.objctrl.SetClothesStateAll(clothIndex)
    
    def get_cloth(self):
        # return state index of (top, bottom, bra, shorts, grove, panst, sock, shoes) in tuple
        return tuple(self.objctrl.charFileStatus.clothesState)
        
    def set_accessory(self, accIndex, accShow=None):
        # param format 1: set one accessory
        # accIndex: 0~19
        # accShow: 0(hide)/1(visible)
        # param format 2: set all accessory, like the return value of get_accessory()
        # accIndex: 0/1 for each acessories in tuple(20)
        # accShow: must be None
        # param format 3: hide/show all accessory
        # accIndex: 0/1 for all
        # accShow: must be None
        if accShow != None:
            self.objctrl.ShowAccessory(accIndex, accShow)
        elif isinstance(accIndex, tuple):
            for i in range(len(accIndex) if len(accIndex) <= 20 else 20):
                self.objctrl.ShowAccessory(i, accIndex[i])
        else:
            for i in range(20):
                self.objctrl.ShowAccessory(i, accIndex)
        
    def get_accessory(self):
        # return accessory state on/off in tuple(20)
        return tuple(self.objctrl.charFileStatus.showAccessory)
        
    def set_juice(self, juices):
        # juices: level on (face, FrontUp, BackUp, FrontDown, BackDown) when 0-none, 1-few, 2-lots
        from AIChara.ChaFileDefine import SiruParts
        self.objctrl.SetSiruFlags(SiruParts.SiruKao, juices[0])
        self.objctrl.SetSiruFlags(SiruParts.SiruFrontTop, juices[1])
        self.objctrl.SetSiruFlags(SiruParts.SiruBackTop, juices[2])
        self.objctrl.SetSiruFlags(SiruParts.SiruFrontBot, juices[3])
        self.objctrl.SetSiruFlags(SiruParts.SiruBackBot, juices[4])
        
    def get_juice(self):
        # return juice level of (face, FrontUp, BackUp, FrontDown, BackDown) in tuple
        from AIChara.ChaFileDefine import SiruParts
        jInfo = []
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruKao))
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruFrontTop))
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruBackTop))
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruFrontBot))
        jInfo.append(self.objctrl.GetSiruFlags(SiruParts.SiruBackBot))
        return tuple(jInfo)

    def set_tear(self, level):
        # level: 0~1
        self.objctrl.SetTears(level)
    
    def get_tear(self):
        # return tear level
        return self.objctrl.GetTears()

    def set_tuya(self, level):
        # level: tuya 0~1
        self.objctrl.SetTuyaRate(level)
        
    def get_tuya(self):
        # return tuya rate
        return self.objctrl.oiCharInfo.SkinTuyaRate

    def set_wet(self, level):
        # level: wet 0~1
        self.objctrl.SetWetRate(level)
        
    def get_wet(self):
        # return wet rate
        return self.objctrl.oiCharInfo.WetRate

    def set_son(self, sonState):
        # sonState: (0(False)/1(True), length(0~3))
        self.objctrl.SetVisibleSon(bool(sonState[0]))
        self.objctrl.SetSonLength(sonState[1])
        
    def get_son(self):
        # return son (visible, length) in tuple
        sInfo = []
        sInfo.append(self.objctrl.oiCharInfo.visibleSon)
        sInfo.append(self.objctrl.oiCharInfo.sonLength)
        return tuple(sInfo)

    def set_simple(self, simpleState):
        # simple = one color, 1(true)/0(false)
        self.objctrl.SetVisibleSimple(bool(simpleState))
        
    def set_simple_color(self, simpleColor):
        # simple color
        self.objctrl.SetSimpleColor(tuple4_2_color(simpleColor))

    def get_simple_color(self):
        # return simple color
        simpleColor = self.objctrl.oiCharInfo.simpleColor
        return simpleColor

    def get_look_eye_ptn(self):
        # return eye look at pattern: 0: front, 1: camera, 2: hide from camera, 3: fix, 4: operate
        return self.objctrl.charInfo.GetLookEyesPtn()

    def set_look_neck(self, ptn):
        # ptn for CharaStudio: 0: front, 1: camera, 2: hide from camera, 3: by anime, string = 4: fix
        #if isinstance(ptn, str):
        #    self.set_look_neck_full2(ptn)
        #else:
            self.objctrl.ChangeLookNeckPtn(ptn)

    def get_look_neck(self):
        # return neck look pattern: 0: front, 1: camera, 2: hide from camera, 3: by anime, 4: fix neck full as a string
        ptn = self.objctrl.charInfo.GetLookNeckPtn()
        #if ptn == 4:
        #    return self.get_look_neck_full2()
        #else:
        #    return ptn
        return ptn

    def set_eyebrow_ptn(self, ptn):
        # ptn: 0 to 16
        self.objctrl.charInfo.ChangeEyebrowPtn(ptn)

    def get_eyebrow_ptn(self):
        # return eyebrow pattern
        return self.objctrl.charInfo.GetEyebrowPtn()

    def set_kinematic(self, mode, force=0):
        # mode: 0-none, 1-IK, 2-FK, 3-IK&FK
        from Studio import OICharInfo, OIBoneInfo, FKCtrl
        if mode == 3:
            # try plugin first
            try:
                from extplugins import AI_FKIK
                aifkik = AI_FKIK()
                aifkik.activateFKIK(self)
                if self.get_kinematic() != 3:
                    raise Exception("no response!?")
                return
            except Exception as e:
                print "Fail to set IK&FK by AI_FKIK plugin:", e

            # enable IK
            self.objctrl.finalIK.enabled = True
            self.objctrl.oiCharInfo.enableIK = True
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.Body, self.objctrl.oiCharInfo.activeIK[0], True)
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.RightLeg, self.objctrl.oiCharInfo.activeIK[1], True)
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.LeftLeg, self.objctrl.oiCharInfo.activeIK[2], True)
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.RightArm, self.objctrl.oiCharInfo.activeIK[3], True)
            self.objctrl.ActiveIK(OIBoneInfo.BoneGroup.LeftArm, self.objctrl.oiCharInfo.activeIK[4], True)
            # enable FK, disable "body" because it should be controlled by IK
            self.objctrl.oiCharInfo.activeFK[3] = False
            self.objctrl.fkCtrl.enabled = True
            self.objctrl.oiCharInfo.enableFK = True
            for i in range(len(FKCtrl.parts)):
                try:
                    self.objctrl.ActiveFK(FKCtrl.parts[i], self.objctrl.oiCharInfo.activeFK[i], True)
                except Exception as e:
                    print "Error set kinematic to 3(IK&FK), when ActiveFK[%d: %s]. Error message = %s, Exception type = %s" % (
                    i, str(FKCtrl.parts[i]), str(e), str(type(e)))
            # call ActiveKinematicMode to set pvCopy?
            self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, True, False)
        elif mode == 2:
            if self.objctrl.oiCharInfo.enableIK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, False, force)
                except Exception:
                    print "Error set kinematic to 2(FK), when clear IK"
            if not self.objctrl.oiCharInfo.enableFK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, True, force)
                except Exception:
                    print "Error set kinematic to 2(FK), when set FK"
        elif mode == 1:
            if self.objctrl.oiCharInfo.enableFK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, False, force)
                except Exception:
                    print "Error set kinematic to 1(IK), when clear FK"
            if not self.objctrl.oiCharInfo.enableIK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, True, force)
                except Exception:
                    print "Error set kinematic to 1(IK), when set IK"
        else:
            if self.objctrl.oiCharInfo.enableIK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.IK, False, force)
                except Exception:
                    print "Error set kinematic to 0(None), when clear IK"
            if self.objctrl.oiCharInfo.enableFK:
                try:
                    self.objctrl.ActiveKinematicMode(OICharInfo.KinematicMode.FK, False, force)
                except Exception:
                    print "Error set kinematic to 0(None), when clear FK"

    def export_fk_bone_info(self, activedOnly=1):
        # export a dic contents FK bone info
        biDic = {}
        for binfo in self.objctrl.listBones:
            if (not activedOnly) or binfo.active:
                # posClone = Vector3(binfo.posision.x, binfo.posision.y, binfo.posision.z)
                rot = binfo.boneInfo.changeAmount.rot
                rotClone = Vector3(rot.x if rot.x <= 180 else rot.x - 360, rot.y if rot.y <= 180 else rot.y - 360,
                                   rot.z if rot.z <= 180 else rot.z - 360)
                # abDic[binfo.boneID] = (posClone, rotClone)
                biDic[binfo.boneID] = rotClone
        # print "exported", len(biDic), "bones"
        return biDic

    def import_fk_bone_info(self, biDic):
        # import fk bone info from dic
        for binfo in self.objctrl.listBones:
            if binfo.boneID in biDic:
                if isinstance(biDic[binfo.boneID], Vector3):
                    binfo.boneInfo.changeAmount.rot = biDic[binfo.boneID]
                else:
                    binfo.boneInfo.changeAmount.rot = Vector3(biDic[binfo.boneID][0], biDic[binfo.boneID][1],
                                                              biDic[binfo.boneID][2])

    def export_ik_target_info(self, activedOnly=1):
        # export a dic contents IK target info
        itDic = {}
        for itInfo in self.objctrl.listIKTarget:
            if (not activedOnly) or itInfo.active:
                tgtName = itInfo.boneObject.name
                pos = itInfo.targetInfo.changeAmount.pos
                posClone = Vector3(pos.x, pos.y, pos.z)
                if "_Hand_" in tgtName or "_Foot01_" in tgtName:
                    rot = itInfo.targetInfo.changeAmount.rot
                    rotClone = Vector3(rot.x, rot.y, rot.z)
                    # rotClone = Vector3(rot.x if rot.x <= 180 else rot.x - 360, rot.y if rot.y <= 180 else rot.y - 360, rot.z if rot.z <= 180 else rot.z - 360)
                    itDic[tgtName] = (posClone, rotClone)
                else:
                    itDic[tgtName] = (posClone,)
        # print "exported", len(itDic), "IK Targets"
        return itDic

    def import_ik_target_info(self, itDic):
        # import IK target info from dic
        for ikTgt in self.objctrl.listIKTarget:
            ikTgName = ikTgt.boneObject.name
            if ikTgName in itDic:
                if isinstance(itDic[ikTgName][0], Vector3):
                    ikTgt.targetInfo.changeAmount.pos = itDic[ikTgName][0]
                else:
                    ikTgt.targetInfo.changeAmount.pos = Vector3(itDic[ikTgName][0][0], itDic[ikTgName][0][1], itDic[ikTgName][0][2])
                if ("_Hand_" in ikTgName or "_Foot01_" in ikTgName) and len(itDic[ikTgName]) == 2:
                    if isinstance(itDic[ikTgName][1], Vector3):
                        ikTgt.targetInfo.changeAmount.rot = itDic[ikTgName][1]
                    else:
                        ikTgt.targetInfo.changeAmount.rot = Vector3(itDic[ikTgName][1][0], itDic[ikTgName][1][1],
                                                                    itDic[ikTgName][1][2])

    def get_look_neck_full2(self):
        # needed only to save Fixed state
        if self.get_look_neck() == 4:
            from System.IO import MemoryStream, BinaryWriter
            memoryStream = MemoryStream()
            binaryWriter = BinaryWriter(memoryStream)
            self.objctrl.neckLookCtrl.SaveNeckLookCtrl(binaryWriter)
            binaryWriter.Close()
            memoryStream.Close()
            return bytearray_to_str64(memoryStream.ToArray())
        else:
            return ''

    def set_look_neck_full2(self, str64):
        # needed only to set Fixed state
        if len(str64) > 0:  # if non-fixed-state - move to it!
            self.set_look_neck(4)

        if self.get_look_neck() == 4:
            # print lst
            arrstate = str64_to_bytearray(str64)
            # print arrstate
            from System.IO import MemoryStream, BinaryWriter, BinaryReader
            binaryReader = BinaryReader(MemoryStream(arrstate))
            self.objctrl.neckLookCtrl.LoadNeckLookCtrl(binaryReader)

    def get_curcloth_coordinate(self):
        bytes = self.objctrl.charInfo.nowCoordinate.SaveBytes()
        return bytearray_to_str64(bytes)

    def set_curcloth_coordinate(self, str64):
        bytes = str64_to_bytearray(str64)
        from AIChara import ChaFileDefine 
        try:
            self.objctrl.charInfo.nowCoordinate.LoadBytes(bytes, ChaFileDefine.ChaFileCoordinateVersion)
            self.objctrl.charInfo.Reload()
        except Exception, e:
            print "Exception in set_curcloth_coordinate, %s" % (str(e))

    def get_body_shape(self, p1):
        return self.charInfo.GetShapeBodyValue(p1)

    def set_body_shape(self, p1, p2):
        self.charInfo.SetShapeBodyValue(p1, p2)

    def get_body_shapes_all(self):
        return tuple(self.objctrl.oiCharInfo.charFile.custom.body.shapeValueBody)

    def get_body_shape_names(self):
        from AIChara import ChaFileDefine
        return ChaFileDefine.cf_bodyshapename

    def get_body_shapes_count(self):
        return len(self.get_body_shapes_all())

    def get_face_shape(self, p1):
        return self.charInfo.GetShapeFaceValue(p1)

    def set_face_shape(self, p1, p2):
        self.charInfo.SetShapeFaceValue(p1, p2)

    def get_face_shapes_all(self):
        return tuple(self.objctrl.oiCharInfo.charFile.custom.face.shapeValueFace)

    def get_face_shape_names(self):
        from AIChara import ChaFileDefine
        return ChaFileDefine.cf_headshapename

    def get_face_shapes_count(self):
        return len(self.get_face_shapes_all())

    def get_aipedata(self):
        import extplugins
        if plugin_aipe.isDetected:
            return plugin_aipe.GetCharaSettingsText(self.objctrl)
        else:
            return ""

    def set_aipedata(self, aipedata):
        if aipedata != "":
            import extplugins
            if plugin_aipe.isDetected:
                plugin_aipe.SetCharaSettingsText(self.objctrl, aipedata)




    def export_full_status(self):
        # export a dict contains all actor status
        fs = {}
        fs["visible"] = self.visible
        fs["move_to"] = self.pos
        fs["rotate_to"] = self.rot
        fs["scale_to"] = self.scale
        fs["anim"] = self.get_animate()
        fs["anim_spd"] = self.get_anime_speed()
        fs["anim_ptn"] = self.get_anime_pattern()
        fs["anim_lp"] = self.get_anime_forceloop()
        fs["cloth_all"] = self.get_cloth()
        fs["acc_all"] = self.get_accessory()
        if self.sex == 1:
            fs["juice"] = self.get_juice()
            fs["nip_stand"] = self.get_nipple_stand()
        fs["tear"] = self.get_tear()
        fs["face_red"] = self.get_facered()
        fs["skin_tuya"] = self.get_tuya()
        fs["skin_wet"] = self.get_wet()
        fs["simple"] = self.get_simple()
        fs["simple_color"] = self.get_simple_color()
        fs["son"] = self.get_son()
        fs["look_at"] = self.get_look_eye()
        fs["face_to"] = self.get_look_neck()
        fs["eyebrow"] = self.get_eyebrow_ptn()
        fs["eyes"] = self.get_eyes_ptn()
        fs["eyes_open"] = self.get_eyes_open()
        fs["eyes_blink"] = self.get_eyes_blink()
        fs["mouth"] = self.get_mouth_ptn()
        fs["mouth_open"] = self.get_mouth_open()
        fs["lip_sync"] = self.get_lip_sync()
        fs["hands"] = self.get_hand_ptn()
        fs["kinematic"] = self.get_kinematic()
        fs["fk_active"] = self.get_FK_active()
        fs["fk_set"] = self.export_fk_bone_info()
        fs["ik_active"] = self.get_IK_active()
        fs["ik_set"] = self.export_ik_target_info()
        fs["voice_lst"] = self.get_voice_lst()
        fs["voice_rpt"] = self.get_voice_repeat()

        # ext data, enable by ini setting
        if is_ini_value_true("ExportChara_CurClothesCoord"):
            fs["ext_curclothcoord"] = self.get_curcloth_coordinate()
        if is_ini_value_true("ExportChara_BodyShapes"):
            fs["ext_bodyshapes"] = self.get_body_shapes_all()
        if is_ini_value_true("ExportChara_FaceShapes"):
            fs["ext_faceshapes"] = self.get_face_shapes_all()
        if is_ini_value_true("ExportChara_AnimeAuxParam"):
            fs["anim_optprm"] = self.get_anime_option_param()

        # plugin data, enable by ini setting
        if is_ini_value_true("ExportChara_AIPE"):
            try:
                import extplugins
                if plugin_aipe.isDetected:
                    fs["pl_aipedata"] = self.get_aipedata()
            except Exception, e:
                print "Error during get aipedata"
                pass

        return fs

    def h_partner(self, hType=0, hPosition=0):
        # return tuple of valid partner for current actor
        # 0: male, 1: female, -1: both
        return (-1,)
    
    def h_with(self, partner, hType=0, hPosition=0, hStage=0, extActors=()):
        # partner: another actor as sex partner
        # hType: 0-touth, 1-serve, 2-insert, 3-special, 4-yuri
        # hPosition:
        # hStage:
        # extActors: 
        # sync with partner
        if self.pos != partner.pos or self.rot != partner.rot or self.scale != partner.scale:
            partner.move(pos=self.pos, rot=self.rot, scale=self.scale)
        if self.get_anime_speed() != partner.get_anime_speed():
            partner.set_anime_speed(self.get_anime_speed())
        if self.get_anime_pattern() != partner.get_anime_pattern():
            partner.set_anime_pattern(self.get_anime_pattern())
        if self.get_anime_forceloop() != partner.get_anime_forceloop():
            partner.set_anime_forceloop(self.get_anime_forceloop())
        # decide sex role
        if self.sex == 0:
            mactor = self
            factor = partner
        else:
            mactor = partner
            factor = self
        # show son for male
        mss = mactor.get_son()
        if not mss[0] and mactor.sex == 0:
            mactor.set_son((True, mss[1]))
        # load anime
        from Studio import Info
        info = Info.Instance
        gcDic = info.dicAGroupCategory
        aDic = info.dicAnimeLoadInfo
        if hType == 0:
            # touch
            validCategoryKey = list(gcDic[1].dicCategory.Keys)
            if not hPosition in range(len(validCategoryKey)):
                print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
                return
            validNoKey = list(aDic[1][validCategoryKey[hPosition]].Keys)
            if not hStage in range(len(validNoKey)):
                print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
                return
            print "%s anime(%d, %d, %d)"%(mactor.text_name, 2, validCategoryKey[hPosition], validNoKey[hStage])
            print "%s anime(%d, %d, %d)"%(factor.text_name, 1, validCategoryKey[hPosition], validNoKey[hStage])
            mactor.animate(2, validCategoryKey[hPosition], validNoKey[hStage])
            factor.animate(1, validCategoryKey[hPosition], validNoKey[hStage])
        elif hType == 1:
            # serve
            validCategoryKey = list(gcDic[3].dicCategory.Keys)
            if not hPosition in range(len(validCategoryKey)):
                print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
                return
            validNoKey = list(aDic[3][validCategoryKey[hPosition]].Keys)
            if not hStage in range(len(validNoKey)):
                print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
                return
            mactor.animate(4, validCategoryKey[hPosition], validNoKey[hStage])
            factor.animate(3, validCategoryKey[hPosition], validNoKey[hStage])
        elif hType == 2:
            # insert
            validCategoryKey = list(gcDic[5].dicCategory.Keys)
            if not hPosition in range(len(validCategoryKey)):
                print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
                return
            validNoKey = list(aDic[5][validCategoryKey[hPosition]].Keys)
            if not hStage in range(len(validNoKey)):
                print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
                return
            mactor.animate(6, validCategoryKey[hPosition], validNoKey[hStage])
            factor.animate(5, validCategoryKey[hPosition], validNoKey[hStage])
        elif hType == 3:
            # insert
            validCategoryKey = list(gcDic[7].dicCategory.Keys)
            if not hPosition in range(len(validCategoryKey)):
                print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
                return
            validNoKey = list(aDic[7][validCategoryKey[hPosition]].Keys)
            if not hStage in range(len(validNoKey)):
                print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
                return
            mactor.animate(8, validCategoryKey[hPosition], validNoKey[hStage])
            factor.animate(7, validCategoryKey[hPosition], validNoKey[hStage])
        else:
            # yuri
            validCategoryKey = [215, 217, 219, 221, 223]
            if not hPosition in range(len(validCategoryKey)):
                print "invalid hPosition %d, must be 0~%d"%(hPosition, len(validCategoryKey)-1)
                return
            validNoKey = list(aDic[9][validCategoryKey[hPosition]].Keys)
            if not hStage in range(len(validNoKey)):
                print "invalid hStage %d, must be 0~%d"%(hStage, len(validNoKey)-1)
                return
            mactor.animate(9, validCategoryKey[hPosition], validNoKey[hStage])
            factor.animate(9, validCategoryKey[hPosition]+1, validNoKey[hStage])
        # auto adjust anime param
        print "factor(%s): height=%.2f breast=%.2f"%(factor.text_name, factor.height, factor.breast)
        anime_option_param = (factor.height, factor.breast)
        if factor.isHAnime:
            factor.set_anime_option_param(anime_option_param)
        if mactor.isHAnime:
            mactor.set_anime_option_param(anime_option_param)
        for extActor in extActors:
            if extActor != None and extActor.isHAnime:
                extActor.set_anime_option_param(anime_option_param)

    def get_anime_info_text(self):
        info = "Anime Pattern: "
        from Studio import Info
        gcDic = Info.Instance.dicAGroupCategory
        dic = Info.Instance.dicAnimeLoadInfo
        chAniInfo = self.objctrl.oiCharInfo.animeInfo
        info += "[%d]<color=#ff0000>%s</color>"%(chAniInfo.group, gcDic[chAniInfo.group].name)
        info += " >> "
        info += "[%d]<color=#ffff00>%s</color>"%(chAniInfo.category, gcDic[chAniInfo.group].dicCategory[chAniInfo.category].name)
        info += " >> "
        info += "[%d]<color=#00ff00>%s</color>"%(chAniInfo.no, dic[chAniInfo.group][chAniInfo.category][chAniInfo.no].name)

        cis = self.objctrl.charAnimeCtrl.animator.GetCurrentAnimatorClipInfo(0)
        clip = cis[0].clip
        info2 = "Anime Length: org = %.2f sec (%d frames)"%(clip.length, clip.length * clip.frameRate)
        spd = self.get_anime_speed()
        if spd > 0:
            info2 += ", cur = %.2f sec (@ %.2fx speed)"%(clip.length / spd, spd)

        return info, info2

    @staticmethod
    def get_hanime_group_names():
        from Studio import Info
        info = Info.Instance
        gcDic = info.dicAGroupCategory
        return (gcDic[1].name[1:], gcDic[3].name[1:], gcDic[5].name[1:], gcDic[7].name[1:], gcDic[9].name)
        
    @staticmethod
    def get_hanime_category_names(group):
        from Studio import Info
        info = Info.Instance
        group = (1, 3, 5, 7, 9)[group]
        cDic = info.dicAGroupCategory[group].dicCategory
        if group == 9:
            return (cDic[215].name[:-1], cDic[217].name[:-1], cDic[219].name[:-1], cDic[221].name[:-1], cDic[223].name[:-1])
        else:
            return tuple([v.name for v in cDic.Values])
    
    @staticmethod
    def get_hanime_no_names(group, category):
        from Studio import Info
        info = Info.Instance
        nDic = info.dicAnimeLoadInfo
        group = (1, 3, 5, 7, 9)[group]
        category = tuple(info.dicAGroupCategory[group].dicCategory.Keys)[category]
        nName = []
        for n in nDic[group][category].Keys:
            nName.append(nDic[group][category][n].name)
        return tuple(nName)

#===============================================================================================
class Prop(HSNeoOCI):
    @property
    def visible(self):
        # get visible status
        return self.objctrl.treeNodeObject.visible
        
    @visible.setter
    def visible(self, value):
        # value: 0(hide)/1(visible)
        self.objctrl.treeNodeObject.visible = value
        
    @property
    def name(self):
        return self.objctrl.treeNodeObject.textName
    
    @property
    def isFolder(self):
        from Studio import OCIFolder
        return isinstance(self.objctrl, OCIFolder)
        
    @property
    def isItem(self):
        from Studio import OCIItem
        return isinstance(self.objctrl, OCIItem)
        
    @property
    def isLight(self):
        from Studio import OCILight
        return isinstance(self.objctrl, OCILight)
    
    @property
    def isColorable(self):
        if self.isItem:
            return self.objctrl.isChangeColor
        else:
            return False
            
    @property
    def isAnime(self):
        if self.isItem:
            return self.objctrl.isAnime
        else:
            return False
            
    @property
    def isFK(self):
        if self.isItem:
            return self.objctrl.isFK
        else:
            return False
        
    @property
    def pos(self):
        return self.objctrl.objectInfo.changeAmount.pos
        
    @property
    def rot(self):
        return self.objctrl.objectInfo.changeAmount.rot
   
    @property
    def scale(self):
        return self.objctrl.objectInfo.changeAmount.scale
    
    def move(self, pos=None, rot=None, scale=None):
        if pos:
            if isinstance(pos, tuple) and len(pos) == 3:
                pos = Vector3(pos[0], pos[1], pos[2])
            self.objctrl.objectInfo.changeAmount.pos = pos
            
        if rot:
            if isinstance(rot, tuple) and len(rot) == 3:
                rot = Vector3(rot[0], rot[1], rot[2])
            self.objctrl.objectInfo.changeAmount.rot = rot
            
        if scale and self.isItem: 
            if isinstance(scale, tuple) and len(scale) == 3:
                scale = Vector3(scale[0], scale[1], scale[2])
            self.objctrl.objectInfo.changeAmount.scale = scale
    
    def set_anime_speed(self, speed):
        # speed: 0~1
        self.objctrl.animeSpeed = speed

    def get_anime_speed(self):
        # return anime speed
        return self.objctrl.animeSpeed
        
    def set_color(self, color):
        # color : a tuple of ((UnityEngine.Color, Color, Intensity, Sharpness), (UnityEngine.Color, Color, Intensity, Sharpness))
        # color (light): UnityEngine.Color (r,g,b,a)
        if self.isColorable:
            self.objctrl.SetColor(tuple4_2_color(color[0][0]))
            self.objctrl.SetGloss(tuple4_2_color(color[0][1]))
            self.objctrl.SetIntensity(color[0][2])
            self.objctrl.SetSharpness(color[0][3])
            if self.objctrl.isColor2 and len(color) > 1:
                self.objctrl.SetColor2(tuple4_2_color(color[1][0]))
                self.objctrl.SetGloss2(tuple4_2_color(color[1][1]))
                self.objctrl.SetSharpness2(color[1][3])
            self.objctrl.UpdateColor()
        elif self.isLight:
            self.objctrl.SetColor(tuple4_2_color(color))

    def get_color(self):
        # return a tuple of used color
        if self.isColorable:
            cl = [(self.objctrl.itemInfo.color.rgbaDiffuse, self.objctrl.itemInfo.color.rgbSpecular, self.objctrl.itemInfo.color.specularIntensity, self.objctrl.itemInfo.color.specularSharpness)]
            if self.objctrl.isColor2:
                cl.append((self.objctrl.itemInfo.color2.rgbaDiffuse, self.objctrl.itemInfo.color2.rgbSpecular, self.objctrl.itemInfo.color2.specularIntensity, self.objctrl.itemInfo.color2.specularSharpness))
            return tuple(cl)
        elif self.isLight:
            return self.objctrl.lightInfo.color
            
    def export_fk_bone_info(self):
        # return a tuple of FK bone rot
        if self.isFK:
            boneinfo = []
            for bi in self.objctrl.listBones:
                rot = bi.boneInfo.changeAmount.rot
                rotClone = Vector3(rot.x if rot.x <= 180 else rot.x - 360, rot.y if rot.y <= 180 else rot.y - 360, rot.z if rot.z <= 180 else rot.z - 360)
                boneinfo.append(rotClone)
            return tuple(boneinfo)
        else:
            return ()

    def import_fk_bone_info(self, biList):
        # import fk bone info from dic
        if self.isFK:
            for i in range(len(self.objctrl.listBones)):
                binfo = self.objctrl.listBones[i]
                if i < len(biList):
                    if biList[i] is Vector3:
                        binfo.boneInfo.changeAmount.rot = biList[i]
                    else:
                        binfo.boneInfo.changeAmount.rot = Vector3(biList[i][0], biList[i][1], biList[i][2])

    def import_status(self, status):
        for f in status:
            if f in prop_act_funcs:
                prop_act_funcs[f][0](self, status[f])
            else:
                print "act error: unknown function '%s' for prop" % (f)

    def import_status_diff_optimized(self, status):
        ofs = self.export_full_status()
        dfs = {}
        for key in status.Keys:
            if not key in ofs.Keys or ofs[key] != status[key]:
                dfs[key] = status[key]
        #return dfs
        #print "Optimized import status diff, ", dfs
        self.import_status(dfs)                                                   
 
    def export_full_status(self):
        # export full status of prop for different engines
        raise Exception("Prop.export_full_status is not implemented")
    
    # Light properties/methods
    @property
    def type(self):
        if self.isLight:
            return self.objctrl.lightType
    
    @property
    def no(self):
        if self.isLight:
            return self.objctrl.lightInfo.no
    
    @property
    def enable(self):
        if self.isLight:
            return self.objctrl.lightInfo.enable
    
    def set_enable(self, is_enabled):
        if self.isLight:
            self.objctrl.SetEnable(is_enabled)
    
    @property
    def get_intensity(self):
        if self.isLight:
            return self.objctrl.lightInfo.intensity
        
    def set_intensity(self, intensity):
        if self.isLight:
            self.objctrl.SetIntensity(intensity)
    
    @property
    def get_shadow(self):
        if self.isLight:
            return self.objctrl.lightInfo.shadow
    
    def set_shadow(self, has_shadow):
        if self.isLight:
            self.objctrl.SetShadow(has_shadow)

    @property
    def hasRange(self):
        if self.isLight:# and not self.type == "Directional":
            return True
    
    @property    
    def hasAngle(self):
        if self.isLight:# and self.type == "Spot":
            return True
    
    def get_angle(self): 
        if self.hasAngle:
            return self.objctrl.lightInfo.spotAngle      
        
    def set_angle(self, angle):
        if self.hasAngle:
            self.objctrl.SetSpotAngle(angle)
            
    def get_range(self):
        if self.hasRange:
            return self.objctrl.lightInfo.range
        
    def set_range(self, range):
        if self.hasRange:
            self.objctrl.SetRange(range)

class PropHSNeo(Prop):
    def export_full_status(self):
        # export full status of prop
        fs = {}
        fs["visible"] = self.visible
        fs["move_to"] = self.pos
        fs["rotate_to"] = self.rot
        if self.isItem:
            fs["scale_to"] = self.scale
        if self.isAnime:
            fs["anim_spd"] = self.get_anime_speed()
        if self.isColorable or self.isLight:
            fs["color"] = self.get_color()
        if self.isFK:
            fs["fk_set"] = self.export_fk_bone_info()
        if self.isLight:
            fs["enable"] = self.enable
            fs["intensity"] = self.get_intensity
            fs["shadow"] = self.get_shadow
            if self.hasRange:
                fs["range"] = self.get_range()
            if self.hasAngle:
                fs["angle"] = self.get_angle()

        return fs

class PropPHStudio(Prop):
    def export_full_status(self):
        # export full status of prop
        fs = {}
        fs["visible"] = self.visible
        fs["move_to"] = self.pos
        fs["rotate_to"] = self.rot
        if self.isItem:
            fs["scale_to"] = self.scale
        if self.isAnime:
            fs["anim_spd"] = self.get_anime_speed()
        if self.isColorable or self.isLight:
            fs["color"] = self.get_color()
        if self.isFK:
            fs["fk_set"] = self.export_fk_bone_info()
        if self.isLight:
            fs["enable"] = self.enable
            fs["intensity"] = self.get_intensity
            fs["shadow"] = self.get_shadow
            if self.hasRange:
                fs["range"] = self.get_range()
            if self.hasAngle:
                fs["angle"] = self.get_angle()
        return fs

class PropCharaStudio(Prop):
    def set_color(self, color):
        # color : a tuple of UnityEngine.Color
        if self.isColorable:
            if not isinstance(color, tuple):
                color = (color, None, None, None)
            i = 0
            if self.objctrl.useColor[0] and i < len(color) and color[i] != None:
                self.objctrl.itemInfo.color[0] = tuple4_2_color(color[i])
            i = 1
            if self.objctrl.useColor[1] and i < len(color) and color[i] != None:
                self.objctrl.itemInfo.color[1] = tuple4_2_color(color[i])
            i = 2
            if self.objctrl.useColor[2] and i < len(color) and color[i] != None:
                self.objctrl.itemInfo.color[2] = tuple4_2_color(color[i])
            i = 3
            if self.objctrl.useColor4 and i < len(color) and color[i] != None:
                self.objctrl.itemInfo.color[7] = tuple4_2_color(color[i])
            self.objctrl.UpdateColor()
        elif self.isLight:
            c = tuple4_2_color(color)
            self.objctrl.SetColor(c)

    def get_color(self):
        # return a tuple of used color
        if self.isColorable:
            cl = []
            if self.objctrl.useColor[0]:
                cl.append(self.objctrl.itemInfo.color[0])
            else:
                cl.append(None)
            if self.objctrl.useColor[1]:
                cl.append(self.objctrl.itemInfo.color[1])
            else:
                cl.append(None)
            if self.objctrl.useColor[2]:
                cl.append(self.objctrl.itemInfo.color[2])
            else:
                cl.append(None)
            if self.objctrl.useColor4:
                cl.append(self.objctrl.itemInfo.color[7])
            else:
                cl.append(None)
            return tuple(cl)
        elif self.isLight:
            return self.objctrl.lightInfo.color

    @property
    def hasPattern(self):
        if not self.isItem:
            return False
        for n in self.objctrl.usePattern:
            if n:
                return True
            return False

    def set_pattern(self, param):
        # param: a set of ((key, filepath, clamp), (key, filepath, clamp), (key, filepath, clamp))
        if self.hasPattern:
            for i in range(len(self.objctrl.usePattern)):
                if self.objctrl.usePattern[i] and param[i] != None:
                    self.objctrl.itemInfo.pattern[i].key = param[i][0]
                    self.objctrl.itemInfo.pattern[i].filePath = param[i][1]
                    self.objctrl.itemInfo.pattern[i].clamp = param[i][2]
            self.objctrl.SetupPatternTex()
            self.objctrl.UpdateColor()

    def get_pattern(self):
        if self.hasPattern:
            pt = []
            for i in range(len(self.objctrl.usePattern)):
                if self.objctrl.usePattern[i]:
                    pi = self.objctrl.itemInfo.pattern[i]
                    pt.append((pi.key, pi.filePath, pi.clamp))
                else:
                    pt.append(None)
            return tuple(pt)

    def set_pattern_detail(self, param):
        # param: a set of ((color, ut, vt, us, vs, rot), (color, ut, vt, us, vs, rot), (color, ut, vt, us, vs, rot))
        if self.hasPattern:
            for i in range(len(self.objctrl.usePattern)):
                if self.objctrl.usePattern[i] and param[i] != None:
                    self.objctrl.itemInfo.color[i+3] = tuple4_2_color(param[i][0])
                    self.objctrl.itemInfo.pattern[i].ut = param[i][1]
                    self.objctrl.itemInfo.pattern[i].vt = param[i][2]
                    self.objctrl.itemInfo.pattern[i].us = param[i][3]
                    self.objctrl.itemInfo.pattern[i].vs = param[i][4]
                    self.objctrl.itemInfo.pattern[i].rot = param[i][5]
            self.objctrl.UpdateColor()

    def get_pattern_detail(self):
        if self.hasPattern:
            pt = []
            for i in range(len(self.objctrl.usePattern)):
                if self.objctrl.usePattern[i]:
                    color = self.objctrl.itemInfo.color[i+3]
                    pi = self.objctrl.itemInfo.pattern[i]
                    pt.append((color, pi.ut, pi.vt, pi.us, pi.vs, pi.rot))
                else:
                    pt.append(None)
            return tuple(pt)

    @property
    def hasPanel(self):
        return self.isItem and self.objctrl.checkPanel

    def set_panel(self, param):
        # param: a set of (filepath, clamp)
        if self.hasPanel: 
            self.objctrl.SetMainTex(param[0])
            self.objctrl.SetPatternClamp(0, param[1])

    def get_panel(self):
        if self.hasPanel:
            pi = self.objctrl.itemInfo.panel
            p0 = self.objctrl.itemInfo.pattern[0]
            return (pi.filePath, p0.clamp)

    def set_panel_detail(self, param):
        # param: a set of (color, ut, vt, us, vs, rot)
        if self.hasPanel: 
            p0 = self.objctrl.itemInfo.pattern[0]
            self.objctrl.itemInfo.color[0] = tuple4_2_color(param[0])
            p0.ut = param[1]
            p0.vt = param[2]
            p0.us = param[3]
            p0.vs = param[4]
            p0.rot = param[5]
            self.objctrl.UpdateColor()

    def get_panel_detail(self):
        if self.hasPanel:
            p0 = self.objctrl.itemInfo.pattern[0]
            return (self.objctrl.itemInfo.color[0], p0.ut, p0.vt, p0.us, p0.vs, p0.rot)

    @property
    def hasEmission(self):
        if not self.isItem:
            return False
        else:
            return self.objctrl.checkEmission

    def set_emission(self, param):
        # param: (color, power)
        if self.hasEmission:
            eColor = tuple4_2_color(param[0])
            ePower = param[1]
            self.objctrl.itemInfo.emissionColor = eColor
            self.objctrl.itemInfo.emissionPower = ePower
            self.objctrl.UpdateColor()
        
    def get_emission(self):
        if self.hasEmission:
            eColor = self.objctrl.itemInfo.emissionColor
            ePower = self.objctrl.itemInfo.emissionPower
            return (eColor, ePower)
        else:
            return None

    @property
    def hasAlpha(self):
        return self.isColorable and self.objctrl.checkAlpha

    def set_alpha(self, param):
        # param: 0~1 for alpha
        if param != None:
            self.objctrl.SetAlpha(param)

    def get_alpha(self):
        if self.hasAlpha:
            return self.objctrl.itemInfo.alpha
        else:
            return None

    @property
    def hasLine(self):
        return self.isItem and self.objctrl.checkLine

    def set_line(self, param):
        # param: (lineColor, lineWidth)
        if self.hasLine:
            self.objctrl.SetLineColor(tuple4_2_color(param[0]))
            self.objctrl.SetLineWidth(param[1])

    def get_line(self):
        if self.hasLine:
            return (self.objctrl.itemInfo.lineColor, self.objctrl.itemInfo.lineWidth)

    @property
    def hasShadowColor(self):
        return self.isItem and self.objctrl.checkShadow
    
    def set_shadow_color(self, param):
        # param: color
        if self.hasShadowColor:
            self.objctrl.itemInfo.color[6] = tuple4_2_color(param)
            self.objctrl.UpdateColor()

    def get_shadow_color(self):
        if self.hasShadowColor:
            return self.objctrl.itemInfo.color[6]

    @property
    def hasLightCancel(self):
        return self.isItem and self.objctrl.checkLightCancel

    def set_light_cancel(self, param):
        # param: light cancel
        if self.hasLightCancel:
            self.objctrl.SetLightCancel(param)

    def get_light_cancel(self):
        if self.hasLightCancel:
            return self.objctrl.itemInfo.lightCancel

    @property
    def isDynamicBone(self):
        if self.isItem:
            return self.objctrl.isDynamicBone
        else:
            return False

    def set_dynamicbone_enable(self, param):
        # param: dynamic bone (yure) enable/disable
        if self.isDynamicBone:
            self.objctrl.ActiveDynamicBone(param)

    def get_dynamicbone_enable(self):
        if self.isDynamicBone:
            return self.objctrl.itemInfo.enableDynamicBone

    @property
    def isRoute(self):
        from Studio import OCIRoute
        return isinstance(self.objctrl, OCIRoute)

    def set_route_play(self, param):
        # param: 1=start/0=stop
        if self.isRoute:
            if param:
                self.objctrl.Play()
            else:
                self.objctrl.Stop()

    def get_route_play(self):
        if self.isRoute:
            return self.objctrl.isPlay

    def set_route_full(self, param):
        # route info, ref to get_route_full
        if self.isRoute:
            from Studio import OIRouteInfo, StudioTween, OIRoutePointInfo
            try:
                # route_p, only play/stop info
                if not isinstance(param, tuple):
                    self.set_route_play(param)
                    return
                # route_f, full route setting
                self.objctrl.Stop() # stop for change setting
                cur_status = self.get_route_full()
                for i in range(len(cur_status)):
                    if param[i] == cur_status[i]:
                        continue
                    ri = self.objctrl.routeInfo
                    if i == 0:  # orient
                        ri.orient = value_2_enum(OIRouteInfo.Orient, param[i])
                    elif i == 1: # loop
                        ri.loop = bool(param[i])
                        self.objctrl.UpdateLine()
                    elif i == 2: # points
                        for j in range(len(cur_status[i])):
                            pt = param[i][j]
                            pt_cur = cur_status[i][j]
                            if pt == pt_cur:
                                continue
                            pi = self.objctrl.routeInfo.route[j]
                            for k in range(len(pt_cur)):
                                if pt[k] == pt_cur[k]:
                                    continue
                                if k == 0: # pt pos
                                    pi.changeAmount.pos = pt[k]
                                elif k == 1: # pt rot
                                    pi.changeAmount.rot = pt[k]
                                elif k == 2: # aid pos
                                    pi.aidInfo.changeAmount.pos = pt[k]
                                elif k == 3: # speed
                                    pi.speed = pt[k]
                                elif k == 4: # easeType
                                    pi.easeType = value_2_enum(StudioTween.EaseType, pt[k])
                                elif k == 5: # connection
                                    pi.connection = value_2_enum(OIRoutePointInfo.Connection, pt[k])
                                elif k == 6: # link
                                    pi.link = bool(pt[k])
                        self.objctrl.UpdateLine()
                    elif i == 3: # active
                        self.set_route_play(param[i])
                    else:
                        raise Exception("Unknown route info")
            except Exception, e:
                print "VNGE VNActor Error: Can not set route, ", e

    def get_route_full(self):
        if self.isRoute:
            ri = self.objctrl.routeInfo
            pts = []
            for pi in ri.route:
                # (pt pos, pt rot, aid pos, speed, easeType, connection, link)
                pts.append((pi.changeAmount.pos, pi.changeAmount.rot, pi.aidInfo.changeAmount.pos, pi.speed, pi.easeType.value__, pi.connection.value__, pi.link))
            # (orient, loop, points, active)
            rs = (ri.orient.value__, ri.loop, tuple(pts), ri.active)
            return rs

    def export_full_status(self):
        # export full status of prop
        fs = {}
        fs["visible"] = self.visible
        fs["move_to"] = self.pos
        fs["rotate_to"] = self.rot
        if self.isItem:
            fs["scale_to"] = self.scale
            if self.isAnime:
                fs["anim_spd"] = self.get_anime_speed()
            if self.isColorable:
                fs["color"] = self.get_color()
            if self.hasPattern:
                fs["ptn_set"] = self.get_pattern()
                fs["ptn_dtl"] = self.get_pattern_detail()
            if self.hasPanel:
                fs["pnl_set"] = self.get_panel()
                fs["pnl_dtl"] = self.get_panel_detail()
            if self.hasEmission:
                fs["emission"] = self.get_emission()
            if self.hasAlpha:
                fs["alpha"] = self.get_alpha()
            if self.hasLine:
                fs["line"] = self.get_line()
            if self.hasShadowColor:
                fs["shadow_c"] = self.get_shadow_color()
            if self.hasLightCancel:
                fs["light_cancel"] = self.get_light_cancel()
            if self.isFK:
                fs["fk_set"] = self.export_fk_bone_info()
            if self.isDynamicBone:
                fs["db_active"] = self.get_dynamicbone_enable()
        if self.isLight:
            fs["color"] = self.get_color()
            fs["enable"] = self.enable
            fs["intensity"] = self.get_intensity
            fs["shadow"] = self.get_shadow
            if self.hasRange:
                fs["range"] = self.get_range()
            if self.hasAngle:
                fs["angle"] = self.get_angle()
        if self.isRoute:
            if is_ini_value_true("ExportProp_RouteFull"):
                fs["route_f"] = self.get_route_full()
            else:
                fs["route_p"] = self.get_route_play()
        return fs
        
class PropNeoV2(Prop):
    def set_color(self, color):
        # color : a tuple of UnityEngine.Color
        if self.isColorable:
            if not isinstance(color, tuple):
                color = (color, None, None, None)
            i = 0
            if self.objctrl.useColor[0] and i < len(color) and color[i] != None:
                self.objctrl.itemInfo.colors[0].mainColor = tuple4_2_color(color[i])
            i = 1
            if self.objctrl.useColor[1] and i < len(color) and color[i] != None:
                self.objctrl.itemInfo.colors[1].mainColor = tuple4_2_color(color[i])
            i = 2
            if self.objctrl.useColor[2] and i < len(color) and color[i] != None:
                self.objctrl.itemInfo.colors[2].mainColor = tuple4_2_color(color[i])
            i = 3
            if self.objctrl.useColor4 and i < len(color) and color[i] != None:
                self.objctrl.itemInfo.colors[3].mainColor = tuple4_2_color(color[i])
            self.objctrl.UpdateColor()
        elif self.isLight:
            c = tuple4_2_color(color)
            self.objctrl.SetColor(c)

    def get_color(self):
        # return a tuple of used color
        if self.isColorable:
            cl = []
            if self.objctrl.useColor[0]:
                cl.append(self.objctrl.itemInfo.colors[0].mainColor)
            else:
                cl.append(None)
            if self.objctrl.useColor[1]:
                cl.append(self.objctrl.itemInfo.colors[1].mainColor)
            else:
                cl.append(None)
            if self.objctrl.useColor[2]:
                cl.append(self.objctrl.itemInfo.colors[2].mainColor)
            else:
                cl.append(None)
            if self.objctrl.useColor4:
                cl.append(self.objctrl.itemInfo.colors[3].mainColor)
            else:
                cl.append(None)
            return tuple(cl)
        elif self.isLight:
            return self.objctrl.lightInfo.color

    @property
    def hasPattern(self):
        if not self.isItem:
            return False
        for n in self.objctrl.usePattern:
            if n:
                return True
            return False

    def set_pattern(self, param):
        # param: a set of ((key, filepath, clamp), (key, filepath, clamp), (key, filepath, clamp))
        if self.hasPattern:
            for i in range(len(self.objctrl.usePattern)):
                if self.objctrl.usePattern[i] and param[i] != None:
                    self.objctrl.itemInfo.colors[i].pattern.key = param[i][0]
                    self.objctrl.itemInfo.colors[i].pattern.filePath = param[i][1]
                    self.objctrl.itemInfo.colors[i].pattern.clamp = param[i][2]
            self.objctrl.SetupPatternTex()
            self.objctrl.UpdateColor()

    def get_pattern(self):
        if self.hasPattern:
            pt = []
            for i in range(len(self.objctrl.usePattern)):
                if self.objctrl.usePattern[i]:
                    pi = self.objctrl.itemInfo.colors[i].pattern
                    pt.append((pi.key, pi.filePath, pi.clamp))
                else:
                    pt.append(None)
            return tuple(pt)

    def set_pattern_detail(self, param):
        # param: a set of ((color, ut, vt, us, vs, rot), (color, ut, vt, us, vs, rot), (color, ut, vt, us, vs, rot))
        if self.hasPattern:
            for i in range(len(self.objctrl.usePattern)):
                if self.objctrl.usePattern[i] and param[i] != None:
                    self.objctrl.itemInfo.colors[i].pattern.color = tuple4_2_color(param[i][0])
                    self.objctrl.itemInfo.colors[i].pattern.ut = param[i][1]
                    self.objctrl.itemInfo.colors[i].pattern.vt = param[i][2]
                    self.objctrl.itemInfo.colors[i].pattern.us = param[i][3]
                    self.objctrl.itemInfo.colors[i].pattern.vs = param[i][4]
                    self.objctrl.itemInfo.colors[i].pattern.rot = param[i][5]
            self.objctrl.UpdateColor()

    def get_pattern_detail(self):
        if self.hasPattern:
            pt = []
            for i in range(len(self.objctrl.usePattern)):
                if self.objctrl.usePattern[i]:
                    pi = self.objctrl.itemInfo.colors[i].pattern
                    pt.append((pi.color, pi.ut, pi.vt, pi.us, pi.vs, pi.rot))
                else:
                    pt.append(None)
            return tuple(pt)
    
    @property
    def hasPanel(self):
        return self.isItem and self.objctrl.checkPanel

    def set_panel(self, param):
        # param: a set of (filepath, clamp)
        if self.hasPanel: 
            self.objctrl.SetMainTex(param[0])
            self.objctrl.SetPatternClamp(0, param[1])

    def get_panel(self):
        if self.hasPanel:
            pi = self.objctrl.itemInfo.panel
            p0 = self.objctrl.itemInfo.colors[0].pattern
            return (pi.filePath, p0.clamp)

    def set_panel_detail(self, param):
        # param: a set of (color, ut, vt, us, vs, rot)
        if self.hasPanel: 
            p0 = self.objctrl.itemInfo.colors[0].pattern
            self.objctrl.itemInfo.colors[0].mainColor = tuple4_2_color(param[0])
            p0.ut = param[1]
            p0.vt = param[2]
            p0.us = param[3]
            p0.vs = param[4]
            p0.rot = param[5]
            self.objctrl.UpdateColor()

    def get_panel_detail(self):
        if self.hasPanel:
            p0 = self.objctrl.itemInfo.colors[0].pattern
            return (self.objctrl.itemInfo.colors[0].mainColor, p0.ut, p0.vt, p0.us, p0.vs, p0.rot)

    @property
    def hasMetallic(self):
        if not self.isColorable:
            return False
        for n in self.objctrl.useMetallic:
            if n:
                return True
        return False

    def set_metallic(self, param):
        # param: a set of ((metallic, glossiness), (metallic, glossiness), ...)
        if self.hasMetallic:
            for i in range(len(self.objctrl.useMetallic)):
                if self.objctrl.useMetallic[i] and param[i] != None:
                    self.objctrl.itemInfo.colors[i].metallic = param[i][0]
                    self.objctrl.itemInfo.colors[i].glossiness = param[i][1]
            self.objctrl.UpdateColor()

    def get_metallic(self):
        if self.hasMetallic:
            mv = []
            for i in range(len(self.objctrl.useMetallic)):
                if self.objctrl.useMetallic[i]:
                    mv.append((self.objctrl.itemInfo.colors[i].metallic, self.objctrl.itemInfo.colors[i].glossiness))
                else:
                    mv.append(None)
            return tuple(mv)
        else:
            return None

    @property
    def hasEmission(self):
        if not self.isItem:
            return False
        else:
            return self.objctrl.CheckEmission

    def set_emission(self, param):
        # param: (color, power)
        if self.hasEmission:
            eColor = tuple4_2_color(param[0])
            ePower = param[1]
            #self.objctrl.SetEmissionColor(eColor)
            #self.objctrl.SetEmissionPower(ePower)
            self.objctrl.itemInfo.emissionColor = eColor
            self.objctrl.itemInfo.emissionPower = ePower
            self.objctrl.UpdateColor()
        
    def get_emission(self):
        if self.hasEmission:
            eColor = self.objctrl.itemInfo.emissionColor
            ePower = self.objctrl.itemInfo.emissionPower
            return (eColor, ePower)
        else:
            return None

    @property
    def hasAlpha(self):
        return self.isColorable and self.objctrl.CheckAlpha

    def set_alpha(self, param):
        # param: 0~1 for alpha
        if param != None:
            self.objctrl.SetAlpha(param)

    def get_alpha(self):
        if self.hasAlpha:
            return self.objctrl.itemInfo.alpha
        else:
            return None

    @property
    def hasOption(self):
        return self.isItem and self.objctrl.CheckOption

    def set_option(self, param):
        # param: True/False for item option setting
        if param != None:
            self.objctrl.SetOptionVisible(bool(param))

    def get_option(self):
        if self.hasOption and self.objctrl.itemInfo.option != None and len(self.objctrl.itemInfo.option) > 0:
            return self.objctrl.itemInfo.option[0]
        else:
            return None

    # fk enable
    def set_fk_enable(self, param):
        # param: fk enable/disable
        if self.isFK:
            self.objctrl.ActiveFK(param)

    def get_fk_enable(self):
        if self.isFK:
            return self.objctrl.itemInfo.enableFK

    @property
    def isDynamicBone(self):
        if self.isItem:
            return self.objctrl.isDynamicBone
        else:
            return False

    def set_dynamicbone_enable(self, param):
        # param: dynamic bone (yure) enable/disable
        if self.isDynamicBone:
            self.objctrl.ActiveDynamicBone(param)

    def get_dynamicbone_enable(self):
        if self.isDynamicBone:
            return self.objctrl.itemInfo.enableDynamicBone

    @property
    def hasAnimePattern(self):
        return self.isItem and self.isAnime and self.objctrl.CheckAnimePattern

    def set_anime_pattern(self, param):
        # param: anime pattern no
        if self.hasAnimePattern:
            self.objctrl.SetAnimePattern(param)
    
    def get_anime_pattern(self):
        if self.hasAnimePattern:
            return self.objctrl.itemInfo.animePattern
    
    @property
    def isRoute(self):
        from Studio import OCIRoute
        return isinstance(self.objctrl, OCIRoute)

    def set_route_play(self, param):
        # param: 1=start/0=stop
        if self.isRoute:
            if param:
                self.objctrl.Play()
            else:
                self.objctrl.Stop()

    def get_route_play(self):
        if self.isRoute:
            return self.objctrl.isPlay

    def set_route_full(self, param):
        # route info, ref to get_route_full
        if self.isRoute:
            from Studio import OIRouteInfo, StudioTween, OIRoutePointInfo
            try:
                # route_p, only play/stop info
                if not isinstance(param, tuple):
                    self.set_route_play(param)
                    return
                # route_f, full route setting
                self.objctrl.Stop() # stop for change setting
                cur_status = self.get_route_full()
                for i in range(len(cur_status)):
                    if param[i] == cur_status[i]:
                        continue
                    ri = self.objctrl.routeInfo
                    if i == 0:  # orient
                        ri.orient = value_2_enum(OIRouteInfo.Orient, param[i])
                    elif i == 1: # loop
                        ri.loop = bool(param[i])
                        self.objctrl.UpdateLine()
                    elif i == 2: # points
                        for j in range(len(cur_status[i])):
                            pt = param[i][j]
                            pt_cur = cur_status[i][j]
                            if pt == pt_cur:
                                continue
                            pi = self.objctrl.routeInfo.route[j]
                            for k in range(len(pt_cur)):
                                if pt[k] == pt_cur[k]:
                                    continue
                                if k == 0: # pt pos
                                    pi.changeAmount.pos = pt[k]
                                elif k == 1: # pt rot
                                    pi.changeAmount.rot = pt[k]
                                elif k == 2: # aid pos
                                    pi.aidInfo.changeAmount.pos = pt[k]
                                elif k == 3: # speed
                                    pi.speed = pt[k]
                                elif k == 4: # easeType
                                    pi.easeType = value_2_enum(StudioTween.EaseType, pt[k])
                                elif k == 5: # connection
                                    pi.connection = value_2_enum(OIRoutePointInfo.Connection, pt[k])
                                elif k == 6: # link
                                    pi.link = bool(pt[k])
                        self.objctrl.UpdateLine()
                    elif i == 3: # active
                        self.set_route_play(param[i])
                    else:
                        raise Exception("Unknown route info")
            except Exception, e:
                print "VNGE VNActor Error: Can not set route, ", e

    def get_route_full(self):
        if self.isRoute:
            ri = self.objctrl.routeInfo
            pts = []
            for pi in ri.route:
                # (pt pos, pt rot, aid pos, speed, easeType, connection, link)
                pts.append((pi.changeAmount.pos, pi.changeAmount.rot, pi.aidInfo.changeAmount.pos, pi.speed, pi.easeType.value__, pi.connection.value__, pi.link))
            # (orient, loop, points, active)
            rs = (ri.orient.value__, ri.loop, tuple(pts), ri.active)
            return rs

    def export_full_status(self):
        # export full status of prop
        fs = {}
        fs["visible"] = self.visible
        fs["move_to"] = self.pos
        fs["rotate_to"] = self.rot
        if self.isItem:
            fs["scale_to"] = self.scale
            if self.isColorable:
                fs["color"] = self.get_color()
            if self.hasPattern:
                fs["ptn_set"] = self.get_pattern()
                fs["ptn_dtl"] = self.get_pattern_detail()
            if self.hasPanel:
                fs["pnl_set"] = self.get_panel()
                fs["pnl_dtl"] = self.get_panel_detail()
            if self.hasMetallic:
                fs["metallic"] = self.get_metallic()
            if self.hasEmission:
                fs["emission"] = self.get_emission()
            if self.hasAlpha:
                fs["alpha"] = self.get_alpha()
            if self.hasOption:
                fs["option"] = self.get_option()
            if self.isFK:
                fs["fk_active"] = self.get_fk_enable()
                if fs["fk_active"]:
                    fs["fk_set"] = self.export_fk_bone_info()
                else:
                    fs["fk_set"] = ()
            if self.isDynamicBone:
                fs["db_active"] = self.get_dynamicbone_enable()
            if self.isAnime:
                fs["anim_spd"] = self.get_anime_speed()
            if self.hasAnimePattern:
                fs["anim_ptn"] = self.get_anime_pattern()
        if self.isLight:
            fs["color"] = self.get_color()
            fs["enable"] = self.enable
            fs["intensity"] = self.get_intensity
            fs["shadow"] = self.get_shadow
            if self.hasRange:
                fs["range"] = self.get_range()
            if self.hasAngle:
                fs["angle"] = self.get_angle()
        if self.isRoute:
            if is_ini_value_true("ExportProp_RouteFull"):
                fs["route_f"] = self.get_route_full()
            else:
                fs["route_p"] = self.get_route_play()

        return fs

#===============================================================================================
# camera action wrapper functions
# All scripts: func(game, param)
def cam_goto_preset(game, param):
    if not isinstance(param, tuple):
        #param = set (1~10)
        game.to_camera(param)
    elif len(param) == 2:
        # param = (set, duration)
        game.anim_to_camera_num(param[1], param[0])
    elif len(param) == 3:
        # param = (set, duration, style)
        game.anim_to_camera_num(param[1], param[0], param[2])
    elif len(param) == 4:
        # param = (set, duration, style, onCamEnd)
        game.anim_to_camera_num(param[1], param[0], param[2], param[3])
    else:
        print "cam_anim_set param format error"

def cam_goto_pos(game, param):
    if len(param) == 3:
        # param = ((pos_x, pos_y, pos_z), (dis_x, dis_y, dis_z), (rot_x, rot_y, rot_z))
        game.move_camera(pos=param[0], distance=param[1], rotate=param[2])
    elif len(param) == 4:
        # param = ((pos_x, pos_y, pos_z), (dis_x, dis_y, dis_z), (rot_x, rot_y, rot_z), duration)
        game.anim_to_camera(param[3], pos=param[0], distance=param[1], rotate=param[2])
    elif len(param) == 5:
        # param = ((pos_x, pos_y, pos_z), (dis_x, dis_y, dis_z), (rot_x, rot_y, rot_z), duration, style)
        game.anim_to_camera(param[3], pos=param[0], distance=param[1], rotate=param[2], style=param[4])
    elif len(param) == 6:
        # param = ((pos_x, pos_y, pos_z), (dis_x, dis_y, dis_z), (rot_x, rot_y, rot_z), duration, style, onCameraEnd)
        game.anim_to_camera(param[3], pos=param[0], distance=param[1], rotate=param[2], fov=param[4], style=param[5])
    else:
        print "cam_goto_pos param format error"

def cam_rotate(game, param):
    camobj = game.get_camera_num(0) # get current camera position - as 0 index
    v3 = camobj["rotate"] # getting vector for rotate
    if len(param) == 3 and (not isinstance(param[0], tuple)):
        # param = (rot_delta_x, rot_delta_y, rot_delta_z)
        camobj["rotate"] = Vector3(v3.x+param[0], v3.y+param[1], v3.z+param[2]) # set new rotation
        game.move_camera_obj(camobj) # move to this camera
    elif len(param) == 2:
        # param = ((rot_delta_x, rot_delta_y, rot_delta_z), duration)
        camobj["rotate"] = Vector3(v3.x+param[0][0], v3.y+param[0][1], v3.z+param[0][2]) # set new rotation
        game.anim_to_camera_obj(param[1], camobj) # animate to this camera
    elif len(param) == 3:
        # param = ((rot_delta_x, rot_delta_y, rot_delta_z), duration, style)
        camobj["rotate"] = Vector3(v3.x+param[0][0], v3.y+param[0][1], v3.z+param[0][2]) # set new rotation
        game.anim_to_camera_obj(param[1], camobj, param[2]) # animate to this camera
    elif len(param) == 4:
        # param = ((rot_delta_x, rot_delta_y, rot_delta_z), duration, style, onCameraEnd)
        camobj["rotate"] = Vector3(v3.x+param[0][0], v3.y+param[0][1], v3.z+param[0][2]) # set new rotation
        game.anim_to_camera_obj(param[1], camobj, param[2], param[3]) # animate to this camera
    else:
        print "cam_rotate param format error"

def cam_zoom(game, param):
    camobj = game.get_camera_num(0) # get current camera position - as 0 index
    dv3 = camobj["distance"] # getting vector for distance
    if (not isinstance(param, tuple)):
        # param = zoom_delta, use positive value to zoom in, and negative value for zoom out 
        camobj["distance"] = game.vec3(dv3.x, dv3.y, dv3.z+param[0]) # set new distance
        game.move_camera_obj(param[1], camobj) # move to this camera
    elif len(param) == 2:
        # param = (zoom_delta, duration)
        camobj["distance"] = game.vec3(dv3.x, dv3.y, dv3.z+param[0]) # set new distance
        game.anim_to_camera_obj(param[1], camobj) # animate to this camera
    elif len(param) == 3:
        # param = (zoom_delta, duration, style)
        camobj["distance"] = game.vec3(dv3.x, dv3.y, dv3.z+param[0]) # set new distance
        game.anim_to_camera_obj(param[1], camobj, param[2]) # animate to this camera
    elif len(param) == 4:
        # param = (zoom_delta, duration, style, onCameraEnd)
        camobj["distance"] = game.vec3(dv3.x, dv3.y, dv3.z+param[0]) # set new distance
        game.anim_to_camera_obj(param[1], camobj, param[2], param[3]) # animate to this camera
    else:
        print "cam_rotate param format error"

def set_camera_data(game, data):
    # game is not used now
    from Studio import Studio
    c = Studio.Instance.cameraCtrl
    cdata = c.cameraData
    try:
        cdata.pos = data[0]
        cdata.distance = data[1]
        cdata.rotate = data[2]
        c.fieldOfView = data[3]
    except:
        print "set_camera_data failed! Wrong cam data format?", data

def get_camera_data(game):
    # game is not used now
    from Studio import Studio
    c = Studio.Instance.cameraCtrl
    cdata = c.cameraData
    cam_data = (cdata.pos, cdata.distance, cdata.rotate, c.fieldOfView)
    return cam_data

def set_camera_name(game, name):
    # set the named camera as active camera, if name is None or not found, switch to default camera
    # if active an object camera, return true. Or return false if non object camera actived.
    """:type game: vngameengine.VNNeoController"""
    if game.isCharaStudio or game.isNEOV2:
        from Studio import OCICamera
        for ociobj in game.studio.dicObjectCtrl.Values:
            if isinstance(ociobj, OCICamera) and ociobj.name == name:
                if game.studio.ociCamera != ociobj:
                    game.studio.ChangeCamera(ociobj)
                return
        game.studio.ChangeCamera(None)

def get_camera_name(game):
    # return the current active camera's name, or return None if no camera actived.
    """:type game: vngameengine.VNNeoController"""
    if game.isCharaStudio or game.isNEOV2:
        if game.studio.ociCamera != None:
            return game.studio.ociCamera.name
    return None

cam_act_funcs = {
    'goto_preset': (cam_goto_preset, False),
    'goto_pos': (cam_goto_pos, True),
    'rotate': (cam_rotate, False),
    'zoom': (cam_zoom, False),
}

#===============================================================================================
# character action wrapper functions list
# All scripts: func(char, param)
def char_anime(char, param):
    if len(param) == 3:
        # param = (group, category, no)
        char.animate(param[0], param[1], param[2])
    elif len(param) == 4:
        # param = (group, category, no, normalizedTime)
        char.animate(param[0], param[1], param[2], param[3])
    elif len(param) == 5:
        # param = (group, category, no, normalizedTime, forceload)
        char.animate(param[0], param[1], param[2], param[3], param[4])
    else:
        print "char_anime param format error"

def char_anime_speed(char, param):
    # param = speed (0~3)
    char.set_anime_speed(param)
    
def char_anime_pattern(char, param):
    # param = pattern (0~1)
    char.set_anime_pattern(param)
    
def char_anime_forceloop(char, param):
    # param = force loop (0/1)
    char.set_anime_forceloop(param)
    
def char_anime_optionparam(char, param):
    # param = (aux value 1, aux value 2)
    char.set_anime_option_param(param)
    
def char_anime_restart(char, param):
    # param ignore
    char.restart_anime()
    
def char_load_cloth(char, param):
    # load cloth
    char.load_clothes_file(param)
    
def char_cloth_type(char, param):
    #print "char_cloth_type:", str(param), "not implemented, charInfo.ChangeCoordinateTypeAndReload() will clash"
    char.set_coordinate_type(param)
    
def char_cloth(char, param):
    # param = (clothIndex, clothState)
    char.set_cloth(param[0], param[1])

def char_all_clothes(char, param):
    # param = 0(all), 1(half), 2(nude)
    # or
    # param = (top, bottom, bra, shorts, grove, panst, sock, shoe)
    char.set_cloth(param)

def char_accessory(char, param):
    # param = (accIndex, accShow)
    char.set_accessory(param[0], param[1])

def char_all_accessories(char, param):
    # param = 0(hide all)/1(show all)
    # or
    # param = (accShow0, accShow1, ... accShow19)
    char.set_accessory(param)

def char_juice(char, param):
    # param = juice level on (face, FrontUp, BackUp, FrontDown, BackDown) where 0-none, 1-few, 2-lots, or just on int to set all
    if not isinstance(param, tuple) and not isinstance(param, list):
        param = (param, param, param, param, param)
    char.set_juice(param)

def char_tear(char, param):
    # param = tear level(0,1,2,3) or (0~1 for PH)
    char.set_tear(param)
    
def char_face_red(char, param):
    # param = hohoAka level(0~1)
    char.set_facered(param)
    
def char_nip_stand(char, param):
    # param = nipple stand level (0~1)
    char.set_nipple_stand(param)

def char_tuya(char, param):
    # param = skin tuya 0~1
    char.set_tuya(param)

def char_wet(char, param):
    # param = skin wet 0~1
    char.set_wet(param)

def char_face_option(char, param):
    # param = 0-none, 1-ball, 2-tape
    char.set_face_option(param)
    
def char_son(char, param):
    # param = visible or (visible(0/1), length(0~3))
    char.set_son(param)
    
def char_simple(char, param):
    # param = simple visible
    char.set_simple(param)
    
def char_simple_color(char, param):
    # param = simple color
    char.set_simple_color(param)

def char_eyes_look(char, param):
    # param = 0, 1, 2, 3, 4 or (x, y, z)
    if not (isinstance(param, tuple) or isinstance(param, Vector3)):
        param = int(param)
    char.set_look_eye(param)
    
def char_eyes_look_ptn(char, param):
    # param = 0, 1, 2, 3, 4
    char.set_look_eye_ptn(param)
    
def char_eyes_look_pos(char, param):
    # param = Vector3 or (x, y, z)
    char.set_look_eye_pos(param)

def char_neck_look(char, param):
    # param = 0, 1, 2, 3, 4
    char.set_look_neck(param)

def char_neck_look_full(char, param):
    # param = array of bytes, use dump to get it
    try:
        char.set_look_neck_full(param)
    except Exception, e:
        print("Error in setting char neck in Fixed state: " + str(e))
        print("Sorry, we just pass it...")

def char_neck_look_full2(char, param):
    # param = array of bytes, use dump to get it
    try:
        char.set_look_neck_full2(param)
    except Exception, e:
        print("Error in setting char neck in Fixed state (2): " + str(e))
        print("Sorry, we just pass it...")

def char_eyebrow(char, param):
    # param = eyebrow pattern
    char.set_eyebrow_ptn(param)
    
def char_eyes(char, param):
    # param = eye pattern
    char.set_eyes_ptn(param)

def char_eyes_open(char, param):
    # param = 0~1
    char.set_eyes_open(param)

def char_eyes_blink(char, param):
    # param = 0(False)/1(True)
    char.set_eyes_blink(param)

def char_mouth(char, param):
    # param = mouth pattern
    char.set_mouth_ptn(param)

def char_mouth_open(char, param):
    # param = 0~1
    char.set_mouth_open(param)
    
def char_lip_sync(char, param):
    # param = 0/1
    char.set_lip_sync(param)
    
def char_hands(char, param):
    # param = (left hand ptn, right hand ptn)
    char.set_hand_ptn(param)

def char_move(char, param):
    # param = (pos_delta_x, pos_delta_y, pos_delta_z)
    cp = char.pos
    ncp = Vector3(cp.x + param[0], cp.y + param[1], cp.z + param[2])
    char.move(pos=ncp)

def char_move_to(char, param):
    # param = (pos_dst_x, pos_dst_y, pos_dst_z)
    char.move(pos=param)
    
def char_turn(char, param):
    # param = rot_delta_y
    rt = char.rot
    nrt = Vector3(rt.x, rt.y + param, rt.z)
    char.move(rot=nrt)
    
def char_turn_to(char, param):
    # param = rot_dst_y
    rt = char.rot
    nrt = Vector3(rt.x, param, rt.z)
    char.move(rot=nrt)

def char_rotate_to(char, param):
    # param = (rot_x, rot_y, rot_z)
    # for rotate x and z
    char.move(rot=param)

def char_scale_to(char, param):
    # param = (scale_x, scale_y, scale_z) or scale
    if not isinstance(param, tuple) and not isinstance(param, Vector3):
        param = (param, param, param)
    char.move(scale=param)
    
def char_kinematic(char, param):
    # param = 0-none, 1-IK, 2-FK
    char.set_kinematic(param)

def char_fk_active(char, param):
    # param = 0/1 flag in tuple (hair, neck, Breast, body, right hand, left hand, skirt)
    curFk = char.get_FK_active()
    for i in range(7):
        if param[i] != curFk[i]:
            char.set_FK_active(i, param[i])
            
def char_fk_set(char, param):
    # param = fk bones info dict
    char.import_fk_bone_info(param)
    
def char_ik_active(char, param):
    # param = 0/1 flag in tuple (body, right leg, left leg, right arm, left arm)
    curIk = char.get_IK_active()
    for i in range(5):
        if param[i] != curIk[i]:
            char.set_IK_active(i, param[i])
            
def char_ik_set(char, param):
    # param = ik target info dict
    char.import_ik_target_info(param)
    
def char_voice_lst(char, param):
    # param = voice list
    # always play the voice
    char.set_voice_lst(param)
    
def char_voice_rpt(char, param):
    # param = voice repeat flag
    char.set_voice_repeat(param)
    
def char_visible(char, param):
    # param = 0 or 1
    char.visible = param

def char_shoes(char, param):
    # param = 0 or 1
    char.set_shoes_type(param)

def char_ext_curclothcoord(char, param):
    # param = voice repeat flag
    try:
        char.set_curcloth_coordinate(param)
    except Exception, e:
        print "VNGE VNActor error: can't set curcloth coord", e
        pass

def char_ext_curclothcoordnoacc(char, param):
    # param = voice repeat flag
    try:
        char.set_curcloth_coordinate_no_accessory(param)
    except Exception, e:
        print "VNGE VNActor error: can't set curcloth coord", e
        pass


def char_ext_bodyshapes(char, param):
    # param = body shape array
    try:
        char.set_body_shapes_all(param)
    except Exception, e:
        print "VNGE VNActor error: can't set body shapes", e
        pass

def char_ext_faceshapes(char, param):
    # param = face shape array
    try:
        char.set_face_shapes_all(param)
    except Exception, e:
        print "VNGE VNActor error: can't set face shapes", e
        pass

def char_pl_hspedata(char, param):
    # param = hspe data
    try:
        char.set_hspedata(param)
    except Exception, e:
        print "VNGE VNActor error: can't set HSPE data", e
        pass

def char_pl_kkpedata(char, param):
    # param = kkpe data
    try:
        char.set_kkpedata(param)
    except Exception, e:
        print "VNGE VNActor error: can't set KKPE data", e
        pass

def char_pl_aipedata(char, param):
    # param = aipe data
    try:
        char.set_aipedata(param)
    except Exception, e:
        print "VNGE VNActor error: can't set AIPE data", e
        pass

char_act_funcs = {
    'anim': (char_anime, False),
    'anim_spd': (char_anime_speed, True),
    'anim_ptn': (char_anime_pattern, True),
    'anim_lp': (char_anime_forceloop, False),
    'anim_optprm': (char_anime_optionparam, True),
    'anim_restart': (char_anime_restart, False),
    'load_cloth': (char_load_cloth, False),
    'cloth_type': (char_cloth_type, False),
    'cloth': (char_cloth, False),
    'cloth_all': (char_all_clothes, False),
    'acc': (char_accessory, False),
    'acc_all': (char_all_accessories, False),
    'juice': (char_juice, False),
    'tear': (char_tear, False), # tear can be animate in PlayHome. But not in Neo or CharaStudio
    'face_red': (char_face_red, True),
    'nip_stand': (char_nip_stand, True),
    'skin_tuya': (char_tuya, True),
    'skin_wet': (char_wet, True),
    'face_opt': (char_face_option, False),
    'son': (char_son, True),
    'simple': (char_simple, False),
    'simple_color': (char_simple_color, True),
    'look_at': (char_eyes_look, True),
    'look_at_ptn': (char_eyes_look_ptn, False),
    'look_at_pos': (char_eyes_look_pos, True),
    'face_to': (char_neck_look, False),
    'face_to_full': (char_neck_look_full, False),
    'face_to_full2': (char_neck_look_full2, False),
    'eyebrow': (char_eyebrow, False),
    'eyes': (char_eyes, False),
    'eyes_open': (char_eyes_open, True),
    'eyes_blink': (char_eyes_blink, False),
    'mouth': (char_mouth, False),
    'mouth_open': (char_mouth_open, True),
    'lip_sync': (char_lip_sync, False),
    'hands': (char_hands, False),
    'move': (char_move, False),
    'move_to': (char_move_to, True),
    'turn': (char_turn, False),
    'turn_to': (char_turn_to, True),
    'rotate_to': (char_rotate_to, True),
    'scale_to': (char_scale_to, True),
    'kinematic': (char_kinematic, False),
    'fk_active': (char_fk_active, False),
    'fk_set': (char_fk_set, True),
    'ik_active': (char_ik_active, False),
    'ik_set': (char_ik_set, True),
    'voice_lst': (char_voice_lst, False),
    'voice_rpt': (char_voice_rpt, False),
    'visible': (char_visible, False),
    'shoes': (char_shoes, False),


    'ext_curclothcoord': (char_ext_curclothcoord, False),
    'ext_curclothcoordnoacc': (char_ext_curclothcoordnoacc, False),
    'ext_bodyshapes': (char_ext_bodyshapes, True),
    'ext_faceshapes': (char_ext_faceshapes, True),
    'pl_hspedata': (char_pl_hspedata, False),
    'pl_kkpedata': (char_pl_kkpedata, False),
    'pl_aipedata': (char_pl_aipedata, False),
}

#===============================================================================================
# prop action wrapper functions
# All scripts: func(prop, param)
def prop_visible(prop, param):
    # param = 0(hide)/1(show)
    prop.visible = param

def prop_move(prop, param):
    # param = (pos_delta_x, pos_delta_y, pos_delta_z)
    cp = prop.pos
    ncp = Vector3(cp.x + param[0], cp.y + param[1], cp.z + param[2])
    prop.move(pos = ncp)

def prop_move_to(prop, param):
    # param = (pos_x, pos_y, pos_z) or Vector3
    if isinstance(param, Vector3):
        ncp = param
    else:
        ncp = Vector3(param[0], param[1], param[2])
    prop.move(pos = ncp)

def prop_rotate(prop, param):
    # param = (rot_delta_x, rot_delta_y, rot_delta_z)
    rt = prop.rot
    nrt = Vector3(rt.x + param[0], rt.y + param[1], rt.z + param[2])
    prop.move(rot = nrt)

def prop_rotate_to(prop, param):
    # param = (rot_x, rot_y, rot_z) or Vector3
    if isinstance(param, Vector3):
        nrt = param
    else:
        nrt = Vector3(param[0], param[1], param[2])
    prop.move(rot = nrt)

def prop_scale_to(prop, param):
    # param = (scale_x, scale_y, scale_z) or Vector3 or scale
    if isinstance(param, tuple):
        nsl = Vector3(param[0], param[1], param[2])
    elif isinstance(param, Vector3):
        nsl = param
    else:
        nsl = Vector3(param, param, param)
    prop.move(scale = nsl)

def prop_color_neo(prop, param):
    # param = ((Color, Color, float, float), (color, color, float, foat)) or ((Color, Color, float, float),) or (Color, Color, float, float), where Color can be (r,g,b) or (r,g,b,a)
    try:
        if isinstance(param, tuple) and len(param) in (1,2) and isinstance(param[0], tuple) and isinstance(param[0][0], Color):
            # maybe format ((Color, Color, float, float), (color, color, float, foat))
            prop.set_color(param)
        elif isinstance(param, tuple) and len(param) in (1,2) and isinstance(param[0], tuple) and isinstance(param[0][0], tuple):
            # maybe format ((Color, Color, float, float), (color, color, float, foat)) where Color is in tuple
            colLst = []
            for pc in param:
                if len(pc[0]) == 3:
                    col1 = Color(pc[0][0], pc[0][1], pc[0][2])
                else:
                    col1 = Color(pc[0][0], pc[0][1], pc[0][2], pc[0][3])
                if len(pc[1]) == 3:
                    col2 = Color(pc[1][0], pc[1][1], pc[1][2])
                else:
                    col2 = Color(pc[1][0], pc[1][1], pc[1][2], pc[1][3])
                colLst.append((col1, col2, pc[2], pc[3]))
            prop.set_color(tuple(colLst))
        elif isinstance(param, tuple) and len(param) == 4:
            if isinstance(param[0], Color):
                col1 = param[0]
            elif len(param[0]) == 3:
                col1 = Color(param[0][0], param[0][1], param[0][2])
            else:
                col1 = Color(param[0][0], param[0][1], param[0][2], param[0][3])
            if isinstance(param[1], Color):
                col2 = param[1]
            elif len(param[1]) == 3:
                col2 = Color(param[1][0], param[1][1], param[1][2])
            else:
                col2 = Color(param[1][0], param[1][1], param[1][2], param[1][3])
            prop.set_color(((col1, col2, param[2], param[3]),))
        else:
            raise Exception("Unknown format.")
    except Exception as e:
        print "prop_color param format error:", e

def prop_color_charastudio(prop, param):
    # param = ((R, G, B, A), (R, G, B, A), ...) or ((R, G, B), (R, G, B), ...) or (R, G, B) or (R, G, B, A) or (Color, Color, ...) or Color
    clist = []
    if isinstance(param, Color):
        clist.append(param)
    elif isinstance(param[0], Color):
        for subc in param:
            clist.append(subc)
    elif isinstance(param[0], tuple):
        for subc in param:
            if len(subc) == 4:
                ncolor = Color(subc[0], subc[1], subc[2], subc[3])
            else:
                ncolor = Color(subc[0], subc[1], subc[2])
            clist.append(ncolor)
    else:
        if len(param) == 4:
            ncolor = Color(param[0], param[1], param[2], param[3])
        else:
            ncolor = Color(param[0], param[1], param[2])
        clist.append(ncolor)
    prop.set_color(tuple(clist))

def prop_color(prop, param):
    # param depend on engine. Try use prop's set_color first. If not fit, use engine depends function
    try:
        prop.set_color(param)
    except:
        if isinstance(prop, PropCharaStudio):
            prop_color_charastudio(prop, param)
        else:
            prop_color_neo(prop, param)

def prop_pattern(prop, param):
    # param: a set of ((key, filepath, clamp), (key, filepath, clamp), (key, filepath, clamp))
    prop.set_pattern(param)

def prop_pattern_detail(prop, param):
    # param: a set of ((color, ut, vt, us, vs, rot), (color, ut, vt, us, vs, rot), (color, ut, vt, us, vs, rot))
    prop.set_pattern_detail(param)
    
def prop_panel(prop, param):
    # param: a set of (filepath, clamp)
    prop.set_panel(param)

def prop_panel_detail(prop, param):
    # param: a set of (color, ut, vt, us, vs, rot)
    prop.set_panel_detail(param)
    
def prop_metallic(prop, param):
    # param: a list of ((metallic, glossiness), (metallic, glossiness), ...)
    prop.set_metallic(param)

def prop_emission(prop, param):
    # param: (color, power)
    prop.set_emission(param)

def prop_alpha(prop, param):
    # param = 0~1
    prop.set_alpha(param)

def prop_line(prop, param):
    # param: (color, width)
    prop.set_line(param)

def prop_shadow_color(prop, param):
    # param: shadow color
    prop.set_shadow_color(param)

def prop_light_cancel(prop, param):
    # param: light cancel
    prop.set_light_cancel(param)

def prop_option(prop, param):
    # param = 0(hide)/1(show)
    prop.set_option(param)

def prop_fk_enable(prop, param):
    # param = 0/1
    prop.set_fk_enable(param)

def prop_fk_set(prop, param):
    # param: a list/tuple of Vector3 or tuple(3), as the rot of prop's FK bone
    prop.import_fk_bone_info(param)

def prop_dynamicbone_enable(prop, param):
    # param: 0/1
    prop.set_dynamicbone_enable(param)
    
def prop_anime_speed(prop, param):
    # param = speed (0~3)
    prop.set_anime_speed(param)

def prop_anime_pattern(prop, param):
    # param = pattern index
    prop.set_anime_pattern(param)

# lighting
def prop_enable(prop, param):
    # param = 0(hide)/1(show)
    prop.set_enable(param)

def prop_intensity(prop, param):
    prop.set_intensity(param)

def prop_shadow(prop, param):
    prop.set_shadow(param)

def prop_angle(prop, param):
    prop.set_angle(param)

def prop_range(prop, param):
    prop.set_range(param)

# route
def prop_route(prop, param):
    prop.set_route_full(param)
    
prop_act_funcs = {
    'visible': (prop_visible, False),
    'move': (prop_move, False),
    'move_to': (prop_move_to, True),
    'rotate': (prop_rotate, False),
    'rotate_to': (prop_rotate_to, True),
    'scale_to': (prop_scale_to, True),
    'color_neo' : (prop_color_neo, True),
    'color_cs' : (prop_color_charastudio, True),
    'color' : (prop_color, True),
    'ptn_set': (prop_pattern, False),
    'ptn_dtl': (prop_pattern_detail, True),
    'pnl_set': (prop_panel, False),
    'pnl_dtl': (prop_panel_detail, True),    
    'metallic' : (prop_metallic, True),
    'emission' : (prop_emission, True),
    'alpha' : (prop_alpha, True),
    'line': (prop_line, True),
    'shadow_c': (prop_shadow_color, True),
    'light_cancel': (prop_light_cancel, True),
    'option' : (prop_option, False),
    'fk_active' : (prop_fk_enable, False),
    'fk_set' : (prop_fk_set, True),
    'db_active' : (prop_dynamicbone_enable, False),
    'anim_spd': (prop_anime_speed, True),
    'anim_ptn': (prop_anime_pattern, False),
    # for light only
    'enable': (prop_enable, False),
    'intensity': (prop_intensity, True),
    'shadow': (prop_shadow, False),
    'range': (prop_range, True),
    'angle': (prop_angle, True),
    # for route only
    'route_p': (prop_route, False),
    'route_f': (prop_route, False),
}

#===============================================================================================
# system action wrapper functions
# All scripts: func(game, param)
def sys_idle(game, param = None):
    # as name says, do nothing, using in anime to wait, param ignored
    return
    
def sys_next(game, param = None):
    # the same as click next, param ignored
    game.NextText(game)
    
def sys_skip(game, param):
    # skip some steps, param: steps to skip, should be > 0
    for i in range(param):
        game.nextTexts.pop(0)
    
def sys_branch(game, param):
    # start a select scene: param = ([button1, button2, ...], [func1, func2, ...])
    # if use int in func(n), will call the sys_branch_skip by skip(n)
    funclist = []
    for f in param[1]:
        if isinstance(f, int):
            funclist.append((sys_branch_skip, f))
        else:
            funclist.append(f)
    game.set_buttons(param[0], funclist)
    
def sys_branch_skip(game, param):
    # skip some steps, param: steps to skip, should be >= 0. if param == 0 skip to next, just like sys_next()
    # function in step will be ignored
    if len(game.nextTexts) > param:
        #game.NextText(game) get target and run it
        skptgt = game.nextTexts[param]
        #print "skip to ['%s', '%s']"%(skptgt[0], skptgt[1])
        game.set_text(skptgt[0], skptgt[1])
        game.set_buttons([game.btnNextText], [game.NextText])
        if(len(skptgt) > 2):
            func = skptgt[2]
            func(game, skptgt[3])
        # pop skipped one
        for i in range(param + 1):
            game.nextTexts.pop(0)
    else:
        raise Exception("sys_branch_skip: unable to skip %d steps when only %d steps in queue!"%(param, len(game.nextTexts)))
        
def sys_set_variable(game, param):
    # set some variables in act script, param = (variable, key, value) or (variable, value)
    # variable must be a mutable obj such like list and dict
    # if key is omitted, function set all values in 'variable' so make sure 'value' is a list or dict just like 'variable'
    if len(param) == 2:
        if isinstance(param[0], list):
            for i in range(len(param[0])):
                param[0][i] = param[1][i]
        if isinstance(param[0], dict):
            for k in param[0].Keys:
                param[0][k] = param[1][k]
    elif len(param) == 3:
        param[0][param[1]] = param[2]
    else:
        raise Exception("sys_set_variable format error: " + str(param))
        
def sys_visible(game, param):
    # param = 0(hide)/1(show)
    game.visible = param
    
def sys_lock(game, param):
    # param = 0(unlock)/1(lock)
    game.isHideGameButtons = param

def sys_text(game, param):
    # param = (char, text)
    game.set_text(param[0], param[1])
    
def sys_lipsync(game, param):
    # param = 0(disable)/1(enable)
    game.isfAutoLipSync = param
    
def sys_btn_next(game, param = "Next >>"):
    # param = "next button text"
    #game.btnNextText = param
    game.set_buttons([param],[game.NextText])

def sys_wait_anime(game, param):
    # wait anime of actor play once: param = actorID
    # return True if anime is over or actor not found
    actor = game.scenef_get_actor(param)
    if actor != None:
        return actor.isAnimeOver
    else:
        return True
        
def sys_wait_voice(game, param):
    # wait voice of actor over: param = actorID
    # return True if voice is over or actor not found
    actor = game.scenef_get_actor(param)
    if actor != None:
        return not actor.isVoicePlay
    else:
        return True
    
def sys_bgm(game, param):
    # set bgm, param = (bgm no, play)
    if game.studio.bgmCtrl.no != param[0]:
        game.studio.bgmCtrl.Play(param[0])
    if game.studio.bgmCtrl.play != bool(param[1]):
        if param[1]:
            game.studio.bgmCtrl.Play()
        else:
            game.studio.bgmCtrl.Stop()

def sys_env(game, param):
    # set evn sound, param = (evn no, play), StudioNeo only
    if game.isStudioNEO:
        if game.studio.envCtrl.no != param[0]:
            game.studio.envCtrl.Play(param[0])
        if game.studio.envCtrl.play != bool(param[1]):
            if param[1]:
                game.studio.envCtrl.Play()
            else:
                game.studio.envCtrl.Stop()
    else:
        print "sys_env only supports HoneySelect Studio Neo"

def sys_wav(game, param):
    # set outside wav sound, param = (wav file, play, repeat)
    from os import path
    from UnityEngine import Application
    from Studio import BGMCtrl
    wavName = param[0].strip()
    if wavName != "":
        if not wavName.lower().endswith(".wav"):
            wavName += ".wav"
        # load wav in game scene folder if existed
        wavInScene = path.join(game.get_scene_dir(), game.sceneDir, wavName)
        if path.isfile(wavInScene):
            if game.isStudioNEO:
                wavRevPath = path.join('..', 'studioneo', 'scene', game.sceneDir, wavName)
            else:
                wavRevPath = path.join('..', 'studio', 'scene', game.sceneDir, wavName)
            if game.studio.outsideSoundCtrl.fileName != wavRevPath:
                game.studio.outsideSoundCtrl.Play(wavRevPath)
        else:
            # load wav in game default audio folder if existed
            wavInDefault = path.realpath(path.join(Application.dataPath,'..','UserData','audio',wavName))
            if path.isfile(wavInDefault):
                if game.studio.outsideSoundCtrl.fileName != wavName:
                    game.studio.outsideSoundCtrl.Play(wavName)
    if game.studio.outsideSoundCtrl.play != bool(param[1]) or wavName == "":
        if bool(param[1]):
            game.studio.outsideSoundCtrl.Play()
        else:
            game.studio.outsideSoundCtrl.Stop()
    if bool(param[2]):
        game.studio.outsideSoundCtrl.repeat = BGMCtrl.Repeat.All
    else:
        game.studio.outsideSoundCtrl.repeat = BGMCtrl.Repeat.None

def sys_map(game, param):
    # set map
    if hasattr(game.studio_scene, "map"):
        if param != game.studio_scene.map:
            if game.isCharaStudio:
                game.change_map_to(param)
            else:
                game.studio.AddMap(param)
    elif hasattr(game.studio_scene, "mapInfo"):
        if param != game.studio_scene.mapInfo.no:
            game.studio.AddMap(param, False, False, False)
            
def sys_map_pos(game, param):
    # set map pos: param = Vector3 or (x, y, z)
    if isinstance(param, tuple):
        param = Vector3(param[0], param[1], param[2])
    if hasattr(game.studio_scene, "caMap"):
        game.studio_scene.caMap.pos = param
    elif hasattr(game.studio_scene, "mapInfo"):
        game.studio_scene.mapInfo.ca.pos = param

def sys_map_rot(game, param):
    # set map rot: param = Vector3 or (x, y, z)
    if isinstance(param, tuple):
        param = Vector3(param[0], param[1], param[2])
    if hasattr(game.studio_scene, "caMap"):
        game.studio_scene.caMap.rot = param
    elif hasattr(game.studio_scene, "mapInfo"):
        game.studio_scene.mapInfo.ca.rot = param
    
def sys_map_sun(game, param):
    # set sunLightType, param = sunLightType index, CharaStudio only
    if game.isCharaStudio:
        from Studio import Map
        from SunLightInfo import Info
        st = (Info.Type.DayTime, Info.Type.Evening, Info.Type.Night)
        map = Map.Instance
        map.sunType = st[param]
    else:
        print "sys_map_sun only supports CharaStudio"

def sys_map_option(game, param):
    # set map option visible: param = 1/0
    if game.isCharaStudio:
        from Studio import Map
        map = Map.Instance
        map.visibleOption = bool(param)
    if game.isNEOV2:
        from Studio import Map
        map = Map.Instance
        map.VisibleOption = bool(param)
    else:
        print "sys_map_option only supports StudioNEOV2"

def sys_map_light(game, param):
    # set map light visible: param = 1/0
    if game.isNEOV2:
        from Studio import Map
        map = Map.Instance
        map.VisibleLight = bool(param)
    else:
        print "sys_map_option only supports VisibleLight"


def sys_skybox(game, param):
    # set sky box, param = sky box index, Playhome only
    if game.isPlayHomeStudio:
        game.studio.AddSkybox(param)
    else:
        print "sys_skybox only supports PlayHome Studio"
    
def sys_bg_png(game, param = ""):
    # set background png, param = png file name
    from os import path
    from UnityEngine import Application
    pngName = param.strip()
    if pngName != "":
        if not pngName.lower().endswith(".png"):
            pngName += ".png"
        # load png in game scene folder if existed
        pngInScene = path.join(game.get_scene_dir(), game.sceneDir, pngName)
        if path.isfile(pngInScene):
            game.scene_set_bg_png(pngName)
            return
        # load png in game default background folder if existed
        if game.isCharaStudio or game.isNEOV2:
            pngInDefault = path.realpath(path.join(Application.dataPath,'..','UserData','bg',pngName))
        else:
            pngInDefault = path.realpath(path.join(Application.dataPath,'..','UserData','background',pngName))
        if path.isfile(pngInDefault):
            game.scene_set_bg_png_orig(pngName)
            return
    # remove if param == "" or file not existed
    game.scene_set_bg_png_orig("")
    
def sys_fm_png(game, param = ""):
    # set frame png, param = png file name, CharaStudio only
    if game.isCharaStudio or game.isNEOV2:
        from os import path
        from UnityEngine import Application
        pngName = param.strip()
        if pngName != "":
            if not pngName.lower().endswith(".png"):
                pngName += ".png"
            # load png in game scene folder if existed
            pngInScene = path.join(game.get_scene_dir(), game.sceneDir, pngName)
            if path.isfile(pngInScene):
                pngRevPath = path.join('..', 'studio', 'scene', game.sceneDir, pngName)
                game.scene_set_framefile(pngRevPath)
                return
            # load png in game default background folder if existed
            pngInDefault = path.realpath(path.join(Application.dataPath,'..','UserData','frame',pngName))
            if path.isfile(pngInDefault):
                game.scene_set_framefile(pngName)
                return
        # remove if param == "" or file not existed
        game.scene_set_framefile("")
    else:
        print "sys_fm_png only supports CharaStudio"

def sys_char_light(game, param):
    # set chara light
    # param for HS, KK, AI = (color, intensity, rot_y, rot_x, shadow)
    # param for PH = (color, intensity, rot_y, rot_x, shadow, method)
    if game.isStudioNEO:
        sc = game.studio_scene
        sc.cameraLightColor.SetDiffuseRGB(tuple4_2_color(param[0]))
        sc.cameraLightIntensity = param[1]
        sc.cameraLightRot[0] = param[2]
        sc.cameraLightRot[1] = param[3]
        sc.cameraLightShadow = param[4]
        game.studio.cameraLightCtrl.Reflect()
    elif game.isPlayHomeStudio:
        sc = game.studio_scene
        sc.cameraLightColor = tuple4_2_color(param[0])
        sc.cameraLightIntensity = param[1]
        sc.cameraLightRot[0] = param[2]
        sc.cameraLightRot[1] = param[3]
        sc.cameraLightShadow = param[4]
        sc.cameraMethod = param[5]
        game.studio.cameraLightCtrl.Reflect()
    elif game.isCharaStudio or game.isNEOV2:
        cl = game.studio_scene.charaLight
        cl.color = tuple4_2_color(param[0])
        cl.intensity = param[1]
        cl.rot[0] = param[2]
        cl.rot[1] = param[3]
        cl.shadow = param[4]
        game.studio.cameraLightCtrl.Reflect()
    else:
        pass

def sys_pl_neoextsave(game, param):
    # HSStudioNEOExtSave plugin - for HSNeoAdvAddon
    import extplugins
    if extplugins.ExtPlugin.exists("HSStudioNEOExtSave"):
        pl_neoext = extplugins.HSStudioNEOExtSave()
        pl_neoext.ExtDataSet(param)
    else:
        print "this require HSStudioNEOExtSave plugin"

def sys_pl_nodescon(game, param):
    # NodesConstraints
    import extplugins
    if extplugins.ExtPlugin.exists("NodesConstraints"):
        pl_neoext = extplugins.NodesConstraints()
        pl_neoext.SetSysSettingsText(param)
    else:
        print "this require NodesConstraints plugin"

def sys_pl_dhh(game, param):
    # DHH
    import extplugins
    if game.isNEOV2 and extplugins.ExtPlugin.exists("DHH_AI4"):
        pl_dhh = extplugins.DHH_AI()
        pl_dhh.setEnable(param[0])
        pl_dhh.importGraphSetting(param[1])
    else:
        print "this require DHH_AI4 (for AI) plugin"

def export_sys_status(game):
    # export a dict contains all system status
    #from Studio import Studio
    #studio = Studio.Instance

    """:type game: vngameengine.VNNeoController"""

    from Studio import BGMCtrl
    fs = {}
    fs["bgm"] = (game.studio.bgmCtrl.no, game.studio.bgmCtrl.play)
    if game.isStudioNEO:
        fs["env"] = (game.studio.envCtrl.no, game.studio.envCtrl.play)
    fs["wav"] = (game.studio.outsideSoundCtrl.fileName, game.studio.outsideSoundCtrl.play, game.studio.outsideSoundCtrl.repeat == BGMCtrl.Repeat.All)
    ''''''
    if hasattr(game.studio_scene, "map"):
    	# HS/PH/KK/AI
        fs["map"] = game.studio_scene.map
        fs["map_pos"] = game.studio_scene.caMap.pos
        fs["map_rot"] = game.studio_scene.caMap.rot
        if game.isCharaStudio:
            fs["map_sun"] = game.studio_scene.sunLightType
        if game.isCharaStudio or game.isNEOV2:
            fs["map_opt"] = game.studio_scene.mapOption
    elif hasattr(game.studio_scene, "mapInfo"):
    	# AI/HS2
        fs["map"] = game.studio_scene.mapInfo.no
        fs["map_pos"] = game.studio_scene.mapInfo.ca.pos
        fs["map_rot"] = game.studio_scene.mapInfo.ca.rot
        fs["map_light"] = game.studio_scene.mapInfo.light
        fs["map_opt"] = game.studio_scene.mapInfo.option

    if game.isPlayHomeStudio:
        fs["skybox"] = game.studio_scene.skybox
    fs["bg_png"] = game.scene_get_bg_png_orig()
    if game.isCharaStudio or game.isNEOV2:
        fs["fm_png"] = game.scene_get_framefile()
    if game.isStudioNEO:
        sc = game.studio_scene
        fs["char_light"] = (sc.cameraLightColor.rgbDiffuse, sc.cameraLightIntensity, sc.cameraLightRot[0], sc.cameraLightRot[1], sc.cameraLightShadow)
    elif game.isPlayHomeStudio:
        sc = game.studio_scene
        fs["char_light"] = (sc.cameraLightColor, sc.cameraLightIntensity, sc.cameraLightRot[0], sc.cameraLightRot[1], sc.cameraLightShadow, sc.cameraMethod)
    elif game.isCharaStudio or game.isNEOV2:
        cl = game.studio_scene.charaLight
        fs["char_light"] = (cl.color, cl.intensity, cl.rot[0], cl.rot[1], cl.shadow)

    # external plugins data
    import extplugins
    if game.isStudioNEO:
        if extplugins.ExtPlugin.exists("HSStudioNEOExtSave"):
            if is_ini_value_true("ExportSys_NeoExtSave"):
                pl_neoext = extplugins.HSStudioNEOExtSave()
                fs["pl_neoextsave"] = pl_neoext.ExtDataGet()

    if game.isStudioNEO or game.isCharaStudio or game.isNEOV2:
        if extplugins.ExtPlugin.exists("NodesConstraints"):
            if is_ini_value_true("ExportSys_NodesConstraints"):
                pl_nodescon = extplugins.NodesConstraints()
                fs["pl_nodescon"] = pl_nodescon.GetSysSettingsText()

    if game.isNEOV2:
        if extplugins.ExtPlugin.exists("DHH_AI4"):
            if is_ini_value_true("ExportSys_DHH"):
                pl_dhh = extplugins.DHH_AI()
                fs["pl_dhh"] = (pl_dhh.getEnable(), pl_dhh.exportGraphSetting())

    #print fs
    return fs

sys_act_funcs = {
    'idle': (sys_idle, True),
    'next': (sys_next, False),
    'skip': (sys_skip, False),
    'branch': (sys_branch, False),
    'set_vari': (sys_set_variable, False),
    'visible': (sys_visible, False),
    'lock': (sys_lock, False),
    'text': (sys_text, False),
    'lipsync': (sys_lipsync, False),
    'btn_next': (sys_btn_next, False),
    'wait_anime': (sys_wait_anime, True),
    'wait_voice': (sys_wait_voice, True),
    'bgm': (sys_bgm, False),
    'env': (sys_env, False),
    'wav': (sys_wav, False),
    'map': (sys_map, False),
    'map_pos': (sys_map_pos, True),
    'map_rot': (sys_map_rot, True),
    'map_sun': (sys_map_sun, False),
    'map_opt': (sys_map_option, False),
    'map_light': (sys_map_light, False),
    'skybox': (sys_skybox, False),
    'bg_png': (sys_bg_png, False),
    'fm_png': (sys_fm_png, False),
    'char_light': (sys_char_light, False),

    'pl_neoextsave': (sys_pl_neoextsave, False),
    'pl_nodescon': (sys_pl_nodescon, False),
    'pl_dhh': (sys_pl_dhh, False),
}

def get_hanime_group_names(game):
    if game.isStudioNEO:
        return ActorHSNeo.get_hanime_group_names()
    elif game.isPlayHomeStudio:
        return ActorPHStudio.get_hanime_group_names()
    elif game.isCharaStudio:
        return ActorCharaStudio.get_hanime_group_names()
    elif game.isNEOV2:
        return ActorNeoV2.get_hanime_group_names()
    else:
        raise Exception("Classic studio not supported!")
        
def get_hanime_category_names(game, group):
    if game.isStudioNEO:
        return ActorHSNeo.get_hanime_category_names(group)
    elif game.isPlayHomeStudio:
        return ActorPHStudio.get_hanime_category_names(group)
    elif game.isCharaStudio:
        return ActorCharaStudio.get_hanime_category_names(group)
    elif game.isNEOV2:
        return ActorNeoV2.get_hanime_category_names(group)
    else:
        raise Exception("Classic studio not supported!")

def get_hanime_no_names(game, group, category):
    if game.isStudioNEO:
        return ActorHSNeo.get_hanime_no_names(group, category)
    elif game.isPlayHomeStudio:
        return ActorPHStudio.get_hanime_no_names(group, category)
    elif game.isCharaStudio:
        return ActorCharaStudio.get_hanime_no_names(group, category)
    elif game.isNEOV2:
        return ActorNeoV2.get_hanime_no_names(group, category)
    else:
        raise Exception("Classic studio not supported!")

# ----- support functions ----------
def bytearray_to_list(ba):
    ar = []
    for i in ba:
        ar.append(i)
    return ar

def list_to_bytearray(list):
    from System import Array, Byte
    #return Array[Byte]([Byte(i) for i in list])
    #return Array[Byte](list)

    from System.IO import MemoryStream, BinaryWriter
    
    #print bytearray(list)
    memoryStream = MemoryStream()
    binaryWriter = BinaryWriter(memoryStream)
    for i in list:
        #binaryWriter.Write(bytes([i]))
        #binaryWriter.Write(str(i).encode())
        binaryWriter.Write(Byte(i))

    #binaryWriter.Write(list[0])
    binaryWriter.Close()
    memoryStream.Close()
    return memoryStream.ToArray()


def bytearray_to_str64(ba):
    from System import Convert
    res = Convert.ToBase64String(ba, 0, ba.Length)
    #print res
    return res


def str64_to_bytearray(str):
    from System import Array, Byte
    from System import Convert
    return Convert.FromBase64String(str)
    # return Array[Byte]([Byte(i) for i in list])
    # return Array[Byte](list)

def str_to_bytearray(str):
    import System
    result = System.Text.Encoding.UTF8.GetBytes(str)
    return result

def bytearray_to_str(ba):
    import System
    result = System.Text.Encoding.UTF8.GetString(ba);
    return result

def tuple4_2_color(param):
    # utility for color
    if isinstance(param, tuple) and len(param) == 4:
        return Color(param[0], param[1], param[2], param[3])
    elif isinstance(param, Color):
        return param
    else:
        raise Exception("Can not transform '%s' to UnityEngine.Color"%str(param))

def tuple3_2_vector3(param):
    # utility for Vector3
    if (isinstance(param, tuple) or isinstance(param, list)) and len(param) == 3:
        return Vector3(param[0], param[1], param[2])
    elif isinstance(param, Vector3):
        return param
    else:
        raise Exception("Can not transform '%s' to UnityEngine.Vector3"%str(param))

def value_2_enum(enum, value):
    # convert value to enum
    for ei in enum.GetValues(enum):
        if ei.value__ == value:
            return ei
    raise Exception("Can not convert '%d' to %s"%(value, str(enum)))

# ini file

_iniOptions = None
_iniTranslation = None
_iniExportOptDesp = None

def load_ini_file(forceReload = False):
    global _iniOptions
    global _iniTranslation
    global _iniExportOptDesp
    if forceReload or _iniOptions == None or _iniTranslation == None or _iniExportOptDesp == None:
        # load only needed
        _iniOptions = {}
        _iniTranslation = {}
        _iniExportOptDesp = {}

        import ConfigParser, sys, os.path
        config = ConfigParser.SafeConfigParser()
        config.read(os.path.splitext(__file__)[0] + '.ini')

        # option for current engine
        from vngameengine import get_engine_id
        engineid = get_engine_id()
        for k, v in config.items(engineid):
            _iniOptions[k.lower()] = v
        #print _iniOptions

        # translation strings for all engine
        for k, v in config.items("Translation"):
            _iniTranslation[k.lower()] = v
        
        # description strings for all engine
        for k, v in config.items("ExportOptionDescription"):
            _iniExportOptDesp[k.lower()] = v
    else:
        # already parsed
        pass

def get_ini_value(elem): # get ini value for cur engine
    global _iniOptions
    load_ini_file()

    # main code
    elemlower = elem.lower()
    if elemlower in _iniOptions:
        return _iniOptions[elemlower]

    return None

def is_ini_value_true(elem):
    val = get_ini_value(elem)
    if val != None and val != 0 and val != "0":
        return True
    return False

def set_ini_value(elem, val):
    global _iniOptions
    if is_ini_value_true(elem) != val:
        elemlower = elem.lower()
        _iniOptions[elemlower] = "1" if val else "0"

def get_ini_options():
    global _iniOptions
    load_ini_file()
    # return all keys
    return sorted(_iniOptions.keys())

def get_ini_translation(elem): # get ini translation data
    global _iniTranslation
    load_ini_file()

    # main code
    elemlower = elem.lower()
    if elemlower in _iniTranslation:
        return _iniTranslation[elemlower]

    return None

def get_ini_exportOptionDesp(elem): # get ini export option description
    global _iniExportOptDesp
    load_ini_file()

    # main code
    elemlower = elem.lower()
    if elemlower in _iniExportOptDesp:
        return _iniExportOptDesp[elemlower]

    return None