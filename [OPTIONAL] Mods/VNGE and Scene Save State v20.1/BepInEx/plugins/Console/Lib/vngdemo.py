#vngame;charastudio;Demos/Laboratory Girl
#for vngameengine 7.5 and vnframe 1.1

# UTF-8 encode is not supported T.T
# -*- coding: UTF-8 -*-
from vnactor import *
from vnframe import *

def start(game):
    from vngameengine import importOrReload
    importOrReload("vnactor")
    importOrReload("vnframe")

    game.gdata.test = "Hello!"

    # -- init game engine ---
    game.isfAutoLipSync = True # enable lip sync in vngameengine

    # -------- some options we want to init ---------
    #game.isDevDumpButtons = True
    game.sceneDir = "wcf\\" # please, move all your scene files in separate folder - to avoid collisions with other vn games
    game.btnNextText = "Next >>" # for localization and other purposes

    game.skin_set_byname("skin_renpy")  # setting RenPy-like skin for visual novel

    # init scene anime
    init_scene_anime(game)

    # auto hide and lock style for your game
    game.isHideWindowDuringCameraAnimation = False
    game.isLockWindowDuringSceneAnimation = True
    
    # load scene and start a timer to init scene after loaded
    game.load_scene("vng1.png")
    game.scnLoadTID = game.set_timer(60, load_scene_timeout, load_scene_wait)
    print "start load scene"
    
def load_scene_timeout(game):
    #if game.sceneLoaded == False:
    toEnd(game, "ERROR: Load scene timeout!")
    
def load_scene_wait(game, dt, time, duration):
    if game.isFuncLocked == False:
        game.clear_timer(game.scnLoadTID)
        init_scene(game)
        print "load and init scene done!\n"

def init_scene(game):
    """:type game: vngameengine.VNNeoController"""
    try:
        # init status
        game.visible = 1
        
        # load scene infomation
        register_actor_prop_by_tag(game)

        # or you can load actors and props manually
        """
        females = game.scene_get_all_females()  # get list<HSNeoOCIChar> of females in scene
        males = game.scene_get_all_males()      # get list<HSNeoOCIChar> of males in scene
        if (len(females) == 0 or len(males) == 0):
            toEnd(game, "ERROR: Lost actor!")
            return
        game.actors['main'] = Actor(females[0].objctrl);
        game.actors['boy'] = Actor(males[0].objctrl);
        for alias in game.actors:
            print type(game.actors[alias]), game.actors[alias].text_name, "as", alias
        # ---------------------------
        # We can define additional characters (other than "s", system)
        # first param is an character ID, second - header text color (RRGGBB), third - name 
        # ---------------------------
        game.register_char("boy", "aa5555", game.actors["boy"].text_name)
        game.register_char("main", "55aa55", game.actors["main"].text_name)
        """
        
        # game start
        start_seq1(game)
        #start_seq2(game)
        #start_seq3(game)

    except Exception as e:
        toEnd(game, "init_scene FAILED: "+str(e))

def start_seq1(game):
    ik_yes = {
    'cf_j_forearm01_R' : (Vector3(0.198, 1.102, 0.128), Vector3(0.000, 0.000, 0.000)),
    'cf_j_arm00_R' : (Vector3(0.103, 1.323, -0.022), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_R' : (Vector3(0.070, 1.295, 0.218), Vector3(309.108, 162.055, 76.854)),
    }

    ik_tp = {
    'cf_j_forearm01_R' : (Vector3(-0.159, 0.646, 0.098), Vector3(0.000, 0.000, 0.000)),
    'cf_j_arm00_R' : (Vector3(-0.100, 0.853, 0.094), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_R' : (Vector3(-0.114, 0.662, -0.059), Vector3(317.159, 67.439, 51.795)),
    }

    ik_hbld = {
    'cf_j_forearm01_R' : (Vector3(-0.202, 0.239, 0.021), Vector3(0.000, 0.000, 0.000)),
    'cf_j_arm00_R' : (Vector3(-0.101, 0.453, 0.016), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_R' : (Vector3(-0.073, 0.283, -0.044), Vector3(12.633, 197.632, 190.210)),
    }   
 
    fk_punch = {
    15: Vector3(309.632, 315.537, 327.395),
    16: Vector3(358.929, 0.672, 0.652),
    17: Vector3(347.281, 355.364, 4.340),
    }
    
    fk_bepunch = {
    0: Vector3(62.783, 179.384, 355.972),
    1: Vector3(326.186, 359.954, 0.000),
    2: Vector3(324.994, 0.000, 0.000),
    3: Vector3(351.745, 359.258, 359.905),
    4: Vector3(349.864, 0.201, 2.180),
    5: Vector3(358.296, 0.265, 4.143),
    6: Vector3(277.573, 263.037, 93.622),
    7: Vector3(79.380, 179.999, 179.999),
    8: Vector3(10.741, 350.609, 355.114),
    9: Vector3(294.093, 327.894, 41.080),
    10: Vector3(288.000, 96.584, 267.842),
    11: Vector3(78.989, 179.987, 179.986),
    12: Vector3(12.833, 6.632, 4.730),
    13: Vector3(294.480, 18.580, 338.026),
    14: Vector3(358.646, 19.956, 3.722),
    15: Vector3(352.752, 332.055, 287.946),
    16: Vector3(334.362, 199.284, 83.422),
    17: Vector3(31.516, 358.408, 42.629),
    18: Vector3(357.981, 330.062, 356.500),
    19: Vector3(355.267, 44.935, 84.263),
    20: Vector3(0.000, 38.162, 0.000),
    21: Vector3(66.054, 354.653, 282.800),
    65: Vector3(0.000, 0.000, 0.000),
    66: Vector3(0.000, 0.000, 0.000),
    67: Vector3(0.000, 0.000, 0.000),
    68: Vector3(0.000, 0.000, 0.000),
    69: Vector3(0.000, 0.000, 0.000),
    }
    
    game.texts_next([
        ["s", "ta..ta..ta..ta..."],
        ["s", "ta..ta..ta..ta............", anime, (
            #({'cam' : {'goto_pos': ((1.093, 0.676, -0.969), (0.000, 0.000, -3.053), (20.300, 217.299, 0.000))}, 'main' : {'eyes_blink' : 0}}),
            #({'cam' : {'goto_pos': ((1.093, 0.676, -0.969), (0.000, 0.000, -3.053), (37.000, 159.550, 0.000), 2.5, 'slow-fast2')}}),
            ({'cam' : {'goto_pos': ((1.003, 0.618, -0.882), (0.000, 0.000, -2.858), (34.550, 211.350, 0.000))}, 'main' : {'eyes_blink' : 0}}),
            ({'cam' : {'goto_pos': ((1.003, 0.641, -0.882), (0.000, 0.000, -2.152), (34.550, 211.350, 0.000), 2.5, 'slow-fast2')}}),
            ({'sys' : {'idle' : 0}}, 0.2),
            ({'tapeff' : {'visible' : 1, 'move_to' : (0.628, 0.322, 0.109)}}),
            ({'sys' : {'idle' : 0}}, 0.2),
            ({'tapeff' : {'move' : (-0.1, 0, 0)}}),
            ({'sys' : {'idle' : 0}}, 0.2),
            ({'tapeff' : {'move' : (0.05, 0, 0)}}),
            ({'sys' : {'idle' : 0}}, 0.2),
            ({'tapeff' : {'move' : (-0.05, -0.05, 0)}}),
            ({'sys' : {'idle' : 0}}, 0.2),
            ({'tapeff' : {'move' : (0.05, 0.05, 0)}}),
            ({'sys' : {'idle' : 0}}, 0.2),
            ({'tapeff' : {'visible' : 0, 'move' : (-0.22, 0, 0)}}),
            ({'sys' : {'idle' : 0}}, 1.8),
            ({'cam' : {'goto_pos': ((0.982, 0.670, -0.966), (0.000, 0.000, -0.965), (36.950, 159.550, 0.000))}}),
            ({'tapeff' : {'visible' : 1}, 'sys' : {'text': ("s", "DA")}}),
        )],
        ["s", "System scaning ......", anime, (
            ({'tapeff' : {'visible' : 0}, 'cam' : {'goto_pos': ((0.002, 0.442, -0.828), (0.000, 0.000, -1.998), (79.850, 180.600, 0.000))}}),
            ({'sys' : {'idle' : 0}}, 0.5),
            ({'cam' : {'goto_pos': ((0.002, 0.442, 0.288), (0.000, 0.000, -1.998), (79.850, 180.600, 0.000), 6)}}),
            ({'scanner' : {'move_to' : ((-0.498, 0.081, -0.242), (-0.498, 0.081, 0.158))}}, 2),
            ({'len2'    : {'color' : (0, 1, 0)}}),
            ({'scanner' : {'move_to' : ((-0.498, 0.081, 0.158), (-0.498, 0.081, 0.558))}}, 2),
            ({'len3'    : {'color' : (0, 1, 0)}}),
            ({'scanner' : {'move_to' : ((-0.498, 0.081, 0.558), (-0.498, 0.081, 0.958))}}, 2),
            ({'len1'    : {'color' : (0, 1, 0)}, 'sys' : {'text': ("s", "System scaning ...... All Green")}}),
        )],
        ["s", "Starting OS.....", anime, (
            ({'cam' : {'goto_pos': ((-0.044, 0.578, -0.208), (0.000, 0.000, -1.988), (8.900, 241.549, 0.000), 2)}}),
            ({'sys' : {'idle' : 0}}, 0.5),
            ({'scanner' : {'rotate_to' : ((0, 0, 0), (0, 0, 90))}}, 2),
            ({'sys' : {'text': ("s", "Starting OS..... Completed")}}),
        )],
        ["dr", "At Last!!!", act, {
            'cam': {'goto_pos': ((0.786, 0.928, -0.409), (0.000, 0.000, -3.333), (1.300, 90.350, -33.204))},
            'chair': {'move_to': (1.3, -0.2, 0.8), 'rotate_to': (0.0, 237.7, 0.0)},
            'dr':  {'move_to': (0.8, 0.0, -0.3), 'turn_to': 241, 'kinematic': 0, 'anim': (0, 2, 2), 'hands': (0, 0)}
        }],
        ["dr", "Hello?", anime, (
            ({'cam'  : {'goto_pos': ((0.011, 0.423, -0.807), (0.000, 0.000, -1.583), (85.750, 146.650, -33.204))}}),
            ({'sys'  : {'idle' : 0}}, 0.5),
            ({'cam'  : {'goto_pos': ((0.011, 0.531, -0.807), (0.000, 0.000, -0.765), (85.750, 146.650, -33.204), 1)}}),
            ({'main' : {'eyes_open' : (0, 1)}}, 1.5, "slow-fast2"),
        )],
        ["main", "...Are you my master?", act, {
            'main' : {'eyes_blink' : 1},
        }],
        ["dr",   "Yes! Yes! Yes! I'm Dr. HAKASE!! How do you feeling?", act, {
            'cam'  : {'goto_pos': ((0.852, 1.016, -0.334), (0.000, 0.000, -3.383), (-8.950, 61.750, 0.000))},
            'dr':  {'anim': (0, 1, 25), 'hands': (0, 1), 'kinematic': 1, 'ik_active': (0, 0, 0, 1, 0), 'ik_set': ik_yes},
        }],
        ["main", "...I don't know...", act, {
            'cam'  : {'goto_pos': ((0.011, 0.531, -0.807), (0.000, 0.000, -0.765), (85.750, 146.650, -33.204))},
        }],
        ["dr",   "That's OK! No hurry! Let's do some simple test."],
        ["dr",   "Try to trace my finger by eyes. Left... right... ", anime, (
            ({ 'main': {'look_at': ((   0, 0, 0.2),(-0.3, 0, 0.2))}}, 2),
            ({ 'main': {'look_at': ((-0.3, 0, 0.2),( 0.3, 0, 0.2))}}, 3),
            ({ 'main': {'look_at': (( 0.3, 0, 0.2),(   0, 0, 0.2))}}, 2),
        )],
        ["dr",   "OK! Now try turn your head to me.", anime, (
            ({ 'main': {'fk_active' : (1, 0, 0, 1, 0, 0, 0), 'face_to': 1, 'look_at': 1}, 'cam'  : {'goto_pos': ((0.011, 0.571, -0.807), (0.000, 0.000, -1.090), (40.050, 236.700, 56.483), 1.5)}}),
            ({ 'sys' : {'idle' : 0}}, 3),
            ({ 'main': {'face_to': 4}}),
        )],
        ["dr",   "Great! So tell me, what is this?", act, {
            'cam': {'goto_pos': ((1.139, 0.729, -0.645), (0.000, 0.000, -3.300), (12.550, 95.250, -33.540))},
            'dr':  {'anim': (0, 4, 10), 'hands': (4, 11)},
            'pen': {'visible': 1},
        }],
        ["main", "A pen.", act, {
            'cam': {'goto_pos': ((0.011, 0.571, -0.807), (0.000, 0.000, -1.090), (40.050, 236.700, 56.483))}
        }],
        ["dr",   "And what's this?", act, {
            'cam': {'goto_pos': ((0.216, 0.662, -0.662), (0.000, 0.000, -1.849), (16.850, 80.400, 0.000))},
            'dr':  {'move_to': (0.3, 0.01, -0.6), 'turn_to': 69.9, 'anim': (1, 104, 2), 'hands': (0, 5), 'kinematic': 1, 'ik_active': (0, 0, 0, 1, 0), 'ik_set': ik_tp},
            'pen': {'visible': 0},
            'vib': {'visible': 1},
        }],
        ["s", "", anime, (
            ({ 'cam' : {'goto_pos': ((0.011, 0.571, -0.807), (0.000, 0.000, -1.000), (40.050, 236.700, 56.483))}, 'dr': {'visible': 0}, 'sys': {'visible': 0}}),
            ({ 'main': {'eyebrow': 12, 'eyes': 17, 'mouth': 18, 'mouth_open': 0.8}}),
            ({ 'sys' : {'idle' : 0}}, 2.5),
            ({ 'main': {'face_red': (0, 0.3), 'mouth_open': (0.8, 0)}}, 1),
            ({ 'main': {'eyebrow': 10, 'eyes': 18, 'mouth': 12}}),
            ({ 'main': {'face_red': (0.3, 1), 'mouth_open': (0.2, 0.8)}}, 2),
            ({ 'sys' : {'visible': 1}}),
        )],
        ["s",   "", act, {
            'cam':  {'goto_pos': ((0.255, 0.604, -0.642), (0.000, 0.000, -2.700), (6.100, -187.950, 0.000))},
            'dr':   {'visible': 1, 'kinematic': 2, 'fk_set': fk_bepunch},
            'main': {'fk_set': fk_punch, 'hands': (0, 1)},
            'nbld': {'visible': 1},
        }],
        ["dr",   "Vision, voice, expression, database... and arm motion control OK. Violence control ... may be bugged...", act, {
            'cam': {'goto_pos': ((0.221, 0.364, -0.719), (0.000, 0.000, -2.625), (-5.300, 203.9, 0.000))},
            'dr':  {'move_to': (0.9, 0.0, 0.1), 'turn_to': 210.3, 'kinematic': 1, 'anim': (1, 102, 0), 'anim_spd': 0.5, 'ik_set': ik_hbld},
            'vib': {'visible': 0},
        }],
        ["s",   "", act, {
            'cam':  {'goto_pos': ((0.221, 1.892, -0.719), (0.000, 0.000, -2.455), (-5.300, 203.9, 0.000), 1, 'slow-fast2')},
        }],
    ], start_seq2)

def start_seq2(game):
    ik_sit = {
    'cf_j_leg01_R' : (Vector3(0.027, 0.458, 0.379), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg03_R' : (Vector3(0.167, 0.096, 0.284), Vector3(357.811, 354.269, 359.985)),
    'cf_j_arm00_L' : (Vector3(-0.101, 0.894, -0.077), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_R' : (Vector3(0.022, 0.584, 0.155), Vector3(341.411, 239.148, 352.220)),
    'cf_j_forearm01_L' : (Vector3(-0.139, 0.667, -0.039), Vector3(0.000, 0.000, 0.000)),
    'cf_j_arm00_R' : (Vector3(0.101, 0.894, -0.077), Vector3(0.000, 0.000, 0.000)),
    'cf_j_forearm01_R' : (Vector3(0.146, 0.673, -0.018), Vector3(0.000, 0.000, 0.000)),
    'cf_j_thigh00_L' : (Vector3(-0.076, 0.492, -0.040), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hips' : (Vector3(0.000, 0.644, -0.059), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg01_L' : (Vector3(-0.018, 0.460, 0.378), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg03_L' : (Vector3(-0.157, 0.096, 0.285), Vector3(354.414, 15.225, 359.944)),
    'cf_j_thigh00_R' : (Vector3(0.076, 0.492, -0.040), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_L' : (Vector3(-0.034, 0.565, 0.139), Vector3(356.150, 109.640, 367.865)),
    }
    
    ik_std2 = {
    'cf_j_leg01_R' : (Vector3(0.059, 0.476, 0.053), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg03_R' : (Vector3(0.037, 0.080, -0.003), Vector3(366.217, 356.310, 356.570)),
    'cf_j_arm00_L' : (Vector3(-0.086, 1.295, -0.029), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_R' : (Vector3(0.211, 0.858, -0.033), Vector3(350.969, 350.510, 317.672)),
    'cf_j_forearm01_L' : (Vector3(-0.150, 1.082, -0.098), Vector3(0.000, 0.000, 0.000)),
    'cf_j_arm00_R' : (Vector3(0.113, 1.288, -0.025), Vector3(0.000, 0.000, 0.000)),
    'cf_j_forearm01_R' : (Vector3(0.126, 1.065, -0.091), Vector3(0.000, 0.000, 0.000)),
    'cf_j_thigh00_L' : (Vector3(-0.064, 0.889, -0.003), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hips' : (Vector3(0.007, 1.044, -0.001), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg01_L' : (Vector3(-0.050, 0.470, 0.050), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg03_L' : (Vector3(-0.042, 0.080, -0.043), Vector3(374.574, 3.026, 361.727)),
    'cf_j_thigh00_R' : (Vector3(0.088, 0.894, -0.007), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_L' : (Vector3(-0.056, 1.087, 0.112), Vector3(292.436, 266.291, 253.844)),
    }
    
    fk_yoga = {
    0: Vector3(353.270, 352.107, 345.116),
    1: Vector3(1.309, 355.965, 0.121),
    2: Vector3(357, 2.629, 358.7),
    3: Vector3(0.364, 0.856, 2.237),
    4: Vector3(358.897, 365.243, 14.813),
    5: Vector3(0.000, 0.000, 360.000),
    6: Vector3(364.529, 6.433, 7.172),
    7: Vector3(12.338, 0.000, 0.000),
    8: Vector3(344.073, 379.458, 1.746),
    9: Vector3(351.570, 355.518, 365.286),
    10: Vector3(315.617, 288.911, 0.322),
    11: Vector3(61.303, 179.994, 179.994),
    12: Vector3(25.714, 331.335, 356.467),
    13: Vector3(353.525, 17.836, 341.918),
    14: Vector3(361.386, 361.886, 8.030),
    15: Vector3(333.668, 395.795, 341.314),
    16: Vector3(0.005, 328.081, -0.003),
    #17: Vector3(364.097, 361.963, 56.642),
    17: Vector3(364.097, 361.963, 56.642),
    18: Vector3(6.172, 351.502, 344.243),
    19: Vector3(316.954, 334.202, 24.540),
    20: Vector3(0.000, 34.321, 0.000),
    #21: Vector3(40.662, 10.356, -29),
    21: Vector3(140.662, 110.356, 100),
    }

    fk_hileg = {
    0: Vector3(340.720, 362.180, 311.058),      #root
    1: Vector3(4.170, 357.885, 10.761),         #neck up
    2: Vector3(360.282, 1.536, 368.415),        #neck base
    3: Vector3(9.679, 0.861, 15.822),           #chest
    4: Vector3(371.792, 359.970, 23.406),       #upper body
    5: Vector3(5.053, 2.998, 357.175),          #lower body
    6: Vector3(338.662, 30.156, 47.599),        #R Leg
    7: Vector3(8.769, 0.000, 0.000),            #R knee
    8: Vector3(360.235, 337.662, 7.420),        #R foot
    9: Vector3(353.246, 356.645, 356.552),      #R toe
    10: Vector3(312.072, 86.128, 194.525),      #L Leg
    11: Vector3(8.831, 0.000, 0.000),           #L knee
    12: Vector3(26.904, 354.820, 351.554),      #L foot
    13: Vector3(395.774, 7.506, 368.746),       #L toe
    14: Vector3(338.052, 356.136, 37.517),      #R should-base
    15: Vector3(329.039, 286.933, 414.765),     #R should
    16: Vector3(0.003, 293.347, -0.005),        #R elbow
    17: Vector3(351.189, 348.323, 25.178),      #R hand
    18: Vector3(4.209, 369.079, 335.334),       #L should-base
    19: Vector3(326.861, 286.082, 66.355),      #L should
    20: Vector3(0.000, 127.105, 0.000),         #L elbow
    21: Vector3(288.022, 232.095, 128.031),     #L hand
    }

    fk_kick = {
    0: Vector3(344.719, 252.533, 28.095),
    1: Vector3(21.357, 335.603, 357.796),
    2: Vector3(14.019, 22.373, 8.244),
    3: Vector3(3.171, 14.485, 352.970),
    4: Vector3(3.369, 13.989, 352.776),
    5: Vector3(1.001, 2.666, 4.318),
    6: Vector3(303.693, 46.073, 333.006),
    7: Vector3(16.106, 0.000, 0.000),
    8: Vector3(0.984, 347.090, 351.581),
    9: Vector3(9.400, 349.925, 1.174),
    10: Vector3(17.057, 349.764, 319.456),
    11: Vector3(12.304, 0.000, 0.000),
    12: Vector3(341.254, 355.470, 5.816),
    13: Vector3(354.999, 8.381, 358.521),
    14: Vector3(0.000, 0.000, 0.000),
    15: Vector3(3.900, 89.170, 327.013),
    16: Vector3(0.005, 332.024, -0.003),
    17: Vector3(24.001, 26.345, 29.088),
    18: Vector3(0.000, 0.000, 0.000),
    19: Vector3(345.904, 337.636, 10.975),
    20: Vector3(0.000, 131.953, 0.000),
    21: Vector3(340.303, 29.605, 343.356),
    197: Vector3(0.000, 0.000, 14.710),
    198: Vector3(0.000, 0.000, 10.492),
    199: Vector3(0.000, 0.000, 8.309),
    }
    
    ik_yes = {
    'cf_j_forearm01_R': (Vector3(0.156, 0.674, 0.026), Vector3(0.000, 0.000, 0.000)), 
    'cf_j_arm00_R': (Vector3(0.099, 0.898, -0.028), Vector3(0.000, 0.000, 0.000)), 
    'cf_j_hand_R': (Vector3(0.066, 0.914, 0.234), Vector3(352.731, 168.115, 62.384))
    }
    
    ik_touch = {
    'cf_j_forearm01_R' : (Vector3(0.138, 1.092, 0.345), Vector3(0.000, 0.000, 0.000)),
    'cf_j_arm00_R' : (Vector3(0.076, 1.286, 0.105), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_R' : (Vector3(0.005, 1.185, 0.526), Vector3(335.092, 263.303, 63.372)),
    'cf_j_leg01_R' : (Vector3(0.114, 0.478, 0.074), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg03_R' : (Vector3(0.215, 0.082, -0.022), Vector3(11.997, 7.460, 9.249)),
    'cf_j_thigh00_R' : (Vector3(0.085, 0.897, -0.023), Vector3(0.000, 0.000, 0.000)),
    'cf_j_thigh00_L' : (Vector3(-0.065, 0.897, -0.062), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg01_L' : (Vector3(-0.090, 0.479, 0.036), Vector3(0.000, 0.000, 0.000)),
    'cf_j_leg03_L' : (Vector3(-0.129, 0.088, -0.077), Vector3(17.878, 344.005, 350.870)),
    }

    fk_beg = {
    0: Vector3(358.802, 334.989, 8.532),
    1: Vector3(314.775, 8.887, 359.471),
    2: Vector3(317.953, 12.231, 0.359),
    3: Vector3(20.294, 357.270, 352.174),
    4: Vector3(30.549, 357.029, 354.170),
    5: Vector3(4.075, 355.017, 359.645),
    6: Vector3(303.576, 352.758, 29.110),
    7: Vector3(30.541, 180.000, 180.000),
    8: Vector3(54.400, 337.983, 347.443),
    9: Vector3(19.589, 355.860, 359.472),
    10: Vector3(324.440, 53.731, 292.312),
    11: Vector3(28.488, 179.997, 179.996),
    12: Vector3(46.432, 17.461, 9.555),
    13: Vector3(11.751, 3.402, 357.244),
    14: Vector3(0.000, 0.000, 350.811),
    15: Vector3(352.729, 351.458, 315.918),
    16: Vector3(5.016, 262.030, 319.372),
    17: Vector3(356.479, 30.360, 13.963),
    18: Vector3(0.000, 0.000, 0.000),
    19: Vector3(315.626, 179.493, 270.483),
    20: Vector3(65.981, 37.198, 0.000),
    21: Vector3(355.611, 4.232, 294.721),
    }

    fk_swing = {
    0: Vector3(357.158, 13.409, 347.135),
    1: Vector3(13.139, 355.071, 11.797),
    2: Vector3(344.889, 13.535, 357.516),
    3: Vector3(3.929, 3.185, 356.470),
    4: Vector3(3.929, 3.185, 356.470),
    5: Vector3(0.000, 0.000, 0.000),
    6: Vector3(359.204, 9.429, 31.239),
    7: Vector3(48.923, 0.000, 0.000),
    8: Vector3(16.107, 11.879, 4.493),
    9: Vector3(319.533, 10.130, 354.649),
    10: Vector3(325.109, 13.084, 16.763),
    11: Vector3(47.159, 0.001, 0.002),
    12: Vector3(2.806, 31.544, 1.470),
    13: Vector3(353.032, 3.774, 354.593),
    14: Vector3(0.000, 0.000, 352.559),
    15: Vector3(337.536, 342.390, 291.697),
    16: Vector3(0.004, 309.359, -0.004),
    17: Vector3(291.734, 358.456, 28.317),
    18: Vector3(0.000, 0.000, 4.944),
    19: Vector3(348.584, 66.812, 48.208),
    20: Vector3(0.000, 45.296, 0.000),
    21: Vector3(358.446, 330.868, 2.491),
    }
    
    game.texts_next([
    #debug_game_texts_next(game, 10, [
        ["dr", "OK... Lets continue the test.", act, {
            'cam': {'goto_pos': ((0.826, 0.608, 0.326), (0.000, 0.000, -3.283), (10.250, 206, 0.000), 1, 'slow-fast2')},
            'scanner': {'move_to' : (-0.498, 0.081, -0.242), 'rotate_to' : (0, 0, 0)},
            'nbld': {'visible': 0},
            'chair':{'move_to': (1.670, -0.212, 1.456), 'rotate_to': (0, 242.6, 0)},
            'dr'  : {'turn_to': 240, 'move_to': (1.78, 0, 0.736), 'anim': (0, 6, 7), 'kinematic': 0, 'hands': (0, 9)},
            'main': {'rotate_to': (0, 53, 0), 'move_to': (0.3, 0.0, 0.3), 'kinematic': 0, 'anim': (0, 6, 0), 'hands': (0, 0), 'face_red': 0, 'eyebrow': 0, 'eyes': 0, 'eyes_open': 1, 'eyes_blink': 1, 'mouth': 0, 'mouth_open': 0},
        }],
        ["dr", "Now, try stand up, slowly", anime, (
            ({ 'cam' : {'goto_pos': ((0.614, 1.029, 0.413), (0.000, 0.000, -3.316), (7.800, 236, 0.000), 1)}}),
            ({ 'main': {'kinematic': 1, 'ik_set': ik_sit, 'face_to': 1}}),
            ({ 'main': {'ik_set' : (ik_sit, ik_std2), 'move_to': ((0.3, 0.0, 0.3), (0.609, 0, 0.406))}}, 1.5),
            ({ 'main': {'kinematic': 0, 'anim': (0, 0, 2)}}),
        )],
        ["dr", "Take a walk", anime, (
            ({ 'cam' : {'goto_pos': ((0.638, 0.794, 5.372), (0.000, 0.000, -4.369), (10.100, 179.000, 0.000), 5)}}),
            ({ 'main': {'anim': (0, 3, 0), 'anim_spd': 0.65, 'turn_to': 0, 'face_to': 0}, 'dr': {'anim': (0, 6, 12), 'hands': (0, 0), 'face_to': 1}}),
            ({ 'main': {'move_to': ((0.609, 0, 0.406), (0.609, 0, 0.406+5))}, 'dr': {'turn_to': (240, 360)}, 'chair': {'rotate_to': ((0, 242.6, 0), (0, 360, 0))}}, 5, "linear"),
            ({ 'main': {'anim': (0, 0, 2), 'anim_spd': 1}}),
        )],
        ["dr", "Good! Now walk around the lab", anime, (
            ({ 'cam' : {'goto_pos': ((5.587, 0.866, 5.372), (0.000, 0.000, -5.504), (8.750, 160.950, 0.000), 5)}}),
            ({ 'main': {'turn_to': (0, 90)}}, 0.5),
            ({ 'main': {'anim': (0, 3, 0), 'anim_spd': 0.65}}),
            ({ 'main': {'move_to': ((0.609, 0, 5.406), (0.609+5, 0, 5.406))}, 'dr': {'turn_to': (0, 45)}, 'chair': {'rotate_to': ((0, 0, 0), (0, 45, 0))}}, 5, "linear"),
            ({ 'main': {'anim': (0, 0, 6), 'anim_spd': 1}}),
            ({ 'main': {'turn_to': (90, 180)}}, 0.5),
            ({ 'cam' : {'goto_pos': ((5.604, 0.881, 0.414), (0.000, 0.000, -4.392), (8.750, 160.950, 0.000), 5)}}),
            ({ 'main': {'anim': (0, 3, 0), 'anim_spd': 0.65}}),
            ({ 'main': {'move_to': ((5.609, 0, 5.406), (5.609, 0, 5.406-5))}, 'dr': {'turn_to': (45, 90)}, 'chair': {'rotate_to': ((0, 45, 0), (0, 90, 0))}}, 5, "linear"),
            ({ 'main': {'anim': (0, 0, 6), 'anim_spd': 1}}),
            ({ 'cam' : {'goto_pos': ((5.740, 0.903, 0.491), (0.000, 0.000, -4.392), (8.600, 261.800, 0.000), 0.5)}}),
            ({ 'main': {'turn_to': (180, 270)}}, 0.5),
            ({ 'cam' : {'goto_pos': ((1.761, 0.594, 0.791), (0.000, 0.000, -3.865), (26.800, 275.150, 0.000), 3)}}),
            ({ 'main': {'anim': (0, 3, 0), 'anim_spd': 0.65}}),
            ({ 'main': {'move_to': ((5.609, 0, 0.406), (5.609-3, 0, 0.406))}}, 3, "linear"),
            ({ 'main': {'anim': (0, 0, 7), 'anim_spd': 1}}),
        )],
        ["dr", "Seems you are already used to control your body. How about a yoga pose?"],
        ["main", "Ok", anime, (
            ({ 'cam' : {'goto_pos': ((3.462, 0.871, 0.686), (0.000, 0.000, -4.930), (1.050, 73.300, 27.854))}, 'sys':{'visible': 0}}),
            ({ 'main': {'anim': (10, 62, 1), 'anim_spd': 0.8}}),
            ({ 'sys' : {'idle' : 0}}, 13.6),
            ({ 'main': {'anim_spd': 0}, 'sys':{'visible': 1}}),
        )],
        ["dr", "...then, high leg!"],
        ["", "", anime, (
            ({ 'cam' : {'goto_pos': ((3.462, 0.871, 0.686), (0.000, 0.000, -4.930), (1.050, 73.300, 27.854))}, 'sys':{'visible': 0}}),
            ({ 'sys' : {'idle' : 0}}, 0.5),
            ({ 'main': {'kinematic': 2, 'fk_active': (0, 1, 0, 1, 0, 0, 0), 'fk_set': fk_yoga}}),
            ({ 'main': {'fk_set' : (fk_yoga, fk_hileg), 'face_red': (0, 0.8)}}, 5, "slow-fast"),
            ({ 'main': {'kinematic': 0, 'anim': (7, 61, 1)}, 'sys':{'visible': 1, 'text': ('main', 'I have done...')}}),
        )],
        ["dr", "Perfect View! Oh, I mean ... perfect balance and suppleness! Just as designed! I'm really a genius!!", act, {
            'cam' : {'goto_pos': ((1.445, 0.774, 0.729), (0.000, 0.000, -1.452), (20.750, -94.600, 0.000))},
            'main': {'visible': 0},
            'dr':   {'hands': (0, 1), 'mouth': 19, 'eyes': 24, 'face_to': 3, 'eyebrow': 1, 'kinematic': 1, 'ik_active': (0, 0, 0, 1, 0), 'ik_set': ik_yes},
        }],
        ["dr", "Now, the final test. Let's check if your body sensor works properly...", anime, (
            ({ 'cam' : {'goto_pos': ((2.320, 1.078, 0.562), (0.000, 0.000, -2.990), (13.400, -188.050, 0.000))}}),
            ({ 'main': {'anim': (0, 0, 5), 'visible': 1, 'look_at': (-0.2, 0, 0.2)}, 'dr':{'anim': (0, 0, 21), 'move_to': (1.962, 0, 0.396), 'ik_active': (0, 1, 1, 1, 0), 'ik_set': ik_touch, 'hands': (0, 18)}, 'chair':{'move_to': (1.359, -0.212, 1.647)}}),
            ({ 'cam' : {'goto_pos': ((2.568, 1.267, 0.386), (0.000, 0.000, -1.252), (19.250, -208.350, 0.000), 2)}}),
            ({ 'sys' : {'idle' : 0}}, 3),
            ({ 'dr'  : {'hands' : (0, 20)}}),
            ({ 'sys' : {'idle' : 0}}, 0.5),
            ({ 'dr'  : {'hands' : (0, 18)}, 'main': {'mouth': 12, 'eyes': 27, 'eyebrow': 1}}),
            ({ 'sys' : {'idle' : 0}}, 0.5),
            ({ 'dr'  : {'hands' : (0, 20)}}),
            ({ 'main': {'mouth_open': (0, 0.8)}}, 0.7),
            ({ 'dr'  : {'hands' : (0, 18)}}),
            ({ 'sys' : {'idle' : 0}}, 0.5),
            ({ 'dr'  : {'hands' : (0, 20)}}),
        )],
        ["dr", "Oh!", anime, (
            ({ 'sys' : {'visible': 0}, 'main': {'move_to': (2.695, 0, 0.065), 'turn_to': 348.2, 'kinematic': 2, 'fk_active': (1, 1, 0, 1, 0, 0, 0), 'fk_set': fk_kick, 'face_to': 0}, 'dr': {'move_to': (1.957, 0, 0.277), 'turn_to': 121.768, 'mouth': 9, 'mouth_open': 1, 'eyes': 22, 'eyebrow': 2}}),
            ({ 'cam' : {'goto_pos': (((2.484, 0.791, 0.170), (0.000, 0.000, -3.464), (86.551, -349.100, 0.000)), ((2.484, 0.791, 0.170), (0.000, 0.000, -1.964), (86.551, -349.100, 0.000)))}}, 0.3),
            ({ 'sys' : {'idle' : 0}}, 1.2),
            ({ 'cam' : {'goto_pos': (((2.065, 1.061, 0.161), (0.000, 0.000, -3.909), (6.951, -108.900, 0.000)), ((2.065, 1.061, 0.161), (0.000, 0.000, -2.409), (6.951, -108.900, 0.000)))}}, 0.3),
            ({ 'sys' : {'idle' : 0}}, 1.2),
            ({ 'cam' : {'goto_pos': (((2.254, 0.911, 0.262), (0.000, 0.000, -3.839), (4.301, -276.500, 0.000)), ((2.254, 0.911, 0.262), (0.000, 0.000, -2.339), (4.301, -276.500, 0.000)))}}, 0.3),
            ({ 'sys' : {'visible': 1}}),
        )],
        ["dr", "What! No, No, No! KSGGK system is still at the experimental stage...", anime, (
            ({ 'cam' : {'goto_pos': ((2.839, 1.099, 0.030), (0.000, 0.000, -2.245), (-8.150, -266.600, 0.000))}}),
            ({ 'sys' : {'visible': 0}, 
               'main': {'move_to': (2.695, 0, 0.065), 'turn_to': 254, 'kinematic': 0, 'face_to': 3, 'look_at': 1, 'eyes': 10, 'mouth_open': 0.8, 'anim_spd': 0.8, 'anim': (7, 65, 20)}, 
               'dr'  : {'move_to': (1.957, -0.631, 0.277), 'turn_to': 121.768, 'scale_to': 0.95, 'kinematic': 2, 'fk_set': fk_beg},
               'kira': {'visible': 1}, 
               'cly' : {'visible': 1, 'scale_to': (0.176, 1.300, 0.176), 'color': (0, 1, 1)}}),
            ({ 'cam' : {'goto_pos': ((2.839, 1.089, 0.030), (0.000, 0.000, -3.865), (-8.150, -266.600, 0.000), 3)}}),
            ({ 'cly' : {'scale_to': ((0.176, 1.300, 0.176), (1.232, 1.450, 1.232))}}, 2.2),
            ({ 'sys' : {'visible': 1, 'lock': 1}, 'main': {'anim_spd': 0}}),
            ({ 'cly' : {'scale_to': ((1.232, 1.450, 1.232), (2.760, 1.450, 2.760)), 'color': ((0, 1, 1), (1, 1, 1))}}, 3),
            ({ 'sys' : {'lock': 0}, 'kira': {'visible': 0}, 'cly' : {'visible': 0}, 'bat' : {'visible': 1}, 'main': {'anim_spd': 0}}),
        )],
        ["dr", "And weapon system should be disabled by default!\nWait!! My bad!!\nFreeze all motor functions!!!", anime, (
            ({ 'sys' : {'lock': 1}}),
            ({ 'cam' : {'goto_pos': ((2.029, 0.649, 0.259), (0.000, 0.000, -3.477), (6.151, 269.100, 0.000))}}),
            ({ 'cam' : {'goto_pos': ((2.029, 0.856, 0.259), (0.000, 0.000, -5.470), (12.051, 269.350, 0.000), 1.5)}}),
            ({ 'sys' : {'idle' : 0}}, 2),
            ({ 'sys' : {'lock': 0}}),
        )],
        ["dr", "<size=32>FREEZE ALL MOTOR FUN...</size>", anime, (
            ({ 'main': {'anim_spd': 1}, 'sys' : {'lock': 1}, 'cam' : {'goto_pos': ((2.029, 0.799, 0.259), (0.000, 0.000, -2.400), (12.052, 269.350, 0.000),1.1, "slow-fast3")}}),
            ({ 'sys' : {'idle' : 0}}, 1.8),
            ({ 'main': {'anim_spd': 0, 'kinematic': 2, 'fk_set': fk_swing, 'fk_active': (0, 1, 0, 1, 0, 0, 0)}, 'sys': {'visible': 1, 'text': ("main", "<size=32>TENCHU</size>")}}),
            ({ 'sys' : {'idle' : 0}}, 1.2),
            ({ 'cam' : {'goto_pos': ((2.029, 0.799, 0.259), (0.000, 0.000, -2.400), (-5.848, 90.250, 0.000))}}),
            ({ 'cam' : {'goto_pos': ((2.029, 0.667, 0.259), (0.000, 0.000, -1.517), (-5.848, 90.250, 0.000), 0.2)}}),
            ({ 'sys' : {'idle' : 0}}, 1.2),
            ({ 'dr'  : {'visible': 0}, 'chair': {'visible': 0}}),
            ({ 'cam' : {'goto_pos': ((4.102, 1.574, -0.606), (0.000, 0.000, -3.480), (-18.898, 114.049, 0.000))}}),
            ({ 'cam' : {'goto_pos': ((3.973, 0.643, -0.546), (0.000, 0.000, -3.627), (-4.512, 109.894, -91.417), 2, "slow-fast2")}}),
            ({ 'main': {'kinematic': 0}}),
            ({ 'main': {'anim_spd': (1, 0.5)}}, 2),
            ({ 'sys' : {'visible': 1, 'text': ("main", "NAMUSAN")}}),
            ({ 'sys' : {'idle' : 0}}, 1),
            ({ 'sys' : {'lock' : 0}}, 1),
        )],
        ["s", "", act, {
            'cam' : {'goto_pos': ((1.791, 3.086, 0.148), (0.000, 0.000, -3.627), (-77.766, 109.894, -91.417), 2, "fast-slow")},
        }],
    ], start_seq3)

def start_seq3(game):
    fk_sit = {
    0: Vector3(356.820, 355.580, 1.053),
    1: Vector3(357.632, 2.370, 358.000),
    2: Vector3(359.313, 1.627, 359.225),
    3: Vector3(10.094, 0.808, 359.685),
    4: Vector3(0.000, 0.000, 0.000),
    5: Vector3(345.818, 358.762, 0.671),
    6: Vector3(289.731, 14.036, 349.255),
    7: Vector3(89.893, 0.000, 0.000),
    8: Vector3(358.910, 6.929, 2.605),
    9: Vector3(0.000, 0.000, 0.000),
    10: Vector3(289.551, 352.443, 15.183),
    11: Vector3(88.148, 0.070, 0.071),
    12: Vector3(1.395, 353.374, 355.453),
    13: Vector3(0.000, 0.000, 0.000),
    14: Vector3(0.000, 0.000, 0.000),
    15: Vector3(331.965, 335.174, 299.176),
    16: Vector3(19.702, 237.712, 351.360),
    17: Vector3(339.269, 340.420, 47.124),
    18: Vector3(0.000, 0.000, 0.000),
    19: Vector3(326.091, 22.360, 68.650),
    20: Vector3(3.647, 117.861, 19.139),
    21: Vector3(10.950, 7.686, 314.065),
    }
    
    ik_glass = {
    'cf_j_forearm01_R' : (Vector3(0.168, 0.673, 0.169), Vector3(0.000, 0.000, 0.000)),
    'cf_j_arm00_R' : (Vector3(0.094, 0.878, 0.020), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_R' : (Vector3(0.069, 0.922, 0.104), Vector3(351.549, 170.975, 105.764)),
    }

    ik_thank = {
    'cf_j_arm00_L' : (Vector3(-0.108, 0.886, 0.010), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_R' : (Vector3(0.069, 0.880, 0.104), Vector3(351.549, 170.975, 130.597)),
    'cf_j_forearm01_L' : (Vector3(-0.091, 0.667, 0.089), Vector3(0.000, 0.000, 0.000)),
    'cf_j_arm00_R' : (Vector3(0.094, 0.878, 0.020), Vector3(0.000, 0.000, 0.000)),
    'cf_j_forearm01_R' : (Vector3(0.168, 0.673, 0.169), Vector3(0.000, 0.000, 0.000)),
    'cf_j_hand_L' : (Vector3(0.023, 0.867, 0.107), Vector3(335.228, 198.006, 297.647)),
    }
    
    game.texts_next([
    #debug_game_texts_next(game, 1, [
        #["", ""],
        ["", "", anime, (
            ({ 'sys' : {'visible': 0}, 'bat': {'visible':0}, 'bat2': {'visible':1}, 'pc': {'visible':0}, 'rei': {'visible':1}, 
               'chair':{'visible': 1, 'move_to': (1.168, -0.212, 0.266), 'rotate_to': (0, 180, 0)},
               'dr'  : {'visible': 1, 'move_to': (-0.591, 0.107, 0.167), 'rotate_to': (270.855, 180.000, 180.000), 'scale_to': (1.000, 1.000, 1.000), 'kinematic': 0, 'anim': (0, 0, 0),}, 
               'main': {'visible': 1, 'move_to': (1.094, -0.415, -0.458), 'rotate_to': (0.000, 180.000, 0.000), 'kinematic': 2, 'fk_active': (0, 1, 0, 1, 0, 0, 0), 'fk_set': fk_sit, 'hands': (7, 7), 'eyebrow': 0, 'eyes': 0, 'eyes_open': 0, 'eyes_blink': 0, 'mouth': 0, 'mouth_open': 0, 'face_red':0.2, 'cloth_all': (0, 0, 0, 0, 3, 0, 0, 0), 'acc_all': (1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1)},
             }),
            ({ 'cam' : {'goto_pos': ((-0.622, 0.304, 0.145), (0.000, 0.000, -1.970), (-3.650, 209.849, 0.000))}}),
            ({ 'sys' : {'idle': 0}}, 1),
            ({ 'cam' : {'goto_pos': ((1.012, 0.305, -0.290), (0.000, 0.000, -2.860), (0.650, 153.849, 0.000),4)}}),
            ({ 'sys' : {'idle': 0}}, 5),
            ({ 'cam' : {'goto_pos': ((1.117, 0.787, -0.462), (0.000, 0.000, -1.712), (15.150, 21.549, 0.000))}}),
            ({ 'sys' : {'idle': 0}}, 1),
            ({ 'cam' : {'goto_pos': ((1.117, 0.787, -0.462), (0.000, 0.000, -1.712), (15.650, 152.549, 0.000),4)}}),
            ({ 'sys' : {'idle': 0}}, 4),
            ({ 'sys' : {'visible': 1}}),
        )],
        ["", "", anime, (
            ({ 'main': {'move_to': (1.094, 0, -0.458), 'kinematic': 0, 'anim': (0, 6, 14), 'anim_spd': 0.3, 'eyes_open': 1, 'eyes_blink': 1, 'look_at': 1, 'face_to': 1, 'hands': (0, 0)},
               'sys' : {'visible': 0}, 'chair': {'move_to': (1.031, -0.212, 0.266)}}),
            ({ 'cam' : {'goto_pos': ((1.117, 0.567, -0.462), (0.000, 0.000, -3.502), (2.250, 163.949, 0.000), 2)}}),
            ({ 'main': {'turn_to': (180, 330)}, 'chair': {'rotate_to': ((0, 180, 0), (0, 330, 0))}}, 2, "fast-slow"),
            ({ 'sys' : {'visible': 1, 'text': ("main", "Hello, guys.")}}),
        )],
        ["main", "Since the Dr...", anime, (
            ({ 'cam' : {'goto_pos': ((1.043, 0.824, -0.442), (0.000, 0.000, -2.029), (1.200, 164.399, 0.000), 2)}}),
            ({ 'main': {'look_at': 2, 'face_to': 2}, 'sys': {'lock': 1}}),
            ({ 'sys' : {'idle': 0}}, 3),
            ({ 'main': {'look_at': 1, 'face_to': 1}}),
            ({ 'sys' : {'idle': 0}}, 1),
            ({ 'sys' : {'text': ("main", "Since the Dr... Dr. whatever was gone.")}}),
            ({ 'sys' : {'idle': 0}}, 3),
            ({ 'sys' : {'lock': 0}}),
        )],
        ["main", "I will talk for him.", act, {
            'cam' : {'goto_pos': ((1.043, 0.989, -0.442), (0.000, 0.000, -0.894), (1.200, 164.399, 0.000))}, 
            'main': {'kinematic': 1, 'ik_active': (0, 0, 0, 1, 0), 'ik_set': ik_glass},
        }],
        ["main", "At first, great thanks to <b>keitaro1978</b> for the <b>VNGameEngine</b> and <b>TheHologram</b> for the <b>HS Console</b>.\nEverything you see is base on these mods.", act, {
            'cam' : {'goto_pos': ((1.043, 0.989, -0.442), (0.000, 0.000, -1.194), (1.200, 164.399, 0.000))},
            'main': {'eyebrow': 12, 'eyes': 7, 'mouth':2, 'ik_active': (0, 0, 0, 1, 1), 'ik_set': ik_thank},
        }],
        ["main", "Inspired by the ideas from <b>ruris_dream</b> and <b>VNSceneScript</b>, a help class to control the actor and a frame to control the scene anime was developped. I think you are already noticed what it can do.", act, {
            'cam' : {'goto_pos': ((1.043, 0.824, -0.442), (0.000, 0.000, -2.329), (1.200, 164.399, 0.000), 2)},
            'main': {'kinematic': 0, 'anim': (0, 6, 15), 'anim_spd': 1},
        }],
        ["main", "Using a tag folder we can tell the python script which one to interactive with. So you can edit the scene file, add something, or replace the actor with your owner favorite character. You can customize the game without modify the python script!", act, {
            'cam' : {'goto_pos': ((0.869, 0.695, -0.424), (0.000, 0.000, -3.404), (21.950, 182.999, 0.000), 2)},
            'main': {'anim': (0, 6, 9), 'anim_spd': 0.8},
        }],
        ["main", "But you wouldn't replace me, would you?", anime, (
            ({ 'cam' : {'goto_pos': ((1.043, 0.989, -0.442), (0.000, 0.000, -0.894), (1.200, 164.399, 0.000))}, 'main': {'eyes': 2, 'eyes_open': 0}, 'sys': {'lock': 1}}), 
            ({ 'sys' : {'idle': 0}}, 3),
            ({ 'sys' : {'lock': 0}}),
        )],
        ["main", "<size=30>WOULD YOU?</size>", act, {
            'cam' : {'goto_pos': ((-0.548, 0.224, 0.224), (0.000, 0.000, -1.611), (9.900, 208.249, 0.000))},
        }],
        ["main", "Oh, here is a long todo list left... Improve the lip sync function... Develop a tool to generate script automatically...etc...etc...", act, {
            'cam' : {'goto_pos': ((1.043, 0.824, -0.442), (0.000, 0.000, -2.029), (1.200, 164.399, 0.000))},
            'phone':{'visible': 1, 'move_to': (0, -0.031, 0.017), 'rotate_to': (312.393, 170.648, 83.803)},
            'main': {'anim': (0, 6, 4), 'eyes_open': 1, 'face_to': 3, 'look_at': 0},
        }],
        ["main", "Maybe later!\nAnd I think you guys can make something much more cool!\nI am tired now. Bye-Bye!", act, {
            'cam' : {'goto_pos': ((1.224, 1.176, -0.557), (0.000, 0.000, -2.641), (7.600, 168.999, 0.000))},
            'phone':{'move_to': (-0.191, -0.586, 0.078)},
            'main': {'anim': (0, 2, 25), 'anim_spd': 0, 'look_at': 1},
        }],
    ], toEnd)

def toEnd(game, text="<size=32>THE END</size>"):
    game.set_text_s(text)
    game.set_buttons_end_game()
