"""
LibJsonEncoder
(for SceneConsole, SceneSaveState, PoseConsole etc.)
1.1

1.1
- added wrapper for code/encode
"""
import copy
import sys

from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Vector2, Input, KeyCode
from UnityEngine import Event, EventType, WaitForSeconds, GameObject, Color
from System import String, Array

from System import Single, Byte
from json import encoder
import json
from array import array

# JSON Encoder and Decoder
def encode_custom(obj):
    if isinstance(obj, Single):
        return float(obj)
    elif isinstance(obj, Byte):
        return int(obj)
    elif isinstance(obj, Vector3):
        return {"__Vector3__": True, "x": obj.x, "y": obj.y, "z": obj.z}
    elif isinstance(obj, Vector2):
        return {"__Vector2__": True, "x": obj.x, "y": obj.y}
    elif isinstance(obj, Color):
        return {"__Color__": True, "r": obj.r, "g": obj.g, "b": obj.b, "a": obj.a}
    else:
        type_name = obj.__class__.__name__
        raise TypeError("Object of type %s is not JSON serializable" % type_name)


class SceneEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Single):
            return float(obj)
        elif isinstance(obj, Byte):
            return int(obj)
        elif isinstance(obj, Vector3):
            return {"__Vector3__": True, "x": obj.x, "y": obj.y, "z": obj.z}
        elif isinstance(obj, Vector2):
            return {"__Vector2__": True, "x": obj.x, "y": obj.y}
        elif isinstance(obj, Color):
            return {"__Color__": True, "r": obj.r, "g": obj.g, "b": obj.b, "a": obj.a}
        else:
            # print ("Object:%s, Type:%s, Class_attr:%s"%(repr(obj), obj.__class__.__name__, dir(obj)))
            super(SceneEncoder, self).default(obj)

    def encode(self, obj):
        def hint_tuples(item):
            if isinstance(item, tuple):
                return {'__tuple__': True, 'list': [hint_tuples(i) for i in item]}
            if isinstance(item, list):
                return [hint_tuples(e) for e in item]
            if isinstance(item, dict):
                return {key: hint_tuples(value) for key, value in item.items()}
            else:
                return item

        return super(SceneEncoder, self).encode(hint_tuples(obj))


def sceneDecoder(dict):
    # if "_customClass" in dict:
    if "__Vector3__" in dict.keys():
        return Vector3(dict["x"], dict["y"], dict["z"])
    elif "__Vector2__" in dict.keys():
        return Vector2(dict["x"], dict["y"])
    elif "__Color__" in dict.keys():
        return Color(dict["r"], dict["g"], dict["b"], dict["a"])
    elif "__tuple__" in dict.keys():
        return tuple(dict["list"])
    else:
        ndict = {}
        for k in dict.keys():
            if str.isdigit(k):
                ndict[int(k)] = dict[k]
            else:
                ndict[k] = dict[k]
        dict = ndict
    return dict

# wrapper functions
def json_decode(str):
    return json.loads(str, object_hook=sceneDecoder)

def json_encode(obj):
    return json.dumps(obj, cls=SceneEncoder)