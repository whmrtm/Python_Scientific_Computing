# -*- coding: utf-8 -*-
import pyaudio
import wave

chunk = 1024

wf = wave.open(r"sample.wav", 'rb')

p = pyaudio.PyAudio()

stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

while True:
    data = wf.readframes(chunk)
    if data == "": break
    stream.write(data)

stream.close()
p.terminate()