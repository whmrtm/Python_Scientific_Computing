# -*- coding: utf-8 -*-
"""
Created on Mon Sep  17 20:21:21 2015
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

        # Initialize data


        self.OR = OwenRecorder()
        self.OR.setup()

        
        x, y = self.OR.fft()        
        # set canvas
        self.setTitle("A RealtimeFFT Demonstration")
        self.canvas().setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Plain)
        self.canvas().setLineWidth(1)    
        # set curve parameter
        self.curve = Qwt.QwtPlotCurve("Frequency")
        self.curve.setPen(QtGui.QPen(QtCore.Qt.blue,1.5))
        self.curve.setStyle(Qwt.QwtPlotCurve.Lines)
        self.curve.setCurveAttribute(Qwt.QwtPlotCurve.Fitted, True)
        self.curve.attach(self)        
        # set axis                
        self.setAxisScale(Qwt.QwtPlot.yLeft,0,1400,200)
        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Frequency")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Amplitude")   
        # Update the plot every 100ms
        self.startTimer(100)

    def timerEvent(self,event):
        self.OR.setup()
        x,y = self.OR.fft()
        self.curve.setData(x,y)
        self.replot()
        
def main():  
    app = QtGui.QApplication(sys.argv)
    myplot = DataPlot()
    myplot.resize(500,300)
    myplot.show()
    myplot.OR.close()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()