# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hou_ImportFile.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_wg_ImportFile(object):
    def setupUi(self, wg_ImportFile):
        if not wg_ImportFile.objectName():
            wg_ImportFile.setObjectName(u"wg_ImportFile")
        wg_ImportFile.resize(340, 372)
        self.verticalLayout = QVBoxLayout(wg_ImportFile)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_4 = QWidget(wg_ImportFile)
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

        self.gb_import = QGroupBox(wg_ImportFile)
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

        self.groupBox_2 = QGroupBox(self.gb_import)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_3 = QWidget(self.groupBox_2)
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

        self.b_goTo = QPushButton(self.widget_3)
        self.b_goTo.setObjectName(u"b_goTo")
        self.b_goTo.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_4.addWidget(self.b_goTo)


        self.verticalLayout_4.addWidget(self.widget_3)

        self.widget_2 = QWidget(self.groupBox_2)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.b_import = QPushButton(self.widget_2)
        self.b_import.setObjectName(u"b_import")
        self.b_import.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.b_import)

        self.b_objMerge = QPushButton(self.widget_2)
        self.b_objMerge.setObjectName(u"b_objMerge")
        self.b_objMerge.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.b_objMerge)


        self.verticalLayout_4.addWidget(self.widget_2)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.gb_options = QGroupBox(self.gb_import)
        self.gb_options.setObjectName(u"gb_options")
        self.verticalLayout_6 = QVBoxLayout(self.gb_options)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.f_updateOnly = QWidget(self.gb_options)
        self.f_updateOnly.setObjectName(u"f_updateOnly")
        self.horizontalLayout_16 = QHBoxLayout(self.f_updateOnly)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(9, 0, 9, 0)
        self.l_updateOnly = QLabel(self.f_updateOnly)
        self.l_updateOnly.setObjectName(u"l_updateOnly")

        self.horizontalLayout_16.addWidget(self.l_updateOnly)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_12)

        self.chb_updateOnly = QCheckBox(self.f_updateOnly)
        self.chb_updateOnly.setObjectName(u"chb_updateOnly")
        self.chb_updateOnly.setChecked(True)

        self.horizontalLayout_16.addWidget(self.chb_updateOnly)


        self.verticalLayout_6.addWidget(self.f_updateOnly)

        self.f_nameSpaces = QWidget(self.gb_options)
        self.f_nameSpaces.setObjectName(u"f_nameSpaces")
        self.horizontalLayout_12 = QHBoxLayout(self.f_nameSpaces)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(9, 0, 9, 0)
        self.l_keepRefEdits_2 = QLabel(self.f_nameSpaces)
        self.l_keepRefEdits_2.setObjectName(u"l_keepRefEdits_2")

        self.horizontalLayout_12.addWidget(self.l_keepRefEdits_2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_7)

        self.chb_autoNameSpaces = QCheckBox(self.f_nameSpaces)
        self.chb_autoNameSpaces.setObjectName(u"chb_autoNameSpaces")
        self.chb_autoNameSpaces.setChecked(False)

        self.horizontalLayout_12.addWidget(self.chb_autoNameSpaces)

        self.horizontalSpacer_3 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_3)

        self.b_nameSpaces = QPushButton(self.f_nameSpaces)
        self.b_nameSpaces.setObjectName(u"b_nameSpaces")
        self.b_nameSpaces.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_12.addWidget(self.b_nameSpaces)


        self.verticalLayout_6.addWidget(self.f_nameSpaces)


        self.verticalLayout_2.addWidget(self.gb_options)


        self.verticalLayout.addWidget(self.gb_import)


        self.retranslateUi(wg_ImportFile)

        QMetaObject.connectSlotsByName(wg_ImportFile)
    # setupUi

    def retranslateUi(self, wg_ImportFile):
        wg_ImportFile.setWindowTitle(QCoreApplication.translate("wg_ImportFile", u"ImportFile", None))
        self.l_name.setText(QCoreApplication.translate("wg_ImportFile", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_ImportFile", u"ImportFile", None))
        self.gb_import.setTitle(QCoreApplication.translate("wg_ImportFile", u"Import", None))
        self.groupBox.setTitle(QCoreApplication.translate("wg_ImportFile", u"Version", None))
        self.label_3.setText(QCoreApplication.translate("wg_ImportFile", u"Current Version:", None))
        self.l_curVersion.setText(QCoreApplication.translate("wg_ImportFile", u"-", None))
        self.label_6.setText(QCoreApplication.translate("wg_ImportFile", u"Latest Version:", None))
        self.l_latestVersion.setText(QCoreApplication.translate("wg_ImportFile", u"-", None))
        self.l_autoUpdate.setText(QCoreApplication.translate("wg_ImportFile", u"Auto load latest version:", None))
        self.chb_autoUpdate.setText("")
        self.b_browse.setText(QCoreApplication.translate("wg_ImportFile", u"Browse", None))
        self.b_importLatest.setText(QCoreApplication.translate("wg_ImportFile", u"Import latest Version", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("wg_ImportFile", u"Scene", None))
        self.label.setText(QCoreApplication.translate("wg_ImportFile", u"Status:", None))
        self.l_status.setText(QCoreApplication.translate("wg_ImportFile", u"Not found in scene", None))
        self.b_goTo.setText(QCoreApplication.translate("wg_ImportFile", u"Go to Node", None))
        self.b_import.setText(QCoreApplication.translate("wg_ImportFile", u"Re-Import", None))
        self.b_objMerge.setText(QCoreApplication.translate("wg_ImportFile", u"Create Obj Merge", None))
        self.gb_options.setTitle(QCoreApplication.translate("wg_ImportFile", u"Options", None))
        self.l_updateOnly.setText(QCoreApplication.translate("wg_ImportFile", u"Update path only:", None))
        self.chb_updateOnly.setText("")
        self.l_keepRefEdits_2.setText(QCoreApplication.translate("wg_ImportFile", u"Maya Namespaces:", None))
        self.chb_autoNameSpaces.setText(QCoreApplication.translate("wg_ImportFile", u"Auto", None))
        self.b_nameSpaces.setText(QCoreApplication.translate("wg_ImportFile", u"Remove", None))
    # retranslateUi

