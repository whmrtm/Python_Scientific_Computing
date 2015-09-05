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
        self._sec = 3
        self._buffersize = 1024
        self.threadsDieNow = False
        
        self.frames = int(self._framerate/self._buffersize*self._sec)                        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = pyaudio.paInt16,
                             channels = self._channels,
                             input = True,
                             rate = self._framerate,
                             frames_per_buffer = self._buffersize)
        self.audio = np.empty((self.frames*self._buffersize),
                                 dtype=np.int16)
    def setup(self):
        str_data = []        
        for i in range(self.frames):
            data = self.stream.read(self._buffersize)
            str_data.append(data)
        str_data = b''.join(str_data)
        return str_data
    def test_plot(self):
        """Test record data """
        str_data = self.setup()
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data.shape = -1, 2
        wave_data = wave_data.T
        self.audio = wave_data
        time = np.arange(0,self._sec,self._sec/(self.frames*self._buffersize))
        
        pl.plot(time,wave_data[0])
        pl.show()
        return time
    def record(self):
        """Record data from stream"""
        frames = int(self._framerate/self._buffersize*self._sec)
        while not self.threadsDieNow:            
            str_data = []        
            for i in range(frames):
                data = self.stream.read(self._buffersize)
                str_data.append(data)
            str_data = b''.join(str_data)
            wave_data = np.fromstring(str_data, dtype=np.short)
            wave_data.shape = -1, 2
            wave_data = wave_data.T
            self.audio = wave_data[0]
                        
    def continuousStart(self):
        """CALL THIS to start running forever."""
        self.t = threading.Thread(target = self.record())
        self.t.start()

    def continuousEnd(self):
        """shut down continuous recording."""
        self.threadsDieNow = True
    def audio_plot(self):
        pl.plot(self.audio.flatten)
        pl.show()
OR = OwenRecorder()

OR.setup()
OR.test_plot()

                
        

