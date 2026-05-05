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
import platform
import random
import logging
import tempfile
import re

import nuke
if nuke.env.get("gui"):
    try:
        from nukescripts import flipbooking, renderdialog, fnFlipbookRenderer
    except:
        pass

try:
    from qtpy.QtCore import *
    from qtpy.QtGui import *
    from qtpy.QtWidgets import *
except:
    if nuke.NUKE_VERSION_MAJOR >= 16:
        from PySide6.QtCore import *
        from PySide6.QtGui import *
        from PySide6.QtWidgets import *
    else:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *


try:
    from PrismUtils.Decorators import err_catcher as err_catcher
except:
    # err_catcher = lambda name: lambda func, *args, **kwargs: func(*args, **kwargs)
    from functools import wraps
    def err_catcher(name):
        return lambda x, y=name, z=False: err_handler(x, name=y, plugin=z)

    def err_handler(func, name="", plugin=False):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return func_wrapper


logger = logging.getLogger(__name__)


class Prism_Nuke_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.isRendering = {}
        self.core.registerCallback(
            "postSaveScene", self.postSaveScene, plugin=self.plugin
        )
        self.core.registerCallback("postBuildScene", self.postBuildScene, plugin=self.plugin)
        self.core.registerCallback(
            "onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self.plugin
        )
        self.core.registerCallback(
            "onPreMediaPlayerDragged", self.onPreMediaPlayerDragged, plugin=self.plugin
        )
        self.core.registerCallback(
            "onStateManagerOpen", self.onStateManagerOpen, plugin=self.plugin
        )
        self.core.registerCallback(
            "productSelectorContextMenuRequested", self.productSelectorContextMenuRequested, plugin=self.plugin
        )
        self.core.registerCallback(
            "updatedEnvironmentVars", self.updatedEnvironmentVars, plugin=self.plugin
        )
        if "OCIO" in [item["key"] for item in self.core.users.getUserEnvironment()]:
            self.refreshOcio()

        nuke.addOnUserCreate(self.refreshOcio, nodeClass="Root")
        self.isRenderingFlipbook = False

    @err_catcher(name=__name__)
    def startup(self, origin):
        if self.core.uiAvailable:
            origin.timer.stop()

            for obj in QApplication.topLevelWidgets():
                if (
                    obj.inherits("QMainWindow")
                    and obj.metaObject().className() == "Foundry::UI::DockMainWindow"
                ):
                    nukeQtParent = obj
                    break
            else:
                nukeQtParent = QWidget()

            # origin.messageParent = QWidget()
            # origin.messageParent.setParent(nukeQtParent, Qt.Window)
            origin.messageParent = nukeQtParent
            if platform.system() != "Windows" and self.core.useOnTop:
                origin.messageParent.setWindowFlags(
                    origin.messageParent.windowFlags() ^ Qt.WindowStaysOnTopHint
                )

        self.addPluginPaths()
        if self.core.uiAvailable:
            self.addMenus()

        self.addCallbacks()

    @err_catcher(name=__name__)
    def addPluginPaths(self):
        gdir = os.path.join(
            os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "Gizmos"
        )
        gdir = gdir.replace("\\", "/")
        nuke.pluginAddPath(gdir)

    @err_catcher(name=__name__)
    def addMenus(self):
        nuke.menu("Nuke").addCommand("Prism/Save", self.saveScene, "Ctrl+s")
        nuke.menu("Nuke").addCommand("Prism/Save Version", self.core.saveScene, "Alt+Shift+s")
        nuke.menu("Nuke").addCommand("Prism/Save Comment...", self.core.saveWithComment, "Ctrl+Shift+S")
        nuke.menu("Nuke").addCommand("Prism/Project Browser...", self.core.projectBrowser)
        nuke.menu("Nuke").addCommand("Prism/Settings...", self.core.prismSettings)
        nuke.menu("Nuke").addCommand("Prism/Manage Media Versions...", self.openMediaVersionsDialog)
        if (nuke.NUKE_VERSION_MAJOR >= 16) or (nuke.NUKE_VERSION_MAJOR == 15 and nuke.NUKE_VERSION_MINOR >= 2) and os.getenv("PRISM_NUKE_ENABLE_MULTISHOT", "0") == "1":
            nuke.menu("Nuke").addCommand("Prism/Import Shots...", self.onImportShotsTriggered)

        nuke.menu("Nuke").addCommand("Prism/Export Nodes...", self.onExportTriggered)

        toolbar = nuke.toolbar("Nodes")
        iconPath = os.path.join(
            self.core.prismRoot, "Scripts", "UserInterfacesPrism", "p_tray.png"
        )
        toolbar.addMenu("Prism", icon=iconPath)
        useReadPrism = self.core.getConfig("nuke", "useReadPrism", dft=True, config="user")
        if useReadPrism:
            nuke.menu("Nuke").addCommand("Prism/Read...", self.createReadWithBrowse, "r", shortcutContext=2)
        else:
            nuke.menu("Nuke").addCommand("Prism/Read...", self.createReadWithBrowse)

        useWritePrism = self.core.getConfig("nuke", "useWritePrism", dft=False, config="user")
        if useWritePrism:
            toolbar.addCommand("Prism/WritePrism", lambda: nuke.createNode("WritePrism"), "w", shortcutContext=2)

    @err_catcher(name=__name__)
    def addCallbacks(self):
        nuke.addOnScriptLoad(self.core.sceneOpen)
        nuke.addFilenameFilter(self.expandEnvVarsInFilepath)
        nuke.addOnScriptSave(self.core.scenefileSaved)
        nuke.addOnUserCreate(self.onUserNodeCreated)
        if os.getenv("PRISM_NUKE_ENABLE_MULTISHOT", "0") == "1":
            nuke.addKnobChanged(self.onRootKnobChanged, node=nuke.Root())

        import nukescripts
        nukescripts.drop.addDropDataCallback(self.dropHandler)

    @err_catcher(name=__name__)
    def dropHandler(self, mimeType, text):
        if not getattr(self.core, "projectPath", None):
            return

        text = text.replace("\\", "/")
        useRel = self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user")
        if os.path.isdir(text):
            srcs = self.core.media.getImgSources(text)
        elif os.path.isfile(text):
            srcs = [text]
        else:
            return

        success = False
        for src in srcs:
            if os.path.splitext(src)[1] not in self.core.media.supportedFormats:
                continue

            if "#"*self.core.framePadding not in src:
                src = self.core.media.getSequenceFromFilename(src)

            if "#"*self.core.framePadding in src:
                files = self.core.media.getFilesFromSequence(src)
                start, end = self.core.media.getFrameRangeFromSequence(files)
                if start and end and start != "?" and end != "?":
                    src += " %s-%s" % (start, end)

            if useRel and text.replace("\\", "/").startswith(self.core.projectPath.replace("\\", "/")):
                src = self.makePathRelative(src)

            read_node = nuke.createNode("Read", inpanel=False)
            read_node["file"].fromUserText(src)
            success = True
            
            if success:
                return True

    @err_catcher(name=__name__)
    def makePathRelative(self, path):
        path = path.replace("\\", "/")
        prjPath = self.core.projectPath.replace("\\", "/").rstrip("/")
        newVars = (nuke.NUKE_VERSION_MAJOR >= 16) or (nuke.NUKE_VERSION_MAJOR == 15 and nuke.NUKE_VERSION_MINOR >= 2)
        if newVars:
            relPath = path.replace(prjPath, "%PRISM_JOB")
        else:
            relPath = path.replace(prjPath, "%PRISM_JOB%")

        return relPath

    @err_catcher(name=__name__)
    def expandEnvVarsInFilepath(self, path):
        if not self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user"):
            return path

        expanded_path = os.path.expandvars(path)
        if hasattr(self.core, "projectPath"):
            prjPath = self.core.projectPath.replace("\\", "/").rstrip("/")
            expanded_path = expanded_path.replace("%PRISM_JOB", prjPath)

        return expanded_path

    @err_catcher(name=__name__)
    def updatedEnvironmentVars(self, reason, envVars, beforeRefresh=False):
        doReload = False

        if reason == "refreshProject" and getattr(self, "unloadedOCIO", False):
            doReload = True
        else:
            for envVar in envVars:
                if envVar["key"] == "OCIO" and envVar["value"] != envVar["orig"]:
                    if reason == "unloadProject" and beforeRefresh:
                        self.unloadedOCIO = True
                        continue

                    doReload = True

        if doReload:
            self.unloadedOCIO = False
            self.refreshOcio()

    @err_catcher(name=__name__)
    def refreshOcio(self):
        ocio = os.getenv("OCIO", "")
        if ocio:
            r = nuke.root()
            r["colorManagement"].setValue("OCIO")
            r["OCIO_config"].setValue("custom")
            r["customOCIOConfigPath"].setValue(ocio.replace("\\", "/"))
            r.knob("reloadConfig").execute()

    @err_catcher(name=__name__)
    def sceneOpen(self, origin):
        if self.core.shouldAutosaveTimerRun():
            origin.startAutosaveTimer()

        if os.getenv("PRISM_NUKE_CHECK_MEDIA_ON_SCENE_OPEN", "1") == "1":
            dlg = MediaVersionsDialog(self)
            if dlg.getOutdatedMedia():
                msgStr = "There are new media versions available."
                msg = self.core.popupQuestion(
                    msgStr,
                    buttons=["Show Versions...", "Ignore"],
                    icon=QMessageBox.Information,
                    escapeButton="Ignore",
                    default="Ignore",
                    doExec=False,
                )
                if not self.core.isStr(msg):
                    msg.buttonClicked.connect(self.onShowVersionsClicked)
                    msg.show()

        self.refreshWriteNodes()

    @err_catcher(name=__name__)
    def onShowVersionsClicked(self, button):
        result = button.text()
        if result == "Show Versions...":
            self.openMediaVersionsDialog()

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin, path=True):
        try:
            currentFileName = nuke.value("root.name")
            if currentFileName:
                currentFileName = os.path.abspath(currentFileName)

        except:
            currentFileName = ""

        if currentFileName == "Root":
            currentFileName = ""

        if not path:
            currentFileName = os.path.basename(currentFileName)

        return currentFileName

    @err_catcher(name=__name__)
    def getCurrentSceneFiles(self, origin):
        return [self.core.getCurrentFileName()]

    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        return self.sceneFormats[0]

    @err_catcher(name=__name__)
    def saveScene(self, origin=None, filepath=None, details={}):
        try:
            if filepath:
                return nuke.scriptSaveAs(filename=filepath, overwrite=1)
            else:
                return nuke.scriptSave()

        except:
            return ""

    @err_catcher(name=__name__)
    def getImportPaths(self, origin):
        return False

    @err_catcher(name=__name__)
    def getFrameRange(self, origin):
        startframe = nuke.root().knob("first_frame").value()
        endframe = nuke.root().knob("last_frame").value()

        return [startframe, endframe]

    @err_catcher(name=__name__)
    def getCurrentFrame(self):
        currentFrame = nuke.root().knob("frame").value()
        return currentFrame

    @err_catcher(name=__name__)
    def setFrameRange(self, origin, startFrame, endFrame):
        nuke.root().knob("first_frame").setValue(float(startFrame))
        nuke.root().knob("last_frame").setValue(float(endFrame))

    @err_catcher(name=__name__)
    def getFPS(self, origin):
        return nuke.knob("root.fps")

    @err_catcher(name=__name__)
    def setFPS(self, origin, fps):
        return nuke.knob("root.fps", str(fps))

    @err_catcher(name=__name__)
    def getResolution(self):
        resFormat = [nuke.root().width(), nuke.root().height()]
        return resFormat

    @err_catcher(name=__name__)
    def setResolution(self, width=None, height=None, pixelAspect=None):
        if pixelAspect:
            return nuke.knob("root.format", "%s %s 0 0 %s %s %s" % (width, height, width, height, pixelAspect))
        else:
            return nuke.knob("root.format", "%s %s" % (width, height))

    @err_catcher(name=__name__)
    def getPixelAspectRatio(self):
        return nuke.root().pixelAspect()

    @err_catcher(name=__name__)
    def setPixelAspectRatio(self, pixelAspect):
        res = self.getResolution()
        self.setResolution(res[0], res[1], pixelAspect)

    @err_catcher(name=__name__)
    def updateNukeNodes(self):
        updatedNodes = []

        for i in nuke.selectedNodes():
            if i.Class() != "Read":
                continue

            curPath = i.knob("file").value()
            curPath = self.expandEnvVarsInFilepath(curPath)
            version = self.core.mediaProducts.getLatestVersionFromFilepath(curPath)
            if version and version["path"] not in curPath:
                filepattern = self.core.mediaProducts.getFilePatternFromVersion(version)
                filepaths = self.core.media.getFilesFromSequence(filepattern)
                if not filepaths:
                    sources = self.core.media.getImgSources(os.path.dirname(filepattern))
                    if not sources:
                        continue

                    filepattern = sources[0]

                if self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user"):
                    filepattern = self.makePathRelative(filepattern)

                filepattern = filepattern.replace("\\", "/")
                i.knob("file").setValue(filepattern)
                updatedNodes.append(i)

        if len(updatedNodes) == 0:
            self.core.popup("No nodes were updated", severity="info")
        else:
            mStr = "%s nodes were updated:\n\n" % len(updatedNodes)
            for i in updatedNodes:
                mStr += i.name() + "\n"

            self.core.popup(mStr, severity="info")

    # @err_catcher(name=__name__)
    # def renderAllWritePrismNodes(self):
    #     wpNodes = [node for node in nuke.allNodes() if node.Class() == "WritePrism"]
    #     self.renderWritePrismNodes(wpNodes)

    # @err_catcher(name=__name__)
    # def renderSelectedWritePrismNodes(self):
    #     wpNodes = [node for node in nuke.selectedNodes() if node.Class() == "WritePrism"]
    #     self.renderWritePrismNodes(wpNodes)

    # @err_catcher(name=__name__)
    # def renderWritePrismNodes(self, nodes):
    #     for node in nodes:
    #         self.getOutputPath(node.node("WritePrismBase"), node)

    #     import nukescripts
    #     nukescripts.showRenderDialog(nodes, False)

    @err_catcher(name=__name__)
    def getCamNodes(self, origin, cur=False):
        sceneCams = ["nuke"]
        return sceneCams

    @err_catcher(name=__name__)
    def getCamName(self, origin, handle):
        return handle

    @err_catcher(name=__name__)
    def isNodeValid(self, origin, handle):
        return True

    @err_catcher(name=__name__)
    def readNode_onBrowseClicked(self, node, quiet=False):
        if hasattr(self, "dlg_media"):
            self.dlg_media.close()

        if not getattr(self.core, "projectPath", None):
            if not quiet:
                self.core.popup("There is no active project in Prism.")

            return

        self.dlg_media = ReadMediaDialog(self, node)
        self.dlg_media.mediaSelected.connect(lambda x: self.readNode_mediaSelected(node, x))
        self.dlg_media.show()

    @err_catcher(name=__name__)
    def readNode_mediaSelected(self, node, version):
        mediaFiles = self.core.mediaProducts.getFilesFromContext(version)
        validFiles = self.core.media.filterValidMediaFiles(mediaFiles)
        if not validFiles:
            return

        validFiles = sorted(validFiles, key=lambda x: x if "cryptomatte" not in os.path.basename(x) else "zzz" + x)
        baseName, extension = os.path.splitext(validFiles[0])
        seqFiles = self.core.media.detectSequences(validFiles)
        if seqFiles:
            path = list(seqFiles)[0].replace("\\", "/")
            useRel = self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user")
            if "#"*self.core.framePadding not in path:
                path = self.core.media.getSequenceFromFilename(path)

            if "#"*self.core.framePadding in path:
                files = self.core.media.getFilesFromSequence(path)
                start, end = self.core.media.getFrameRangeFromSequence(files)
                if start and end and start != "?" and end != "?":
                    path += " %s-%s" % (start, end)

            if useRel:
                path = self.makePathRelative(path)

            node.knob("file").fromUserText(path)

    @err_catcher(name=__name__)
    def readNode_onOpenInClicked(self, node):
        self.core.openFolder(node.knob("file").value())

    @err_catcher(name=__name__)
    def createReadWithBrowse(self):
        readNode = nuke.createNode("Read")
        self.readNode_onBrowseClicked(readNode, quiet=True)

    @err_catcher(name=__name__)
    def getIdentifierFromNode(self, node):
        return node.knob("identifier").evaluate()

    @err_catcher(name=__name__)
    def getCommentFromNode(self, node):
        return node.knob("comment").value()

    @err_catcher(name=__name__)
    def sm_render_fixOutputPath(self, origin, outputName, singleFrame=False, state=None):
        if self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user"):
            outputName = self.makePathRelative(outputName)

        return outputName

    @err_catcher(name=__name__)
    def getRenderVersionFromWriteNode(self, node):
        version = None
        if node.knob("autoversion") and not node.knob("autoversion").value():
            intVersion = node.knob("renderversion").value()
            version = self.core.versionFormat % intVersion

        return version

    @err_catcher(name=__name__)
    def getOutputPath(self, node, group=None, render=False, updateValues=True, force=False):
        if self.isRenderingFlipbook:
            return

        if not group:
            group = node

        if not nuke.env.get("gui") and not force:
            filename = group.knob("fileName").toScript()
            if render and self.core.getConfig("globals", "backupScenesOnPublish", config="project"):
                self.core.entities.backupScenefile(os.path.dirname(filename))

            return filename

        try:
            taskName = self.getIdentifierFromNode(group)
            comment = self.getCommentFromNode(group)
            fileType = group.knob("file_type").value()
            location = group.knob("location").value()
        except Exception as e:
            logger.warning("failed to get node knob values: %s" % str(e))
            return ""

        if not bool(location.strip()):
            location = "global"

        version = self.getRenderVersionFromWriteNode(group)
        outputName = self.core.getCompositingOut(
            taskName,
            fileType,
            version,
            render,
            location,
            comment=comment,
            node=node,
        )

        isNukeAssist = "--nukeassist" in nuke.rawArgs
        if not self.isNodeRendering(node) and not isNukeAssist and updateValues or render:
            group.knob("fileName").setValue(outputName)
            # group.knob("fileName").clearFlag(0x10000000) # makes knob read-only, but leads to double property Uis

        return outputName

    @err_catcher(name=__name__)
    def startRender(self, node, group=None, start=None, end=None, dependencies=None):
        if not group:
            group = node

        if group.knob("submitJob").value():
            return self.openFarmSubmitter(node, group, dependencies=dependencies)

        taskName = self.getIdentifierFromNode(group)
        if not taskName:
            self.core.popup("Please choose an identifier")
            return

        fileName = self.getOutputPath(node, group, force=True)
        if fileName == "FileNotInPipeline":
            self.core.showFileNotInProjectWarning(title="Warning")
            return

        if start is None and not self.core.uiAvailable:
            start = nuke.root().knob("first_frame").value()
            end = nuke.root().knob("last_frame").value()

        settings = {
            "outputName": fileName,
            "node": node,
            "group": group,
            "start": start,
            "end": end,
            "identifier": taskName,
        }
        scenefile = self.core.getCurrentFileName()
        kwargs = {
            "state": self,
            "scenefile": scenefile,
            "settings": settings,
        }

        result = self.core.callback("preRender", **kwargs)
        for res in result:
            if isinstance(res, dict) and res.get("cancel", False):
                return [
                    "Nuke Render - error - %s" % res.get("details", "preRender hook returned False")
                ]

        self.core.saveScene(versionUp=False, prismReq=False)
        if start is None:
            node.knob("Render").execute()
        else:
            nuke.execute(node, start, end)

        self.getOutputPath(node, group)
        kwargs = {
            "state": self,
            "scenefile": scenefile,
            "settings": settings,
        }

        self.core.callback("postRender", **kwargs)

    @err_catcher(name=__name__)
    def showPrevVersions(self, node, group=None):
        if not group:
            group = node

        self.dlg_version = VersionDlg(self, node, group)
        if not self.dlg_version.isValid:
            return

        if group.knob("renderversion"):
            self.dlg_version.versionSelected.connect(lambda x: group.knob("autoversion").setValue(0))
            self.dlg_version.versionSelected.connect(group.knob("renderversion").setValue)

        self.dlg_version.show()

    @err_catcher(name=__name__)
    def startedRendering(self, node, outputPath):
        nodePath = node.fullName()
        self.isRendering[nodePath] = [True, outputPath]

        nodeName = "root." + node.fullName()
        parentName = ".".join(nodeName.split(".")[:-1])
        group = nuke.toNode(parentName)
        if not group or group.Class() != "WritePrism":
            group = node

        prevKnob = group.knob("prevFileName")
        if prevKnob:
            prevKnob.setValue(outputPath)
            prevKnobE = group.knob("prevFileNameEdit")
            if prevKnobE:
                prevKnobE.setValue(outputPath)

    @err_catcher(name=__name__)
    def isNodeRendering(self, node):
        nodePath = node.fullName()
        rendering = nodePath in self.isRendering and self.isRendering[nodePath][0]
        return rendering

    @err_catcher(name=__name__)
    def getPathFromRenderingNode(self, node):
        nodePath = node.fullName()
        if nodePath in self.isRendering:
            return self.isRendering[nodePath][1]
        else:
            return ""

    @err_catcher(name=__name__)
    def finishedRendering(self, node):
        nodePath = node.fullName()
        if nodePath in self.isRendering:
            del self.isRendering[nodePath]

    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        return nuke.NUKE_VERSION_STRING

    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self, origin):
        origin.actionStateManager.setEnabled(False)

    @err_catcher(name=__name__)
    def onPreMediaPlayerDragged(self, origin, urlList):
        urlList[:] = [urlList[0]]

    @err_catcher(name=__name__)
    def newScene(self, force=False):
        nuke.scriptClear()
        return True

    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        if os.path.splitext(filepath)[1] not in self.sceneFormats:
            return False

        try:
            cleared = nuke.scriptSaveAndClear()
        except Exception as e:
            if "cannot clear script whilst executing" in str(e):
                self.core.popup(e)

            cleared = False

        if cleared:
            try:
                nuke.scriptOpen(filepath)
            except:
                pass

        return True

    @err_catcher(name=__name__)
    def importImages(self, filepath=None, mediaBrowser=None, parent=None):
        if mediaBrowser:
            if mediaBrowser.origin.getCurrentAOV() and mediaBrowser.origin.w_preview.cb_layer.count() > 1:
                fString = "Please select an import option:"
                buttons = ["Current AOV", "All AOVs", "Layout all AOVs"]
                parent = parent or mediaBrowser.origin.projectBrowser
                result = self.core.popupQuestion(fString, buttons=buttons, icon=QMessageBox.NoIcon, parent=parent)
            else:
                result = "Current AOV"

            if result == "Current AOV":
                self.nukeImportSource(mediaBrowser)
            elif result == "All AOVs":
                self.nukeImportPasses(mediaBrowser)
            elif result == "Layout all AOVs":
                self.nukeLayout(mediaBrowser)
            else:
                return

    @err_catcher(name=__name__)
    def importMedia(self, filepath, start=None, end=None):
        if "#"*self.core.framePadding not in filepath:
            filepath = self.core.media.getSequenceFromFilename(filepath)

        if start is None:
            if "#"*self.core.framePadding in filepath:
                files = self.core.media.getFilesFromSequence(filepath)
                s, e = self.core.media.getFrameRangeFromSequence(files)
                if s and e and s != "?" and e != "?":
                    start = s
                    end = e

        if start is not None:
            filepath += " %s-%s" % (start, end)

        if self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user"):
            filepath = self.makePathRelative(filepath)

        read_node = nuke.createNode("Read", inpanel=False)
        read_node["file"].fromUserText(filepath)
        return read_node

    @err_catcher(name=__name__)
    def nukeImportSource(self, origin):
        sourceData = origin.compGetImportSource()

        for i in sourceData:
            filePath = i[0]
            firstFrame = i[1]
            lastFrame = i[2]
            if self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user"):
                filePath = self.makePathRelative(filePath)

            node = nuke.createNode(
                "Read",
                "file \"%s\"" % filePath,
                False,
            )
            if firstFrame is not None:
                node.knob("first").setValue(firstFrame)
            if lastFrame is not None:
                node.knob("last").setValue(lastFrame)

    @err_catcher(name=__name__)
    def nukeImportPasses(self, origin):
        sourceData = origin.compGetImportPasses()

        for i in sourceData:
            filePath = i[0]
            firstFrame = i[1]
            lastFrame = i[2]
            if self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user"):
                filePath = self.makePathRelative(filePath)

            node = nuke.createNode(
                "Read",
                "file \"%s\"" % filePath,
                False,
            )
            if firstFrame is not None:
                node.knob("first").setValue(firstFrame)
            if lastFrame is not None:
                node.knob("last").setValue(lastFrame)

    @err_catcher(name=__name__)
    def nukeLayout(self, origin):
        if nuke.env["nc"]:
            msg = "This feature is disabled because of the scripting limitations in Nuke non-commercial."
            self.core.popup(msg)
            return

        allExistingNodes = nuke.allNodes()
        try:
            allBBx = max([node.xpos() for node in allExistingNodes])
        except:
            allBBx = 0

        self.nukeYPos = 0
        xOffset = 200
        nukeXPos = allBBx + xOffset
        nukeSetupWidth = 950
        nukeSetupHeight = 400
        nukeYDistance = 700
        nukeBeautyYDistance = 500
        nukeBackDropFontSize = 100
        self.nukeIdxNode = None
        passFolder = os.path.dirname(os.path.dirname(origin.seq[0])).replace("\\", "/")

        if not os.path.exists(passFolder):
            return

        beautyTriggers = ["beauty", "rgb", "rgba"]
        componentsTriggers = [
            "ls",
            "select",
            "gi",
            "spec",
            "refr",
            "refl",
            "light",
            "lighting",
            "highlight",
            "diff",
            "diffuse",
            "emission",
            "sss",
            "vol",
        ]
        masksTriggers = ["mm", "mask", "puzzleMatte", "matte", "puzzle"]

        beautyPass = []
        componentPasses = []
        maskPasses = []
        utilityPasses = []

        self.maskNodes = []
        self.utilityNodes = []

        passes = [
            x
            for x in os.listdir(passFolder)
            if x[-5:] not in ["(mp4)", "(jpg)", "(png)"]
            and os.path.isdir(os.path.join(passFolder, x))
            and len(os.listdir(os.path.join(passFolder, x))) > 0
        ]

        passesBeauty = []
        passesComponents = []
        passesMasks = []
        passesUtilities = []

        for curPass in passes:
            assigned = False

            for trigger in beautyTriggers:
                if trigger in curPass.lower():
                    passesBeauty.append(curPass)
                    assigned = True
                    break

            if assigned:
                continue

            for trigger in componentsTriggers:
                if trigger in curPass.lower():
                    passesComponents.append(curPass)
                    assigned = True
                    break

            if assigned:
                continue

            for trigger in masksTriggers:
                if trigger in curPass.lower():
                    passesMasks.append(curPass)
                    assigned = True
                    break

            if assigned:
                continue

            passesUtilities.append(curPass)

        passes = passesBeauty + passesComponents + passesMasks + passesUtilities
        maskNum = 0
        utilsNum = 0

        for curPass in passes:
            curPassPath = os.path.join(passFolder, curPass)
            curPassName = os.listdir(curPassPath)[0].split(".")[0]

            if len(os.listdir(curPassPath)) > 1:
                if (
                    origin.pstart is None
                    or origin.pend is None
                    or origin.pstart == "?"
                    or origin.pend == "?"
                ):
                    self.core.popup(origin.pstart)
                    return

                firstFrame = origin.pstart
                lastFrame = origin.pend

                increment = "####"
                curPassFormat = os.listdir(curPassPath)[0].split(".")[-1]

                filePath = os.path.join(
                    passFolder,
                    curPass,
                    ".".join([curPassName, increment, curPassFormat]),
                ).replace("\\", "/")
            else:
                filePath = os.path.join(
                    curPassPath, os.listdir(curPassPath)[0]
                ).replace("\\", "/")
                firstFrame = 0
                lastFrame = 0

            # createPasses
            # beauty
            if curPass in passesBeauty:
                self.createBeautyPass(
                    origin,
                    filePath,
                    firstFrame,
                    lastFrame,
                    curPass,
                    nukeXPos,
                    nukeSetupWidth,
                    nukeBeautyYDistance,
                    nukeBackDropFontSize,
                )

            # components
            elif curPass in passesComponents:
                self.createComponentPass(
                    origin,
                    filePath,
                    firstFrame,
                    lastFrame,
                    curPass,
                    nukeXPos,
                    nukeSetupWidth,
                    nukeSetupHeight,
                    nukeBackDropFontSize,
                    nukeYDistance,
                )

            # masks
            elif curPass in passesMasks:
                maskNum += 1
                self.createMaskPass(
                    origin,
                    filePath,
                    firstFrame,
                    lastFrame,
                    nukeXPos,
                    nukeSetupWidth,
                    maskNum,
                )

            # utility
            elif curPass in passesUtilities:
                utilsNum += 1
                self.createUtilityPass(
                    origin,
                    filePath,
                    firstFrame,
                    lastFrame,
                    nukeXPos,
                    nukeSetupWidth,
                    utilsNum,
                )

        # maskbackdrop
        if len(self.maskNodes) > 0:
            bdX = min([node.xpos() for node in self.maskNodes])
            bdY = min([node.ypos() for node in self.maskNodes])
            bdW = (
                max([node.xpos() + node.screenWidth() for node in self.maskNodes]) - bdX
            )
            bdH = (
                max([node.ypos() + node.screenHeight() for node in self.maskNodes])
                - bdY
            )

            # backdrop boundry offsets
            left, top, right, bottom = (-160, -135, 160, 80)

            # boundry offsets
            bdX += left
            bdY += top
            bdW += right - left
            bdH += bottom - top

            # createbackdrop
            maskBackdropColor = int("%02x%02x%02x%02x" % (255, 125, 125, 1), 16)
            backDrop = nuke.nodes.BackdropNode(
                xpos=bdX,
                bdwidth=bdW,
                ypos=bdY,
                bdheight=bdH,
                tile_color=maskBackdropColor,
                note_font_size=nukeBackDropFontSize,
                label="<center><b>" + "Masks" + "</b><c/enter>",
            )

        # utilitybackdrop
        if len(self.utilityNodes) > 0:
            bdX = min([node.xpos() for node in self.utilityNodes])
            bdY = min([node.ypos() for node in self.utilityNodes])
            bdW = (
                max([node.xpos() + node.screenWidth() for node in self.utilityNodes])
                - bdX
            )
            bdH = (
                max([node.ypos() + node.screenHeight() for node in self.utilityNodes])
                - bdY
            )

            # backdrop boundry offsets
            left, top, right, bottom = (-160, -135, 160, 80)

            # boundry offsets
            bdX += left
            bdY += top
            bdW += right - left
            bdH += bottom - top

            # createbackdrop
            maskBackdropColor = int("%02x%02x%02x%02x" % (125, 255, 125, 1), 16)
            backDrop = nuke.nodes.BackdropNode(
                xpos=bdX,
                bdwidth=bdW,
                ypos=bdY,
                bdheight=bdH,
                tile_color=maskBackdropColor,
                note_font_size=nukeBackDropFontSize,
                label="<center><b>" + "Utilities" + "</b><c/enter>",
            )

    @err_catcher(name=__name__)
    def createBeautyPass(
        self,
        origin,
        filePath,
        firstFrame,
        lastFrame,
        curPass,
        nukeXPos,
        nukeSetupWidth,
        nukeBeautyYDistance,
        nukeBackDropFontSize,
    ):

        curReadNode = nuke.createNode(
            "Read",
            'file "%s" first %s last %s origfirst %s origlast %s'
            % (filePath, firstFrame, lastFrame, firstFrame, lastFrame),
            False,
        )

        nodeArray = [curReadNode]

        # backdropcolor
        r = (float(random.randint(30 + int((self.nukeYPos / 3) % 3), 80))) / 100
        g = (float(random.randint(20 + int((self.nukeYPos / 3) % 3), 80))) / 100
        b = (float(random.randint(15 + int((self.nukeYPos / 3) % 3), 80))) / 100
        hexColour = int("%02x%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255), 1), 16)

        # positions
        curReadNodeWidth = int(curReadNode.screenWidth() * 0.5 - 6)
        curReadNodeHeight = int(curReadNode.screenHeight() * 0.5 - 3)

        curReadNode.setYpos(self.nukeYPos + curReadNodeHeight)
        curReadNode.setXpos(nukeXPos + nukeSetupWidth)

        # backdrop boundries
        bdX = min([node.xpos() for node in nodeArray])
        bdY = min([node.ypos() for node in nodeArray])
        bdW = max([node.xpos() + node.screenWidth() for node in nodeArray]) - bdX
        bdH = max([node.ypos() + node.screenHeight() for node in nodeArray]) - bdY

        # backdrop boundry offsets
        left, top, right, bottom = (-160, -135, 160, 80)

        # boundry offsets
        bdX += left
        bdY += top
        bdW += right - left
        bdH += bottom - top

        # createbackdrop
        backDrop = nuke.nodes.BackdropNode(
            xpos=bdX,
            bdwidth=bdW,
            ypos=bdY,
            bdheight=bdH,
            tile_color=hexColour,
            note_font_size=nukeBackDropFontSize,
            label="<center><b>" + curPass + "</b><c/enter>",
        )

        # increment position
        self.nukeYPos += nukeBeautyYDistance

        # current nukeIdxNode
        self.nukeIdxNode = curReadNode

    @err_catcher(name=__name__)
    def createComponentPass(
        self,
        origin,
        filePath,
        firstFrame,
        lastFrame,
        curPass,
        nukeXPos,
        nukeSetupWidth,
        nukeSetupHeight,
        nukeBackDropFontSize,
        nukeYDistance,
    ):

        curReadNode = nuke.createNode(
            "Read",
            'file "%s" first %s last %s origfirst %s origlast %s'
            % (filePath, firstFrame, lastFrame, firstFrame, lastFrame),
            False,
        )
        mergeNode1 = nuke.createNode("Merge", "operation difference", False)
        dotNode = nuke.createNode("Dot", "", False)
        dotNodeCorner = nuke.createNode("Dot", "", False)
        mergeNode2 = nuke.createNode("Merge", "operation plus", False)

        nodeArray = [curReadNode, dotNode, mergeNode1, mergeNode2, dotNodeCorner]

        # positions
        curReadNode.setYpos(self.nukeYPos)
        curReadNode.setXpos(nukeXPos)

        curReadNodeWidth = int(curReadNode.screenWidth() * 0.5 - 6)
        curReadNodeHeight = int(curReadNode.screenHeight() * 0.5 - 3)

        mergeNode1.setYpos(self.nukeYPos + curReadNodeHeight)
        mergeNode1.setXpos(nukeXPos + nukeSetupWidth)

        dotNode.setYpos(
            self.nukeYPos + curReadNodeHeight + int(curReadNode.screenWidth() * 0.7)
        )
        dotNode.setXpos(nukeXPos + curReadNodeWidth)

        dotNodeCorner.setYpos(self.nukeYPos + nukeSetupHeight)
        dotNodeCorner.setXpos(nukeXPos + curReadNodeWidth)

        mergeNode2.setYpos(self.nukeYPos + nukeSetupHeight - 4)
        mergeNode2.setXpos(nukeXPos + nukeSetupWidth)

        # #inputs
        mergeNode1.setInput(1, curReadNode)
        dotNode.setInput(0, curReadNode)
        dotNodeCorner.setInput(0, dotNode)
        mergeNode2.setInput(1, dotNodeCorner)
        mergeNode2.setInput(0, mergeNode1)

        if self.nukeIdxNode != None:
            mergeNode1.setInput(0, self.nukeIdxNode)

        # backdrop boundry offsets
        left, top, right, bottom = (-10, -125, 100, 50)

        # backdropcolor
        r = (float(random.randint(30 + int((self.nukeYPos / 3) % 3), 80))) / 100
        g = (float(random.randint(20 + int((self.nukeYPos / 3) % 3), 80))) / 100
        b = (float(random.randint(15 + int((self.nukeYPos / 3) % 3), 80))) / 100
        hexColour = int("%02x%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255), 1), 16)

        # backdrop boundries
        bdX = min([node.xpos() for node in nodeArray])
        bdY = min([node.ypos() for node in nodeArray])
        bdW = max([node.xpos() + node.screenWidth() for node in nodeArray]) - bdX
        bdH = max([node.ypos() + node.screenHeight() for node in nodeArray]) - bdY

        # boundry offsets
        bdX += left
        bdY += top
        bdW += right - left
        bdH += bottom - top

        # createbackdrop
        backDrop = nuke.nodes.BackdropNode(
            xpos=bdX,
            bdwidth=bdW,
            ypos=bdY,
            bdheight=bdH,
            tile_color=hexColour,
            note_font_size=nukeBackDropFontSize,
            label="<b>" + curPass + "</b>",
        )

        # increment position
        self.nukeYPos += nukeYDistance

        # current nukeIdxNode
        self.nukeIdxNode = mergeNode2

    @err_catcher(name=__name__)
    def createMaskPass(
        self, origin, filePath, firstFrame, lastFrame, nukeXPos, nukeSetupWidth, idx
    ):

        curReadNode = nuke.createNode(
            "Read",
            'file "%s" first %s last %s origfirst %s origlast %s'
            % (filePath, firstFrame, lastFrame, firstFrame, lastFrame),
            False,
        )
        curReadNode.setYpos(0)
        curReadNode.setXpos(nukeXPos + nukeSetupWidth + 500 + idx * 350)

        val = 0.5
        r = int("%02x%02x%02x%02x" % (int(val * 255), 0, 0, 1), 16)
        g = int("%02x%02x%02x%02x" % (0, int(val * 255), 0, 1), 16)
        b = int("%02x%02x%02x%02x" % (0, 0, int(val * 255), 1), 16)

        created = False
        if "cryptomatte" in os.path.basename(filePath):
            try:
                cmatte = nuke.createNode("Cryptomatte", inpanel=False)
            except:
                pass
            else:
                created = True
                cmatte.setInput(0, curReadNode)
                self.maskNodes.append(curReadNode)
                self.maskNodes.append(cmatte)

        if not created:
            redShuffle = nuke.createNode(
                "Shuffle", "red red blue red green red alpha red", inpanel=False
            )
            greenShuffle = nuke.createNode(
                "Shuffle", "red green blue green green green alpha green", inpanel=False
            )
            blueShuffle = nuke.createNode(
                "Shuffle", "red blue blue blue green blue alpha blue", inpanel=False
            )

            redShuffle["tile_color"].setValue(r)
            greenShuffle["tile_color"].setValue(g)
            blueShuffle["tile_color"].setValue(b)

            redShuffle.setInput(0, curReadNode)
            greenShuffle.setInput(0, curReadNode)
            blueShuffle.setInput(0, curReadNode)

            redShuffle.setXpos(redShuffle.xpos() - 110)
            # 	greenShuffle.setXpos(greenShuffle.xpos()-110)
            blueShuffle.setXpos(blueShuffle.xpos() + 110)

            self.maskNodes.append(curReadNode)
            self.maskNodes.append(redShuffle)
            self.maskNodes.append(greenShuffle)
            self.maskNodes.append(blueShuffle)

    @err_catcher(name=__name__)
    def createUtilityPass(
        self, origin, filePath, firstFrame, lastFrame, nukeXPos, nukeSetupWidth, idx
    ):

        curReadNode = nuke.createNode(
            "Read",
            'file "%s" first %s last %s origfirst %s origlast %s'
            % (filePath, firstFrame, lastFrame, firstFrame, lastFrame),
            False,
        )
        curReadNode.setYpos(0)
        curReadNode.setXpos(nukeXPos + nukeSetupWidth + 500 + idx * 100)
        try:
            curReadNode.setXpos(
                curReadNode.xpos()
                + self.maskNodes[-1].xpos()
                - nukeXPos
                - nukeSetupWidth
            )
        except:
            pass

        self.utilityNodes.append(curReadNode)

    @err_catcher(name=__name__)
    def postSaveScene(self, origin, filepath, versionUp, comment, isPublish, details):
        """
        origin:     PrismCore instance
        filepath:   The filepath of the scenefile, which was saved
        versionUp:  (bool) True if this save increments the version of that scenefile
        comment:    The string, which is used as the comment for the scenefile. Empty string if no comment was given.
        isPublish:  (bool) True if this save was triggered by a publish
        """
        self.refreshWriteNodes()

    @err_catcher(name=__name__)
    def postBuildScene(self, **kwargs):
        self.core.appPlugin.refreshOcio()
        sbData = self.core.getConfig("sceneBuilding", config="project")
        details = kwargs["entity"].copy()
        details["department"] = kwargs["department"]
        details["task"] = kwargs["task"]
        if "nuke_load_media" in sbData:
            if self.core.entities.doesContextMatchTaskFilters(sbData["nuke_load_media"], details):
                self.buildScene()

    @err_catcher(name=__name__)
    def buildScene(self):
        entity = self.core.getCurrentScenefileData()
        idfs = self.core.mediaProducts.getIdentifiersFromEntity(entity)
        plates = []

        import fnmatch
        plateNames = [name.strip().lower() for name in os.getenv("PRISM_NUKE_LOAD_MEDIA", "plate*, light*").split(",")]
        for idf in idfs:
            group = (self.core.mediaProducts.getGroupFromIdentifier(idf) or "").lower()
            idfName = idf["identifier"].lower()
            valid = False
            for plateName in plateNames:
                if fnmatch.fnmatch(group, plateName) or fnmatch.fnmatch(idfName, plateName):
                    valid = True
                    break

            if not valid:
                continue

            version = self.core.mediaProducts.getVersion(entity, idf["identifier"], mediaType=idf.get("mediaType"))
            if not version:
                continue

            platePath = self.core.mediaProducts.getFileFromVersion(version, findExisting=True)
            if platePath:
                plates.append(platePath)

        readNodes = []
        for idx, plate in enumerate(plates):
            readNode = self.core.appPlugin.importMedia(plate)
            readNode.setXpos(idx * 200)
            readNode.setYpos(0)
            readNodes.append(readNode)

        useWritePrism = self.core.getConfig("nuke", "useWritePrism", dft=False, config="user")
        if useWritePrism:
            writeType = "WritePrism"
        else:
            writeType = "Write"

        writeNode = nuke.createNode(writeType)
        if readNodes:
            writeNode.setInput(0, readNodes[0])

        writeNode.setXpos(0)
        writeNode.setYpos(300)
        viewers = [node for node in nuke.allNodes() if node.Class() == "Viewer"]
        if not viewers:
            viewer = nuke.createNode("Viewer")
            viewers = [viewer]

        viewers[0].setInput(0, writeNode)
        viewers[0].setYpos(400)

    @err_catcher(name=__name__)
    def refreshWriteNodes(self):
        for node in nuke.allNodes():
            nodeClass = node.Class()
            if nodeClass == "WritePrism":
                node.knob("refresh").execute()
            elif nodeClass == "Write":
                if node.knob("tab_prism") and node.knob("refresh"):
                    node.knob("refresh").execute()

    @err_catcher(name=__name__)
    def onUserNodeCreated(self):
        node = nuke.thisNode()
        if not node:
            return

        try:
            nodeClass = node.Class()
        except:
            pass

        try:
            group = nuke.thisGroup()
        except:
            group = None

        addWriteKnobs = os.environ.get("PRISM_NUKE_WRITE_ADD_KNOBS", "1") == "1"
        if nodeClass == "Write" and (not group or group.Class() != "WritePrism") and addWriteKnobs:
            if not node.knob("tab_prism"):
                self.addUiToWriteNode(node)

            self.updateNodeUI("write", node)
            self.getOutputPath(node)

            cmd = "try:\n\tpcore.getPlugin(\"Nuke\").updateNodeUI(\"write\", nuke.toNode(nuke.thisNode().fullName().rsplit(\".\", 1)[0]))\nexcept:\n\tpass"
            node.knob("knobChanged").setValue(cmd)
            idfKnob = node.knob("identifier")
            if idfKnob and not idfKnob.value():
                idf = self.core.getCurrentScenefileData().get("task")
                if idf:
                    idfKnob.setValue(idf)
                    self.getOutputPath(node)

        elif nodeClass == "Read" and os.getenv("PRISM_NUKE_READ_ADD_KNOBS", "1") == "1":
            if not node.knob("tab_prism"):
                self.addUiToReadNode(node)

            self.updateNodeUI("read", node)
            cmd = "try:\n\tpcore.getPlugin(\"Nuke\").updateNodeUI(\"read\", nuke.toNode(nuke.thisNode().fullName().rsplit(\".\", 1)[0]))\nexcept:\n\tpass"
            node.knob("knobChanged").setValue(cmd)

        kwargs = {"origin": self, "node": node}
        self.core.callback("onNukeNodeCreated", **kwargs)

    @err_catcher(name=__name__)
    def onRootKnobChanged(self):
        knob = nuke.thisKnob()
        if knob.name() != "gsv":
            return

        self.refreshGSVs()

    @err_catcher(name=__name__)
    def addUiToWriteNode(self, node):
        knobs = ["identifier", "comment", "location", "fileName", "refresh", "startRender", "showPrevVersions", "submitJob", "prevFileName", "openDir"]
        for knob in knobs:
            k = node.knob(knob)
            if k:
                node.removeKnob(k)

        tab = node.knob("tab_prism")
        if not tab:
            tab = nuke.Tab_Knob('tab_prism', 'Prism')
            node.addKnob(tab)

        knobIdf = nuke.EvalString_Knob("identifier", "identifier")
        node.addKnob(knobIdf)
        knobComment = nuke.EvalString_Knob("comment", "comment (optional)")
        node.addKnob(knobComment)
        knobVersion = nuke.Int_Knob("renderversion", "Version")
        knobVersion.setValue(1)
        node.addKnob(knobVersion)
        knobVersion.setEnabled(False)
        knobAutoVersion = nuke.Boolean_Knob("autoversion", "auto")
        node.addKnob(knobAutoVersion)
        knobAutoVersion.setValue(1)
        knobPrevVersions = nuke.PyScript_Knob("showPrevVersions", "Show Previous Versions...", "pcore.appPlugin.showPrevVersions(nuke.thisNode())")
        node.addKnob(knobPrevVersions)
        knobLoc = nuke.Enumeration_Knob("location", "location", ["                              "])
        node.addKnob(knobLoc)
        knobDiv = nuke.Text_Knob("")
        node.addKnob(knobDiv)
        knobFilepath = nuke.EvalString_Knob("fileName", "filepath")
        knobFilepath.setValue("FileNotInPipeline")
        node.addKnob(knobFilepath)
        knobRefresh = nuke.PyScript_Knob("refresh", "Refresh", "pcore.appPlugin.getOutputPath(nuke.thisNode())")
        knobRefresh.setFlag(nuke.STARTLINE)
        node.addKnob(knobRefresh)
        knobDiv = nuke.Text_Knob("")
        node.addKnob(knobDiv)
        knobRender = nuke.PyScript_Knob("startRender", "Render", "pcore.appPlugin.startRender(nuke.thisNode())")
        node.addKnob(knobRender)
        knobSubmit = nuke.Boolean_Knob("submitJob", "Submit Job")
        node.addKnob(knobSubmit)
        knobPrev = nuke.Text_Knob("prevFileName", "previous filepath", "-")
        node.addKnob(knobPrev)
        knobOpen = nuke.PyScript_Knob("openDir", "Open In...", "pcore.appPlugin.openInClicked(nuke.thisNode())")
        knobOpen.setFlag(nuke.STARTLINE)
        node.addKnob(knobOpen)
        knobOpen = nuke.PyScript_Knob("createRead", "Create Read", "pcore.appPlugin.createRead(nuke.thisNode())")
        node.addKnob(knobOpen)

        node.knob("create_directories").setValue(True)
        node.knob("file").setValue("[value fileName]")
        node.knob("file_type").setValue("exr")
        node.knob("beforeRender").setValue("try: pcore.appPlugin.getOutputPath(nuke.thisNode(), render=True)\nexcept: pass")
        node.knob("afterRender").setValue("try: pcore.appPlugin.finishedRendering(nuke.thisNode())\nexcept: pass")

    @err_catcher(name=__name__)
    def addUiToReadNode(self, node):
        knobs = ["identifier", "comment", "location", "fileName", "refresh", "startRender", "showPrevVersions", "submitJob", "prevFileName", "openDir"]
        for knob in knobs:
            k = node.knob(knob)
            if k:
                node.removeKnob(k)

        tab = node.knob("tab_prism")
        if not tab:
            tab = nuke.Tab_Knob('tab_prism', 'Prism')
            node.addKnob(tab)

        knobFilepath = nuke.Text_Knob("fileName", "File", "")
        node.addKnob(knobFilepath)
        knobBrowse = nuke.PyScript_Knob("browse", "Browse...", "pcore.appPlugin.readNode_onBrowseClicked(nuke.thisNode())")
        knobBrowse.setFlag(nuke.STARTLINE)
        node.addKnob(knobBrowse)
        knobExplorer = nuke.PyScript_Knob("openExplorer", "Open In Explorer...", "pcore.appPlugin.readNode_onOpenInClicked(nuke.thisNode())")
        node.addKnob(knobExplorer)

    @err_catcher(name=__name__)
    def readGizmoCreated(self):
        pass

    @err_catcher(name=__name__)
    def writeGizmoCreated(self):
        group = nuke.thisGroup()
        self.getOutputPath(nuke.thisNode(), group)

        cmd = "try:\n\tpcore.getPlugin(\"Nuke\").updateNodeUI(\"writePrism\", nuke.toNode(nuke.thisNode().fullName().rsplit(\".\", 1)[0]))\nexcept:\n\tpass"
        nuke.thisNode().node("WritePrismBase").knob("knobChanged").setValue(cmd)
        idfKnob = nuke.thisNode().knob("identifier")
        if idfKnob and not idfKnob.value():
            idf = self.core.getCurrentScenefileData().get("task")
            if idf:
                idfKnob.setValue(idf)
                self.getOutputPath(nuke.thisNode(), group)

        val = group.knob("prevFileName").value()
        if not val or val == "-":
            knobe = group.knob("prevFileNameEdit")
            if knobe:
                vale = knobe.value()
                if vale and vale != val:
                    group.knob("prevFileName").setValue(vale)

        kwargs = {"origin": self, "node": nuke.thisNode()}
        self.core.callback("onWriteGizmoCreated", **kwargs)

    @err_catcher(name=__name__)
    def updateNodeUI(self, nodeType, node):
        if not nuke.env.get("gui"):
            return

        if nodeType in ["writePrism", "write"]:
            locations = self.core.paths.getRenderProductBasePaths()
            locNames = list(locations.keys())
            try:
                node.knob("location").setValues(locNames)
            except:
                pass

            if nodeType == "WritePrismBase":
                base = node.node("WritePrismBase")
                if base:
                    knobs = base.knobs()
                    try:
                        node.knobs()["datatype"].setVisible(bool(knobs.get("datatype")))
                    except:
                        pass

                    try:
                        node.knobs()["compression"].setVisible(bool(knobs.get("compression")))
                    except:
                        pass

            knob = nuke.thisKnob()
            if knob and knob.name() in ["identifier", "location", "renderversion", "autoversion"]:
                self.getOutputPath(node)

            if knob and knob.name() == "autoversion":
                nuke.thisNode().knob("renderversion").setEnabled(not knob.value())

        elif nodeType in ["read"]:
            try:
                if node.knob("file"):
                    node.knob("fileName").setValue(node.knob("file").value())
            except:
                pass

    @err_catcher(name=__name__)
    def createRead(self, node, group=None):
        if group:
            group.end()

        if not group:
            group = node

        filepath = group.knob("prevFileName").value()
        if not os.path.exists(os.path.dirname(filepath)):
            filepath = group.knob("fileName").value()
            if not os.path.exists(os.path.dirname(filepath)):
                context = self.core.paths.getRenderProductData(filepath, mediaType="2drenders")
                intVersion = self.core.products.getIntVersionFromVersionName(context.get("version") or "")
                if intVersion is not None:
                    context["version"] = self.core.versionFormat % (intVersion - 1)
                    filepath = self.core.mediaProducts.generateMediaProductPath(
                        entity=context,
                        task=context["identifier"],
                        version=context["version"],
                        extension=context.get("extension", ""),
                        mediaType="2drenders",
                        comment=context.get("comment", ""),
                        location=context.get("location", "global"),
                        framePadding="#",
                    )

                filepath = self.expandEnvVarsInFilepath(filepath)
                if not os.path.exists(os.path.dirname(filepath)):
                    self.core.popup("Folder doesn't exist: %s" % os.path.dirname(filepath))
                    return

        seqs = nuke.getFileNameList(os.path.dirname(filepath))
        if not seqs:
            self.core.popup("No renderings exist in current filepath.")
            return

        if "#" not in os.path.basename(filepath):
            base, ext = os.path.splitext(filepath)
            filepath = base + "#" + ext

        pattern = os.path.basename(filepath).replace("#", ".*")
        useRel = self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user")
        for seq in seqs:
            if re.match(pattern, seq):
                readNode = nuke.createNode('Read')
                filepath = os.path.join(os.path.dirname(filepath), seq)
                if useRel:
                    filepath = self.makePathRelative(filepath)

                readNode.knob('file').fromUserText(filepath)
                break
        else:
            self.core.popup("No media files found.\nMake sure the rendering is completed and try again.")

    @err_catcher(name=__name__)
    def sm_render_getDeadlineParams(self, origin, dlParams, homeDir):
        dlParams["jobInfoFile"] = os.path.join(homeDir, "temp", "nuke_submit_info.job")
        dlParams["pluginInfoFile"] = os.path.join(
            homeDir, "temp", "nuke_plugin_info.job"
        )

        dlParams["jobInfos"]["Plugin"] = "Nuke"
        dlParams["jobInfos"]["Comment"] = "Prism-Submission-Nuke_ImageRender"

        if hasattr(self, "submitter") and getattr(self.submitter, "useBatchname", False):
            dlParams["jobInfos"]["BatchName"] = dlParams["jobInfos"]["Name"]

        self.core.getPlugin("Deadline").addEnvironmentItem(
            dlParams["jobInfos"],
            "PRISM_NUKE_TERMINAL_FILES",
            os.path.abspath(__file__)
        )
        self.core.getPlugin("Deadline").addEnvironmentItem(
            dlParams["jobInfos"],
            "PRISM_NUKE_USE_RELATIVE_PATHS",
            self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user")
        )
        self.core.getPlugin("Deadline").addEnvironmentItem(
            dlParams["jobInfos"],
            "PRISM_JOB",
            os.getenv("PRISM_JOB", "")
        )

        dlParams["jobInfos"]["OutputFilename0"] = self.expandEnvVarsInFilepath(dlParams["jobInfos"]["OutputFilename0"])
        dlParams["pluginInfos"]["Version"] = self.getAppVersion(origin).split("v")[0]
        dlParams["pluginInfos"]["OutputFilePath"] = os.path.split(
            dlParams["jobInfos"]["OutputFilename0"]
        )[0]
        base, ext = os.path.splitext(
            os.path.basename(dlParams["jobInfos"]["OutputFilename0"])
        )
        dlParams["pluginInfos"]["OutputFilePrefix"] = base
        dlParams["pluginInfos"]["BatchMode"] = True
        dlParams["pluginInfos"]["BatchModeIsMovie"] = ext in self.core.media.videoFormats
        dlParams["pluginInfos"]["WriteNode"] = origin.node.fullName()

    @err_catcher(name=__name__)
    def openFarmSubmitter(self, node, group=None, dependencies=None):
        if not group:
            group = node

        taskName = self.getIdentifierFromNode(group)
        if not taskName:
            self.core.popup("Please choose an identifier")
            return

        fileName = self.getOutputPath(node, group)
        if fileName == "FileNotInPipeline":
            self.core.showFileNotInProjectWarning(title="Warning")
            return

        settings = {
            "outputName": fileName,
            "node": node,
            "group": group,
            "identifier": taskName,
        }
        scenefile = self.core.getCurrentFileName()
        kwargs = {
            "state": self,
            "scenefile": scenefile,
            "settings": settings,
        }

        result = self.core.callback("onNukeOpenFarmSubmitter", **kwargs)
        for res in result:
            if isinstance(res, dict) and res.get("cancel", False):
                return [
                    "Nuke Submitter - error - %s" % res.get("details", "onNukeOpenFarmSubmitter hook returned False")
                ]

        sm = self.core.getStateManager()
        state = sm.createState("ImageRender")
        state.ui.mediaType = "2drenders"
        if not state.ui.cb_manager.count():
            msg = "No farm submitter is installed."
            self.core.popup(msg)
            return

        if hasattr(self, "submitter") and self.submitter.isVisible():
            self.submitter.close()

        state.ui.node = node
        state.ui.group = group
        self.submitter = Farm_Submitter(self, state, dependencies=dependencies)
        self.submitter.loadSettings()
        state.ui.chb_version.setChecked(False)
        state.ui.setTaskname(self.getIdentifierFromNode(group))
        fmt = "." + group.knob("file_type").value()
        if state.ui.cb_format.findText(fmt) == -1:
            state.ui.cb_format.addItem(fmt)

        state.ui.setFormat(fmt)
        if self.core.uiAvailable:
            self.submitter.show()
        else:
            self.submitter.submit()

    @err_catcher(name=__name__)
    def openInClicked(self, node, group=None):
        if not group:
            group = node

        path = group.knob("prevFileName").value()
        if path == "None":
            return

        path = self.expandEnvVarsInFilepath(path)
        menu = QMenu()

        act_play = QAction("Play")
        act_play.triggered.connect(lambda: self.core.media.playMediaInExternalPlayer(path))
        menu.addAction(act_play)

        act_browser = QAction("Open in Media Browser")
        act_browser.triggered.connect(lambda: self.openInMediaBrowser(path))
        menu.addAction(act_browser)

        act_open = QAction("Open in explorer")
        act_open.triggered.connect(lambda: self.core.openFolder(path))
        menu.addAction(act_open)

        act_copy = self.core.getCopyAction(path)
        menu.addAction(act_copy)

        menu.exec_(QCursor.pos())

    @err_catcher(name=__name__)
    def openInMediaBrowser(self, path):
        self.core.projectBrowser()
        self.core.pb.showTab("Media")
        data = self.core.paths.getRenderProductData(path, mediaType="2drenders")
        self.core.pb.mediaBrowser.showRender(entity=data, identifier=data.get("identifier", "") + " (2d)", version=data.get("version"))

    @err_catcher(name=__name__)
    def sm_getExternalFiles(self, origin):
        import re
        from collections import defaultdict
        prevSelectedNodes = nuke.selectedNodes() or []

        found = defaultdict(set)
        file_knob_names = {
            "file", "files", "filename", "proxy", "proxy_input", "root",
            "clip", "frame", "file0", "file1", "file2", "gizmo", "font", "icon"
        }

        [n.setSelected(False) for n in nuke.selectedNodes()]
        if os.getenv("PRISM_NUKE_TRACK_UNCONNECTED_DEPENDENCIES", "1") == "1":
            nodes = nuke.allNodes(recurseGroups=True)
        else:
            for node in nuke.allNodes(recurseGroups=True):
                if node.Class() == "Write" or node.Class() == "WritePrism":
                    node.setSelected(True)

            nuke.selectConnectedNodes()
            nodes = nuke.selectedNodes()

        for node in nodes:
            if node.Class() == "Write" or node.Class() == "WritePrism":
                continue

            for kname, knob in node.knobs().items():
                if kname.lower() in file_knob_names or knob.Class() in ("File_Knob", "InputFile_Knob"):
                    try:
                        val = knob.getValue()
                    except Exception:
                        # fallback: try to get as string
                        try:
                            val = str(knob)
                        except Exception:
                            val = None
                    if val is None:
                        continue

                    # knob.getValue may return list/tuple for multi-file knobs
                    if isinstance(val, (list, tuple)):
                        vals = val
                    else:
                        vals = [val]

                    for v in vals:
                        if not v:
                            continue
                        # try to evaluate/expand expressions: nuke.filename? nuke.toNode?
                        # nuke.knob(value) may contain expressions. nuke.filename(node) gives filename for Read nodes:
                        # Try some special cases:
                        if hasattr(node, "knob") and kname == "file":
                            # Try nuke.filename for read nodes
                            try:
                                resolved = nuke.filename(node)
                            except Exception:
                                resolved = v
                        else:
                            resolved = nuke.expression(v) if isinstance(v, str) and "$" in v else v

                        resolved = os.path.expanduser(os.path.expandvars(str(resolved)))
                        resolved = resolved.replace('\\', os.sep)
                        found['all'].add(resolved)

                        if resolved.endswith(('.gizmo', '.nk')):
                            found['gizmos'].add(resolved)
                        elif resolved.endswith(('.py',)):
                            found['plugins'].add(resolved)
                        elif resolved.endswith(('.otf', '.ttf')):
                            found['fonts'].add(resolved)
                        elif resolved.endswith(('.ocio', '.icc', '.cube', '.3dl')):
                            found['ocio'].add(resolved)
                        elif re.search(r'\.exr$|\.dpx$|\.jpg$|\.png$|\.tif$|\.tiff$|\.mov$|\.mp4$|\.cin$', resolved.lower()):
                            found['files'].add(resolved)
                        else:
                            found['others'].add(resolved)

        # existence checking
        found['absolute'] = {p for p in found['all'] if os.path.isabs(p)}
        # found['relative'] = {p for p in found['all'] if not os.path.isabs(p)}
        # found['exists'] = {p for p in found['all'] if os.path.exists(p)}
        # found['missing'] = found['all'] - found['exists']
        [n.setSelected(False) for n in nuke.selectedNodes()]
        [n.setSelected(True) for n in prevSelectedNodes]
        return [found['absolute'], []]

    @err_catcher(name=__name__)
    def sm_render_preExecute(self, origin):
        warnings = []
        return warnings

    @err_catcher(name=__name__)
    def sm_render_preSubmit(self, origin, rSettings):
        pass

    @err_catcher(name=__name__)
    def sm_render_undoRenderSettings(self, origin, rSettings):
        pass

    @err_catcher(name=__name__)
    def captureViewportThumbnail(self):
        if "fnFlipbookRenderer" not in globals():
            logger.debug("failed to capture thumbnail because the \"fnFlipbookRenderer\" module isn't available.")
            return

        path = tempfile.NamedTemporaryFile(suffix=".jpg").name
        viewer = nuke.activeViewer()
        if not viewer:
            return

        inputNr = viewer.activeInput()
        if inputNr is None:
            return

        prevSelectedNodes = nuke.selectedNodes() or []

        inputNode = viewer.node().input(inputNr)
        dlg = renderdialog._getFlipbookDialog(inputNode)
        factory = flipbooking.gFlipbookFactory
        names = factory.getNames()
        flipbook = factory.getApplication(names[0])

        fb = PrismRenderedFlipbook(dlg, flipbook)
        self.isRenderingFlipbook = True
        fb.doFlipbook(path.replace("\\", "/"), self.getCurrentFrame())
        self.isRenderingFlipbook = False
        pm = self.core.media.getPixmapFromPath(path)
        try:
            os.remove(path)
        except:
            pass

        [n.setSelected(False) for n in nuke.selectedNodes()]
        [n.setSelected(True) for n in prevSelectedNodes]
        return pm

    @err_catcher(name=__name__)
    def onImportShotsTriggered(self):
        dlg = ShotListDlg(self)
        dlg.w_entities.getPage("Shots").tw_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        dlg.entitiesAdded.connect(self.loadShotsIntoNuke)
        dlg.entitiesInserted.connect(lambda x: callback(x, insert=True))
        dlg.exec_()

    @err_catcher(name=__name__)
    def loadShotsIntoNuke(self, data, origin=None, insert=False):
        node_read = nuke.nodes.Read(name="Shot_Read", xpos=0, ypos=0, file="%{prism.multishot_read}")
        node_switch = nuke.nodes.VariableSwitch(name="Shot_Switch", xpos=0, ypos=400)
        node_switch.connectInput(0, node_read)
        node_write = nuke.nodes.Write(name="Shot_Write", xpos=0, ypos=600, file="%{prism.multishot_write}")
        node_write.connectInput(0, node_switch)

        gsv_knob = nuke.root()["gsv"]

        curShots = self.getShotsFromScene()
        newShotNames = [self.core.entities.getShotName(d) for d in data]
        for newShotName in newShotNames:
            if newShotName not in curShots:
                curShots.append(newShotName)

        if gsv_knob.getGsvValue("prism.shot") is None:
            gsv_knob.setGsvValue("prism.shot", "")

        if gsv_knob.getDataType("prism.shot") != nuke.gsv.DataType.List:
            gsv_knob.setDataType("prism.shot", nuke.gsv.DataType.List)

        gsv_knob.setListOptions("prism.shot", sorted(curShots))
        self.refreshGSVs()

    @err_catcher(name=__name__)
    def refreshGSVs(self):
        try:
            gsv_knob = nuke.root()["gsv"]
        except:
            return

        curShots = self.getShotsFromScene()
        val = gsv_knob.value()
        import copy
        origVal = copy.deepcopy(val)
        if "prism" not in val:
            val["prism"] = {}

        if "shot" not in val["prism"]:
            val["prism"]["shot"] = ""

        if "identifier" not in val["prism"]:
            val["prism"]["identifier"] = ""

        if "version" not in val["prism"]:
            val["prism"]["version"] = ""

        if "aov" not in val["prism"]:
            val["prism"]["aov"] = ""

        shotData = val["prism"]["shot"].split("-")
        if len(shotData) != 2:
            identifiers = []
        else:
            entity = {"type": "shot", "sequence": shotData[0], "shot": shotData[1]}
            identifiers = self.core.mediaProducts.getIdentifierNames(entity)

        if identifiers:
            ctx = entity.copy()
            ctx["identifier"] = val["prism"]["identifier"]
            versions = sorted([version["version"] for version in self.core.mediaProducts.getVersionsFromContext(ctx)], reverse=True)
        else:
            versions = []

        if versions:
            ctx["version"] = val["prism"]["version"]
            if ctx["version"] == "latest":
                ctx["version"] = versions[0]

            aovs = [aov["aov"] for aov in self.core.mediaProducts.getAOVsFromVersion(ctx)]
        else:
            aovs = []

        readpath = ""
        if versions:
            ctx["aov"] = val["prism"]["aov"]
            mediaFiles = self.core.mediaProducts.getFilesFromContext(ctx)
            validFiles = self.core.media.filterValidMediaFiles(mediaFiles)
            if validFiles:
                validFiles = sorted(validFiles, key=lambda x: x if "cryptomatte" not in os.path.basename(x) else "zzz" + x)
                seqFiles = self.core.media.detectSequences(validFiles)
                if seqFiles:
                    readpath = list(seqFiles)[0].replace("\\", "/")

        writepath = self.core.projectPath + "test_write.exr"

        val["prism"]["multishot_read"] = readpath
        val["prism"]["multishot_write"] = writepath
        if val != origVal:
            gsv_knob.setValue(val)

        changed = False
        if gsv_knob.getDataType("prism.shot") != nuke.gsv.DataType.List:
            gsv_knob.setDataType("prism.shot", nuke.gsv.DataType.List)
            gsv_knob.setFavorite("prism.shot", True)

        if gsv_knob.getListOptions("prism.shot") != curShots:
            gsv_knob.setListOptions("prism.shot", curShots)
            changed = True

        if gsv_knob.getDataType("prism.identifier") != nuke.gsv.DataType.List:
            gsv_knob.setDataType("prism.identifier", nuke.gsv.DataType.List)
            gsv_knob.setFavorite("prism.identifier", True)

        if gsv_knob.getListOptions("prism.identifier") != sorted(identifiers):
            gsv_knob.setListOptions("prism.identifier", sorted(identifiers))
            changed = True

        if gsv_knob.getDataType("prism.version") != nuke.gsv.DataType.List:
            gsv_knob.setDataType("prism.version", nuke.gsv.DataType.List)
            gsv_knob.setFavorite("prism.version", True)

        if gsv_knob.getListOptions("prism.version") != ["latest"] + sorted(versions):
            gsv_knob.setListOptions("prism.version", ["latest"] + sorted(versions))
            changed = True

        if gsv_knob.getDataType("prism.aov") != nuke.gsv.DataType.List:
            gsv_knob.setDataType("prism.aov", nuke.gsv.DataType.List)
            gsv_knob.setFavorite("prism.aov", True)

        if gsv_knob.getListOptions("prism.aov") != sorted(aovs):
            gsv_knob.setListOptions("prism.aov", sorted(aovs))
            changed = True

        if changed:
            self.refreshGSVs()

    @err_catcher(name=__name__)
    def getShotsFromScene(self):
        knob = nuke.root()["gsv"]
        return knob.getListOptions("prism.shot")

    @err_catcher(name=__name__)
    def onExportTriggered(self, selectedPaths=None):
        sm = self.core.getStateManager()
        if not sm:
            return

        if not self.core.fileInPipeline():
            self.core.showFileNotInProjectWarning(title="Warning")
            return False

        for state in sm.states:
            if state.ui.className == "NukeExport":
                break
        else:
            state = sm.createState("NukeExport")
            if not state:
                msg = "Failed to create export state. Please contact the support."
                self.core.popup(msg)
                return

        if hasattr(self, "dlg_export"):
            self.dlg_export.close()

        self.dlg_export = ExporterDlg(self, state)
        state.ui.setTaskname("nuke")
        self.dlg_export.show()

    @err_catcher(name=__name__)
    def onStateManagerOpen(self, origin):
        import default_Export
        import default_Export_ui

        class NukeExportClass(QWidget, default_Export_ui.Ui_wg_Export, NukeExport, default_Export.ExportClass):
            def __init__(self):
                QWidget.__init__(self)
                self.setupUi(self)

        origin.loadState(NukeExportClass)

    @err_catcher(name=__name__)
    def sm_export_addObjects(self, origin, objects=None):
        pass

    @err_catcher(name=__name__)
    def sm_export_preExecute(self, origin, startFrame, endFrame):
        warnings = []

        if not nuke.selectedNodes():
            warnings.append(
                [
                    "No nodes selected.",
                    "Select nodes to export.",
                    3,
                ]
            )

        return warnings

    @err_catcher(name=__name__)
    def sm_export_exportAppObjects(
        self,
        origin,
        startFrame,
        endFrame,
        outputName,
    ):
        nuke.nodeCopy(outputName)
        return outputName

    @err_catcher(name=__name__)
    def sm_import_importToApp(self, origin, doImport, update, impFileName):
        fileName = os.path.splitext(os.path.basename(impFileName))
        result = False

        ext = fileName[1].lower()
        if ext in self.plugin.sceneFormats:
            path = impFileName.replace("\\", "/")
            msg = "How do you want to import the nuke script?"
            result = self.core.popupQuestion(msg, buttons=["Paste Nodes", "Livegroup", "Precomp"])
            if result == "Paste Nodes":
                result = nuke.nodePaste(path)
            elif result == "Livegroup":
                liveGroup = nuke.createNode("LiveGroup")
                liveGroup.knob("published").fromScript("1")
                liveGroup.knob("file").setValue(path)
            elif result == "Precomp":
                nuke.createNode("Precomp", "file \"%s\"" % path)

        elif ext in [".obj", ".fbx", ".abc"]:
            path = impFileName.replace("\\", "/")
            node_read = nuke.nodes.ReadGeo2()
            node_read['file'].setValue(path) 
            node_scene = nuke.nodes.Scene(xpos=node_read.xpos() + 10, ypos=node_read.ypos()+200)
            node_render = nuke.nodes.ScanlineRender(xpos=node_read.xpos(), ypos=node_read.ypos()+400)
            node_render.connectInput(1, node_scene)
            node_scene.connectInput(0, node_read)
            result = [node_read]
        else:
            self.core.popup("Format is not supported.")
            return {"result": False, "doImport": doImport}

        return {"result": result, "doImport": doImport}

    @err_catcher(name=__name__)
    def importCamera(self, data, filepath):
        path = filepath.replace("\\", "/")
        node_read = nuke.nodes.Camera3(read_from_file_link=True, file_link=path)
        node_scene = nuke.nodes.Scene(xpos=node_read.xpos()+300, ypos=node_read.ypos())
        node_render = nuke.nodes.ScanlineRender(xpos=node_scene.xpos()-10, ypos=node_read.ypos()+200)
        node_render.connectInput(0, node_read)
        node_render.connectInput(1, node_scene)
        node_scene.connectInput(0, node_read)

    @err_catcher(name=__name__)
    def productSelectorContextMenuRequested(self, origin, widget, pos, menu):
        if widget == origin.tw_versions:
            row = widget.rowAt(pos.y())
            if row != -1:
                pathC = widget.model().columnCount() - 1
                path = widget.model().index(row, pathC).data()
                ext = os.path.splitext(path)[1]
                if ext in [".fbx", ".abc"]:
                    item = origin.tw_identifier.currentItem()
                    data = item.data(0, Qt.UserRole)
                    action = QAction("Import Camera", origin)
                    action.triggered.connect(lambda: self.importCamera(data, filepath=path))
                    for idx, act in enumerate(menu.actions()):
                        if act.text() == "Import":
                            menu.insertAction(menu.actions()[idx+1], action)
                            break
                    else:
                        menu.insertAction(0, action)

    @err_catcher(name=__name__)
    def openMediaVersionsDialog(self):
        if hasattr(self, "dlg_mediaVersions") and self.core.isObjectValid(self.dlg_mediaVersions) and self.dlg_mediaVersions.isVisible():
            self.dlg_mediaVersions.close()

        self.dlg_mediaVersions = MediaVersionsDialog(self)
        self.dlg_mediaVersions.show()


if nuke.env.get("gui") and "fnFlipbookRenderer" in globals():
    class PrismRenderedFlipbook(fnFlipbookRenderer.SynchronousRenderedFlipbook):

        def __init__(self, flipbookDialog, flipbookToRun):
            fnFlipbookRenderer.SynchronousRenderedFlipbook.__init__(self, flipbookDialog, flipbookToRun)

        def doFlipbook(self, outputpath, frame):
            self.initializeFlipbookNode()
            self.renderFlipbookNode(outputpath, frame)

        def renderFlipbookNode(self, outputpath, frame):
            self._writeNode['file'].setValue(outputpath)
            self._writeNode['file_type'].setValue("jpeg")
            curSpace = self._writeNode['colorspace'].value()
            result = self._writeNode['colorspace'].setValue("sRGB")
            if not result:
                result = self._writeNode['colorspace'].setValue("Output - sRGB")
                if not result:
                    self._writeNode['colorspace'].setValue(curSpace)

            frange = nuke.FrameRanges(str(int(frame)))
            try:
                frameRange, views = self.getFlipbookOptions()
                nuke.executeMultiple(
                    (self._writeNode,),
                    frange,
                    views,
                    self._flipbookDialog._continueOnError.value()
                )
            except Exception as msg:
                import traceback
                print(traceback.format_exc())
                nuke.delete(self._nodeToFlipbook)
                self._nodeToFlipbook = None
                if msg.args[0][0:9] != "Cancelled":
                    nuke.message("Flipbook render failed:\n%s" % (msg.args[0],))
            finally:
                nuke.delete(self._nodeToFlipbook)
                self._nodeToFlipbook = None


class Farm_Submitter(QDialog):
    def __init__(self, plugin, state, dependencies=None):
        super(Farm_Submitter, self).__init__()
        self.plugin = plugin
        self.core = self.plugin.core
        self.core.parentWindow(self)
        self.state = state
        self.dependencies = dependencies
        self.setupUi()

    @err_catcher(name=__name__)
    def setupUi(self):
        self.setWindowTitle("Prism Farm Submitter - %s" % self.state.ui.node.fullName())
        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)
        self.lo_main.addWidget(self.state.ui)
        self.state.ui.f_name.setVisible(False)
        self.state.ui.w_format.setVisible(False)
        self.state.ui.f_taskname.setVisible(False)
        self.state.ui.f_resolution.setVisible(False)
        self.state.ui.gb_passes.setHidden(True)
        self.state.ui.gb_previous.setHidden(True)
        self.state.ui.gb_submit.setChecked(True)
        self.state.ui.gb_submit.setCheckable(False)
        self.state.ui.w_version.setVisible(False)
        self.state.ui.chb_version.setChecked(False)
        self.state.ui.f_cam.setVisible(False)
        if self.state.ui.cb_manager.count() == 1:
            self.state.ui.f_manager.setVisible(False)
            self.state.ui.gb_submit.setTitle(self.state.ui.cb_manager.currentText())

        self.lo_main.addStretch()
        self.b_submit = QPushButton("Submit")
        self.lo_main.addWidget(self.b_submit)
        self.b_submit.clicked.connect(self.submit)

    @err_catcher(name=__name__)
    def closeEvent(self, event):
        self.saveCurrentSettings()

    @err_catcher(name=__name__)
    def saveCurrentSettings(self):
        settings = self.state.ui.getStateProps()
        self.core.setConfig("nuke", "renderSubmissionSettings", val=settings, config="user")

    @err_catcher(name=__name__)
    def loadSettings(self, settings=None):
        settings = settings or self.core.getConfig("nuke", "renderSubmissionSettings") or {}
        self.state.ui.loadData(settings)

    @err_catcher(name=__name__)
    def submit(self):
        self.hide()
        self.state.ui.gb_submit.setCheckable(True)
        self.state.ui.gb_submit.setChecked(True)

        sm = self.core.getStateManager()
        comment = self.plugin.getCommentFromNode(self.state.ui.group)
        sm.e_comment.setText(comment)
        incrementScene = os.getenv("PRISM_NUKE_SUBMISSION_INCREMENT_SCENE", "0") == "1"
        versionWarning = os.getenv("PRISM_NUKE_SUBMISSION_VERSION_WARNING", "0") == "1"
        version = self.plugin.getRenderVersionFromWriteNode(self.state.ui.group) or "next"
        result = sm.publish(
            successPopup=False,
            executeState=True,
            states=[self.state],
            saveScene=True,
            incrementScene=incrementScene,
            dependencies=self.dependencies,
            useVersion=version,
            versionWarning=versionWarning,
        )
        prevKnob = self.state.ui.group.knob("prevFileName")
        if prevKnob:
            path = self.state.ui.l_pathLast.text() or "-"
            prevKnob.setValue(path)
            prevKnobE = self.state.ui.group.knob("prevFileNameEdit")
            if prevKnobE:
                prevKnobE.setValue(path)

        sm.deleteState(self.state)
        self.plugin.getOutputPath(self.state.ui.node, self.state.ui.group)
        if result:
            msg = "Job submitted successfully."
            self.core.popup(msg, severity="info")

        self.close()


class ShotListDlg(QDialog):

    entitiesAdded = Signal(object)
    entitiesInserted = Signal(object)

    def __init__(self, origin, parent=None):
        super(ShotListDlg, self).__init__()
        self.parentDlg = parent
        self.plugin = origin.plugin
        self.core = self.plugin.core
        self.setupUi()

    @err_catcher(name=__name__)
    def setupUi(self):
        title = "Choose Shots"

        self.setWindowTitle(title)
        self.core.parentWindow(self, parent=self.parentDlg)

        import EntityWidget
        self.w_entities = EntityWidget.EntityWidget(core=self.core, refresh=True, pages=["Shots"])
        self.w_entities.editEntitiesOnDclick = False
        self.w_entities.getPage("Shots").tw_tree.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.w_entities.getPage("Shots").setSearchVisible(False)

        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Add", QDialogButtonBox.AcceptRole)
        if self.plugin.getShotsFromScene():
            self.bb_main.addButton("Insert", QDialogButtonBox.AcceptRole)

        self.bb_main.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.bb_main.clicked.connect(self.buttonClicked)

        self.lo_main.addWidget(self.w_entities)
        self.lo_main.addWidget(self.bb_main)

    @err_catcher(name=__name__)
    def itemDoubleClicked(self, item, column):
        self.buttonClicked("add")

    @err_catcher(name=__name__)
    def buttonClicked(self, button):
        if button == "add" or button.text() in ["Add", "Insert"]:
            entities = self.w_entities.getCurrentData(returnOne=False)
            if isinstance(entities, dict):
                entities = [entities]

            validEntities = []
            for entity in entities:
                if entity.get("type", "") not in ["asset", "shot"]:
                    continue

                validEntities.append(entity)

            if not validEntities:
                msg = "Invalid shot selected."
                self.core.popup(msg, parent=self)
                return

            if button == "add" or button.text() in ["Add"]:
                self.entitiesAdded.emit(validEntities)
            else:
                self.entitiesInserted.emit(validEntities)

        self.close()

    @err_catcher(name=__name__)
    def sizeHint(self):
        return QSize(500, 500)


class NukeExport(object):
    className = "NukeExport"

    def setup(self, state, core, stateManager, node=None, stateData=None):
        super(NukeExport, self).setup(state, core, stateManager, node, stateData)
        self.w_name.setVisible(False)
        self.w_range.setVisible(False)
        self.f_frameRange_2.setVisible(False)
        self.w_wholeScene.setVisible(False)
        self.chb_wholeScene.setChecked(True)
        self.gb_objects.setVisible(False)
        self.w_additionalOptions.setVisible(False)
        self.w_outType.setVisible(False)
        self.gb_previous.setVisible(False)
        self.cb_context.setVisible(False)
        self.setRangeType("Single Frame")


class ExporterDlg(QDialog):
    def __init__(self, origin, state):
        super(ExporterDlg, self).__init__()
        self.origin = origin
        self.plugin = self.origin.plugin
        self.core = self.plugin.core
        self.core.parentWindow(self)
        self.state = state
        self.showSm = False
        if self.core.sm.isVisible():
            self.core.sm.setHidden(True)
            self.showSm = True

        self.setupUi()

    @err_catcher(name=__name__)
    def sizeHint(self):
        hint = super(ExporterDlg, self).sizeHint()
        hint += QSize(100, 0)
        return hint

    @err_catcher(name=__name__)
    def setupUi(self):
        self.setWindowTitle("Prism - Export Selected Nodes")
        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)
        self.lo_main.addWidget(self.state.ui)

        self.b_submit = QPushButton("Export")
        self.lo_main.addWidget(self.b_submit)
        self.b_submit.clicked.connect(self.submit)

    @err_catcher(name=__name__)
    def closeEvent(self, event):
        curItem = self.core.sm.getCurrentItem(self.core.sm.activeList)
        if self.state and curItem and id(self.state) == id(curItem):
            self.core.sm.showState()

        if self.showSm:
            self.core.sm.setHidden(False)

        event.accept()

    @err_catcher(name=__name__)
    def submit(self):
        self.hide()

        sanityChecks = True
        version = None
        saveScene = False
        incrementScene = False

        sm = self.core.getStateManager()
        result = sm.publish(
            successPopup=False,
            executeState=True,
            states=[self.state],
            useVersion=version,
            saveScene=saveScene,
            incrementScene=incrementScene,
            sanityChecks=sanityChecks,
            versionWarning=False,
        )
        if result:
            msg = "Exported nodes successfully."
            result = self.core.popupQuestion(msg, buttons=["Open in Product Browser", "Open in Explorer", "Close"], icon=QMessageBox.Information)
            path = self.state.ui.l_pathLast.text()
            if result == "Open in Product Browser":
                self.core.projectBrowser()
                self.core.pb.showTab("Products")
                data = self.core.paths.getCachePathData(path)
                self.core.pb.productBrowser.navigateToProduct(data["product"], entity=data)
            elif result == "Open in Explorer":
                self.core.openFolder(path)

            self.close()
        else:
            self.show()


class Prism_NoQt(object):
    def __init__(self):
        self.addPluginPaths()
        nuke.addFilenameFilter(self.expandEnvVarsInFilepath)

    def addPluginPaths(self):
        gdir = os.path.join(
            os.path.abspath(os.path.dirname(os.path.dirname(__file__))), "Gizmos"
        )
        gdir = gdir.replace("\\", "/")
        nuke.pluginAddPath(gdir)

    @err_catcher(name=__name__)
    def expandEnvVarsInFilepath(self, path):
        if os.getenv("PRISM_NUKE_USE_RELATIVE_PATHS", "1") == "0":
            return path

        expanded_path = os.path.expandvars(path)
        expanded_path = expanded_path.replace("%PRISM_JOB", os.getenv("PRISM_JOB"))
        return expanded_path


class VersionDlg(QDialog):

    versionSelected = Signal(object)

    def __init__(self, parent, node, group):
        super(VersionDlg, self).__init__()
        self.plugin = parent
        self.core = self.plugin.core
        self.node = node
        self.group = group
        self.isValid = False
        self.setupUi()

    @err_catcher(name=__name__)
    def setupUi(self):
        filepath = self.core.getCurrentFileName()
        entity = self.core.getScenefileData(filepath)
        if not entity or not entity.get("type"):
            msg = "Please save your scene in the Prism project first."
            self.core.popup(msg)
            return

        identifier = self.plugin.getIdentifierFromNode(self.group)
        if not identifier:
            msg = "Please enter an identifier in the settings of this node first."
            self.core.popup(msg)
            return

        if entity.get("type") == "asset":
            entityName = entity["asset_path"]
        elif entity.get("type") == "shot":
            entityName = self.core.entities.getShotName(entity)

        title = "Select version (%s - %s)" % (entityName, identifier)

        self.setWindowTitle(title)
        self.core.parentWindow(self)

        import MediaBrowser
        self.w_browser = MediaBrowser.MediaBrowser(core=self.core)
        self.w_browser.headerHeightSet = True
        self.w_browser.w_entities.setVisible(False)
        self.w_browser.w_identifier.setVisible(False)
        self.w_browser.lw_version.itemDoubleClicked.disconnect()
        self.w_browser.lw_version.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Use Selected Version", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Cancel", QDialogButtonBox.RejectRole)

        self.bb_main.clicked.connect(self.buttonClicked)

        self.lo_main.addWidget(self.w_browser)
        self.lo_main.addWidget(self.bb_main)

        self.w_browser.navigate([entity, identifier + " (2d)"])
        idf = self.w_browser.getCurrentIdentifier()
        if not idf or idf["identifier"] != identifier:
            msg = "The identifier \"%s\" doesn't exist yet." % identifier
            self.core.popup(msg)
            return

        self.isValid = self.w_browser.lw_version.count() > 0
        if not self.isValid:
            msg = "No version exists under the current identifier."
            self.core.popup(msg)
            return

    @err_catcher(name=__name__)
    def itemDoubleClicked(self, item):
        self.buttonClicked("select")

    @err_catcher(name=__name__)
    def buttonClicked(self, button):
        if button == "select" or button.text() == "Use Selected Version":
            version = self.w_browser.getCurrentVersion()
            if not version:
                msg = "Invalid version selected."
                self.core.popup(msg, parent=self)
                return

            intVersion = self.core.products.getIntVersionFromVersionName(version.get("version") or "")
            if intVersion is None:
                msg = "Invalid version selected."
                self.core.popup(msg, parent=self)
                return

            self.versionSelected.emit(intVersion)

        self.close()


class ReadMediaDialog(QDialog):

    mediaSelected = Signal(object)

    def __init__(self, parent, node):
        super(ReadMediaDialog, self).__init__()
        self.plugin = parent
        self.core = self.plugin.core
        self.node = node
        self.isValid = False
        self.setupUi()

    @err_catcher(name=__name__)
    def setupUi(self):
        filepath = self.core.getCurrentFileName()
        entity = self.core.getScenefileData(filepath)
        title = "Select Media"
        self.setWindowTitle(title)
        self.core.parentWindow(self)

        import MediaBrowser
        self.w_browser = MediaBrowser.MediaBrowser(core=self.core)
        self.w_browser.headerHeightSet = True
        self.w_browser.lw_version.itemDoubleClicked.disconnect()
        self.w_browser.lw_version.itemDoubleClicked.connect(self.itemDoubleClicked)

        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Open", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Cancel", QDialogButtonBox.RejectRole)

        self.bb_main.clicked.connect(self.buttonClicked)

        self.lo_main.addWidget(self.w_browser)
        self.lo_main.addWidget(self.bb_main)

        self.w_browser.navigate([entity])

    @err_catcher(name=__name__)
    def itemDoubleClicked(self, item):
        self.buttonClicked("select")

    @err_catcher(name=__name__)
    def buttonClicked(self, button):
        if button == "select" or button.text() == "Open":
            data = self.w_browser.getCurrentSource()
            if not data:
                data = self.w_browser.getCurrentAOV()
                if not data:
                    data = self.w_browser.getCurrentVersion()
                    if not data:
                        data = self.w_browser.getCurrentIdentifier()

            if not data:
                msg = "Invalid version selected."
                self.core.popup(msg, parent=self)
                return

            self.mediaSelected.emit(data)

        self.close()


class MediaVersionsDialog(QDialog):
    """Non-modal dialog for managing media versions in Read nodes"""
    
    def __init__(self, plugin):
        super(MediaVersionsDialog, self).__init__()
        self.plugin = plugin
        self.core = plugin.core
        self.groupByShot = False
        self.nodeItems = []
        
        self.setupUi()
        self.connectEvents()
        self.refreshNodes()
    
    @err_catcher(name=__name__)
    def setupUi(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Manage Media Versions")
        self.resize(1200, 600)
        self.core.parentWindow(self)
        
        # Make it non-modal
        self.setWindowModality(Qt.NonModal)
        
        # Main layout
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        self.btn_refresh = QPushButton("Refresh")
        self.btn_refresh.setToolTip("Refresh the list of Read nodes")
        toolbar.addWidget(self.btn_refresh)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Tree widget
        self.tree = QTreeWidget()
        self.tree.setAlternatingRowColors(True)
        self.tree.setSortingEnabled(True)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        
        # Setup columns
        self.setupColumns()
        
        layout.addWidget(self.tree)
        
        # Status bar
        self.statusLabel = QLabel("Ready")
        toolbar.addWidget(self.statusLabel)
        
        self.setLayout(layout)
        
    @err_catcher(name=__name__)
    def setupColumns(self):
        """Setup tree widget columns"""
        columns = ["Node Name", "Asset/Shot", "Identifier", "Version", "Status", "Filepath"]
        self.tree.setHeaderLabels(columns)
        
        # Set column widths
        self.tree.setColumnWidth(0, 150)  # Node Name
        self.tree.setColumnWidth(1, 120)  # Shot
        self.tree.setColumnWidth(2, 150)  # Identifier
        self.tree.setColumnWidth(3, 100)  # Version
        self.tree.setColumnWidth(4, 120)  # Status
        self.tree.setColumnWidth(5, 400)  # Filepath
    
    @err_catcher(name=__name__)
    def connectEvents(self):
        """Connect UI events"""
        self.btn_refresh.clicked.connect(self.refreshNodes)
        self.tree.customContextMenuRequested.connect(self.showContextMenu)
        self.tree.itemSelectionChanged.connect(self.onSelectionChanged)
        self.tree.itemDoubleClicked.connect(self.onItemDoubleClicked)

    @err_catcher(name=__name__)
    def getOutdatedMedia(self):
        items = []
        for item in self.nodeItems:
            status = item.text(4).lower()
            if status == "update available":
                items.append(item)

        return items

    @err_catcher(name=__name__)
    def refreshNodes(self):
        """Scan all Read nodes and populate the tree widget"""
        self.tree.clear()
        self.nodeItems = []
        
        # Get all Read nodes in the script
        readNodes = [node for node in nuke.allNodes(recurseGroups=True) if node.Class() in ["Read", "DeepRead"]]
        
        if not readNodes:
            self.statusLabel.setText("No Read nodes found in script")
            return
            
        items = []
        for node in readNodes:
            item = self.createTreeItem(node)
            if item:
                items.append(item)
        
        if self.groupByShot:
            self.groupItemsByShot(items)
        else:
            for item in items:
                self.tree.addTopLevelItem(item)

        for item in items:
            # Create version combo box
            self.createVersionComboBox(item)

        self.nodeItems = items
        self.statusLabel.setText(f"Found {len(items)} Read nodes")
        self.tree.expandAll()
        self.tree.resizeColumnToContents(0)
        self.tree.setColumnWidth(0, self.tree.columnWidth(0) + 20)
        self.tree.resizeColumnToContents(1)
        self.tree.setColumnWidth(1, self.tree.columnWidth(1) + 20)
        self.tree.resizeColumnToContents(2)
        self.tree.setColumnWidth(2, self.tree.columnWidth(2) + 20)
        self.tree.resizeColumnToContents(3)
        self.tree.setColumnWidth(3, self.tree.columnWidth(3) + 20)

    @err_catcher(name=__name__)
    def createTreeItem(self, node):
        """Create a tree widget item for a Read node"""
        filepath = node.knob("file").value() or ""
        entityName = ""
        identifier = ""
        version = ""
        pathData = {}
        if filepath:                
            # Expand environment variables
            filepath = self.plugin.expandEnvVarsInFilepath(filepath)
            
            # Try to get information from Prism path structure
            pathData = self.getContextFromFilepath(filepath)
            if pathData:
                identifier = pathData.get("identifier", "")
                version = pathData.get("version", "")
                entityName = self.core.entities.getEntityName(pathData)
        
        # Calculate status
        status, statusColor = self.calculateVersionStatus(filepath, version)
        
        # Create the tree item
        item = QTreeWidgetItem([
            node.fullName(),
            entityName,
            identifier,
            version,
            status,
            filepath
        ])
        
        # Store the node reference and additional data
        item.setData(0, Qt.UserRole, {"node": node, "context": pathData})
        item.setData(4, Qt.UserRole + 1, statusColor)  # Store status color
        item.setToolTip(5, filepath)
        
        # Set status column background color
        if statusColor:
            item.setBackground(4, QColor(statusColor))
        
        return item

    @err_catcher(name=__name__)
    def getContextFromFilepath(self, filepath):
        mediaType = self.core.mediaProducts.getMediaTypeFromPath(filepath) or "2drenders"
        pathData = self.core.paths.getRenderProductData(filepath, mediaType=mediaType)
        if pathData and not pathData.get("identifier"):
            entityType = self.core.paths.getEntityTypeFromPath(filepath)
            key = None
            if mediaType == "playblasts":
                if entityType == "asset":
                    key = "playblastFilesAssets"
                elif entityType == "shot":
                    key = "playblastFilesShots"
            else:
                if entityType == "asset":
                    key = "renderFilesAssets"
                elif entityType == "shot":
                    key = "renderFilesShots"

            if not key:
                return pathData
            
            context = {
                "type": entityType,
                "entityType": entityType,
            }

            context["mediaType"] = mediaType
            location = self.core.paths.getLocationFromPath(filepath)
            if location:
                context["project_path"] = self.core.paths.getRenderProductBasePaths()[location]

            template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
            context.update(pathData)
            pathData = self.core.projects.extractKeysFromPath(os.path.dirname(os.path.normpath(filepath)), os.path.dirname(template), context=context)

        return pathData
    
    @err_catcher(name=__name__)
    def calculateVersionStatus(self, filepath, currentVersion):
        """Calculate version status for a media file"""
        if not filepath or not currentVersion:
            return "unknown", "#636363"  # Gray background
        
        try:
            # Get available versions
            versions = self.getAvailableVersions(filepath)
            if not versions:
                return "unknown", "#636363"  # Gray background
            
            # Get the latest version (first in sorted list)
            latestVersion = versions[0] if versions else None
            
            if not latestVersion:
                return "unknown", "#636363"  # Gray background
            
            if currentVersion == latestVersion:
                return "latest", "#266D26"  # Light green background
            else:
                return "update available", "#AF571C"  # Light orange background
                
        except Exception as e:
            logger.warning(f"Failed to calculate version status for {filepath}: {str(e)}")
            return "unknown", "#636363"  # Gray background

    @err_catcher(name=__name__)
    def createVersionComboBox(self, item):
        node = item.data(0, Qt.UserRole)["node"]
        filepath = node.knob("file").value() or ""
        filepath = self.plugin.expandEnvVarsInFilepath(filepath)
        """Create version combo box for the item"""
        combo = QComboBox()
        
        # Get available versions
        versions = self.getAvailableVersions(filepath)
        
        if versions:
            combo.addItems(versions)
            
            # Set current version
            try:
                mediaType = self.core.mediaProducts.getMediaTypeFromPath(filepath) or "2drenders"
                pathData = self.core.paths.getRenderProductData(filepath, mediaType=mediaType)
                currentVersion = pathData.get("version", "")
                if currentVersion and currentVersion in versions:
                    combo.setCurrentText(currentVersion)
            except:
                pass
            
            # Connect version change signal
            combo.currentTextChanged.connect(
                lambda version, n=node: self.onVersionChanged(n, version)
            )
        else:
            combo.addItem("No versions found")
            combo.setEnabled(False)
            
        # Set the combo box in the tree
        self.tree.setItemWidget(item, 3, combo)

    @err_catcher(name=__name__)
    def getAvailableVersions(self, filepath):
        """Get available versions for a media file"""
        mediaType = self.core.mediaProducts.getMediaTypeFromPath(filepath) or "2drenders"
        pathData = self.core.paths.getRenderProductData(filepath, mediaType=mediaType)
        if not pathData:
            return []
            
        # Create context for version lookup
        ctx = {
            "type": pathData.get("type"),
            "identifier": pathData.get("identifier", ""),
            "mediaType": mediaType,
        }
        if ctx["type"] == "asset":
            ctx["asset_path"] = pathData.get("asset_path", "")
        elif ctx["type"] == "shot":
            ctx["sequence"] = pathData.get("sequence", "")
            ctx["shot"] = pathData.get("shot", "")
        
        # Get all versions
        versions = self.core.mediaProducts.getVersionsFromContext(ctx)
        versionNames = [v["version"] for v in versions]
        
        # Sort versions (latest first)
        return sorted(versionNames, reverse=True)
    
    @err_catcher(name=__name__)
    def onVersionChanged(self, node, version):
        """Handle version change in combo box"""
        # Get current filepath
        currentPath = node.knob("file").value()
        currentPath = self.plugin.expandEnvVarsInFilepath(currentPath)
        
        # Get path data
        mediaType = self.core.mediaProducts.getMediaTypeFromPath(currentPath) or "2drenders"
        pathData = self.core.paths.getRenderProductData(currentPath, mediaType=mediaType)
        if not pathData:
            return

        version = self.core.mediaProducts.getVersion(pathData, pathData["identifier"], mediaType=mediaType, version=version)
        if not version:
            self.core.popup(f"Version {version} not found.")
            return
    
        aovs = self.core.mediaProducts.getAOVsFromVersion(pathData)
        if aovs:
            aosNames = [aov["aov"] for aov in aovs]
            aov = pathData.get("aov") if pathData.get("aov") and pathData.get("aov") in aosNames else aosNames[0]
        else:
            aov = None

        newPath = self.core.mediaProducts.getFileFromVersion(version, aov=aov, findExisting=True)
        if not newPath:
            self.core.popup(f"File for version {version} not found.")
            return
        
        # Update the Read node
        useRel = self.core.getConfig("nuke", "useRelativePaths", dft=False, config="user")
        if useRel:
            newPath = self.plugin.makePathRelative(newPath)
        
        # Handle frame range
        if "#" in newPath:
            files = self.core.media.getFilesFromSequence(newPath)
            start, end = self.core.media.getFrameRangeFromSequence(files)
            if start and end and start != "?" and end != "?":
                newPath += f" {start}-{end}"
        
        node.knob("file").fromUserText(newPath)
        
        # Refresh the item
        self.refreshSingleItem(node)
        return True
                
    @err_catcher(name=__name__)
    def refreshSingleItem(self, node):
        """Refresh a single tree item"""
        # Find the item for this node
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if item.data(0, Qt.UserRole)["node"] == node:
                # Update filepath and version info
                filepath = node.knob("file").value()
                filepath = self.plugin.expandEnvVarsInFilepath(filepath)
                item.setText(5, filepath)  # Filepath column is now index 5
                
                # Update version
                try:
                    pathData = self.getContextFromFilepath(filepath)
                    version = pathData.get("version", "") if pathData else ""
                    item.setText(3, version)  # Version column
                    
                    # Update status
                    status, statusColor = self.calculateVersionStatus(filepath, version)
                    item.setText(4, status)  # Status column
                    if statusColor:
                        item.setBackground(4, QColor(statusColor))
                        
                except Exception as e:
                    logger.warning(f"Failed to refresh item for node {node.name()}: {str(e)}")
                    
                break
    
    @err_catcher(name=__name__)
    def groupItemsByShot(self, items):
        """Group tree items by shot"""
        shotGroups = {}
        
        for item in items:
            shotName = item.text(1)  # Shot column
            if not shotName:
                shotName = "Unknown"
                
            if shotName not in shotGroups:
                # Create shot group
                shotItem = QTreeWidgetItem([shotName, "", "", "", "", ""])  # Added extra column for Status
                font = shotItem.font(0)
                font.setBold(True)
                shotItem.setFont(0, font)
                shotGroups[shotName] = shotItem
                self.tree.addTopLevelItem(shotItem)
            
            # Add item under shot group
            shotGroups[shotName].addChild(item)

    @err_catcher(name=__name__)
    def showContextMenu(self, position):
        """Show context menu"""
        menu = QMenu()
        
        # Check if any items are selected
        selectedItems = self.tree.selectedItems()
        if selectedItems:
            # Update to latest action
            updateAction = menu.addAction("Update to Latest")
            updateAction.triggered.connect(self.updateSelectedToLatest)
            menu.addSeparator()
        
        # Group by shot toggle
        if self.groupByShot:
            action = menu.addAction("Ungroup by Shot")
        else:
            action = menu.addAction("Group by Shot")
        action.triggered.connect(self.toggleGroupByShot)
        
        menu.addSeparator()
        
        # Refresh action
        refreshAction = menu.addAction("Refresh")
        refreshAction.triggered.connect(self.refreshNodes)
        
        # Show menu at cursor position
        menu.exec_(self.tree.mapToGlobal(position))
    
    @err_catcher(name=__name__)
    def updateSelectedToLatest(self):
        """Update all selected nodes to their latest versions"""
        selectedItems = self.tree.selectedItems()
        if not selectedItems:
            return
        
        updatedCount = 0
        failedCount = 0
        
        for item in selectedItems:
            try:
                node = item.data(0, Qt.UserRole)["node"]
                if not node or not hasattr(node, 'knob'):
                    continue
                
                # Get current filepath
                currentPath = node.knob("file").value()
                if not currentPath:
                    continue
                    
                currentPath = self.plugin.expandEnvVarsInFilepath(currentPath)
                
                # Get available versions
                versions = self.getAvailableVersions(currentPath)
                if not versions:
                    failedCount += 1
                    continue
                
                # Get latest version
                latestVersion = versions[0]
                currentVersion = item.text(3)  # Version column
                
                if currentVersion == latestVersion:
                    continue  # Already latest
                
                # Update to latest version
                result = self.onVersionChanged(node, latestVersion)
                if result:
                    updatedCount += 1
                else:
                    failedCount += 1
                
            except Exception as e:
                logger.warning(f"Failed to update node {node.name() if node else 'unknown'}: {str(e)}")
                failedCount += 1
        
        # Show result message
        if updatedCount > 0 or failedCount > 0:
            message = f"Updated {updatedCount} nodes"
            if failedCount > 0:
                message += f", {failedCount} failed"

            logger.info(message)
            # self.core.popup(message, severity="info" if failedCount == 0 else "warning")
        
        # Refresh the tree to update status indicators
        self.refreshNodes()
    
    @err_catcher(name=__name__)
    def toggleGroupByShot(self):
        """Toggle grouping by shot"""
        self.groupByShot = not self.groupByShot
        self.refreshNodes()
    
    @err_catcher(name=__name__)
    def onSelectionChanged(self):
        """Handle tree widget selection change - sync with Nuke node selection"""
        try:
            # Get selected tree items
            selectedItems = self.tree.selectedItems()
            
            # Clear current Nuke selection
            for node in nuke.selectedNodes():
                node.setSelected(False)
            
            # Select corresponding nodes in Nuke
            for item in selectedItems:
                node = item.data(0, Qt.UserRole)["node"]
                if node and hasattr(node, 'setSelected'):
                    try:
                        node.setSelected(True)
                    except:
                        # Node might have been deleted
                        pass
                        
        except Exception as e:
            logger.warning(f"Failed to sync selection: {str(e)}")
    
    @err_catcher(name=__name__)
    def onItemDoubleClicked(self, item, column):
        """Handle double-click on tree item - frame to node in Nuke"""
        try:
            node = item.data(0, Qt.UserRole)["node"]
            if not node or not hasattr(node, 'setSelected'):
                return
                
            # Clear current selection and select only this node
            for n in nuke.selectedNodes():
                n.setSelected(False)
            node.setSelected(True)
            
            # Frame to the node in the node graph
            # This uses Nuke's zoom functionality to frame the selected node
            nuke.zoom(2, [node.xpos(), node.ypos()])
            
        except Exception as e:
            logger.warning(f"Failed to frame to node: {str(e)}")
