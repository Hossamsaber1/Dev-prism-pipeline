# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ItemList.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_ItemList(object):
    def setupUi(self, dlg_ItemList):
        if not dlg_ItemList.objectName():
            dlg_ItemList.setObjectName(u"dlg_ItemList")
        dlg_ItemList.resize(292, 393)
        self.verticalLayout = QVBoxLayout(dlg_ItemList)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tw_steps = QTableWidget(dlg_ItemList)
        self.tw_steps.setObjectName(u"tw_steps")
        self.tw_steps.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_steps.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_steps.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_steps.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_steps.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_steps.horizontalHeader().setHighlightSections(False)
        self.tw_steps.horizontalHeader().setProperty("showSortIndicator", True)
        self.tw_steps.horizontalHeader().setStretchLastSection(True)
        self.tw_steps.verticalHeader().setVisible(False)
        self.tw_steps.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.tw_steps)

        self.chb_category = QCheckBox(dlg_ItemList)
        self.chb_category.setObjectName(u"chb_category")
        self.chb_category.setChecked(True)

        self.verticalLayout.addWidget(self.chb_category)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(dlg_ItemList)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dlg_ItemList)

        QMetaObject.connectSlotsByName(dlg_ItemList)
    # setupUi

    def retranslateUi(self, dlg_ItemList):
        dlg_ItemList.setWindowTitle(QCoreApplication.translate("dlg_ItemList", u"Select Departments", None))
        self.chb_category.setText(QCoreApplication.translate("dlg_ItemList", u"Create default tasks", None))
    # retranslateUi

