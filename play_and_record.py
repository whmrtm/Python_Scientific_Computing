# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:33:54 2015

@author: Owen
"""
# -*- coding: utf-8 -*-
import pyaudio
import wave
import numpy as np
import pylab as pl


wf = wave.open(r"sample.wav", 'rb')


CHUNK = 1024
RATE = wf.getframerate()
params = wf.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]




pread = pyaudio.PyAudio()
precord = pyaudio.PyAudio()
# Open stream
stream1 = pread.open(format = pread.get_format_from_width(sampwidth),
                channels = nchannels,
                rate = framerate,
                output = True)

stream2 = precord.open(format = pread.get_format_from_width(sampwidth),
                channels = nchannels,
                rate = framerate,
                input = True)
# write stream
print("* recording")

frames = []
while True:
    data = wf.readframes(CHUNK)
    if data == "": break
    stream1.write(data)
    read_data = stream2.read(CHUNK)
    frames.append(read_data)

print("* done recording")
    




stream1.close()
stream2.close()

pread.terminate()
precord.terminate()


wf.close()
wf = wave.open(r"sample.wav", 'rb')

read_data = wf.readframes(nframes)

frames = b''.join(frames)
wave_data = np.fromstring(frames, dtype=np.short)
wave_data.shape = -1, 2
wave_data = wave_data.T

time = np.linspace(0,1000,len(wave_data[0]))


#transfer data into array
read_data = np.fromstring(read_data, dtype=np.short)
read_data.shape = -1, 2
read_data = read_data.T
time1 = np.arange(0, nframes) * (1.0 / framerate)
wf.close()

# plot
pl.subplot(321) 
pl.plot(time, wave_data[0])
pl.xlabel("Channel 1")

pl.subplot(323) 
pl.plot(time, wave_data[1])
pl.xlabel("Channel 2")
pl.subplot(325)
pl.magnitude_spectrum(wave_data[0],Fs = params[2])
#
pl.subplot(322) 
pl.plot(time1, read_data[0])
pl.subplot(324) 
pl.plot(time1, read_data[1],)
pl.xlabel("time (seconds)")
pl.subplot(326)
pl.magnitude_spectrum(read_data[0],Fs = params[2])
pl.show()
