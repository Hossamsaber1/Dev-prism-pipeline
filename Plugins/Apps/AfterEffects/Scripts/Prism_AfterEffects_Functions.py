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
import socket
import glob
import logging
import copy
try:
    import psutil
except:
    pass

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher as err_catcher


logger = logging.getLogger(__name__)


class Prism_AfterEffects_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.core.registerCallback(
            "onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self.plugin
        )
        self.core.registerCallback(
            "mediaPlayerContextMenuRequested", self.mediaPlayerContextMenuRequested, plugin=self.plugin
        )

    @err_catcher(name=__name__)
    def startup(self, origin):
        origin.timer.stop()
        appIcon = QIcon(self.appIcon)
        qapp = QApplication.instance()
        qapp.setWindowIcon(appIcon)

        origin.messageParent = QWidget()
        self.core.setActiveStyleSheet("AfterEffects")
        if self.core.useOnTop:
            origin.messageParent.setWindowFlags(
                origin.messageParent.windowFlags() ^ Qt.WindowStaysOnTopHint
            )

        pid = self.getAePid()
        self.aePid = int(pid) if pid else None
        self.aeAliveTimer = QTimer()
        self.aeAliveTimer.timeout.connect(self.checkAeAlive)
        self.aeAliveTimer.setSingleShot(True)
        self.checkAeAlive()
        origin.startAutosaveTimer()

    @err_catcher(name=__name__)
    def checkAeAlive(self):
        if "psutil" not in globals():
            return

        if self.aePid and psutil.pid_exists(self.aePid):
            self.aeAliveTimer.start(5 * 1000)
        else:
            QApplication.instance().quit()

    @err_catcher(name=__name__)
    def sendCmd(self, cmd):
        HOST = '127.0.0.1'
        PORT = 9888
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
            except Exception as e:
                logger.debug("sending cmd: %s" % cmd)
                self.core.popup("Failed to communiate with After Effects.\n(%s)" % str(e))
                return

            data = (cmd).encode("utf-8")
            s.sendall(data)
            data = s.recv(1024)

        return data

    @err_catcher(name=__name__)
    def getAePid(self):
        cmd = "pid"
        pid = (self.sendCmd(cmd) or "".encode()).decode("utf-8")
        return pid

    @err_catcher(name=__name__)
    def autosaveEnabled(self, origin):
        cmd = "app.preferences.getPrefAsLong(\"Auto Save\", \"Enable Auto Save3\", PREFType.PREF_Type_MACHINE_INDEPENDENT);"
        enabled = (self.sendCmd(cmd) or "".encode()).decode("utf-8")
        return enabled == "1"

    @err_catcher(name=__name__)
    def sceneOpen(self, origin):
        if self.core.shouldAutosaveTimerRun():
            origin.startAutosaveTimer()

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin, path=True):
        cmd = "app.project.file.fsName;"
        filename = (self.sendCmd(cmd) or "".encode()).decode("utf-8")
        if path:
            return filename
        else:
            return os.path.basename(filename)

    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        return self.sceneFormats[0]

    @err_catcher(name=__name__)
    def saveScene(self, origin, filepath, details={}):
        cmd = "app.project.save(File(\"%s\"));" % filepath
        self.sendCmd(cmd)
        return True

    @err_catcher(name=__name__)
    def getImportPaths(self, origin):
        return False

    @err_catcher(name=__name__)
    def hasActiveComp(self):
        cmd = """
        if (app.project && app.project.activeItem && app.project.activeItem instanceof CompItem) {
            "{\\"result\\": True}";
        } else {
            "{\\"result\\": False}";
        }"""

        result = self.sendCmd(cmd)
        if not result:
            return

        result = result.decode("utf-8")
        if result == "null":
            return

        result = eval(result)
        return result["result"]

    @err_catcher(name=__name__)
    def getCompositionNames(self):
        cmd = """
        function getAllCompositions() {
            var project = app.project;
            var compositions = [];

            if (project && project.items) {
                for (var i = 1; i <= project.items.length; i++) {
                    var item = project.items[i];
                    if (item instanceof CompItem) {
                        compositions.push(item.name);
                    }
                }
            }

            return compositions;
        }

        // Example usage
        var compositions = getAllCompositions();
        var compositionNames = compositions.join(",");
        "{\\"result\\": True, \\"compositions\\": \\"" + compositionNames + "\\"}";"""

        result = self.sendCmd(cmd)
        if not result:
            return

        result = result.decode("utf-8")
        if result == "null":
            return

        result = eval(result)
        return [x for x in result["compositions"].split(",") if x]

    @err_catcher(name=__name__)
    def getFrameRange(self, origin):
        startframe = None
        endframe = None

        cmd = """
        if (app.project && app.project.activeItem && app.project.activeItem instanceof CompItem) {
            var comp = app.project.activeItem;
            var frameRate = comp.frameRate;
            var startFrame = comp.displayStartFrame;
            var durationFrames = comp.duration * frameRate;
            var endFrame = startFrame + durationFrames - 1;
            "{\\"result\\": True, \\"startFrame\\": " + startFrame + ", \\"endFrame\\": " + endFrame + "}";
        } else {
            "{\\"result\\": False, \\"details\\": \\"No active composition found.\\"}";
        }"""

        result = self.sendCmd(cmd)
        if not result:
            return [startframe, endframe]

        result = result.decode("utf-8")
        if result == "null":
            return [startframe, endframe]

        result = eval(result)
        if result["result"] is True:
            startframe = result["startFrame"]
            endframe = result["endFrame"]

        return [startframe, endframe]

    @err_catcher(name=__name__)
    def setFrameRange(self, origin, startFrame, endFrame):
        cmd = """
        if (app.project && app.project.activeItem && app.project.activeItem instanceof CompItem) {
            var comp = app.project.activeItem;
            var frameRate = comp.frameRate;
            var startFrame = %s;
            comp.displayStartFrame = startFrame;
            comp.duration = (%s - startFrame + 1) / frameRate;
            comp.workAreaStart = 0;
            comp.workAreaDuration = comp.duration;
            "{\\"result\\": True}";
        } else {
            "{\\"result\\": False, \\"details\\": \\"No active composition found.\\"}";
        }""" % (startFrame, endFrame)
        self.sendCmd(cmd)
    
    @err_catcher(name=__name__)
    def getFPS(self, origin):
        cmd = """
        if (app.project && app.project.activeItem && app.project.activeItem instanceof CompItem) {
            var comp = app.project.activeItem;
            var frameRate = comp.frameRate;
            "{\\"result\\": True, \\"frameRate\\": " + frameRate + "}";
        } else {
            "{\\"result\\": False, \\"details\\": \\"No active composition found.\\"}";
        }"""
        
        result = self.sendCmd(cmd)
        if not result:
            return None

        result = result.decode("utf-8")
        if result == "null":
            return None

        result = eval(result)
        if result["result"] is True:
            return result["frameRate"]
        else:
            return None

    @err_catcher(name=__name__)
    def setFPS(self, origin, fps):
        cmd = """
        if (app.project && app.project.activeItem && app.project.activeItem instanceof CompItem) {
            var comp = app.project.activeItem;
            comp.frameRate = %s;
            "{\\"result\\": True, \\"frameRate\\": " + comp.frameRate + "}";
        } else {
            "{\\"result\\": False, \\"details\\": \\"No active composition found.\\"}";
        }""" % fps

        self.sendCmd(cmd)

    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        cmd = """
        if (app) {
            var version = app.version;
            "{\\"result\\": True, \\"version\\": \\"" + version + "\\"}";
        } else {
            "{\\"result\\": False, \\"details\\": \\"No app found.\\"}";
        }"""

        result = self.sendCmd(cmd)
        if not result:
            return None

        result = result.decode("utf-8")
        if result == "null":
            return None

        result = eval(result)
        if result["result"] is True:
            return result["version"]
        else:
            return None

    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        cmd = "app.open(File(\"%s\"));" % filepath
        self.sendCmd(cmd)
        return True

    @err_catcher(name=__name__)
    def getCurrentSceneFiles(self, origin):
        curFileName = self.core.getCurrentFileName()
        scenefiles = [curFileName]
        return scenefiles

    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self, origin):
        origin.actionStateManager.setEnabled(False)
    
    @err_catcher(name=__name__)
    def mediaPlayerContextMenuRequested(self, origin, menu):
        if len(origin.seq) > 0 and type(origin).__name__ == "MediaPlayer":
            actReplace = QAction("Replace Active Item...", origin)
            actReplace.triggered.connect(lambda: self.replaceActiveItemFromMediaBrowser(origin))
            menu.addAction(actReplace)

    @err_catcher(name=__name__)
    def replaceActiveItemFromMediaBrowser(self, origin):
        sourceData = origin.compGetImportSource()
        for sourceDat in sourceData:
            filepath = sourceDat[0]
            self.replaceActiveItem(filepath)

    @err_catcher(name=__name__)
    def importImages(self, filepath=None, mediaBrowser=None, parent=None):
        if mediaBrowser:
            if mediaBrowser.origin.getCurrentAOV() and mediaBrowser.origin.w_preview.cb_layer.count() > 1:
                fString = "Please select an import option:"
                buttons = ["Current AOV", "All AOVs"]
                result = self.core.popupQuestion(fString, buttons=buttons, icon=QMessageBox.NoIcon)
            else:
                result = "Current AOV"

            if result == "Current AOV":
                self.importSource(mediaBrowser)
            elif result == "All AOVs":
                self.importAOVs(mediaBrowser)
            else:
                return

    @err_catcher(name=__name__)
    def importSource(self, origin):
        sourceData = origin.compGetImportSource()
        for sourceDat in sourceData:
            filepath = sourceDat[0]
            self.importMedia(filepath)
        
    @err_catcher(name=__name__)
    def importAOVs(self, origin):
        sourceData = origin.compGetImportPasses()
        for sourceDat in sourceData:
            filepath = sourceDat[0]
            self.importMedia(filepath)

    @err_catcher(name=__name__)
    def sm_getExternalFiles(self, origin):
        footageItems = self.getFootageFromProject() or []
        paths = []
        for footageItem in footageItems:
            paths.append(footageItem["path"])

        return [paths, []]

    @err_catcher(name=__name__)
    def getMediaFromEntities(self, entities, identifier):
        versions = []
        for entity in entities:
            if entity.get("type") != "shot":
                continue

            for idf in [idf.strip() for idf in identifier.split(",")]:
                context = entity.copy()
                if identifier.endswith(" (playblast)"):
                    context["mediaType"] = "playblasts"
                    idf = identifier.replace(" (playblast)", "")
                elif identifier.endswith(" (2d)"):
                    context["mediaType"] = "2drenders"
                    idf = identifier.replace(" (2d)", "")
                elif identifier.endswith(" (external)"):
                    context["mediaType"] = "externalMedia"
                    idf = identifier.replace(" (external)", "")
                else:
                    context["mediaType"] = "3drenders"

                context["identifier"] = idf

                version = self.core.mediaProducts.getLatestVersionFromIdentifier(context)
                if not version:
                    logger.debug("Couldn't find a version for context: %s" % context)
                    continue

                if context.get("mediaType") not in ["playblasts", "2drenders"]:
                    aovs = self.core.mediaProducts.getAOVsFromVersion(version)
                    if not aovs:
                        logger.debug("Couldn't find any AOVs for version: %s" % version)
                        continue

                    aov = aovs[0]
                else:
                    aov = version

                filepaths = self.core.mediaProducts.getFilesFromContext(aov)
                if not filepaths:
                    logger.debug("Couldn't find any files for AOV: %s" % aov)
                    continue

                version["filepaths"] = filepaths
                versions.append(version)

        return versions

    @err_catcher(name=__name__)
    def importMediaVersions(self, entities, identifiers, addToComp=False):
        versions = []
        for identifier in identifiers:
            versions += self.getMediaFromEntities(entities, identifier)

        if not versions:
            msg = "Couldn't find any media for the selected context."
            self.core.popup(msg)
            return False

        result = False
        for version in versions:
            pattern = self.core.media.getSequenceFromFilename(version["filepaths"][0])
            res = self.importMedia(pattern, addToComp=addToComp)
            if not res:
                continue

            res = res.decode("utf-8")
            if res == "null":
                continue

            result = eval(res)

        return result.get("result") if result else False

    @err_catcher(name=__name__)
    def importMedia(self, filepath, addToComp=False):
        filepaths = self.core.media.getFilesFromSequence(filepath)
        if not filepaths:
            return

        if addToComp:
            addToComp = """
    if (activeItem instanceof CompItem) {
        var newLayer = activeItem.layers.add(importedFile);
    }
            """
        else:
            addToComp = ""

        cmd = """
if (app.project) {
    var activeItem = app.project.activeItem;
    var importOptions = new ImportOptions(File("%s"));
    importOptions.sequence = %s;
    if (importOptions.canImportAs(ImportAsType.FOOTAGE)) {
        importOptions.importAs = ImportAsType.FOOTAGE;
    }
    var importedFile = app.project.importFile(importOptions);
    %s
    "{\\"result\\": True, \\"fileName\\": \\"" + importedFile.name + "\\"}";
} else {
    "{\\"result\\": False, \\"details\\": \\"No project found.\\"}";
}""" % (filepaths[0].replace("\\", "/"), "true" if len(filepaths) > 1 else "false", addToComp)

        result = self.sendCmd(cmd)
        return result

    @err_catcher(name=__name__)
    def replaceActiveItem(self, filepath):
        filepaths = self.core.media.getFilesFromSequence(filepath)
        if not filepaths:
            return

        cmd = """
if (app.project && app.project.activeItem && app.project.activeItem instanceof FootageItem) {
    var curItem = app.project.activeItem
    if (curItem instanceof FootageItem) {
        curItem.replace(File("%s"));
    }
    "{\\"result\\": True, \\"fileName\\": \\"" + curItem.name + "\\"}";
} else {
    "{\\"result\\": False, \\"details\\": \\"No active item found.\\"}";
}""" % (filepaths[0].replace("\\", "/"))

        if len(filepaths) > 1:
            cmd = cmd.replace("curItem.replace(File(\"%s\"));" % filepaths[0].replace("\\", "/"), "curItem.replaceWithSequence(File(\"%s\"), false);" % filepaths[0].replace("\\", "/"))

        result = self.sendCmd(cmd)
        if not result:
            return None

        result = result.decode("utf-8")
        if result == "null":
            return None

        result = eval(result)
        if result["result"] is False:
            self.core.popup(result["details"])

        return result["result"]

    @err_catcher(name=__name__)
    def replaceItem(self, idx, filepath):
        filepaths = self.core.media.getFilesFromSequence(filepath)
        if not filepaths:
            return

        cmd = """
if (app.project) {
    var curItem = app.project.item(%s)
    if (curItem instanceof FootageItem) {
        curItem.replace(File("%s"));
    }
    "{\\"result\\": True, \\"fileName\\": \\"" + curItem.name + "\\"}";
} else {
    "{\\"result\\": False, \\"details\\": \\"No project active.\\"}";
}""" % (idx, filepaths[0].replace("\\", "/"))

        if len(filepaths) > 1:
            cmd = cmd.replace("curItem.replace(File(\"%s\"));" % filepaths[0].replace("\\", "/"), "curItem.replaceWithSequence(File(\"%s\"), false);" % filepaths[0].replace("\\", "/"))

        result = self.sendCmd(cmd)
        if not result:
            return None

        result = result.decode("utf-8")
        if result == "null":
            return None

        result = eval(result)
        if result["result"] is False:
            self.core.popup(result["details"])

        return result["result"]

    @err_catcher(name=__name__)
    def getFootageFromProject(self):
        cmd = """
function getAllFootage() {
    var project = app.project;
    var footages = [];

    if (project && project.items) {
        for (var i = 1; i <= project.items.length; i++) {
            var item = project.items[i];
            if (item instanceof FootageItem) {
                footages.push(i);
                footages.push(item.file.path);
                footages.push(item.file.name);
            }
        }
    }

    return footages;
}
if (app.project) {
    var footage = getAllFootage();
    var footageData = footage.join(",");
    "{\\"result\\": True, \\"footage\\": \\"" + footageData + "\\"}";
} else {
    "{\\"result\\": False, \\"details\\": \\"No project active.\\"}";
}"""

        result = self.sendCmd(cmd)
        if not result:
            return None

        result = result.decode("utf-8")
        if result == "null":
            return None

        result = eval(result)
        if result["result"] is False:
            self.core.popup(result["details"])
        else:
            resultData = []
            for idx, data in enumerate(result["footage"].split(",")):
                if (idx % 3) == 2:
                    resultData[-1]["path"] = os.path.normpath(resultData[-1]["path"] + "/" + data)
                    resultData[-1]["name"] = data
                elif (idx % 3) == 1:
                    if data and data[0] == "/" and data[1] != "/" and data[2] == "/":
                        data = data.strip("/")
                        data = os.path.normpath(data[0].upper() + ":" + data[1:])

                    resultData[-1]["path"] = data
                elif data:
                    resultData.append({"idx": int(data)})

            return resultData

    @err_catcher(name=__name__)
    def sm_render_getDeadlineSubmissionParams(self, origin, dlParams, jobOutputFile):
        dlParams["Build"] = dlParams["build"]
        dlParams["OutputFilePath"] = os.path.split(jobOutputFile)[0]
        dlParams["OutputFilePrefix"] = os.path.splitext(
            os.path.basename(jobOutputFile)
        )[0]
        dlParams["Renderer"] = self.getCurrentRenderer(origin)

        if origin.chb_resOverride.isChecked() and "resolution" in dlParams:
            resString = "Image"
            dlParams[resString + "Width"] = str(origin.sp_resWidth.value())
            dlParams[resString + "Height"] = str(origin.sp_resHeight.value())

        return dlParams

    @err_catcher(name=__name__)
    def openImportMediaDlg(self):
        self.dlg_importMedia = ImportMediaDlg(self)
        self.dlg_importMedia.show()

    @err_catcher(name=__name__)
    def checkVersions(self):
        items = self.getFootageFromProject() or []
        outdatedItems = []
        for item in items:
            version = self.core.mediaProducts.getLatestVersionFromFilepath(item["path"])
            if version and version["path"] not in item["path"]:
                filepattern = self.core.mediaProducts.getFileFromVersion(version, findExisting=True)
                if not filepattern:
                    continue

                item["latestPath"] = filepattern
                outdatedItems.append(item)

        if outdatedItems:
            msg = "The following versions are outdated:\n\n"
            for item in outdatedItems:
                msg += item["name"] + "\n"
        else:
            msg = "All versions are up to date."
            self.core.popup(msg, severity="info")
            return

        result = self.core.popupQuestion(msg, buttons=["Update All", "Cancel"])
        if result == "Update All":
            for item in outdatedItems:
                idx = item["idx"]
                self.replaceItem(idx, item["latestPath"])
    
    @err_catcher(name=__name__)
    def openRenderDlg(self):
        if hasattr(self, "dlg_render"):
            self.dlg_render.close()

        self.dlg_render = RenderDlg(self)
        self.dlg_render.show()
        return self.dlg_render
    
    @err_catcher(name=__name__)
    def getRenderTemplates(self):
        cmd = """
if (app.project && app.project.activeItem && app.project.activeItem instanceof CompItem) {
    var comp = app.project.activeItem;
    var renderQueueItem = app.project.renderQueue.items.add(comp);
    var outputModule = renderQueueItem.outputModule(1);
    var templateNames = outputModule.templates.join(",")
    renderQueueItem.remove();
    "{\\"result\\": True, \\"templates\\": \\"" + templateNames + "\\"}";
} else {
    "{\\"result\\": False, \\"details\\": \\"No app found.\\"}";
}"""

        result = self.sendCmd(cmd)
        if not result:
            return None

        result = result.decode("utf-8")
        if result == "null":
            return None

        try:
            result = eval(result)
        except:
            result = {"result": False}

        if result["result"] is True:
            templates = [x for x in result["templates"].split(",") if not x.startswith("_HIDDEN") ]
            return templates
        else:
            return None

    @err_catcher(name=__name__)
    def setOutputPath(self, entity, identifier, comment="", composition=None, location="global", template="", useAME=False, outputPath=None):
        extension = ".jpg"
        if self.core.getConfig("globals", "productTasks", config="project"):
            fileName = self.core.getCurrentFileName()
            context = self.core.getScenefileData(fileName)
            entity["department"] = os.getenv("PRISM_AE_DEPARTMENT", context.get("department", "Conform"))
            entity["task"] = os.getenv("PRISM_AE_TASK", context.get("task", "Conform"))

        if not outputPath:
            outputPath = self.core.mediaProducts.generateMediaProductPath(
                entity=entity,
                task=identifier,
                extension=extension,
                comment=comment,
                location=location,
                mediaType="2drenders",
            )

        if not os.path.exists(os.path.dirname(outputPath)):
            try:
                os.makedirs(os.path.dirname(outputPath))
            except:
                self.core.popup("Could not create directory:\n\n%s" % os.path.dirname(outputPath))
                return

        useCurrent = "true" if composition == "Current Composition" else "false"
        if useAME:
            ame = """
    app.project.renderQueue.queueInAME(false)
            """
        else:
            ame = ""

        cmd = """
function getCompositionByName(compName) {
    var project = app.project;
    
    if (project && project.items) {
        for (var i = 1; i <= project.items.length; i++) {
            var item = project.items[i];
            if (item instanceof CompItem && item.name === compName) {
                return item;
            }
        }
    }
    
    return null;
}

var comp = null;
var useCurrent = %s;
if (useCurrent){
    if (app.project && app.project.activeItem && app.project.activeItem instanceof CompItem) {
        comp = app.project.activeItem;
    }
} else {
    comp = getCompositionByName("%s")
}

if (comp) {
    var renderQueueItem = app.project.renderQueue.items.add(comp);
    var outputModule = renderQueueItem.outputModule(1);
    outputModule.file = new File("%s");
    var template = "%s";
    if (template) {
        outputModule.applyTemplate(template);
    }
    %s
    "{\\"result\\": True}";
} else {
    "{\\"result\\": False, \\"details\\": \\"No active composition found.\\"}";
}""" % (useCurrent, composition, outputPath.replace("\\", "/"), template, ame)
        result = self.sendCmd(cmd)
        if not result:
            return None

        result = result.decode("utf-8")
        if result == "null":
            return None

        result = eval(result)
        if result["result"] is True:
            return outputPath
        else:
            return None

    @err_catcher(name=__name__)
    def startRender(self):
        cmd = """
if (app.project && app.project.renderQueue.numItems > 0) {
    app.project.renderQueue.render();
    "{\\"result\\": True, \\"details\\": \\"Render started.\\"}";
} else {
    "{\\"result\\": False, \\"details\\": \\"No items in render queue.\\"}";
}"""

        result = self.sendCmd(cmd)
        if not result:
            return None

        result = result.decode("utf-8")
        if result == "null":
            return None

        result = eval(result)
        if result["result"] is True:
            return result["details"]
        else:
            return None


class RenderDlg(QDialog):
    def __init__(self, plugin):
        super(RenderDlg, self).__init__()
        self.plugin = plugin
        self.core = self.plugin.core
        self.identifiers = []
        self.entity = None
        self.setupUi()
        self.loadSettings()
        curEntity = self.core.getCurrentScenefileData()
        if curEntity and curEntity.get("type"):
            self.setEntity(curEntity)

        self.core.callback(
            "onAfterEffectsRenderDlgCreated", args=[self]
        )

    @err_catcher(name=__name__)
    def setupUi(self):
        self.setWindowTitle("Render Setup")
        self.core.parentWindow(self)
        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        self.lo_widgets = QGridLayout()

        self.lo_entity = QHBoxLayout()
        self.l_entity = QLabel("Entity:")
        self.l_entityName = QLabel("")
        self.b_entity = QPushButton("Choose...")
        self.b_entity.setStyleSheet("color: rgb(240, 50, 50); border-color: rgb(240, 50, 50);")
        self.b_entity.clicked.connect(self.chooseEntity)
        self.b_entity.setFocusPolicy(Qt.NoFocus)
        self.lo_widgets.addWidget(self.l_entity, 0, 0)
        self.lo_widgets.setColumnStretch(1, 1)
        self.lo_widgets.addWidget(self.l_entityName, 0, 1)
        self.lo_widgets.addWidget(self.b_entity, 0, 2, 1, 2)

        self.l_identifier = QLabel("Identifier:    ")
        self.e_identifier = QLineEdit("")
        self.b_identifier = QToolButton()
        self.b_identifier.setFocusPolicy(Qt.NoFocus)
        self.b_identifier.setArrowType(Qt.DownArrow)
        self.b_identifier.clicked.connect(self.showIdentifiers)
        self.b_identifier.setVisible(False)
        self.lo_widgets.addWidget(self.l_identifier, 1, 0)
        self.lo_widgets.addWidget(self.e_identifier, 1, 1, 1, 3)
        self.lo_widgets.addWidget(self.b_identifier, 1, 3)

        self.l_comment = QLabel("Comment:")
        self.e_comment = QLineEdit("")
        self.lo_widgets.addWidget(self.l_comment, 2, 0)
        self.lo_widgets.addWidget(self.e_comment, 2, 1, 1, 3)

        paths = self.core.paths.getRenderProductBasePaths()
        row = 3
        if len(paths) > 1:
            self.l_location = QLabel("Location:")
            self.cb_location = QComboBox()
            self.cb_location.setFocusPolicy(Qt.NoFocus)
            self.lo_widgets.addWidget(self.l_location, row, 0)
            self.lo_widgets.addWidget(self.cb_location, row, 1, 1, 3)
            self.cb_location.addItems(list(paths.keys()))
            row += 1

        comps = self.plugin.getCompositionNames() or []
        comps.insert(0, "Current Composition")
        self.l_composition = QLabel("Composition:")
        self.cb_composition = QComboBox()
        self.cb_composition.setFocusPolicy(Qt.NoFocus)
        self.lo_widgets.addWidget(self.l_composition, row, 0)
        self.lo_widgets.addWidget(self.cb_composition, row, 1, 1, 3)
        self.cb_composition.addItems(comps)
        row += 1

        templates = self.plugin.getRenderTemplates()
        self.chb_template = QCheckBox()
        if templates:
            self.l_template = QLabel("Template:")
            self.w_template = QWidget()
            self.lo_template = QHBoxLayout(self.w_template)
            self.chb_template.setChecked(True)
            self.cb_template = QComboBox()
            self.chb_template.stateChanged.connect(lambda checked: self.cb_template.setEnabled(checked))
            self.cb_template.setFocusPolicy(Qt.NoFocus)
            self.cb_template.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.lo_template.addWidget(self.chb_template)
            self.lo_template.addWidget(self.cb_template)
            self.lo_template.setContentsMargins(0, 0, 0, 0)
            self.lo_widgets.addWidget(self.l_template, row, 0)
            self.lo_widgets.addWidget(self.w_template, row, 1, 1, 3)
            self.cb_template.addItems(templates)
            idx = self.cb_template.findText("H.264 - Match Render Settings - 15 Mbps")
            if idx != -1:
                self.cb_template.setCurrentIndex(idx)

            row += 1

        self.lo_main.addLayout(self.lo_widgets)

        self.bb_main = QDialogButtonBox()
        b_add = self.bb_main.addButton("Add to Render Queue", QDialogButtonBox.AcceptRole)
        b_add.setContextMenuPolicy(Qt.CustomContextMenu)
        b_add.customContextMenuRequested.connect(self.onAddQueueContextMenuRequested)
        self.bb_main.addButton("Render", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Cancel", QDialogButtonBox.RejectRole)

        self.bb_main.clicked.connect(self.buttonClicked)

        self.lo_main.addStretch()
        self.lo_main.addWidget(self.bb_main)

    @err_catcher(name=__name__)
    def onAddQueueContextMenuRequested(self, pos=None):
        pos = QCursor.pos()
        tmenu = QMenu(self)

        tAct = QAction("Add to Media Encoder Render Queue", self)
        tAct.triggered.connect(self.addToAMEQueue)
        tmenu.addAction(tAct)

        tmenu.exec_(pos)

    @err_catcher(name=__name__)
    def addToAMEQueue(self):
        self.buttonClicked("Add to Render Queue", useAME=True)

    @err_catcher(name=__name__)
    def loadSettings(self):
        settings = self.core.getConfig("afterEffects", config="user") or {}
        if "render_entity" in settings:
            self.setEntity(settings["render_entity"])

        if "render_identifier" in settings:
            self.e_identifier.setText(settings["render_identifier"])

        if "render_comment" in settings:
            self.e_comment.setText(settings["render_comment"])

        if "render_location" in settings and hasattr(self, "cb_location"):
            idx = self.cb_location.findText(settings["render_location"])
            if idx != -1:
                self.cb_location.setCurrentIndex(idx)

        if "render_composition" in settings and hasattr(self, "cb_composition"):
            idx = self.cb_composition.findText(settings["render_composition"])
            if idx != -1:
                self.cb_composition.setCurrentIndex(idx)

        if "render_use_template" in settings and hasattr(self, "chb_template"):
            self.chb_template.setChecked(settings["render_use_template"])

        if "render_template" in settings and hasattr(self, "cb_template"):
            idx = self.cb_template.findText(settings["render_template"])
            if idx != -1:
                self.cb_template.setCurrentIndex(idx)

    @err_catcher(name=__name__)
    def sizeHint(self):
        return QSize(400, 250)

    @err_catcher(name=__name__)
    def closeEvent(self, event):
        data = {
            "afterEffects": {
                "render_entity": self.entity,
                "render_identifier": self.e_identifier.text(),
                "render_comment": self.e_comment.text(),
            }
        }

        if hasattr(self, "cb_location"):
            data["afterEffects"]["render_location"] = self.cb_location.currentText()

        if hasattr(self, "cb_composition"):
            data["afterEffects"]["render_composition"] = self.cb_composition.currentText()

        if hasattr(self, "chb_template"):
            data["afterEffects"]["render_use_template"] = self.chb_template.isChecked()

        if hasattr(self, "cb_template"):
            data["afterEffects"]["render_template"] = self.cb_template.currentText()

        self.core.setConfig(data=data, config="user", updateNestedData={"exclude": ["render_entity"]})

    @err_catcher(name=__name__)
    def getIdentifier(self):
        return self.e_identifier.text()

    @err_catcher(name=__name__)
    def getComment(self):
        return self.e_comment.text()

    @err_catcher(name=__name__)
    def getLocation(self):
        if not hasattr(self, "cb_location"):
            return "global"

        return self.cb_location.currentText()

    @err_catcher(name=__name__)
    def getComposition(self):
        return self.cb_composition.currentText()

    @err_catcher(name=__name__)
    def setEntity(self, entity):
        if isinstance(entity, list):
            entity = entity[0]

        entity = entity or {}
        self.entity = entity
        self.b_entity.setStyleSheet("")

        entityType = self.entity.get("type")
        if entityType == "asset":
            entityName = entity.get("asset_path", "")
        elif entityType == "shot":
            entityName = self.core.entities.getShotName(entity)
        else:
            entityName = ""

        self.l_entityName.setText(entityName)
        self.identifiers = self.core.getTaskNames(taskType="2d", context=copy.deepcopy(self.entity), addDepartments=False)
        self.b_identifier.setVisible(bool(self.identifiers))
        if self.identifiers:
            self.lo_widgets.addWidget(self.e_identifier, 1, 1, 1, 2)
        else:
            self.lo_widgets.addWidget(self.e_identifier, 1, 1, 1, 3)

    @err_catcher(name=__name__)
    def chooseEntity(self):
        dlg = EntityDlg(self)
        dlg.w_browser.entered()
        dlg.entitiesSelected.connect(self.setEntity)
        if self.entity:
            dlg.w_browser.w_entities.navigate(self.entity)

        dlg.exec_()

    @err_catcher(name=__name__)
    def showIdentifiers(self):
        pos = QCursor.pos()
        tmenu = QMenu(self)

        for identifier in self.identifiers:
            tAct = QAction(identifier, self)
            tAct.triggered.connect(lambda x=None, t=identifier: self.e_identifier.setText(t))
            tmenu.addAction(tAct)

        tmenu.exec_(pos)

    @err_catcher(name=__name__)
    def validate(self):
        if not self.entity:
            msg = "No entity is selected."
            self.core.popup(msg, parent=self)
            return False

        if not self.getIdentifier():
            msg = "No identifier is specified."
            self.core.popup(msg, parent=self)
            return False

        if not self.plugin.hasActiveComp():
            msg = "No composition is currently active."
            self.core.popup(msg, parent=self)
            return False

        return True

    @err_catcher(name=__name__)
    def saveVersionInfo(self, outputpath):
        identifier = self.getIdentifier()
        comment = self.getComment()
        details = self.entity.copy()
        if "filename" in details:
            del details["filename"]

        if "extension" in details:
            del details["extension"]

        version = self.core.paths.getRenderProductData(outputpath, mediaType="2drenders", isVersionFolder=True).get("version", "")
        fileName = self.core.getCurrentFileName()
        details["sourceScene"] = fileName
        details["identifier"] = identifier
        details["comment"] = comment
        details["version"] = version
        infopath = outputpath

        self.core.saveVersionInfo(
            filepath=infopath, details=details
        )

    @err_catcher(name=__name__)
    def buttonClicked(self, button, useAME=False):
        if self.chb_template.isChecked() and hasattr(self, "cb_template"):
            template = self.cb_template.currentText()
        else:
            template = ""

        if button == "Add to Render Queue" or button.text() == "Add to Render Queue":
            if not self.validate():
                return

            identifier = self.getIdentifier()
            comment = self.getComment()
            composition = self.getComposition()
            location = self.getLocation()
            outputpath = self.plugin.setOutputPath(
                entity=self.entity,
                identifier=identifier,
                comment=comment,
                composition=composition,
                location=location,
                template=template,
                useAME=useAME,
            )
            self.saveVersionInfo(os.path.dirname(outputpath))
        elif button.text() == "Render":
            if not self.validate():
                return

            identifier = self.getIdentifier()
            comment = self.getComment()
            composition = self.getComposition()
            location = self.getLocation()

            rSettings = {
                "identifier": identifier,
                "comment": comment,
                "composition": composition,
                "location": location,
            }
            kwargs = {
                "origin": self,
                "settings": rSettings,
            }
            result = self.core.callback("preRender", **kwargs)
            outputName = None
            for res in result:
                if isinstance(res, dict) and res.get("cancel", False):
                    return [
                        self.state.text(0)
                        + " - error - %s" % res.get("details", "preRender hook returned False")
                    ]

                if res and "outputName" in res:
                    outputName = res["outputName"]

            outputpath = self.plugin.setOutputPath(
                entity=self.entity,
                identifier=identifier,
                comment=comment,
                composition=composition,
                location=location,
                template=template,
                outputPath=outputName,
            )
            if not outputpath:
                return

            self.saveVersionInfo(os.path.dirname(outputpath))
            with self.core.waitPopup(self.core, "Rendering. Please wait..."):
                result = self.plugin.startRender()

            kwargs = {
                "settings": rSettings,
                "outputpath": outputpath,
                "result": result,
            }

            self.core.callback("postRender", **kwargs)
            base, ext = os.path.splitext(outputpath)
            globPath = base.strip("#") + "*"
            files = glob.glob(globPath)
            if files:
                msg = "Finished rendering successfully."
                result = self.core.popupQuestion(msg, buttons=["Open in Project Browser", "Open in Explorer", "Close"], icon=QMessageBox.Information, parent=self)
                if result == "Open in Project Browser":
                    pb = self.core.projectBrowser()
                    pb.showTab("Media")
                    pb.refreshUI()
                    pb.mediaBrowser.showRender(self.entity, identifier + " (2d)")

                elif result == "Open in Explorer":

                    self.core.openFolder(files[0])
            else:
                msg = "Render failed. The expected mediafile doesn't exist:\n\n%s" % globPath
                self.core.popup(msg, parent=self)

            self.close()
        else:
            self.close()


class ImportMediaDlg(QDialog):
    def __init__(self, plugin):
        super(ImportMediaDlg, self).__init__()
        self.plugin = plugin
        self.core = self.plugin.core
        self.identifiers = []
        self.shots = None
        self.setupUi()

    @err_catcher(name=__name__)
    def setupUi(self):
        self.setWindowTitle("Import Media")
        self.core.parentWindow(self)
        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        self.lo_widgets = QGridLayout()

        self.lo_entity = QHBoxLayout()
        self.l_entity = QLabel("Shots:")
        self.l_entityName = QLabel("")
        self.l_entityName.setWordWrap(True)
        self.b_entity = QPushButton("Choose...")
        self.b_entity.setStyleSheet("color: rgb(240, 50, 50); border-color: rgb(240, 50, 50);")
        self.b_entity.clicked.connect(self.chooseEntity)
        self.b_entity.setFocusPolicy(Qt.NoFocus)
        self.lo_widgets.addWidget(self.l_entity, 0, 0)
        self.lo_widgets.setColumnStretch(1, 1)
        self.lo_widgets.addWidget(self.l_entityName, 0, 1)
        self.lo_widgets.addWidget(self.b_entity, 0, 2, 1, 2)

        self.l_identifier = QLabel("Identifier:    ")
        self.e_identifier = QLineEdit("")
        self.b_identifier = QToolButton()
        self.b_identifier.setFocusPolicy(Qt.NoFocus)
        self.b_identifier.setArrowType(Qt.DownArrow)
        self.b_identifier.clicked.connect(self.showIdentifiers)
        self.b_identifier.setVisible(False)
        self.lo_widgets.addWidget(self.l_identifier, 1, 0)
        self.lo_widgets.addWidget(self.e_identifier, 1, 1, 1, 3)
        self.lo_widgets.addWidget(self.b_identifier, 1, 3)

        self.l_addToComp = QLabel("Add to Current Composition:")
        self.chb_addToComp = QCheckBox()
        self.chb_addToComp.setChecked(True)
        self.lo_widgets.addWidget(self.l_addToComp, 2, 0)
        self.lo_widgets.addWidget(self.chb_addToComp, 2, 1, 1, 3)

        self.lo_main.addLayout(self.lo_widgets)

        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Preview", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Import", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Cancel", QDialogButtonBox.RejectRole)

        self.bb_main.clicked.connect(self.buttonClicked)

        self.lo_main.addStretch()
        self.lo_main.addWidget(self.bb_main)

    @err_catcher(name=__name__)
    def sizeHint(self):
        return QSize(400, 150)

    @err_catcher(name=__name__)
    def getIdentifiers(self):
        return [x.strip() for x in self.e_identifier.text().split(",")]

    @err_catcher(name=__name__)
    def setShots(self, shots):
        if not isinstance(shots, list):
            shots = [shots]

        self.shots = shots
        self.b_entity.setStyleSheet("")

        shotNames = []
        self.identifiers = []
        identifiers = []
        for shot in self.shots:
            shotName = self.core.entities.getShotName(shot)
            if not shotName:
                continue

            shotNames.append(shotName)
            taskTypes = ["3d", "2d", "playblast", "external"]
            for taskType in taskTypes:
                ids = self.core.getTaskNames(taskType=taskType, context=copy.deepcopy(shot), addDepartments=False)
                if taskType == "playblast":
                    ids = [i + " (playblast)" for i in ids if i]
                elif taskType == "2d":
                    ids = [i + " (2d)" for i in ids if i]
                elif taskType == "external":
                    ids = [i + " (external)" for i in ids if i]

                identifiers += ids

        self.identifiers = sorted(list(set(identifiers)))
        shotStr = ", ".join(shotNames)
        self.l_entityName.setText(shotStr)

        self.b_identifier.setVisible(bool(self.identifiers))
        if self.identifiers:
            self.lo_widgets.addWidget(self.e_identifier, 1, 1, 1, 2)
        else:
            self.lo_widgets.addWidget(self.e_identifier, 1, 1, 1, 3)

    @err_catcher(name=__name__)
    def chooseEntity(self):
        dlg = EntityDlg(self)
        dlg.w_browser.w_entities.getPage("Shots").tw_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        dlg.w_browser.w_entities.tb_entities.removeTab(0)
        dlg.w_browser.w_entities.navigate({"type": "shot"})
        dlg.w_browser.entered(navData={"type": "shot"})
        dlg.entitiesSelected.connect(self.setShots)
        if self.shots:
            dlg.w_browser.w_entities.navigate(self.shots)

        dlg.exec_()

    @err_catcher(name=__name__)
    def showIdentifiers(self):
        pos = QCursor.pos()
        tmenu = QMenu(self)

        for identifier in self.identifiers:
            tAct = QAction(identifier, self)
            tAct.triggered.connect(lambda x=None, t=identifier: self.addIdentifier(t))
            tmenu.addAction(tAct)

        tmenu.exec_(pos)

    @err_catcher(name=__name__)
    def addIdentifier(self, identifier):
        idfs = [idf.strip() for idf in self.e_identifier.text().split(",") if idf]
        if identifier in idfs:
            newIdfs = [idf for idf in idfs if idf != identifier]
        else:
            newIdfs = idfs + [identifier]

        self.e_identifier.setText(", ".join(newIdfs))

    @err_catcher(name=__name__)
    def validate(self):
        if not self.shots:
            msg = "No shots are selected."
            self.core.popup(msg, parent=self)
            return False

        if not self.getIdentifiers():
            msg = "No identifier is specified."
            self.core.popup(msg, parent=self)
            return False

        return True

    @err_catcher(name=__name__)
    def buttonClicked(self, button):
        if button.text() == "Import":
            if not self.validate():
                return

            identifiers = self.getIdentifiers()
            result = self.plugin.importMediaVersions(entities=self.shots, identifiers=identifiers, addToComp=self.chb_addToComp.isChecked())
            if not result and not isinstance(result, list) and result is not False:
                msg = "Importing media failed."
                self.core.popup(msg, parent=self)

            self.close()
        elif button.text() == "Preview":
            if not self.validate():
                return

            versions = []
            identifiers = self.getIdentifiers()
            for identifier in identifiers:
                versions += self.plugin.getMediaFromEntities(entities=self.shots, identifier=identifier)

            if self.chb_addToComp.isChecked():
                msg = "The following media will be added to the current composition:\n\n"
            else:
                msg = "The following media will be added as sources to the current project:\n\n"

            for version in versions:
                shotName = self.core.entities.getShotName(version)
                pattern = self.core.media.getSequenceFromFilename(version["filepaths"][0])
                line = "Shot: %s\nPath: %s\n" % (shotName, pattern)
                msg += line

            self.core.popup(msg, parent=self, severity="info")
        else:
            self.close()


class EntityDlg(QDialog):

    entitiesSelected = Signal(object)

    def __init__(self, parent):
        super(EntityDlg, self).__init__()
        self.parentDlg = parent
        self.plugin = self.parentDlg.plugin
        self.core = self.plugin.core
        self.setupUi()

    @err_catcher(name=__name__)
    def setupUi(self):
        title = "Choose Shots"

        self.setWindowTitle(title)
        self.core.parentWindow(self, parent=self.parentDlg)

        import MediaBrowser
        self.w_browser = MediaBrowser.MediaBrowser(core=self.core, refresh=False)
        self.w_browser.w_entities.getPage("Assets").tw_tree.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.w_browser.w_entities.getPage("Shots").tw_tree.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.setExpanded(False)

        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Select", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.b_expand = self.bb_main.addButton("▶", QDialogButtonBox.RejectRole)
        self.b_expand.setToolTip("Expand")

        self.bb_main.clicked.connect(self.buttonClicked)

        self.lo_main.addWidget(self.w_browser)
        self.lo_main.addWidget(self.bb_main)

    @err_catcher(name=__name__)
    def itemDoubleClicked(self, item, column):
        self.buttonClicked("select")

    @err_catcher(name=__name__)
    def buttonClicked(self, button):
        if button == "select" or button.text() == "Select":
            entities = self.w_browser.w_entities.getCurrentData(returnOne=False)
            if isinstance(entities, dict):
                entities = [entities]

            validEntities = []
            for entity in entities:
                if entity.get("type", "") not in ["asset", "shot"]:
                    continue

                validEntities.append(entity)

            if not validEntities:
                msg = "Invalid entity selected."
                self.core.popup(msg, parent=self)
                return

            self.entitiesSelected.emit(validEntities)
        elif button.text() == "▶":
            self.setExpanded(True)
            button.setVisible(False)
            return

        self.close()

    @err_catcher(name=__name__)
    def setExpanded(self, expand):
        self.w_browser.w_identifier.setVisible(expand)
        self.w_browser.w_version.setVisible(expand)
        self.w_browser.w_preview.setVisible(expand)

        if expand:
            newwidth = 1200
            curwidth = self.geometry().width()
            self.resize(newwidth, self.geometry().height())
            self.move(self.pos().x()-((newwidth-curwidth)/2), self.pos().y())

    @err_catcher(name=__name__)
    def sizeHint(self):
        return QSize(500, 500)
