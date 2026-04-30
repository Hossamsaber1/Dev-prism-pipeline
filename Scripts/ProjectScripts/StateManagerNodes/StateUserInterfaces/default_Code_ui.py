# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'default_Code.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_wg_Code(object):
    def setupUi(self, wg_Code):
        if not wg_Code.objectName():
            wg_Code.setObjectName(u"wg_Code")
        wg_Code.resize(340, 384)
        self.verticalLayout = QVBoxLayout(wg_Code)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.w_name = QWidget(wg_Code)
        self.w_name.setObjectName(u"w_name")
        self.horizontalLayout_5 = QHBoxLayout(self.w_name)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(9, 0, 18, 0)
        self.l_name = QLabel(self.w_name)
        self.l_name.setObjectName(u"l_name")

        self.horizontalLayout_5.addWidget(self.l_name)

        self.e_name = QLineEdit(self.w_name)
        self.e_name.setObjectName(u"e_name")
        self.e_name.setMinimumSize(QSize(0, 0))
        self.e_name.setMaximumSize(QSize(9999, 16777215))

        self.horizontalLayout_5.addWidget(self.e_name)

        self.l_class = QLabel(self.w_name)
        self.l_class.setObjectName(u"l_class")
        font = QFont()
        font.setBold(True)
        self.l_class.setFont(font)

        self.horizontalLayout_5.addWidget(self.l_class)


        self.verticalLayout.addWidget(self.w_name)

        self.gb_code = QGroupBox(wg_Code)
        self.gb_code.setObjectName(u"gb_code")
        self.verticalLayout_2 = QVBoxLayout(self.gb_code)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.w_presets = QWidget(self.gb_code)
        self.w_presets.setObjectName(u"w_presets")
        self.horizontalLayout_7 = QHBoxLayout(self.w_presets)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(9, 0, 9, 0)
        self.l_code = QLabel(self.w_presets)
        self.l_code.setObjectName(u"l_code")

        self.horizontalLayout_7.addWidget(self.l_code)

        self.b_presets = QToolButton(self.w_presets)
        self.b_presets.setObjectName(u"b_presets")
        self.b_presets.setArrowType(Qt.DownArrow)

        self.horizontalLayout_7.addWidget(self.b_presets)


        self.verticalLayout_2.addWidget(self.w_presets)

        self.widget = QWidget(self.gb_code)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.te_code = QPlainTextEdit(self.widget)
        self.te_code.setObjectName(u"te_code")

        self.verticalLayout_3.addWidget(self.te_code)


        self.verticalLayout_2.addWidget(self.widget)

        self.w_execute = QWidget(self.gb_code)
        self.w_execute.setObjectName(u"w_execute")
        self.horizontalLayout_2 = QHBoxLayout(self.w_execute)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 9, 0)
        self.b_execute = QPushButton(self.w_execute)
        self.b_execute.setObjectName(u"b_execute")
        self.b_execute.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_2.addWidget(self.b_execute)


        self.verticalLayout_2.addWidget(self.w_execute)


        self.verticalLayout.addWidget(self.gb_code)


        self.retranslateUi(wg_Code)

        QMetaObject.connectSlotsByName(wg_Code)
    # setupUi

    def retranslateUi(self, wg_Code):
        wg_Code.setWindowTitle(QCoreApplication.translate("wg_Code", u"Code", None))
        self.l_name.setText(QCoreApplication.translate("wg_Code", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_Code", u"Code", None))
        self.gb_code.setTitle(QCoreApplication.translate("wg_Code", u"General", None))
        self.l_code.setText(QCoreApplication.translate("wg_Code", u"Code:", None))
        self.b_presets.setText(QCoreApplication.translate("wg_Code", u"...", None))
        self.b_execute.setText(QCoreApplication.translate("wg_Code", u"Execute now", None))
    # retranslateUi

