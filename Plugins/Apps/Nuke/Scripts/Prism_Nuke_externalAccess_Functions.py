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
import sys
import subprocess
import traceback

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_Nuke_externalAccess_Functions(object):
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
        origin.w_nukeVersion = QWidget()
        origin.lo_nukeVersion = QHBoxLayout(origin.w_nukeVersion)
        origin.lo_nukeVersion.setContentsMargins(0, 0, 0, 0)
        origin.l_nukeVersion = QLabel("Nuke Version:")
        origin.cb_nukeVersion = QComboBox()
        origin.cb_nukeVersion.addItems(["Default", "NukeX", "NukeX (Non-Commercial)", "Indie", "Assist", "Studio", "Studio (Non-Commercial)", "Non-Commercial"])
        origin.lo_nukeVersion.addWidget(origin.l_nukeVersion)
        origin.lo_nukeVersion.addWidget(origin.cb_nukeVersion)
        origin.lo_nukeVersion.addStretch()
        tab.layout().addWidget(origin.w_nukeVersion)

        origin.chb_nukeRelativePaths = QCheckBox("Use relative paths")
        tab.layout().addWidget(origin.chb_nukeRelativePaths)

        origin.chb_nukeUseReadPrism = QCheckBox("Open Prism window with \"R\" shortcut")
        origin.chb_nukeUseReadPrism.setChecked(True)
        tab.layout().addWidget(origin.chb_nukeUseReadPrism)

        origin.chb_nukeUseWritePrism = QCheckBox("Use WritePrism gizmo")
        origin.chb_nukeUseWritePrism.setChecked(False)
        tab.layout().addWidget(origin.chb_nukeUseWritePrism)

    @err_catcher(name=__name__)
    def userSettings_saveSettings(self, origin, settings):
        if "nuke" not in settings:
            settings["nuke"] = {}

        settings["nuke"]["nukeVersion"] = origin.cb_nukeVersion.currentText()
        settings["nuke"]["useRelativePaths"] = origin.chb_nukeRelativePaths.isChecked()
        settings["nuke"]["useReadPrism"] = origin.chb_nukeUseReadPrism.isChecked()
        settings["nuke"]["useWritePrism"] = origin.chb_nukeUseWritePrism.isChecked()

    @err_catcher(name=__name__)
    def userSettings_loadSettings(self, origin, settings):
        if "nuke" in settings:
            if "nukeVersion" in settings["nuke"]:
                origin.cb_nukeVersion.setCurrentText(settings["nuke"]["nukeVersion"])
            if "useRelativePaths" in settings["nuke"]:
                origin.chb_nukeRelativePaths.setChecked(settings["nuke"]["useRelativePaths"])
            if "useReadPrism" in settings["nuke"]:
                origin.chb_nukeUseReadPrism.setChecked(settings["nuke"]["useReadPrism"])
            if "useWritePrism" in settings["nuke"]:
                origin.chb_nukeUseWritePrism.setChecked(settings["nuke"]["useWritePrism"])

    @err_catcher(name=__name__)
    def getAutobackPath(self, origin):
        autobackpath = ""

        fileStr = "Nuke Script ("
        for i in self.sceneFormats:
            fileStr += "*%s " % i

        fileStr += ")"

        return autobackpath, fileStr

    @err_catcher(name=__name__)
    def customizeExecutable(self, origin, appPath, filepath):
        fileStarted = False
        nukeVersion = self.core.getConfig("nuke", "nukeVersion")
        if nukeVersion and nukeVersion != "Default":
            if appPath == "":
                if not hasattr(self, "nukePath"):
                    self.nukePath = self.core.getDefaultAppByExtension(".nk")

                if self.nukePath is not None and os.path.exists(self.nukePath):
                    appPath = self.nukePath
                else:
                    QMessageBox.warning(
                        self.core.messageParent,
                        "Warning",
                        "Nuke executable doesn't exist:\n\n%s" % self.nukePath,
                    )

            if appPath is not None and appPath != "":
                args = [appPath, self.core.fixPath(filepath)]
                if nukeVersion == "NukeX":
                    args.insert(-1, "--nukex")
                elif nukeVersion == "NukeX (Non-Commercial)":
                    args.insert(-1, "--nukex")
                    args.insert(-1, "--nc")
                elif nukeVersion == "Indie":
                    args.insert(-1, "--indie")
                elif nukeVersion == "Assist":
                    args.insert(-1, "--nukeassist")
                elif nukeVersion == "Studio":
                    args.insert(-1, "--studio")
                elif nukeVersion == "Studio (Non-Commercial)":
                    args.insert(-1, "--studio")
                    args.insert(-1, "--nc")
                elif nukeVersion == "Non-Commercial":
                    args.insert(-1, "--nc")

                dccEnv = self.core.startEnv.copy()
                usrEnv = self.core.users.getUserEnvironment(appPluginName="Nuke")
                for envVar in usrEnv:
                    dccEnv[envVar["key"]] = envVar["value"]

                prjEnv = self.core.projects.getProjectEnvironment(appPluginName="Nuke")
                for envVar in prjEnv:
                    dccEnv[envVar["key"]] = envVar["value"]

                self.core.callback(name="preLaunchApp", args=[args, dccEnv])

                try:
                    subprocess.Popen(args, env=self.core.startEnv)
                except:
                    mods = QApplication.keyboardModifiers()
                    if mods == Qt.ControlModifier:
                        if os.path.isfile(args[0]):
                            msg = "Could not execute file:\n\n%s\n\nUsed arguments: %s" % (traceback.format_exc(), args)
                        else:
                            msg = "Executable doesn't exist:\n\n%s\n\nCheck your executable override in the Prism User Settings." % args[0]
                        self.core.popup(msg)
                    else:
                        subprocess.Popen(" ".join(args), env=self.core.startEnv, shell=True)
                        fileStarted = True
                else:
                    fileStarted = True

        return fileStarted

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
            if "sceneBuilding" in settings:
                if "nuke_load_media" in settings["sceneBuilding"]:
                    origin.w_nukeLoadMedia.setDftTasks(settings["sceneBuilding"]["nuke_load_media"])

    @err_catcher(name=__name__)
    def preProjectSettingsSave(self, origin, settings):
        if "nuke" not in settings:
            settings["nuke"] = {}

        if "sceneBuilding" not in settings:
            settings["sceneBuilding"] = {}

        val = origin.w_nukeLoadMedia.dftTasks()
        settings["sceneBuilding"]["nuke_load_media"] = val

    @err_catcher(name=__name__)
    def projectSettings_loadUI(self, origin):
        self.addUiToProjectSettings(origin)

    @err_catcher(name=__name__)
    def addUiToProjectSettings(self, projectSettings):
        if not hasattr(projectSettings, "w_sceneBuildingNuke"):
            projectSettings.w_sceneBuildingNuke = QGroupBox("Nuke")
            projectSettings.lo_sceneBuildingNuke = QVBoxLayout(projectSettings.w_sceneBuildingNuke)
            idx = projectSettings.lo_sceneBuilding.count()
            projectSettings.lo_sceneBuilding.insertWidget(idx - 1, projectSettings.w_sceneBuildingNuke)

        from PrismUtils import ProjectWidgets
        projectSettings.w_nukeLoadMedia = ProjectWidgets.DefaultSettingItem(projectSettings, "Load Media:")
        projectSettings.lo_sceneBuildingNuke.addWidget(projectSettings.w_nukeLoadMedia)
