# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 13:28:05 2019

@author: aman
"""

import os
import fps
import latency
import roundtrip
import matplotlib.pyplot as plt

def trials(dname,module,include=None,suffix='.csv',**kwargs):
    if include is None:
        include = lambda x:x.endswith(suffix)
    elif type(include) is str:
        match = include
        include = lambda x:x.endswith(suffix) and match in x       
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
    plt.xlabel('Number of Elements')
    plt.ylabel('Frames / second')
    plt.legend()
    plt.show()
    
def fig_fps_nonoverlap_144hz():
    bv = trials('../benchmarks/fps/acquisition/data/BonVision',fps)
    bv144 = trials('../benchmarks/fps/acquisition/data/BonVision144Hz',fps,
                   threshold=20)
    plt.figure()
    fps.stats_fps(bv144,label='BonVision 144Hz')
    fps.stats_fps(bv,label='BonVision')
    ticks = range(len(fps.gridsizes))
    plt.xticks(ticks,[fps.gridsizes[i]**2 for i in ticks])
    plt.title('Non-overlapping Elements (3s / trial)')
    plt.xlabel('Number of Elements')
    plt.ylabel('Frames / second')
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
    plt.xlabel('Number of Elements')
    plt.ylabel('Frames / second')
    plt.legend()
    plt.show()
    
def fig_fps_overlap_144Hz():
    bv = trials('../benchmarks/fps-overlap/acquisition/data/BonVision60Hz',fps,
                threshold=20)
    bv144 = trials('../benchmarks/fps-overlap/acquisition/data/BonVision144Hz',fps,
                   threshold=20)
    plt.figure()
    fps.stats_fps(bv144,label='BonVision 144Hz')
    fps.stats_fps(bv,label='BonVision 60Hz')
    ticks = range(len(fps.overlap))
    plt.xticks(ticks,[fps.overlap[i] for i in ticks])
    plt.title('Overlapping Elements (3s / trial)')
    plt.xlabel('Number of Elements')
    plt.ylabel('Frames / second')
    plt.legend()
    plt.show()

def fig_latency_software():
    data = trials('../benchmarks/latency/acquisition/data/software',latency)
    latency.hist_latency(data[::-1],alpha=0.8)
    plt.title('Closed-loop latency @ 60Hz')
    plt.show()
    
def fig_latency_software_frames():
    data = trials('../benchmarks/latency/acquisition/data/software',latency)
    latency.hist_sf_latency_frames(data[::-1],alpha=0.8)
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
    
def fig_latency_hardware_frames():
    data = trials('../benchmarks/latency/acquisition/data/hardware',latency)
    hmd = trials('../benchmarks/latency/acquisition/data/hardware-hmd',latency,
                 threshold=200,iti=0.2,ioffset=-1) # cleanup HMD photo-response
    data[1] = hmd[0]
    latency.hist_latency_frames(data[::-1],alpha=0.8)
    plt.title('Hardware display latency')
    plt.show()
    
def stats_latency_hardware():
    data = trials('../benchmarks/latency/acquisition/data/hardware',latency)
    hmd = trials('../benchmarks/latency/acquisition/data/hardware-hmd',latency,
                 threshold=200,iti=0.2,ioffset=-1) # cleanup HMD photo-response
    data[1] = hmd[0]
    results = (trial[5] for trial in data[::-1])
    return [(trial.name,trial.mean(),trial.std()*2,len(trial))
            for trial in results]
    
def stats_latency_hardware_frames():
    data = trials('../benchmarks/latency/acquisition/data/hardware',latency)
    hmd = trials('../benchmarks/latency/acquisition/data/hardware-hmd',latency,
                 threshold=200,iti=0.2,ioffset=-1) # cleanup HMD photo-response
    data[1] = hmd[0]
    ifi = [1000.0 / float(trial[5].name.split('-')[1].split('Hz')[0])
           for trial in data[::-1]]
    results = (trial[5]/interval for trial,interval in zip(data[::-1],ifi))
    return [(trial.name,trial.mean(),trial.std()*2,len(trial))
            for trial in results]
    
def stats_roundtrip():
    data = trials('../benchmarks/latency/harp/data',roundtrip)
    return [(trial.mean(),2*trial.std) for trial in data]

def fig_fps_videoplayback(size='720p'):
    labels = ['preload','stream-buf0','stream-buf1','stream-buf2','stream-buf4']
    data = [trials('../benchmarks/fps-video/acquisition/data/'+size,fps,
            include=label,threshold=20) for label in labels]
    plt.figure(size,figsize=(6,6))
    for condition,label in zip(data,labels):
        fps.stats_fps(condition,x=fps.playbackrates,label=label)
    plt.xlabel('Requested Frame Rate (Hz)')
    plt.ylabel('Actual Frame Rate (Hz)')
    plt.title('Resolution: {0}, Movie Frame Count = 300'.format(size.split('-')[-1]))
    plt.xlim(0,105)
    plt.ylim(0,105)
    plt.legend(loc='upper left')

def fig_fps_videoplayback_framecount(size='720p'):
    labels = ['preload','stream-buf0','stream-buf1','stream-buf2','stream-buf4']
    data = [trials('../benchmarks/fps-video/acquisition/data/'+size,fps,
            include=label,threshold=20) for label in labels]
    plt.figure(size,figsize=(6,6))
    for condition,label in zip(data,labels):
        fps.stats_frame_count(condition,x=fps.playbackrates,label=label)
    plt.xlabel('Requested Frame Rate (Hz)')
    plt.ylabel('Measured Frame Count')
    plt.title('Resolution: {0}, Movie Frame Count = 300'.format(size.split('-')[-1]))
    plt.ylim(250,310)
    plt.ylim(50,310)
    plt.legend(loc='lower left')
    
def aux_drop_distribution_trial(trial):
    intervals = []
    for t,targetfps in zip(trial[-2],fps.playbackrates):
        threshold = 1.5 / targetfps
        ifi = (t.diff()/2).reset_index().Timestamp
        intervals.append(ifi[ifi > threshold])
    return intervals

def aux_drop_distribution_condition(condition):
    drops = [aux_drop_distribution_trial(trial) for trial in condition]
    aggregate = [pd.concat(trial[0]).index for trial in zip(drops)]
    return aggregate
    
def fig_fps_videoplayback_dropdistribution(size='720p'):
    labels = ['preload','stream-buf0','stream-buf1','stream-buf2','stream-buf4']
    data = [trials('../benchmarks/fps-video/acquisition/data/'+size,fps,
            include=label,threshold=20) for label in labels]
    plt.figure(size,figsize=(6,6))
    for condition,label in zip(data,labels):
        drops = [aux_drop_distribution_trial(trial) for trial in condition]
        aggregate = [pd.concat(trial[0]).index for trial in zip(drops)]
        
#        fps.stats_frame_count(condition,x=fps.playbackrates,label=label)
        break
    