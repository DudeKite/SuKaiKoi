"""
vn game engine Face expressions
v1.0
- first version by Keitaro (see simplegamedemoadv2 - with lipsync - for example)
v1.1
- added conf_neo_male by @cochese42

"""
def init_faceexpressions(game):
    """:type game: vngameengine.VNNeoController"""
    game.event_reg_listener("set_text", faceexp_text_handler)

# neo config
conf_neo_male = {
    'normal': {'mouth': 1, 'eyes': 0, 'eyes_open': 1.000},
    'angry_whatyousay': {'mouth': 5, 'eyes': 4, 'eyes_open': 1.000},
    'glare': {'eyes': 0, 'eyes_open': 1.000, 'mouth': 0, 'mouth_open': 0.000},
    'blank_stare': {'eyes': 0, 'eyes_open': 0.772, 'mouth': 0, 'mouth_open': 0.169},
    'tired_stare': {'eyes': 0, 'eyes_open': 0.478, 'mouth': 0, 'mouth_open': 0.426},
    'sleeping': {'eyes': 0, 'eyes_open': 0.051, 'mouth': 0, 'mouth_open': 0.721},
    'normal_smile': {'eyes': 0, 'eyes_open': 1, 'mouth': 1, 'mouth_open': 0},
    'happy_smile': {'eyes': 3, 'eyes_open': 1, 'mouth': 1, 'mouth_open': 1},
    'very_happy_smile': {'eyes': 3, 'eyes_open': 1, 'mouth': 2, 'mouth_open': 1},
    'kind_smile': {'eyes': 3, 'eyes_open': 1, 'mouth': 1, 'mouth_open': 0},
    'angry_smile': {'eyes': 4, 'eyes_open': 1, 'mouth': 1, 'mouth_open': 1},
    'evil_smile': {'eyes': 4, 'eyes_open': 1, 'mouth': 1, 'mouth_open': 0},
    'concentration': {'eyes': 4, 'eyes_open': 0, 'mouth': 1, 'mouth_open': 0},
    'unhappy': {'eyes': 4, 'eyes_open': 1, 'mouth': 0, 'mouth_open': 0},
    'unhappy_talking': {'eyes': 4, 'eyes_open': 1, 'mouth': 0, 'mouth_open': 0.8},
    'unhappy_eyes_closed': {'eyes': 4, 'eyes_open': 0, 'mouth': 0, 'mouth_open': 0},
    'surprise_smile': {'eyes': 5, 'eyes_open': 1, 'mouth': 1, 'mouth_open': 1},
    'stunned_smile': {'eyes': 5, 'eyes_open': 1, 'mouth': 1, 'mouth_open': 0},
    'stunned': {'eyes': 5, 'eyes_open': 1, 'mouth': 0, 'mouth_open': 0},
    'shocked': {'eyes': 5, 'eyes_open': 1, 'mouth': 0, 'mouth_open': 1},
    'sad': {'eyes': 5, 'eyes_open': 1, 'mouth': 0, 'mouth_open': 0},
    'sad_shocked': {'eyes': 5, 'eyes_open': 1, 'mouth': 0, 'mouth_open': 0.5},
    'laughing': {'eyes': 10, 'eyes_open': 1, 'mouth': 2, 'mouth_open': 1},
    'smiling_talking': {'eyes': 3, 'eyes_open': 1, 'mouth': 2, 'mouth_open': 0.5},
    'very_angry': {'eyes': 4, 'eyes_open': 1, 'mouth': 3, 'mouth_open': 0},
    'very_angry_talking': {'eyes': 4, 'eyes_open': 1, 'mouth': 3, 'mouth_open': 0.5},
    'very_angry_shouting': {'eyes': 4, 'eyes_open': 1, 'mouth': 3, 'mouth_open': 1},
    'crying': {'eyes': 3, 'eyes_open': 1, 'mouth': 3, 'mouth_open': 0.5},
    'serious': {'eyes': 0, 'eyes_open': 1, 'mouth': 3, 'mouth_open': 0},
    'serious_talking': {'eyes': 0, 'eyes_open': 1, 'mouth': 3, 'mouth_open': 0.5},
    'serious_shouting': {'eyes': 0, 'eyes_open': 1, 'mouth': 3, 'mouth_open': 1},
    'sexy_smile': {'eyes': 0, 'eyes_open': 0.8, 'mouth': 6, 'mouth_open': 0},
    'thoughtful_smile': {'eyes': 3, 'eyes_open': 1, 'mouth': 7, 'mouth_open': 0},
    'silly_smile': {'eyes': 3, 'eyes_open': 1, 'mouth': 7, 'mouth_open': 0},
}

conf_neo_female = {
    'normal': {'mouth': 1, 'eyes': 0, 'eyes_open': 1.000},
    'angry_whatyousay': {'mouth': 6, 'eyes': 3, 'eyes_open': 1.000,  'mouth_open': 0.245},
}
conf_neo = [conf_neo_male, conf_neo_female]

# playhome config
conf_ph_male = {
}
conf_ph_female = {
}
conf_ph = [conf_ph_male, conf_ph_female]

# charastudio config
conf_chara_male = {
}
conf_chara_female = {
}
conf_chara = [conf_chara_male, conf_chara_female]

#------- main code --------------

def faceexp_text_handler(game, evid, param):
    """:type game: vngameengine.VNNeoController"""
    charfull, text = param

    charA = charfull.split("//")
    char = charA[0]  # charfull may be "me//surprised" etc.
    if len(charA) > 1: # we have additional construct
        faceexp = charA[1]
        actor = game.scenef_get_actor(char)
        if actor != None:
            #print actor.sex
            # studio neo expressions
            if game.isStudioNEO:
                if faceexp in conf_neo[actor.sex]:
                    vnframe_actcompact(game, {char: conf_neo[actor.sex][faceexp]})
            if game.isPlayHomeStudio:
                if faceexp in conf_ph[actor.sex]:
                    vnframe_actcompact(game, {char: conf_ph[actor.sex][faceexp]})
            if game.isCharaStudio:
                if faceexp in conf_chara[actor.sex]:
                    vnframe_actcompact(game, {char: conf_chara[actor.sex][faceexp]})

# ---- simplified vnactor script call ----------

from vnactor import cam_act_funcs, sys_act_funcs, char_act_funcs, prop_act_funcs, export_sys_status

def vnframe_actcompact(game, script):
    """:type game: vngameengine.VNNeoController"""
    # act script must be a dict
    # script: { 'tgt1' : {'tgt_fuc1' : tgt_func1_param, 'tgt_func2' : tgt_func2_param, ... }, 'tgt2' : {...}, ... }
    # tgt can be "cam" for camera, "sys" for system, actor name for actor or prop name for prop
    actors = game.scenef_get_all_actors()
    for tgt in script:
        try:
            # If this is a character in this scene
            if tgt in actors:
                for f in script[tgt]:
                    if f in char_act_funcs:
                        char_act_funcs[f][0](actors[tgt], script[tgt][f])
                    else:
                        print "act error: unknown function '%s' for '%s'!"%(f, tgt)
            else:
                print "act error: unknown target '%s'!"%(tgt)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print "act error in process tgt='%s' script='%s'"%(tgt, script[tgt]) + " : " + str(e)
