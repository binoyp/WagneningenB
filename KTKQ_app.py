# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 22:21:23 2015

@author: Binoy
"""

from PyQt4 import QtGui
from PyQt4.QtCore import *
import os, subprocess

from ui_MainForm import Ui_MainWindow, MatplotlibWidget
from loadparam import ktparam,kqparam
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from ktkq_ver1 import *

class mainWin(QtGui.QMainWindow, Ui_MainWindow):
    """
    main window class

    """

    def __init__(self):
        super(mainWin, self).__init__()
        self.setupUi(self)
        self.cmd_takeval.setEnabled(0)
    @pyqtSignature("")
    def on_cmd_pltkq_clicked(self):
        
        self.aea0 = float(self.wid_le_aea0.text())
        self.z = int(self.wid_le_z.text())
        self.jvals = np.arange(0.01,1.5,.1) 
        js =[0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

        if self.chkRange.checkState():
            pass
        else:
            self.pd = float(self.wid_le_pd.text())
  
        kqs = [kq( j, self.pd, self.aea0, self.z) for j in js]
        kts = [kt( j, self.pd, self.aea0, self.z) for j in js]
            
        tab = np.transpose(np.vstack((js,kqs,kts)))
        dat =  tabulate(tab,headers = ['j' ,'kq', 'kt'],tablefmt = "plain", stralign = 'right') +"\n"
        
        
        self.wid_te.setTabStopWidth(8)
        self.wid_te.setPlainText(dat)
        self.kqvals = np.array([kq(v,self.pd, self.aea0,self.z) for v in self.jvals])
        self.ktvals = np.array([kt(v,self.pd, self.aea0,self.z) for v in self.jvals])
        self.etavals = (self.ktvals*self.jvals)/(self.kqvals*2*3.14)
        self.ktfit = np.polyfit(self.jvals,self.ktvals,3)
        self.kqfit = np.polyfit(self.jvals, self.kqvals, 3)
        self.etafit = np.polyfit(self.jvals, self.etavals, 3)
#        print ktfit
        self.mplwid.axes.clear()
        self.mplwid.axes.plot(self.jvals,self.kqvals*10, label = "$10 K_Q$")
        self.mplwid.axes.grid(1)
        self.mplwid.axes.hold(1)
        self.mplwid.axes.set_ylim(0,0.8)
        self.mplwid.axes.plot(self.jvals,self.ktvals, label = "$K_T$")
#        self.mplwid.axes.plot(self.jvals,self.etavals, label = "$\eta_0$")
        self.mplwid.axes.legend()
        self.mplwid.draw()  
        self.cmd_takeval.setEnabled(1)
    
    @pyqtSignature("")
    def on_cmd_takeval_clicked(self):
        
        seliden = self.comboBox.currentText()
        
        if seliden =="kt":

            ktident = float(self.wid_le_ktkq.text())
            pol2 = self.ktfit[:]
            pol2[-1] = pol2[-1] - ktident
            polsol = np.roots(pol2)
            
            roots  = filter(lambda x: (float(x)>0) & (float(x) <1.4), polsol)
            self.wid_te.appendPlainText('\n' + str(roots))
            selj = roots[0]
            self.mplwid.axes.hlines(ktident, 0, selj)
            self.mplwid.axes.vlines(selj,0,kt(selj,self.pd,self.aea0,self.z))
            self.mplwid.draw()
            self.cmd_takeval.setEnabled(0)
            outdat = "\nselected j :\t"+str(selj) + "\n" + "kq val:" + str(kq(selj,self.pd,self.aea0,self.z))
            self.wid_te.appendPlainText(outdat)
        if seliden =="kq":

            kqident = float(self.wid_le_ktkq.text())
            pol2 = self.kqfit[:]
            pol2[-1] = pol2[-1] - kqident
            polsol = np.roots(pol2)
            
            roots  = filter(lambda x: (float(x)>0) & (float(x) <1.4), polsol)
            self.wid_te.appendPlainText('\n' + str(roots))
            
            selj = roots[0]
            self.mplwid.axes.hlines(kqident*10, 0, selj)
            self.mplwid.axes.vlines(selj,0,kq(selj,self.pd,self.aea0,self.z)*10)
            self.mplwid.draw()
            self.cmd_takeval.setEnabled(0)
            outdat = "\nselected j :\t"+str(selj) + "\n" + "kt val:" + str(kt(selj,self.pd,self.aea0,self.z))
            self.wid_te.appendPlainText(outdat)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)    
    app.setStyle("Cleanlooks")
    window = mainWin()

    window.show()
    r = app.exec_()
#    r = raw_input("Hit enter")

    
