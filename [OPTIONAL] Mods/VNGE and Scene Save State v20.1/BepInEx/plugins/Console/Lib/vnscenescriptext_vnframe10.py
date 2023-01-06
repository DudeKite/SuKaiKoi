"""
VN Scene Script Ext - vnframe10
Provide functions to call VNFrame acts and anime functions

f_stinit, f_acts, f_actm, f_act, f_anime

Examples:
(init)
:useext:vnframe10
:a:i:f_stinit
(actual actions)
:a:0:f_acts:main:anim:(0,0,0)
:a:2:f_actm:main::{'anim':(7, 20, 2)}
:a:0:f_act:::{'desk': {'move_to': (1.043, 0.000, -0.810)}}
:a:3:f_act:::{'main': {'anim': (0, 4, 0), 'rotate_to': (0.000, 10.000, 0.000), 'anim_spd': 0.000}}
:a:4:f_act:::{'main': {'anim_spd': 1.000}}
:a:5:f_anime:::(({ 'desk': {'move_to': ((1.043, 0.000, -0.810), (1.043, 0.000, -0.362))},}, 1.00, 'linear'),)
:a:0:f_acts:sys:text:('s', 'Start pos!')
"""

import vnframe

def custom_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    # ------- texts --------
    if act["action"] == "f_stinit":
        # example of simple action
        vnframe.register_actor_prop_by_tag(game)
        vnframe.init_scene_anime(game)
        game.isLockWindowDuringSceneAnimation = True
        return True

    if act["action"] == "f_acts":
        try:
            import ast
            obj1 = ast.literal_eval(act["actionparam3"])
        except Exception, e:
            print "f_acts error, can't parse param %s"%act["actionparam3"]
            return True
        script = {act["actionparam"]: {act["actionparam2"]: obj1}}
        vnframe.act(game, script)

        #print "f_acts: ", script

        return True

    if act["action"] == "f_actm":
        try:
            import ast
            obj1 = ast.literal_eval(act["actionparam3"])
        except Exception, e:
            print "f_actm error, can't parse param %s"%act["actionparam3"]
            return True
        script = {act["actionparam"]: obj1}
        vnframe.act(game, script)

        #print "f_acts: ", script

        return True

    if act["action"] == "f_act":
        try:
            import ast
            obj1 = ast.literal_eval(act["actionparam3"])
        except Exception, e:
            print "f_act error, can't parse param %s"%act["actionparam3"]
            return True
        script = obj1
        vnframe.act(game, script)

        #print "f_acts: ", script

        return True

    if act["action"] == "f_anime":
        try:
            import ast
            obj1 = ast.literal_eval(act["actionparam3"])
        except Exception, e:
            print "f_act error, can't parse param %s"%act["actionparam3"]
            return True
        script = obj1
        vnframe.anime(game, script)

        #print "f_acts: ", script

        return True

    return False


# -----

def debug_buttons(game,state):
    return [] # if we want no additional buttons

    # return in format of set_buttons_alt
    #return ["Demo btn (keitaro10)", demo1]

def demo1(game):
    """:type game: vngameengine.VNNeoController"""
    game.show_blocking_message_time("Some demo message")