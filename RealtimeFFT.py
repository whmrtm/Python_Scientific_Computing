# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 20:21:21 2015

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

        self.canvas().setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Plain)
        self.canvas().setLineWidth(1)
        # Initialize data


        self.OR = OwenRecorder()
        self.OR.setup()

        
        x, y = self.OR.fft()        

        self.setTitle("A QwtPlot Demonstration")
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);
        
        self.curve = Qwt.QwtPlotCurve("WTF")
        
        self.curve.attach(self)
#        self.curve.setSymbol(Qwt.QwtSymbol(Qwt.QwtSymbol.Ellipse,
#                                        QtGui.QBrush(),
#                                        QtGui.QPen(QtCore.Qt.yellow),
#                                        QtCore.QSize(7, 7)))
        self.curve.setPen(QtGui.QPen(QtCore.Qt.blue))
        self.curve.setData(x,y)
        

        mY = Qwt.QwtPlotMarker()
        mY.setYValue(0.0)
        mY.attach(self)
        
        self.setAxisScale(Qwt.QwtPlot.yLeft,0,1400,200)
        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Values")   

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
#    myplot.OR.continuousStart()
    myplot.show()
    myplot.OR.close()
    
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()