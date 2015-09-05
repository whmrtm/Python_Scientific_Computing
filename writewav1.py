# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 10:46:01 2015

@author: Owen
"""

import wave
import numpy as np
import pylab as plt
import struct

framerate = 44100
time = 5

time = np.arange(0,time,1./framerate)
#y = np.linspace(1,1,time*framerate).tostring()
wv = wave.open("wvtest1.wav","wb")
wv.setparams((2, 2, framerate, 0, 'NONE', 'not compressed'))
for i in range(0, 44100*5):
        value = int(np.sin(i)*2*1000)
        packed_value = struct.pack('h', value)
        wv.writeframes(packed_value)
        wv.writeframes(packed_value)

wv.close()



#plt.specgram(y,NFFT=100,noverlap = 0,Fs=1./dt)
#plt.show()



