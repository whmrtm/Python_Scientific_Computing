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
        self._channels = 2
        self._samplewidth = 2
        self._framerate = 44100
        self._active = False
        self._sec = 0.05
        self._buffersize = 1024
        
        

    def setup(self):
        self.frames = int(self._framerate/self._buffersize*self._sec)                        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = pyaudio.paInt16,
                             channels = self._channels,
                             input = True,
                             rate = self._framerate,
                             frames_per_buffer = self._buffersize)
        self.audio = np.empty((self.frames*self._buffersize),
                                 dtype=np.int16)
        self.time = np.arange(0,self._sec,self._sec/(self.frames*self._buffersize))
        self.threadsDieNow = False
        self.newAudio = False
    def close(self):
        self.p.close(self.stream)
    
    def test_read(self):
        str_data = []        
        data = self.stream.read(self._buffersize*self.frames)
        str_data.append(data)
        str_data = b''.join(str_data)
        wave_data = np.fromstring(str_data, dtype=np.int16)
        wave_data.shape = -1, 2
        wave_data = wave_data.T
        self.audio = wave_data[0]
        return wave_data[0]
    def record(self):
        """Record data from stream"""
        while not self.threadsDieNow:            
            str_data = []        
            for i in range(self.frames):
                data = self.stream.read(self._buffersize)
                str_data.append(data)
            str_data = b''.join(str_data)
            wave_data = np.fromstring(str_data, dtype=np.short)
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            self.audio = wave_data[0]
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

#OR.setup()
#OR.continuousStart()
#OR.close()
#OR.continuousEnd()
#
#OR.audio_plot()
#OR.test_read()
#OR.audio_plot()
#
#                
        

