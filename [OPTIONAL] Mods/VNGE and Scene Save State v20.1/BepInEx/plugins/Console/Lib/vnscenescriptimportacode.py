"""
VN Scene Script by Keitaro
Import :acode
"""
def start(game):
    # show window if it was hidden
    if not game.visible: game.visible = True

    import vnscenescript
    vnscenescript.dutil_syncwithfile_full_acode(game, (":acode", "vnscene_acode.txt"))
    game.show_blocking_message_time(":acode imported from file!")
