# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon Jul 07 21:06:42 2014
#      by: PyQt4 UI code generator 4.10.1
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(426, 125)
        self.gridLayout_4 = QtGui.QGridLayout(Form)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.LineEdit_USERKEY = QtGui.QLineEdit(Form)
        self.LineEdit_USERKEY.setObjectName(_fromUtf8("LineEdit_USERKEY"))
        self.gridLayout_3.addWidget(self.LineEdit_USERKEY, 0, 1, 1, 2)
        self.Button_USERKEY = QtGui.QPushButton(Form)
        self.Button_USERKEY.setCheckable(False)
        self.Button_USERKEY.setChecked(False)
        self.Button_USERKEY.setObjectName(_fromUtf8("Button_USERKEY"))
        self.gridLayout_3.addWidget(self.Button_USERKEY, 1, 2, 1, 1)
        self.Label_USERKEY = QtGui.QLabel(Form)
        self.Label_USERKEY.setObjectName(_fromUtf8("Label_USERKEY"))
        self.gridLayout_3.addWidget(self.Label_USERKEY, 0, 0, 1, 1)
        self.Label_INFO = QtGui.QLabel(Form)
        self.Label_INFO.setFrameShape(QtGui.QFrame.NoFrame)
        self.Label_INFO.setObjectName(_fromUtf8("Label_INFO"))
        self.gridLayout_3.addWidget(self.Label_INFO, 2, 0, 1, 3)
        self.Button_GETKEY = QtGui.QPushButton(Form)
        self.Button_GETKEY.setObjectName(_fromUtf8("Button_GETKEY"))
        self.gridLayout_3.addWidget(self.Button_GETKEY, 1, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "灵异阴阳录代理", None))
        self.Button_USERKEY.setText(_translate("Form", "确认", None))
        self.Label_USERKEY.setText(_translate("Form", "输入USERKEY", None))
        self.Label_INFO.setText(_translate("Form", "提示", None))
        self.Button_GETKEY.setText(_translate("Form", "监听", None))

