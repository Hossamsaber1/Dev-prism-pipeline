# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MediaBrowser.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_w_mediaBrowser(object):
    def setupUi(self, w_mediaBrowser):
        if not w_mediaBrowser.objectName():
            w_mediaBrowser.setObjectName(u"w_mediaBrowser")
        w_mediaBrowser.resize(714, 393)
        self.horizontalLayout = QHBoxLayout(w_mediaBrowser)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.splitter1 = QSplitter(w_mediaBrowser)
        self.splitter1.setObjectName(u"splitter1")
        self.splitter1.setOrientation(Qt.Horizontal)
        self.w_identifier = QWidget(self.splitter1)
        self.w_identifier.setObjectName(u"w_identifier")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_identifier.sizePolicy().hasHeightForWidth())
        self.w_identifier.setSizePolicy(sizePolicy)
        self.verticalLayout_8 = QVBoxLayout(self.w_identifier)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.l_identifier = QLabel(self.w_identifier)
        self.l_identifier.setObjectName(u"l_identifier")

        self.verticalLayout_8.addWidget(self.l_identifier)

        self.tw_identifier = QTreeWidget(self.w_identifier)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tw_identifier.setHeaderItem(__qtreewidgetitem)
        self.tw_identifier.setObjectName(u"tw_identifier")
        self.tw_identifier.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_identifier.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tw_identifier.setIndentation(10)
        self.tw_identifier.header().setVisible(False)

        self.verticalLayout_8.addWidget(self.tw_identifier)

        self.w_autoUpdate = QWidget(self.w_identifier)
        self.w_autoUpdate.setObjectName(u"w_autoUpdate")
        self.horizontalLayout_10 = QHBoxLayout(self.w_autoUpdate)
        self.horizontalLayout_10.setSpacing(15)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 5, 0, 0)
        self.chb_autoUpdate = QCheckBox(self.w_autoUpdate)
        self.chb_autoUpdate.setObjectName(u"chb_autoUpdate")
        self.chb_autoUpdate.setChecked(True)

        self.horizontalLayout_10.addWidget(self.chb_autoUpdate)

        self.b_refresh = QPushButton(self.w_autoUpdate)
        self.b_refresh.setObjectName(u"b_refresh")
        self.b_refresh.setEnabled(False)
        self.b_refresh.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_10.addWidget(self.b_refresh)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_3)


        self.verticalLayout_8.addWidget(self.w_autoUpdate)

        self.splitter1.addWidget(self.w_identifier)
        self.w_version = QWidget(self.splitter1)
        self.w_version.setObjectName(u"w_version")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(9)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_version.sizePolicy().hasHeightForWidth())
        self.w_version.setSizePolicy(sizePolicy1)
        self.verticalLayout_11 = QVBoxLayout(self.w_version)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.l_version = QLabel(self.w_version)
        self.l_version.setObjectName(u"l_version")

        self.verticalLayout_11.addWidget(self.l_version)

        self.lw_version = QListWidget(self.w_version)
        self.lw_version.setObjectName(u"lw_version")
        self.lw_version.setMaximumSize(QSize(16777215, 9999))
        self.lw_version.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lw_version.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_11.addWidget(self.lw_version)

        self.splitter1.addWidget(self.w_version)

        self.horizontalLayout.addWidget(self.splitter1)


        self.retranslateUi(w_mediaBrowser)

        QMetaObject.connectSlotsByName(w_mediaBrowser)
    # setupUi

    def retranslateUi(self, w_mediaBrowser):
        w_mediaBrowser.setWindowTitle(QCoreApplication.translate("w_mediaBrowser", u"Media Browser", None))
        self.l_identifier.setText(QCoreApplication.translate("w_mediaBrowser", u"Identifiers:", None))
        self.chb_autoUpdate.setText(QCoreApplication.translate("w_mediaBrowser", u"Auto update", None))
        self.b_refresh.setText(QCoreApplication.translate("w_mediaBrowser", u"Refresh Tasks", None))
        self.l_version.setText(QCoreApplication.translate("w_mediaBrowser", u"Versions:", None))
    # retranslateUi

