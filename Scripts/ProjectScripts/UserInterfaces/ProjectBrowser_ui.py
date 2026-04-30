# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProjectBrowser.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qtpy.QtCore import *  # type: ignore
from qtpy.QtGui import *  # type: ignore
from qtpy.QtWidgets import *  # type: ignore

class Ui_mw_ProjectBrowser(object):
    def setupUi(self, mw_ProjectBrowser):
        if not mw_ProjectBrowser.objectName():
            mw_ProjectBrowser.setObjectName(u"mw_ProjectBrowser")
        mw_ProjectBrowser.resize(1074, 618)
        mw_ProjectBrowser.setMouseTracking(False)
        self.actionPrismSettings = QAction(mw_ProjectBrowser)
        self.actionPrismSettings.setObjectName(u"actionPrismSettings")
        self.actionRefresh = QAction(mw_ProjectBrowser)
        self.actionRefresh.setObjectName(u"actionRefresh")
        self.actionAssets = QAction(mw_ProjectBrowser)
        self.actionAssets.setObjectName(u"actionAssets")
        self.actionAssets.setCheckable(True)
        self.actionAssets.setChecked(True)
        self.actionShots = QAction(mw_ProjectBrowser)
        self.actionShots.setObjectName(u"actionShots")
        self.actionShots.setCheckable(True)
        self.actionShots.setChecked(True)
        self.actionFiles = QAction(mw_ProjectBrowser)
        self.actionFiles.setObjectName(u"actionFiles")
        self.actionFiles.setCheckable(True)
        self.actionFiles.setChecked(True)
        self.actionRecent = QAction(mw_ProjectBrowser)
        self.actionRecent.setObjectName(u"actionRecent")
        self.actionRecent.setCheckable(True)
        self.actionRecent.setChecked(True)
        self.actionOpenOnStart = QAction(mw_ProjectBrowser)
        self.actionOpenOnStart.setObjectName(u"actionOpenOnStart")
        self.actionOpenOnStart.setCheckable(True)
        self.actionOpenOnStart.setChecked(True)
        self.actionRenderWatch = QAction(mw_ProjectBrowser)
        self.actionRenderWatch.setObjectName(u"actionRenderWatch")
        self.actionStateManager = QAction(mw_ProjectBrowser)
        self.actionStateManager.setObjectName(u"actionStateManager")
        self.actionCloseAfterLoad = QAction(mw_ProjectBrowser)
        self.actionCloseAfterLoad.setObjectName(u"actionCloseAfterLoad")
        self.actionCloseAfterLoad.setCheckable(True)
        self.actionCloseAfterLoad.setChecked(True)
        self.actionAutoplay = QAction(mw_ProjectBrowser)
        self.actionAutoplay.setObjectName(u"actionAutoplay")
        self.actionAutoplay.setCheckable(True)
        self.actionAutoplay.setChecked(False)
        self.actionMedia = QAction(mw_ProjectBrowser)
        self.actionMedia.setObjectName(u"actionMedia")
        self.actionMedia.setCheckable(True)
        self.actionMedia.setChecked(True)
        self.actionTest = QAction(mw_ProjectBrowser)
        self.actionTest.setObjectName(u"actionTest")
        self.actionCheckForUpdates = QAction(mw_ProjectBrowser)
        self.actionCheckForUpdates.setObjectName(u"actionCheckForUpdates")
        self.actionCheckForUpdates.setCheckable(True)
        self.actionCheckForUpdates.setChecked(True)
        self.actionCheckForShotFrameRange = QAction(mw_ProjectBrowser)
        self.actionCheckForShotFrameRange.setObjectName(u"actionCheckForShotFrameRange")
        self.actionCheckForShotFrameRange.setCheckable(True)
        self.actionCheckForShotFrameRange.setChecked(True)
        self.actionProjectSettings = QAction(mw_ProjectBrowser)
        self.actionProjectSettings.setObjectName(u"actionProjectSettings")
        self.actionRefreshCurrentTabOnly = QAction(mw_ProjectBrowser)
        self.actionRefreshCurrentTabOnly.setObjectName(u"actionRefreshCurrentTabOnly")
        self.actionRefreshCurrentTabOnly.setCheckable(True)
        self.actionRefreshWhenSwitchingTabs = QAction(mw_ProjectBrowser)
        self.actionRefreshWhenSwitchingTabs.setObjectName(u"actionRefreshWhenSwitchingTabs")
        self.actionRefreshWhenSwitchingTabs.setCheckable(True)
        self.centralwidget = QWidget(mw_ProjectBrowser)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_17 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1054, 577))
        self.lo_scrollArea = QHBoxLayout(self.scrollAreaWidgetContents)
        self.lo_scrollArea.setObjectName(u"lo_scrollArea")
        self.w_header = QWidget(self.scrollAreaWidgetContents)
        self.w_header.setObjectName(u"w_header")
        self.verticalLayout = QVBoxLayout(self.w_header)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tbw_project = QTabWidget(self.w_header)
        self.tbw_project.setObjectName(u"tbw_project")

        self.verticalLayout.addWidget(self.tbw_project)


        self.lo_scrollArea.addWidget(self.w_header)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_17.addWidget(self.scrollArea)

        mw_ProjectBrowser.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mw_ProjectBrowser)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1074, 21))
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        mw_ProjectBrowser.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuTools.menuAction())
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionOpenOnStart)
        self.menuTools.addAction(self.actionCheckForUpdates)
        self.menuTools.addAction(self.actionCheckForShotFrameRange)
        self.menuTools.addAction(self.actionCloseAfterLoad)
        self.menuTools.addAction(self.actionAutoplay)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionStateManager)
        self.menuTools.addAction(self.actionPrismSettings)

        self.retranslateUi(mw_ProjectBrowser)

        self.tbw_project.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(mw_ProjectBrowser)
    # setupUi

    def retranslateUi(self, mw_ProjectBrowser):
        mw_ProjectBrowser.setWindowTitle(QCoreApplication.translate("mw_ProjectBrowser", u"ProjectBrowser", None))
        self.actionPrismSettings.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Settings...", None))
        self.actionRefresh.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Refresh", None))
        self.actionAssets.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Assets", None))
        self.actionShots.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Shots", None))
        self.actionFiles.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Files", None))
        self.actionRecent.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Recent", None))
        self.actionOpenOnStart.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Open on startup", None))
        self.actionRenderWatch.setText(QCoreApplication.translate("mw_ProjectBrowser", u"RenderWatch", None))
        self.actionStateManager.setText(QCoreApplication.translate("mw_ProjectBrowser", u"State Manager...", None))
        self.actionCloseAfterLoad.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Close after loading", None))
        self.actionAutoplay.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Autoplay preview", None))
        self.actionMedia.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Media", None))
        self.actionTest.setText(QCoreApplication.translate("mw_ProjectBrowser", u"test", None))
        self.actionCheckForUpdates.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Check for latest import version", None))
        self.actionCheckForShotFrameRange.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Check for shot frame range", None))
        self.actionProjectSettings.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Project Settings...", None))
        self.actionRefreshCurrentTabOnly.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Refresh current tab only", None))
        self.actionRefreshWhenSwitchingTabs.setText(QCoreApplication.translate("mw_ProjectBrowser", u"Refresh when switching tabs", None))
        self.menuTools.setTitle(QCoreApplication.translate("mw_ProjectBrowser", u"Options", None))
    # retranslateUi

