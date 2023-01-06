"""
VN Scene Script Ext - vnframe11
Provide functions to call VNFrame acts and anime functions

f_stinit, f_acts, f_actm, f_act, f_anime

1.1 - added f_synch and f_animclipnum
1.1.1 - also added synch as synonym for f_synch
1.1.2 - synch can take only 1 actionparam, for some special H-anime
        add 'synchr' cmd which sync and restart anime, BUT may cause anime change?? 
1.2 - add "f_height" and "f_breast" function


Function: f_height - set actor's height
Syntax:
    f_height:actorid:height
Examples:
    f_height:act0:0.5


Function: f_breast - set actor's breast size
Syntax:
    f_breast:actorid:breastsize
Examples:
    f_breast:act0:0.5


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

    # f_synch/synch : sync h anime aux param to female's height and breast
    # sample: f_synch:femaleid:[maleid]
    if act["action"] == "f_synch" or act["action"] == "synch":
        # example of simple action
        fid = act["actionparam"]
        factor = game.scenef_get_actor(fid)
        anime_option_param = (factor.height, factor.breast)
        #if factor.isHAnime:
        factor.set_anime_option_param(anime_option_param)
 
        if "actionparam2" in act.keys():
            mid = act["actionparam2"]
            mactor = game.scenef_get_actor(mid)
            #if mactor.isHAnime:
            mactor.set_anime_option_param(anime_option_param)

        return True

    # f_synchr/synchr : sync h anime aux param to female's height and breast, and restart anime
    # sample: f_synchr:femaleid:[maleid]
    if act["action"] == "f_synchr" or act["action"] == "synchr":
        # example of simple action
        fid = act["actionparam"]
        factor = game.scenef_get_actor(fid)
        anime_option_param = (factor.height, factor.breast)
        #if factor.isHAnime:
        factor.set_anime_option_param(anime_option_param)
        factor.restart_anime()
 
        if "actionparam2" in act.keys():
            mid = act["actionparam2"]
            mactor = game.scenef_get_actor(mid)
            #if mactor.isHAnime:
            mactor.set_anime_option_param(anime_option_param)
            mactor.restart_anime()

        return True

    # f_height: set actor's height
    # sample: f_height:actorid:height
    if act["action"] == "f_height":
        try:
            fid = act["actionparam"]
            factor = game.scenef_get_actor(fid)
            heightvalue = float(act["actionparam2"])
            factor.height = heightvalue
            #print "set height of %s to %f"%(factor.text_name, heightvalue)
            return True

        except Exception, e:
            print "f_height error, can't parse command '%s':"%act["origintext"], e
            return True

    # f_breast: set actor's breast
    # sample: f_breast:actorid:breast
    if act["action"] == "f_breast":
        try:
            fid = act["actionparam"]
            factor = game.scenef_get_actor(fid)
            breastvalue = float(act["actionparam2"])
            factor.breast = breastvalue
            #print "set breast of %s to %f"%(factor.text_name, heightvalue)
            return True

        except Exception, e:
            print "f_breast error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "f_animclipnum":
        fid = act["actionparam"]
        factor = game.scenef_get_actor(fid)

        curanim = list(factor.get_animate())
        curanim[2] = int(act["actionparam2"])
        factor.animate(curanim[0], curanim[1], curanim[2])

        return True

    import vnscenescriptext_vnframe10
    return vnscenescriptext_vnframe10.custom_action(game,act)


# -----

def debug_buttons(game,state):
    return [] # if we want no additional buttons

    # return in format of set_buttons_alt
    #return ["Demo btn (keitaro10)", demo1]

def demo1(game):
    """:type game: vngameengine.VNNeoController"""
    game.show_blocking_message_time("Some demo message")