#vngame;all;Demos/-- All demos  --
def start(game):
    """:type game: vngameengine.VNController"""
    game.set_text_s("Choose demo:")
    btns = [
        "Start Main Demo >", (game.game_start_fromfile, "maingamedemo"),
        # "Start Simple Demo >", (game.game_start_fromfile, "simplegamedemoadv"),
        "Engine features tech demo >", (game.game_start_fromfile, "techdemo"),
        "Main Demo + checkpoints features >", (game.game_start_fromfile, "maingamedemocheckpoints"),
    ]

    if game.isStudioNEO:
        btns += "Simple game demo (with fake lip sync) >", (game.game_start_fromfile, "simplegamedemoadv2"),

    #if not game.isClassicStudio:
    #    btns += "Simple game demo (with fake lip sync) >", (game.game_start_fromfile, "simplegamedemoadv2"),

    game.set_buttons_alt(btns)


