# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Folder.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_wg_Folder(object):
    def setupUi(self, wg_Folder):
        if not wg_Folder.objectName():
            wg_Folder.setObjectName(u"wg_Folder")
        wg_Folder.resize(340, 20)
        self.verticalLayout = QVBoxLayout(wg_Folder)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(wg_Folder)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, 18, 0)
        self.l_name = QLabel(self.widget)
        self.l_name.setObjectName(u"l_name")

        self.horizontalLayout.addWidget(self.l_name)

        self.e_name = QLineEdit(self.widget)
        self.e_name.setObjectName(u"e_name")

        self.horizontalLayout.addWidget(self.e_name)

        self.l_class = QLabel(self.widget)
        self.l_class.setObjectName(u"l_class")
        font = QFont()
        font.setBold(True)
        self.l_class.setFont(font)

        self.horizontalLayout.addWidget(self.l_class)


        self.verticalLayout.addWidget(self.widget)


        self.retranslateUi(wg_Folder)

        QMetaObject.connectSlotsByName(wg_Folder)
    # setupUi

    def retranslateUi(self, wg_Folder):
        wg_Folder.setWindowTitle(QCoreApplication.translate("wg_Folder", u"Folder", None))
        self.l_name.setText(QCoreApplication.translate("wg_Folder", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_Folder", u"Folder", None))
    # retranslateUi

