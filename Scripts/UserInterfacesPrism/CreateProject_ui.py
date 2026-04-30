# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CreateProject.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_dlg_createProject(object):
    def setupUi(self, dlg_createProject):
        if not dlg_createProject.objectName():
            dlg_createProject.setObjectName(u"dlg_createProject")
        dlg_createProject.resize(726, 418)
        self.horizontalLayout_11 = QHBoxLayout(dlg_createProject)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.scrollArea = QScrollArea(dlg_createProject)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 300))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 689, 400))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 9, 9, 9)
        self.sw_project = QStackedWidget(self.scrollAreaWidgetContents)
        self.sw_project.setObjectName(u"sw_project")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.w_start = QWidget(self.page)
        self.w_start.setObjectName(u"w_start")
        self.gridLayout = QGridLayout(self.w_start)
        self.gridLayout.setObjectName(u"gridLayout")
        self.l_preset = QLabel(self.w_start)
        self.l_preset.setObjectName(u"l_preset")

        self.gridLayout.addWidget(self.l_preset, 3, 0, 1, 1)

        self.l_name = QLabel(self.w_start)
        self.l_name.setObjectName(u"l_name")

        self.gridLayout.addWidget(self.l_name, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 5, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 1, 1, 1)

        self.e_path = QLineEdit(self.w_start)
        self.e_path.setObjectName(u"e_path")

        self.gridLayout.addWidget(self.e_path, 1, 1, 1, 1)

        self.b_browse = QToolButton(self.w_start)
        self.b_browse.setObjectName(u"b_browse")

        self.gridLayout.addWidget(self.b_browse, 1, 2, 1, 1)

        self.l_path = QLabel(self.w_start)
        self.l_path.setObjectName(u"l_path")

        self.gridLayout.addWidget(self.l_path, 1, 0, 1, 1)

        self.widget_4 = QWidget(self.w_start)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.l_preview = QLabel(self.widget_4)
        self.l_preview.setObjectName(u"l_preview")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_preview.sizePolicy().hasHeightForWidth())
        self.l_preview.setSizePolicy(sizePolicy)
        self.l_preview.setMinimumSize(QSize(300, 169))
        self.l_preview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.l_preview.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.l_preview)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.gridLayout.addWidget(self.widget_4, 6, 1, 1, 1)

        self.label_2 = QLabel(self.w_start)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)

        self.e_name = QLineEdit(self.w_start)
        self.e_name.setObjectName(u"e_name")

        self.gridLayout.addWidget(self.e_name, 0, 1, 1, 1)

        self.w_preset = QWidget(self.w_start)
        self.w_preset.setObjectName(u"w_preset")
        self.horizontalLayout_6 = QHBoxLayout(self.w_preset)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_4)

        self.cb_preset = QComboBox(self.w_preset)
        self.cb_preset.setObjectName(u"cb_preset")

        self.horizontalLayout_6.addWidget(self.cb_preset)

        self.b_reload = QToolButton(self.w_preset)
        self.b_reload.setObjectName(u"b_reload")

        self.horizontalLayout_6.addWidget(self.b_reload)

        self.b_addPreset = QToolButton(self.w_preset)
        self.b_addPreset.setObjectName(u"b_addPreset")

        self.horizontalLayout_6.addWidget(self.b_addPreset)

        self.b_managePresets = QToolButton(self.w_preset)
        self.b_managePresets.setObjectName(u"b_managePresets")

        self.horizontalLayout_6.addWidget(self.b_managePresets)


        self.gridLayout.addWidget(self.w_preset, 3, 1, 1, 1)

        self.l_placeholder = QLabel(self.w_start)
        self.l_placeholder.setObjectName(u"l_placeholder")

        self.gridLayout.addWidget(self.l_placeholder, 4, 1, 1, 1)


        self.verticalLayout.addWidget(self.w_start)

        self.sw_project.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_3 = QVBoxLayout(self.page_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_32 = QWidget(self.page_2)
        self.widget_32.setObjectName(u"widget_32")
        self.verticalLayout_6 = QVBoxLayout(self.widget_32)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tw_structure = QTreeWidget(self.widget_32)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tw_structure.setHeaderItem(__qtreewidgetitem)
        self.tw_structure.setObjectName(u"tw_structure")
        self.tw_structure.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_structure.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_structure.setIndentation(10)

        self.verticalLayout_6.addWidget(self.tw_structure)

        self.b_settings = QPushButton(self.widget_32)
        self.b_settings.setObjectName(u"b_settings")

        self.verticalLayout_6.addWidget(self.b_settings)


        self.verticalLayout_3.addWidget(self.widget_32)

        self.sw_project.addWidget(self.page_2)

        self.verticalLayout_2.addWidget(self.sw_project)

        self.w_footer = QWidget(self.scrollAreaWidgetContents)
        self.w_footer.setObjectName(u"w_footer")
        self.horizontalLayout_3 = QHBoxLayout(self.w_footer)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.b_back = QPushButton(self.w_footer)
        self.b_back.setObjectName(u"b_back")

        self.horizontalLayout_3.addWidget(self.b_back)

        self.b_next = QPushButton(self.w_footer)
        self.b_next.setObjectName(u"b_next")

        self.horizontalLayout_3.addWidget(self.b_next)

        self.b_create = QPushButton(self.w_footer)
        self.b_create.setObjectName(u"b_create")

        self.horizontalLayout_3.addWidget(self.b_create)

        self.sp_footer = QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.sp_footer)


        self.verticalLayout_2.addWidget(self.w_footer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_11.addWidget(self.scrollArea)

        QWidget.setTabOrder(self.scrollArea, self.e_name)
        QWidget.setTabOrder(self.e_name, self.e_path)
        QWidget.setTabOrder(self.e_path, self.b_browse)

        self.retranslateUi(dlg_createProject)

        self.sw_project.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(dlg_createProject)
    # setupUi

    def retranslateUi(self, dlg_createProject):
        dlg_createProject.setWindowTitle(QCoreApplication.translate("dlg_createProject", u"Create Project", None))
        self.l_preset.setText(QCoreApplication.translate("dlg_createProject", u"Preset:", None))
        self.l_name.setText(QCoreApplication.translate("dlg_createProject", u"Project Name:", None))
#if QT_CONFIG(tooltip)
        self.b_browse.setToolTip(QCoreApplication.translate("dlg_createProject", u"browse", None))
#endif // QT_CONFIG(tooltip)
        self.b_browse.setText(QCoreApplication.translate("dlg_createProject", u"...", None))
        self.l_path.setText(QCoreApplication.translate("dlg_createProject", u"Project Path:", None))
        self.l_preview.setText(QCoreApplication.translate("dlg_createProject", u"Preview image", None))
        self.label_2.setText(QCoreApplication.translate("dlg_createProject", u"Image (optional):", None))
        self.b_reload.setText(QCoreApplication.translate("dlg_createProject", u"...", None))
        self.b_addPreset.setText(QCoreApplication.translate("dlg_createProject", u"...", None))
        self.b_managePresets.setText(QCoreApplication.translate("dlg_createProject", u"...", None))
        self.l_placeholder.setText("")
        self.b_settings.setText(QCoreApplication.translate("dlg_createProject", u"Customize Project Settings...", None))
        self.b_back.setText(QCoreApplication.translate("dlg_createProject", u"Back", None))
        self.b_next.setText(QCoreApplication.translate("dlg_createProject", u"Edit Settings", None))
        self.b_create.setText(QCoreApplication.translate("dlg_createProject", u"Create", None))
    # retranslateUi

