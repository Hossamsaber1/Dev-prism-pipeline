# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hou_InstallHDA.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_wg_InstallHDA(object):
    def setupUi(self, wg_InstallHDA):
        if not wg_InstallHDA.objectName():
            wg_InstallHDA.setObjectName(u"wg_InstallHDA")
        wg_InstallHDA.resize(340, 241)
        self.verticalLayout = QVBoxLayout(wg_InstallHDA)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_4 = QWidget(wg_InstallHDA)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, 18, 0)
        self.l_name = QLabel(self.widget_4)
        self.l_name.setObjectName(u"l_name")

        self.horizontalLayout_2.addWidget(self.l_name)

        self.e_name = QLineEdit(self.widget_4)
        self.e_name.setObjectName(u"e_name")
        self.e_name.setMinimumSize(QSize(0, 0))
        self.e_name.setMaximumSize(QSize(9999, 16777215))

        self.horizontalLayout_2.addWidget(self.e_name)

        self.l_class = QLabel(self.widget_4)
        self.l_class.setObjectName(u"l_class")
        font = QFont()
        font.setBold(True)
        self.l_class.setFont(font)

        self.horizontalLayout_2.addWidget(self.l_class)


        self.verticalLayout.addWidget(self.widget_4)

        self.gb_import = QGroupBox(wg_InstallHDA)
        self.gb_import.setObjectName(u"gb_import")
        self.verticalLayout_2 = QVBoxLayout(self.gb_import)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.gb_import)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.w_currentVersion = QWidget(self.groupBox)
        self.w_currentVersion.setObjectName(u"w_currentVersion")
        self.horizontalLayout_5 = QHBoxLayout(self.w_currentVersion)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.label_3 = QLabel(self.w_currentVersion)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.l_curVersion = QLabel(self.w_currentVersion)
        self.l_curVersion.setObjectName(u"l_curVersion")

        self.horizontalLayout_5.addWidget(self.l_curVersion)


        self.verticalLayout_3.addWidget(self.w_currentVersion)

        self.w_latestVersion = QWidget(self.groupBox)
        self.w_latestVersion.setObjectName(u"w_latestVersion")
        self.horizontalLayout_6 = QHBoxLayout(self.w_latestVersion)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.label_6 = QLabel(self.w_latestVersion)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.l_latestVersion = QLabel(self.w_latestVersion)
        self.l_latestVersion.setObjectName(u"l_latestVersion")

        self.horizontalLayout_6.addWidget(self.l_latestVersion)


        self.verticalLayout_3.addWidget(self.w_latestVersion)

        self.w_autoUpdate = QWidget(self.groupBox)
        self.w_autoUpdate.setObjectName(u"w_autoUpdate")
        self.horizontalLayout_14 = QHBoxLayout(self.w_autoUpdate)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(9, 0, 9, 0)
        self.l_autoUpdate = QLabel(self.w_autoUpdate)
        self.l_autoUpdate.setObjectName(u"l_autoUpdate")

        self.horizontalLayout_14.addWidget(self.l_autoUpdate)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_10)

        self.chb_autoUpdate = QCheckBox(self.w_autoUpdate)
        self.chb_autoUpdate.setObjectName(u"chb_autoUpdate")
        self.chb_autoUpdate.setChecked(False)

        self.horizontalLayout_14.addWidget(self.chb_autoUpdate)


        self.verticalLayout_3.addWidget(self.w_autoUpdate)

        self.w_importLatest = QWidget(self.groupBox)
        self.w_importLatest.setObjectName(u"w_importLatest")
        self.horizontalLayout_7 = QHBoxLayout(self.w_importLatest)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.b_browse = QPushButton(self.w_importLatest)
        self.b_browse.setObjectName(u"b_browse")
        self.b_browse.setFocusPolicy(Qt.NoFocus)
        self.b_browse.setContextMenuPolicy(Qt.CustomContextMenu)

        self.horizontalLayout_7.addWidget(self.b_browse)

        self.b_importLatest = QPushButton(self.w_importLatest)
        self.b_importLatest.setObjectName(u"b_importLatest")
        self.b_importLatest.setMinimumSize(QSize(0, 0))
        self.b_importLatest.setMaximumSize(QSize(99999, 16777215))
        self.b_importLatest.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_7.addWidget(self.b_importLatest)


        self.verticalLayout_3.addWidget(self.w_importLatest)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.widget_3 = QWidget(self.gb_import)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(40, 0))
        self.label.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_4.addWidget(self.label)

        self.l_status = QLabel(self.widget_3)
        self.l_status.setObjectName(u"l_status")
        self.l_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.l_status)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.widget_2 = QWidget(self.gb_import)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.b_import = QPushButton(self.widget_2)
        self.b_import.setObjectName(u"b_import")
        self.b_import.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.b_import)

        self.b_createNode = QPushButton(self.widget_2)
        self.b_createNode.setObjectName(u"b_createNode")
        self.b_createNode.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.b_createNode)


        self.verticalLayout_2.addWidget(self.widget_2)


        self.verticalLayout.addWidget(self.gb_import)


        self.retranslateUi(wg_InstallHDA)

        QMetaObject.connectSlotsByName(wg_InstallHDA)
    # setupUi

    def retranslateUi(self, wg_InstallHDA):
        wg_InstallHDA.setWindowTitle(QCoreApplication.translate("wg_InstallHDA", u"ImportFile", None))
        self.l_name.setText(QCoreApplication.translate("wg_InstallHDA", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_InstallHDA", u"Install HDA", None))
        self.gb_import.setTitle(QCoreApplication.translate("wg_InstallHDA", u"Import", None))
        self.groupBox.setTitle(QCoreApplication.translate("wg_InstallHDA", u"Version", None))
        self.label_3.setText(QCoreApplication.translate("wg_InstallHDA", u"Current Version:", None))
        self.l_curVersion.setText(QCoreApplication.translate("wg_InstallHDA", u"-", None))
        self.label_6.setText(QCoreApplication.translate("wg_InstallHDA", u"Latest Version:", None))
        self.l_latestVersion.setText(QCoreApplication.translate("wg_InstallHDA", u"-", None))
        self.l_autoUpdate.setText(QCoreApplication.translate("wg_InstallHDA", u"Auto load latest version:", None))
        self.chb_autoUpdate.setText("")
        self.b_browse.setText(QCoreApplication.translate("wg_InstallHDA", u"Browse", None))
        self.b_importLatest.setText(QCoreApplication.translate("wg_InstallHDA", u"Install latest Version", None))
        self.label.setText(QCoreApplication.translate("wg_InstallHDA", u"Status:", None))
        self.l_status.setText(QCoreApplication.translate("wg_InstallHDA", u"Not found in scene", None))
        self.b_import.setText(QCoreApplication.translate("wg_InstallHDA", u"Re-Install", None))
        self.b_createNode.setText(QCoreApplication.translate("wg_InstallHDA", u"Create Node", None))
    # retranslateUi

