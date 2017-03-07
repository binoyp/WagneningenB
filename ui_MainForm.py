# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 672)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.mplwid = MatplotlibWidget(self.centralwidget)
        self.mplwid.setMinimumSize(QtCore.QSize(0, 500))
        self.mplwid.setObjectName(_fromUtf8("mplwid"))
        self.horizontalLayout_2.addWidget(self.mplwid)
        self.wid_te = QtGui.QPlainTextEdit(self.centralwidget)
        self.wid_te.setMaximumSize(QtCore.QSize(300, 16777215))
        self.wid_te.setObjectName(_fromUtf8("wid_te"))
        self.horizontalLayout_2.addWidget(self.wid_te)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.wid_le_aea0 = QtGui.QLineEdit(self.centralwidget)
        self.wid_le_aea0.setObjectName(_fromUtf8("wid_le_aea0"))
        self.gridLayout.addWidget(self.wid_le_aea0, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.wid_le_z = QtGui.QLineEdit(self.centralwidget)
        self.wid_le_z.setObjectName(_fromUtf8("wid_le_z"))
        self.gridLayout.addWidget(self.wid_le_z, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cmd_pltkq = QtGui.QPushButton(self.centralwidget)
        self.cmd_pltkq.setObjectName(_fromUtf8("cmd_pltkq"))
        self.gridLayout.addWidget(self.cmd_pltkq, 3, 1, 1, 1)
        self.wid_le_pd = QtGui.QLineEdit(self.centralwidget)
        self.wid_le_pd.setObjectName(_fromUtf8("wid_le_pd"))
        self.gridLayout.addWidget(self.wid_le_pd, 1, 1, 1, 1)
        self.chkRange = QtGui.QCheckBox(self.centralwidget)
        self.chkRange.setObjectName(_fromUtf8("chkRange"))
        self.gridLayout.addWidget(self.chkRange, 1, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.wid_le_ktkq = QtGui.QLineEdit(self.centralwidget)
        self.wid_le_ktkq.setObjectName(_fromUtf8("wid_le_ktkq"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.wid_le_ktkq)
        self.cmd_takeval = QtGui.QPushButton(self.centralwidget)
        self.cmd_takeval.setObjectName(_fromUtf8("cmd_takeval"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.cmd_takeval)
        self.horizontalLayout.addLayout(self.formLayout_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_Exit = QtGui.QAction(MainWindow)
        self.action_Exit.setObjectName(_fromUtf8("action_Exit"))
        self.menuFile.addAction(self.action_Exit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Kt Kq Plotter", None))
        self.wid_le_aea0.setText(_translate("MainWindow", "0.7", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">A</span><span style=\" font-size:11pt; vertical-align:sub;\">E </span><span style=\" font-size:11pt;\">/A</span><span style=\" font-size:11pt; vertical-align:sub;\">0</span></p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "Z", None))
        self.wid_le_z.setText(_translate("MainWindow", "4", None))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt;\">P/D</span></p></body></html>", None))
        self.cmd_pltkq.setText(_translate("MainWindow", "Plot kt kq curve", None))
        self.wid_le_pd.setText(_translate("MainWindow", "0.8", None))
        self.chkRange.setText(_translate("MainWindow", "Range", None))
        self.label_4.setText(_translate("MainWindow", "IIdentity", None))
        self.comboBox.setItemText(0, _translate("MainWindow", "kt", None))
        self.comboBox.setItemText(1, _translate("MainWindow", "kq", None))
        self.label_5.setText(_translate("MainWindow", "Value", None))
        self.cmd_takeval.setText(_translate("MainWindow", "Take Vaues", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.action_Exit.setText(_translate("MainWindow", "&Exit", None))

from matplotlibwidget import MatplotlibWidget
