# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Wed Nov  9 20:19:04 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(454, 355)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(199, 20, 161, 21))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.nickname_field = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.nickname_field.setObjectName("nickname_field")
        self.horizontalLayout_3.addWidget(self.nickname_field)
        self.status_field = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.status_field.setObjectName("status_field")
        self.horizontalLayout_3.addWidget(self.status_field)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 161, 311))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.user_nickname_field = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.user_nickname_field.setObjectName("user_nickname_field")
        self.horizontalLayout_4.addWidget(self.user_nickname_field)
        self.user_status_field = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.user_status_field.setObjectName("user_status_field")
        self.horizontalLayout_4.addWidget(self.user_status_field)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.users_list = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.users_list.setObjectName("users_list")
        self.verticalLayout_4.addWidget(self.users_list)
        self.message_edit = QtWidgets.QLineEdit(Form)
        self.message_edit.setGeometry(QtCore.QRect(200, 300, 211, 27))
        self.message_edit.setObjectName("message_edit")
        self.send_btn = QtWidgets.QPushButton(Form)
        self.send_btn.setGeometry(QtCore.QRect(420, 300, 21, 26))
        self.send_btn.setObjectName("send_btn")
        self.message_list = QtWidgets.QListWidget(Form)
        self.message_list.setGeometry(QtCore.QRect(200, 50, 241, 231))
        self.message_list.setObjectName("message_list")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Faker`s messanger"))
        self.nickname_field.setText(_translate("Form", "nickname"))
        self.status_field.setText(_translate("Form", "status"))
        self.user_nickname_field.setText(_translate("Form", "nickname"))
        self.user_status_field.setText(_translate("Form", "status"))
        self.send_btn.setText(_translate("Form", "<-"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

