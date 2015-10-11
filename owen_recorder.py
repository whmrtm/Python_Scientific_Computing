# -*- coding: utf-8 -*-
"""
Created on Fri Sep  14 21:52:13 2015

@author: Owen
"""

import numpy as np
import pyaudio
import pylab as pl


class OwenRecorder():
    def __init__(self):
        '''built-in parameters'''
        self._channels = 2
        self._samplewidth = 2
        self._framerate = 48100
        self._active = False
        self._sec = 0.01
#        control the precision
        self._buffersize = 2**12
        

    def setup(self):
        '''setup basic parameters'''
        self.frames = int(self._framerate*self._sec/self._buffersize)
        if self.frames == 0:
            self.frames = 1                                    
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = pyaudio.paInt16,
                             channels = self._channels,
                             input = True,
                             rate = self._framerate,
                             frames_per_buffer = self._buffersize)
        self.audio = np.empty((self.frames*self._buffersize),
                                 dtype=np.int16)
                                 
        self.time = np.arange(0,self._sec,
                              self._sec/(self.frames*self._buffersize),
                                dtype = float)
        self.threadsDieNow = False
        self.newAudio = False
        
    def close(self):
        '''close'''
        self.p.close(self.stream)
    
    def test_read(self):
        '''test my read'''
        #TODO: could use flatten
        #extract one channel of signal
        str_data = []        
        data = self.stream.read(self._buffersize*self.frames)
        str_data.append(data)
        str_data = b''.join(str_data)
        wave_data = np.fromstring(str_data, dtype=np.int16) 
        if self._channels == 2:        
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            wave_data = wave_data[0]
        self.audio = wave_data
        return wave_data
        
    def fft(self,data=None,trimBy=6,logScale=False,divBy=100):
        '''Fourier transform'''        
        self.test_read()
        if data == None: 
                data = self.audio.flatten()
        left,right = np.split(np.abs(np.fft.fft(data)),2)
        ys = np.add(left,right[::-1])
        # log scale        
        if logScale:
            ys = np.multiply(20,np.log10(ys))
        xs = np.arange(self._buffersize/2,dtype=float)
        # control frequency range
        if trimBy:
            i = int((self._buffersize/2)/trimBy)
            ys = ys[:i]
            xs = xs[:i]*self._framerate/self._buffersize
        # control anplitude
        if divBy:
            ys = ys/float(divBy)
        return xs,ys
        
       
#test:
OR = OwenRecorder()
OR.setup()
pl.show()
xs,ys = OR.fft()
points, = pl.plot(xs,ys)
points.set_linewidth(2.5)
pl.ylabel("Amplitude")
pl.xlabel("Frequency")
pl.ylim(0,4000)
pl.title("Realtime FFT Demonstration")

while True:    
    xs,ys = OR.fft()
    points.set_data(xs,ys)
    pl.pause(0.01)
    
    
