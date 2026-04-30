# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PrismInstaller.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_installer(object):
    def setupUi(self, dlg_installer):
        if not dlg_installer.objectName():
            dlg_installer.setObjectName(u"dlg_installer")
        dlg_installer.resize(680, 720)
        self.verticalLayout = QVBoxLayout(dlg_installer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 15, -1, -1)
        self.label = QLabel(dlg_installer)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tw_components = QTreeWidget(dlg_installer)
        self.tw_components.setObjectName(u"tw_components")
        self.tw_components.setMinimumSize(QSize(0, 100))
        self.tw_components.header().setVisible(False)
        self.tw_components.header().setDefaultSectionSize(200)

        self.verticalLayout.addWidget(self.tw_components)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(dlg_installer)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dlg_installer)
        self.buttonBox.accepted.connect(dlg_installer.accept)
        self.buttonBox.rejected.connect(dlg_installer.reject)

        QMetaObject.connectSlotsByName(dlg_installer)
    # setupUi

    def retranslateUi(self, dlg_installer):
        dlg_installer.setWindowTitle(QCoreApplication.translate("dlg_installer", u"Setup Prism integrations", None))
        self.label.setText(QCoreApplication.translate("dlg_installer", u"Please select the integrations you want to install:", None))
        ___qtreewidgetitem = self.tw_components.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("dlg_installer", u"paths", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("dlg_installer", u"programm", None));
    # retranslateUi

