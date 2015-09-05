import ui_plot
import sys
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from owen_recoder import *

def plotSomething():
    x = OR.test_plot()
    y = OR.audio
    c.setData(x,y)
    uiplot.qwtPlot.replot()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    win_plot = ui_plot.QtGui.QMainWindow()
    uiplot = ui_plot.Qwt5
    uiplot.setupUi(win_plot)
    #uiplot.btnB.clicked.connect(lambda: uiplot.timer.setInterval(100.0))
    #uiplot.btnC.clicked.connect(lambda: uiplot.timer.setInterval(10.0))
    #uiplot.btnD.clicked.connect(lambda: uiplot.timer.setInterval(1.0))
    c=Qwt.QwtPlotCurve()  
    c.attach(uiplot.qwtPlot)

    uiplot.qwtPlot.setAxisScale(uiplot.qwtPlot.yLeft, 0, 1000)

    uiplot.timer = QtCore.QTimer()
    uiplot.timer.start(1.0)

    win_plot.connect(uiplot.timer, QtCore.SIGNAL('timeout()'), plotSomething) 
    
    OR = OwenRecorder()
    

    ### DISPLAY WINDOWS
    win_plot.show()
    code=app.exec_()
    SR.close()
    sys.exit(code)