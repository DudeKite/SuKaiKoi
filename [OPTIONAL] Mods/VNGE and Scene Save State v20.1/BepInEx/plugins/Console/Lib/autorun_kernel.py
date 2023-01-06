# autorun for kernel stuff
# all PY files starting with "autorun_" will run an VNGE startup
def start_autorun(game):
    """:type game: vngameengine.VNNeoController"""

    if not game.isClassicStudio:
        if game.isSceneEventsSupported:
            game.event_reg_listener("scene_loaded_after",scene_loaded_after,"kernel",True)
            game.event_reg_listener("scene_loaded",scene_loaded,"kernel",True)
            game.event_reg_listener("scene_imported_after",scene_imported_after,"kernel",True)

            game.event_reg_listener("scene_saved",scene_saved,"kernel",True)

    import scenesavestate
    scenesavestate.autorun_start(game)

def scene_saved(game, eventid, param):
    """:type game: vngameengine.VNNeoController"""
    if(game.isSceneDataSaveSupported):
        import scenesavestate
        if scenesavestate._sc != None:
            scenesavestate.scene_saved(game)

def scene_loaded(game, eventid, param):
    """:type game: vngameengine.VNNeoController"""
    if(game.isSceneDataSaveSupported):
        import scenesavestate
        if scenesavestate._sc != None:
            scenesavestate.scene_loaded(game)




def scene_loaded_after(game, eventid, param):
    """:type game: vngameengine.VNNeoController"""

    #print "arun_reloadprops persistent event scene_loaded"
    game.scenef_register_actorsprops()
    reloadVNText(game)
    if game.isSceneAutorunAnimDisabled: # we can disable VNAnime loading on current scene
        game.isSceneAutorunAnimDisabled = False
    else:
        reloadVNAnime(game, False)

    aiLoadSavedDHH(game)
    showDialogOnSceneLoad(game)


def scene_imported_after(game, eventid, param):
    """:type game: vngameengine.VNNeoController"""
    reloadVNText(game)
    reloadVNAnime(game, True)

def aiLoadSavedDHH(game):
    """:type game: vngameengine.VNNeoController"""
    if game.isNEOV2:
        from vngameengine import HSNeoOCIFolder
        fld = HSNeoOCIFolder.find_single_startswith("-vngedhhaisave:")
        if fld != None:
            try:
                import sceneutils
                sceneutils.ai_load_dhh(game)
            except Exception, e:
                print "VNGE: can't auto-load DHH settings", e

def reloadVNText(game):
    """:type game: vngameengine.VNNeoController"""
    try:
        import vntext
        mgr = vntext.get_vntext_manager(game)
        mgr.reloadTextInfo()
    except Exception, e:
        print "reloadVNText exception during scene load/import: ", e


def reloadVNAnime(game, isImport):
    """:type game: vngameengine.VNNeoController"""
    try:
        print "VNAnime Info: Auto initialize vnanime on scene %s"%("import..." if isImport else "load...")
        import vnanime
        if isImport:
            vnanime.merge_imported_clips(game)
        # re-init
        vnanime.init_keyframe_anime(game)
        # start autorun clip
        vnanime.start_autorun_clips(game)
    except Exception, e:
        print "reloadVNAnime exception during scene load/import: ", e

def showDialogOnSceneLoad(game):
    """:type game: vngameengine.VNNeoController"""
    from vngameengine import getEngineOptions
    from vngameengine import HSNeoOCIFolder
    from vngameengine import color_text,color_text_green,color_text_gray,color_text_yellowlight,color_text_red
    option = getEngineOptions()
    # check is option set up
    if "showdialogonsceneload" in option:
        if option["showdialogonsceneload"] == "1":

            if game.isTitleScreen: # only on title screen
                btns = []

                isData = False

                if HSNeoOCIFolder.find_single_startswith(":vnscenescript:") != None:
                    btns.append(color_text_green("Play VN Scene"))
                    btns.append(dlgPlayVNSS)
                    isData = True

                if HSNeoOCIFolder.find_single_startswith("-scenesavestate:") != None:
                    btns.append("Open scenes in SSS editor")
                    btns.append(dlgPlaySSS)
                    isData = True

                import scenesavestate
                if len(scenesavestate._sc.block) > 0:
                    btns.append("Open scenes in SSS editor")
                    btns.append(dlgPlaySSS)
                    isData = True


                if isData:
                    if game.visible:
                        btns.append(color_text_gray("return back"))
                        btns.append((dlgBack, True))
                    else:
                        game.visible = True
                        btns.append(color_text_gray("return back"))
                        btns.append((dlgBack, False))

                    game.set_text_s("<b>This scene contains VNGE data!</b>\nWhat to do?")
                    game.set_buttons_alt(btns)

def dlgPlayVNSS(game):
    """:type game: vngameengine.VNNeoController"""
    game.game_start_fromfile(game,"vnscenescriptrunview")

def dlgPlaySSS(game):
    """:type game: vngameengine.VNNeoController"""
    game.game_start_fromfile(game,"scenesavestate")

def dlgBack(game,param):
    """:type game: vngameengine.VNNeoController"""
    game.return_to_start_screen()
    game.visible = param
