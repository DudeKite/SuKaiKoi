"""
VN Scene Script by Keitaro
Simple view runner
"""
def start(game):
    # from vngameengine import import_or_reload
    # import_or_reload("skin_renpy")

    """:type game: vngameengine.VNNeoController"""
    # show window if it was hidden
    #game.isHideWindowDuringCameraAnimation = True  # this setting hide game window during animation between cameras

    if not game.visible: game.visible = True

    skin = game.get_ini_option("vnscenescriptrunskin")
    if skin:
        game.skin_set_byname(skin)

    import vngameengine
    vngameengine.import_or_reload("vnscenescript").start_cur_view(game)

