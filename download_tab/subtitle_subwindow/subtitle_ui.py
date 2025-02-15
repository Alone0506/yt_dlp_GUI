# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\wii03\Desktop\video_downloader\download_tab\subtitle_subwindow\subtitle.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(826, 568)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        Form.setFont(font)
        Form.setStyleSheet("QWidget {\n"
"    background-color: #F0F4F4;\n"
"    color: #2E7D32;\n"
"}\n"
"\n"
"/* QLabel settings */\n"
"QLabel {\n"
"    color: #2E7D32;\n"
"}\n"
"\n"
"/* QPushButton settings */\n"
"QPushButton {\n"
"    background-color: #A5D6A7;\n"
"    border: 1px solid #81C784;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #81C784;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #4CAF50;\n"
"}\n"
"\n"
"/* QTableWidget settings */\n"
"QTableWidget {\n"
"    background-color: #FFFFFF;\n"
"    alternate-background-color: #E8F5E9;  /* 表格的交替行背景颜色 */\n"
"    gridline-color: #A5D6A7;   /* 網格線 */\n"
"    selection-background-color: #A5D6A7;\n"
"    border: 1px solid #81C784;\n"
"}\n"
"QTableWidget::item {\n"
"    border: 1px solid #81C784;\n"
"    padding: 2px;\n"
"}\n"
"QTableWidget::item::selected{\n"
"    color:white;\n"
"    background:#609d78;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #426c54;\n"
"    color: white;\n"
"    padding: 4px;\n"
"    border: 1px solid #81C784;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.subtitles_table = QtWidgets.QTableWidget(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.subtitles_table.setFont(font)
        self.subtitles_table.setObjectName("subtitles_table")
        self.subtitles_table.setColumnCount(8)
        self.subtitles_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.subtitles_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.subtitles_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.subtitles_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.subtitles_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.subtitles_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.subtitles_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.subtitles_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.subtitles_table.setHorizontalHeaderItem(7, item)
        self.subtitles_table.horizontalHeader().setMinimumSectionSize(25)
        self.verticalLayout.addWidget(self.subtitles_table)
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.auto_subtitles_table = QtWidgets.QTableWidget(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.auto_subtitles_table.setFont(font)
        self.auto_subtitles_table.setObjectName("auto_subtitles_table")
        self.auto_subtitles_table.setColumnCount(8)
        self.auto_subtitles_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.auto_subtitles_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.auto_subtitles_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.auto_subtitles_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.auto_subtitles_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.auto_subtitles_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.auto_subtitles_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.auto_subtitles_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.auto_subtitles_table.setHorizontalHeaderItem(7, item)
        self.auto_subtitles_table.horizontalHeader().setDefaultSectionSize(100)
        self.auto_subtitles_table.horizontalHeader().setMinimumSectionSize(25)
        self.verticalLayout.addWidget(self.auto_subtitles_table)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.ok_btn = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        self.ok_btn.setFont(font)
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout.addWidget(self.ok_btn)
        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Subtitle"))
        self.label.setText(_translate("Form", "Subtitles (suggest vtt)"))
        item = self.subtitles_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "LANGUAGE"))
        item = self.subtitles_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "NAME"))
        item = self.subtitles_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "json3"))
        item = self.subtitles_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "srv1"))
        item = self.subtitles_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "srv2"))
        item = self.subtitles_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "srv3"))
        item = self.subtitles_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "ttml"))
        item = self.subtitles_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "vtt"))
        self.label_2.setText(_translate("Form", "Auto Subtitles (suggest vtt)"))
        item = self.auto_subtitles_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "LANGUAGE"))
        item = self.auto_subtitles_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "NAME"))
        item = self.auto_subtitles_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "json3"))
        item = self.auto_subtitles_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "srv1"))
        item = self.auto_subtitles_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "srv2"))
        item = self.auto_subtitles_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "srv3"))
        item = self.auto_subtitles_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "ttml"))
        item = self.auto_subtitles_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "vtt"))
        self.label_4.setText(_translate("Form", "You can select no subtitle or select multiple subtitles."))
        self.ok_btn.setText(_translate("Form", "ok !"))
