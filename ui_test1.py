# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 20:46:09 2015

@author: Owen
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 16:53:40 2015

@author: Owen
"""

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt
from owen_recoder import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(569, 391)
        self.qwtPlot = Qwt5.QwtPlot(Form)
        self.qwtPlot.setGeometry(QtCore.QRect(60, 60, 400, 200))
        self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.plot()
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
    def plot(self):
        
        c = Qwt.QwtPlotCurve()
        c.attach(self.qwtPlot)
        self.timer = QtCore.QTimer()
        self.timer.start(1.0)

#        OR = OwenRecorder()   
#        x = OR.test_plot()
#        y = OR.audio        
        x = np.linspace(0,100,2000)
        y = np.sin(x)
        c.setData(x,y)        
        self.qwtPlot.replot()
from PyQt4 import Qwt5
if __name__ == "__main__":
         
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
