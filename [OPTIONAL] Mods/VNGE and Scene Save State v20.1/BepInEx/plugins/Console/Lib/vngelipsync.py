"""
vn game engine Lip sync module
v1.0
thanks to @countd360

support lipsync of different versions:
- v10 - default, the simplest
- v11 - more weighted open mouse
"""

import random
rng = random.WichmannHill()
# we will not use simple random because of bug
# see https://github.com/IronLanguages/ironpython2/issues/231 for details

def flipsync_text_handler(self, charfull, text):
    char = charfull.split("//")[0] # charfull may be "me//surprised" etc.
    if self.fAutoLipSyncVer == "v10" or self.fAutoLipSyncVer == "v11":
        fake_lipsync_stop(self)
        if not text.startswith("!") and len(text) > 0:  # we have "!silent chara thouthgs" construction
            if self.isfAutoLipSync and (self.scenef_get_actor(char) != None):
                # print char, "Reads:", text, "("+str(len(text))+" letters)"
                self.readingChar = self.scenef_get_actor(char)
                self.readingProgress = 0
                self.lipAnimeTID = self.set_timer(len(text) / self.readingSpeed, _fake_lipSync_end, _fake_lipSync_upd)
            else:
                self.readingChar = None
                self.readingProgress = 0
                self.lipAnimeTID = -1

def _fake_lipSync_end(self):
    self.readingChar.set_mouth_open(0)
    self.readingChar = None
    self.lipAnimeTID = -1

def _fake_lipSync_upd(self, dt, time, duration):
    if time >= self.readingProgress:
        import random
        mo = random.random()
        # print "fake lipsync: dt=%s, time=%s, random=%f"%(str(dt), str(time), mo)
        if self.fAutoLipSyncVer == "v10":
            self.readingChar.set_mouth_open(mo)
        elif self.fAutoLipSyncVer == "v11":
            mo = rng.random()

            if mo > 0.7:
                self.readingChar.set_mouth_open(1.0)
            else:
                self.readingChar.set_mouth_open(mo)

        self.readingProgress += 0.1

def fake_lipsync_stop(self):
    if self.lipAnimeTID != -1:
        self.clear_timer(self.lipAnimeTID, 1)