# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Mon Jul 07 17:11:17 2014
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
        Form.resize(281, 171)
        self.LineEdit_USERKEY = QtGui.QLineEdit(Form)
        self.LineEdit_USERKEY.setGeometry(QtCore.QRect(90, 20, 161, 20))
        self.LineEdit_USERKEY.setObjectName(_fromUtf8("LineEdit_USERKEY"))
        self.Label_USERKEY = QtGui.QLabel(Form)
        self.Label_USERKEY.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.Label_USERKEY.setObjectName(_fromUtf8("Label_USERKEY"))
        self.Button_USERKEY = QtGui.QPushButton(Form)
        self.Button_USERKEY.setGeometry(QtCore.QRect(170, 50, 75, 23))
        self.Button_USERKEY.setCheckable(False)
        self.Button_USERKEY.setChecked(False)
        self.Button_USERKEY.setObjectName(_fromUtf8("Button_USERKEY"))
        self.Button_GETKEY = QtGui.QPushButton(Form)
        self.Button_GETKEY.setGeometry(QtCore.QRect(10, 50, 75, 23))
        self.Button_GETKEY.setObjectName(_fromUtf8("Button_GETKEY"))
        self.Label_INFO = QtGui.QLabel(Form)
        self.Label_INFO.setGeometry(QtCore.QRect(20, 100, 231, 21))
        self.Label_INFO.setFrameShape(QtGui.QFrame.NoFrame)
        self.Label_INFO.setText(_fromUtf8(""))
        self.Label_INFO.setObjectName(_fromUtf8("Label_INFO"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.Label_USERKEY.setText(_translate("Form", "输入USERKEY", None))
        self.Button_USERKEY.setText(_translate("Form", "确认", None))
        self.Button_GETKEY.setText(_translate("Form", "监听", None))

