#import UnityEngine

def reset():
    from Studio import Studio
    studio = Studio.Instance
    studio.InitScene(False)


# additional Keitaro vngame functions 
def load_scene(file=''):
    from Studio import Studio
    studio = Studio.Instance
    from os import path
    #return path.join(get_scene_dir(),file)
    studio.LoadScene(path.join(get_scene_dir(),file))

def get_scene_dir():
    from UnityEngine import Application
    from os import path
    return path.realpath(path.join(Application.dataPath,'..','UserData','studioneo','scene'))        
#

