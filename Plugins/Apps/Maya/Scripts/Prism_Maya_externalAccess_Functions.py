# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


import os
import platform
import shutil

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_Maya_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.core.registerCallback(
            "userSettings_saveSettings",
            self.userSettings_saveSettings,
            plugin=self.plugin,
        )
        self.core.registerCallback(
            "userSettings_loadSettings",
            self.userSettings_loadSettings,
            plugin=self.plugin,
        )
        self.core.registerCallback("getPresetScenes", self.getPresetScenes, plugin=self.plugin)
        self.core.registerCallback(
            "preProjectSettingsLoad", self.preProjectSettingsLoad, plugin=self.plugin
        )
        self.core.registerCallback(
            "preProjectSettingsSave", self.preProjectSettingsSave, plugin=self.plugin
        )
        self.core.registerCallback(
            "projectSettings_loadUI", self.projectSettings_loadUI, plugin=self.plugin
        )

    @err_catcher(name=__name__)
    def userSettings_loadUI(self, origin, tab):
        if self.core.appPlugin.pluginName == "Maya":
            origin.w_addModulePath = QWidget()
            origin.b_addModulePath = QPushButton(
                "Add current project to Maya module path"
            )
            lo_addModulePath = QHBoxLayout()
            origin.w_addModulePath.setLayout(lo_addModulePath)
            lo_addModulePath.setContentsMargins(0, 9, 0, 9)
            lo_addModulePath.addStretch()
            lo_addModulePath.addWidget(origin.b_addModulePath)
            tab.layout().addWidget(origin.w_addModulePath)

            origin.b_addModulePath.clicked.connect(self.appendEnvFile)

            if not os.path.exists(self.core.prismIni):
                origin.b_addModulePath.setEnabled(False)

        tab.lo_settings = QGridLayout()
        tab.layout().addLayout(tab.lo_settings)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        tab.lo_settings.addItem(spacer, 0, 0)

        origin.l_mayaSceneType = QLabel("Save scene as:")
        origin.cb_mayaSceneType = QComboBox()
        tab.lo_settings.addWidget(origin.l_mayaSceneType, 1, 1)
        tab.lo_settings.addWidget(origin.cb_mayaSceneType, 1, 2)

        self.saveSceneTypes = [
            ".ma",
            ".mb",
            ".ma (prefer current scene type)",
            ".mb (prefer current scene type)",
        ]

        origin.cb_mayaSceneType.addItems(self.saveSceneTypes)

        origin.l_mayaProject = QLabel("Set Maya project to Prism project: ")
        origin.chb_mayaProject = QCheckBox("")
        origin.chb_mayaProject.setChecked(True)
        origin.chb_mayaProject.setLayoutDirection(Qt.RightToLeft)

        origin.l_mayaPluginPaths = QLabel("Add project to Maya plugin search paths: ")
        origin.chb_mayaPluginPaths = QCheckBox("")
        origin.chb_mayaPluginPaths.setLayoutDirection(Qt.RightToLeft)

        tab.lo_settings.addWidget(origin.l_mayaProject, 2, 1)
        tab.lo_settings.addWidget(origin.chb_mayaProject, 2, 2)
        tab.lo_settings.addWidget(origin.l_mayaPluginPaths, 3, 1)
        tab.lo_settings.addWidget(origin.chb_mayaPluginPaths, 3, 2)

    @err_catcher(name=__name__)
    def userSettings_saveSettings(self, origin, settings):
        if "maya" not in settings:
            settings["maya"] = {}

        settings["maya"]["saveSceneType"] = origin.cb_mayaSceneType.currentText()
        settings["maya"]["setMayaProject"] = origin.chb_mayaProject.isChecked()
        settings["maya"]["addProjectPluginPaths"] = origin.chb_mayaPluginPaths.isChecked()
        if self.core.appPlugin.pluginName == "Maya":
            if settings["maya"]["setMayaProject"]:
                if getattr(self.core, "projectPath", None):
                    prj = self.core.appPlugin.getMayaProject()
                    if os.path.normpath(prj) != os.path.normpath(self.core.projectPath):
                        self.core.appPlugin.setMayaProject(self.core.projectPath)
            else:
                self.core.appPlugin.setMayaProject(default=True)

            if settings["maya"]["addProjectPluginPaths"]:
                self.core.appPlugin.addProjectPaths()

    @err_catcher(name=__name__)
    def userSettings_loadSettings(self, origin, settings):
        if "maya" in settings:
            if "saveSceneType" in settings["maya"]:
                saveType = settings["maya"]["saveSceneType"]
                idx = origin.cb_mayaSceneType.findText(saveType)
                if idx != -1:
                    origin.cb_mayaSceneType.setCurrentIndex(idx)

            if "setMayaProject" in settings["maya"]:
                mayaProject = settings["maya"]["setMayaProject"]
                origin.chb_mayaProject.setChecked(mayaProject)

            if "addProjectPluginPaths" in settings["maya"]:
                pluginPaths = settings["maya"]["addProjectPluginPaths"]
                origin.chb_mayaPluginPaths.setChecked(pluginPaths)

    @err_catcher(name=__name__)
    def getAutobackPath(self, origin):
        autobackpath = ""
        if self.core.appPlugin.pluginName == "Maya":
            import maya.cmds as cmds
            autobackpath = cmds.autoSave(q=True, destinationFolder=True)
        else:
            if platform.system() == "Windows":
                autobackpath = os.path.join(
                    self.core.getWindowsDocumentsPath(),
                    "maya",
                    "projects",
                    "default",
                    "autosave",
                )

        fileStr = "Maya Scene File ("
        for i in self.sceneFormats:
            fileStr += "*%s " % i

        fileStr += ")"

        return autobackpath, fileStr

    @err_catcher(name=__name__)
    def getScenefilePaths(self, scenePath):
        xgenfiles = [
            x
            for x in os.listdir(os.path.dirname(scenePath))
            if x.startswith(os.path.splitext(os.path.basename(scenePath))[0])
            and os.path.splitext(x)[1] in [".xgen", ".abc"]
        ]
        return xgenfiles

    @err_catcher(name=__name__)
    def copySceneFile(self, origin, origFile, targetPath, mode="copy"):
        xgenfiles = self.getScenefilePaths(origFile)
        for i in xgenfiles:
            curFilePath = os.path.join(os.path.dirname(origFile), i).replace("\\", "/")
            tFilePath = os.path.join(os.path.dirname(targetPath), i).replace("\\", "/")
            if curFilePath != tFilePath:
                if mode == "copy":
                    shutil.copy2(curFilePath, tFilePath)
                elif mode == "move":
                    shutil.move(curFilePath, tFilePath)

    @err_catcher(name=__name__)
    def getPresetScenes(self, presetScenes):
        if os.getenv("PRISM_SHOW_DEFAULT_SCENEFILE_PRESETS", "1") != "1":
            return

        presetDir = os.path.join(self.pluginDirectory, "Presets")
        scenes = self.core.entities.getPresetScenesFromFolder(presetDir)
        presetScenes += scenes

    @err_catcher(name=__name__)
    def preProjectSettingsLoad(self, origin, settings):
        if settings:
            if "maya" in settings:
                if "setPrefix" in settings["maya"]:
                    origin.e_mayaSetPrefix.setText(settings["maya"]["setPrefix"])

                if "useRelativePaths" in settings["maya"]:
                    origin.chb_mayaRelative.setChecked(settings["maya"]["useRelativePaths"])
            
            if "sceneBuilding" in settings:
                if "maya_apply_abc_caches" in settings["sceneBuilding"]:
                    origin.w_mayaAbcCaches.setDftTasks(settings["sceneBuilding"]["maya_apply_abc_caches"])

    @err_catcher(name=__name__)
    def preProjectSettingsSave(self, origin, settings):
        if "maya" not in settings:
            settings["maya"] = {}

        prefix = origin.e_mayaSetPrefix.text()
        settings["maya"]["setPrefix"] = prefix

        rel = origin.chb_mayaRelative.isChecked()
        settings["maya"]["useRelativePaths"] = rel

        if "sceneBuilding" not in settings:
            settings["sceneBuilding"] = {}

        val = origin.w_mayaAbcCaches.dftTasks()
        settings["sceneBuilding"]["maya_apply_abc_caches"] = val

    @err_catcher(name=__name__)
    def projectSettings_loadUI(self, origin):
        self.addUiToProjectSettings(origin)

    @err_catcher(name=__name__)
    def addUiToProjectSettings(self, projectSettings):
        projectSettings.w_maya = QGroupBox("Maya")
        lo_maya = QGridLayout()
        projectSettings.w_maya.setLayout(lo_maya)

        ttip = "Prefix for all selection sets created by Prism in Maya."
        l_prefix = QLabel("Selection Set Prefix:")
        l_prefix.setToolTip(ttip)
        projectSettings.e_mayaSetPrefix = QLineEdit()
        projectSettings.e_mayaSetPrefix.setToolTip(ttip)

        lo_maya.addWidget(l_prefix, 0, 0)
        sp_stretch = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        lo_maya.addItem(sp_stretch, 0, 1)
        lo_maya.addWidget(projectSettings.e_mayaSetPrefix, 0, 2)

        ttip = "When enabled Prism will use filepaths, relative to the Maya project when referencing files in Maya. When disabled, Prism will use absolute filepaths instead."
        l_relative = QLabel("Use relative paths:")
        l_relative.setToolTip(ttip)
        projectSettings.chb_mayaRelative = QCheckBox()
        projectSettings.chb_mayaRelative.setToolTip(ttip)

        lo_maya.addWidget(l_relative, 1, 0)
        sp_stretch = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Preferred)
        lo_maya.addItem(sp_stretch, 1, 1)
        lo_maya.addWidget(projectSettings.chb_mayaRelative, 1, 2)

        projectSettings.w_prjSettings.layout().addWidget(projectSettings.w_maya)

        if not hasattr(projectSettings, "w_sceneBuildingMaya"):
            projectSettings.w_sceneBuildingMaya = QGroupBox("Maya")
            projectSettings.lo_sceneBuildingMaya = QVBoxLayout(projectSettings.w_sceneBuildingMaya)
            idx = projectSettings.lo_sceneBuilding.count()
            projectSettings.lo_sceneBuilding.insertWidget(idx - 1, projectSettings.w_sceneBuildingMaya)

        from PrismUtils import ProjectWidgets
        dftTasks = {
            "entities": [],
            "departments": [],
            "tasks": [],
        }
        projectSettings.w_mayaAbcCaches = ProjectWidgets.DefaultSettingItem(projectSettings, "Apply Alembic Caches:", dftTasks)
        projectSettings.lo_sceneBuildingMaya.addWidget(projectSettings.w_mayaAbcCaches)
