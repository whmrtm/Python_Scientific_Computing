# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:13:07 2015

@author: Owen
"""

# -*- coding: utf-8 -*-
import wave
import pylab as pl
import numpy as np


f = wave.open(r"C:\Users\Owen\desktop\sample.wav", "rb")

# (nchannels, sampwidth, framerate, nframes, comptype, compname)
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

# read data of the wave
str_data = f.readframes(nframes)
f.close()

#transfer data into array
wave_data = np.fromstring(str_data, dtype=np.short)
wave_data.shape = -1, 2
wave_data = wave_data.T
time = np.arange(0, nframes) * (1.0 / framerate)

# plot
pl.subplot(211) 
pl.plot(time, wave_data[0])
pl.subplot(212) 
pl.plot(time, wave_data[1], c="g")
pl.xlabel("time (seconds)")
pl.show()