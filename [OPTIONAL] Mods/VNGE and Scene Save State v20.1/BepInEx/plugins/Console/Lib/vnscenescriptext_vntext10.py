"""
VN Scene Script Ext - vntext10
Provide functions to call VNText functions to change vntext in scene

f_dyntext,

v1.0: 
- add f_dyntext function


Function: f_dyntext - update dynamic texts
Syntax:
    :a:n:f_dyntext:::textinfo
    where 'textinfo': dynamic text info export from VNTextManager

"""

def custom_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    if act["action"] == "f_dyntext":
        try:
            textinfo = act["actionparam3"]
            from vntext import get_vntext_manager
            mgr = get_vntext_manager(game)
            mgr.importDynamicTextSetting(textinfo)

            return True
        except Exception, e:
            print "vntext error, can't parse command '%s':"%act["origintext"], e
            return True


def debug_buttons(game,state):
    return [] # if we want no additional buttons

    # return in format of set_buttons_alt
    #return ["Demo btn (keitaro10)", demo1]