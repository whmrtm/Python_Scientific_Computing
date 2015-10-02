# -*- coding: utf-8 -*-
"""
Created on Sun Sep  16 14:52:59 2015

@author: Owen
"""


import sys
from PyQt4 import QtGui, QtCore
import PyQt4.Qwt5 as Qwt
import PyQt4 as Qt
import numpy as np
from owen_recorder import *

class DataPlot(Qwt.QwtPlot):
    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

#        self.setCanvasBackground(Qt.Qt.w)
#        self.alignScales()
        self.canvas().setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Plain)
        self.canvas().setLineWidth(1)
        # Initialize data


        self.OR = OwenRecorder()
        self.OR.setup()

        self.x = np.arange(0,100*self.OR._sec,
                              self.OR._sec/(self.OR.frames*self.OR._buffersize),
                                dtype = float)
        self.y = np.zeros(len(self.x), float)
        
        self.setTitle("A Realtime Amplitude Demonstration")
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

        self.curve = Qwt.QwtPlotCurve("Amplitude")
        self.curve.attach(self)
        self.curve.setPen(QtGui.QPen(QtCore.Qt.red))


        mY = Qwt.QwtPlotMarker()
        mY.setYValue(0.0)
        mY.attach(self)
        
        self.setAxisScale(Qwt.QwtPlot.yLeft,-300,300,100)
        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Values")   

        self.startTimer(100)
    def timerEvent(self,event):
        self.OR.setup()
        single_length = len(self.OR.time)
        '''Move the plot from left to the right'''
        self.y = np.concatenate((self.y[:single_length],self.y[:-single_length]),1)
        single_result = self.OR.test_read()         
        for i in range(single_length):
            self.y[i] = single_result[i]
        self.curve.setData(self.x,self.y)        
        self.replot()
        
def main():  
    app = QtGui.QApplication(sys.argv)
    myplot = DataPlot()
    myplot.resize(500,300)
#    myplot.OR.continuousStart()
    myplot.show()
    myplot.OR.close()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()