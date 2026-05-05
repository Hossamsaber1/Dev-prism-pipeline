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
import logging
import shutil
import time

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher

from PrismUtils import PrismWidgets


logger = logging.getLogger(__name__)


class ProjectEntities(object):
    def __init__(self, core):
        self.core = core
        self.entityFolders = {"asset": ["Textures"], "shot": []}
        self.entityActions = {}
        self.depIcons = {}
        self.entityDlg = EntityDlg
        self.refreshOmittedEntities()
        self.addEntityAction(
            key="importConnectedAssets",
            types=["shot"],
            function=lambda entities=None, parent=None: self.core.products.importConnectedAssetsForEntities(entities),
            label="Import Connected Assets..."
        )

    @err_catcher(name=__name__)
    def refreshOmittedEntities(self):
        self.omittedEntities = {"asset": [], "shot": []}
        omits = self.core.getConfig(config="omit") or {}

        oShots = omits.get("shot") or []
        oAssets = omits.get("asset") or []

        self.omittedEntities["shot"] = oShots
        self.omittedEntities["asset"] = oAssets
        self.omittedEntities["assetFolder"] = oAssets

    @err_catcher(name=__name__)
    def isEntityOmitted(self, entity):
        if entity["type"] in ["asset", "assetFolder"]:
            return self.isAssetOmitted(entity)
        elif entity["type"] == "shot":
            return self.isShotOmitted(entity)

    @err_catcher(name=__name__)
    def isAssetOmitted(self, entity):
        omitted = entity["asset_path"].replace("\\", "/") in [a.replace("\\", "/") for a in self.omittedEntities["asset"]]
        return omitted

    @err_catcher(name=__name__)
    def isEpisodeOmitted(self, entity):
        return False

    @err_catcher(name=__name__)
    def isSequenceOmitted(self, entity):
        return False

    @err_catcher(name=__name__)
    def isShotOmitted(self, entity):
        if entity["sequence"] in self.omittedEntities["shot"]:
            if entity["shot"] in self.omittedEntities["shot"][entity["sequence"]]:
                return True

        return False

    @err_catcher(name=__name__)
    def getShotSubFolders(self):
        subfolders = []

        template = self.core.projects.getTemplatePath("departments")
        template = template.replace("\\", "/")
        sceneFolder = template.split("/")[1]
        if sceneFolder:
            subfolders.append(sceneFolder)

        template = self.core.projects.getTemplatePath("products")
        template = template.replace("\\", "/")
        productFolder = template.split("/")[1]
        if productFolder:
            subfolders.append(productFolder)

        template = self.core.projects.getTemplatePath("3drenders")
        template = template.replace("\\", "/")
        renderFolder = template.split("/")[1]
        if renderFolder:
            subfolders.append(renderFolder)

        template = self.core.projects.getTemplatePath("playblasts")
        template = template.replace("\\", "/")
        playblastFolder = template.split("/")[1]
        if playblastFolder:
            subfolders.append(playblastFolder)

        return subfolders

    @err_catcher(name=__name__)
    def getTypeFromShotPath(self, path, content=None):
        if not os.path.exists(path):
            return

        if content is None:
            content = os.listdir(path)

        subfolders = self.getShotSubFolders()

        if self.core.getConfig(
            "globals", "useStrictShotDetection", dft=False, config="project"
        ):
            isShot = True
            for folder in subfolders:
                if folder not in content:
                    isShot = False

        else:
            isShot = False
            for folder in subfolders:
                if folder in content:
                    isShot = True

        if isShot:
            return "shot"
        else:
            return "folder"

    @err_catcher(name=__name__)
    def getShotName(self, entity):
        if "sequence" not in entity:
            return

        if "shot" in entity:
            shotname = (entity["sequence"] or "") + "-" + (entity["shot"] or "")
        else:
            shotname = entity["sequence"] or ""

        if "episode" in entity:
            shotname = "%s-%s" % (entity["episode"], shotname)

        return shotname

    @err_catcher(name=__name__)
    def setShotRange(self, entity, start, end):
        seqRanges = self.core.getConfig(
            "shotRanges", entity["sequence"], config="shotinfo", allowCache=False
        )
        if not seqRanges:
            seqRanges = {}

        seqRanges[entity["shot"]] = [start, end]
        self.core.setConfig(
            "shotRanges", entity["sequence"], seqRanges, config="shotinfo"
        )

    @err_catcher(name=__name__)
    def getShotRange(self, entity, handles=False):
        ranges = self.core.getConfig("shotRanges", config="shotinfo") or {}
        if entity.get("sequence") in ranges:
            if entity.get("shot") in ranges[entity["sequence"]]:
                shotRange = ranges[entity["sequence"]][entity["shot"]].copy()
                if handles:
                    metaData = self.getMetaData(entity)
                    if "handles_in" in metaData:
                        try:
                            shotRange[0] = shotRange[0] - int(metaData["handles_in"]["value"])
                        except:
                            pass

                    if "handles_out" in metaData:
                        try:
                            shotRange[1] = shotRange[1] + int(metaData["handles_out"]["value"])
                        except:
                            pass

                    if "handles" in metaData:
                        try:
                            handleNum = int(metaData["handles"]["value"])
                        except:
                            pass
                        else:
                            if "handles_in" not in metaData:
                                shotRange[0] = shotRange[0] - handleNum

                            if "handles_out" not in metaData:
                                shotRange[1] = shotRange[1] + handleNum

                return shotRange

    @err_catcher(name=__name__)
    def getEpisodes(self, searchFilter="", locations=None):
        epDirs = self.getLocations(locations)
        epDicts = []
        for epDir in epDirs:
            context = {"project_path": epDir["path"]}
            template = self.core.projects.getResolvedProjectStructurePath(
                "episodes", context=context
            )
            epData = self.core.projects.getMatchingPaths(template)
            for data in epData:
                if "." in os.path.basename(data["path"]) and os.path.isfile(data["path"]):
                    continue

                if data["episode"].startswith("_"):
                    continue

                if self.isEpisodeOmitted(data):
                    continue

                if (
                    searchFilter.lower() not in data["episode"].lower()
                ):
                    metaData = self.getMetaData(data)
                    if not metaData or searchFilter.lower() not in metaData.get("Description", {}).get("value", "").lower():
                        continue

                data["location"] = epDir["location"]
                data["type"] = "shot"
                epDicts.append(data)

        episodes = []
        for epDict in sorted(epDicts, key=lambda x: x["path"]):
            for episode in episodes:
                if (
                    epDict["episode"] == episode["episode"]
                ):
                    data = {"location": epDict["location"], "path": epDict["path"]}
                    episode["paths"].append(data)
                    break
            else:
                epDict["paths"] = [
                    {"location": epDict["location"], "path": epDict["path"]}
                ]
                episodes.append(epDict)

        episodes = sorted(episodes, key=lambda x: self.core.naturalKeys(x["episode"]))
        return episodes

    @err_catcher(name=__name__)
    def getSequences(self, searchFilter="", locations=None, episode=None):
        seqDirs = self.getLocations(locations)
        seqDicts = []
        for seqDir in seqDirs:
            context = {"project_path": seqDir["path"]}
            if episode:
                context["episode"] = episode

            template = self.core.projects.getResolvedProjectStructurePath(
                "sequences", context=context
            )
            seqData = self.core.projects.getMatchingPaths(template)
            for data in seqData:
                if "." in os.path.basename(data["path"]) and os.path.isfile(data["path"]):
                    continue

                if data["sequence"].startswith("_"):
                    continue

                if self.isSequenceOmitted(data):
                    continue

                if searchFilter:
                    if (
                        searchFilter.lower() not in data["sequence"].lower()
                    ):
                        metaData = self.getMetaData(data)
                        if not metaData or searchFilter.lower() not in metaData.get("Description", {}).get("value", "").lower():
                            if not self.getShots(sequence=data["sequence"], searchFilter=searchFilter, locations=locations, episode=episode):
                                continue

                data["location"] = seqDir["location"]
                data["type"] = "shot"
                if episode:
                    data["episode"] = episode

                seqDicts.append(data)

        sequences = []
        for seqDict in sorted(seqDicts, key=lambda x: x["path"]):
            for sequence in sequences:
                if (
                    seqDict["sequence"] == sequence["sequence"]
                ):
                    data = {"location": seqDict["location"], "path": seqDict["path"]}
                    sequence["paths"].append(data)
                    break
            else:
                seqDict["paths"] = [
                    {"location": seqDict["location"], "path": seqDict["path"]}
                ]
                sequences.append(seqDict)

        sequences = sorted(sequences, key=lambda x: self.core.naturalKeys(x["sequence"]))
        return sequences

    @err_catcher(name=__name__)
    def getLocations(self, locations=None):
        locationDicts = []
        location_paths = self.core.paths.getExportProductBasePaths()
        location_paths.update(self.core.paths.getRenderProductBasePaths())
        for location in location_paths:
            if locations is not None and location not in locations:
                continue
            locDir = {"location": location, "path": location_paths[location]}
            locationDicts.append(locDir)

        return locationDicts

    @err_catcher(name=__name__)
    def filterValidShots(self, shotData, searchFilter=""):
        validShots = []
        for data in shotData:
            if "." in os.path.basename(data["path"]) and os.path.isfile(data["path"]):
                continue

            if data.get("episode", "").startswith("_"):
                continue

            if data["sequence"].startswith("_"):
                continue

            if data["shot"].startswith("_"):
                continue

            if self.isShotOmitted(data):
                continue

            if (
                ("episode" not in data or searchFilter.lower() not in data["episode"].lower())
                and searchFilter.lower() not in data["sequence"].lower()
                and searchFilter.lower() not in data["shot"].lower()
            ):
                metaData = self.getMetaData(data)
                if not metaData or searchFilter.lower() not in metaData.get("Description", {}).get("value", "").lower():
                    continue

            validShots.append(data)

        return validShots

    @err_catcher(name=__name__)
    def combineShotsFromLocations(self, shotData):
        shots = []
        for shotDict in sorted(shotData, key=lambda x: x["path"]):
            for shot in shots:
                if (
                    shotDict["sequence"] == shot["sequence"]
                    and shotDict["shot"] == shot["shot"]
                    and ("episode" not in shotDict or shotDict.get("episode") == shot.get("episode"))
                ):
                    data = {"location": shotDict["location"], "path": shotDict["path"]}
                    shot["paths"].append(data)
                    break
            else:
                shotDict["paths"] = [
                    {"location": shotDict["location"], "path": shotDict["path"]}
                ]
                shots.append(shotDict)

        return shots

    @err_catcher(name=__name__)
    def getShot(self, sequence, shot, episode=None, projectPath=None):
        if not sequence or not shot:
            return

        shot = {"type": "shot", "sequence": sequence, "shot": shot}
        if episode:
            shot["episode"] = episode

        shotpath = self.core.projects.getResolvedProjectStructurePath(
            "shots", context=shot
        )
        existed = os.path.exists(shotpath)
        if existed:
            return shot
        else:
            return

    @err_catcher(name=__name__)
    def getShots(self, searchFilter="", locations=None, episode=None, sequence=None):
        seqDirs = self.getLocations(locations)
        shotDicts = []
        for seqDir in seqDirs:
            context = {"project_path": seqDir["path"]}
            if episode:
                context["episode"] = episode

            if sequence:
                context["sequence"] = sequence

            template = self.core.projects.getResolvedProjectStructurePath(
                "shots", context=context
            )
            shotData = self.core.projects.getMatchingPaths(template)
            for data in shotData:
                if episode:
                    data["episode"] = episode

                if sequence:
                    data["sequence"] = sequence

                data["location"] = seqDir["location"]
                data["type"] = "shot"

            shotDicts += self.filterValidShots(shotData, searchFilter=searchFilter)

        shots = self.combineShotsFromLocations(shotDicts)
        shots = sorted(shots, key=lambda x: self.core.naturalKeys(x["shot"]))
        return shots

    @err_catcher(name=__name__)
    def getShotsFromSequence(self, sequence):
        shots = self.core.entities.getShots(sequence=sequence)
        return shots

    @err_catcher(name=__name__)
    def getSteps(self, entity):
        departments = []
        # Compatibility patch: keep legacy departments discoverable, but always
        # expose the simplified default department for the main artist workflow.
        defaultDepartment = self.core.paths.normalizeDepartment(
            None, context=entity, reason="scene browser department list"
        )
        departments.append(defaultDepartment)

        stepDirs = []
        templates = self.core.projects.getResolvedProjectStructurePaths(
            "departments", context=entity
        )

        if self.core.useLocalFiles:
            for template in templates:
                path = self.core.convertPath(template, target="global")
                lpath = self.core.convertPath(template, target="local")
                if path not in stepDirs:
                    stepDirs.append(path)

                if lpath not in stepDirs:
                    stepDirs.append(lpath)
        else:
            stepDirs = templates

        dirContent = []
        for sDir in stepDirs:
            dirContent += self.core.projects.getMatchingPaths(sDir)

        for content in sorted(dirContent, key=lambda x: x.get("department")):
            dep = content.get("department", "")
            if not dep or dep.startswith("_"):
                continue

            if os.path.isdir(content["path"]) and dep not in departments:
                departments.append(dep)

        departments = self.orderDepartments(entity, departments)
        return departments

    @err_catcher(name=__name__)
    def getCategories(self, entity, step=None):
        cats = []
        step = self.core.paths.normalizeDepartment(
            step, context=entity, reason="scene browser task list"
        )
        defaultTask = self.core.paths.normalizeTask(
            None, context=entity, reason="scene browser task list"
        )
        path = self.core.getEntityPath(entity=entity, step=step)
        catDirs = [path]

        if self.core.useLocalFiles:
            path = self.core.convertPath(path, target="global")
            lpath = self.core.convertPath(path, target="local")
            catDirs = [path, lpath]

        dirContent = []

        for cDir in catDirs:
            if os.path.exists(cDir):
                dirContent += [os.path.join(cDir, x) for x in os.listdir(cDir)]

        for i in sorted(dirContent, key=lambda x: os.path.basename(x)):
            catName = os.path.basename(i)
            if catName.startswith("_"):
                continue

            if os.path.isdir(i) and catName not in cats:
                cats.append(catName)

        if defaultTask not in cats:
            cats.insert(0, defaultTask)

        cats = self.orderTasks(entity, step, cats)
        return cats

    @err_catcher(name=__name__)
    def getScenefiles(self, entity=None, step=None, category=None, extensions=None, path=None):
        scenefiles = []

        if not path:
            step = self.core.paths.normalizeDepartment(
                step, context=entity, reason="scenefile lookup"
            )
            category = self.core.paths.normalizeTask(
                category, context=entity, reason="scenefile lookup"
            )
            if entity["type"] == "asset":
                if (
                    self.core.compareVersions(self.core.projectVersion, "v1.2.1.6")
                    == "lower"
                ):
                    path = self.core.getEntityPath(entity=entity, step=step)
                else:
                    path = self.core.getEntityPath(
                        entity=entity, step=step, category=category
                    )
            elif entity["type"] == "shot":
                path = self.core.getEntityPath(
                    entity=entity,
                    step=step,
                    category=category,
                )

        sceneDirs = [path]
        if (
            entity
            and self.core.paths.isSimplifiedArtistWorkflowEnabled()
            and entity.get("type") in ["asset", "shot"]
            and self.core.paths.isDefaultDepartmentTask(step, category)
        ):
            simpleDir = self.core.paths.getSimplifiedScenefileFolder(entity)
            if simpleDir and simpleDir not in sceneDirs:
                sceneDirs.insert(0, simpleDir)
                logger.debug("Scanning simplified scenefile folder: %s", simpleDir)

            # Compatibility patch: also scan the legacy scenefile root so older
            # department/task based files remain visible in the flattened browser.
            legacyContext = entity.copy()
            legacyContext["department"] = step
            legacyDepPath = self.core.projects.getResolvedProjectStructurePath(
                "departments", context=legacyContext
            )
            legacyRoot = os.path.dirname(legacyDepPath)
            if legacyRoot and legacyRoot not in sceneDirs:
                sceneDirs.append(legacyRoot)
                logger.debug("Scanning legacy scenefile root: %s", legacyRoot)

        if self.core.useLocalFiles:
            locationDirs = []
            for sDir in sceneDirs:
                gpath = self.core.convertPath(sDir, target="global")
                lpath = self.core.convertPath(sDir, target="local")
                if gpath not in locationDirs:
                    locationDirs.append(gpath)
                if lpath not in locationDirs:
                    locationDirs.append(lpath)

            sceneDirs = locationDirs

        sfiles = {}
        for sDir in sceneDirs:
            if not sDir or not os.path.exists(sDir):
                continue

            for root, dirs, files in os.walk(sDir):
                for f in files:
                    if f in sfiles:
                        continue

                    scenePath = os.path.join(root, f).replace("\\", "/")
                    if self.isValidScenefilename(scenePath, extensions=extensions):
                        sfiles[f] = scenePath

        scenefiles = list(sfiles.values())
        return scenefiles

    @err_catcher(name=__name__)
    def getScenefile(self, entity, department, task, version):
        scenefiles = self.getScenefiles(entity, department, task)
        highversion = [None, None]
        for scenefile in scenefiles:
            ext = os.path.splitext(scenefile)[1]
            if not self.isValidScenefilename(scenefile):
                continue

            fname = self.core.getScenefileData(scenefile)
            if fname.get("type") != entity.get("type"):
                continue

            try:
                sversion = int(fname["version"][-self.core.versionPadding:])
            except:
                continue

            if (
                ext.lower() in self.core.media.supportedFormats
                and self.core.versionFormat.startswith("v")
                and fname["version"][-(self.core.versionPadding+1)] != "v"
            ):
                continue

            if version == "latest":
                if highversion[0] is None or sversion > highversion[0]:
                    highversion = [sversion, scenefile]
            else:
                if isinstance(version, int):
                    if version == sversion:
                        return scenefile
                else:
                    if version == fname["version"]:
                        return scenefile

        if version == "latest":
            return highversion[1]

    @err_catcher(name=__name__)
    def isValidScenefilename(self, filename, extensions=None):
        ext = os.path.splitext(filename)[1]
        if ext in [
            ".jpg",
            ".json",
            ".yml",
            ".ini",
            ".lock",
            ".old",
            ".db"
        ]:
            return False

        if ext in self.getBlacklistedExtensions():
            return False

        sData = self.core.getScenefileData(filename)

        try:
            int(sData["extension"][-5:])  # ignore maya temp files
            logger.debug("maya temp file")
            return False
        except Exception:
            pass

        if "extension" not in sData:
            logger.debug("no extension")
            return False

        if sData["extension"].endswith("~"):  # ignore nuke autosave files
            logger.debug("nuke autosave file")
            return False

        if filename.endswith(".painter_lock"):  # ignore substance painter lock files
            logger.debug("substance lockfile")
            return False

        if sData["extension"] == ".spp" and "autosave_" in filename:  # ignore substance painter autosave files
            logger.debug("substance lockfile")
            return False

        if filename.endswith("autosave"):
            logger.debug("autosave file")
            return False

        if sData["extension"].startswith(".blend") and sData["extension"] != ".blend":  # ignore Blender autosave files
            logger.debug("Blender autosave file")
            return False

        if extensions:
            unknownScene = sData["extension"] not in self.core.getPluginSceneFormats()
            if unknownScene:
                if "*" not in extensions:
                    logger.debug("invalid extension: %s" % sData["extension"])
                    return False
            else:
                if sData["extension"] not in extensions:
                    logger.debug("invalid extension: %s" % sData["extension"])
                    return False

        return True

    @err_catcher(name=__name__)
    def orderDepartments(self, entity, departments):
        if entity.get("type") == "asset":
            pdeps = self.core.projects.getAssetDepartments()
        elif entity.get("type") == "shot":
            pdeps = self.core.projects.getShotDepartments()
        else:
            return departments

        abbrs = [d["abbreviation"] for d in pdeps]
        deps = sorted(departments, key=lambda x: self.indexOf(x, abbrs))
        return deps

    @err_catcher(name=__name__)
    def orderTasks(self, entity, department, tasks):
        if entity.get("type") == "asset":
            pdeps = self.core.projects.getAssetDepartments()
        elif entity.get("type") == "shot":
            pdeps = self.core.projects.getShotDepartments()
        else:
            return tasks

        for dep in pdeps:
            if dep["abbreviation"] == department:
                tasks = sorted(tasks, key=lambda x: self.indexOf(x, dep["defaultTasks"]) if x in dep["defaultTasks"] else 999)
                break

        return tasks

    @err_catcher(name=__name__)
    def indexOf(self, val, listData):
        try:
            idx = listData.index(val)
        except ValueError:
            idx = -1

        return idx

    @err_catcher(name=__name__)
    def getDependencies(self, path):
        info = self.core.getVersioninfoPath(path)
        deps = []
        source = self.core.getConfig("source scene", configPath=info)
        if source:
            deps.append(source)

        depPaths = (
            self.core.getConfig("dependencies", configPath=info) or []
        )
        deps += depPaths
        extFiles = (
            self.core.getConfig("externalFiles", configPath=info) or []
        )
        deps += extFiles

        return deps

    @err_catcher(name=__name__)
    def getCurrentDependencies(self):
        deps = (
            getattr(self.core.appPlugin, "getImportPaths", lambda x: None)(self.core)
            or []
        )

        if type(deps) == str:
            deps = eval(deps.replace("\\", "/").replace("//", "/"))
        deps = [str(x[0]) for x in deps]

        extFiles = getattr(
            self.core.appPlugin, "sm_getExternalFiles", lambda x: [[], []]
        )(self.core)[0]
        extFiles = list(set(extFiles))

        return {"dependencies": deps, "externalFiles": extFiles}

    @err_catcher(name=__name__)
    def createEntity(self, entity, dialog=None, frameRange=None, silent=False, description=None, preview=None, metaData=None):
        if entity["type"] == "asset":
            result = self.createAsset(entity, description=description, preview=preview, metaData=metaData, dialog=dialog)
        elif entity["type"] == "assetFolder":
            result = self.createAssetFolder(entity, dialog=dialog)
        elif entity["type"] == "shot":
            result = self.createShot(entity, frameRange=frameRange, preview=preview, metaData=metaData)
        else:
            return {}

        if not result:
            return {}

        if result.get("existed"):
            if entity["type"] in ["asset", "assetFolder"]:
                name = entity["asset_path"]
            elif entity["type"] == "shot":
                name = self.getShotName(entity)

            if self.isEntityOmitted(entity) and self.core.uiAvailable:
                msgText = (
                    "The %s %s already exists, but is marked as omitted.\n\nDo you want to restore it?"
                    % (entity["type"], name)
                )
                resultq = self.core.popupQuestion(msgText)

                if resultq == "Yes":
                    self.omitEntity(entity, omit=False)
            else:
                if not silent:
                    self.core.popup("The %s already exists:\n\n%s" % (entity["type"], name))

        if result.get("error"):
            self.core.popup(result["error"])

        return result

    @err_catcher(name=__name__)
    def createAssetFolder(self, entity, dialog=None):
        fullAssetPath = os.path.join(self.core.assetPath, entity["asset_path"])

        existed = os.path.exists(fullAssetPath)
        if not os.path.exists(fullAssetPath):
            os.makedirs(fullAssetPath)

        if not existed:
            self.core.callback(
                name="onAssetFolderCreated",
                args=[self, entity, dialog],
            )

        result = {
            "entity": entity,
            "existed": existed,
        }
        logger.debug("assetFolder created: %s" % result)
        return result

    @err_catcher(name=__name__)
    def createAsset(self, entity, description=None, preview=None, metaData=None, dialog=None):
        fullAssetPath = os.path.join(self.core.assetPath, entity["asset_path"])

        assetName = self.getAssetNameFromPath(fullAssetPath)
        if not self.isValidAssetName(assetName):
            return {"error": "Invalid assetname."}

        existed = os.path.exists(fullAssetPath)
        if existed and self.getTypeFromAssetPath(fullAssetPath) == "folder":
            return {"error": "A folder with this name exists already."}

        for f in self.entityFolders["asset"]:
            aFolder = os.path.join(fullAssetPath, f)
            if not os.path.exists(aFolder):
                os.makedirs(aFolder)

        assetDep = self.core.projects.getResolvedProjectStructurePath(
            "departments", context=entity
        )
        assetProducts = self.core.projects.getResolvedProjectStructurePath(
            "products", context=entity
        )
        asset3dRenders = self.core.projects.getResolvedProjectStructurePath(
            "3drenders", context=entity
        )
        asset2dRenders = self.core.projects.getResolvedProjectStructurePath(
            "2drenders", context=entity
        )
        assetPlayblasts = self.core.projects.getResolvedProjectStructurePath(
            "playblasts", context=entity
        )
        assetFolders = [
            os.path.dirname(assetDep),
            os.path.dirname(assetProducts),
            os.path.dirname(asset3dRenders),
            os.path.dirname(asset2dRenders),
            os.path.dirname(assetPlayblasts),
        ]

        for assetFolder in assetFolders:
            if not os.path.exists(assetFolder):
                try:
                    os.makedirs(assetFolder)
                except Exception as e:
                    return {"error": "Failed to create folder:\n\n%s\n\nError: %s" % (assetFolder, str(e))}

        if description:
            self.core.entities.setAssetDescription(assetName, description)

        if preview:
            self.core.entities.setEntityPreview(entity, preview)

        if metaData:
            self.core.entities.setMetaData(entity, metaData)

        if not existed:
            self.core.callback(
                name="onAssetCreated",
                args=[self, entity, dialog],
            )

        result = {
            "entity": entity,
            "existed": existed,
        }
        logger.debug("asset created: %s" % result)
        return result

    @err_catcher(name=__name__)
    def createShot(self, entity, frameRange=None, preview=None, metaData=None):
        sBase = self.core.getEntityPath(entity=entity)
        existed = os.path.exists(sBase)

        for f in self.entityFolders["shot"]:
            sFolder = os.path.join(sBase, f)
            if not os.path.exists(sFolder):
                try:
                    os.makedirs(sFolder)
                except Exception as e:
                    if e.errno == 13:
                        self.core.popup(
                            "Missing permissions to create folder:\n\n%s" % sFolder
                        )
                        return {}
                    else:
                        raise

        shotDep = self.core.projects.getResolvedProjectStructurePath(
            "departments", context=entity
        )
        shotProducts = self.core.projects.getResolvedProjectStructurePath(
            "products", context=entity
        )
        shot3dRenders = self.core.projects.getResolvedProjectStructurePath(
            "3drenders", context=entity
        )
        shot2dRenders = self.core.projects.getResolvedProjectStructurePath(
            "2drenders", context=entity
        )
        shotPlayblasts = self.core.projects.getResolvedProjectStructurePath(
            "playblasts", context=entity
        )
        shotFolders = [
            os.path.dirname(shotDep),
            os.path.dirname(shotProducts),
            os.path.dirname(shot3dRenders),
            os.path.dirname(shot2dRenders),
            os.path.dirname(shotPlayblasts),
        ]

        for shotFolder in shotFolders:
            while "@" in os.path.basename(shotFolder):
                shotFolder = os.path.dirname(shotFolder)

            if not os.path.exists(shotFolder):
                os.makedirs(shotFolder)

        if frameRange:
            self.setShotRange(entity, frameRange[0], frameRange[1])

        if preview:
            self.core.entities.setEntityPreview(entity, preview)

        if metaData:
            self.core.entities.setMetaData(entity, metaData)

        if not existed:
            self.core.callback(name="onShotCreated", args=[self, entity])

        result = {
            "entity": entity,
            "entityPath": sBase,
            "existed": existed,
        }
        logger.debug("shot created: %s" % result)
        return result

    @err_catcher(name=__name__)
    def createDepartment(self, department, entity, stepPath="", createCat=True):
        if not stepPath:
            stepPath = self.core.getEntityPath(entity=entity, step=department)

        if not os.path.exists(stepPath):
            existed = False
            try:
                os.makedirs(stepPath)
            except:
                self.core.popup("The department %s could not be created.\n\n%s" % (department, stepPath))
                return False
        else:
            existed = True
            logger.debug("step already exists: %s" % stepPath)

        settings = {
            "createDefaultCategory": (
                entity["type"] == "shot"
                or self.core.compareVersions(self.core.projectVersion, "v1.2.1.6")
                != "lower"
            )
            and createCat
        }

        self.core.callback(
            name="onDepartmentCreated",
            args=[self, entity, department, stepPath, settings],
        )

        if not existed:
            logger.debug("department created %s" % stepPath)

        if settings["createDefaultCategory"]:
            paths = self.createDefaultCat(entity, department)
            return paths

        return stepPath

    @err_catcher(name=__name__)
    def getLongDepartmentName(self, entity, abbreviation):
        if entity == "asset":
            deps = self.core.projects.getAssetDepartments()
        elif entity in ["shot", "sequence"]:
            deps = self.core.projects.getShotDepartments()
        else:
            return

        fullNames = [dep["name"] for dep in deps if dep["abbreviation"] == abbreviation]
        if fullNames:
            return fullNames[0]

    @err_catcher(name=__name__)
    def getDepartmentAbbreviation(self, entity, department):
        if entity == "asset":
            deps = self.core.projects.getAssetDepartments()
        elif entity in ["shot", "sequence"]:
            deps = self.core.projects.getShotDepartments()

        abbrvs = [dep["abbreviation"] for dep in deps if dep["name"] == department]
        if abbrvs:
            return abbrvs[0]

    @err_catcher(name=__name__)
    def getDepartmentIcon(self, department):
        if department in self.depIcons:
            return self.depIcons[department]

        path = os.path.join(self.core.projects.getPipelineFolder(), "Icons", department + ".png")
        icon = QIcon(path)
        self.depIcons[department] = icon
        return icon

    @err_catcher(name=__name__)
    def getDefaultTasksForDepartment(self, entity, department):
        if entity == "asset":
            existingDeps = self.core.projects.getAssetDepartments()
        elif entity in ["shot", "sequence"]:
            existingDeps = self.core.projects.getShotDepartments()

        if department not in [d["abbreviation"] for d in existingDeps]:
            msgStr = (
                "Department '%s' doesn't exist in the project config. Couldn't get default task."
                % department
            )
            logger.debug(msgStr)
            return

        tasks = [d for d in existingDeps if d["abbreviation"] == department][0]["defaultTasks"]
        if not isinstance(tasks, list):
            tasks = [tasks]

        return tasks

    @err_catcher(name=__name__)
    def createDefaultCat(self, entity, step):
        tasks = self.getDefaultTasksForDepartment(entity["type"], step)
        if not tasks:
            return

        paths = []
        for category in tasks:
            paths.append(self.createCategory(entity, step, category))

        return paths

    @err_catcher(name=__name__)
    def createCategory(self, entity, step, category):
        catPath = self.core.getEntityPath(entity=entity, step=step, category=category)
        if not os.path.exists(catPath):
            try:
                os.makedirs(catPath)
            except:
                self.core.popup("The directory %s could not be created" % catPath)
                return
            else:
                self.core.callback(
                    name="onTaskCreated",
                    args=[self, entity, step, category, catPath],
                )

            logger.debug("task created %s" % catPath)
        else:
            logger.debug("task already exists: %s" % catPath)

        return catPath

    @err_catcher(name=__name__)
    def createTasksFromPreset(self, entity, preset=None, presetName=None):
        if not preset and presetName:
            if entity.get("type") == "asset":
                presets = self.core.projects.getAssetTaskPresets()
            else:
                presets = self.core.projects.getShotTaskPresets()

            for p in presets:
                if p.get("name") == presetName:
                    preset = p
                    break
            else:
                self.core.popup("Invalid preset name: %s" % presetName)
                return

        logger.debug("creating tasks from preset - entity: %s - preset: %s" % (entity, preset))
        paths = []
        for dep in preset.get("departments", []):
            abbrv = self.getDepartmentAbbreviation(entity.get("type"), dep["name"])
            if not abbrv:
                continue

            self.createDepartment(abbrv, entity, createCat=False)
            for task in dep.get("tasks", []):
                paths.append(self.createCategory(entity, abbrv, task))

        return paths

    @err_catcher(name=__name__)
    def getTaskDataPath(self, entity, department, task):
        taskPath = self.core.getEntityPath(entity=entity, step=department, category=task)
        filename = "info" + self.core.configs.getProjectExtension()
        infoPath = os.path.join(taskPath, filename)
        return infoPath

    @err_catcher(name=__name__)
    def getTaskData(self, entity, department, task):
        infoPath = self.getTaskDataPath(entity, department, task)
        data = self.core.getConfig(configPath=infoPath)
        return data

    @err_catcher(name=__name__)
    def setTaskData(self, entity, department, task, key, val):
        infoPath = self.getTaskDataPath(entity, department, task)
        self.core.setConfig(key, val=val, configPath=infoPath)
        return True

    @err_catcher(name=__name__)
    def omitEntity(self, entity, omit=True):
        if entity["type"] == "assetFolder":
            entityType = "asset"
        else:
            entityType = entity["type"]

        if entityType == "asset":
            entityName = entity["asset_path"]
        elif entityType == "shot":
            entityName = self.core.entities.getShotName(entity)

        omits = self.core.getConfig(entityType, config="omit")
        if omit:
            if entityType == "asset":
                if not omits:
                    omits = []

                if entityName not in omits:
                    omits.append(entityName)
            elif entityType == "shot":
                if not omits:
                    omits = {}

                if not entity["sequence"] in omits:
                    omits[entity["sequence"]] = []

                if entity["shot"] not in omits[entity["sequence"]]:
                    omits[entity["sequence"]].append(entity["shot"])

            self.core.setConfig(entityType, val=omits, config="omit")
            logger.debug("omitted %s %s" % (entityType, entityName))
        else:
            if not omits:
                return False

            if entityType == "asset":
                if entityName.replace("\\", "/") in omits:
                    omits.remove(entityName.replace("\\", "/"))
                elif entityName.replace("/", "\\") in omits:
                    omits.remove(entityName.replace("/", "\\"))
                else:
                    return False

            elif entityType == "shot":
                if entity["sequence"] not in omits:
                    return False

                if entity["shot"] not in omits[entity["sequence"]]:
                    return False

                omits[entity["sequence"]].remove(entity["shot"])

            self.core.setConfig(entityType, val=omits, config="omit")
            logger.debug("restored %s %s" % (entityType, entityName))

        self.refreshOmittedEntities()
        return True

    @err_catcher(name=__name__)
    def setComment(self, filepath, comment):
        newPath = ""
        data = self.core.getScenefileData(filepath)

        if self.core.useLocalFiles:
            localPath = filepath.replace(
                self.core.projectPath, self.core.localProjectPath
            )
            if os.path.exists(localPath):
                localData = self.core.getScenefileData(localPath)
                scenedata = {"entity": localData}
                if "department" in localData:
                    scenedata["department"] = localData["department"]

                if "task" in localData:
                    scenedata["task"] = localData["task"]

                if "extension" in localData:
                    scenedata["extension"] = localData["extension"]

                if "version" in localData:
                    scenedata["version"] = localData["version"]

                if "user" in localData:
                    scenedata["user"] = localData["user"]

                scenedata["comment"] = comment
                if "department" in localData:
                    newPath = self.core.generateScenePath(**scenedata)
                    self.core.copySceneFile(localPath, newPath, mode="move")
                else:
                    newPath = localPath

                self.setScenefileInfo(newPath, "comment", comment)

        if os.path.exists(filepath):
            scenedata = {"entity": data}
            if "department" in data:
                scenedata["department"] = data["department"]

            if "task" in data:
                scenedata["task"] = data["task"]

            if "extension" in data:
                scenedata["extension"] = data["extension"]

            if "version" in data:
                scenedata["version"] = data["version"]

            if "user" in data:
                scenedata["user"] = data["user"]

            scenedata["comment"] = comment
            if "department" in data:
                newPath = self.core.generateScenePath(**scenedata)
                self.core.copySceneFile(filepath, newPath, mode="move")
            else:
                newPath = filepath

            self.setScenefileInfo(newPath, "comment", comment)

        return newPath

    @err_catcher(name=__name__)
    def setDescription(self, filepath, description):
        self.setScenefileInfo(filepath, "description", description)

    @err_catcher(name=__name__)
    def getAssetDescription(self, assetName, projectPath=None):
        pipeFolder = self.core.projects.getPipelineFolder()
        if projectPath:
            pipeFolder = pipeFolder.replace(os.path.normpath(self.core.projectPath), projectPath)

        assetFile = os.path.join(
            pipeFolder,
            "Assetinfo",
            "assetInfo" + self.core.configs.getProjectExtension(),
        )

        description = ""

        assetInfos = self.core.getConfig(configPath=assetFile)
        if not assetInfos:
            assetInfos = {}

        if assetName in assetInfos and "description" in assetInfos[assetName]:
            description = assetInfos[assetName]["description"]

        return description

    @err_catcher(name=__name__)
    def setAssetDescription(self, assetName, description):
        assetFile = os.path.join(
            self.core.projects.getPipelineFolder(),
            "Assetinfo",
            "assetInfo" + self.core.configs.getProjectExtension(),
        )
        assetInfos = self.core.getConfig(configPath=assetFile)
        if not assetInfos:
            assetInfos = {}

        if assetName not in assetInfos:
            assetInfos[assetName] = {}

        assetInfos[assetName]["description"] = description

        self.core.setConfig(data=assetInfos, configPath=assetFile)

    @err_catcher(name=__name__)
    def getMetaData(self, entity, projectPath=None):
        metadata = {}
        if not entity:
            return metadata

        if entity.get("type") == "asset":
            if projectPath:
                pipeFolder = self.core.projects.getPipelineFolder()
                pipeFolder = pipeFolder.replace(os.path.normpath(self.core.projectPath), projectPath)
                assetFile = os.path.join(
                    pipeFolder,
                    "Assetinfo",
                    "assetInfo" + self.core.configs.getProjectExtension(),
                )
                data = self.core.getConfig(configPath=assetFile) or {}
            else:
                data = self.core.getConfig(config="assetinfo") or {}

            if "assets" not in data:
                return metadata

            if "asset_path" not in entity:
                return metadata

            entityName = self.core.entities.getAssetNameFromPath(entity["asset_path"])
            if entityName not in data["assets"]:
                return metadata

            metadata = data["assets"][entityName].get("metadata", {})

        elif entity.get("type") == "shot":
            data = self.core.getConfig(config="shotinfo") or {}
            if "shots" not in data:
                return metadata

            if entity.get("sequence", "") not in data["shots"]:
                return metadata

            if entity["shot"] not in data["shots"][entity["sequence"]]:
                return metadata

            metadata = data["shots"][entity["sequence"]][entity["shot"]].get("metadata", {})

        return metadata

    @err_catcher(name=__name__)
    def setMetaData(self, entity=None, metaData=None, entities=None, metaDatas=None):
        if entity and not entities:
            entities = [entity]
            metaDatas = [metaData]

        assetConfig = None
        shotConfig = None
        for idx, entity in enumerate(entities):
            metaData = metaDatas[idx]
            if entity["type"] == "asset":
                if assetConfig is None:
                    assetConfig = self.core.getConfig(config="assetinfo", allowCache=False) or {}

                if "assets" not in assetConfig:
                    assetConfig["assets"] = {}

                entityName = self.core.entities.getAssetNameFromPath(entity["asset_path"])
                if entityName not in assetConfig["assets"]:
                    assetConfig["assets"][entityName] = {}

                assetConfig["assets"][entityName]["metadata"] = metaData
            elif entity["type"] == "shot":
                if shotConfig is None:
                    shotConfig = self.core.getConfig(config="shotinfo", allowCache=False) or {}

                if "shots" not in shotConfig:
                    shotConfig["shots"] = {}

                if entity["sequence"] not in shotConfig["shots"]:
                    shotConfig["shots"][entity["sequence"]] = {}

                if entity["shot"] not in shotConfig["shots"][entity["sequence"]]:
                    shotConfig["shots"][entity["sequence"]][entity["shot"]] = {}

                shotConfig["shots"][entity["sequence"]][entity["shot"]]["metadata"] = metaData
        
        if assetConfig is not None:
            self.core.setConfig(data=assetConfig, config="assetinfo", updateNestedData=False)

        if shotConfig is not None:
            self.core.setConfig(data=shotConfig, config="shotinfo", updateNestedData=False)

    @err_catcher(name=__name__)
    def deleteShot(self, shotName):
        shotPath = self.core.getEntityPath(shot=shotName)
        while True:
            try:
                if os.path.exists(shotPath):
                    shutil.rmtree(shotPath)
                if self.core.useLocalFiles:
                    lShotPath = shotPath.replace(
                        self.core.projectPath, self.core.localProjectPath
                    )
                    if os.path.exists(lShotPath):
                        shutil.rmtree(lShotPath)
                break
            except Exception as e:
                msg = (
                    'Permission denied.\nAnother programm uses files in the shotfolder.\n\nThe shot "%s" could not be deleted completly.\n\n%s'
                    % (shotName, str(e)),
                )
                result = self.core.popupQuestion(msg, buttons=["Retry", "Cancel"])
                if result == "Cancel":
                    self.core.popup("Deleting shot canceled.")
                    break

    @err_catcher(name=__name__)
    def renameEpisode(self, curEpName, newEpName, locations=None):
        epFolder = os.path.normpath(self.core.getEntityPath(entity={"type": "episode", "episode": curEpName}))
        newEpFolder = os.path.normpath(self.core.getEntityPath(entity={"type": "episode", "episode": newEpName}))
        epFolders = {}
        if not locations or "global" in locations:
            epFolders[epFolder] = newEpFolder

        if self.core.useLocalFiles:
            if not locations or "local" in locations:
                lEpFolder = epFolder.replace(
                    self.core.projectPath, self.core.localProjectPath
                )
                newLEpFolder = newEpFolder.replace(
                    self.core.projectPath, self.core.localProjectPath
                )
                epFolders[lEpFolder] = newLEpFolder

        curShots = self.getShotsFromEpisode(curEpName)

        while True:
            try:
                for k in epFolders:
                    if os.path.exists(k):
                        os.rename(k, epFolders[k])

                    cwd = os.getcwd()
                    for i in os.walk(epFolders[k]):
                        os.chdir(i[0])
                        for k in i[1]:
                            if curEpName in k:
                                os.rename(k, k.replace(curEpName, newEpName))
                        for k in i[2]:
                            if os.path.splitext(k)[1] == self.core.configs.preferredExtension:
                                filepath = os.path.join(i[0], k)
                                fepName = self.core.getConfig("episode", configPath=filepath)
                                if fepName == curEpName:
                                    self.core.setConfig("episode", val=newEpName, configPath=filepath)

                            if curEpName in k:
                                os.rename(k, k.replace(curEpName, newEpName))
                    os.chdir(cwd)

                break

            except Exception as e:
                logger.debug(e)
                msg = QMessageBox(
                    QMessageBox.Warning,
                    "Warning",
                    'Permission denied.\nAnother programm uses files in the epsidoefolder.\n\nThe episode "%s" could not be renamed to "%s" completly.\n\n%s'
                    % (curEpName, curEpName, str(e)),
                    QMessageBox.Cancel,
                )
                msg.addButton("Retry", QMessageBox.YesRole)
                self.core.parentWindow(msg)
                action = msg.exec_()

                if action != 0:
                    self.core.popup("Renaming episode canceled.")
                    return

        for curShot in curShots:
            oldPrvPath = self.getEntityPreviewPath(curShot)
            newShot = curShot.copy()
            newShot["episode"] = newEpName
            newPrvPath = self.getEntityPreviewPath(newShot)
            if os.path.exists(oldPrvPath):
                os.rename(oldPrvPath, newPrvPath)

        curRange = self.core.getConfig("shotRanges", config="shotinfo")
        if curRange and curEpName in curRange:
            cursRange = curRange[curEpName]
            del curRange[curEpName]
            curRange[newEpName] = cursRange
            self.core.setConfig("shotRanges", val=curRange, config="shotinfo")

        curRange = self.core.getConfig("shots", config="shotinfo")
        if curRange and curEpName in curRange:
            cursRange = curRange[curEpName]
            del curRange[curEpName]
            curRange[newEpName] = cursRange
            self.core.setConfig("shots", val=curRange, config="shotinfo")

    @err_catcher(name=__name__)
    def renameSequence(self, curSeqName, newSeqName, locations=None):
        seqFolder = os.path.normpath(self.core.getEntityPath(entity={"type": "sequence", "sequence": curSeqName}))
        newSeqFolder = os.path.normpath(self.core.getEntityPath(entity={"type": "sequence", "sequence": newSeqName}))
        seqFolders = {}
        if not locations or "global" in locations:
            seqFolders[seqFolder] = newSeqFolder

        if self.core.useLocalFiles:
            if not locations or "local" in locations:
                lSeqFolder = seqFolder.replace(
                    self.core.projectPath, self.core.localProjectPath
                )
                newLSeqFolder = newSeqFolder.replace(
                    self.core.projectPath, self.core.localProjectPath
                )
                seqFolders[lSeqFolder] = newLSeqFolder

        curShots = self.getShots(sequence=curSeqName)
        while True:
            try:
                for k in seqFolders:
                    if os.path.exists(k):
                        os.rename(k, seqFolders[k])

                    cwd = os.getcwd()
                    for i in os.walk(seqFolders[k]):
                        os.chdir(i[0])
                        for k in i[1]:
                            if curSeqName in k:
                                os.rename(k, k.replace(curSeqName, newSeqName))
                        for k in i[2]:
                            if os.path.splitext(k)[1] == self.core.configs.preferredExtension:
                                filepath = os.path.join(i[0], k)
                                fseqName = self.core.getConfig("sequence", configPath=filepath)
                                if fseqName == curSeqName:
                                    self.core.setConfig("sequence", val=newSeqName, configPath=filepath)

                            if curSeqName in k:
                                os.rename(k, k.replace(curSeqName, newSeqName))
                    os.chdir(cwd)

                break

            except Exception as e:
                logger.debug(e)
                msg = QMessageBox(
                    QMessageBox.Warning,
                    "Warning",
                    'Permission denied.\nAnother programm uses files in the sequencefolder.\n\nThe sequence "%s" could not be renamed to "%s" completly.\n\n%s'
                    % (curSeqName, curSeqName, str(e)),
                    QMessageBox.Cancel,
                )
                msg.addButton("Retry", QMessageBox.YesRole)
                self.core.parentWindow(msg)
                action = msg.exec_()

                if action != 0:
                    self.core.popup("Renaming sequence canceled.")
                    return

        for curShot in curShots:
            oldPrvPath = self.getEntityPreviewPath(curShot)
            newShot = curShot.copy()
            newShot["sequence"] = newSeqName
            newPrvPath = self.getEntityPreviewPath(newShot)
            if os.path.exists(oldPrvPath):
                os.rename(oldPrvPath, newPrvPath)

        curRange = self.core.getConfig("shotRanges", config="shotinfo")
        if curRange and curSeqName in curRange:
            cursRange = curRange[curSeqName]
            del curRange[curSeqName]
            curRange[newSeqName] = cursRange
            self.core.setConfig("shotRanges", val=curRange, config="shotinfo")

        curRange = self.core.getConfig("shots", config="shotinfo")
        if curRange and curSeqName in curRange:
            cursRange = curRange[curSeqName]
            del curRange[curSeqName]
            curRange[newSeqName] = cursRange
            self.core.setConfig("shots", val=curRange, config="shotinfo")

    @err_catcher(name=__name__)
    def renameShot(self, curShotData, newShotData, locations=None):
        shotFolder = os.path.normpath(self.core.getEntityPath(entity=curShotData))
        newShotFolder = os.path.normpath(self.core.getEntityPath(entity=newShotData))
        shotFolders = {}
        if not locations or "global" in locations:
            shotFolders[shotFolder] = newShotFolder

        if self.core.useLocalFiles:
            if not locations or "local" in locations:
                lShotFolder = shotFolder.replace(
                    self.core.projectPath, self.core.localProjectPath
                )
                newLShotFolder = newShotFolder.replace(
                    self.core.projectPath, self.core.localProjectPath
                )
                shotFolders[lShotFolder] = newLShotFolder

        while True:
            try:
                for k in shotFolders:
                    if os.path.exists(k):
                        os.rename(k, shotFolders[k])

                    cwd = os.getcwd()
                    for i in os.walk(shotFolders[k]):
                        os.chdir(i[0])
                        for k in i[1]:
                            if curShotData["shot"] in k:
                                os.rename(k, k.replace(curShotData["shot"], newShotData["shot"]))
                        for k in i[2]:
                            if os.path.splitext(k)[1] == self.core.configs.preferredExtension:
                                filepath = os.path.join(i[0], k)
                                shotName = self.core.getConfig("shot", configPath=filepath)
                                if shotName == curShotData["shot"]:
                                    self.core.setConfig("shot", val=newShotData["shot"], configPath=filepath)

                            if curShotData["shot"] in k:
                                os.rename(k, k.replace(curShotData["shot"], newShotData["shot"]))

                    os.chdir(cwd)

                oldPrvPath = self.getEntityPreviewPath(curShotData)
                newPrvPath = self.getEntityPreviewPath(newShotData)
                if os.path.exists(oldPrvPath):
                    os.rename(oldPrvPath, newPrvPath)

                break

            except Exception as e:
                logger.debug(e)
                msg = 'Permission denied.\nAnother programm uses files in the shotfolder.\n\nThe shot "%s" could not be renamed to "%s" completly.\n\n%s' % (self.getShotName(curShotData), self.getShotName(newShotData), str(e))
                result = self.core.popupQuestion(msg, buttons=["Retry", "Cancel"], icon=QMessageBox.Warning)
                if result != "Retry":
                    self.core.popup("Renaming shot canceled.")
                    return

        curRange = self.core.getConfig("shotRanges", curShotData["sequence"], config="shotinfo")
        if curRange and curShotData["shot"] in curRange:
            cursRange = curRange[curShotData["shot"]]
            del curRange[curShotData["shot"]]
            curRange[newShotData["shot"]] = cursRange
            self.core.setConfig("shotRanges", curShotData["sequence"], curRange, config="shotinfo")

        curRange = self.core.getConfig("shots", curShotData["sequence"], config="shotinfo")
        if curRange and curShotData["shot"] in curRange:
            cursRange = curRange[curShotData["shot"]]
            del curRange[curShotData["shot"]]
            curRange[newShotData["shot"]] = cursRange
            self.core.setConfig("shots", curShotData["sequence"], curRange, config="shotinfo")

    @err_catcher(name=__name__)
    def getAssetSubFolders(self):
        subfolders = []

        template = self.core.projects.getTemplatePath("departments")
        template = template.replace("\\", "/")
        sceneFolder = template.split("/")[1]
        if sceneFolder:
            subfolders.append(sceneFolder)

        template = self.core.projects.getTemplatePath("products")
        template = template.replace("\\", "/")
        productFolder = template.split("/")[1]
        if productFolder:
            subfolders.append(productFolder)

        template = self.core.projects.getTemplatePath("3drenders")
        template = template.replace("\\", "/")
        renderFolder = template.split("/")[1]
        if renderFolder:
            subfolders.append(renderFolder)

        template = self.core.projects.getTemplatePath("playblasts")
        template = template.replace("\\", "/")
        playblastFolder = template.split("/")[1]
        if playblastFolder:
            subfolders.append(playblastFolder)

        return subfolders

    @err_catcher(name=__name__)
    def getTypeFromAssetPath(self, path, content=None):
        if not os.path.exists(path):
            return

        if content is None:
            content = os.listdir(path)

        subfolders = self.getAssetSubFolders()

        if self.core.getConfig(
            "globals", "useStrictAssetDetection", dft=False, config="project"
        ):
            isAsset = True
            for folder in subfolders:
                if folder not in content:
                    isAsset = False

        else:
            isAsset = False
            for folder in subfolders:
                if folder in content:
                    isAsset = True

        if isAsset:
            return "asset"
        else:
            return "folder"

    @err_catcher(name=__name__)
    def getAsset(self, assetName, projectPath=None):
        base = self.core.assetPath
        if projectPath:
            base = base.replace(os.path.normpath(self.core.projectPath), projectPath)

        fullAssetPath = os.path.join(base, assetName)
        existed = os.path.exists(fullAssetPath)
        if existed:
            return {"type": "asset", "asset_path": assetName}
        else:
            return

    @err_catcher(name=__name__)
    def getAssets(self, path=None, depth=0):
        assets = []
        paths = self.getAssetPaths(path=path, depth=depth)
        assets = [{"type": "asset", "asset_path": self.getAssetRelPathFromPath(p)} for p in paths]
        return assets

    @err_catcher(name=__name__)
    def getAssetPaths(self, path=None, returnFolders=False, depth=0):
        aBasePath = path or self.core.assetPath
        assets = []
        assetFolders = []

        for root, folders, files in os.walk(aBasePath):
            for folder in folders:
                folderPath = os.path.join(root, folder)
                if self.getTypeFromAssetPath(folderPath) == "asset":
                    assets.append(folderPath)
                else:
                    if depth == 1:
                        assetFolders.append(folderPath)
                    else:
                        nextDepth = 0 if depth == 0 else (depth - 1)
                        childAssets, childFolders = self.getAssetPaths(
                            path=folderPath, returnFolders=True, depth=nextDepth
                        )
                        if childAssets or childFolders:
                            assets += childAssets
                            assetFolders += childFolders
                        else:
                            assetFolders.append(folderPath)
            break

        if returnFolders:
            return assets, assetFolders
        else:
            return assets

    @err_catcher(name=__name__)
    def getEmptyAssetFolders(self):
        assets, folders = self.getAssetPaths(returnFolders=True)
        emptyFolders = []
        for folder in folders:
            for asset in assets:
                if folder in asset:
                    break
            else:
                for folder2 in folders:
                    if folder in folder2 and len(folder) < len(folder2):
                        break
                else:
                    emptyFolders.append(folder)

        return emptyFolders

    @err_catcher(name=__name__)
    def getAssetPathFromAssetName(self, assetName):
        if os.path.isabs(assetName):
            assetPath = assetName
        else:
            assetPaths = self.getAssetPaths()
            path = os.path.join(self.core.assetPath, assetName)
            if path in assetPaths:
                assetPath = path
            else:
                for assetPath in assetPaths:
                    if os.path.basename(assetPath) == assetName:
                        assetPath = assetPath
                        break
                else:
                    return

        return assetPath

    @err_catcher(name=__name__)
    def getAssetFoldersFromPath(self, path, pathType="asset"):
        relPath = self.getAssetRelPathFromPath(path)
        folders = os.path.normpath(relPath).split(os.sep)
        if pathType == "asset":
            folders = folders[:-1]
        return folders

    @err_catcher(name=__name__)
    def filterAssets(self, assets, filterStr, projectPath=None):
        filteredPaths = []
        for absAssetPath in assets:
            base = self.core.assetPath
            if projectPath:
                base = base.replace(os.path.normpath(self.core.projectPath), projectPath)

            assetPath = absAssetPath.replace(base, "")
            if self.core.useLocalFiles:
                localAssetPath = self.core.getAssetPath(location="local")
                assetPath = assetPath.replace(localAssetPath, "")
            assetPath = assetPath[1:]

            if filterStr.lower() in assetPath.lower():
                filteredPaths.append(absAssetPath)
            else:
                description = self.getAssetDescription(self.getAssetNameFromPath(assetPath), projectPath=projectPath) or ""
                if filterStr.lower() in description.lower():
                    filteredPaths.append(absAssetPath)
                else:
                    entity = self.getAsset(assetPath, projectPath=projectPath)
                    metaData = self.getMetaData(entity, projectPath=projectPath)
                    if metaData and "tags" in metaData:
                        tags = [x.strip() for x in metaData["tags"]["value"].split(",")]
                        if filterStr in tags:
                            filteredPaths.append(absAssetPath)

        return filteredPaths

    @err_catcher(name=__name__)
    def filterOmittedAssets(self, assets):
        filteredPaths = []
        for absAssetPath in assets:
            assetName = self.getAssetRelPathFromPath(absAssetPath)
            if assetName not in self.omittedEntities["asset"]:
                filteredPaths.append(absAssetPath)

        return filteredPaths

    @err_catcher(name=__name__)
    def isAssetPathOmitted(self, assetPath):
        isOmitted = not bool(self.filterOmittedAssets([assetPath]))
        return isOmitted

    @err_catcher(name=__name__)
    def isValidAssetName(self, assetName):
        if self.core.getConfig("globals", "useStrictAssetDetection"):
            return True
        else:
            return assetName not in self.getAssetSubFolders()

    @err_catcher(name=__name__)
    def getAssetNameFromPath(self, path):
        return os.path.basename(path)

    @err_catcher(name=__name__)
    def getAssetRelPathFromPath(self, path, projectPath=None):
        path = self.core.convertPath(path, "global")
        base = self.core.assetPath
        if projectPath:
            base = base.replace(os.path.normpath(self.core.projectPath), projectPath)

        return path.replace(base, "").strip("\\").strip("/")

    @err_catcher(name=__name__)
    def getScenefileData(self, fileName, preview=False, getEntityFromPath=False):
        data = self.core.getConfig(configPath=self.getScenefileInfoPath(fileName)) or {}
        data = dict(data)
        if fileName and (not data or getEntityFromPath):
            compatData = self.core.paths.getSimplifiedScenefileData(fileName)
            entityType = self.core.paths.getEntityTypeFromPath(fileName)
            key = None
            if entityType == "asset":
                key = "assetScenefiles"
            elif entityType == "shot":
                key = "shotScenefiles"

            if key:
                template = self.core.projects.getTemplatePath(key)
                hasData = bool(data)
                data["type"] = entityType
                data["entityType"] = entityType
                pathData = compatData or self.core.projects.extractKeysFromPath(
                    fileName, template, context=data
                )
                if pathData.get("asset_path"):
                    pathData["asset"] = os.path.basename(pathData["asset_path"])

                if not hasData:
                    data = pathData
                elif getEntityFromPath:
                    if entityType == "asset":
                        if "asset" in pathData:
                            data["asset"] = pathData["asset"]

                        if "asset_path" in pathData:
                            data["asset_path"] = pathData["asset_path"]
                    if entityType == "shot":
                        if "shot" in pathData:
                            data["shot"] = pathData["shot"]

                        if "sequence" in pathData:
                            data["sequence"] = pathData["sequence"]

                        if "episode" in pathData:
                            data["episode"] = pathData["episode"]

                if compatData:
                    data["department"] = compatData.get("department")
                    data["task"] = compatData.get("task")

        if fileName:
            data["filename"] = fileName
            data["extension"] = os.path.splitext(fileName)[1]

        if "type" not in data:
            etype = self.core.paths.getEntityTypeFromPath(fileName)
            if etype:
                data["type"] = etype

        data["locations"] = {}
        glbPath = self.core.convertPath(fileName, "global")
        if os.path.exists(glbPath):
            data["locations"]["global"] = glbPath

        if (
            self.core.useLocalFiles
            and os.path.exists(self.core.convertPath(fileName, "local"))
        ):
            data["locations"]["local"] = self.core.convertPath(fileName, "local")

        if preview:
            prvPath = os.path.splitext(fileName)[0] + "preview.jpg"
            if os.path.exists(prvPath):
                data["preview"] = prvPath

        return data

    @err_catcher(name=__name__)
    def getCurrentScenefileData(self):
        fn = self.core.getCurrentFileName()
        return self.getScenefileData(fn)

    @err_catcher(name=__name__)
    def getScenePreviewPath(self, scenepath):
        return os.path.splitext(scenepath)[0] + "preview.jpg"

    @err_catcher(name=__name__)
    def setScenePreview(self, scenepath, preview):
        prvPath = self.getScenePreviewPath(scenepath)
        self.core.media.savePixmap(preview, prvPath)

    @err_catcher(name=__name__)
    def getScenefileInfoPath(self, scenePath):
        return (
            os.path.splitext(scenePath)[0]
            + "versioninfo"
            + self.core.configs.getProjectExtension()
        )

    @err_catcher(name=__name__)
    def setScenefileInfo(self, scenePath, key, value):
        infoPath = self.getScenefileInfoPath(scenePath)

        sceneInfo = {}
        if os.path.exists(infoPath):
            sceneInfo = self.core.getConfig(configPath=infoPath) or {}

        sceneInfo[key] = value
        self.core.setConfig(data=sceneInfo, configPath=infoPath)

    @err_catcher(name=__name__)
    def getHighestVersion(
        self,
        entity,
        department,
        task,
        getExistingPath=False,
        fileTypes="*",
        localVersions=True,
        getExistingVersion=False,
    ):
        department = self.core.paths.normalizeDepartment(
            department, context=entity, reason="version lookup"
        )
        task = self.core.paths.normalizeTask(
            task, context=entity, reason="version lookup"
        )
        scenefiles = self.getScenefiles(entity=entity, step=department, category=task)
        highversion = [None, ""]
        for scenefile in scenefiles:
            ext = os.path.splitext(scenefile)[1]
            if fileTypes != "*" and ext not in fileTypes:
                continue

            if not self.isValidScenefilename(scenefile):
                continue

            fname = self.core.getScenefileData(scenefile)
            if fname.get("type") != entity.get("type"):
                continue

            try:
                version = int(fname["version"][-self.core.versionPadding:])
            except:
                continue

            if (
                ext.lower() in self.core.media.supportedFormats
                and self.core.versionFormat.startswith("v")
                and fname["version"][-(self.core.versionPadding+1)] != "v"
            ):
                continue

            if highversion[0] is None or version > highversion[0]:
                highversion = [version, scenefile]

        if getExistingVersion:
            return highversion
        elif getExistingPath:
            return highversion[1]
        else:
            if highversion[0] is None:
                return self.core.versionFormat % (self.core.lowestVersion)
            else:
                return self.core.versionFormat % (highversion[0] + 1)

    @err_catcher(name=__name__)
    def getTaskNames(self, taskType=None, locations=None, context=None, key=None, taskname=None, addDepartments=True):
        if key is None:
            if taskType == "export":
                key = "products"
            elif taskType == "3d":
                key = "3drenders"
            elif taskType == "2d":
                key = "2drenders"
            elif taskType == "playblast":
                key = "playblasts"
            elif taskType == "external":
                key = "externalMedia"
            elif taskType == "textures":
                key = "textures"
            else:
                raise Exception("Invalid taskType: %s" % taskType)

        context = context or {}
        fname = self.core.getCurrentFileName()
        fnameData = self.core.getScenefileData(fname)
        context.update(fnameData)
        if "version" in context:
            del context["version"]

        if "type" in context:
            departmentNames = self.getCategories(
                context, step=context.get("department")
            )
        else:
            departmentNames = []

        if key == "products":
            locations = self.core.paths.getExportProductBasePaths()
        else:
            locations = self.core.paths.getRenderProductBasePaths()

        productDirs = []
        for location in locations:
            if locations is not None and location not in locations:
                continue

            productDir = {"location": location, "path": locations[location]}
            productDirs.append(productDir)

        productDicts = []
        for productDir in productDirs:
            context["project_path"] = productDir["path"]
            template = self.core.projects.getResolvedProjectStructurePath(
                key, context=context
            )
            productData = self.core.projects.getMatchingPaths(template)
            productDicts += productData

        taskList = []
        for data in productDicts:
            if taskname is None:
                if key == "products":
                    taskname = "product"
                else:
                    taskname = "identifier"

            taskList.append(data[taskname])

        if addDepartments:
            taskList += departmentNames

        taskList = list(set(taskList))
        return taskList

    @err_catcher(name=__name__)
    def getEntityPreviewPath(self, entity):
        if entity["type"] == "asset":
            folderName = "Assetinfo"
            entityName = self.getAssetNameFromPath(entity.get("asset_path", ""))
        elif entity["type"] in ["shot", "sequence", "episode"]:
            folderName = "Shotinfo"
            if entity["type"] == "episode":
                entityName = "ep_%s" % entity["episode"]
            elif entity["type"] == "sequence":
                entityName = "seq_%s" % entity["sequence"]
            elif entity["type"] == "shot":
                entityName = self.getShotName(entity)

        ext = os.getenv("PRISM_ENTITY_THUMBNAIL_EXT", ".jpg")
        imgName = "%s_preview%s" % (entityName, ext)
        pipeFolder = self.core.projects.getPipelineFolder()
        if entity.get("project_path"):
            pipeFolder = pipeFolder.replace(os.path.normpath(self.core.projectPath), entity["project_path"])

        imgPath = os.path.join(
            pipeFolder, folderName, imgName
        )
        return imgPath

    @err_catcher(name=__name__)
    def getEntityPreview(self, entity, width=None, height=None):
        pm = None
        imgPath = self.getEntityPreviewPath(entity)
        if os.path.exists(imgPath):
            pm = self.core.media.getPixmapFromPath(imgPath)
            if width and height:
                pm = self.core.media.scalePixmap(pm, width, height)

        return pm

    @err_catcher(name=__name__)
    def setEntityPreview(self, entity, pixmap, width=250, height=141):
        if not pixmap:
            logger.debug("invalid pixmap")
            return

        if (pixmap.width() / float(pixmap.height())) > 1.7778:
            pmsmall = pixmap.scaledToWidth(width)
        else:
            pmsmall = pixmap.scaledToHeight(height)

        prvPath = self.getEntityPreviewPath(entity)
        logger.debug("setting entity preview for: %s" % entity)
        self.core.media.savePixmap(pmsmall, prvPath)
        return pmsmall

    @err_catcher(name=__name__)
    def getPresetScene(self, name):
        presets = self.getPresetScenes()
        for preset in presets:
            if preset["label"] == name or os.path.basename(preset["path"]) == name:
                return preset

    @err_catcher(name=__name__)
    def getPresetScenes(self):
        presetDir = os.path.join(self.core.projects.getPipelineFolder(), "PresetScenes")
        folders = [presetDir]
        folders += [x.strip() for x in os.getenv("PRISM_SCENEFILE_PRESET_PATHS", "").split(os.pathsep) if x]
        presetScenes = []
        for folder in folders:
            presetScenes += self.getPresetScenesFromFolder(folder)

        self.core.callback("getPresetScenes", args=[presetScenes])
        return presetScenes

    @err_catcher(name=__name__)
    def getBlacklistedExtensions(self):
        extsStr = os.getenv("PRISM_BLACKLISTED_EXTENSIONS", "")
        exts = [ext.strip() for ext in extsStr.split(",")]
        return exts

    @err_catcher(name=__name__)
    def getPresetScenesFromFolder(self, folder):
        presetScenes = []
        if os.path.exists(folder):
            blacklisted = self.getBlacklistedExtensions()
            for root, folders, files in os.walk(folder):
                for filename in sorted(files):
                    if filename == "readme.txt":
                        continue

                    if filename.startswith(".") or filename.startswith("_"):
                        continue

                    if blacklisted:
                        _, ext = os.path.splitext(filename)
                        if ext in blacklisted:
                            continue

                    relPresetDir = root.replace(folder, "")
                    if relPresetDir:
                        presetName = (
                            relPresetDir[1:].replace("\\", "/") + "/" + filename
                        )
                    else:
                        presetName = filename

                    presetName = os.path.splitext(presetName)[0]
                    path = os.path.join(root, filename)
                    presetScenes.append({"label": presetName, "path": path})

        return presetScenes

    @err_catcher(name=__name__)
    def getScenePresetPathFromName(self, name):
        scenes = self.getPresetScenes()
        for scene in scenes:
            if scene["label"] == name:
                return scene["path"]

    @err_catcher(name=__name__)
    def ingestScenefiles(self, files, entity, department, task, finishCallback=None, data=None, rename=True):
        kwargs = {
            "entity": entity,
            "department": department,
            "task": task,
            "comment": "",
            "user": self.core.user,
        }
        version = self.core.entities.getHighestVersion(entity, department, task)
        kwargs["version"] = version
        if data:
            kwargs.update(data)

        createdFiles = []
        for idx, file in enumerate(files):
            kwargs["extension"] = os.path.splitext(file)[1]
            targetPath = self.core.paths.generateScenePath(**kwargs)
            if self.core.useLocalFiles:
                targetPath = self.core.convertPath(targetPath, target="local")

            if not rename:
                targetPath = os.path.join(os.path.dirname(targetPath), os.path.basename(file))

            if not os.path.exists(os.path.dirname(targetPath)):
                try:
                    os.makedirs(os.path.dirname(targetPath))
                except:
                    self.core.popup("The directory could not be created")
                    return

            targetPath = targetPath.replace("\\", "/")

            thread = self.core.copyWithProgress(file, targetPath, finishCallback=finishCallback)
            thread.wait(999999999)
            details = entity.copy()
            details["department"] = department
            details["task"] = task
            details["user"] = kwargs["user"]
            details["version"] = kwargs["version"]
            details["comment"] = kwargs["comment"]
            details["extension"] = kwargs["extension"]
            self.core.saveSceneInfo(targetPath, details=details)
            createdFiles.append(targetPath)
            logger.debug("ingested scenefile: %s" % targetPath)

        return createdFiles

    @err_catcher(name=__name__)
    def createSceneFromPreset(
        self,
        entity,
        fileName,
        step=None,
        category=None,
        comment=None,
        version=None,
        location="local",
    ):
        comment = comment or ""
        user = self.core.user

        if entity["type"] not in ["asset", "shot"]:
            self.core.popup("Invalid entity:\n\n%s" % entity["type"])
            return

        if not version:
            version = self.core.entities.getHighestVersion(entity, step, category)

        if os.path.isabs(fileName):
            scene = fileName
        else:
            preset = self.getPresetScene(fileName)
            if preset:
                scene = preset["path"]
            else:
                scene = fileName

        if not os.path.exists(scene):
            self.core.popup(
                "The preset scenefile doesn't exist:\n\n%s"
                % scene
            )
            return

        ext = os.path.splitext(scene)[1]
        filePath = self.core.generateScenePath(
            entity,
            step,
            task=category,
            extension=ext,
            comment=comment,
            version=version,
            user=user,
        )

        if location == "local" and self.core.useLocalFiles:
            filePath = self.core.convertPath(filePath, "local")

        if os.path.exists(filePath):
            msg = (
                "Skipped creating a new version from preset.\nThe filepath exists already:\n\n%s"
                % filePath
            )
            self.core.popup(msg)
            return

        if not os.path.exists(os.path.dirname(filePath)):
            try:
                os.makedirs(os.path.dirname(filePath))
            except:
                self.core.popup(
                    "The directory could not be created:\n\n%s"
                    % os.path.dirname(filePath)
                )
                return

        filePath = filePath.replace("\\", "/")

        shutil.copyfile(scene, filePath)
        details = entity.copy()
        details["department"] = step
        details["task"] = category
        details["user"] = user
        details["version"] = version
        details["comment"] = comment
        details["extension"] = ext
        self.core.saveSceneInfo(filePath, details=details)

        self.core.callback(
            name="onSceneFromPresetCreated",
            args=[self, filePath],
        )

        logger.debug("Created scene from preset: %s" % filePath)
        return filePath

    @err_catcher(name=__name__)
    def createPresetScene(self):
        presetDir = os.path.join(self.core.projects.getPipelineFolder(), "PresetScenes")

        newItem = PrismWidgets.CreateItem(
            core=self.core,
            startText=self.core.appPlugin.pluginName.replace(" ", ""),
        )

        self.core.parentWindow(newItem)
        newItem.e_item.setFocus()
        newItem.setWindowTitle("Create preset scene")
        newItem.l_item.setText("Preset name:")
        result = newItem.exec_()

        if result != 1:
            return

        pName = newItem.e_item.text()

        filepath = os.path.join(presetDir, pName)
        filepath = filepath.replace("\\", "/")
        filepath += self.core.appPlugin.getSceneExtension(self)

        self.core.saveScene(filepath=filepath, prismReq=False)
        return filepath

    @err_catcher(name=__name__)
    def getAutobackPath(self, prog, entity=None, department=None, task=None):
        if prog == self.core.appPlugin.pluginName:
            if not hasattr(self.core.appPlugin, "getAutobackPath"):
                return

            autobackpath, fileStr = self.core.appPlugin.getAutobackPath(self)
        else:
            for i in self.core.unloadedAppPlugins.values():
                if i.pluginName == prog:
                    if not hasattr(i, "getAutobackPath"):
                        return

                    autobackpath, fileStr = i.getAutobackPath(self)

        if not autobackpath and entity:
            if entity["type"] == "asset":
                cVersion = self.core.compareVersions(
                    self.core.projectVersion, "v1.2.1.6"
                )
                if cVersion == "lower":
                    autobackpath = self.core.getEntityPath(entity=entity, step=department)
                else:
                    autobackpath = self.core.getEntityPath(
                        entity=entity, step=department, category=task
                    )

            elif entity["type"] == "shot":
                autobackpath = self.core.getEntityPath(
                    entity=entity, step=department, category=task
                )

        return autobackpath, fileStr

    @err_catcher(name=__name__)
    def createVersionFromAutoBackupDlg(
        self, prog, entity, department, task, parent=None
    ):
        parent = parent or self.core.messageParent
        result = self.getAutobackPath(prog, entity, department, task)
        if not result:
            return

        autobackpath, fileStr = result
        autobfile = QFileDialog.getOpenFileName(
            parent, "Select Autoback File", autobackpath, fileStr
        )[0]

        if not autobfile:
            return

        return self.createVersionFromAutoBackup(autobfile, entity, department, task)

    @err_catcher(name=__name__)
    def createVersionFromAutoBackup(self, filepath, entity, department, task):
        version = self.core.entities.getHighestVersion(entity, department, task)
        targetpath = self.core.generateScenePath(
            entity=entity,
            department=department,
            task=task,
            extension=os.path.splitext(filepath)[1],
            version=version
        )

        if self.core.useLocalFiles:
            targetpath = self.core.convertPath(targetpath, "local")

        if os.path.exists(targetpath):
            msg = (
                "Skipped creating a new version from autoback.\nThe filepath exists already:\n\n%s"
                % targetpath
            )
            self.core.popup(msg)
            return

        if not os.path.exists(os.path.dirname(targetpath)):
            try:
                os.makedirs(os.path.dirname(targetpath))
            except:
                self.core.popup("The directory could not be created")
                return

        targetpath = targetpath.replace("\\", "/")
        self.core.copySceneFile(filepath, targetpath)

        details = entity.copy()
        details["department"] = department
        details["task"] = task
        details["extension"] = os.path.splitext(filepath)[1]
        details["comment"] = ""
        details["version"] = version
        self.core.saveSceneInfo(targetpath, details=details)
        logger.debug("Created scene from autoback: %s" % targetpath)
        return targetpath

    @err_catcher(name=__name__)
    def copySceneFile(self, filepath, entity, department, task, location=None):
        version = self.core.entities.getHighestVersion(entity, department, task)
        targetpath = self.core.generateScenePath(
            entity=entity,
            department=department,
            task=task,
            extension=os.path.splitext(filepath)[1],
            version=version,
            location=location
        )

        if location is None:
            if self.core.useLocalFiles:
                targetpath = self.core.convertPath(targetpath, "local")

        if not os.path.exists(os.path.dirname(targetpath)):
            try:
                os.makedirs(os.path.dirname(targetpath))
            except:
                self.core.popup("The directory could not be created")
                return

        targetpath = targetpath.replace("\\", "/")
        self.core.copySceneFile(filepath, targetpath)

        details = entity.copy()
        details["department"] = department
        details["task"] = task
        details["extension"] = os.path.splitext(filepath)[1]
        details["version"] = version
        self.core.saveSceneInfo(targetpath, details=details, replace=True)
        logger.debug("Copied scene: %s" % targetpath)
        return targetpath

    @err_catcher(name=__name__)
    def createVersionFromCurrentScene(self, entity, department, task):
        version = self.core.entities.getHighestVersion(entity, department, task)
        filepath = self.core.generateScenePath(
            entity=entity,
            department=department,
            task=task,
            extension=self.core.appPlugin.getSceneExtension(self),
            version=version
        )

        if self.core.useLocalFiles:
            filepath = self.core.convertPath(filepath, "local")

        if not os.path.exists(os.path.dirname(filepath)):
            try:
                os.makedirs(os.path.dirname(filepath))
            except:
                self.core.popup("The directory could not be created")
                return

        filepath = filepath.replace("\\", "/")
        self.core.startAutosaveTimer(quit=True)

        details = entity.copy()
        details["department"] = department
        details["task"] = task
        details["extension"] = os.path.splitext(filepath)[1]
        details["comment"] = ""
        details["version"] = version
        filepath = self.core.saveScene(filepath=filepath, details=details)
        self.core.sceneOpen()
        if self.core.shouldAutosaveTimerRun():
            self.core.startAutosaveTimer()

        logger.debug("Created scene from current: %s" % filepath)
        return filepath

    @err_catcher(name=__name__)
    def backupScenefile(self, targetFolder, bufferMinutes=5):
        filename = self.core.getCurrentFileName()
        if not filename:
            return

        target = os.path.join(targetFolder, os.path.basename(filename))
        if os.path.exists(target):
            mtime = os.path.getmtime(target)
            if time.time() - mtime < (60 * bufferMinutes):
                return

            base, ext = os.path.splitext(os.path.basename(target))
            backupNum = 1
            while True:
                backup = os.path.join(os.path.dirname(target), "_backup", base + "_" + str(backupNum) + ext)
                if not os.path.exists(backup):
                    break
                else:
                    mtime = os.path.getmtime(backup)
                    if time.time() - mtime < (60 * bufferMinutes):
                        return
                    backupNum += 1
            self.core.copySceneFile(target, backup)

        self.core.copySceneFile(filename, target)
        logger.debug("backed up scenefile: %s" % target)

    @err_catcher(name=__name__)
    def addEntityAction(self, key, types, function, label):
        self.entityActions[key] = {"types": types, "function": function, "label": label}

    @err_catcher(name=__name__)
    def removeEntityAction(self, key):
        if key in self.entityActions:
            del self.entityActions[key]
            return True

    @err_catcher(name=__name__)
    def getAssetActions(self):
        actions = {act: self.entityActions[act] for act in self.entityActions if "asset" in self.entityActions[act]["types"]}
        return actions

    @err_catcher(name=__name__)
    def getShotActions(self):
        actions = {act: self.entityActions[act] for act in self.entityActions if "shot" in self.entityActions[act]["types"]}
        return actions

    @err_catcher(name=__name__)
    def connectEntityDlg(self, entities=None, parent=None):
        self.dlg_connectEntities = ConnectEntitiesDlg(self.core, parent)
        self.dlg_connectEntities.navigate(entities)
        self.dlg_connectEntities.show()

    @err_catcher(name=__name__)
    def getConnectedEntities(self, entity):
        centities = {}
        if not entity:
            return centities

        if entity.get("type") == "asset":
            data = self.core.getConfig(config="assetinfo") or {}
            if "assets" not in data:
                return centities

            if "asset_path" not in entity:
                return centities

            entityName = self.core.entities.getAssetNameFromPath(entity["asset_path"])
            if entityName not in data["assets"]:
                return centities

            centities = data["assets"][entityName].get("connectedEntities", {})

        elif entity.get("type") == "shot" and "sequence" in entity:
            data = self.core.getConfig(config="shotinfo") or {}
            if "shots" not in data:
                return centities

            if entity["sequence"] not in data["shots"]:
                return centities

            if entity["shot"] not in data["shots"][entity["sequence"]]:
                return centities

            centities = data["shots"][entity["sequence"]][entity["shot"]].get("connectedEntities", {})

        return centities

    @err_catcher(name=__name__)
    def setConnectedEntities(self, entities, connectedEntities, add=False, remove=False, setReverse=True):
        assetInfo = None
        shotInfo = None
        for entity in entities:
            if entity["type"] == "asset" and "asset_path" in entity:
                if assetInfo is None:
                    assetInfo = self.core.getConfig(config="assetinfo", allowCache=False) or {}

                if "assets" not in assetInfo:
                    assetInfo["assets"] = {}

                entityName = self.core.entities.getAssetNameFromPath(entity["asset_path"])
                if entityName not in assetInfo["assets"]:
                    assetInfo["assets"][entityName] = {}

                entityInfo = assetInfo["assets"][entityName]

            elif entity["type"] == "shot":
                if shotInfo is None:
                    shotInfo = self.core.getConfig(config="shotinfo", allowCache=False) or {}

                if "shots" not in shotInfo:
                    shotInfo["shots"] = {}

                if entity["sequence"] not in shotInfo["shots"]:
                    shotInfo["shots"][entity["sequence"]] = {}

                if entity["shot"] not in shotInfo["shots"][entity["sequence"]]:
                    shotInfo["shots"][entity["sequence"]][entity["shot"]] = {}

                entityInfo = shotInfo["shots"][entity["sequence"]][entity["shot"]]

            curEntities = entityInfo.get("connectedEntities", [])
            centities = []
            if add or remove:
                centities = list(curEntities)

            if remove:
                newEntities = []
                toRemoveNames = [self.getEntityName(e) for e in connectedEntities]
                for centity in centities:
                    if self.getEntityName(centity) not in toRemoveNames:
                        newEntities.append(centity)

                centities = [self.getCleanEntity(e) for e in newEntities]
            else:
                centities += [self.getCleanEntity(e) for e in connectedEntities]

            if not remove:
                centityNames = [self.getEntityName(e) for e in centities]
                removed = []
                for curEntity in curEntities:
                    name = self.getEntityName(curEntity)
                    if name not in centityNames:
                        removed.append(curEntity)

                if removed:
                    self.setConnectedEntities(removed, [entity], remove=True, setReverse=False)

            entityInfo["connectedEntities"] = centities

        if setReverse:
            self.setConnectedEntities(connectedEntities, entities, add=True, setReverse=False)
        
        if assetInfo:
            self.core.setConfig(data=assetInfo, config="assetinfo", updateNestedData=False)

        if shotInfo:
            self.core.setConfig(data=shotInfo, config="shotinfo", updateNestedData=False)

        return True

    @err_catcher(name=__name__)
    def getCleanEntity(self, entity):
        data = {}
        data["type"] = entity.get("type")
        if entity.get("type") == "asset":
            data["asset_path"] = entity.get("asset_path")
        elif entity.get("type") == "shot":
            data["shot"] = entity.get("shot")
            data["sequence"] = entity.get("sequence")

        return data

    @err_catcher(name=__name__)
    def getUniqueEntities(self, entities):
        data = {}
        for entity in entities:
            uid = self.getEntityName(entity)
            if uid not in data:
                data[uid] = entity

        uentities = list(data.values())
        return uentities

    @err_catcher(name=__name__)
    def getEntityName(self, entity):
        if not entity:
            return

        name = None
        if entity.get("type") == "asset":
            name = entity.get("asset_path", "").replace("\\", "/")
        elif entity.get("type") == "shot":
            name = self.getShotName(entity)

        return name


class EntityDlg(QDialog):

    entitySelected = Signal(object)

    def __init__(self, origin, parent=None):
        super(EntityDlg, self).__init__()
        self.origin = origin
        self.parentDlg = parent
        self.core = self.origin.core
        self.setupUi()

    @err_catcher(name=__name__)
    def setupUi(self):
        title = "Select entity"

        self.setWindowTitle(title)
        self.core.parentWindow(self, parent=self.parentDlg)

        import EntityWidget
        self.w_entities = EntityWidget.EntityWidget(core=self.core, refresh=True)
        self.w_entities.getPage("Assets").tw_tree.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.w_entities.getPage("Shots").tw_tree.itemDoubleClicked.connect(self.itemDoubleClicked)
        self.w_entities.getPage("Assets").setSearchVisible(False)
        self.w_entities.getPage("Shots").setSearchVisible(False)

        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Select", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Close", QDialogButtonBox.RejectRole)

        self.bb_main.clicked.connect(self.buttonClicked)

        self.lo_main.addWidget(self.w_entities)
        self.lo_main.addWidget(self.bb_main)

    @err_catcher(name=__name__)
    def itemDoubleClicked(self, item, column):
        self.buttonClicked("select")

    @err_catcher(name=__name__)
    def buttonClicked(self, button):
        if button == "select" or button.text() == "Select":
            entities = self.w_entities.getCurrentData()
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

            self.entitySelected.emit(validEntities[0])

        self.close()

    @err_catcher(name=__name__)
    def sizeHint(self):
        return QSize(400, 400)


class ConnectEntitiesDlg(QDialog):
    def __init__(self, core, parent=None):
        super(ConnectEntitiesDlg, self).__init__()
        self.parentDlg = parent
        self.core = core

        self.setupUi()

    @err_catcher(name=__name__)
    def setupUi(self):
        title = "Connect Entities"
        self.setWindowTitle(title)
        self.core.parentWindow(self, parent=self.parentDlg)

        self.w_entitiesParent = QWidget()
        self.lo_entitiesParent = QHBoxLayout()
        self.w_entitiesParent.setLayout(self.lo_entitiesParent)

        self.w_selEntities = QWidget()
        self.w_selEntities.setObjectName("w_selEntities")
        self.gb_connectedEntities = QGroupBox("Connected Entities")
        self.gb_connectedEntities.setObjectName("gb_connectedEntities")

        self.lo_entitiesParent.addWidget(self.w_selEntities)
        self.lo_entitiesParent.addWidget(self.gb_connectedEntities)

        import EntityWidget
        self.w_entities = EntityWidget.EntityWidget(core=self.core, refresh=True)
        self.w_connectedEnities = EntityWidget.EntityWidget(core=self.core, refresh=False)
        self.w_connectedEnities.getPage("Assets").useCounter = True
        self.w_connectedEnities.refreshEntities()
        self.w_connectedEnities.tb_entities.setVisible(False)
        self.w_entities.tabChanged.connect(self.tabChanged)

        self.w_entities.getPage("Assets").itemChanged.connect(self.onSelectedEntityChanged)
        self.w_entities.getPage("Shots").itemChanged.connect(self.onSelectedEntityChanged)
        self.w_entities.getPage("Assets").setSearchVisible(False)
        self.w_entities.getPage("Shots").setSearchVisible(False)

        self.w_connectedEnities.getPage("Assets").itemChanged.connect(self.refreshConnectedEntityInfo)
        self.w_connectedEnities.getPage("Shots").itemChanged.connect(self.refreshConnectedEntityInfo)
        self.w_connectedEnities.getPage("Assets").setSearchVisible(False)
        self.w_connectedEnities.getPage("Shots").setSearchVisible(False)

        self.l_info = QLabel()
        self.l_connectedInfo = QLabel()

        self.lo_assets = QVBoxLayout()
        self.w_selEntities.setLayout(self.lo_assets)
        self.lo_assets.addWidget(self.w_entities)
        self.lo_assets.addWidget(self.l_info)

        self.lo_shots = QVBoxLayout()
        self.gb_connectedEntities.setLayout(self.lo_shots)
        self.lo_shots.addWidget(self.w_connectedEnities)
        self.lo_shots.addWidget(self.l_connectedInfo)

        self.refreshEntityInfo()
        self.refreshConnectedEntityInfo()

        self.tabChanged()

        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Apply", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Close", QDialogButtonBox.RejectRole)

        self.bb_main.accepted.connect(self.onAccepted)
        self.bb_main.rejected.connect(self.reject)

        self.lo_main.addWidget(self.w_entitiesParent)
        self.lo_main.addWidget(self.bb_main)

    @err_catcher(name=__name__)
    def sizeHint(self):
        return QSize(800, 700)

    @err_catcher(name=__name__)
    def onAccepted(self):
        entities = self.w_entities.getCurrentData(returnOne=False)
        entities = [e for e in entities if e["type"] in ["asset", "shot"] and ("asset_path" in e or "shot" in e)]
        if not entities:
            msg = "No valid entity selected."
            self.core.popup(msg)
            return

        page = self.w_connectedEnities.getCurrentPage()
        if page.useCounter:
            connectedEntities = []
            items = page.tw_tree.selectedItems()
            for item in items:
                entity = page.getDataFromItem(item)
                if entity["type"] in ["asset", "shot"] and (entity.get("asset_path") or entity.get("shot")):
                    for idx in range(page.getCount(item)):
                        connectedEntities.append(entity)
        else:
            connectedEntities = self.w_connectedEnities.getCurrentData(returnOne=False)
            connectedEntities = [e for e in connectedEntities if (e["type"] in ["asset", "shot"] and (e.get("asset_path") or e.get("shot")))]

        result = self.core.entities.setConnectedEntities(entities, connectedEntities)
        if not result:
            return

        entityNames = [self.core.entities.getEntityName(e) for e in entities]
        connectedNames = [self.core.entities.getEntityName(e) for e in connectedEntities] or ["-"]
        msg = "Entity-Connections were set successfully:\n\n%s\n\nto:\n\n%s" % ("\n".join(entityNames), "\n".join(connectedNames))
        self.core.popup(msg, severity="info", parent=self)

    @err_catcher(name=__name__)
    def tabChanged(self):
        self.w_connectedEnities.tb_entities.setCurrentIndex(not bool(self.w_entities.tb_entities.currentIndex()))
        self.gb_connectedEntities.setTitle("Connected %s" % self.w_connectedEnities.getCurrentPageName())
        self.selectConnectedEntities()
        self.refreshEntityInfo()
        self.refreshConnectedEntityInfo()

    @err_catcher(name=__name__)
    def onSelectedEntityChanged(self, items=None):
        self.refreshEntityInfo(items)
        self.selectConnectedEntities()

    @err_catcher(name=__name__)
    def selectConnectedEntities(self):
        entities = self.w_entities.getCurrentData(returnOne=False)
        connected = []
        for entity in entities:
            connected += self.core.entities.getConnectedEntities(entity)

        self.w_connectedEnities.navigate(connected, clear=True)

    @err_catcher(name=__name__)
    def refreshEntities(self):
        self.w_assets.refreshEntities()
        self.w_shots.refreshEntities()

    @err_catcher(name=__name__)
    def refreshEntityInfo(self, items=None):
        page = self.w_entities.getCurrentPage()
        if items is None:
            items = page.tw_tree.selectedItems()
        elif not isinstance(items, list):
            items = [items]

        if page.useCounter:
            entities = []
            for item in items:
                entity = page.getDataFromItem(item)
                if entity["type"] in ["asset", "shot"]:
                    for idx in range(page.getCount(item)):
                        entities.append(entity)

        else:
            entities = [page.getDataFromItem(item) for item in items]
            entities = [entity for entity in entities if entity["type"] in ["asset", "shot"]]

        if page.entityType == "asset":
            if len(entities) == 1:
                text = "%s Asset selected" % len(entities)
            else:
                text = "%s Assets selected" % len(entities)
        else:
            if len(entities) == 1:
                text = "%s Shot selected" % len(entities)
            else:
                text = "%s Shots selected" % len(entities)

        self.l_info.setText(text)

    @err_catcher(name=__name__)
    def refreshConnectedEntityInfo(self, items=None):
        page = self.w_connectedEnities.getCurrentPage()
        if items is None:
            items = page.tw_tree.selectedItems()
        elif not isinstance(items, list):
            items = [items]

        if page.useCounter:
            entities = []
            for item in items:
                entity = page.getDataFromItem(item)
                if entity["type"] in ["asset", "shot"]:
                    for idx in range(page.getCount(item)):
                        entities.append(entity)

        else:
            entities = [page.getDataFromItem(item) for item in items]
            entities = [entity for entity in entities if entity["type"] in ["asset", "shot"]]

        if page.entityType == "asset":
            if len(entities) == 1:
                text = "%s Asset selected" % len(entities)
            else:
                text = "%s Assets selected" % len(entities)
        else:
            if len(entities) == 1:
                text = "%s Shot selected" % len(entities)
            else:
                text = "%s Shots selected" % len(entities)

        self.l_connectedInfo.setText(text)

    @err_catcher(name=__name__)
    def navigate(self, entities):
        self.w_entities.navigate(entities)
