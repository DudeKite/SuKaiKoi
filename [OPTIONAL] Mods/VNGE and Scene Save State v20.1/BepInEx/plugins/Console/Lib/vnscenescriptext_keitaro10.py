"""
VN Scene Script Ext - keitaro10
"""
def custom_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    # ------- texts --------
    if act["action"] == "kedemotext":
        # example of simple action
        game.set_text_s(act["actionparam"])
        return True

    if act["action"] == "chanim":
        # example of action, located under chara bone - to be applied at concrete character
        # hope all such actions will be started with prefix ch

        # act["treeobj"] is a TreeNodeObject
        try:
            dicobjctrl = game.studio.dicInfo
            tnodeobjchar = act["treeobj"].parent.parent.parent
            objctrl = dicobjctrl[tnodeobjchar]
            # octrl must be OCIChar object
            from Studio import OCIChar
            if isinstance(objctrl, OCIChar):
                # i use my support object HSNeoOCIChar, but you can do what you want with founded OCIChar object
                # params can be found in scene dump
                from vngameengine import HSNeoOCIChar
                obj = HSNeoOCIChar(objctrl)

                ar = act["actionparam"].split(",")
                if len(ar) == 5:
                    try:
                        obj.animate(int(ar[0]),int(ar[1]),int(ar[2]),float(ar[3]),float(ar[4]))
                    except Exception, e:
                        game.show_blocking_message_time("ERROR: action %s error set animation params"%act["origintext"])
                else:
                    game.show_blocking_message_time("ERROR: action %s not contain 5 animation params"%act["origintext"])
            else:
                game.show_blocking_message_time("ERROR: action %s is not located under char head"%act["origintext"])
        except Exception, e:
            game.show_blocking_message_time("ERROR: action %s is not located under char head"%act["origintext"])

        return True

    return False

def debug_buttons(game,state):
    return [] # if we want no additional buttons

    # return in format of set_buttons_alt
    #return ["Demo btn (keitaro10)", demo1]

def demo1(game):
    """:type game: vngameengine.VNNeoController"""
    game.show_blocking_message_time("Some demo message")