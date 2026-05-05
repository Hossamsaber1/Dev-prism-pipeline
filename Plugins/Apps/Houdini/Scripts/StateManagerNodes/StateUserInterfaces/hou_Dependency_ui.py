# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hou_Dependency.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_wg_Dependency(object):
    def setupUi(self, wg_Dependency):
        if not wg_Dependency.objectName():
            wg_Dependency.setObjectName(u"wg_Dependency")
        wg_Dependency.resize(340, 643)
        self.verticalLayout = QVBoxLayout(wg_Dependency)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(wg_Dependency)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, 18, 0)
        self.l_name = QLabel(self.widget_4)
        self.l_name.setObjectName(u"l_name")

        self.horizontalLayout_2.addWidget(self.l_name)

        self.e_name = QLineEdit(self.widget_4)
        self.e_name.setObjectName(u"e_name")

        self.horizontalLayout_2.addWidget(self.e_name)

        self.l_class = QLabel(self.widget_4)
        self.l_class.setObjectName(u"l_class")
        font = QFont()
        font.setBold(True)
        self.l_class.setFont(font)

        self.horizontalLayout_2.addWidget(self.l_class)


        self.verticalLayout.addWidget(self.widget_4)

        self.f_manager = QWidget(wg_Dependency)
        self.f_manager.setObjectName(u"f_manager")
        self.horizontalLayout_8 = QHBoxLayout(self.f_manager)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.l_manager = QLabel(self.f_manager)
        self.l_manager.setObjectName(u"l_manager")

        self.horizontalLayout_8.addWidget(self.l_manager)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_19)

        self.cb_manager = QComboBox(self.f_manager)
        self.cb_manager.setObjectName(u"cb_manager")
        self.cb_manager.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_8.addWidget(self.cb_manager)


        self.verticalLayout.addWidget(self.f_manager)

        self.gb_dlDependency = QGroupBox(wg_Dependency)
        self.gb_dlDependency.setObjectName(u"gb_dlDependency")
        self.verticalLayout_2 = QVBoxLayout(self.gb_dlDependency)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 18, -1, -1)
        self.w_clear = QWidget(self.gb_dlDependency)
        self.w_clear.setObjectName(u"w_clear")
        self.horizontalLayout_4 = QHBoxLayout(self.w_clear)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(9, 0, 9, 0)
        self.l_clear = QLabel(self.w_clear)
        self.l_clear.setObjectName(u"l_clear")

        self.horizontalLayout_4.addWidget(self.l_clear)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.chb_clear = QCheckBox(self.w_clear)
        self.chb_clear.setObjectName(u"chb_clear")
        self.chb_clear.setChecked(True)

        self.horizontalLayout_4.addWidget(self.chb_clear)


        self.verticalLayout_2.addWidget(self.w_clear)

        self.widget_5 = QWidget(self.gb_dlDependency)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(9, 0, 9, 0)
        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.cb_depType = QComboBox(self.widget_5)
        self.cb_depType.setObjectName(u"cb_depType")
        self.cb_depType.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_3.addWidget(self.cb_depType)


        self.verticalLayout_2.addWidget(self.widget_5)

        self.w_offset = QWidget(self.gb_dlDependency)
        self.w_offset.setObjectName(u"w_offset")
        self.horizontalLayout = QHBoxLayout(self.w_offset)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.label = QLabel(self.w_offset)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.label)

        self.sp_offset = QSpinBox(self.w_offset)
        self.sp_offset.setObjectName(u"sp_offset")
        self.sp_offset.setMinimum(-99999)
        self.sp_offset.setMaximum(99999)

        self.horizontalLayout.addWidget(self.sp_offset)


        self.verticalLayout_2.addWidget(self.w_offset)

        self.widget = QWidget(self.gb_dlDependency)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.tw_caches = QTreeWidget(self.widget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tw_caches.setHeaderItem(__qtreewidgetitem)
        self.tw_caches.setObjectName(u"tw_caches")
        self.tw_caches.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_caches.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_caches.setItemsExpandable(True)
        self.tw_caches.setExpandsOnDoubleClick(True)
        self.tw_caches.header().setVisible(True)

        self.verticalLayout_3.addWidget(self.tw_caches)


        self.verticalLayout_2.addWidget(self.widget)


        self.verticalLayout.addWidget(self.gb_dlDependency)


        self.retranslateUi(wg_Dependency)

        QMetaObject.connectSlotsByName(wg_Dependency)
    # setupUi

    def retranslateUi(self, wg_Dependency):
        wg_Dependency.setWindowTitle(QCoreApplication.translate("wg_Dependency", u"Dependency", None))
        self.l_name.setText(QCoreApplication.translate("wg_Dependency", u"Name:", None))
        self.l_class.setText(QCoreApplication.translate("wg_Dependency", u"Dependency", None))
        self.l_manager.setText(QCoreApplication.translate("wg_Dependency", u"Manager:", None))
        self.gb_dlDependency.setTitle(QCoreApplication.translate("wg_Dependency", u" Dependency", None))
        self.l_clear.setText(QCoreApplication.translate("wg_Dependency", u"Clear all existing dependencies:", None))
        self.chb_clear.setText("")
        self.label_3.setText(QCoreApplication.translate("wg_Dependency", u"Release when:", None))
        self.label.setText(QCoreApplication.translate("wg_Dependency", u"Start when next n frames exist", None))
        self.sp_offset.setSuffix("")
    # retranslateUi

