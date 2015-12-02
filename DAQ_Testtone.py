# -*- coding: utf-8 -*
"""
Created on Thu Oct 29 21:11:39 2015

@author: Owen

Analog input and output
Testtone using analog signal

"""

from PyDAQmx import *
import numpy as np
import time
import wave
import pylab as pl

'''Read wav file to get the data'''
def readwav(path):
    f = wave.open(path,"rb")
    # get parameters
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    print(params)
    # read data of the wave
    str_data = f.readframes(nframes)
    f.close()

    #transfer data into array (float64 format!!)
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data = np.array(wave_data, dtype=np.float64)    
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    # The data has to be c-continuous and writable
    wave_data = np.require(wave_data, dtype=np.float64,
                           requirements=['C','W'])
    #time = np.arange(0, nframes) * (1.0 / framerate)
    #For this program, just return one channel of data for convenience
    return framerate, sampwidth, nframes, wave_data[0]

framerate, sample_width, nframes, wave_data = readwav("sample.wav")

#modify wave_data to adapt to the analog limit [-10, 10]
#Sample width(in python is byte)
#8 — Allocates 8 bits to each sample, allowing a resolution of 256 levels
#16 — Allocates 16 bits to each sample, allowing a resolution of 65536 levels
#24 — Allocates 24 bits to each sample, allowing a resolution of 16777216 levels
wave_data = 20/(2**(sample_width*8))*wave_data


'''Write the data into the ao0 Channel'''

OutputChannel = "myDAQ1/ao0"
InputChannel = "myDAQ1/ai0"
SamplingRate = framerate

Writetask = TaskHandle()
DAQmxCreateTask("", Writetask)
DAQmxCreateAOVoltageChan(Writetask, OutputChannel, "",
                         -10, 10, DAQmx_Val_Volts, None)
DAQmxCfgSampClkTiming(Writetask, "", SamplingRate, DAQmx_Val_Rising, 
                      DAQmx_Val_ContSamps, nframes)
Written = DAQmxWriteAnalogF64(Writetask, nframes, 0, 0,
                              DAQmx_Val_GroupByChannel, wave_data, None, None)

'''Read data from ao1 Channel'''
Readtask = TaskHandle()
DAQmxCreateTask("", Readtask)
DAQmxCreateAIVoltageChan(Readtask, InputChannel, "", DAQmx_Val_Cfg_Default,
                         -10.0,10.0,DAQmx_Val_Volts,None)
DAQmxCfgSampClkTiming(Readtask,"",SamplingRate,
                      DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,nframes)



'''Start the tasks'''

'''TODO:make up the time delay to reduce error'''
DAQmxStartTask(Readtask)
DAQmxStartTask(Writetask)

read = int32()
data = np.zeros((nframes,), dtype=numpy.float64)
DAQmxReadAnalogF64(Readtask,nframes,10.0,DAQmx_Val_GroupByChannel,
                           data,nframes,byref(read),None)
DAQmxStopTask(Writetask)
DAQmxStopTask(Readtask)

'''Display the results '''

pl.figure(0) 
sec = nframes / framerate
time1 = np.linspace(0,sec,len(data))
pl.xlabel("Time/sec")
pl.ylabel("Voltage/v")
pl.plot(time1,data,'b')
print(len(data))

pl.figure(1)
pl.xlabel("Time/sec")
pl.ylabel("Voltage/v")
pl.plot(time1,wave_data,'g')
print(len(wave_data))