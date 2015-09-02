# -*- coding: utf-8 -*-
import wave
import numpy as np
import scipy.signal as signal

framerate = 44100
time = 10

# Generate 10 seconds of 44.1Hz from 100Hz~1kHz wave
t = np.arange(0, time, 1.0/framerate)
wave_data = signal.chirp(t, 100, time, 1000, method='linear') * 10000
wave_data = wave_data.astype(np.short)

# open wav file
f = wave.open(r"C:\Users\Owen\Desktop\audio\sweep.wav", "wb")

# set channal, width, and framerate
f.setnchannels(1)
f.setsampwidth(2)
f.setframerate(framerate)
# transfer to binary file
f.writeframes(wave_data.tostring())
f.close()