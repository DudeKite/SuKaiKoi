"""
VN Game Engine - several menus

menu is special construction, that allow doing some user choices, and ends with call game.menu_finish(result)
as result you can pass some expecting menu result

conventions:
- menu function always has 1 param
- after menu actions you must call game.menu_finish(result) to continue main game logic
- please, name menu function as menu_*
- please, try don't change text in menu - only change buttons. Expected that game has it's own text descriptions
"""

# ------- menu example choose female ----------
def menu_example_choose_female(game,param):
    """:type game: vngameengine.VNController"""
    ofems = game.scene_get_all_females()
    arTxts = []
    arBtns = []
    for i in range(len(ofems)):
        ofem = ofems[i];
        arTxts.append(ofem.text_name)
        arBtns.append( (_menu_choose_female2,i) )
    game.set_buttons(arTxts,arBtns)

def _menu_choose_female2(game,param):
    """:type game: vngameengine.VNController"""
    game.menu_finish(param) # pass female num as resut

# ------- menu example undress female ----------
def menu_example_undress_female(game, femnum):
    arTxts = ["Dress female", "Half-dress female", "Full undress female", "Next >"]
    arBtns = [(_menu_example_undress_female2,(femnum,0)),
              (_menu_example_undress_female2,(femnum,1)),
              (_menu_example_undress_female2, (femnum, 2)),
              _menu_simple_finish
              ]
    game.set_buttons(arTxts, arBtns)

def _menu_example_undress_female2(game, param):
    femnum = param[0]
    state = param[1]
    util_undressGirl(game,femnum,state)

def _menu_simple_finish(game):
    game.menu_finish(None) # no result for this menu

def util_undressGirl(game,femnum,state):
    """:type game: vngameengine.VNController"""
    ofem = game.scene_get_all_females()[femnum]
    if game.isClassicStudio:  #
        ofem = ofem;
        """:type ofem: hs.HSFemale"""  # trick for typehinting - ofem is hs.HSFemale object in Studio
        ofem.set_clothes_state_all(state)
    else:
        ofem = ofem;
        """:type ofem: vngameengine.HSNeoOCIChar"""  # trick for typehinting - ofem is HSNeoOCIChar object in NEO-based engines
        ofem.female_all_clothes_state(state)

# ------- menu example advanced - choose and undress female ----------
# this is an example how to combine several menus
def menu_exampleadv_choose_undress_female(game,param):
    """:type game: vngameengine.VNController"""
    game.run_menu(menu_example_choose_female,"",_men1)

def _men1(game):
    """:type game: vngameengine.VNController"""
    result = game.menu_result # here we get a num of choosen female
    game.set_text_s("So... how about play with the girl clothes?")
    game.run_menu(menu_example_undress_female,result,_menu_simple_finish)
