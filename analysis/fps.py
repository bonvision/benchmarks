# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 19:07:55 2019

@author: aman
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

gridsizes = [1,2,3,4,6,8,12,16,24,32,48,64]
overlap = [2,4,8,16,32,64,128,256]

def load(fname,threshold=50):
    data = pd.read_csv(fname,usecols=range(4))
    sync = data.DataElement0.diff()
    dsync = sync > threshold
    rising = np.flatnonzero(np.diff(np.int8(dsync)) > 0.0)+1
    risetimes = data.Timestamp[rising]
    trials = np.diff(risetimes) > 1.5 # split when stable more than 1.5 secs
    risetimes = np.split(risetimes,np.flatnonzero(trials)+1)
    fps = [2/t.diff().mean() for t in risetimes]
    return data,sync,dsync,risetimes,fps

def stats_fps(trials,**kwargs):
    data = pd.DataFrame([t[-1] for t in trials])
    data.dropna(axis=1,how='all',inplace=True)
    x = range(len(data.columns))
    meanfps = data.mean()
    plt.errorbar(x,meanfps,data.std(),**kwargs)
    plt.xlabel('Number of Elements')
    plt.ylabel('Frames / second')