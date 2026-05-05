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
import time
import traceback
import logging
import tempfile

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher as err_catcher

import c4d


logger = logging.getLogger(__name__)


class Prism_Cinema4D_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.exportHandlers = {
            ".abc": {"exportFunction": self.exportAlembic},
            ".fbx": {"exportFunction": self.exportFBX},
            ".obj": {"exportFunction": self.exportObj},
            ".rs": {"exportFunction": self.exportRs},
            ".c4d": {"exportFunction": self.exportC4d},
        }
        scripts_folder = os.path.join(c4d.storage.GeGetC4DPath(c4d.C4D_PATH_LIBRARY), "scripts")
        if scripts_folder not in sys.path:
            sys.path.append(scripts_folder)

        try:
            import arnold
            hasArnold = True
        except:
            hasArnold = False

        if hasArnold:
            self.exportHandlers[".ass"] = {"exportFunction": self.exportAss}
        else:
            if ".ass" in self.outputFormats:
                self.outputFormats.remove(".ass")

        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self.plugin)
        self.core.registerCallback(
            "prePlayblast", self.prePlayblast, plugin=self.plugin
        )

    @err_catcher(name=__name__)
    def startup(self, origin):
        origin.timer.stop()
        appIcon = QIcon(self.appIcon)
        qapp = QApplication.instance()
        qapp.setWindowIcon(appIcon)

        origin.messageParent = QWidget()
        self.core.setActiveStyleSheet("Cinema4D")
        if self.core.useOnTop:
            origin.messageParent.setWindowFlags(
                origin.messageParent.windowFlags() ^ Qt.WindowStaysOnTopHint
            )

        origin.startAutosaveTimer()

    @err_catcher(name=__name__)
    def pluginMessage(self, id, data):
        if id == c4d.C4DPL_BUILDMENU:
            mainMenu = c4d.gui.GetMenuResource("M_EDITOR")
            pluginsMenu = c4d.gui.SearchPluginMenuResource()

            menu = c4d.BaseContainer()
            menu.InsData(c4d.MENURESOURCE_SUBTITLE, "Prism")
            menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_1063247")
            menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_1063248")
            menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_1063249")
            menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_1063250")
            menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_1063251")

            if pluginsMenu:
                mainMenu.InsDataAfter(c4d.MENURESOURCE_STRING, menu, pluginsMenu)
            else:
                mainMenu.InsData(c4d.MENURESOURCE_STRING, menu)

    @err_catcher(name=__name__)
    def autosaveEnabled(self, origin):
        return c4d.plugins.FindPlugin(465001626, c4d.PLUGINTYPE_PREFS)[c4d.PREF_FILE_AUTOEVERY]

    @err_catcher(name=__name__)
    def sceneOpen(self, origin):
        if self.core.shouldAutosaveTimerRun():
            origin.startAutosaveTimer()

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin, path=True):
        doc = c4d.documents.GetActiveDocument()
        if not doc:
            return ""

        if path:
            return "%s/%s" % (doc.GetDocumentPath(), doc.GetDocumentName())
        else:
            return doc.GetDocumentName()

    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        return self.sceneFormats[0]

    @err_catcher(name=__name__)
    def saveScene(self, origin, filepath, details={}):
        doc = c4d.documents.GetActiveDocument()
        doc.SetDocumentPath(os.path.dirname(filepath))
        doc.SetDocumentName(os.path.basename(filepath))
        result = c4d.documents.SaveDocument(doc, filepath, c4d.SAVEDOCUMENTFLAGS_0, c4d.FORMAT_C4DEXPORT) 
        self.core.scenefileSaved()
        return result

    @err_catcher(name=__name__)
    def getImportPaths(self, origin):
        doc = c4d.documents.GetActiveDocument()
        if not doc:
            return

        cid, value, bc = self.findUserDataByName(doc, "PrismImports")
        if not value or len(value) == 0:
            return False

        return value

    @err_catcher(name=__name__)
    def getFrameRange(self, origin):
        doc = c4d.documents.GetActiveDocument()
        startframe = doc.GetMinTime().GetFrame(doc.GetFps())
        endframe = doc.GetMaxTime().GetFrame(doc.GetFps())
        return [startframe, endframe]

    @err_catcher(name=__name__)
    def setFrameRange(self, origin, startFrame, endFrame):
        doc = c4d.documents.GetActiveDocument()
        doc.SetMinTime(c4d.BaseTime(startFrame/doc.GetFps()))
        doc.SetMaxTime(c4d.BaseTime(endFrame/doc.GetFps()))
        doc.SetLoopMinTime(c4d.BaseTime(startFrame/doc.GetFps()))
        doc.SetLoopMaxTime(c4d.BaseTime(endFrame/doc.GetFps()))

    @err_catcher(name=__name__)
    def getFPS(self, origin):
        doc = c4d.documents.GetActiveDocument()
        fps = doc.GetFps()
        return fps

    @err_catcher(name=__name__)
    def setFPS(self, origin, fps):
        doc = c4d.documents.GetActiveDocument()
        doc.SetFps(int(fps))

    @err_catcher(name=__name__)
    def getResolution(self):
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
        width = rd.GetDataInstance()[c4d.RDATA_XRES]
        height = rd.GetDataInstance()[c4d.RDATA_YRES]
        return [width, height]

    @err_catcher(name=__name__)
    def setResolution(self, width=None, height=None):
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
        if width:
            rd[c4d.RDATA_XRES] = width
        if height:
            rd[c4d.RDATA_YRES] = height

    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        return c4d.GetC4DVersion()

    @err_catcher(name=__name__)
    def getProgramVersion(self, origin):
        return c4d.GetC4DVersion()

    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        c4d.documents.LoadFile(filepath)
        self.core.sceneOpen()
        return True

    @err_catcher(name=__name__)
    def sm_export_addObjects(self, origin, objects=None):
        if not objects:
            doc = c4d.documents.GetActiveDocument()
            objects = doc.GetSelection()

        for obj in objects:
            if not hasattr(obj, "GetGUID"):
                continue

            guid = obj.GetGUID()
            if guid not in origin.nodes:
                origin.nodes.append(guid)

        origin.updateUi()
        origin.stateManager.saveStatesToScene()

    @err_catcher(name=__name__)
    def getNodeName(self, origin, guid):
        if isinstance(guid, int):
            node = self.getObject(guid)
        else:
            node = guid

        if self.isNodeValid(origin, node):
            try:
                return node.GetName()
            except:
                return node
        else:
            return "invalid"

    @err_catcher(name=__name__)
    def getObject(self, node):
        doc = c4d.documents.GetActiveDocument()
        obj = doc.GetFirstObject()
        while obj:
            result = self.findObjByGuid(obj, node)
            if result:
                return result

            obj = obj.GetNext()

    @err_catcher(name=__name__)
    def findObjByGuid(self, obj, guid):        
        if obj.GetGUID() == guid:
            return obj
        
        # Traverse the children of the current object
        child = obj.GetDown()
        while child:
            result = self.findObjByGuid(child, guid)
            if result:
                return result

            child = child.GetNext()

    @err_catcher(name=__name__)
    def selectNodes(self, origin):
        if not origin.lw_objects.selectedItems():
            return

        doc = c4d.documents.GetActiveDocument()
        doc.SetActiveObject(None, c4d.SELECTION_NEW)
        for item in origin.lw_objects.selectedItems():
            guid = origin.nodes[origin.lw_objects.row(item)]
            node = self.getObject(guid)
            if self.isNodeValid(origin, node):
                doc.SetActiveObject(node, c4d.SELECTION_ADD)

        c4d.EventAdd()

    @err_catcher(name=__name__)
    def isNodeValid(self, origin, handle):
        if isinstance(handle, int):
            handle = self.getObject(handle)

        return bool(handle)

    @err_catcher(name=__name__)
    def getAllCamerasRecursive(self, obj, cameras):
        if obj.GetTypeName() in ["RS Camera", "Camera"]:
            cameras.append(obj.GetGUID())
        
        child = obj.GetDown()
        while child:
            self.getAllCamerasRecursive(child, cameras)
            child = child.GetNext()

    @err_catcher(name=__name__)
    def getCamNodes(self, origin, cur=False):
        sceneCams = []
        doc = c4d.documents.GetActiveDocument()
        obj = doc.GetFirstObject()

        while obj:
            self.getAllCamerasRecursive(obj, sceneCams)            
            obj = obj.GetNext()

        if cur:
            sceneCams = ["Current View"] + sceneCams

        return sceneCams

    @err_catcher(name=__name__)
    def getCamName(self, origin, handle):
        if handle == "Current View":
            return handle

        return self.getNodeName(origin, handle)

    @err_catcher(name=__name__)
    def selectCam(self, origin):
        if self.isNodeValid(origin, self.getObject(origin.curCam)):
            doc = c4d.documents.GetActiveDocument()
            doc.SetActiveObject(None, c4d.SELECTION_NEW)
            doc.SetActiveObject(self.getObject(origin.curCam), c4d.SELECTION_ADD)
            c4d.EventAdd()

    @err_catcher(name=__name__)
    def onStateManagerOpen(self, origin):
        origin.resize(origin.width() + 50, origin.height())

    @err_catcher(name=__name__)
    def sm_export_startup(self, origin):
        origin.f_objectList.setStyleSheet(
            "QFrame { border: 0px solid rgb(150,150,150); }"
        )
        if hasattr(origin, "w_additionalOptions"):
            origin.w_additionalOptions.setVisible(False)

    @err_catcher(name=__name__)
    def sm_export_exportShotcam(self, origin, startFrame, endFrame, outputName):
        result = self.sm_export_exportAppObjects(
            origin,
            startFrame,
            endFrame,
            (outputName + ".abc"),
            nodes=[origin.curCam],
            expType=".abc",
        )
        result = self.sm_export_exportAppObjects(
            origin,
            startFrame,
            endFrame,
            (outputName + ".fbx"),
            nodes=[origin.curCam],
            expType=".fbx",
        )
        return result

    @err_catcher(name=__name__)
    def sm_export_exportAppObjects(
        self,
        origin,
        startFrame,
        endFrame,
        outputName,
        scaledExport=False,
        nodes=None,
        expType=None,
    ):
        expNodes = origin.nodes
        doc = c4d.documents.GetActiveDocument()
        doc.SetActiveObject(None, c4d.SELECTION_NEW)

        expObjs = [self.getObject(expNode) for expNode in expNodes]
        for expObj in expObjs:
            if self.isNodeValid(origin, expObj):
                doc.SetActiveObject(expObj, c4d.SELECTION_ADD)

        ext = origin.getOutputType()
        if ext in self.exportHandlers:
            outputName = self.exportHandlers[ext]["exportFunction"](
                outputName, origin, startFrame, endFrame, expObjs
            )
        else:
            msg = "Canceled: Format \"%s\" is not supported." % ext
            return msg

        doc.SetActiveObject(None, c4d.SELECTION_NEW)
        return outputName

    @err_catcher(name=__name__)
    def exportObj(self, outputName, origin, startFrame, endFrame, expNodes):
        doc = c4d.documents.GetActiveDocument()
        plugin_id = c4d.FORMAT_OBJ2EXPORT
        plug = c4d.plugins.FindPlugin(plugin_id, c4d.PLUGINTYPE_SCENESAVER)
        if plug is None:
            self.core.popup("Failed to retrieve the alembic exporter.")
            return

        data = dict()
        if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
            self.core.popup("Failed to retrieve private data.")
            return

        exportSettings = data.get("imexporter", None)
        if exportSettings is None:
            self.core.popup("Failed to retrieve BaseContainer private data.")
            return

        for frame in range(startFrame, endFrame + 1):
            fps = doc.GetFps()
            time = c4d.BaseTime(frame, fps)
            doc.SetTime(time)
            c4d.EventAdd()

            foutputName = outputName.replace("####", format(frame, "04"))
            if c4d.documents.SaveDocument(doc, foutputName, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, plugin_id):
                logger.info(f"Document successfully exported to {foutputName}")
            else:
                logger.info(f"Failed to export document to {foutputName}")

        outputName = foutputName
        return outputName

    @err_catcher(name=__name__)
    def exportFBX(self, outputName, origin, startFrame, endFrame, expNodes):
        doc = c4d.documents.GetActiveDocument()
        plugin_id = c4d.FORMAT_FBX_EXPORT
        plug = c4d.plugins.FindPlugin(plugin_id, c4d.PLUGINTYPE_SCENESAVER)
        if plug is None:
            self.core.popup("Failed to retrieve the fbx exporter.")
            return

        data = dict()
        if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
            self.core.popup("Failed to retrieve private data.")
            return

        exportSettings = data.get("imexporter", None)
        if exportSettings is None:
            self.core.popup("Failed to retrieve BaseContainer private data.")
            return

        exportSettings[c4d.FBXEXPORT_SELECTION_ONLY] = not origin.chb_wholeScene.isChecked()

        if c4d.documents.SaveDocument(doc, outputName, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, plugin_id):
            logger.info(f"Document successfully exported to {outputName}")
        else:
            logger.info(f"Failed to export document to {outputName}")

        return outputName

    @err_catcher(name=__name__)
    def exportAlembic(self, outputName, origin, startFrame, endFrame, expNodes):
        doc = c4d.documents.GetActiveDocument()
        plugin_id = c4d.FORMAT_ABCEXPORT
        plug = c4d.plugins.FindPlugin(plugin_id, c4d.PLUGINTYPE_SCENESAVER)
        if plug is None:
            self.core.popup("Failed to retrieve the alembic exporter.")
            return

        data = dict()
        if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
            self.core.popup("Failed to retrieve private data.")
            return

        exportSettings = data.get("imexporter", None)
        if exportSettings is None:
            self.core.popup("Failed to retrieve BaseContainer private data.")
            return

        exportSettings[c4d.ABCEXPORT_SELECTION_ONLY] = not origin.chb_wholeScene.isChecked()
        exportSettings[c4d.ABCEXPORT_FRAME_START] = startFrame
        exportSettings[c4d.ABCEXPORT_FRAME_END] = endFrame

        if c4d.documents.SaveDocument(doc, outputName, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, plugin_id):
            logger.info(f"Document successfully exported to {outputName}")
        else:
            logger.info(f"Failed to export document to {outputName}")

        return outputName

    @err_catcher(name=__name__)
    def exportRs(self, outputName, origin, startFrame, endFrame, expNodes):
        doc = c4d.documents.GetActiveDocument()
        import redshift as rs
        plugin_id = rs.Frsproxyexport
        plug = c4d.plugins.FindPlugin(plugin_id, c4d.PLUGINTYPE_SCENESAVER)
        if plug is None:
            self.core.popup("Failed to retrieve the rsproxy exporter.")
            return

        data = dict()
        if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
            self.core.popup("Failed to retrieve private data.")
            return

        exportSettings = data.get("imexporter", None)
        if exportSettings is None:
            self.core.popup("Failed to retrieve BaseContainer private data.")
            return

        exportSettings[c4d.REDSHIFT_PROXYEXPORT_OBJECTS_SELECTION] = not origin.chb_wholeScene.isChecked()
        exportSettings[c4d.REDSHIFT_PROXYEXPORT_ANIMATION_FRAME_START] = startFrame
        exportSettings[c4d.REDSHIFT_PROXYEXPORT_ANIMATION_FRAME_END] = endFrame
        exportSettings[c4d.REDSHIFT_PROXYEXPORT_ORIGIN] = c4d.REDSHIFT_PROXYEXPORT_ORIGIN_WORLD
        exportSettings[c4d.REDSHIFT_PROXYEXPORT_SCALE] = doc[c4d.DOCUMENT_DOCUNIT]

        if c4d.documents.SaveDocument(doc, outputName, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, plugin_id):
            logger.info(f"Document successfully exported to {outputName}")
        else:
            logger.info(f"Failed to export document to {outputName}")

        return outputName

    @err_catcher(name=__name__)
    def exportAss(self, outputName, origin, startFrame, endFrame, expNodes):
        import arnold.scene as arnold_scene
        doc = c4d.documents.GetActiveDocument()
        if origin.chb_wholeScene.isChecked():
            objectMode = arnold_scene.SCENE_EXPORT_OBJECT_MODE_ALL
        else:
            objectMode = arnold_scene.SCENE_EXPORT_OBJECT_MODE_SELECTED

        try:
            arnold_scene.Export(
                doc=doc,
                filename=outputName,
                fileFormat=arnold_scene.SCENE_EXPORT_FORMAT_ASS,
                compressed=False,
                bbox=True,
                binary=False,
                expandProcedurals=False,
                startFrame=int(startFrame),
                endFrame=int(endFrame),
                stepFrame=1,
                mask=0x001C,  # Export Lights, Shapes, and Shaders
                objectMode=objectMode,
                exportObjectHierarchy=True,
                replaceWithProcedural=False
            )
        except Exception as e:
            self.core.popup("Error exporting Arnold ASS file: %s" % str(e))
            return

        return outputName

    @err_catcher(name=__name__)
    def exportC4d(self, outputName, origin, startFrame, endFrame, expNodes):
        doc = c4d.documents.GetActiveDocument()
        plugin_id = c4d.FORMAT_C4DEXPORT
        plug = c4d.plugins.FindPlugin(plugin_id, c4d.PLUGINTYPE_SCENESAVER)
        if plug is None:
            self.core.popup("Failed to retrieve the c4d exporter.")
            return

        data = dict()
        if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
            self.core.popup("Failed to retrieve private data.")
            return

        exportSettings = data.get("imexporter", None)
        if exportSettings is None:
            self.core.popup("Failed to retrieve BaseContainer private data.")
            return

        if c4d.documents.SaveDocument(doc, outputName, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, plugin_id):
            logger.info(f"Document successfully exported to {outputName}")
        else:
            logger.info(f"Failed to export document to {outputName}")

        return outputName

    @err_catcher(name=__name__)
    def sm_export_preExecute(self, origin, startFrame, endFrame):
        warnings = []
        return warnings

    @err_catcher(name=__name__)
    def sm_render_startup(self, origin):
        origin.gb_passes.setHidden(True)
        if hasattr(origin, "f_renderLayer"):
            origin.f_renderLayer.setVisible(True)

        origin.l_renderLayer.setText("Take:")

    @err_catcher(name=__name__)
    def sm_render_getRenderLayer(self, origin):
        rlayers = self.getTakesFromScene()
        rlayerNames = ["Current"]
        for rlayer in rlayers:
            rlayerNames.append(rlayer.GetName())

        rlayerNames += [
            "All Checked Takes",
            "All Checked Takes (separate identifiers)",
            "All Takes",
            "All Takes (separate identifiers)"
        ]
        return rlayerNames

    @err_catcher(name=__name__)
    def sm_render_getIdentifiers(self, origin):
        layer = self.getSelectedTake(origin)
        if layer == "All Checked Takes (separate identifiers)":
            rlayers = self.getTakesFromScene() or []
            rrlayers = []
            for layer in rlayers:
                if layer.IsChecked():
                    rrlayers.append(layer)

            rlayers = rrlayers
        elif layer == "All Takes (separate identifiers)":
            rlayers = self.getTakesFromScene() or []
        else:
            return

        rlayers = [rlayer.GetName() for rlayer in rlayers]
        return rlayers

    @err_catcher(name=__name__)
    def sm_render_getLayers(self, origin):
        layer = self.getSelectedTake(origin)
        if layer == "All Checked Takes":
            rlayers = self.getTakesFromScene() or []
            rrlayers = []
            for layer in rlayers:
                if layer.IsChecked():
                    rrlayers.append(layer)

            rlayers = rrlayers
        elif layer == "All Takes":
            rlayers = self.getTakesFromScene() or []
        else:
            return

        rlayers = [rlayer.GetName() for rlayer in rlayers]
        return rlayers

    @err_catcher(name=__name__)
    def getSelectedTake(self, origin):
        return origin.cb_renderLayer.currentText()

    @err_catcher(name=__name__)
    def sm_render_updateUi(self, origin):
        multipleLayers = self.getSelectedTake(origin) in ["All Checked Takes (separate identifiers)", "All Takes (separate identifiers)"]
        origin.f_taskname.setEnabled(not multipleLayers)
        if multipleLayers:
            origin.setTaskWarn(False)
        else:
            origin.setTaskWarn(not bool(origin.getTaskname()))

    @err_catcher(name=__name__)
    def getAdditionalRenderContext(self, origin, context=None, identifier=None, layer=None):
        selRenderLayer = origin.cb_renderLayer.currentText()
        if selRenderLayer in ["All Checked Takes (separate identifiers)", "All Takes (separate identifiers)"]:
            selRenderLayer = identifier
        elif selRenderLayer in ["All Checked Takes", "All Takes"]:
            selRenderLayer = layer

        if selRenderLayer == "Main":
            return

        return {"layer": selRenderLayer}

    @err_catcher(name=__name__)
    def sm_render_preSubmit(self, origin, rSettings):
        renderTake = self.getSelectedTake(origin)
        if renderTake in ["All Checked Takes (separate identifiers)", "All Takes (separate identifiers)"]:
            renderTake = rSettings["identifier"]
        elif renderTake in ["All Checked Takes", "All Takes"]:
            renderTake = rSettings["layer"]

        for take in self.getTakesFromScene():
            if take.GetName() == renderTake:
                doc = c4d.documents.GetActiveDocument()
                takeData = doc.GetTakeData()
                takeData.SetCurrentTake(take)

        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
        bc = rd.GetDataInstance()

        rendererId = c4d.documents.GetActiveDocument().GetActiveRenderData()[c4d.RDATA_RENDERENGINE]
        renderer = c4d.plugins.FindPlugin(rendererId, c4d.PLUGINTYPE_ANY)
        if renderer:
            rendererName = renderer.GetName()
        else:
            rendererName = ""

        if rendererName == "Arnold Renderer":
            prism_path = rSettings["outputName"]
            beauty_path = prism_path.rsplit(".", 1)[0] + ".."
            crypto_path = prism_path.replace("beauty", "crypto").rsplit(".", 1)[0] + ".."
            bc.SetFilename(c4d.RDATA_PATH, beauty_path)
            bc.SetFilename(c4d.RDATA_MULTIPASS_FILENAME, crypto_path)
            rSettings["outputName"] = beauty_path + rSettings["outputName"].rsplit(".", 1)[1]
            original_format = bc.GetInt32(c4d.RDATA_FORMAT)
            bc.SetInt32(c4d.RDATA_FORMAT, original_format)
        elif rendererName == "V-Ray":
            
            bc.SetFilename(c4d.RDATA_PATH, rSettings["outputName"])
            bc.SetBool(c4d.RDATA_GLOBALSAVE, True)
            bc.SetBool(c4d.RDATA_SAVEIMAGE, True)
            base, ext = os.path.splitext(rSettings["outputName"].lower())
            if ext == ".exr":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_EXR)
            elif ext == ".png":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_PNG)
            elif ext == ".jpg":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_JPG)

            ID_VRAY_VIDEOPOST = 1053272
            VRAY_VP_OUTPUT_SETTINGS_FILENAME = 1000403
            if not doc:
                raise Exception("No active document found.")
            if not rd:
                raise Exception("No render settings found.")

            vp = rd.GetFirstVideoPost()
            while vp:
                if vp.GetType() == ID_VRAY_VIDEOPOST:
                    break

                vp = vp.GetNext()

            if not vp:
                raise Exception("V-Ray VideoPost not found.")

            doc.StartUndo()
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, vp)
            vray_path = rSettings["outputName"].replace("beauty", "mp")
            vray_path = vray_path.replace("..", ".$frame.")
            vp[VRAY_VP_OUTPUT_SETTINGS_FILENAME] = vray_path
            doc.EndUndo()
            c4d.EventAdd()

        else:
            bc.SetFilename(c4d.RDATA_PATH, rSettings["outputName"])
            bc.SetBool(c4d.RDATA_GLOBALSAVE, True)
            bc.SetBool(c4d.RDATA_SAVEIMAGE, True)
            base, ext = os.path.splitext(rSettings["outputName"].lower())
            if ext == ".exr":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_EXR)
            elif ext == ".png":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_PNG)
            elif ext == ".jpg":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_JPG)

        rd.SetData(bc)

    @err_catcher(name=__name__)
    def sm_render_fixOutputPath(self, origin, outputName, singleFrame=False, state=None):
        base = os.path.splitext(outputName)[0].strip("#.")
        if not singleFrame:
            base += "."

        outputName = base + os.path.splitext(outputName)[1]

        return outputName

    @err_catcher(name=__name__)
    def sm_render_startLocalRender(self, origin, outputName, rSettings):
        if origin.chb_resOverride.isChecked():
            resolution = self.getResolution()

            rSettings["width"] = resolution[0]
            rSettings["height"] = resolution[1]

            self.setResolution(
                origin.sp_resWidth.value(),
                origin.sp_resHeight.value(),
            )

        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
        if origin.curCam and origin.curCam != "Current View":
            bd = doc.GetActiveBaseDraw()
            bd.SetSceneCamera(self.getObject(origin.curCam))

        if rSettings["startFrame"] is None:
            frameChunks = [[x, x] for x in rSettings["frames"]]
        else:
            frameChunks = [[rSettings["startFrame"], rSettings["endFrame"]]]

        singleFrame = rSettings["rangeType"] == "Single Frame"
        try:
            for frameChunk in frameChunks:
                bc = rd.GetDataInstance()
                if singleFrame:
                    bc.SetInt32(c4d.RDATA_FRAMESEQUENCE, c4d.RDATA_FRAMESEQUENCE_CURRENTFRAME)
                else:
                    bc.SetInt32(c4d.RDATA_FRAMESEQUENCE, c4d.RDATA_FRAMESEQUENCE_MANUAL)

                bc.SetTime(c4d.RDATA_FRAMEFROM, c4d.BaseTime(frameChunk[0], doc.GetFps()))
                bc.SetTime(c4d.RDATA_FRAMETO, c4d.BaseTime(frameChunk[1], doc.GetFps()))
                bc.SetInt32(c4d.RDATA_FRAMERATE, doc.GetFps())
                rd.SetData(bc)

                bmp = c4d.bitmaps.MultipassBitmap(int(rd[c4d.RDATA_XRES]), int(rd[c4d.RDATA_YRES]), c4d.COLORMODE_RGB)
                bmp.AddChannel(True, True)
                result = c4d.documents.RenderDocument(doc, bc, bmp, c4d.RENDERFLAGS_EXTERNAL | c4d.RENDERFLAGS_CREATE_PICTUREVIEWER  | c4d.RENDERFLAGS_OPEN_PICTUREVIEWER)
                if result != c4d.RENDERRESULT_OK:
# doc = c4d.documents.GetActiveDocument()
# rd = doc.GetActiveRenderData()
# bc = rd.GetDataInstance()
# bc.SetInt32(c4d.RDATA_FRAMESEQUENCE, c4d.RDATA_FRAMESEQUENCE_CURRENTFRAME)
# bc.SetTime(c4d.RDATA_FRAMEFROM, c4d.BaseTime(1001, doc.GetFps()))
# bc.SetTime(c4d.RDATA_FRAMETO, c4d.BaseTime(1001, doc.GetFps()))
# bc.SetInt32(c4d.RDATA_FRAMERATE, doc.GetFps())
# rd.SetData(bc)
# bmp = c4d.bitmaps.MultipassBitmap(int(rd[c4d.RDATA_XRES]), int(rd[c4d.RDATA_YRES]), c4d.COLORMODE_RGB)
# bmp.AddChannel(True, True)
# result = c4d.documents.RenderDocument(doc, bc, bmp, c4d.RENDERFLAGS_EXTERNAL | c4d.RENDERFLAGS_CREATE_PICTUREVIEWER  | c4d.RENDERFLAGS_OPEN_PICTUREVIEWER)
# print(result)
                    return "Execute Canceled: render command returned error: %s" % result  # make sure Maxon app is started

            if len(os.listdir(os.path.dirname(outputName))) > 0:
                return "Result=Success"
            else:
                return "unknown error (files do not exist)"
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            erStr = "%s ERROR - sm_default_imageRender %s:\n%s" % (
                time.strftime("%d/%m/%y %X"),
                origin.core.version,
                traceback.format_exc(),
            )
            self.core.writeErrorLog(erStr)
            return "Execute Canceled: unknown error (view console for more information)"

    @err_catcher(name=__name__)
    def sm_render_undoRenderSettings(self, origin, rSettings):
        pass

    @err_catcher(name=__name__)
    def sm_render_getDeadlineParams(self, origin, dlParams, homeDir):
        dlParams["jobInfoFile"] = os.path.join(
            homeDir, "temp", "cinema4d_submit_info.job"
        )
        dlParams["pluginInfoFile"] = os.path.join(
            homeDir, "temp", "cinema4d_plugin_info.job"
        )

        dlParams["jobInfos"]["Plugin"] = "Cinema4D"
        dlParams["jobInfos"]["Comment"] = "Prism-Submission-Cinema4D_ImageRender"
        dlParams["pluginInfos"]["Version"] = str(self.getAppVersion(origin))[:4]
        dlParams["pluginInfos"]["FilePath"] = dlParams["jobInfos"]["OutputFilename0"]

    @err_catcher(name=__name__)
    def getCurrentRenderer(self, origin):
        RENDERER_NAMES = {
            c4d.RDATA_RENDERENGINE_STANDARD: "Standard Renderer",
            c4d.RDATA_RENDERENGINE_PHYSICAL: "Physical Renderer",
            c4d.RDATA_RENDERENGINE_REDSHIFT: "Redshift Renderer",
            c4d.RDATA_RENDERENGINE_PREVIEWHARDWARE: "Viewport Renderer",
        }

        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetActiveRenderData()
        rendererId = rd.GetDataInstance().GetInt32(c4d.RDATA_RENDERENGINE)
        rendererName = RENDERER_NAMES.get(rendererId, "Unknown Renderer")
        return rendererName

    def getTakesFromScene(self):
        takes = []
        doc = c4d.documents.GetActiveDocument()
        takeData = doc.GetTakeData()
        if takeData is None:
            return []

        mainTake = takeData.GetMainTake()
        takes.append(mainTake)
        take = mainTake.GetDown()

        while take is not None:
            takes.append((take))
            take = take.GetNext()

        return takes

    @err_catcher(name=__name__)
    def getCurrentSceneFiles(self, origin):
        curFileName = self.core.getCurrentFileName()
        scenefiles = [curFileName]
        return scenefiles

    @err_catcher(name=__name__)
    def sm_render_preExecute(self, origin):
        warnings = []
        return warnings

    @err_catcher(name=__name__)
    def deleteNodes(self, origin, handles, num=0):
        for guid in handles:
            obj = self.getObject(guid)
            if obj:
                obj.Remove()

        c4d.EventAdd()

    @err_catcher(name=__name__)
    def sm_import_importToApp(self, origin, doImport, update, impFileName):
        doc = c4d.documents.GetActiveDocument()
        result = False
        origin.preDelete(
            baseText="Do you want to delete the currently connected objects?\n\n"
        )

        existingNodes = []
        obj = doc.GetFirstObject()
        while obj:
            existingNodes.append(obj)
            obj = obj.GetNext()

        if impFileName.lower().endswith(".ass"):
            try:
                procedural = c4d.BaseObject(1032509)
                if procedural is None:
                    raise Exception("Failed to create Arnold procedural object")

                bc = procedural.GetDataInstance()
                bc.SetFilename(200, impFileName)
                bc.SetFilename(1001, impFileName)
                assetName = os.path.splitext(os.path.basename(impFileName))[0]
                procedural.SetName(assetName)
                doc.InsertObject(procedural)
                doc.AddUndo(c4d.UNDOTYPE_NEW, procedural)
                procedural.Message(c4d.MSG_UPDATE)
                procedural.SetDirty(c4d.DIRTYFLAGS_ALL)
                c4d.EventAdd()
                result = True
            except Exception as e:
                self.core.popup("Failed to import .ass file: %s\nError: %s" % (impFileName, str(e)))
                return

        else:
            doc = c4d.documents.GetActiveDocument()
            merge_flags = c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS
            result = c4d.documents.MergeDocument(doc, impFileName, merge_flags)
            if not result:
                self.core.popup("Failed to import file.")
                return

        c4d.EventAdd()

        importedNodes = []
        obj = doc.GetFirstObject()
        while obj:
            if obj not in existingNodes:
                importedNodes.append(obj)

            obj = obj.GetNext()

        if origin.chb_trackObjects.isChecked():
            origin.nodes = [obj.GetGUID() for obj in importedNodes]

        doc.SetActiveObject(None, c4d.SELECTION_NEW)
        for obj in importedNodes:
            if self.isNodeValid(origin, obj):
                doc.SetActiveObject(obj, c4d.SELECTION_ADD)

        result = len(importedNodes) > 0

        return {"result": result, "doImport": doImport}

    @err_catcher(name=__name__)
    def sm_import_updateObjects(self, origin):
        pass

    @err_catcher(name=__name__)
    def sm_import_removeNameSpaces(self, origin):
        for guid in origin.nodes:
            if not self.getObject(guid):
                continue

            newName = self.getNodeName(origin, guid).rsplit(":", 1)[-1]
            if newName != self.getNodeName(origin, guid):
                self.getObject(guid).SetName(newName)

        origin.updateUi()

    @err_catcher(name=__name__)
    def sm_playblast_startup(self, origin):
        frange = self.getFrameRange(origin)
        origin.sp_rangeStart.setValue(frange[0])
        origin.sp_rangeEnd.setValue(frange[1])

    @err_catcher(name=__name__)
    def getPlayblastRenderData(self):
        doc = c4d.documents.GetActiveDocument()
        rd = doc.GetFirstRenderData()
        while rd:
            if rd.GetName() == "Playblast":
                return rd

            rd = rd.GetNext()

    @err_catcher(name=__name__)
    def createPlayblastRenderData(self):
        doc = c4d.documents.GetActiveDocument()
        rd = c4d.documents.RenderData()
        rd.SetName("Playblast")
        doc.InsertRenderData(rd)
        return rd

    @err_catcher(name=__name__)
    def sm_playblast_createPlayblast(self, origin, jobFrames, outputName):
        rd = self.getPlayblastRenderData()
        if not rd:
            rd = self.createPlayblastRenderData()

        doc = c4d.documents.GetActiveDocument()
        doc.SetActiveRenderData(rd)
        if origin.chb_resOverride.isChecked():
            self.setResolution(
                origin.sp_resWidth.value(),
                origin.sp_resHeight.value(),
            )

        if origin.curCam and origin.curCam != "Don't override":
            bd = doc.GetActiveBaseDraw()
            bd.SetSceneCamera(self.getObject(origin.curCam))

        singleFrame = origin.cb_rangeType.currentText() == "Single Frame"
        try:
            bc = rd.GetDataInstance()
            if singleFrame:
                bc.SetInt32(c4d.RDATA_FRAMESEQUENCE, c4d.RDATA_FRAMESEQUENCE_CURRENTFRAME)
            else:
                bc.SetInt32(c4d.RDATA_FRAMESEQUENCE, c4d.RDATA_FRAMESEQUENCE_MANUAL)

            bc.SetTime(c4d.RDATA_FRAMEFROM, c4d.BaseTime(jobFrames[0], doc.GetFps()))
            bc.SetTime(c4d.RDATA_FRAMETO, c4d.BaseTime(jobFrames[1], doc.GetFps()))
            bc.SetInt32(c4d.RDATA_FRAMERATE, doc.GetFps())
            bc.SetFilename(c4d.RDATA_PATH, outputName)
            bc.SetBool(c4d.RDATA_GLOBALSAVE, True)
            bc.SetBool(c4d.RDATA_SAVEIMAGE, True)
            base, ext = os.path.splitext(outputName.lower())
            if ext == ".exr":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_EXR)
            elif ext == ".png":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_PNG)
            elif ext == ".jpg":
                bc.SetInt32(c4d.RDATA_FORMAT, c4d.FILTER_JPG)

            bc.SetInt32(c4d.RDATA_RENDERENGINE, c4d.RDATA_RENDERENGINE_PREVIEWHARDWARE)
            rd.SetData(bc)

            bmp = c4d.bitmaps.MultipassBitmap(int(rd[c4d.RDATA_XRES]), int(rd[c4d.RDATA_YRES]), c4d.COLORMODE_RGB)
            bmp.AddChannel(True, True)
            flags = (c4d.RENDERFLAGS_EXTERNAL | c4d.RENDERFLAGS_PREVIEWRENDER | c4d.RENDERFLAGS_CREATE_PICTUREVIEWER | c4d.RENDERFLAGS_OPEN_PICTUREVIEWER)
            result = c4d.documents.RenderDocument(doc, bc, bmp, flags)
            if result != c4d.RENDERRESULT_OK:
                return "error: %s" % result

            if len(os.listdir(os.path.dirname(outputName))) > 0:
                return "Result=Success"
            else:
                return "unknown error (files do not exist)"
        except Exception:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            erStr = "%s ERROR - sm_default_playblast %s:\n%s" % (
                time.strftime("%d/%m/%y %X"),
                origin.core.version,
                traceback.format_exc(),
            )
            self.core.writeErrorLog(erStr)
            return "Execute Canceled: unknown error (view console for more information)"

    @err_catcher(name=__name__)
    def sm_playblast_preExecute(self, origin):
        warnings = []
        return warnings

    @err_catcher(name=__name__)
    def prePlayblast(self, **kwargs):
        base, ext = os.path.splitext(kwargs["outputpath"])
        outputName = base.rstrip("#") + ext        
        if outputName and outputName != kwargs["outputpath"]:
            return {"outputName": outputName}

    @err_catcher(name=__name__)
    def sm_playblast_execute(self, origin):
        pass

    @err_catcher(name=__name__)
    def captureViewportThumbnail(self):
        path = tempfile.NamedTemporaryFile(suffix=".png").name
        doc = c4d.documents.GetActiveDocument()
        bd = doc.GetActiveBaseDraw()
        frame = bd.GetFrame()
        width = frame["cr"] - frame["cl"]
        height = frame["cb"] - frame["ct"]
        bmp = c4d.bitmaps.BaseBitmap()
        bmp.Init(width, height)

        prevRd = doc.GetActiveRenderData()
        rd = c4d.documents.RenderData()
        rd.SetName("__prism_preview__")
        doc.InsertRenderData(rd)
        doc.SetActiveRenderData(rd)

        bc = rd.GetDataInstance()
        bc.SetInt32(c4d.RDATA_RENDERENGINE, c4d.RDATA_RENDERENGINE_PREVIEWHARDWARE)
        rd.SetData(bc)
        c4d.documents.RenderDocument(doc, rd.GetDataInstance(), bmp, c4d.RENDERFLAGS_EXTERNAL)
        doc.SetActiveRenderData(prevRd)
        rd.Remove()
        bmp.Save(path, c4d.FILTER_PNG)
        pm = self.core.media.getPixmapFromPath(path)
        try:
            os.remove(path)
        except:
            pass

        return pm

    @err_catcher(name=__name__)
    def sm_saveStates(self, origin, buf):
        doc = c4d.documents.GetActiveDocument()
        if not doc:
            return

        cid, value, bc = self.findUserDataByName(doc, "PrismStates")
        if not bc:
            bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STRING)
            bc[c4d.DESC_NAME] = "PrismStates"
            bc[c4d.DESC_DEFAULT] = ""
            cid = doc.AddUserData(bc)

        if cid:
            doc[cid] = buf

        c4d.EventAdd()

    @err_catcher(name=__name__)
    def sm_saveImports(self, origin, importPaths):
        doc = c4d.documents.GetActiveDocument()
        if not doc:
            return

        cid, value, bc = self.findUserDataByName(doc, "PrismImports")
        if not bc:
            bc = c4d.GetCustomDataTypeDefault(c4d.DTYPE_STRING)
            bc[c4d.DESC_NAME] = "PrismImports"
            bc[c4d.DESC_DEFAULT] = ""
            cid = doc.AddUserData(bc)

        if cid:
            doc[cid] = importPaths

        c4d.EventAdd()

    @err_catcher(name=__name__)
    def sm_preSaveToScene(self, origin):
        if (not origin.scenename) or origin.scenename.startswith("\\Untitled ") or origin.scenename == self.core.getCurrentFileName():
            return

        origin.saveEnabled = False

        msg = QMessageBox(
            QMessageBox.NoIcon,
            "State Manager",
            "The scenefile changed.",
        )
        msg.addButton("Save current states to scene", QMessageBox.YesRole)
        msg.addButton("Reload states from scene", QMessageBox.NoRole)
        msg.addButton("Close", QMessageBox.NoRole)

        msg.setParent(self.core.messageParent, Qt.Window)

        action = msg.exec_()

        origin.scenename = self.core.getCurrentFileName()

        if action == 1:
            self.core.closeSM(restart=True)
            return False
        elif action == 2:
            self.core.closeSM()
            return False

        origin.saveEnabled = True

    @err_catcher(name=__name__)
    def findUserDataByName(self, obj, name):
        for id, bc in obj.GetUserDataContainer():
            if bc[c4d.DESC_NAME] == name:
                return id, obj[id], bc

        return None, None, None

    @err_catcher(name=__name__)
    def sm_readStates(self, origin):
        doc = c4d.documents.GetActiveDocument()
        if not doc:
            return

        cid, value, bc = self.findUserDataByName(doc, "PrismStates")
        return value

    @err_catcher(name=__name__)
    def sm_deleteStates(self, origin):
        doc = c4d.documents.GetActiveDocument()
        cid, value, bc = self.findUserDataByName(doc, "PrismStates")
        if cid:
            doc.RemoveUserData(cid)

        c4d.EventAdd()

    @err_catcher(name=__name__)
    def sm_getExternalFiles(self, origin):
        extFiles = []
        return [extFiles, []]
