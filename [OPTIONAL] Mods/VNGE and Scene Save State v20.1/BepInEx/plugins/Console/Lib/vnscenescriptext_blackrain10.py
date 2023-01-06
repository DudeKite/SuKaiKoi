"""
VN Scene Script Ext - blackrain10
v0.1
"""
import operator
from vnscenescript import statestr_to_int, _on_timer_next, run_state_wr
from vngameengine import random_randint, random_choice

ops1 = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt
}

ops2 = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '/': operator.floordiv,
    '%': operator.mod,
    '^': operator.pow
}

def cmp(arg1, op, arg2):
    operation = ops1.get(op)
    return operation(arg1, arg2)

def mathop(arg1, op, arg2):
    operation = ops2.get(op)
    return operation(arg1, arg2)

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False    

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def custom_action(game,act):
    """:type game: vngameengine.VNNeoController"""

    # txtfv - display a formatted string using a variable list
    #   ex: txtfv::x,y,z:x is {} y is {} z is {}
    #   note: if you use this in SceneSaveState, you will need to manually remove
    #         the extra txtf entry that is automatically added
    #         undefined variables resolve to 0
    if act["action"] == "txtfv":
        text = act["actionparam3"].replace("\\n","\n")
        varlist = str(act["actionparam2"]).split(',')
        valuelist = []
        if hasattr(game.gdata, 'brVars'):
            variables = game.gdata.brVars
            for var in varlist:
                if var in variables:
                    valuelist.append(str(variables[var]))
                else:
                    valuelist.append("0")
            game.set_text(act["actionparam"],text.format(*valuelist))
        else:
            emptyset = ["0","0","0"]
            game.set_text(act["actionparam"],text.format(*emptyset))
        return True

    # nextstatecond - if condition is true, goto 1st state, otherwise goto 2nd state
    #   ex: nextstatecond:x,>,5:102:103
    #   note: undefined variables resolve to 0
    if act["action"] == "nextstatecond":
        cmplist = str(act["actionparam"]).split(',')
        if resolvecond(game,cmplist):
            game.scenedata.scNextState = statestr_to_int(game,act["actionparam2"])
        else:
            game.scenedata.scNextState = statestr_to_int(game,act["actionparam3"])
        return True

    # timernextcond - if condition is true, goto 1st state after timer, else 2nd state
    #   ex: timernextcond:x,>,5:3.0:103,104
    if act["action"] == "timernextcond":
        stlist = act["actionparam3"].split(",")
        cmplist = str(act["actionparam"]).split(',')
        if resolvecond(game,cmplist):
            st = statestr_to_int(game, stlist[0])
        else:
            st = statestr_to_int(game, stlist[1])
        if act.has_key("actionparam3") and len(act["actionparam3"]) > 0:
            game.scenedata.scNextState = st
        game.scenedata.scIsTimerNext = True
        game.set_timer(float(act["actionparam2"]),_on_timer_next)
        return True

    # addbtncond - create button, if condition true, goto first state, otherwise second state
    #   ex: addbtncond:Click me:x,>,5:102,103
    if act["action"] == "addbtncond":
        stlist = act["actionparam3"].split(",")
        cmplist = str(act["actionparam2"]).split(',')
        if resolvecond(game,cmplist):
            st = statestr_to_int(game, stlist[0])
        else:
            st = statestr_to_int(game, stlist[1])
        game.scenedata.scACustomButtons.append(act["actionparam"])
        game.scenedata.scACustomButtons.append((run_state_wr, (st, True)))
        return True

    # timernext2 - alternative timernext that allows buttons
    if act["action"] == "timernext2":
        if act.has_key("actionparam2") and len(act["actionparam2"]) > 0:
            game.scenedata.scNextState = statestr_to_int(game,act["actionparam2"])
        game.scenedata.scIsTimerNext = False
        game.set_timer(float(act["actionparam"]),_on_timer_next)
        return True

    # stoptimer - turn off timer, call this on states that other buttons jump to
    if act["action"] == "stoptimer":
        game.clear_timer(0)
        return True

    # enablelipsync - toggle lipsync on, use with disablelipsync
    if act["action"] == "enablelipsync":
        game.isfAutoLipSync = True
        return True

    # disablelipsync - toggle lipsync off, call after initflipsync
    #   useful when other poses/animations need control of the mouth during dialogue
    if act["action"] == "disablelipsync":
        game.isfAutoLipSync = False
        return True

    # setvar - set a variable to a number (if a var is specified its value is resolved)
    #   ex: setvar:x:3
    #       setvar:x:y
    #       setvar:x:rand,1,10 (can also use setrandvar)
    if act["action"] == "setvar":
        setvar(game, act["actionparam"], act["actionparam2"])
        return True

    # setrandvar - set var to a random number
    #   ex: setrandvar:x:1,10
    if act["action"] == "setrandvar":
        param2 = act["actionparam2"]
        param2r = "rand," + param2
        setvar(game, act["actionparam"], param2r)
        return True

    # setrandsumvar - set var to multiple random numbers summed together
    #   ex: setrandsumvar:x:1,6:3 (equivalent to a 3d6 dice total)
    if act["action"] == "setrandsumvar":
        param2 = act["actionparam2"]
        param2r = "rand," + param2
        randlist = param2r.split(',')
        r1 = int(randlist[1])
        r2 = int(randlist[2])
        sum = 0
        count = int(act["actionparam3"])
        for x in range(int(count)):
            sum += int(random_randint(r1,r2))

        setvar(game, act["actionparam"], str(sum))
        return True

    # opvar - perform math operation on a variable 
    #   ex: opvar:x:+5 (resolves to x = x + 5)
    #       opvar:x:*2 (resolves to x = x * 2)
    #       opvar:x:+rand,1,10 (can also use oprandvar)
    if act["action"] == "opvar":
        opvar(game, act["actionparam"], act["actionparam2"])
        return True

    # oprandvar - perform math operation on a variable using a random number
    #   ex: oprandvar:x:+1,10
    if act["action"] == "oprandvar":
        op = str(act["actionparam2"])[0]
        range = str(act["actionparam2"])[1:]
        param2 = op + "rand," + range
        opvar(game, act["actionparam"], param2)
        return True

    # printvar - useful for debugging, display stored variable
    #   ex: printvar:x
    if act["action"] == "printvar":
        if hasattr(game.gdata, 'brVars'):
            variables = game.gdata.brVars
            var = str(act["actionparam"])
            if var in variables:
                text1 = var + " = "
                text2 = text1 + str(variables[var])
                game.set_text_s(text2)
            else:
                text1 = var + " not defined"
                game.set_text_s(text1)
        else:
            game.set_text_s("brVars not defined")
        return True

# setvar
#   arg1 - (str)variable name
#   arg2 - (str)number, variable name, or random number (format like: rand,1,10)
#   ex: opvar(x,5)
def setvar(game,arg1,arg2):
    if not hasattr(game.gdata, 'brVars'):
        game.gdata.brVars = {}
    variables = game.gdata.brVars
    var = str(arg1)

    if is_number(arg2):
        if float(arg2).is_integer():
            setval = int(arg2)
        else:
            setval = float(arg2)
    elif str(arg2)[0:4] == "rand":
        randlist = arg2.split(',')
        if len(randlist) == 3:
            setval = int(random_randint(int(randlist[1]),int(randlist[2])))
    else: # might be a variable
        var2 = arg2
        if var2 in variables:
            if is_number(variables[var2]):
                if float(variables[var2]).is_integer():
                    setval = int(variables[var2])
                else:
                    setval = float(variables[var2])
            else:
                setval = variables[var2]
        else:
            setval = 0 # undefined var

    variables[var] = setval
    return setval

# opvar
#   arg1 = (str)variable name
#   arg2 = +-*/(str)number, variable name, or random number (format like: rand,1,10)
#   ex: opvar(x,+5)
def opvar(game,arg1,arg2):
    if not hasattr(game.gdata, 'brVars'):
        game.gdata.brVars = {}
    variables = game.gdata.brVars
    var = str(arg1)

    op = str(arg2)[0]
    param2 = str(arg2)[1:]

    if is_number(param2):
        if float(param2).is_integer():
            opval = int(param2)
        else:
            opval = float(param2)
    elif str(param2)[0:4] == "rand":
        randlist = param2.split(',')
        if len(randlist) == 3:
            opval = int(random_randint(int(randlist[1]),int(randlist[2])))
    else: # might be a variable
        var2 = param2
        if var2 in variables:
            if is_number(variables[var2]):
                if float(variables[var2]).is_integer():
                    opval = int(variables[var2])
                else:
                    opval = float(variables[var2])
            else:
                opval = variables[var2]
        else:
            opval = 0 # undefined var
    
    if var in variables:
        variables[var] = mathop(variables[var],op,opval)
    else:
        variables[var] = mathop(0,op,opval)
    return int(variables[var])

# resolvecond - resolve a conditional expression formatted like [x,<,5] and return true or false
#   note: valid comparison operators are <, >, <=, >=, ==, !=
def resolvecond(game,list1):
    # parse list
    arg1 = list1[0]
    op = list1[1]
    arg2 = list1[2]
    # resolve any variables
    if hasattr(game.gdata, 'brVars'):
        variables = game.gdata.brVars
        if not is_number(arg1) and arg1 in variables:
            arg1 = variables[arg1]
        if not is_number(arg2) and arg2 in variables:
            arg2 = variables[arg2]
    # cast arg values
    if is_number(arg1):
        if float(arg1).is_integer():
            arg1v = int(arg1)
        else:
            arg1v = float(arg1)
    else:
        arg1v = 0 # catch undefined variables
    if is_number(arg2):
        if float(arg2).is_integer():
            arg2v = int(arg2)
        else:
            arg2v = float(arg2)
    else:
        arg1v = 0 # catch undefined variables
        
    return cmp(arg1v,op,arg2v)

def debug_print(game,var):
    typestr = str(type(var).__name__)
    varstr = str(var)
    msg = typestr + " " + varstr
    game.set_text_s(msg)
    return True

def debug_buttons(game,state):
    return [] # if we want no additional buttons