# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 21:11:39 2015

@author: Owen
"""

from PyDAQmx import *
import numpy as np
from numpy import pi
import time
import pylab as pl
def main():
    taskHandle = TaskHandle()
    DAQmxCreateTask("", taskHandle)
    
    physicalChannel = "myDAQ1/ao0"
    
    #write sine signal to the output channel    
    t = np.linspace(0, 2*pi, 1000)
    data = 6*np.sin(t)
    
    DAQmxCreateAOVoltageChan(taskHandle, physicalChannel, "", 
                              -10.0, 10.0, DAQmx_Val_Volts, None)
                              
    DAQmxCfgSampClkTiming(taskHandle, "", 100.0, DAQmx_Val_Rising, 
                           DAQmx_Val_ContSamps, 1000)
                           
    written = DAQmxWriteAnalogF64(taskHandle, 1000, 0, 10.0, 
                                   DAQmx_Val_GroupByChannel, data, None, None)
    Readtask = TaskHandle()
    DAQmxCreateTask("", Readtask)
    DAQmxCreateAIVoltageChan(Readtask, "myDAQ1/ai0", "", DAQmx_Val_Cfg_Default,
                                 -10.0,10.0,DAQmx_Val_Volts,None)
    DAQmxCfgSampClkTiming(Readtask,"",100,
                              DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,1000)
        
        
        
    read = int32()
    data1 = np.zeros((1000,), dtype=numpy.float64)
    DAQmxStartTask(Readtask)
    DAQmxStartTask(taskHandle)
        
    DAQmxReadAnalogF64(Readtask,1000,10.0,DAQmx_Val_GroupByChannel,
                           data1,1000,byref(read),None)

    DAQmxStopTask(taskHandle)
    DAQmxStopTask(Readtask)
        
    time1 = np.linspace(0,15,len(data1))
    pl.plot(time1,data1)
        
if __name__ == "__main__":
    main()
