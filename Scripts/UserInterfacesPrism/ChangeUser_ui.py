# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ChangeUser.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_ChangeUser(object):
    def setupUi(self, dlg_ChangeUser):
        if not dlg_ChangeUser.objectName():
            dlg_ChangeUser.setObjectName(u"dlg_ChangeUser")
        dlg_ChangeUser.resize(368, 73)
        self.verticalLayout = QVBoxLayout(dlg_ChangeUser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.w_username = QWidget(dlg_ChangeUser)
        self.w_username.setObjectName(u"w_username")
        self.horizontalLayout = QHBoxLayout(self.w_username)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.l_username = QLabel(self.w_username)
        self.l_username.setObjectName(u"l_username")

        self.horizontalLayout.addWidget(self.l_username)

        self.e_username = QLineEdit(self.w_username)
        self.e_username.setObjectName(u"e_username")

        self.horizontalLayout.addWidget(self.e_username)


        self.verticalLayout.addWidget(self.w_username)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(dlg_ChangeUser)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dlg_ChangeUser)
        self.buttonBox.accepted.connect(dlg_ChangeUser.accept)
        self.buttonBox.rejected.connect(dlg_ChangeUser.reject)

        QMetaObject.connectSlotsByName(dlg_ChangeUser)
    # setupUi

    def retranslateUi(self, dlg_ChangeUser):
        dlg_ChangeUser.setWindowTitle(QCoreApplication.translate("dlg_ChangeUser", u"Change User", None))
        self.l_username.setText(QCoreApplication.translate("dlg_ChangeUser", u"Local Username:", None))
    # retranslateUi

