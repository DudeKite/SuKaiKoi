"""
VN Scene Script Ext - game util
by Countd360
Provide functions to support game play

contents:
gskin, gskin_setattr, 
gpersdata_save, gpersdata_load, gpersdata_clear, 
gpersdata_to_brvars, brvars_to_gpersdata,


Function: gskin - switch game skin to 'skinname'
Syntax:
    gskin:skinname
Examples:
    gskin:skin_btnonly


Function: gskin_setattr - change skin attrubite 'pname' to 'pval'
Syntax:
    gskin_setattr:pname::pval
Examples:
    gskin_setattr:maxButtonsInSet::3


Function: gpersdata_save - save gpersdata to file 'Gpdata/[fname].dat'. If dst scene setted, goto dst scene when [next] clicked.
Syntax:
    gpersdata_save:fname:[normal next]:[error next]
Examples:
    gpersdata_save:mygame
    gpersdata_save:mygame:103
    gpersdata_save:mygame::104
    gpersdata_save:mygame:103:104


Function: gpersdata_load - load gpersdata from file 'Gpdata/[fname].dat'. If dst scene setted, goto dst scene when [next] clicked.
Syntax:
    gpersdata_load:fname:[normal next]:[error next]
Examples:
    gpersdata_load:mygame
    gpersdata_load:mygame:103
    gpersdata_load:mygame::104
    gpersdata_load:mygame:103:104


Function: gpersdata_clear - clear all var in gpersdata and delete gpersdata file 'Gpdata/[fname].dat'.
Syntax:
    gpersdata_clear:fname
Examples:
    gpersdata_clear:mygame


Function: gpersdata_to_brvars - load gpersdata to brVars(blackrain ext), if var name list not set load all in gpersdata
Syntax:
    gpersdata_to_brvars:[var name list, split by comma]
Examples:
    gpersdata_to_brvars
    gpersdata_to_brvars:var1,var2,var3


Function: brvars_to_gpersdata - load brVars(blackrain ext) to gpersdata, if var name list not set load all in brVars
Syntax:
    brvars_to_gpersdata:[var name list, split by comma]
Examples:
    brvars_to_gpersdata
    brvars_to_gpersdata:var1,var2,var3

"""

from vnscenescript import statestr_to_int

def custom_action(game, act):
    """:type game: vngameengine.VNNeoController"""

    if act["action"] == "gskin":
        try:
            # save current skin's end button setting
            cskin = game.skin_get_current()
            if hasattr(cskin, "isEndButton") and hasattr(cskin, "endButtonTxt") and hasattr(cskin, "endButtonCall"):
                isEndButton = cskin.isEndButton
                endButtonTxt = cskin.endButtonTxt
                endButtonCall = cskin.endButtonCall
            else:
                isEndButton = None
            
            # change skin
            sname = act["actionparam"]
            game.skin_set_byname(sname)

            # restore end button setting
            if isEndButton:
                cskin = game.skin_get_current()
                cskin.isEndButton = isEndButton
                cskin.endButtonTxt = endButtonTxt
                cskin.endButtonCall = endButtonCall

            return True
        except Exception, e:
            print "gskin error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "gskin_setattr":
        try:
            pname = act["actionparam"]
            pval = eval(act["actionparam3"])
            # save current skin's end button setting
            cskin = game.skin_get_current()
            setattr(cskin, pname, pval)

            return True
        except Exception, e:
            print "gskin_var error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "gpersdata_save":
        try:
            fname = act["actionparam"]
            if act.has_key("actionparam2") and len(act["actionparam2"]) > 0:
                ndst = act["actionparam2"]
            else:
                ndst = None
            if act.has_key("actionparam3") and len(act["actionparam3"]) > 0:
                edst = act["actionparam3"]
            else:
                edst = None

            # save current gpersdata
            result = game.gpersdata_save(fname)
            if result:
                if ndst:
                    game.scenedata.scNextState = statestr_to_int(game, ndst)
            else:
                if edst:
                    game.scenedata.scNextState = statestr_to_int(game, edst)

            return True
        except Exception, e:
            print "gpersdata_save error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "gpersdata_load":
        try:
            fname = act["actionparam"]
            if act.has_key("actionparam2") and len(act["actionparam2"]) > 0:
                ndst = act["actionparam2"]
            else:
                ndst = None
            if act.has_key("actionparam3") and len(act["actionparam3"]) > 0:
                edst = act["actionparam3"]
            else:
                edst = None

            # load gpersdata
            result = game.gpersdata_load(fname)
            if result:
                if ndst:
                    game.scenedata.scNextState = statestr_to_int(game, ndst)
            else:
                if edst:
                    game.scenedata.scNextState = statestr_to_int(game, edst)

            return True
        except Exception, e:
            print "gpersdata_load error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "gpersdata_clear":
        try:
            fname = act["actionparam"]

            # clear gpersdata
            game.gpersdata_clear(fname)

            return True
        except Exception, e:
            print "gpersdata_clear error, can't parse command '%s':"%act["origintext"], e
            return True


    if act["action"] == "gpersdata_to_brvars":
        try:
            if act.has_key("actionparam") and len(act["actionparam"]) > 0:
                varnames = [s.strip() for s in act["actionparam"].split(",")]
            else:
                varnames = None

            # load gpersdata data to brVars
            for vname in game.gpersdata.keys():
                if varnames == None or vname in varnames:
                    if not hasattr(game.gdata, 'brVars'):
                        game.gdata.brVars = {}
                    game.gdata.brVars[vname] = game.gpersdata[vname]
                    print "gpersdata_to_brvars: %s = %s"%(vname, str(game.gpersdata[vname]))

            return True
        except Exception, e:
            print "gpersdata_to_brvars error, can't parse command '%s':"%act["origintext"], e
            return True

    if act["action"] == "brvars_to_gpersdata":
        try:
            if act.has_key("actionparam") and len(act["actionparam"]) > 0:
                varnames = [s.strip() for s in act["actionparam"].split(",")]
            else:
                varnames = None

            # load brVars to gpersdata data
            if not hasattr(game.gdata, 'brVars'):
                print "brVars not found! Set some vars first!"
                return True
            for vname in game.gdata.brVars.keys():
                if varnames == None or vname in varnames:
                    game.gpersdata[vname] = game.gdata.brVars[vname]
                    print "brvars_to_gpersdata: %s = %s"%(vname, str(game.gpersdata[vname]))

            return True
        except Exception, e:
            print "brvars_to_gpersdata error, can't parse command '%s':"%act["origintext"], e
            return True

def debug_buttons(game,state):
    return [] # if we want no additional buttons

    # return in format of set_buttons_alt
    #return ["Demo btn (keitaro10)", demo1]