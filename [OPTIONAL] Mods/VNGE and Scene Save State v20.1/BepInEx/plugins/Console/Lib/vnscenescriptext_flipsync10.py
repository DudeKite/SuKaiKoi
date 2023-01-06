"""
VN Scene Script Ext - flipsync
Provide simple function to init lip-sync in vngameengine

syntax:
:a:i:initflipsync:version[:readspeed]
  version: the version of fake lip-sync you want to use in game, v10 or v11
  readspeed: reading speed parameter, bigger the number faster they read
             12 as default may suit English texts, and for Chinese or Japanese texts 6 will be good.
             if readspeed is omitted, 12 will be used

example:
:a:i:initflipsync:v10
or
:a:i:initflipsync:v11:10


"""
def custom_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    # ------- texts --------
    if act["action"] == "initflipsync":
        game.scenef_register_actorsprops()
        game.isfAutoLipSync = True
        game.fAutoLipSyncVer = act["actionparam"]
        if act.has_key('actionparam2') and len(act['actionparam2']) > 0:
            game.readingSpeed = float(act['actionparam2'])
        return True

# -----

def debug_buttons(game,state):
    return [] # if we want no additional buttons

