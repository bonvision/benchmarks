#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from psychopy import core, visual, event

# create a window to draw in
win = visual.Window([1280, 720.0], fullscr=True, allowGUI=False)

# INITIALISE SOME STIMULI
for k in [2,4,8,16,32,64,128,256]:
    angles = np.linspace(1,360,k)
    stim = [visual.GratingStim(win, tex="sin", mask="circle", texRes=256,
                                size=[2,2], pos=[0, 0],opacity=0.1,
                                sf=[4, 0], ori=angle, name='gabor' + str(i))
                                for i,angle in zip(range(k),angles)]
    sync = visual.Rect(win, width=0.2, height=0.2, pos=[-1+0.1,-1+0.1],
                       fillColor='white',lineColor=None)
    trialClock = core.Clock()

    # inter-trial interval
    while trialClock.getTime() < 2:
        win.flip()

    # repeat drawing for each frame
    i = 0
    trialClock = core.Clock()
    while trialClock.getTime() < 3:
        sync.fillColor = 'black' if i % 2 == 0 else 'white'
        for gabor in stim:
            gabor.phase += 0.01
            gabor.draw()
        sync.draw()
        # handle key presses each frame
        if event.getKeys(keyList=['escape', 'q']):
            win.close()
            core.quit()

        win.flip()
        i = i + 1

win.close()
core.quit()

# The contents of this file are in the public domain.
