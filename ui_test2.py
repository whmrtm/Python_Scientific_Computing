# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 22:42:55 2015

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

        # Initialize data
        OR = OwenRecorder()
        OR.setup()
        self.x = OR.time
        self.y = OR.test_read()

        self.setTitle("A QwtPlot Demonstration")
        self.insertLegend(Qwt.QwtLegend(), Qwt.QwtPlot.BottomLegend);

        self.curve = Qwt.QwtPlotCurve("WTF")
        self.curve.attach(self)
        self.curve.setPen(QtGui.QPen(QtCore.Qt.red))
        self.curve.setData(self.x,self.y)
        mY = Qwt.QwtPlotMarker()
        mY.setYValue(0.0)
        mY.attach(self)
        self.setAxisTitle(Qwt.QwtPlot.xBottom, "Time (seconds)")
        self.setAxisTitle(Qwt.QwtPlot.yLeft, "Values")
    

def main():  
    app = QtGui.QApplication(sys.argv)
    myplot = DataPlot()

    myplot.resize(500,300)
    myplot.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()