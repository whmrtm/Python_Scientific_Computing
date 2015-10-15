# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 16:00:19 2015

@author: Owen
"""

import pyaudio
import wave
import time


wf = wave.open("sample.wav", 'rb')

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    print(data)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)
stream.stop_stream()
stream.close()
wf.close()

p.terminate()
