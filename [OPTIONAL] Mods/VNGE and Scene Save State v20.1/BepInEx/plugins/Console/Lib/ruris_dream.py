#vngame;studio;Demo intro - Ruris Dream
# demo was provided by Kningets on HongFire
import hs
from Manager import Studio
from UnityEngine import Vector3

studio = Studio.Instance

def start(game):
    # Setup
    #game.isDevDumpButtons = True
    game.sceneDir = "gamedemo/"
    game.btnNextText = ">>"
        
    game.register_char("ruri", "ffaaaa", "Ruri")
    game.register_char("elf", "aaffaa", "Nanaya")

    # Start intro
    intro(game)

# Game functions

# Make a list of chars in a scene
# scene: filename of scene
# cast: {'female': ['girl1', 'girl2'], 'male': ['man1']}
def enumerate_chars(game, cast):
    game.scene_cast = {}
    game.scene_stcast = {}
    # Add girls
    t = list()
    for c in studio.femaleList:
        t.insert(0, c.Value.female)
    for c in cast['female']:
        game.scene_cast[c] = t.pop()
    # Add men
    #t = list()
    #for c in studio.maleList:
    #    t.insert(0, c.Value.male)
    #for c in cast['male']:
    #    game.scene_cast[c] = t.pop()

def load_scene_cast(game, param):
    game.load_scene(param['scene'])
    
    # waiting for loading scene and then use enumerate_chars
    game.scene_cast = param['cast']
    game.set_timer(0.5,_enumerate_chars_timer)
    #enumerate_chars(game, param['cast'])

def _enumerate_chars_timer(game):
    enumerate_chars(game, game.scene_cast)
    
# Acting functions
# script: {'girl1': {'visible': True, 'eye_open': 0.3}}
# All scripts: fun(char, param)
def char_clothes(char, param):
    char.chaClothes.SetClothesStateAll(param)
    
def char_eyes(char, param):
    char.ChangeEyesPtn(param)

# Eyes direction: 0 straight, 1 cam, 2 divert, 3 fixed
def char_eyes_look(char, param):
    char.ChangeLookEyesPtn(param)

# Eye open, param: 0.0-1.0
def char_eyes_open(char, param):
    char.ChangeEyesOpen(param)

# "Juice" param: ([0-2], [0-2], [0-2], [0-2], [0-2])
def char_juice(char, param):
    ok, stChar = hs.get_studio_char_from_char(char)
    if stChar.sexType == 1:      # Only for girls
        stChar.body.siruNewLv = param

def char_load_anim(char, param):
    hs.load_animation(char, param[0], param[1])

def char_mouth(char, param):
    char.ChangeMouthPtn(param)

def char_mouth_open(char, param):
    char.ChangeMouthOpen(param)

# Neck direction: 0 straight, 1 cam, 2 divert, 3 anim, 4 fixed
def char_neck_look(char, param):
    char.ChangeLookNeckPtn(param)

def char_move(char, param):
    ok, stChara = hs.get_studio_char_from_char(char)
    if 'pos' in param:
        stChara.objCtrl.transform.localPosition = Vector3(param['pos'][0], param['pos'][1], param['pos'][2])
    if 'rot' in param:
        stChara.objCtrl.transform.localEulerAngles = Vector3(param['rot'][0], param['rot'][1], param['rot'][2])

def char_play_clip(char, param):
    ok, stChara = hs.get_studio_char_from_char(char)
    stChara.anmMng.anmData.clipName = param
    stChara.anmMng.animator.Play(param, 0, 0.0)

def char_visible(char, param):
    char.visibleAll = param

act_funcs = {
        'anim': char_load_anim,
        'clothes': char_clothes,
        'clip': char_play_clip,
        'eyes': char_eyes,
        'eyes_open': char_eyes_open,
        'juice': char_juice,
        'look': char_eyes_look,
        'face': char_neck_look,
        'mouth': char_mouth,
        'mouth_open': char_mouth_open,
        'move': char_move,
        'visible': char_visible,
        }

def camera_pos(param):
    if 'angle' in param:
        hs.move_camera(angle=param['angle'])
    if 'dir' in param:
        hs.move_camera(dir=param['dir'])
    if 'fov' in param:
        hs.move_camera(fov=param['fov'])
    if 'pos' in param:
        hs.move_camera(pos=param['pos'])

def camera_pos_anim(game, param):
    game.anim_to_camera(2.5, param['pos'], param['dir'], param['angle'], 23.0, "fast-slow4")
        
def camera_goto(param):
    if param >= 1 and param <= 5:
        studio.studioUICamera.CameraLoadState(param-1)

#FIXME: Can't save position right after a camera movment. Needs to wait for some kind of update.
def camera_save(param):
    if param >= 1 and param <= 5:
        #studio.studioUICamera.CameraSaveState(param-1) # for later
        return

##  
def act(game, script):
    for char in script:
        # Handle some "characters" special
        if char == "cam":
            camera_pos(script[char])
            #camera_pos_anim(game, script[char]) # if you want animated movements
        if char == "cam_goto":
            camera_goto(script[char])
        if char == "cam_save":
            camera_save(script[char])
        # If this is a character in this scene
        if char in game.scene_cast:
            for f in script[char]:
                if f in act_funcs:
                    act_funcs[f](game.scene_cast[char], script[char][f])

# Scenes
def intro(game):
    game.texts_next([
        ["ruri", "Zzzz....", load_scene_cast, {'scene': 'intro_ruris.png', 'cast': {'female': ['ruri', 'elf']}} ],
        ["elf", "Oh my, what a cute one. It's my lucky night tonight.", act,
            {
                'cam': {'pos': (0.9, 0.5, -2.2), 'dir': (0.0, 0.0, -4.1), 'angle': (22.6, -266.1, 0.0), 'fov': 23.0},
                'cam_save': 3,
            },
        ],
        ["ruri", "Zzzz....", act, {'cam_save': 4}],
        ["elf", "Awww, she is so adorable."],
        ["ruri", "... Zzzz...hum.", act, {'ruri': {'eyes_open': 0.6}}],
        ["elf", "Oops. *Poof*", act, {'elf': {'visible': False, 'juice': (0, 0 ,0 ,0 ,0 )}}],
        ["ruri", "Anyone there?..", act, {'ruri': {'eyes_open': 1.0, 'mouth': 7}}],
        ["ruri", "*Yawn* It must have been a dream.", act,
            {
                'ruri':
                    {
                        'look': 0, 'mouth': 1,
                        'anim': ('custom/cf_anim_custom.unity3d', 'edit_F'),
                        'clip': 'suwari_pose_02',
                    }
            }
        ],
        ["ruri", "Maybe I should try to get back to sleep...", act,
            {
                'cam': {'pos': (1.0, 0.6, -1.8), 'dir': (0.0, 0.0, -4.8), 'angle': (5.7, -178.0, 0.0)},
            }
        ],
        ["elf", "*Foop* Hello...", act,
            {
                'elf':
                    {
                        'visible': True, 'anim': ('custom/cf_anim_custom.unity3d', 'edit_F'), 'clip': 'suwari_pose_01',
                        'move': {'pos': (1.2, 0.4, -0.4), 'rot': (0.0, 186.1, 0.0)}
                    },
                'ruri': {'eyes': 11, 'mouth': 7},
            }
        ],
        ["ruri", "AAAAH!"],
        ["ruri", "Who are you?", act, {'ruri': {'eyes': 13, 'mouth': 9}}],
        ["elf", "I'm a dream elf. I can do magic tricks."],
        ["ruri", "Like what?"],
        ["elf", "Undressing you.", act, {'ruri': {'clothes': 2}}],
        ["ruri", "AAAAAH!!!", act, {'ruri': {'eyes': 11, 'mouth': 7}}],
        ["elf", "And getting \"juice\" all over you.", act, {'ruri': {'juice': (2,2,2,2,2)}}],
        ["ruri", "Eeeeww!", act, {'ruri': {'eyes': 9, 'mouth': 16}}],
        ["elf", "And clean it off.", act, {'ruri': {'juice': (0,0,0,0,0)}}],
        ["elf", "And get you dressed again.", act, {'ruri': {'clothes': 0}}],
        ["ruri", "Ok...", act, {'cam_goto': 2, 'ruri': {'eyes': 7, 'mouth': 14}}],
        ["ruri", "...so what do you say...", act, {'ruri': {'look': 1}}],
        ["ruri", "Want to have some fun?", act, {'ruri': {'face': 1}}],
    ], ending)


def ending(game):
    game.set_text("s", "The end. :)")
    game.set_buttons(["Restart game >"], [start])

