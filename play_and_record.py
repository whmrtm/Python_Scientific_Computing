# -*- coding: utf-8 -*-
"""
Created on Oct 15 21:33:54 2015

@author: Owen
"""
# -*- coding: utf-8 -*-
import pyaudio
import wave
import numpy as np
import pylab as pl

def readwav(path):
    f = wave.open(path,"rb")
    # get parameters
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
    return time, wave_data



readf = wave.open(r"sample.wav", 'rb')

CHUNK = 1024
params = readf.getparams()
CHANNELS, SAMPLEWIDTH, RATE, NFRAMES = params[:4]



# pyaudio for playing the file
pread = pyaudio.PyAudio()
# pyaudio for recording the sound
precord = pyaudio.PyAudio()

FORMAT = pread.get_format_from_width(SAMPLEWIDTH)

# Open stream
# stream 1 is for playing, while stream1 is for recording
stream1 = pread.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                output = True)

stream2 = precord.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True)
# write frames into stream2, record
print("* recording")

frames = []
while True:
    # write data in stream 1 and play the file
    data = readf.readframes(CHUNK)
    if data == "": break
    stream1.write(data)
    
    # Record the sound
    read_data = stream2.read(CHUNK)
    frames.append(read_data)

print("* done recording")
    
# close all
stream1.close()
stream2.close()

pread.terminate()
precord.terminate()

readf.close()

# write recorded data

wf = wave.open("output.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(SAMPLEWIDTH)
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()





time1, wave_data = readwav("sample.wav")
time2, read_data = readwav("output.wav")

print("time1: " + str(len(time1)),"time2: " + str(len(time2)))
#transfer data into array

# plot
pl.subplot(321) 
pl.plot(time1, wave_data[0],'g')
pl.xlabel("Original: Channel 1")

pl.subplot(323) 
pl.plot(time1, wave_data[1],'g')
pl.xlabel("Original: Channel 2")
pl.subplot(325)
pl.magnitude_spectrum(wave_data[0],Fs = RATE,color='g')

pl.subplot(322) 
pl.plot(time2, read_data[0],'b')
pl.xlabel("Record: Channel 1")

pl.subplot(324) 
pl.plot(time2, read_data[1],'b')
pl.xlabel("Record: Channel 2")
pl.subplot(326)
pl.magnitude_spectrum(read_data[0],Fs = RATE,color='b')
pl.show()
