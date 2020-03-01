# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 14:45:01 2020

@author: gonca
"""

import pandas as pd

def load(fname):
    data = pd.read_csv(fname,usecols=range(4))
    digin = data[(data.RegisterAddress == 32) & (data.DataElement0 == 1)]
    digout = data[data.RegisterAddress == 34]
    digin.reset_index(inplace=True)
    digout.reset_index(inplace=True)
    
    if len(digin) != len(digout):
        print("WARNING: Impulse/response mismatch! Dataset may be corrupt.")
        
    return digout.Timestamp - digin.Timestamp