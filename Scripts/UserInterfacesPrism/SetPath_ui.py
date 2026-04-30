# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetPath.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_SetPath(object):
    def setupUi(self, dlg_SetPath):
        if not dlg_SetPath.objectName():
            dlg_SetPath.setObjectName(u"dlg_SetPath")
        dlg_SetPath.resize(676, 110)
        self.verticalLayout = QVBoxLayout(dlg_SetPath)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.l_description = QLabel(dlg_SetPath)
        self.l_description.setObjectName(u"l_description")

        self.verticalLayout.addWidget(self.l_description)

        self.w_path = QWidget(dlg_SetPath)
        self.w_path.setObjectName(u"w_path")
        self.gridLayout = QGridLayout(self.w_path)
        self.gridLayout.setObjectName(u"gridLayout")
        self.e_path = QLineEdit(self.w_path)
        self.e_path.setObjectName(u"e_path")

        self.gridLayout.addWidget(self.e_path, 0, 1, 1, 1)

        self.l_path = QLabel(self.w_path)
        self.l_path.setObjectName(u"l_path")

        self.gridLayout.addWidget(self.l_path, 0, 0, 1, 1)

        self.b_browse = QPushButton(self.w_path)
        self.b_browse.setObjectName(u"b_browse")
        self.b_browse.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.b_browse, 0, 2, 1, 1)


        self.verticalLayout.addWidget(self.w_path)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(dlg_SetPath)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dlg_SetPath)
        self.buttonBox.accepted.connect(dlg_SetPath.accept)
        self.buttonBox.rejected.connect(dlg_SetPath.reject)

        QMetaObject.connectSlotsByName(dlg_SetPath)
    # setupUi

    def retranslateUi(self, dlg_SetPath):
        dlg_SetPath.setWindowTitle(QCoreApplication.translate("dlg_SetPath", u"Set local projectpath", None))
        self.l_description.setText(QCoreApplication.translate("dlg_SetPath", u"All your local scenefiles are saved in this folder.\n"
"This folder should be on your local hard drive and should not be synrchonized to any server.", None))
        self.l_path.setText(QCoreApplication.translate("dlg_SetPath", u"Local projectpath:", None))
        self.b_browse.setText(QCoreApplication.translate("dlg_SetPath", u"...", None))
    # retranslateUi

