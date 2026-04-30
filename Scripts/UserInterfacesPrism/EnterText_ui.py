# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EnterText.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_EnterText(object):
    def setupUi(self, dlg_EnterText):
        if not dlg_EnterText.objectName():
            dlg_EnterText.setObjectName(u"dlg_EnterText")
        dlg_EnterText.resize(367, 228)
        self.verticalLayout = QVBoxLayout(dlg_EnterText)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.l_info = QLabel(dlg_EnterText)
        self.l_info.setObjectName(u"l_info")

        self.verticalLayout.addWidget(self.l_info)

        self.te_text = QTextEdit(dlg_EnterText)
        self.te_text.setObjectName(u"te_text")

        self.verticalLayout.addWidget(self.te_text)

        self.buttonBox = QDialogButtonBox(dlg_EnterText)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dlg_EnterText)
        self.buttonBox.accepted.connect(dlg_EnterText.accept)
        self.buttonBox.rejected.connect(dlg_EnterText.reject)

        QMetaObject.connectSlotsByName(dlg_EnterText)
    # setupUi

    def retranslateUi(self, dlg_EnterText):
        dlg_EnterText.setWindowTitle(QCoreApplication.translate("dlg_EnterText", u"Enter Text", None))
        self.l_info.setText(QCoreApplication.translate("dlg_EnterText", u"Enter text:", None))
    # retranslateUi

