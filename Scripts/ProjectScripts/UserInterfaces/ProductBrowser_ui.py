# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProductBrowser.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_ProductBrowser(object):
    def setupUi(self, dlg_ProductBrowser):
        if not dlg_ProductBrowser.objectName():
            dlg_ProductBrowser.setObjectName(u"dlg_ProductBrowser")
        dlg_ProductBrowser.resize(1294, 696)
        self.lo_main = QVBoxLayout(dlg_ProductBrowser)
        self.lo_main.setObjectName(u"lo_main")
        self.splitter1 = QSplitter(dlg_ProductBrowser)
        self.splitter1.setObjectName(u"splitter1")
        self.splitter1.setOrientation(Qt.Horizontal)
        self.w_tasks = QWidget(self.splitter1)
        self.w_tasks.setObjectName(u"w_tasks")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_tasks.sizePolicy().hasHeightForWidth())
        self.w_tasks.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.w_tasks)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.l_identifier = QLabel(self.w_tasks)
        self.l_identifier.setObjectName(u"l_identifier")

        self.verticalLayout_3.addWidget(self.l_identifier)

        self.tw_identifier = QTreeWidget(self.w_tasks)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tw_identifier.setHeaderItem(__qtreewidgetitem)
        self.tw_identifier.setObjectName(u"tw_identifier")
        self.tw_identifier.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_identifier.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tw_identifier.setIndentation(10)
        self.tw_identifier.header().setVisible(False)

        self.verticalLayout_3.addWidget(self.tw_identifier)

        self.splitter1.addWidget(self.w_tasks)
        self.w_versions = QWidget(self.splitter1)
        self.w_versions.setObjectName(u"w_versions")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(30)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_versions.sizePolicy().hasHeightForWidth())
        self.w_versions.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.w_versions)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.w_version = QWidget(self.w_versions)
        self.w_version.setObjectName(u"w_version")
        self.horizontalLayout = QHBoxLayout(self.w_version)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.l_version = QLabel(self.w_version)
        self.l_version.setObjectName(u"l_version")

        self.horizontalLayout.addWidget(self.l_version)

        self.l_versionRight = QLabel(self.w_version)
        self.l_versionRight.setObjectName(u"l_versionRight")
        self.l_versionRight.setLayoutDirection(Qt.LeftToRight)
        self.l_versionRight.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.l_versionRight)


        self.verticalLayout_2.addWidget(self.w_version)

        self.tw_versions = QTableWidget(self.w_versions)
        self.tw_versions.setObjectName(u"tw_versions")
        self.tw_versions.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_versions.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_versions.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tw_versions.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_versions.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_versions.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_versions.setShowGrid(False)
        self.tw_versions.setSortingEnabled(True)
        self.tw_versions.horizontalHeader().setCascadingSectionResizes(False)
        self.tw_versions.horizontalHeader().setMinimumSectionSize(0)
        self.tw_versions.horizontalHeader().setHighlightSections(False)
        self.tw_versions.verticalHeader().setVisible(False)

        self.verticalLayout_2.addWidget(self.tw_versions)

        self.splitter1.addWidget(self.w_versions)

        self.lo_main.addWidget(self.splitter1)


        self.retranslateUi(dlg_ProductBrowser)

        QMetaObject.connectSlotsByName(dlg_ProductBrowser)
    # setupUi

    def retranslateUi(self, dlg_ProductBrowser):
        dlg_ProductBrowser.setWindowTitle(QCoreApplication.translate("dlg_ProductBrowser", u"Product Browser", None))
        self.l_identifier.setText(QCoreApplication.translate("dlg_ProductBrowser", u"Products:", None))
        self.l_version.setText(QCoreApplication.translate("dlg_ProductBrowser", u"Versions:", None))
        self.l_versionRight.setText("")
    # retranslateUi

