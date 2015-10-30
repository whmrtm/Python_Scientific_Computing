# -*- coding: utf-8 -*-
import wave
import pylab as pl
import numpy as np


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
f = wave.open(r"sample.wav", "rb")

# (nchannels, sampwidth, framerate, nframes, comptype, compname)
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
print(params)
# read data of the wave
str_data = f.readframes(nframes)
f.close()

#transfer data into array
wave_data = np.fromstring(str_data, dtype=np.short)
wave_data.shape = -1, 2
wave_data = wave_data.T
time = np.arange(0, nframes) * (1.0 / framerate)

# plot
pl.subplot(311) 
pl.plot(time, wave_data[0])
pl.subplot(312) 
pl.plot(time, wave_data[1], c="g")
pl.xlabel("time (seconds)")
pl.subplot(313)
pl.magnitude_spectrum(wave_data[0],Fs = params[2]                                                                                                                                                                                                                                                                                                                                                                                                                                        )
pl.show()