# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 09:58:12 2019

@author: aman
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def latency(fname,threshold=50,iti=0,ioffset=0):
    parts = os.path.split(fname)[1].split('_')
    if threshold == 'file':
        threshold = int(parts[1])
    
    data = pd.read_csv(fname,usecols=range(4))
    analog = data[data.RegisterAddress == 44]
    digital = data[data.RegisterAddress == 32]
    feedback = analog.DataElement0
    dfeedback = (feedback > threshold).astype(np.int8)
    rising = np.flatnonzero(dfeedback.diff() > 0.0)
    impulsetimes = digital[digital.DataElement0 == 1].Timestamp
    responsetimes = analog.Timestamp.iloc[rising+ioffset]
    if iti > 0:
        valid = ~(responsetimes.diff() < iti)
        responsetimes = responsetimes[valid]
    
    if len(impulsetimes) != len(responsetimes):
        print("WARNING: Impulse/response mismatch! Review threshold value.")
    
    impulsetimes.reset_index(drop=True,inplace=True)
    responsetimes.reset_index(drop=True,inplace=True)
    latency = 1000 * (responsetimes - impulsetimes)
    latency.name = parts[0]
    return analog,feedback,dfeedback,impulsetimes,responsetimes,latency

def visualize_latency(latency):
    plt.figure()
    plt.plot(latency[0].Timestamp,latency[0].DataElement0)
    plt.vlines(latency[3],0,200,colors='k',label='input')
    plt.vlines(latency[4],0,200,colors='r',label='response')
    plt.xlabel('Time (s)')
    plt.ylabel('Diode (a.u.)')
    plt.legend()
    
def stats_latency(groups,labels=None):
    plt.figure()
    results = [latency[5] for latency in groups]
    x = range(len(results))
    if labels is None:
        labels = [latency[5].name for latency in groups]
    mean = [r.mean() for r in results]
    sem = [r.std() for r in results]
    plt.bar(x,mean)
    plt.errorbar(x,mean,sem,ecolor='k',fmt='none')
    plt.ylabel('Latency (ms)')
    plt.xticks(x,labels,rotation=45,ha='right')
    
def hist_latency(groups,labels=None,fps=720,**kwargs):
    plt.figure()
    binstep = 1000.0 / fps
    results = [latency[5] for latency in groups]
    if labels is None:
        labels = [latency[5].name for latency in groups]
    for r,label in zip(results,labels):
        minbin = np.floor_divide(r.min(), binstep) * binstep
        maxbin = np.floor_divide(r.max(), binstep)
        bins = np.arange(minbin,(maxbin+1)*binstep,binstep)
        plt.hist(r,bins=bins,label=label,**kwargs)
    plt.xlabel('Latency (ms)')
    plt.ylabel('Frequency')
    plt.legend()