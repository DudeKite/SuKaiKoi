# ChaControl.cs
class ChaControl():
    def __init__(self):
        self.texInnerAlphaMask = None # Texture texInnerAlphaMask
        """:type : Texture"""
        self.dictBustNormal = None # Dictionary<BustNormalKind, BustNormal> dictBustNormal
        """:type : Dictionary<BustNormalKind, BustNormal>"""
        self.enableExpression = None # bool enableExpression
        """:type : bool"""
        self.nowCoordinate = None # ChaFileCoordinate nowCoordinate
        """:type : ChaFileCoordinate"""
        self.notBra = None # bool notBra
        """:type : bool"""
        self.notBot = None # bool notBot
        """:type : bool"""
        self.notShorts = None # bool notShorts
        """:type : bool"""
        self.hideHairAcs = None # bool[] hideHairAcs
        """:type : bool[]"""
        self.isChangeOfClothesRandom = None # bool isChangeOfClothesRandom
        """:type : bool"""
        self.dictStateType = None # Dictionary<int, Dictionary<byte, string>> dictStateType
        """:type : Dictionary<int, Dictionary<byte, string>>"""
        self.bustSoft = None # BustSoft bustSoft
        """:type : BustSoft"""
        self.bustGravity = None # BustGravity bustGravity
        """:type : BustGravity"""
        self.updateCMFaceTex = None # bool[] updateCMFaceTex
        """:type : bool[]"""
        self.updateCMFaceColor = None # bool[] updateCMFaceColor
        """:type : bool[]"""
        self.updateCMFaceLayout = None # bool[] updateCMFaceLayout
        """:type : bool[]"""
        self.updateCMBodyTex = None # bool[] updateCMBodyTex
        """:type : bool[]"""
        self.updateCMBodyColor = None # bool[] updateCMBodyColor
        """:type : bool[]"""
        self.updateCMBodyLayout = None # bool[] updateCMBodyLayout
        """:type : bool[]"""
        self.asVoice = None # AudioSource asVoice
        """:type : AudioSource"""
        self.tearsLv = None # byte tearsLv
        """:type : byte"""
    def Initialize(self, _sex, _hiPoly, _objRoot, _id, _no, _chaFile):
        """
        :type _sex: byte
        :type _hiPoly:  bool
        :type _objRoot:  GameObject
        :type _id:  int
        :type _no:  int
        :type _chaFile:  ChaFileControl
        """
        # void Initialize(byte _sex, bool _hiPoly, GameObject _objRoot, int _id, int _no, ChaFileControl _chaFile = null)
        pass

    def ReleaseAll(self):
        # void ReleaseAll()
        pass

    def ReleaseObject(self):
        # void ReleaseObject()
        pass

    def LoadPreset(self, _sex, presetName):
        """
        :type _sex: int
        :type presetName:  string
        """
        # void LoadPreset(int _sex, string presetName = "")
        pass

    def LoadPresetDemo(self, type):
        """
        :type type: int
        """
        # void LoadPresetDemo(int type)
        pass

    def AssignDefaultCoordinate(self):
        # bool AssignDefaultCoordinate()
        pass

    def AssignDefaultCoordinate(self, chaFile):
        """
        :type chaFile: ChaFileControl
        """
        # static bool AssignDefaultCoordinate(ChaFileControl chaFile)
        pass

    def GetRandomFemaleCard(self, num):
        """
        :type num: int
        """
        # static ChaFileControl[] GetRandomFemaleCard(int num)
        pass

    def SetActiveTop(self, active):
        """
        :type active: bool
        """
        # void SetActiveTop(bool active)
        pass

    def GetActiveTop(self):
        # bool GetActiveTop()
        pass

    def SetPosition(self, x, y, z):
        """
        :type x: float
        :type y:  float
        :type z:  float
        """
        # void SetPosition(float x, float y, float z)
        pass

    def SetPosition(self, pos):
        """
        :type pos: Vector3
        """
        # void SetPosition(Vector3 pos)
        pass

    def GetPosition(self):
        # Vector3 GetPosition()
        pass

    def SetRotation(self, x, y, z):
        """
        :type x: float
        :type y:  float
        :type z:  float
        """
        # void SetRotation(float x, float y, float z)
        pass

    def SetRotation(self, rot):
        """
        :type rot: Vector3
        """
        # void SetRotation(Vector3 rot)
        pass

    def GetRotation(self):
        # Vector3 GetRotation()
        pass

    def SetTransform(self, trf):
        """
        :type trf: Transform
        """
        # void SetTransform(Transform trf)
        pass

    def ChangeSettingMannequin(self, mannequin):
        """
        :type mannequin: bool
        """
        # void ChangeSettingMannequin(bool mannequin)
        pass

    def RestoreMannequinHair(self):
        # void RestoreMannequinHair()
        pass

    def OnDestroy(self):
        # void OnDestroy()
        pass

    def UpdateForce(self):
        # void UpdateForce()
        pass

    def LateUpdateForce(self):
        # void LateUpdateForce()
        pass

    def LoadAnimation(self, assetBundleName, assetName, manifestName):
        """
        :type assetBundleName: string
        :type assetName:  string
        :type manifestName:  string
        """
        # RuntimeAnimatorController LoadAnimation(string assetBundleName, string assetName, string manifestName = "")
        pass

    def AnimPlay(self, stateName):
        """
        :type stateName: string
        """
        # void AnimPlay(string stateName)
        pass

    def getAnimatorStateInfo(self, _nLayer):
        """
        :type _nLayer: int
        """
        # AnimatorStateInfo getAnimatorStateInfo(int _nLayer)
        pass

    def syncPlay(self, _syncState, _nLayer):
        """
        :type _syncState: AnimatorStateInfo
        :type _nLayer:  int
        """
        # bool syncPlay(AnimatorStateInfo _syncState, int _nLayer)
        pass

    def syncPlay(self, _nameHash, _nLayer, _fnormalizedTime):
        """
        :type _nameHash: int
        :type _nLayer:  int
        :type _fnormalizedTime:  float
        """
        # bool syncPlay(int _nameHash, int _nLayer, float _fnormalizedTime)
        pass

    def syncPlay(self, _strameHash, _nLayer, _fnormalizedTime):
        """
        :type _strameHash: string
        :type _nLayer:  int
        :type _fnormalizedTime:  float
        """
        # bool syncPlay(string _strameHash, int _nLayer, float _fnormalizedTime)
        pass

    def setLayerWeight(self, _fWeight, _nLayer):
        """
        :type _fWeight: float
        :type _nLayer:  int
        """
        # bool setLayerWeight(float _fWeight, int _nLayer)
        pass

    def setAllLayerWeight(self, _fWeight):
        """
        :type _fWeight: float
        """
        # bool setAllLayerWeight(float _fWeight)
        pass

    def getLayerWeight(self, _nLayer):
        """
        :type _nLayer: int
        """
        # float getLayerWeight(int _nLayer)
        pass

    def setPlay(self, _strAnmName, _nLayer):
        """
        :type _strAnmName: string
        :type _nLayer:  int
        """
        # bool setPlay(string _strAnmName, int _nLayer)
        pass

    def setAnimatorParamTrigger(self, _strAnmName):
        """
        :type _strAnmName: string
        """
        # void setAnimatorParamTrigger(string _strAnmName)
        pass

    def setAnimatorParamResetTrigger(self, _strAnmName):
        """
        :type _strAnmName: string
        """
        # void setAnimatorParamResetTrigger(string _strAnmName)
        pass

    def setAnimatorParamBool(self, _strAnmName, _bFlag):
        """
        :type _strAnmName: string
        :type _bFlag:  bool
        """
        # void setAnimatorParamBool(string _strAnmName, bool _bFlag)
        pass

    def getAnimatorParamBool(self, _strAnmName):
        """
        :type _strAnmName: string
        """
        # bool getAnimatorParamBool(string _strAnmName)
        pass

    def setAnimatorParamFloat(self, _strAnmName, _fValue):
        """
        :type _strAnmName: string
        :type _fValue:  float
        """
        # void setAnimatorParamFloat(string _strAnmName, float _fValue)
        pass

    def setAnimPtnCrossFade(self, _strAnmName, _fBlendTime, _nLayer, _fCrossStateTime):
        """
        :type _strAnmName: string
        :type _fBlendTime:  float
        :type _nLayer:  int
        :type _fCrossStateTime:  float
        """
        # void setAnimPtnCrossFade(string _strAnmName, float _fBlendTime, int _nLayer, float _fCrossStateTime)
        pass

    def isBlend(self, _nLayer):
        """
        :type _nLayer: int
        """
        # bool isBlend(int _nLayer)
        pass

    def IsNextHash(self, _nLayer, _nameHash):
        """
        :type _nLayer: int
        :type _nameHash:  string
        """
        # bool IsNextHash(int _nLayer, string _nameHash)
        pass

    def GetHeightCategory(self):
        # int GetHeightCategory()
        pass

    def GetWaistCategory(self):
        # int GetWaistCategory()
        pass

    def GetBustCategory(self):
        # int GetBustCategory()
        pass

    def ResetDynamicBoneAll(self):
        # void ResetDynamicBoneAll()
        pass

    def getDynamicBoneBust(self, _eArea):
        """
        :type _eArea: DynamicBoneKind
        """
        # DynamicBone_Ver02 getDynamicBoneBust(DynamicBoneKind _eArea)
        pass

    def InitDynamicBoneBust(self):
        # bool InitDynamicBoneBust()
        pass

    def ReSetupDynamicBoneBust(self, _nArea):
        """
        :type _nArea: int
        """
        # bool ReSetupDynamicBoneBust(int _nArea = 0)
        pass

    def playDynamicBoneBust(self, _nArea, _bPlay):
        """
        :type _nArea: int
        :type _bPlay:  bool
        """
        # bool playDynamicBoneBust(int _nArea, bool _bPlay)
        pass

    def playDynamicBoneBust(self, _eArea, _bPlay):
        """
        :type _eArea: DynamicBoneKind
        :type _bPlay:  bool
        """
        # bool playDynamicBoneBust(DynamicBoneKind _eArea, bool _bPlay)
        pass

    def ChangeNipRate(self, rate):
        """
        :type rate: float
        """
        # bool ChangeNipRate(float rate)
        pass

    def ChangeHitBustBlendShapeValue(self, typeSex):
        """
        :type typeSex: byte
        """
        # void ChangeHitBustBlendShapeValue(byte typeSex)
        pass

    def EnableExpressionIndex(self, indexNo, enable):
        """
        :type indexNo: int
        :type enable:  bool
        """
        # void EnableExpressionIndex(int indexNo, bool enable)
        pass

    def EnableExpressionCategory(self, categoryNo, enable):
        """
        :type categoryNo: int
        :type enable:  bool
        """
        # void EnableExpressionCategory(int categoryNo, bool enable)
        pass

    def SetSiruFlags(self, parts, lv):
        """
        :type parts: ChaFileDefine.SiruParts
        :type lv:  byte
        """
        # void SetSiruFlags(ChaFileDefine.SiruParts parts, byte lv)
        pass

    def GetSiruFlags(self, parts):
        """
        :type parts: ChaFileDefine.SiruParts
        """
        # byte GetSiruFlags(ChaFileDefine.SiruParts parts)
        pass

    def ChangeAlphaMask(self, state):
        """
        :type state: params byte[]
        """
        # void ChangeAlphaMask(params byte[] state)
        pass

    def ChangeSimpleBodyDraw(self, drawSimple):
        """
        :type drawSimple: bool
        """
        # void ChangeSimpleBodyDraw(bool drawSimple)
        pass

    def ChangeSimpleBodyColor(self, color):
        """
        :type color: Color
        """
        # void ChangeSimpleBodyColor(Color color)
        pass

    def GetNowClothesType(self):
        # int GetNowClothesType()
        pass

    def IsKokanHide(self):
        # bool IsKokanHide()
        pass

    def AssignCoordinate(self, type, path):
        """
        :type type: ChaFileDefine.CoordinateType
        :type path:  string
        """
        # bool AssignCoordinate(ChaFileDefine.CoordinateType type, string path)
        pass

    def AssignCoordinate(self, type, srcCoorde):
        """
        :type type: ChaFileDefine.CoordinateType
        :type srcCoorde:  ChaFileCoordinate
        """
        # bool AssignCoordinate(ChaFileDefine.CoordinateType type, ChaFileCoordinate srcCoorde)
        pass

    def AssignCoordinate(self, type):
        """
        :type type: ChaFileDefine.CoordinateType
        """
        # bool AssignCoordinate(ChaFileDefine.CoordinateType type)
        pass

    def SetNowCoordinate(self, path):
        """
        :type path: string
        """
        # bool SetNowCoordinate(string path)
        pass

    def SetNowCoordinate(self, srcCoorde):
        """
        :type srcCoorde: ChaFileCoordinate
        """
        # bool SetNowCoordinate(ChaFileCoordinate srcCoorde)
        pass

    def ChangeCoordinateType(self, changeBackCoordinateType):
        """
        :type changeBackCoordinateType: bool
        """
        # bool ChangeCoordinateType(bool changeBackCoordinateType = true)
        pass

    def ChangeCoordinateType(self, type, changeBackCoordinateType):
        """
        :type type: ChaFileDefine.CoordinateType
        :type changeBackCoordinateType:  bool
        """
        # bool ChangeCoordinateType(ChaFileDefine.CoordinateType type, bool changeBackCoordinateType = true)
        pass

    def ChangeCoordinateTypeAndReload(self, changeBackCoordinateType):
        """
        :type changeBackCoordinateType: bool
        """
        # bool ChangeCoordinateTypeAndReload(bool changeBackCoordinateType = true)
        pass

    def ChangeCoordinateTypeAndReload(self, type, changeBackCoordinateType):
        """
        :type type: ChaFileDefine.CoordinateType
        :type changeBackCoordinateType:  bool
        """
        # bool ChangeCoordinateTypeAndReload(ChaFileDefine.CoordinateType type, bool changeBackCoordinateType = true)
        pass

    def AddClothesStateKind(self, clothesKind, stateType):
        """
        :type clothesKind: int
        :type stateType:  string
        """
        # bool AddClothesStateKind(int clothesKind, string stateType)
        pass

    def RemoveClothesStateKind(self, clothesKind):
        """
        :type clothesKind: int
        """
        # void RemoveClothesStateKind(int clothesKind)
        pass

    def IsClothes(self, clothesKind):
        """
        :type clothesKind: int
        """
        # bool IsClothes(int clothesKind)
        pass

    def IsClothesStateKind(self, clothesKind):
        """
        :type clothesKind: int
        """
        # bool IsClothesStateKind(int clothesKind)
        pass

    def IsShoesStateKind(self):
        # bool IsShoesStateKind()
        pass

    def GetClothesStateKind(self, clothesKind):
        """
        :type clothesKind: int
        """
        # Dictionary<byte, string> GetClothesStateKind(int clothesKind)
        pass

    def IsClothesStateType(self, clothesKind, stateType):
        """
        :type clothesKind: int
        :type stateType:  byte
        """
        # bool IsClothesStateType(int clothesKind, byte stateType)
        pass

    def IsAccessory(self, slotNo):
        """
        :type slotNo: int
        """
        # bool IsAccessory(int slotNo)
        pass

    def SetClothesState(self, clothesKind, state, next):
        """
        :type clothesKind: int
        :type state:  byte
        :type next:  bool
        """
        # void SetClothesState(int clothesKind, byte state, bool next = true)
        pass

    def SetClothesStatePrev(self, clothesKind):
        """
        :type clothesKind: int
        """
        # void SetClothesStatePrev(int clothesKind)
        pass

    def SetClothesStateNext(self, clothesKind):
        """
        :type clothesKind: int
        """
        # void SetClothesStateNext(int clothesKind)
        pass

    def SetClothesStateAll(self, state):
        """
        :type state: byte
        """
        # void SetClothesStateAll(byte state)
        pass

    def UpdateClothesStateAll(self):
        # void UpdateClothesStateAll()
        pass

    def RandomChangeOfClothesLowPoly(self, h):
        """
        :type h: int
        """
        # void RandomChangeOfClothesLowPoly(int h)
        pass

    def RandomChangeOfClothesLowPolyEnd(self):
        # void RandomChangeOfClothesLowPolyEnd()
        pass

    def ChangeToiletStateLowPoly(self):
        # void ChangeToiletStateLowPoly()
        pass

    def SetAccessoryState(self, slotNo, show):
        """
        :type slotNo: int
        :type show:  bool
        """
        # void SetAccessoryState(int slotNo, bool show)
        pass

    def SetAccessoryStateAll(self, show):
        """
        :type show: bool
        """
        # void SetAccessoryStateAll(bool show)
        pass

    def SetAccessoryStateCategory(self, cateNo, show):
        """
        :type cateNo: int
        :type show:  bool
        """
        # void SetAccessoryStateCategory(int cateNo, bool show)
        pass

    def GetAccessoryCategoryCount(self, cateNo):
        """
        :type cateNo: int
        """
        # int GetAccessoryCategoryCount(int cateNo)
        pass

    def GetAccessoryDefaultParentStr(self, type, id):
        """
        :type type: int
        :type id:  int
        """
        # string GetAccessoryDefaultParentStr(int type, int id)
        pass

    def GetAccessoryDefaultParentStr(self, slotNo):
        """
        :type slotNo: int
        """
        # string GetAccessoryDefaultParentStr(int slotNo)
        pass

    def ChangeAccessoryParent(self, slotNo, parentStr):
        """
        :type slotNo: int
        :type parentStr:  string
        """
        # bool ChangeAccessoryParent(int slotNo, string parentStr)
        pass

    def SetAccessoryPos(self, slotNo, correctNo, value, add, flags):
        """
        :type slotNo: int
        :type correctNo:  int
        :type value:  float
        :type add:  bool
        :type flags:  int
        """
        # bool SetAccessoryPos(int slotNo, int correctNo, float value, bool add, int flags = 7)
        pass

    def SetAccessoryRot(self, slotNo, correctNo, value, add, flags):
        """
        :type slotNo: int
        :type correctNo:  int
        :type value:  float
        :type add:  bool
        :type flags:  int
        """
        # bool SetAccessoryRot(int slotNo, int correctNo, float value, bool add, int flags = 7)
        pass

    def SetAccessoryScl(self, slotNo, correctNo, value, add, flags):
        """
        :type slotNo: int
        :type correctNo:  int
        :type value:  float
        :type add:  bool
        :type flags:  int
        """
        # bool SetAccessoryScl(int slotNo, int correctNo, float value, bool add, int flags = 7)
        pass

    def ResetAccessoryMove(self, slotNo, correctNo, type):
        """
        :type slotNo: int
        :type correctNo:  int
        :type type:  int
        """
        # bool ResetAccessoryMove(int slotNo, int correctNo, int type = 7)
        pass

    def UpdateAccessoryMoveFromInfo(self, slotNo):
        """
        :type slotNo: int
        """
        # bool UpdateAccessoryMoveFromInfo(int slotNo)
        pass

    def UpdateAccessoryMoveAllFromInfo(self):
        # bool UpdateAccessoryMoveAllFromInfo()
        pass

    def ChangeAccessoryColor(self, slotNo):
        """
        :type slotNo: int
        """
        # bool ChangeAccessoryColor(int slotNo)
        pass

    def GetAccessoryDefaultColor(self, color, slotNo, no):
        """
        :type color: ref Color
        :type slotNo:  int
        :type no:  int
        """
        # bool GetAccessoryDefaultColor(ref Color color, int slotNo, int no)
        pass

    def SetAccessoryDefaultColor(self, slotNo):
        """
        :type slotNo: int
        """
        # void SetAccessoryDefaultColor(int slotNo)
        pass

    def SetHideHairAccessory(self):
        # void SetHideHairAccessory()
        pass

    def CheckHideHair(self):
        # bool CheckHideHair()
        pass

    def ChangeCustomClothes(self, main, kind, updateColor, updateTex01, updateTex02, updateTex03, updateTex04):
        """
        :type main: bool
        :type kind:  int
        :type updateColor:  bool
        :type updateTex01:  bool
        :type updateTex02:  bool
        :type updateTex03:  bool
        :type updateTex04:  bool
        """
        # bool ChangeCustomClothes(bool main, int kind, bool updateColor, bool updateTex01, bool updateTex02, bool updateTex03, bool updateTex04)
        pass

    def UpdateClothesSiru(self, kind, frontTop, frontBot, downTop, downBot):
        """
        :type kind: int
        :type frontTop:  float
        :type frontBot:  float
        :type downTop:  float
        :type downBot:  float
        """
        # bool UpdateClothesSiru(int kind, float frontTop, float frontBot, float downTop, float downBot)
        pass

    def GetClothesDefaultColor(self, kind, no):
        """
        :type kind: int
        :type no:  int
        """
        # Color GetClothesDefaultColor(int kind, int no)
        pass

    def SetClothesDefaultColor(self, kind):
        """
        :type kind: int
        """
        # void SetClothesDefaultColor(int kind)
        pass

    def IsEmblem(self, kind):
        """
        :type kind: int
        """
        # bool IsEmblem(int kind)
        pass

    def IsEmblem(self, ccc):
        """
        :type ccc: ChaClothesComponent[]
        """
        # bool IsEmblem(ChaClothesComponent[] ccc)
        pass

    def ChangeCustomEmblem(self, kind):
        """
        :type kind: int
        """
        # bool ChangeCustomEmblem(int kind)
        pass

    def AddUpdateCMFaceTexFlags(self, inpBase, inpSub, inpPaint01, inpPaint02, inpCheek, inpLipLine, inpMole):
        """
        :type inpBase: bool
        :type inpSub:  bool
        :type inpPaint01:  bool
        :type inpPaint02:  bool
        :type inpCheek:  bool
        :type inpLipLine:  bool
        :type inpMole:  bool
        """
        # void AddUpdateCMFaceTexFlags(bool inpBase, bool inpSub, bool inpPaint01, bool inpPaint02, bool inpCheek, bool inpLipLine, bool inpMole)
        pass

    def AddUpdateCMFaceColorFlags(self, inpBase, inpSub, inpPaint01, inpPaint02, inpCheek, inpLipLine, inpMole):
        """
        :type inpBase: bool
        :type inpSub:  bool
        :type inpPaint01:  bool
        :type inpPaint02:  bool
        :type inpCheek:  bool
        :type inpLipLine:  bool
        :type inpMole:  bool
        """
        # void AddUpdateCMFaceColorFlags(bool inpBase, bool inpSub, bool inpPaint01, bool inpPaint02, bool inpCheek, bool inpLipLine, bool inpMole)
        pass

    def AddUpdateCMFaceLayoutFlags(self, inpPaint01, inpPaint02, inpMole):
        """
        :type inpPaint01: bool
        :type inpPaint02:  bool
        :type inpMole:  bool
        """
        # void AddUpdateCMFaceLayoutFlags(bool inpPaint01, bool inpPaint02, bool inpMole)
        pass

    def CreateFaceTexture(self):
        # bool CreateFaceTexture()
        pass

    def ChangeSettingWhiteOfEye(self, updateTex, updateColor):
        """
        :type updateTex: bool
        :type updateColor:  bool
        """
        # bool ChangeSettingWhiteOfEye(bool updateTex, bool updateColor)
        pass

    def ChangeSettingEyeL(self, updateBaseTex, updateMaskTex, updateColorAndOffset):
        """
        :type updateBaseTex: bool
        :type updateMaskTex:  bool
        :type updateColorAndOffset:  bool
        """
        # bool ChangeSettingEyeL(bool updateBaseTex, bool updateMaskTex, bool updateColorAndOffset)
        pass

    def ChangeSettingEyeR(self, updateBaseTex, updateMaskTex, updateColorAndOffset):
        """
        :type updateBaseTex: bool
        :type updateMaskTex:  bool
        :type updateColorAndOffset:  bool
        """
        # bool ChangeSettingEyeR(bool updateBaseTex, bool updateMaskTex, bool updateColorAndOffset)
        pass

    def ChangeSettingEye(self, updateBaseTex, updateMaskTex, updateColorAndOffset):
        """
        :type updateBaseTex: bool
        :type updateMaskTex:  bool
        :type updateColorAndOffset:  bool
        """
        # bool ChangeSettingEye(bool updateBaseTex, bool updateMaskTex, bool updateColorAndOffset)
        pass

    def ChangeSettingEye(self, lr, updateBaseTex, updateMaskTex, updateColorAndOffset):
        """
        :type lr: byte
        :type updateBaseTex:  bool
        :type updateMaskTex:  bool
        :type updateColorAndOffset:  bool
        """
        # bool ChangeSettingEye(byte lr, bool updateBaseTex, bool updateMaskTex, bool updateColorAndOffset)
        pass

    def ChangeSettingEyeHLUpPosY(self):
        # bool ChangeSettingEyeHLUpPosY()
        pass

    def ChangeSettingEyeHLDownPosY(self):
        # bool ChangeSettingEyeHLDownPosY()
        pass

    def ChangeSettingEyePosX(self):
        # bool ChangeSettingEyePosX()
        pass

    def ChangeSettingEyePosY(self):
        # bool ChangeSettingEyePosY()
        pass

    def ChangeSettingEyeScaleWidth(self):
        # bool ChangeSettingEyeScaleWidth()
        pass

    def ChangeSettingEyeScaleHeight(self):
        # bool ChangeSettingEyeScaleHeight()
        pass

    def ChangeSettingEyeTilt(self):
        # bool ChangeSettingEyeTilt()
        pass

    def ChangeSettingEyeHiUp(self):
        # bool ChangeSettingEyeHiUp()
        pass

    def ChangeSettingEyeHiUpColor(self):
        # bool ChangeSettingEyeHiUpColor()
        pass

    def ChangeSettingEyeHiDown(self):
        # bool ChangeSettingEyeHiDown()
        pass

    def ChangeSettingEyeHiDownColor(self):
        # bool ChangeSettingEyeHiDownColor()
        pass

    def ChangeSettingEyelineUp(self):
        # bool ChangeSettingEyelineUp()
        pass

    def ChangeSettingEyelineColor(self):
        # bool ChangeSettingEyelineColor()
        pass

    def UpdateEyelineShadowColor(self):
        # bool UpdateEyelineShadowColor()
        pass

    def ChangeSettingEyelineDown(self):
        # bool ChangeSettingEyelineDown()
        pass

    def ChangeSettingEyebrow(self):
        # bool ChangeSettingEyebrow()
        pass

    def ChangeSettingEyebrowColor(self):
        # bool ChangeSettingEyebrowColor()
        pass

    def ChangeSettingNose(self):
        # bool ChangeSettingNose()
        pass

    def VisibleDoubleTooth(self):
        # bool VisibleDoubleTooth()
        pass

    def ChangeSettingFaceDetail(self):
        # bool ChangeSettingFaceDetail()
        pass

    def ChangeSettingFaceDetailPower(self):
        # bool ChangeSettingFaceDetailPower()
        pass

    def ChangeSettingEyeShadow(self):
        # bool ChangeSettingEyeShadow()
        pass

    def ChangeSettingEyeShadowColor(self):
        # bool ChangeSettingEyeShadowColor()
        pass

    def ChangeSettingLip(self):
        # bool ChangeSettingLip()
        pass

    def ChangeSettingLipColor(self):
        # bool ChangeSettingLipColor()
        pass

    def ChangeSettingCheekGlossPower(self):
        # bool ChangeSettingCheekGlossPower()
        pass

    def ChangeSettingLipGlossPower(self):
        # bool ChangeSettingLipGlossPower()
        pass

    def SetFaceBaseMaterial(self):
        # bool SetFaceBaseMaterial()
        pass

    def ReleaseFaceCustomTexture(self):
        # bool ReleaseFaceCustomTexture()
        pass

    def ChangeCustomFaceWithoutCustomTexture(self):
        # void ChangeCustomFaceWithoutCustomTexture()
        pass

    def ChangeSettingHairColor(self, parts, c00, c01, c02):
        """
        :type parts: int
        :type c00:  bool
        :type c01:  bool
        :type c02:  bool
        """
        # void ChangeSettingHairColor(int parts, bool c00, bool c01, bool c02)
        pass

    def ChangeSettingHairOutlineColor(self, parts):
        """
        :type parts: int
        """
        # void ChangeSettingHairOutlineColor(int parts)
        pass

    def GetHairAcsColorNum(self, parts):
        """
        :type parts: int
        """
        # int GetHairAcsColorNum(int parts)
        pass

    def SetAcsDefaultColorParameterOnly(self, parts):
        """
        :type parts: int
        """
        # void SetAcsDefaultColorParameterOnly(int parts)
        pass

    def ChangeSettingHairAcsColor(self, parts):
        """
        :type parts: int
        """
        # void ChangeSettingHairAcsColor(int parts)
        pass

    def ChangeSettingHairLength(self, parts):
        """
        :type parts: int
        """
        # void ChangeSettingHairLength(int parts)
        pass

    def ChangeSettingHairFrontLength(self):
        # bool ChangeSettingHairFrontLength()
        pass

    def LoadHairGlossMask(self):
        # void LoadHairGlossMask()
        pass

    def ChangeSettingHairGlossMaskAll(self):
        # bool ChangeSettingHairGlossMaskAll()
        pass

    def ChangeSettingHairGlossMask(self, parts):
        """
        :type parts: int
        """
        # void ChangeSettingHairGlossMask(int parts)
        pass

    def AddUpdateCMBodyTexFlags(self, inpBase, inpSub, inpPaint01, inpPaint02, inpSunburn):
        """
        :type inpBase: bool
        :type inpSub:  bool
        :type inpPaint01:  bool
        :type inpPaint02:  bool
        :type inpSunburn:  bool
        """
        # void AddUpdateCMBodyTexFlags(bool inpBase, bool inpSub, bool inpPaint01, bool inpPaint02, bool inpSunburn)
        pass

    def AddUpdateCMBodyColorFlags(self, inpBase, inpSub, inpPaint01, inpPaint02, inpSunburn, inpNail):
        """
        :type inpBase: bool
        :type inpSub:  bool
        :type inpPaint01:  bool
        :type inpPaint02:  bool
        :type inpSunburn:  bool
        :type inpNail:  bool
        """
        # void AddUpdateCMBodyColorFlags(bool inpBase, bool inpSub, bool inpPaint01, bool inpPaint02, bool inpSunburn, bool inpNail)
        pass

    def AddUpdateCMBodyLayoutFlags(self, inpPaint01, inpPaint02):
        """
        :type inpPaint01: bool
        :type inpPaint02:  bool
        """
        # void AddUpdateCMBodyLayoutFlags(bool inpPaint01, bool inpPaint02)
        pass

    def CreateBodyTexture(self):
        # bool CreateBodyTexture()
        pass

    def ChangeSettingNip(self):
        # bool ChangeSettingNip()
        pass

    def ChangeSettingAreolaSize(self):
        # bool ChangeSettingAreolaSize()
        pass

    def ChangeSettingNipColor(self):
        # bool ChangeSettingNipColor()
        pass

    def ChangeSettingNipGlossPower(self):
        # bool ChangeSettingNipGlossPower()
        pass

    def ChangeSettingUnderhair(self):
        # bool ChangeSettingUnderhair()
        pass

    def ChangeSettingUnderhairColor(self):
        # bool ChangeSettingUnderhairColor()
        pass

    def VisibleAddBodyLine(self):
        # bool VisibleAddBodyLine()
        pass

    def ChangeSettingBodyDetail(self):
        # bool ChangeSettingBodyDetail()
        pass

    def ChangeSettingBodyDetailPower(self):
        # bool ChangeSettingBodyDetailPower()
        pass

    def ChangeSettingSkinGlossPower(self):
        # bool ChangeSettingSkinGlossPower()
        pass

    def ChangeSettingNailGlossPower(self):
        # bool ChangeSettingNailGlossPower()
        pass

    def GetLayoutInfo(self, id):
        """
        :type id: int
        """
        # Vector4 GetLayoutInfo(int id)
        pass

    def SetBodyBaseMaterial(self):
        # bool SetBodyBaseMaterial()
        pass

    def ReleaseBodyCustomTexture(self):
        # bool ReleaseBodyCustomTexture()
        pass

    def ChangeCustomBodyWithoutCustomTexture(self):
        # void ChangeCustomBodyWithoutCustomTexture()
        pass

    def InitShapeFace(self, trfBone, assetBundleAnmShapeFace, assetAnmShapeFace):
        """
        :type trfBone: Transform
        :type assetBundleAnmShapeFace:  string
        :type assetAnmShapeFace:  string
        """
        # bool InitShapeFace(Transform trfBone, string assetBundleAnmShapeFace, string assetAnmShapeFace)
        pass

    def ReleaseShapeFace(self):
        # void ReleaseShapeFace()
        pass

    def SetShapeFaceValue(self, index, value):
        """
        :type index: int
        :type value:  float
        """
        # bool SetShapeFaceValue(int index, float value)
        pass

    def UpdateShapeFaceValueFromCustomInfo(self):
        # bool UpdateShapeFaceValueFromCustomInfo()
        pass

    def GetShapeFaceValue(self, index):
        """
        :type index: int
        """
        # float GetShapeFaceValue(int index)
        pass

    def UpdateShapeFace(self):
        # void UpdateShapeFace()
        pass

    def DisableShapeMouth(self, disable):
        """
        :type disable: bool
        """
        # void DisableShapeMouth(bool disable)
        pass

    def InitShapeBody(self, trfBone):
        """
        :type trfBone: Transform
        """
        # bool InitShapeBody(Transform trfBone)
        pass

    def ReleaseShapeBody(self):
        # void ReleaseShapeBody()
        pass

    def SetShapeBodyValue(self, index, value):
        """
        :type index: int
        :type value:  float
        """
        # bool SetShapeBodyValue(int index, float value)
        pass

    def UpdateShapeBodyValueFromCustomInfo(self):
        # bool UpdateShapeBodyValueFromCustomInfo()
        pass

    def GetShapeBodyValue(self, index):
        """
        :type index: int
        """
        # float GetShapeBodyValue(int index)
        pass

    def UpdateShapeBody(self):
        # void UpdateShapeBody()
        pass

    def UpdateAlwaysShapeBody(self):
        # void UpdateAlwaysShapeBody()
        pass

    def DisableShapeBodyID(self, LR, id, disable):
        """
        :type LR: int
        :type id:  int
        :type disable:  bool
        """
        # void DisableShapeBodyID(int LR, int id, bool disable)
        pass

    def DisableShapeBust(self, LR, disable):
        """
        :type LR: int
        :type disable:  bool
        """
        # void DisableShapeBust(int LR, bool disable)
        pass

    def DisableShapeNip(self, LR, disable):
        """
        :type LR: int
        :type disable:  bool
        """
        # void DisableShapeNip(int LR, bool disable)
        pass

    def UpdateBustSoftnessAndGravity(self):
        # void UpdateBustSoftnessAndGravity()
        pass

    def ChangeBustSoftness(self, soft):
        """
        :type soft: float
        """
        # void ChangeBustSoftness(float soft)
        pass

    def UpdateBustSoftness(self):
        # bool UpdateBustSoftness()
        pass

    def ChangeBustGravity(self, gravity):
        """
        :type gravity: float
        """
        # void ChangeBustGravity(float gravity)
        pass

    def UpdateBustGravity(self):
        # bool UpdateBustGravity()
        pass

    def HideEyeHighlight(self, hide):
        """
        :type hide: bool
        """
        # void HideEyeHighlight(bool hide)
        pass

    def ChangeEyesShaking(self, enable):
        """
        :type enable: bool
        """
        # void ChangeEyesShaking(bool enable)
        pass

    def GetEyesShaking(self):
        # bool GetEyesShaking()
        pass

    def GetEyesPtnNum(self):
        # int GetEyesPtnNum()
        pass

    def ChangeEyesPtn(self, ptn, blend):
        """
        :type ptn: int
        :type blend:  bool
        """
        # void ChangeEyesPtn(int ptn, bool blend = true)
        pass

    def GetEyesPtn(self):
        # int GetEyesPtn()
        pass

    def ChangeGagEyesMaterial(self, no, tex, v4TileAnim, sizeSpeed, sizeWidth, angleSpeed, yurayura):
        """
        :type no: int
        :type tex:  Texture
        :type v4TileAnim:  Vector4
        :type sizeSpeed:  float
        :type sizeWidth:  float
        :type angleSpeed:  float
        :type yurayura:  float
        """
        # void ChangeGagEyesMaterial(int no, Texture tex, Vector4 v4TileAnim, float sizeSpeed, float sizeWidth, float angleSpeed, float yurayura)
        pass

    def ChangeEyesOpenMax(self, maxValue):
        """
        :type maxValue: float
        """
        # void ChangeEyesOpenMax(float maxValue)
        pass

    def GetEyesOpenMax(self):
        # float GetEyesOpenMax()
        pass

    def ChangeEyebrowPtn(self, ptn, blend):
        """
        :type ptn: int
        :type blend:  bool
        """
        # void ChangeEyebrowPtn(int ptn, bool blend = true)
        pass

    def GetEyebrowPtn(self):
        # int GetEyebrowPtn()
        pass

    def ChangeEyebrowOpenMax(self, maxValue):
        """
        :type maxValue: float
        """
        # void ChangeEyebrowOpenMax(float maxValue)
        pass

    def GetEyebrowOpenMax(self):
        # float GetEyebrowOpenMax()
        pass

    def ChangeEyesBlinkFlag(self, blink):
        """
        :type blink: bool
        """
        # void ChangeEyesBlinkFlag(bool blink)
        pass

    def GetEyesBlinkFlag(self):
        # bool GetEyesBlinkFlag()
        pass

    def ChangeMouthPtn(self, ptn, blend):
        """
        :type ptn: int
        :type blend:  bool
        """
        # void ChangeMouthPtn(int ptn, bool blend = true)
        pass

    def GetMouthPtn(self):
        # int GetMouthPtn()
        pass

    def ChangeMouthOpenMax(self, maxValue):
        """
        :type maxValue: float
        """
        # void ChangeMouthOpenMax(float maxValue)
        pass

    def GetMouthOpenMax(self):
        # float GetMouthOpenMax()
        pass

    def ChangeMouthFixed(self, fix):
        """
        :type fix: bool
        """
        # void ChangeMouthFixed(bool fix)
        pass

    def GetMouthFixed(self):
        # bool GetMouthFixed()
        pass

    def ChangeTongueState(self, state):
        """
        :type state: byte
        """
        # void ChangeTongueState(byte state)
        pass

    def GetTongueState(self):
        # byte GetTongueState()
        pass

    def SetVoiceTransform(self, trfVoice):
        """
        :type trfVoice: Transform
        """
        # bool SetVoiceTransform(Transform trfVoice)
        pass

    def ChangeLookEyesTarget(self, targetType, trfTarg, rate, rotDeg, range, dis):
        """
        :type targetType: int
        :type trfTarg:  Transform
        :type rate:  float
        :type rotDeg:  float
        :type range:  float
        :type dis:  float
        """
        # void ChangeLookEyesTarget(int targetType, Transform trfTarg = null, float rate = 0.5f, float rotDeg = 0f, float range = 1f, float dis = 2f)
        pass

    def ChangeLookEyesPtn(self, ptn):
        """
        :type ptn: int
        """
        # void ChangeLookEyesPtn(int ptn)
        pass

    def GetLookEyesPtn(self):
        # int GetLookEyesPtn()
        pass

    def ChangeLookNeckTarget(self, targetType, trfTarg, rate, rotDeg, range, dis):
        """
        :type targetType: int
        :type trfTarg:  Transform
        :type rate:  float
        :type rotDeg:  float
        :type range:  float
        :type dis:  float
        """
        # void ChangeLookNeckTarget(int targetType, Transform trfTarg = null, float rate = 0.5f, float rotDeg = 0f, float range = 1f, float dis = 0.8f)
        pass

    def ChangeLookNeckPtn(self, ptn, rate):
        """
        :type ptn: int
        :type rate:  float
        """
        # void ChangeLookNeckPtn(int ptn, float rate = 1f)
        pass

    def GetLookNeckPtn(self):
        # int GetLookNeckPtn()
        pass

    def SetForegroundEyesAndEyebrow(self):
        # void SetForegroundEyesAndEyebrow()
        pass

    def ChangeHohoAkaRate(self, value):
        """
        :type value: float
        """
        # void ChangeHohoAkaRate(float value)
        pass

    def IsGagEyes(self):
        # bool IsGagEyes()
        pass

    def Load(self, reflectStatus):
        """
        :type reflectStatus: bool
        """
        # bool Load(bool reflectStatus = false)
        pass

    def LoadAsync(self, reflectStatus, asyncFlags):
        """
        :type reflectStatus: bool
        :type asyncFlags:  bool
        """
        # IEnumerator LoadAsync(bool reflectStatus = false, bool asyncFlags = true)
        pass

    def Reload(self, noChangeClothes, noChangeHead, noChangeHair, noChangeBody):
        """
        :type noChangeClothes: bool
        :type noChangeHead:  bool
        :type noChangeHair:  bool
        :type noChangeBody:  bool
        """
        # bool Reload(bool noChangeClothes = false, bool noChangeHead = false, bool noChangeHair = false, bool noChangeBody = false)
        pass

    def ReloadAsync(self, noChangeClothes, noChangeHead, noChangeHair, noChangeBody, asyncFlags):
        """
        :type noChangeClothes: bool
        :type noChangeHead:  bool
        :type noChangeHair:  bool
        :type noChangeBody:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ReloadAsync(bool noChangeClothes = false, bool noChangeHead = false, bool noChangeHair = false, bool noChangeBody = false, bool asyncFlags = true)
        pass

    def ChangeHead(self, forceChange):
        """
        :type forceChange: bool
        """
        # void ChangeHead(bool forceChange = false)
        pass

    def ChangeHead(self, _headId, forceChange):
        """
        :type _headId: int
        :type forceChange:  bool
        """
        # void ChangeHead(int _headId, bool forceChange = false)
        pass

    def ChangeHeadAsync(self, forceChange):
        """
        :type forceChange: bool
        """
        # IEnumerator ChangeHeadAsync(bool forceChange = false)
        pass

    def ChangeHeadAsync(self, _headId, forceChange, asyncFlags):
        """
        :type _headId: int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeHeadAsync(int _headId, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeHairFront(self, forceChange):
        """
        :type forceChange: bool
        """
        # bool ChangeHairFront(bool forceChange = false)
        pass

    def ChangeHairBack(self, forceChange):
        """
        :type forceChange: bool
        """
        # bool ChangeHairBack(bool forceChange = false)
        pass

    def ChangeHairSide(self, forceChange):
        """
        :type forceChange: bool
        """
        # bool ChangeHairSide(bool forceChange = false)
        pass

    def ChangeHairOption(self, forceChange):
        """
        :type forceChange: bool
        """
        # bool ChangeHairOption(bool forceChange = false)
        pass

    def ChangeHair(self, forceChange):
        """
        :type forceChange: bool
        """
        # void ChangeHair(bool forceChange = false)
        pass

    def ChangeHair(self, kind, id, forceChange):
        """
        :type kind: int
        :type id:  int
        :type forceChange:  bool
        """
        # void ChangeHair(int kind, int id, bool forceChange = false)
        pass

    def ChangeHairAsync(self, forceChange):
        """
        :type forceChange: bool
        """
        # IEnumerator ChangeHairAsync(bool forceChange = false)
        pass

    def ChangeHairAsync(self, kind, id, forceChange, asyncFlags):
        """
        :type kind: int
        :type id:  int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeHairAsync(int kind, int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothes(self, forceChange):
        """
        :type forceChange: bool
        """
        # void ChangeClothes(bool forceChange = false)
        pass

    def ChangeClothes(self, kind, id, subId01, subId02, subId03, forceChange):
        """
        :type kind: int
        :type id:  int
        :type subId01:  int
        :type subId02:  int
        :type subId03:  int
        :type forceChange:  bool
        """
        # void ChangeClothes(int kind, int id, int subId01, int subId02, int subId03, bool forceChange = false)
        pass

    def ChangeClothesAsync(self, forceChange):
        """
        :type forceChange: bool
        """
        # IEnumerator ChangeClothesAsync(bool forceChange = false)
        pass

    def ChangeClothesAsync(self, kind, id, subId01, subId02, subId03, forceChange, asyncFlags):
        """
        :type kind: int
        :type id:  int
        :type subId01:  int
        :type subId02:  int
        :type subId03:  int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesAsync(int kind, int id, int subId01, int subId02, int subId03, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesTop(self, id, subId01, subId02, subId03, forceChange):
        """
        :type id: int
        :type subId01:  int
        :type subId02:  int
        :type subId03:  int
        :type forceChange:  bool
        """
        # void ChangeClothesTop(int id, int subId01, int subId02, int subId03, bool forceChange = false)
        pass

    def ChangeClothesTopAsync(self, id, subId01, subId02, subId03, forceChange, asyncFlags):
        """
        :type id: int
        :type subId01:  int
        :type subId02:  int
        :type subId03:  int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesTopAsync(int id, int subId01, int subId02, int subId03, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesTopParts(self, kind, id, forceChange):
        """
        :type kind: int
        :type id:  int
        :type forceChange:  bool
        """
        # void ChangeClothesTopParts(int kind, int id, bool forceChange = false)
        pass

    def ChangeClothesTopPartsAsync(self, kind, id, forceChange, asyncFlags):
        """
        :type kind: int
        :type id:  int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesTopPartsAsync(int kind, int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesBot(self, id, forceChange):
        """
        :type id: int
        :type forceChange:  bool
        """
        # void ChangeClothesBot(int id, bool forceChange = false)
        pass

    def ChangeClothesBotAsync(self, id, forceChange, asyncFlags):
        """
        :type id: int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesBotAsync(int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesBra(self, id, forceChange):
        """
        :type id: int
        :type forceChange:  bool
        """
        # void ChangeClothesBra(int id, bool forceChange = false)
        pass

    def ChangeClothesBraAsync(self, id, forceChange, asyncFlags):
        """
        :type id: int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesBraAsync(int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesShorts(self, id, forceChange):
        """
        :type id: int
        :type forceChange:  bool
        """
        # void ChangeClothesShorts(int id, bool forceChange = false)
        pass

    def ChangeClothesShortsAsync(self, id, forceChange, asyncFlags):
        """
        :type id: int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesShortsAsync(int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesGloves(self, id, forceChange):
        """
        :type id: int
        :type forceChange:  bool
        """
        # void ChangeClothesGloves(int id, bool forceChange = false)
        pass

    def ChangeClothesGlovesAsync(self, id, forceChange, asyncFlags):
        """
        :type id: int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesGlovesAsync(int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesPanst(self, id, forceChange):
        """
        :type id: int
        :type forceChange:  bool
        """
        # void ChangeClothesPanst(int id, bool forceChange = false)
        pass

    def ChangeClothesPanstAsync(self, id, forceChange, asyncFlags):
        """
        :type id: int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesPanstAsync(int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesSocks(self, id, forceChange):
        """
        :type id: int
        :type forceChange:  bool
        """
        # void ChangeClothesSocks(int id, bool forceChange = false)
        pass

    def ChangeClothesSocksAsync(self, id, forceChange, asyncFlags):
        """
        :type id: int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesSocksAsync(int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeClothesShoes(self, type, id, forceChange):
        """
        :type type: int
        :type id:  int
        :type forceChange:  bool
        """
        # void ChangeClothesShoes(int type, int id, bool forceChange = false)
        pass

    def ChangeClothesShoesAsync(self, type, id, forceChange, asyncFlags):
        """
        :type type: int
        :type id:  int
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeClothesShoesAsync(int type, int id, bool forceChange = false, bool asyncFlags = true)
        pass

    def ChangeAccessory(self, forceChange):
        """
        :type forceChange: bool
        """
        # void ChangeAccessory(bool forceChange = false)
        pass

    def ChangeAccessory(self, slotNo, type, id, parentKey, forceChange):
        """
        :type slotNo: int
        :type type:  int
        :type id:  int
        :type parentKey:  string
        :type forceChange:  bool
        """
        # void ChangeAccessory(int slotNo, int type, int id, string parentKey, bool forceChange = false)
        pass

    def ChangeAccessoryAsync(self, forceChange):
        """
        :type forceChange: bool
        """
        # IEnumerator ChangeAccessoryAsync(bool forceChange = false)
        pass

    def ChangeAccessoryAsync(self, slotNo, type, id, parentKey, forceChange, asyncFlags):
        """
        :type slotNo: int
        :type type:  int
        :type id:  int
        :type parentKey:  string
        :type forceChange:  bool
        :type asyncFlags:  bool
        """
        # IEnumerator ChangeAccessoryAsync(int slotNo, int type, int id, string parentKey, bool forceChange = false, bool asyncFlags = true)
        pass

    def LoadGagMaterial(self):
        # bool LoadGagMaterial()
        pass

    def LoadAlphaMaskTexture(self, assetBundleName, assetName, type):
        """
        :type assetBundleName: string
        :type assetName:  string
        :type type:  byte
        """
        # bool LoadAlphaMaskTexture(string assetBundleName, string assetName, byte type)
        pass

    def InitializeExpression(self, _enable):
        """
        :type _enable: bool
        """
        # bool InitializeExpression(bool _enable = true)
        pass

    def LoadHitObject(self):
        # void LoadHitObject()
        pass

    def ReleaseHitObject(self):
        # void ReleaseHitObject()
        pass

# IKInfo.cs
class IKInfo():
    def __init__(self):
        self.guideObject = None # GuideObject guideObject
        """:type : GuideObject"""
        self.targetInfo = None # OIIKTargetInfo targetInfo
        """:type : OIIKTargetInfo"""
        self.baseObject = None # Transform baseObject
        """:type : Transform"""
        self.targetObject = None # Transform targetObject
        """:type : Transform"""
        self.boneObject = None # Transform boneObject
        """:type : Transform"""
        self.gameObject = None # GameObject gameObject
        """:type : GameObject"""
        self.active = None # bool active
        """:type : bool"""
        self.boneGroup = None # OIBoneInfo.BoneGroup boneGroup => targetInfo.group;
        """:type : OIBoneInfo.BoneGroup"""
        self.scaleRate = None # float scaleRate
        """:type : float"""
        self.layer = None # int layer
        """:type : int"""
    def IKInfo(self, _guideObject, _targetInfo, _base, _target, _bone):
        """
        :type _guideObject: GuideObject
        :type _targetInfo:  OIIKTargetInfo
        :type _base:  Transform
        :type _target:  Transform
        :type _bone:  Transform
        """
        # IKInfo(GuideObject _guideObject, OIIKTargetInfo _targetInfo, Transform _base, Transform _target, Transform _bone)
        pass

    def CopyBaseValue(self):
        # void CopyBaseValue()
        pass

    def CopyBone(self):
        # void CopyBone()
        pass

    def CopyBoneRotation(self):
        # void CopyBoneRotation()
        pass

# OCIChar.cs
class OCIChar():
    def __init__(self):
        self.charReference = None # ChaReference charReference;
        """:type : ChaReference"""
        self.dicAccessPoint = None # Dictionary<int, AccessPointInfo> dicAccessPoint = new Dictionary<int, AccessPointInfo>();
        """:type : Dictionary<int, AccessPointInfo>"""
        self.listBones = None # List<BoneInfo> listBones = new List<BoneInfo>();
        """:type : List<BoneInfo>"""
        self.listIKTarget = None # List<IKInfo> listIKTarget = new List<IKInfo>();
        """:type : List<IKInfo>"""
        self.lookAtInfo = None # LookAtInfo lookAtInfo;
        """:type : LookAtInfo"""
        self.charInfo = None # ChaControl charInfo;
        """:type : ChaControl"""
        self.handAnimeCtrl = None # HandAnimeCtrl[] handAnimeCtrl = new HandAnimeCtrl[2];
        """:type : HandAnimeCtrl[]"""
        self.fkCtrl = None # FKCtrl fkCtrl;
        """:type : FKCtrl"""
        self.ikCtrl = None # IKCtrl ikCtrl;
        """:type : IKCtrl"""
        self.finalIK = None # FullBodyBipedIK finalIK;
        """:type : FullBodyBipedIK"""
        self.neckLookCtrl = None # NeckLookControllerVer2 neckLookCtrl;
        """:type : NeckLookControllerVer2"""
        self.hairDynamic = None # DynamicBone[] hairDynamic;
        """:type : DynamicBone[]"""
        self.skirtDynamic = None # DynamicBone[] skirtDynamic;
        """:type : DynamicBone[]"""
        self.dynamicBust = None # bool[] dynamicBust = new bool[2]
        """:type : bool[]"""
        self.optionItemCtrl = None # OptionItemCtrl optionItemCtrl;
        """:type : OptionItemCtrl"""
        self.isAnimeMotion = None # bool isAnimeMotion;
        """:type : bool"""
        self.isHAnime = None # bool isHAnime;
        """:type : bool"""
        self.charAnimeCtrl = None # CharAnimeCtrl charAnimeCtrl;
        """:type : CharAnimeCtrl"""
        self.yureCtrl = None # YureCtrl yureCtrl;
        """:type : YureCtrl"""
        self.animeParam = None # string[] animeParam = new string[2]
        """:type : string[]"""
        self.dicAccessoryPoint = None # Dictionary<TreeNodeObject, int> dicAccessoryPoint = new Dictionary<TreeNodeObject, int>();
        """:type : Dictionary<TreeNodeObject, int>"""
        self.oiCharInfo = None # OICharInfo oiCharInfo => base.objectInfo as OICharInfo;
        """:type : OICharInfo"""
        self.transSon = None # Transform transSon
        """:type : Transform"""
        self.charFileStatus = None # ChaFileStatus charFileStatus => charInfo.fileStatus;
        """:type : ChaFileStatus"""
        self.sex = None # int sex => charInfo.fileParam.sex;
        """:type : int"""
        self.foregroundEyebrow = None # byte foregroundEyebrow
        """:type : byte"""
        self.foregroundEyes = None # byte foregroundEyes
        """:type : byte"""
        self.voiceCtrl = None # VoiceCtrl voiceCtrl => oiCharInfo.voiceCtrl;
        """:type : VoiceCtrl"""
        self.voiceRepeat = None # VoiceCtrl.Repeat voiceRepeat
        """:type : VoiceCtrl.Repeat"""
        self.preparation = None # Preparation preparation
        """:type : Preparation"""
        self.animeSpeed = None # override float animeSpeed
        """:type : override float"""
        self.animePattern = None # float animePattern
        """:type : float"""
        self.animeOptionParam = None # float[] animeOptionParam => oiCharInfo.animeOptionParam;
        """:type : float[]"""
        self.animeOptionParam1 = None # float animeOptionParam1
        """:type : float"""
        self.animeOptionParam2 = None # float animeOptionParam2
        """:type : float"""
    def OnDelete(self):
        # override void OnDelete()
        pass

    def OnAttach(self, _parent, _child):
        """
        :type _parent: TreeNodeObject
        :type _child:  ObjectCtrlInfo
        """
        # override void OnAttach(TreeNodeObject _parent, ObjectCtrlInfo _child)
        pass

    def OnLoadAttach(self, _parent, _child):
        """
        :type _parent: TreeNodeObject
        :type _child:  ObjectCtrlInfo
        """
        # override void OnLoadAttach(TreeNodeObject _parent, ObjectCtrlInfo _child)
        pass

    def OnDetach(self):
        # override void OnDetach()
        pass

    def OnSelect(self, _select):
        """
        :type _select: bool
        """
        # override void OnSelect(bool _select)
        pass

    def OnDetachChild(self, _child):
        """
        :type _child: ObjectCtrlInfo
        """
        # override void OnDetachChild(ObjectCtrlInfo _child)
        pass

    def OnSavePreprocessing(self):
        # override void OnSavePreprocessing()
        pass

    def OnVisible(self, _visible):
        """
        :type _visible: bool
        """
        # override void OnVisible(bool _visible)
        pass

    def InitKinematic(self, _target, _finalIK, _neckLook, _hairDynamic, _skirtDynamic):
        """
        :type _target: GameObject
        :type _finalIK:  FullBodyBipedIK
        :type _neckLook:  NeckLookControllerVer2
        :type _hairDynamic:  DynamicBone[]
        :type _skirtDynamic:  DynamicBone[]
        """
        # void InitKinematic(GameObject _target, FullBodyBipedIK _finalIK, NeckLookControllerVer2 _neckLook, DynamicBone[] _hairDynamic, DynamicBone[] _skirtDynamic)
        pass

    def InitFK(self, _target):
        """
        :type _target: GameObject
        """
        # void InitFK(GameObject _target)
        pass

    def ActiveKinematicMode(self, _mode, _active, _force):
        """
        :type _mode: OICharInfo.KinematicMode
        :type _active:  bool
        :type _force:  bool
        """
        # void ActiveKinematicMode(OICharInfo.KinematicMode _mode, bool _active, bool _force)
        pass

    def ActiveFK(self, _group, _active, _force):
        """
        :type _group: OIBoneInfo.BoneGroup
        :type _active:  bool
        :type _force:  bool
        """
        # void ActiveFK(OIBoneInfo.BoneGroup _group, bool _active, bool _force = false)
        pass

    def IsFKGroup(self, _group):
        """
        :type _group: OIBoneInfo.BoneGroup
        """
        # bool IsFKGroup(OIBoneInfo.BoneGroup _group)
        pass

    def InitFKBone(self, _group):
        """
        :type _group: OIBoneInfo.BoneGroup
        """
        # void InitFKBone(OIBoneInfo.BoneGroup _group)
        pass

    def ActiveIK(self, _group, _active, _force):
        """
        :type _group: OIBoneInfo.BoneGroup
        :type _active:  bool
        :type _force:  bool
        """
        # void ActiveIK(OIBoneInfo.BoneGroup _group, bool _active, bool _force = false)
        pass

    def UpdateFKColor(self, _parts):
        """
        :type _parts: params OIBoneInfo.BoneGroup[]
        """
        # void UpdateFKColor(params OIBoneInfo.BoneGroup[] _parts)
        pass

    def EnableExpressionCategory(self, _category, _value):
        """
        :type _category: int
        :type _value:  bool
        """
        # void EnableExpressionCategory(int _category, bool _value)
        pass

    def LoadAnime(self, _group, _category, _no, _normalizedTime):
        """
        :type _group: int
        :type _category:  int
        :type _no:  int
        :type _normalizedTime:  float
        """
        # virtual void LoadAnime(int _group, int _category, int _no, float _normalizedTime = 0f)
        pass

    def ChangeHandAnime(self, _type, _ptn):
        """
        :type _type: int
        :type _ptn:  int
        """
        # virtual void ChangeHandAnime(int _type, int _ptn)
        pass

    def RestartAnime(self):
        # virtual void RestartAnime()
        pass

    def ChangeChara(self, _path):
        """
        :type _path: string
        """
        # virtual void ChangeChara(string _path)
        pass

    def SetCoordinateInfo(self, _type, _force):
        """
        :type _type: ChaFileDefine.CoordinateType
        :type _force:  bool
        """
        # virtual void SetCoordinateInfo(ChaFileDefine.CoordinateType _type, bool _force = false)
        pass

    def SetShoesType(self, _type):
        """
        :type _type: int
        """
        # virtual void SetShoesType(int _type)
        pass

    def SetClothesStateAll(self, _state):
        """
        :type _state: int
        """
        # virtual void SetClothesStateAll(int _state)
        pass

    def SetClothesState(self, _id, _state):
        """
        :type _id: int
        :type _state:  byte
        """
        # virtual void SetClothesState(int _id, byte _state)
        pass

    def ShowAccessory(self, _id, _flag):
        """
        :type _id: int
        :type _flag:  bool
        """
        # virtual void ShowAccessory(int _id, bool _flag)
        pass

    def LoadClothesFile(self, _path):
        """
        :type _path: string
        """
        # virtual void LoadClothesFile(string _path)
        pass

    def SetSiruFlags(self, _parts, _state):
        """
        :type _parts: ChaFileDefine.SiruParts
        :type _state:  byte
        """
        # virtual void SetSiruFlags(ChaFileDefine.SiruParts _parts, byte _state)
        pass

    def GetSiruFlags(self, _parts):
        """
        :type _parts: ChaFileDefine.SiruParts
        """
        # virtual byte GetSiruFlags(ChaFileDefine.SiruParts _parts)
        pass

    def SetNipStand(self, _value):
        """
        :type _value: float
        """
        # virtual void SetNipStand(float _value)
        pass

    def SetVisibleSimple(self, _flag):
        """
        :type _flag: bool
        """
        # virtual void SetVisibleSimple(bool _flag)
        pass

    def GetVisibleSimple(self):
        # bool GetVisibleSimple()
        pass

    def SetSimpleColor(self, _color):
        """
        :type _color: Color
        """
        # virtual void SetSimpleColor(Color _color)
        pass

    def SetVisibleSon(self, _flag):
        """
        :type _flag: bool
        """
        # virtual void SetVisibleSon(bool _flag)
        pass

    def GetSonLength(self):
        # virtual float GetSonLength()
        pass

    def SetSonLength(self, _value):
        """
        :type _value: float
        """
        # virtual void SetSonLength(float _value)
        pass

    def SetTearsLv(self, _state):
        """
        :type _state: byte
        """
        # virtual void SetTearsLv(byte _state)
        pass

    def GetTearsLv(self):
        # virtual byte GetTearsLv()
        pass

    def SetHohoAkaRate(self, _value):
        """
        :type _value: float
        """
        # virtual void SetHohoAkaRate(float _value)
        pass

    def GetHohoAkaRate(self):
        # virtual float GetHohoAkaRate()
        pass

    def ChangeLookEyesPtn(self, _ptn, _force):
        """
        :type _ptn: int
        :type _force:  bool
        """
        # virtual void ChangeLookEyesPtn(int _ptn, bool _force = false)
        pass

    def ChangeLookNeckPtn(self, _ptn):
        """
        :type _ptn: int
        """
        # virtual void ChangeLookNeckPtn(int _ptn)
        pass

    def ChangeEyesOpen(self, _value):
        """
        :type _value: float
        """
        # virtual void ChangeEyesOpen(float _value)
        pass

    def ChangeBlink(self, _value):
        """
        :type _value: bool
        """
        # virtual void ChangeBlink(bool _value)
        pass

    def ChangeMouthOpen(self, _value):
        """
        :type _value: float
        """
        # virtual void ChangeMouthOpen(float _value)
        pass

    def ChangeLipSync(self, _value):
        """
        :type _value: bool
        """
        # virtual void ChangeLipSync(bool _value)
        pass

    def SetVoice(self):
        # virtual void SetVoice()
        pass

    def AddVoice(self, _group, _category, _no):
        """
        :type _group: int
        :type _category:  int
        :type _no:  int
        """
        # virtual void AddVoice(int _group, int _category, int _no)
        pass

    def DeleteVoice(self, _index):
        """
        :type _index: int
        """
        # virtual void DeleteVoice(int _index)
        pass

    def DeleteAllVoice(self):
        # virtual void DeleteAllVoice()
        pass

    def PlayVoice(self, _index):
        """
        :type _index: int
        """
        # virtual bool PlayVoice(int _index)
        pass

    def StopVoice(self):
        # virtual void StopVoice()
        pass

# Studio.cs
class Studio():
    def __init__(self):
        self.savePath = None # const string savePath = "studio/scene";
        """:type : const string"""
        self.dicInfo = None # Dictionary<TreeNodeObject, ObjectCtrlInfo> dicInfo = new Dictionary<TreeNodeObject, ObjectCtrlInfo>();
        """:type : Dictionary<TreeNodeObject, ObjectCtrlInfo>"""
        self.dicObjectCtrl = None # Dictionary<int, ObjectCtrlInfo> dicObjectCtrl = new Dictionary<int, ObjectCtrlInfo>();
        """:type : Dictionary<int, ObjectCtrlInfo>"""
        self.dicChangeAmount = None # Dictionary<int, ChangeAmount> dicChangeAmount = new Dictionary<int, ChangeAmount>();
        """:type : Dictionary<int, ChangeAmount>"""
        self.onDelete = None # Action<ObjectCtrlInfo> onDelete;
        """:type : Action<ObjectCtrlInfo>"""
        self.onChangeMap = None # Action onChangeMap;
        """:type : Action"""
        self.workInfo = None # WorkInfo workInfo = new WorkInfo();
        """:type : WorkInfo"""
        self.treeNodeCtrl = None # TreeNodeCtrl treeNodeCtrl => m_TreeNodeCtrl;
        """:type : TreeNodeCtrl"""
        self.rootButtonCtrl = None # RootButtonCtrl rootButtonCtrl => m_RootButtonCtrl;
        """:type : RootButtonCtrl"""
        self.manipulatePanelCtrl = None # ManipulatePanelCtrl manipulatePanelCtrl => _manipulatePanelCtrl;
        """:type : ManipulatePanelCtrl"""
        self.cameraCtrl = None # Studio.CameraControl cameraCtrl => m_CameraCtrl;
        """:type : Studio.CameraControl"""
        self.systemButtonCtrl = None # SystemButtonCtrl systemButtonCtrl => m_SystemButtonCtrl;
        """:type : SystemButtonCtrl"""
        self.bgmCtrl = None # BGMCtrl bgmCtrl => sceneInfo.bgmCtrl;
        """:type : BGMCtrl"""
        self.envCtrl = None # ENVCtrl envCtrl => sceneInfo.envCtrl;
        """:type : ENVCtrl"""
        self.outsideSoundCtrl = None # OutsideSoundCtrl outsideSoundCtrl => sceneInfo.outsideSoundCtrl;
        """:type : OutsideSoundCtrl"""
        self.cameraLightCtrl = None # CameraLightCtrl cameraLightCtrl => m_CameraLightCtrl;
        """:type : CameraLightCtrl"""
        self.mapList = None # MapList mapList => _mapList;
        """:type : MapList"""
        self.colorPalette = None # ColorPalette colorPalette => _colorPalette;
        """:type : ColorPalette"""
        self.patternSelectListCtrl = None # PatternSelectListCtrl patternSelectListCtrl => _patternSelectListCtrl;
        """:type : PatternSelectListCtrl"""
        self.gameScreenShot = None # Studio.GameScreenShot gameScreenShot => _gameScreenShot;
        """:type : Studio.GameScreenShot"""
        self.frameCtrl = None # FrameCtrl frameCtrl => _frameCtrl;
        """:type : FrameCtrl"""
        self.logoList = None # LogoList logoList => _logoList;
        """:type : LogoList"""
        self.isInputNow = None # bool isInputNow => (!(bool)_inputFieldNow) ? ((bool)_inputFieldTMPNow && _inputFieldTMPNow.isFocused) : _inputFieldNow.isFocused;
        """:type : bool"""
        self.textureLine = None # Texture textureLine => _textureLine;
        """:type : Texture"""
        self.sceneInfo = None # SceneInfo sceneInfo
        """:type : SceneInfo"""
        self.optionSystem = None # static OptionSystem optionSystem
        """:type : static OptionSystem"""
        self.cameraCount = None # int cameraCount
        """:type : int"""
        self.isVRMode = None # bool isVRMode
        """:type : bool"""
    def AddFemale(self, _path):
        """
        :type _path: string
        """
        # void AddFemale(string _path)
        pass

    def AddMale(self, _path):
        """
        :type _path: string
        """
        # void AddMale(string _path)
        pass

    def AddMap(self, _no, _close, _wait, _coroutine):
        """
        :type _no: int
        :type _close:  bool
        :type _wait:  bool
        :type _coroutine:  bool
        """
        # void AddMap(int _no, bool _close = true, bool _wait = true, bool _coroutine = true)
        pass

    def AddItem(self, _group, _category, _no):
        """
        :type _group: int
        :type _category:  int
        :type _no:  int
        """
        # void AddItem(int _group, int _category, int _no)
        pass

    def AddLight(self, _no):
        """
        :type _no: int
        """
        # void AddLight(int _no)
        pass

    def AddFolder(self):
        # void AddFolder()
        pass

    def AddCamera(self):
        # void AddCamera()
        pass

    def ChangeCamera(self, _ociCamera, _active, _force):
        """
        :type _ociCamera: OCICamera
        :type _active:  bool
        :type _force:  bool
        """
        # void ChangeCamera(OCICamera _ociCamera, bool _active, bool _force = false)
        pass

    def ChangeCamera(self, _ociCamera):
        """
        :type _ociCamera: OCICamera
        """
        # void ChangeCamera(OCICamera _ociCamera)
        pass

    def DeleteCamera(self, _ociCamera):
        """
        :type _ociCamera: OCICamera
        """
        # void DeleteCamera(OCICamera _ociCamera)
        pass

    def AddRoute(self):
        # void AddRoute()
        pass

    def SetACE(self, _no):
        """
        :type _no: int
        """
        # void SetACE(int _no)
        pass

    def SetSunCaster(self, _key):
        """
        :type _key: int
        """
        # void SetSunCaster(int _key)
        pass

    def UpdateCharaFKColor(self):
        # void UpdateCharaFKColor()
        pass

    def UpdateItemFKColor(self):
        # void UpdateItemFKColor()
        pass

    def Duplicate(self):
        # void Duplicate()
        pass

    def SaveScene(self):
        # void SaveScene()
        pass

    def LoadScene(self, _path):
        """
        :type _path: string
        """
        # bool LoadScene(string _path)
        pass

    def LoadSceneCoroutine(self, _path):
        """
        :type _path: string
        """
        # IEnumerator LoadSceneCoroutine(string _path)
        pass

    def ImportScene(self, _path):
        """
        :type _path: string
        """
        # bool ImportScene(string _path)
        pass

    def InitScene(self, _close):
        """
        :type _close: bool
        """
        # void InitScene(bool _close = true)
        pass

    def OnDeleteNode(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # void OnDeleteNode(TreeNodeObject _node)
        pass

    def OnParentage(self, _parent, _child):
        """
        :type _parent: TreeNodeObject
        :type _child:  TreeNodeObject
        """
        # void OnParentage(TreeNodeObject _parent, TreeNodeObject _child)
        pass

    def ResetOption(self):
        # void ResetOption()
        pass

    def LoadOption(self):
        # void LoadOption()
        pass

    def SaveOption(self):
        # void SaveOption()
        pass

    def AddInfo(self, _info, _ctrlInfo):
        """
        :type _info: ObjectInfo
        :type _ctrlInfo:  ObjectCtrlInfo
        """
        # static void AddInfo(ObjectInfo _info, ObjectCtrlInfo _ctrlInfo)
        pass

    def DeleteInfo(self, _info, _delKey):
        """
        :type _info: ObjectInfo
        :type _delKey:  bool
        """
        # static void DeleteInfo(ObjectInfo _info, bool _delKey = true)
        pass

    def GetInfo(self, _key):
        """
        :type _key: int
        """
        # static ObjectInfo GetInfo(int _key)
        pass

    def AddObjectCtrlInfo(self, _ctrlInfo):
        """
        :type _ctrlInfo: ObjectCtrlInfo
        """
        # static void AddObjectCtrlInfo(ObjectCtrlInfo _ctrlInfo)
        pass

    def GetCtrlInfo(self, _key):
        """
        :type _key: int
        """
        # static ObjectCtrlInfo GetCtrlInfo(int _key)
        pass

    def AddNode(self, _name, _parent):
        """
        :type _name: string
        :type _parent:  TreeNodeObject
        """
        # static TreeNodeObject AddNode(string _name, TreeNodeObject _parent = null)
        pass

    def DeleteNode(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # static void DeleteNode(TreeNodeObject _node)
        pass

    def AddCtrlInfo(self, _info):
        """
        :type _info: ObjectCtrlInfo
        """
        # static void AddCtrlInfo(ObjectCtrlInfo _info)
        pass

    def GetCtrlInfo(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # static ObjectCtrlInfo GetCtrlInfo(TreeNodeObject _node)
        pass

    def GetNewIndex(self):
        # static int GetNewIndex()
        pass

    def SetNewIndex(self, _index):
        """
        :type _index: int
        """
        # static void SetNewIndex(int _index)
        pass

    def DeleteIndex(self, _index):
        """
        :type _index: int
        """
        # static bool DeleteIndex(int _index)
        pass

    def AddLight(self):
        # static void AddLight()
        pass

    def DeleteLight(self):
        # static void DeleteLight()
        pass

    def AddChangeAmount(self, _key, _ca):
        """
        :type _key: int
        :type _ca:  ChangeAmount
        """
        # static void AddChangeAmount(int _key, ChangeAmount _ca)
        pass

    def DeleteChangeAmount(self, _key):
        """
        :type _key: int
        """
        # static bool DeleteChangeAmount(int _key)
        pass

    def GetChangeAmount(self, _key):
        """
        :type _key: int
        """
        # static ChangeAmount GetChangeAmount(int _key)
        pass

    def GetSelectObjectCtrl(self):
        # static ObjectCtrlInfo[] GetSelectObjectCtrl()
        pass

    def Init(self):
        # void Init()
        pass

    def SelectInputField(self, _input, _inputTMP):
        """
        :type _input: InputField
        :type _inputTMP:  TMP_InputField
        """
        # void SelectInputField(InputField _input, TMP_InputField _inputTMP)
        pass

    def DeselectInputField(self, _input, _inputTMP):
        """
        :type _input: InputField
        :type _inputTMP:  TMP_InputField
        """
        # void DeselectInputField(InputField _input, TMP_InputField _inputTMP)
        pass

    def ShowName(self, _transform, _name):
        """
        :type _transform: Transform
        :type _name:  string
        """
        # void ShowName(Transform _transform, string _name)
        pass

# TreeNodeCtrl.cs
class TreeNodeCtrl():
    def __init__(self):
        self.onParentage = None # Action<TreeNodeObject, TreeNodeObject> onParentage;
        """:type : Action<TreeNodeObject, TreeNodeObject>"""
        self.onDelete = None # Action<TreeNodeObject> onDelete;
        """:type : Action<TreeNodeObject>"""
        self.onSelect = None # Action<TreeNodeObject> onSelect;
        """:type : Action<TreeNodeObject>"""
        self.onSelectMultiple = None # Action onSelectMultiple;
        """:type : Action"""
        self.onDeselect = None # Action<TreeNodeObject> onDeselect;
        """:type : Action<TreeNodeObject>"""
        self.selectNode = None # TreeNodeObject selectNode
        """:type : TreeNodeObject"""
        self.selectNodes = None # TreeNodeObject[] selectNodes => hashSelectNode.ToArray();
        """:type : TreeNodeObject[]"""
        self.selectObjectCtrl = None # ObjectCtrlInfo[] selectObjectCtrl
        """:type : ObjectCtrlInfo[]"""
    def AddNode(self, _name, _parent):
        """
        :type _name: string
        :type _parent:  TreeNodeObject
        """
        # TreeNodeObject AddNode(string _name, TreeNodeObject _parent = null)
        pass

    def AddNode(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # bool AddNode(TreeNodeObject _node)
        pass

    def RemoveNode(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # void RemoveNode(TreeNodeObject _node)
        pass

    def CheckNode(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # bool CheckNode(TreeNodeObject _node)
        pass

    def DeleteNode(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # void DeleteNode(TreeNodeObject _node)
        pass

    def DeleteAllNode(self):
        # void DeleteAllNode()
        pass

    def GetNode(self, _index):
        """
        :type _index: int
        """
        # TreeNodeObject GetNode(int _index)
        pass

    def SetParent(self, _node, _parent):
        """
        :type _node: TreeNodeObject
        :type _parent:  TreeNodeObject
        """
        # void SetParent(TreeNodeObject _node, TreeNodeObject _parent)
        pass

    def RefreshHierachy(self):
        # void RefreshHierachy()
        pass

    def SetParent(self):
        # void SetParent()
        pass

    def RemoveNode(self):
        # void RemoveNode()
        pass

    def DeleteNode(self):
        # void DeleteNode()
        pass

    def CopyChangeAmount(self):
        # void CopyChangeAmount()
        pass

    def SelectMultiple(self, _start, _end):
        """
        :type _start: TreeNodeObject
        :type _end:  TreeNodeObject
        """
        # void SelectMultiple(TreeNodeObject _start, TreeNodeObject _end)
        pass

    def SelectSingle(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # void SelectSingle(TreeNodeObject _node)
        pass

    def CheckSelect(self, _node):
        """
        :type _node: TreeNodeObject
        """
        # bool CheckSelect(TreeNodeObject _node)
        pass

    def OnPointerDown(self, eventData):
        """
        :type eventData: PointerEventData
        """
        # void OnPointerDown(PointerEventData eventData)
        pass

# TreeNodeObject.cs
class TreeNodeObject():
    def __init__(self):
        self.onVisible = None # OnVisibleFunc onVisible;
        """:type : OnVisibleFunc"""
        self.treeNode = None # TreeNode treeNode => m_TreeNode;
        """:type : TreeNode"""
        self.buttonState = None # Button buttonState => m_ButtonState;
        """:type : Button"""
        self.buttonSelect = None # Button buttonSelect => m_ButtonSelect;
        """:type : Button"""
        self.imageSelect = None # Image imageSelect => m_ImageSelect;
        """:type : Image"""
        self.colorSelect = None # Color colorSelect
        """:type : Color"""
        self.textName = None # string textName
        """:type : string"""
        self.treeState = None # TreeState treeState
        """:type : TreeState"""
        self.imageState = None # Image imageState
        """:type : Image"""
        self.visible = None # bool visible
        """:type : bool"""
        self.buttonVisible = None # Button buttonVisible => m_ButtonVisible;
        """:type : Button"""
        self.imageVisible = None # Image imageVisible
        """:type : Image"""
        self.imageVisibleWidth = None # float imageVisibleWidth
        """:type : float"""
        self.enableVisible = None # bool enableVisible
        """:type : bool"""
        self.rectNode = None # RectTransform rectNode => _rectNode;
        """:type : RectTransform"""
        self.parent = None # TreeNodeObject parent
        """:type : TreeNodeObject"""
        self.isParent = None # bool isParent => (Object)parent != (Object)null && enableChangeParent;
        """:type : bool"""
        self.childCount = None # int childCount => m_child.Count;
        """:type : int"""
        self.child = None # List<TreeNodeObject> child => m_child;
        """:type : List<TreeNodeObject>"""
        self.enableChangeParent = None # bool enableChangeParent
        """:type : bool"""
        self.enableDelete = None # bool enableDelete
        """:type : bool"""
        self.enableAddChild = None # bool enableAddChild
        """:type : bool"""
        self.enableCopy = None # bool enableCopy
        """:type : bool"""
        self.baseColor = None # Color baseColor
        """:type : Color"""
        self.addPosX = None # float addPosX
        """:type : float"""
        self.childRoot = None # TreeNodeObject childRoot
        """:type : TreeNodeObject"""
    def OnClickState(self):
        # void OnClickState()
        pass

    def OnClickSelect(self):
        # void OnClickSelect()
        pass

    def OnClickVisible(self):
        # void OnClickVisible()
        pass

    def OnDeselect(self):
        # void OnDeselect()
        pass

    def SetParent(self, _parent):
        """
        :type _parent: TreeNodeObject
        """
        # bool SetParent(TreeNodeObject _parent)
        pass

    def AddChild(self, _child):
        """
        :type _child: TreeNodeObject
        """
        # bool AddChild(TreeNodeObject _child)
        pass

    def RemoveChild(self, _child):
        """
        :type _child: TreeNodeObject
        """
        # void RemoveChild(TreeNodeObject _child)
        pass

    def SetTreeState(self, _state):
        """
        :type _state: TreeState
        """
        # void SetTreeState(TreeState _state)
        pass

    def SetVisible(self, _visible):
        """
        :type _visible: bool
        """
        # void SetVisible(bool _visible)
        pass

    def ResetVisible(self):
        # void ResetVisible()
        pass

    def Select(self, _button):
        """
        :type _button: bool
        """
        # void Select(bool _button = false)
        pass

