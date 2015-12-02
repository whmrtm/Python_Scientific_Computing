# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 17:05:47 2015

@author: Owen
"""

import numpy as np
import wave
import csv
'''Read wav file to get the data'''
def readwav(path):
    f = wave.open(path,"rb")
    # get parameters
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    print(params)
    # read data of the wave
    str_data = f.readframes(nframes)
    f.close()

    #transfer data into array (float64 format!!)
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data = np.array(wave_data, dtype=np.float64)    
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    # The data has to be c-continuous and writable
    wave_data = np.require(wave_data, dtype=np.float64,
                           requirements=['C','W'])
    #time = np.arange(0, nframes) * (1.0 / framerate)
    #For this program, just return one channel of data for convenience
    return framerate, sampwidth, nframes, wave_data

framerate, sample_width, nframes, wave_data = readwav("sample.wav")

#modify wave_data to adapt to the analog limit [-10, 10]
#Sample width(in python is byte)
#8 — Allocates 8 bits to each sample, allowing a resolution of 256 levels
#16 — Allocates 16 bits to each sample, allowing a resolution of 65536 levels
#24 — Allocates 24 bits to each sample, allowing a resolution of 16777216 levels
wave_data = 20/(2**(sample_width*8))*wave_data
rows = zip(wave_data[0],wave_data[1])
csvWrite = csv.writer(open('testfile.csv','w',newline=''))
csvWrite.writerows(rows)