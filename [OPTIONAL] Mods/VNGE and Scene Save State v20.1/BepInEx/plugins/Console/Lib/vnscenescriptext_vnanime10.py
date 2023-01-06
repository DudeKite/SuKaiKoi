"""
VN Scene Script Ext - vnanime10
Provide functions to call VNAnime functions to play key frame clips

f_clipinit,
f_clipplay,
f_clippause,
f_clipstop,
f_clipseek,

v1.1: auto initialize for more safely use


Function: f_clipinit - initialize vnanime for vn scene script, and it will load all clips in scene
Syntax:
    :a:i:f_clipinit
Examples:
    :useext:vnanime10
    :a:i:f_clipinit


Function: f_clipplay - play specified clip
Syntax:
    :a:n:f_clipplay:clipname:[loop]:[speed]
    where 'clipname': assign a clip to play
                      if omitted, start all clips. In this case, loop and speed setting are ignored.
          'loop'    : 0 for no loop (= play once), 1 for loop once (= play twice), and so on, -1 for loop forever.
                      if omitted, use the clip's default loop setting.
          'speed'   : playback speed rate. 1 for normal play speed, 2 for double play speed, and so on.
                      if omitted, play at noraml speed.
Examples:
    :a:1:f_clipplay
    :a:1:f_clipplay:clip1
    :a:1:f_clipplay:clip2:-1
    :a:1:f_clipplay:clip3::2
    :a:1:f_clipplay:clip4:0:2


Function: f_clippause - pause specified clip (call f_clipplay will resume the anime)
Syntax:
    :a:n:f_clippause:clipname
    where 'clipname': assign a clip to pause. If omitted, pause all clips.
Examples:
    :a:1:f_clippause
    :a:1:f_clippause:clip1


Function: f_clipstop - stop specified clip (call f_clipplay will restart the anime)
Syntax:
    :a:n:f_clipstop:clipname
    where 'clipname': assign a clip to stop. If omitted, stop all clips.
Examples:
    :a:1:f_clipstop
    :a:1:f_clipstop:clip1


Function: f_clipseek - seek to specified frame of a clip
Syntax:
    :a:n:f_clipseek:clipname:frame
    where 'clipname': assign a clip.
          'frame'   : frame number want to seek to
Examples:
    :a:1:f_clipseek
    :a:1:f_clipseek:clip1

"""

import vnanime

def custom_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    # safe start
    if not vnanime.check_keyframe_anime(game):
        vnanime.init_keyframe_anime(game)

    # ------- texts --------
    if act["action"] == "f_clipinit":
        # init clip anime
        vnanime.init_keyframe_anime(game)
        return True

    if act["action"] == "f_clipplay":
        #print act
        try:
            if act.has_key("actionparam") and len(act["actionparam"]) > 0:
                # get clip by name
                clipname = act["actionparam"]
                tgtClip = game.gdata.kfaManagedClips[clipname]
                # get loop setting
                if act.has_key("actionparam2") and len(act["actionparam2"]) > 0:
                    loop = int(act["actionparam2"])
                else:
                    loop = None
                # set speed
                if act.has_key("actionparam3") and len(act["actionparam3"]) > 0:
                    speed = float(act["actionparam3"])
                    tgtClip.speed = speed
                # play it
                tgtClip.play(loop)
            else:
                # play all
                vnanime.kfa_playAll(game)
            return True
        except Exception, e:
            print "f_clipplay error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "f_clippause":
        try:
            if act.has_key("actionparam") and len(act["actionparam"]) > 0:
                # pause it
                vnanime.kfa_pause(game, act["actionparam"])
            else:
                # pause all
                vnanime.kfa_pauseAll(game)
            return True
        except Exception, e:
            print "f_clippause error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "f_clipstop":
        try:
            if act.has_key("actionparam") and len(act["actionparam"]) > 0:
                # stop it
                vnanime.kfa_stop(game, act["actionparam"])
            else:
                # stop all
                vnanime.kfa_stopAll(game)
            return True
        except Exception, e:
            print "f_clipstop error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "f_clipseek":
        try:
            # seek
            clipname = act["actionparam"]
            pos = int(act["actionparam2"])
            vnanime.kfa_seek(game, clipname, pos)
            return True
        except Exception, e:
            print "f_clipseek error, can't parse command '%s':"%act["origintext"], e
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