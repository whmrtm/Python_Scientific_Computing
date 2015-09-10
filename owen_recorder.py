# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 21:52:13 2015

@author: Owen
"""

#Owen's sound recorder, begin with just fft figure.
#Will work on the specgram version later on
import numpy as np
import pyaudio
import pylab as pl
import threading
#import struct

FRAMERATE = 44100

class OwenRecorder():
    def __init__(self):
        '''built-in parameters'''
        self._channels = 1
        self._samplewidth = 2
        self._framerate = 44100
        self._active = False
        self._sec = 0.1
#        control the precision
        self._buffersize = 2**12
        

    def setup(self):
        '''setup basic parameters'''
        self.frames = int(self._framerate/self._buffersize*self._sec)                        
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
    def fft(self,data=None,trimBy=6,logScale=False,divBy=200):
        self.test_read()
        if data == None: 
                data = self.audio.flatten()
        left,right = np.split(np.abs(np.fft.fft(data)),2)
        ys=np.add(left,right[::-1])
        if logScale:
            ys=np.multiply(20,np.log10(ys))
        xs=np.arange(self._buffersize/2,dtype=float)
        if trimBy:
            i=int((self._buffersize/2)/trimBy)
            ys=ys[:i]
            xs=xs[:i]*self._framerate/self._buffersize
        if divBy:
            ys=ys/float(divBy)
        return xs,ys
        
    def record(self):
        """Record data from stream"""
        while not self.threadsDieNow:            
            str_data = []        
            for i in range(self.frames):
                data = self.stream.read(self._buffersize)
                str_data.append(data)
            self.audio = str_data
            str_data = b''.join(str_data)
            wave_data = np.fromstring(str_data, dtype=np.short)
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            
            self.newAudio = True
                        
    def continuousStart(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target = self.record())
        self.t.start()
        

    def continuousEnd(self):
        """shut down continuous recording."""
        self.threadsDieNow = True
    def audio_plot(self):
        pl.plot(self.audio)
        pl.show()
#OR = OwenRecorder()
#
#OR.setup()
#OR.continuousStart()
#OR.close()
#OR.continuousEnd()
#
#OR.audio_plot()
#OR.test_read()
#xs,ys = OR.fft()
#print()
#pl.plot(xs,ys)
#pl.show()
#OR.audio_plot()
#
#                
        

