# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 13:28:05 2019

@author: aman
"""

import os
import fps
import latency
import matplotlib.pyplot as plt

def trials(dname,module,include='.csv',**kwargs):
    if include is None:
        include = lambda x:True
    elif type(include) is str:
        suffix = include
        include = lambda x:x.endswith(suffix)        
    return [module.load(os.path.join(dname, fname),**kwargs)
            for fname in os.listdir(dname)
            if include(fname)]

def fig_fps_nonoverlap():
    ptb = trials('../benchmarks/fps/acquisition/data/Psychtoolbox',fps)
    bv = trials('../benchmarks/fps/acquisition/data/BonVision',fps)
    ppy = trials('../benchmarks/fps/acquisition/data/PsychoPy',fps)
    plt.figure()
    fps.stats_fps(ptb,label='Psychtoolbox')
    fps.stats_fps(bv,label='BonVision')
    fps.stats_fps(ppy,label='PsychoPy')
    ticks = range(len(fps.gridsizes))
    plt.xticks(ticks,[fps.gridsizes[i]**2 for i in ticks])
    plt.title('Non-overlapping Elements (3s / trial)')
    plt.legend()
    plt.show()

def fig_fps_overlap():
    ptb = trials('../benchmarks/fps-overlap/acquisition/data/Psychtoolbox',fps)
    bv = trials('../benchmarks/fps-overlap/acquisition/data/BonVision',fps)
    ppy = trials('../benchmarks/fps-overlap/acquisition/data/PsychoPy',fps)
    plt.figure()
    fps.stats_fps(ptb,label='Psychtoolbox')
    fps.stats_fps(bv,label='BonVision')
    fps.stats_fps(ppy,label='PsychoPy')
    ticks = range(len(fps.overlap))
    plt.xticks(ticks,[fps.overlap[i] for i in ticks])
    plt.title('Overlapping Elements (3s / trial)')
    plt.legend()
    plt.show()

def fig_latency_software():
    data = trials('../benchmarks/latency/acquisition/data/software',latency)
    latency.hist_latency(data[::-1],alpha=0.8)
    plt.title('Closed-loop latency @ 60Hz')
    plt.show()

def fig_latency_hardware():
    data = trials('../benchmarks/latency/acquisition/data/hardware',latency)
    hmd = trials('../benchmarks/latency/acquisition/data/hardware-hmd',latency,
                 threshold=200,iti=0.2,ioffset=-1) # cleanup HMD photo-response
    data[1] = hmd[0]
    latency.hist_latency(data[::-1],alpha=0.8)
    plt.title('Hardware display latency')
    plt.show()