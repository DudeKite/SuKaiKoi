# regex replacement for VNGE markup
"""
Text Markup.

interpret some md-like syntax to make emphasis and things quicker.

USAGE:

Normal:
text -> text

color emphasis (using the color set in config object):
*text* = <color=#ffffff>text</color>

Size emphasis:
_text_ -> <size=24>text</size>
__text__ -> <size=36>text</size>
___text___ -> <size=48>text</size>

Combination:
_*text*_ -> <color=#ffffff><size=24>text</size></color>
__*text*__ -> <color=#ffffff><size=36>text</size></color>
___*text*___ -> <color=#ffffff><size=42>text</size></color>

"""

import re

config = {
    'bold': 24, 
    'bolder': 36,
    'boldest': 48,
    'color': '#ff8888',
} # replace config with user's config object (from game PY), then replace color with the current char's color.

def markup(matchObj):
    matchString = matchObj.group(0)
    #print(matchString)
    matchStart = matchObj.group(1)
    #print(matchStart)

    if (matchStart == "___*"):
        matchString = "<color=" + str(config['color']) + "><size=" + str(config['boldest']) + ">" + matchString.replace("*", "").replace("_", "") + "</size></color>"
    elif (matchStart == "__*"):
        matchString = "<color=" + str(config['color']) + "><size=" + str(config['bolder']) + ">" + matchString.replace("*", "").replace("_", "") + "</size></color>"
    elif (matchStart == "_*"):
        matchString = "<color=" + str(config['color']) + "><size=" + str(config['bold']) + ">" + matchString.replace("*", "").replace("_", "") + "</size></color>"
    elif (matchStart == "___"):
        matchString = "<size=" + str(config['boldest']) + ">" + matchString.replace("_", "") + "</size>"
    elif (matchStart == "__"):
        matchString = "<size=" + str(config['bolder']) + ">" + matchString.replace("_", "") + "</size>"
    elif (matchStart == "_"):
        matchString = "<size=" + str(config['bold']) + ">" + matchString.replace("_", "") + "</size>"
    elif (matchStart == "*"):
        matchString = "<color=" + str(config['color']) + ">" + matchString.replace("*", "") + "</color>"

    return matchString

def markupReplace(input):
    return re.sub(r"(_{1,3}\*|_{1,3}|\*)(.[^_*]+)(\*_{1,3}|_{1,3}|\*)", markup, input)    # Replace a string with a part of itself

# ----------- game functions ---------------
def markup_set_text(game,char,text):
    """:type game: vngameengine.VNController"""
    game.set_text(char,markupReplace(text))

def markup_texts_next(game,nexttexts,onend):
    """:type game: vngameengine.VNController"""
    ntexts2 = []
    for f in nexttexts:
        f[1] = markupReplace(f[1])
        ntexts2.append(f)
    game.texts_next(ntexts2,onend)