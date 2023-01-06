"""
VN Scene Script Ext - objcam10
by Countd360
Provide functions to support switch between object camera

objcam,

Function: objcam - switch to object camera name with 'name', if 'name' is empty, switch to normal camera
Syntax:
    :a:n:objcam:name
Examples:
    :a:n:objcam:camera1
    :a:n:objcam:

"""

def custom_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    if act["action"] == "objcam":
        try:
            cname = act["actionparam"]
            #from vnactor import set_camera_name
            #set_camera_name(game, cname)
            def do_set_camera_timer(game):
                from vnactor import set_camera_name
                set_camera_name(game, game.scenedata.vnsstempSetObjCameraName)
            game.scenedata.vnsstempSetObjCameraName = cname
            tid = game.set_timer(0.1, do_set_camera_timer, None)

            return True
        except Exception, e:
            print "objcam error, can't parse command '%s':"%act["origintext"], e
            return True


def debug_buttons(game,state):
    return [] # if we want no additional buttons

    # return in format of set_buttons_alt
    #return ["Demo btn (keitaro10)", demo1]