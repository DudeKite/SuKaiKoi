"""
VN Scene Script Ext - keitaro10
"""
def custom_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    # ------- texts --------
    if act["action"] == "gagwparam":
        # example of simple action
        if hasattr(game.gdata, 'gagStWork'):
            params = game.gdata.gagStWork
            if params:
                par = act["actionparam"]
                parval = int(act["actionparam2"])
                pardesc = act["actionparam3"]
                if par in params:
                    params[par] += parval
                else:
                    params[par] = parval
                params["desc_"+par] = pardesc

        #game.set_text_s(act["actionparam"])
        return True



    # cameras
    if act["action"] == "camanimt":
        game.anim_to_camera_num(float(act["actionparam2"]), int(act["actionparam"]), "fast-slow")
        return True

    if act["action"] == "camanimt2":
        game.anim_to_camera_num(float(act["actionparam3"]), int(act["actionparam"]),
                                {'style': "linear", 'target_camera_zooming_in': float(act["actionparam2"])})
        return True

    # old functions
    if act["action"] == "chanrestart":
        try:
            dicobjctrl = game.studio.dicInfo
            tnodeobjchar = act["treeobj"].parent.parent.parent
            objctrl = dicobjctrl[tnodeobjchar]
            # octrl must be OCIChar object
            from Studio import OCIChar
            if isinstance(objctrl, OCIChar):
                # i use my support object HSNeoOCIChar, but you can do what you want with founded OCIChar object
                # params can be found in scene dump
                from vngameengine import HSNeoOCIChar
                obj = HSNeoOCIChar(objctrl)

                obj.restart_anime()
            else:
                game.show_blocking_message_time("ERROR: action %s is not located under char head"%act["origintext"])
        except Exception, e:
            game.show_blocking_message_time("ERROR: action %s is not located under char head"%act["origintext"])


        return True

    if act["action"] == "chanspeed":
        try:
            dicobjctrl = game.studio.dicInfo
            tnodeobjchar = act["treeobj"].parent.parent.parent
            objctrl = dicobjctrl[tnodeobjchar]
            # octrl must be OCIChar object
            from Studio import OCIChar
            if isinstance(objctrl, OCIChar):
                # i use my support object HSNeoOCIChar, but you can do what you want with founded OCIChar object
                # params can be found in scene dump
                from vngameengine import HSNeoOCIChar
                obj = HSNeoOCIChar(objctrl)

                obj.objctrl.animeSpeed = float(act["actionparam"])
            else:
                game.show_blocking_message_time("ERROR: action %s is not located under char head"%act["origintext"])
        except Exception, e:
            game.show_blocking_message_time("ERROR: action %s is not located under char head"%act["origintext"])


        return True



def debug_buttons(game,state):
    return [] # if we want no additional buttons

    # return in format of set_buttons_alt
    #return ["Demo btn (keitaro10)", demo1]

