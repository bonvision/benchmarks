#!/usr/bin/env python
# -*- coding: utf-8 -*-

from psychopy import core, visual, event

# create a window to draw in
win = visual.Window([1280, 720.0], fullscr=True, allowGUI=False)

# INITIALISE SOME STIMULI
for k in [1,2,3,4,6,8,12,16,24,32,48,64]:
    sz = 2/k
    stim = [visual.GratingStim(win, tex="sin", mask="circle", texRes=256,
                                size=[sz,sz], pos=[j * sz - 1 + sz/2, i * sz - 1 + sz/2],
                                sf=[4, 0], ori=0, name='gabor' + str(j) + str(i))
                                for j in range(k) for i in range(k)]
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
