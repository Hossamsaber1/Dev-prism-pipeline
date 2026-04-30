# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StateManager.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_mw_StateManager(object):
    def setupUi(self, mw_StateManager):
        if not mw_StateManager.objectName():
            mw_StateManager.setObjectName(u"mw_StateManager")
        mw_StateManager.resize(722, 831)
        mw_StateManager.setFocusPolicy(Qt.ClickFocus)
        self.actionProjectBrowser = QAction(mw_StateManager)
        self.actionProjectBrowser.setObjectName(u"actionProjectBrowser")
        self.actionPrismSettings = QAction(mw_StateManager)
        self.actionPrismSettings.setObjectName(u"actionPrismSettings")
        self.actionCopyStates = QAction(mw_StateManager)
        self.actionCopyStates.setObjectName(u"actionCopyStates")
        self.actionPasteStates = QAction(mw_StateManager)
        self.actionPasteStates.setObjectName(u"actionPasteStates")
        self.actionRemoveStates = QAction(mw_StateManager)
        self.actionRemoveStates.setObjectName(u"actionRemoveStates")
        self.centralwidget = QWidget(mw_StateManager)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 720, 808))
        self.horizontalLayout_2 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.splitter = QSplitter(self.scrollAreaWidgetContents)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.widget = QWidget(self.splitter)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 10, 0, 5)
        self.splitter_2 = QSplitter(self.widget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.gb_import = QGroupBox(self.splitter_2)
        self.gb_import.setObjectName(u"gb_import")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(30)
        sizePolicy1.setHeightForWidth(self.gb_import.sizePolicy().hasHeightForWidth())
        self.gb_import.setSizePolicy(sizePolicy1)
        self.lo_import = QVBoxLayout(self.gb_import)
        self.lo_import.setObjectName(u"lo_import")
        self.lo_import.setContentsMargins(5, 14, 5, 5)
        self.w_CreateImports = QWidget(self.gb_import)
        self.w_CreateImports.setObjectName(u"w_CreateImports")
        self.horizontalLayout_3 = QHBoxLayout(self.w_CreateImports)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, 0, 5)
        self.b_createImport = QPushButton(self.w_CreateImports)
        self.b_createImport.setObjectName(u"b_createImport")
        self.b_createImport.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.b_createImport)

        self.b_shotCam = QPushButton(self.w_CreateImports)
        self.b_shotCam.setObjectName(u"b_shotCam")
        self.b_shotCam.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_3.addWidget(self.b_shotCam)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.b_showImportStates = QPushButton(self.w_CreateImports)
        self.b_showImportStates.setObjectName(u"b_showImportStates")
        self.b_showImportStates.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_3.addWidget(self.b_showImportStates)


        self.lo_import.addWidget(self.w_CreateImports)

        self.f_import = QFrame(self.gb_import)
        self.f_import.setObjectName(u"f_import")
        self.f_import.setFrameShape(QFrame.StyledPanel)
        self.f_import.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.f_import)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.tw_import = QTreeWidget(self.f_import)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tw_import.setHeaderItem(__qtreewidgetitem)
        self.tw_import.setObjectName(u"tw_import")
        self.tw_import.setFocusPolicy(Qt.ClickFocus)
        self.tw_import.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_import.setAcceptDrops(True)
        self.tw_import.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_import.setDragEnabled(True)
        self.tw_import.setDragDropMode(QAbstractItemView.InternalMove)
        self.tw_import.setDefaultDropAction(Qt.MoveAction)
        self.tw_import.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tw_import.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_import.setIndentation(20)
        self.tw_import.header().setVisible(False)

        self.verticalLayout_7.addWidget(self.tw_import)


        self.lo_import.addWidget(self.f_import)

        self.splitter_2.addWidget(self.gb_import)
        self.gb_export = QGroupBox(self.splitter_2)
        self.gb_export.setObjectName(u"gb_export")
        sizePolicy1.setHeightForWidth(self.gb_export.sizePolicy().hasHeightForWidth())
        self.gb_export.setSizePolicy(sizePolicy1)
        self.lo_export = QVBoxLayout(self.gb_export)
        self.lo_export.setObjectName(u"lo_export")
        self.lo_export.setContentsMargins(5, 14, 5, 5)
        self.w_CreateExports = QWidget(self.gb_export)
        self.w_CreateExports.setObjectName(u"w_CreateExports")
        self.horizontalLayout_4 = QHBoxLayout(self.w_CreateExports)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, -1, 0, 5)
        self.b_createExport = QPushButton(self.w_CreateExports)
        self.b_createExport.setObjectName(u"b_createExport")
        self.b_createExport.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_4.addWidget(self.b_createExport)

        self.b_createRender = QPushButton(self.w_CreateExports)
        self.b_createRender.setObjectName(u"b_createRender")
        self.b_createRender.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_4.addWidget(self.b_createRender)

        self.b_createPlayblast = QPushButton(self.w_CreateExports)
        self.b_createPlayblast.setObjectName(u"b_createPlayblast")
        self.b_createPlayblast.setFocusPolicy(Qt.NoFocus)

        self.horizontalLayout_4.addWidget(self.b_createPlayblast)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.b_showExportStates = QPushButton(self.w_CreateExports)
        self.b_showExportStates.setObjectName(u"b_showExportStates")
        self.b_showExportStates.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_4.addWidget(self.b_showExportStates)


        self.lo_export.addWidget(self.w_CreateExports)

        self.f_export = QFrame(self.gb_export)
        self.f_export.setObjectName(u"f_export")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.f_export.sizePolicy().hasHeightForWidth())
        self.f_export.setSizePolicy(sizePolicy2)
        self.f_export.setFrameShape(QFrame.StyledPanel)
        self.f_export.setFrameShadow(QFrame.Raised)
        self.f_export.setLineWidth(1)
        self.f_export.setMidLineWidth(0)
        self.verticalLayout = QVBoxLayout(self.f_export)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tw_export = QTreeWidget(self.f_export)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.tw_export.setHeaderItem(__qtreewidgetitem1)
        self.tw_export.setObjectName(u"tw_export")
        self.tw_export.setFocusPolicy(Qt.ClickFocus)
        self.tw_export.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_export.setAcceptDrops(True)
        self.tw_export.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_export.setDragEnabled(True)
        self.tw_export.setDragDropMode(QAbstractItemView.InternalMove)
        self.tw_export.setDefaultDropAction(Qt.MoveAction)
        self.tw_export.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tw_export.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_export.setIndentation(20)
        self.tw_export.header().setVisible(False)

        self.verticalLayout.addWidget(self.tw_export)


        self.lo_export.addWidget(self.f_export)

        self.gb_publish = QGroupBox(self.gb_export)
        self.gb_publish.setObjectName(u"gb_publish")
        self.verticalLayout_6 = QVBoxLayout(self.gb_publish)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget_2 = QWidget(self.gb_publish)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.l_comment = QLabel(self.widget_2)
        self.l_comment.setObjectName(u"l_comment")

        self.horizontalLayout_5.addWidget(self.l_comment)

        self.e_comment = QLineEdit(self.widget_2)
        self.e_comment.setObjectName(u"e_comment")

        self.horizontalLayout_5.addWidget(self.e_comment)

        self.b_description = QToolButton(self.widget_2)
        self.b_description.setObjectName(u"b_description")
        self.b_description.setFocusPolicy(Qt.NoFocus)
        self.b_description.setContextMenuPolicy(Qt.CustomContextMenu)

        self.horizontalLayout_5.addWidget(self.b_description)

        self.b_preview = QToolButton(self.widget_2)
        self.b_preview.setObjectName(u"b_preview")
        self.b_preview.setFocusPolicy(Qt.NoFocus)
        self.b_preview.setContextMenuPolicy(Qt.CustomContextMenu)

        self.horizontalLayout_5.addWidget(self.b_preview)


        self.verticalLayout_6.addWidget(self.widget_2)

        self.b_publish = QPushButton(self.gb_publish)
        self.b_publish.setObjectName(u"b_publish")
        self.b_publish.setEnabled(False)
        self.b_publish.setFocusPolicy(Qt.NoFocus)
        self.b_publish.setAutoDefault(False)

        self.verticalLayout_6.addWidget(self.b_publish)


        self.lo_export.addWidget(self.gb_publish)

        self.splitter_2.addWidget(self.gb_export)

        self.verticalLayout_2.addWidget(self.splitter_2)

        self.splitter.addWidget(self.widget)
        self.sa_stateSettings = QScrollArea(self.splitter)
        self.sa_stateSettings.setObjectName(u"sa_stateSettings")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(30)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sa_stateSettings.sizePolicy().hasHeightForWidth())
        self.sa_stateSettings.setSizePolicy(sizePolicy3)
        self.sa_stateSettings.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 408, 788))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.scrollAreaWidgetContents_2)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_8 = QVBoxLayout(self.widget_3)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.w_stateUi = QWidget(self.widget_3)
        self.w_stateUi.setObjectName(u"w_stateUi")
        self.lo_stateUi = QVBoxLayout(self.w_stateUi)
        self.lo_stateUi.setObjectName(u"lo_stateUi")
        self.lo_stateUi.setContentsMargins(9, 9, 9, 9)

        self.verticalLayout_8.addWidget(self.w_stateUi)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer)


        self.verticalLayout_3.addWidget(self.widget_3)

        self.sa_stateSettings.setWidget(self.scrollAreaWidgetContents_2)
        self.splitter.addWidget(self.sa_stateSettings)

        self.horizontalLayout_2.addWidget(self.splitter)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.scrollArea)

        mw_StateManager.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mw_StateManager)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 722, 21))
        self.menuAbout = QMenu(self.menubar)
        self.menuAbout.setObjectName(u"menuAbout")
        self.menuRecentProjects = QMenu(self.menuAbout)
        self.menuRecentProjects.setObjectName(u"menuRecentProjects")
        mw_StateManager.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuAbout.menuAction())
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionCopyStates)
        self.menuAbout.addAction(self.actionPasteStates)
        self.menuAbout.addAction(self.actionRemoveStates)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.actionProjectBrowser)
        self.menuAbout.addAction(self.actionPrismSettings)
        self.menuAbout.addSeparator()
        self.menuAbout.addAction(self.menuRecentProjects.menuAction())

        self.retranslateUi(mw_StateManager)

        QMetaObject.connectSlotsByName(mw_StateManager)
    # setupUi

    def retranslateUi(self, mw_StateManager):
        mw_StateManager.setWindowTitle(QCoreApplication.translate("mw_StateManager", u"State Manager", None))
        self.actionProjectBrowser.setText(QCoreApplication.translate("mw_StateManager", u"Project Browser...", None))
        self.actionPrismSettings.setText(QCoreApplication.translate("mw_StateManager", u"Settings...", None))
        self.actionCopyStates.setText(QCoreApplication.translate("mw_StateManager", u"Copy all states", None))
        self.actionPasteStates.setText(QCoreApplication.translate("mw_StateManager", u"Paste all states", None))
        self.actionRemoveStates.setText(QCoreApplication.translate("mw_StateManager", u"Remove all states", None))
        self.gb_import.setTitle(QCoreApplication.translate("mw_StateManager", u"Import", None))
#if QT_CONFIG(tooltip)
        self.b_createImport.setToolTip(QCoreApplication.translate("mw_StateManager", u"Create an ImportFile state", None))
#endif // QT_CONFIG(tooltip)
        self.b_createImport.setText(QCoreApplication.translate("mw_StateManager", u"Import", None))
#if QT_CONFIG(tooltip)
        self.b_shotCam.setToolTip(QCoreApplication.translate("mw_StateManager", u"Import the latest Shot Camera", None))
#endif // QT_CONFIG(tooltip)
        self.b_shotCam.setText(QCoreApplication.translate("mw_StateManager", u"Import Camera", None))
#if QT_CONFIG(tooltip)
        self.b_showImportStates.setToolTip(QCoreApplication.translate("mw_StateManager", u"show available import state types", None))
#endif // QT_CONFIG(tooltip)
        self.b_showImportStates.setText(QCoreApplication.translate("mw_StateManager", u"\u25bc", None))
        self.gb_export.setTitle(QCoreApplication.translate("mw_StateManager", u"Export", None))
#if QT_CONFIG(tooltip)
        self.b_createExport.setToolTip(QCoreApplication.translate("mw_StateManager", u"Create an Export state", None))
#endif // QT_CONFIG(tooltip)
        self.b_createExport.setText(QCoreApplication.translate("mw_StateManager", u"Export", None))
#if QT_CONFIG(tooltip)
        self.b_createRender.setToolTip(QCoreApplication.translate("mw_StateManager", u"Create an ImageRender state", None))
#endif // QT_CONFIG(tooltip)
        self.b_createRender.setText(QCoreApplication.translate("mw_StateManager", u"Render", None))
#if QT_CONFIG(tooltip)
        self.b_createPlayblast.setToolTip(QCoreApplication.translate("mw_StateManager", u"Create a Playblast state", None))
#endif // QT_CONFIG(tooltip)
        self.b_createPlayblast.setText(QCoreApplication.translate("mw_StateManager", u"Playblast", None))
#if QT_CONFIG(tooltip)
        self.b_showExportStates.setToolTip(QCoreApplication.translate("mw_StateManager", u"show available export state types", None))
#endif // QT_CONFIG(tooltip)
        self.b_showExportStates.setText(QCoreApplication.translate("mw_StateManager", u"\u25bc", None))
        self.gb_publish.setTitle(QCoreApplication.translate("mw_StateManager", u"Publish", None))
        self.l_comment.setText(QCoreApplication.translate("mw_StateManager", u"Comment:", None))
#if QT_CONFIG(tooltip)
        self.b_description.setToolTip(QCoreApplication.translate("mw_StateManager", u"Add a description to the published file", None))
#endif // QT_CONFIG(tooltip)
        self.b_description.setText(QCoreApplication.translate("mw_StateManager", u"D", None))
#if QT_CONFIG(tooltip)
        self.b_preview.setToolTip(QCoreApplication.translate("mw_StateManager", u"Add a preview to the published file", None))
#endif // QT_CONFIG(tooltip)
        self.b_preview.setText(QCoreApplication.translate("mw_StateManager", u"P", None))
        self.b_publish.setText(QCoreApplication.translate("mw_StateManager", u"Publish", None))
        self.menuAbout.setTitle(QCoreApplication.translate("mw_StateManager", u"Options", None))
        self.menuRecentProjects.setTitle(QCoreApplication.translate("mw_StateManager", u"Projects", None))
    # retranslateUi

