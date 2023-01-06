vnscenescripttext_blackrain10
v0.1

Instructions:
Unzip archive to your HS game folder, or simply copy vnscenescripttext_blackrain10.py into /Plugins/Console/Lib

This is a vnscenescript extension intended to allow for more dynamic scenes using vnscenescript commands, primarily in SceneSaveState (see AdvVNcmds.png).  It adds variable storage, conditional expressions, randomization, some new commands that make use of this, and a few other things.

Please note, this is not a full expression interpreter.  The ability to set variables and evaluate conditions is fairly simple.

This is essentially an alpha version.  If you have feedback, let me know.  

The provided py file is already pretty well commented, but here are the new commands:

txtfv - like txtf except you can provide a list of variables for a formatted string, since SceneSaveState autogenerates txtf, even an empty one, you'll need to manually remove it for this to work (see emptytxtf.png)

nextstatecond - like nextstate except you specify a conditional expression (x,>,5) if its true the first state is picked, otherwise the second state is picked

timernextcond - like timernext except you can specify a conditional expression, similar to nextstatecond

addbtncond - like addbtn except you can specify a conditional expression, similar to nextstatecond

timernext2 - the current timernext command doesn't work with other buttons, this does (note: use stoptimer with this)

stoptimer - use with timernext2, if you add buttons, then add stoptimer wherever those buttons go to because the user might click a button before the timer resolves

enablelipsync - toggle lipsync on, I simply moved this tweak from vnscenescript_flipsync10 so I'm not editing existing files

disablelipsync -  toggle lipsync off

setvar - store a variable in game.gdata.brVars, can set to a single numeric value, another variable, or a random number (setvar:x:3)

setrandvar - same as setvar, just makes using a random number easier (setrandvar:x:1,10)

setrandsumvar - for multiple random numbers summed together, like dice (setrandsumvar:x:1,6:3)

opvar - perform a simple math operation on a variable (opvar:x:+5)

oprandvar - same as opvar but for random numbers (oprandvar:x:+1,10) that adds a random number between 1 and 10 to x

printvar - for debugging, retrieve a variable value and display it, need to manually remove txtf commands added by SceneSaveState for this to work (see emptytxtf.png).