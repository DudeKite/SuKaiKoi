"""
Lib ministates

ministates can be saved and loaded in SSS
and they can run in usual game!

1.0
"""
from vngameengine import HSNeoOCIFolder, HSNeoOCIChar, HSNeoOCIProp, HSNeoOCI
from libjsoncoder import *

def ministates_get_list(game):
    fld = HSNeoOCIFolder.find_single("-ministates:1.0")
    if fld == None:
        return []

    ar = []
    for fldMiniState in fld.treeNodeObject.child:
        ar.append((fldMiniState.textName, fldMiniState))

    return ar

def ministates_run_elem(game, elem):
    state = ministates_get_elem(game,elem)
    ministates_run_savedstate(game,state)

def ministates_get_elem(game,elem):
    res = {}
    for elData in elem.child:

        elDataObj = json_decode(elData.textName)
        res.update(elDataObj)
    return res

def ministates_run_savedstate(game,state):
    elDataObj = state
    for key in elDataObj:
        elId = int(key[4:])

        objctrl = game.studio.dicObjectCtrl[elId]
        actprop = HSNeoOCI.create_from(objctrl)
        if isinstance(actprop, HSNeoOCIChar):
            actprop.as_actor.import_status_diff_optimized(elDataObj[key])
        else:
            actprop.as_prop.import_status_diff_optimized(elDataObj[key])

def ministates_get_elem_by_name(game,name):
    list = ministates_get_list(game)
    for elemFull in list:
        if elemFull[0] == name:
            return elemFull[1]

    return None

def ministates_run_elem_by_name(game,name):
    elem = ministates_get_elem_by_name(game,name)
    if elem != None:
        ministates_run_elem(game,elem)

def ministates_calc_prefix(name):
    ar = name.split("-", 1)
    if len(ar) == 1:
        return ["", name]
    else:
        return ar
