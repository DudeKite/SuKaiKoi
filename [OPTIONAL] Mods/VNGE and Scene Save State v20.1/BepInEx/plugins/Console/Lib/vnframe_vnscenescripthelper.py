#===============================================================================================
# VNFrame Supporter fot VNSceneScript
# v1.0
#===============================================================================================

from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Input, KeyCode

def sshelper_onelineinterface(sh):
    if hasattr(sh, 'dumpClipToVNSceneScript'):
        pass
    else:
        sh.dumpClipToVNSceneScript = False
        sh.dumpClipToVNSceneScriptFile = False
        sh.dumpClipToVNSceneScriptScene = False
        sh.dumpClipVNSSExcludeFKIKVoice = True

    if sh.curSCInfo.dumpAsIndex == 0: # only act for now
        GUILayout.BeginHorizontal();
        #GUILayout.Label("VNSceneScript save", GUILayout.Width(160))
        sh.dumpClipToVNSceneScript = GUILayout.Toggle(sh.dumpClipToVNSceneScript, "VNSceneScript Save", GUILayout.Width(150))
        if sh.dumpClipToVNSceneScript:
            sh.dumpClipToVNSceneScriptFile = GUILayout.Toggle(sh.dumpClipToVNSceneScriptFile, "To file", GUILayout.Width(60))
            sh.dumpClipToVNSceneScriptScene = GUILayout.Toggle(sh.dumpClipToVNSceneScriptScene, "To scene",
                                                              GUILayout.Width(70))
            sh.dumpClipVNSSExcludeFKIKVoice = GUILayout.Toggle(sh.dumpClipVNSSExcludeFKIKVoice, "EXCLUDE FK&IK&Voice",
                                                              GUILayout.Width(170))

        GUILayout.EndHorizontal();

def dumpclip_toscenescript(sh,output):
    if sh.curSCInfo.dumpAsIndex == 0:  # only act for now
        if sh.dumpClipToVNSceneScript:
            arstr = []
            try:
                sh = sh
                """:type : vnframe.ScriptHelper"""

                # preprocessing
                output = output.replace(", act,", ', "act",')
                output = output[:-2]
                output = output.strip()

                #print output
                try:
                    import ast
                    obj = ast.literal_eval(output)
                except Exception as e:
                    err = "dumpclip_toscenescript parsing output error: %s" % (str(e))
                    print err
                    return err
                #print "We parsed succesfully!"
                #print "Here?"


                import vnframe
                arstr.append("txtf:%s::%s"%(obj[0],obj[1]))
                if obj[2] == "act":
                    acto = obj[3]

                    #objstatus = acto[key]
                    #if sh.dumpClipVNSSExcludeFKIKVoice:

                    for key in acto:
                        objstatus = acto[key]
                        if sh.dumpClipVNSSExcludeFKIKVoice:
                            if 'voice_lst' in objstatus:
                                del objstatus['voice_lst']
                            if 'voice_rpt' in objstatus:
                                del objstatus['voice_rpt']
                            if 'ik_set' in objstatus:
                                del objstatus['ik_set']
                            if 'ik_active' in objstatus:
                                del objstatus['ik_active']
                            if 'fk_active' in objstatus:
                                del objstatus['fk_active']
                            if 'fk_set' in objstatus:
                                del objstatus['fk_set']
                            if 'kinematic' in objstatus:
                                del objstatus['kinematic']

                        arstr.append("f_actm:%s::%s"%(key, vnframe.script2string(objstatus)))
                #arstr.append("next")

            except Exception as e:
                err = "dumpclip_toscenescript error: %s"%(str(e))
                print err
                return err

            if sh.dumpClipToVNSceneScriptFile:
                try:
                    f = open('vnscene_acode.txt', 'a+')
                    f.write("next\n")
                    f.write("\n".join(arstr))
                    f.write("\n")
                    f.close()
                except Exception as e:
                    err = "dumpclip_toscenescript file error: %s" % (str(e))
                    print err
                    return err

            if sh.dumpClipToVNSceneScriptScene:
                from vngameengine import HSNeoOCIFolder
                foldername = ":acode"
                fold = HSNeoOCIFolder.find_single(foldername)
                if fold == None:
                    # create
                    fold = HSNeoOCIFolder.add(foldername)

                newfld = HSNeoOCIFolder.add("next")
                newfld.set_parent(fold)
                fold = newfld

                for x in arstr:
                    if x != "":
                        newfld = HSNeoOCIFolder.add(x)
                        newfld.set_parent(fold)

            return ""

        return ""


