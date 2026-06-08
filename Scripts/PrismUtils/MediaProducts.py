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
import platform
import shutil
import glob
import errno
import time
import copy

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher


logger = logging.getLogger(__name__)


def _legacy_dir_exists(path):
    """
    Returns True only when the directory exists AND its basename matches
    with exact case.  Necessary on Windows where os.path.isdir() is
    case-insensitive — without this, the legacy shim would mistake the new
    lowercase 'renders/'/'playblasts/' folders for the old capital-letter
    'Renders/'/'Playblasts/' folders and treat version folders as identifiers.
    """
    parent, name = os.path.split(path)
    try:
        return name in os.listdir(parent)
    except OSError:
        return False


class MediaProducts(object):
    def __init__(self, core):
        self.core = core

    @err_catcher(name=__name__)
    def getSimplifiedMediaBasePath(self, entity, projectPath, mediaType, location=None):
        root = self.core.paths.getSimplifiedOutputRoot(entity, projectPath=projectPath, location=location)
        if not root:
            return ""

        # IMPORTANT: When adding a new flat-mode media key, update routing here
        # AND _flatKeys in Projects.validateFolderStructure()
        # AND _flatKeys in ProjectSettings.validateFolderWidget()
        if mediaType == "playblasts":
            return os.path.join(root, "playblasts")
        elif mediaType == "externalMedia":
            return os.path.join(root, "external")
        else:
            # Both "3drenders" and "2drenders" share the same renders/ folder.
            # They are distinguished at the version level by the presence of
            # AOV subdirectories (3D) vs. files directly in the version folder (2D).
            return os.path.join(root, "renders")

    @err_catcher(name=__name__)
    def getSimplifiedMediaData(self, path, mediaType=None, isVersionFolder=False):
        entityData = self.core.paths.getSimplifiedEntityDataFromPath(path)
        if not entityData:
            return {}

        mediaTypes = [mediaType] if mediaType else ["3drenders", "2drenders", "playblasts", "externalMedia"]
        globalPath = os.path.normpath(self.core.convertPath(path, "global"))
        for mtype in mediaTypes:
            basePath = os.path.normpath(
                self.getSimplifiedMediaBasePath(entityData, entityData["project_path"], mtype)
            )
            if not basePath or not (
                globalPath.startswith(basePath + os.sep) or globalPath == basePath
            ):
                continue

            relPath = os.path.relpath(globalPath, basePath)
            parts = relPath.split(os.sep)
            if os.path.splitext(parts[-1])[1]:
                if len(parts) < 2:
                    continue

                identifier = "media"
                version = parts[0]
                filename = parts[-1]
                _, extension = self.core.paths.splitext(filename)
            else:
                if len(parts) < 1:
                    continue

                identifier = "media"
                version = parts[0]
                extension = ""

            data = entityData.copy()
            data["identifier"] = identifier
            data["version"] = version
            data["type"] = entityData["type"]
            data["project_path"] = entityData["project_path"]
            data["mediaType"] = mtype
            if extension:
                data["extension"] = extension

            if "_" in data.get("version", "") and data["version"].count("_") == 1:
                data["version"], data["wedge"] = data["version"].split("_")

            return data

        return {}

    @err_catcher(name=__name__)
    def createExternalMedia(self, filepath, entity, identifier, version, action="copy", location="global"):
        if entity["type"] not in ("asset", "shot"):
            self.core.popup("Invalid entity is selected. Select an asset or a shot and try again.")
            return

        basePath = self.core.paths.getRenderProductBasePaths()[location]

        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            versionBase = self.getSimplifiedMediaBasePath(entity, basePath, "externalMedia", location=location)
            folderpath = os.path.join(versionBase, version)
        else:
            context = entity.copy()
            context["mediaType"] = "externalMedia"
            context["identifier"] = identifier
            context["version"] = version
            context["aov"] = "rgb"
            if "comment" not in context:
                context["comment"] = ""
            context["project_path"] = basePath

            if entity["type"] == "asset":
                key = "renderFilesAssets"
            else:
                key = "renderFilesShots"

            path = self.core.projects.getResolvedProjectStructurePath(key, context=context)
            folderpath = os.path.dirname(path)

        if not os.path.exists(folderpath):
            os.makedirs(folderpath)

        files = filepath.split(os.pathsep)
        for file in files:
            try:
                if action == "copy":
                    if os.path.isdir(file):
                        os.rmdir(folderpath)
                        shutil.copytree(file, folderpath)
                    else:
                        shutil.copy2(file, folderpath)
                elif action == "move":
                    shutil.move(file, folderpath)
                elif action == "link":
                    redirectFile = os.path.join(folderpath, "REDIRECT.txt")
                    with open(redirectFile, "w") as rfile:
                        rfile.write(file)

            except Exception as e:
                msg = "Failed to add external media:\n\n%s" % e
                self.core.popup(msg)
                continue

        return folderpath

    @err_catcher(name=__name__)
    def getExternalPathFromVersion(self, version):
        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            folderpath = version.get("path", "")
        else:
            if version["type"] == "asset":
                key = "renderFilesAssets"
            elif version["type"] == "shot":
                key = "renderFilesShots"

            context = version.copy()
            context["mediaType"] = "externalMedia"
            context["aov"] = "rgb"

            filepath = self.core.projects.getResolvedProjectStructurePath(
                key, context=context
            )
            folderpath = os.path.dirname(filepath)

        redirectFile = os.path.join(folderpath, "REDIRECT.txt")
        curLoc = ""
        if os.path.exists(redirectFile):
            with open(redirectFile, "r") as rdFile:
                curLoc = rdFile.read()

        return curLoc

    @err_catcher(name=__name__)
    def getDisplayNameForIdentifier(self, identifier, mediaType):
        display = identifier
        if mediaType == "2drenders":
            display += " (2d)"
        elif mediaType == "playblasts":
            display += " (playblast)"
        elif mediaType == "externalMedia":
            display += " (external)"

        return display

    @err_catcher(name=__name__)
    def getIdentifiersByType(self, entity, locations=None):
        locationData = self.core.paths.getRenderProductBasePaths()
        searchLocations = []
        for locData in locationData:
            if not locations or locData in locations or "all" in locations:
                searchLocations.append(locData)

        mediaTypes = {"3d": [], "2d": [], "playblast": [], "external": []}
        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            for loc in searchLocations:
                baseProject = locationData[loc]
                # Flat structure: one entry per physical folder, named after
                # the folder.  3D and 2D renders share the same "renders/"
                # folder so they appear as a single "renders" identifier.
                # IMPORTANT: the middle value (mediaTypeLabel) must match the
                # keys MediaBrowser iterates: "3d", "2d", "playblast", "external".
                folderMap = [
                    ("renders",    "3d",         "3drenders"),
                    ("playblasts", "playblast",  "playblasts"),
                    ("external",   "external",   "externalMedia"),
                ]
                # "renders" and "playblasts" are permanent fixed slots —
                # always visible even before the first render is submitted.
                # "external" only appears when content already exists on disk.
                ALWAYS_SHOW = {"renders", "playblasts"}

                for idfName, mediaTypeLabel, mediaKey in folderMap:
                    basePath = self.getSimplifiedMediaBasePath(entity, baseProject, mediaKey, location=loc)

                    if idfName not in ALWAYS_SHOW:
                        # Dynamic entry: only show when content exists.
                        if not os.path.isdir(basePath):
                            continue
                        hasVersions = any(
                            os.path.isdir(os.path.join(basePath, e))
                            for e in os.listdir(basePath)
                        )
                        if not hasVersions:
                            continue

                    data = entity.copy()
                    data["project_path"] = baseProject
                    data["identifier"] = idfName
                    data["displayName"] = idfName
                    data["path"] = basePath
                    data["location"] = loc
                    data["mediaType"] = mediaKey
                    mediaTypes[mediaTypeLabel].append(data)

                # ----------------------------------------------------------
                # Legacy shim (read-only): surface pre-migration content
                # stored at the old capital-letter paths.
                # Capital "Renders"/"Playblasts" are case-distinct from the
                # new lowercase "renders"/"playblasts", so there is no
                # overlap between old and new content.
                # ----------------------------------------------------------
                entityRoot = self.core.paths.getSimplifiedOutputRoot(entity, projectPath=baseProject)
                if entityRoot:
                    legacyRenderRoot = os.path.join(entityRoot, "Renders")
                    if _legacy_dir_exists(legacyRenderRoot):
                        legacyMap = {
                            "3d":       ("3drenders",    os.path.join(legacyRenderRoot, "3dRender")),
                            "2d":       ("2drenders",    os.path.join(legacyRenderRoot, "2dRender")),
                            "external": ("externalMedia", os.path.join(legacyRenderRoot, "external")),
                        }
                        for lbl, (mKey, legacyBase) in legacyMap.items():
                            if not os.path.isdir(legacyBase):
                                continue
                            for idfName in sorted(os.listdir(legacyBase)):
                                idfPath = os.path.join(legacyBase, idfName)
                                if not os.path.isdir(idfPath):
                                    continue
                                d = entity.copy()
                                d["project_path"] = baseProject
                                d["identifier"] = idfName
                                d["displayName"] = (
                                    idfName if lbl == "3d"
                                    else "%s (%s)" % (idfName, lbl)
                                )
                                d["path"] = idfPath
                                d["location"] = loc
                                d["mediaType"] = mKey
                                d["legacy"] = True
                                mediaTypes[lbl].append(d)

                    legacyPbRoot = os.path.join(entityRoot, "Playblasts")
                    if _legacy_dir_exists(legacyPbRoot):
                        for idfName in sorted(os.listdir(legacyPbRoot)):
                            idfPath = os.path.join(legacyPbRoot, idfName)
                            if not os.path.isdir(idfPath):
                                continue
                            d = entity.copy()
                            d["project_path"] = baseProject
                            d["identifier"] = idfName
                            d["displayName"] = "%s (playblast)" % idfName
                            d["path"] = idfPath
                            d["location"] = loc
                            d["mediaType"] = "playblasts"
                            d["legacy"] = True
                            mediaTypes["playblast"].append(d)

                # ----------------------------------------------------------
                # Legacy shim for pre-flat-migration content in rendering
                # locations. Before the flat structure was introduced, renders
                # in custom locations were stored at:
                #   <RenderingRoot>/Output/<stage>/<entity>/renders/
                # The flat scanner above looks in <RenderingRoot>/<entity>/renders/
                # and will miss this old content.  Surface it as legacy_flat
                # entries so the Media Browser continues to show existing renders.
                # ----------------------------------------------------------
                if self.core.paths._isFlatRenderLocation(loc):
                    oldEntityRoot = self.core.paths.getSimplifiedOutputRoot(entity, projectPath=baseProject)
                    if oldEntityRoot and os.path.isdir(oldEntityRoot):
                        for idfName, mediaTypeLabel, mediaKey in folderMap:
                            suffix = "renders" if "render" in mediaKey else (
                                "playblasts" if mediaKey == "playblasts" else "external"
                            )
                            oldBasePath = os.path.join(oldEntityRoot, suffix)
                            if not os.path.isdir(oldBasePath):
                                continue
                            hasVersions = any(
                                os.path.isdir(os.path.join(oldBasePath, e))
                                for e in os.listdir(oldBasePath)
                            )
                            if not hasVersions:
                                continue
                            d = entity.copy()
                            d["project_path"] = baseProject
                            d["identifier"] = idfName
                            d["displayName"] = idfName
                            d["path"] = oldBasePath
                            d["location"] = loc
                            d["mediaType"] = mediaKey
                            d["legacy_flat"] = True
                            mediaTypes[mediaTypeLabel].append(d)

        if not self.core.paths.isSimplifiedArtistWorkflowEnabled():
            for loc in searchLocations:
                for mtype in mediaTypes:
                    context = entity.copy()
                    context["project_path"] = locationData[loc]
                    if mtype == "3d":
                        key = "3drenders"
                        context["mediaType"] = key
                    elif mtype == "2d":
                        key = "2drenders"
                        context["mediaType"] = key
                    elif mtype == "playblast":
                        key = "playblasts"
                        context["mediaType"] = key
                    elif mtype == "external":
                        key = "externalMedia"
                        context["mediaType"] = key

                    template = self.core.projects.getResolvedProjectStructurePath(
                        key, context=context
                    )
                    productData = self.core.projects.getMatchingPaths(template)
                    validData = []
                    for data in productData:
                        if "." in data["identifier"]:
                            if os.path.isfile(data["path"]):
                                continue

                        data["displayName"] = data["identifier"]
                        data.update(context)
                        if mtype != "3d":
                            data["displayName"] += " (%s)" % mtype

                        validData.append(data)

                    mediaTypes[mtype] += validData

        return mediaTypes

    @err_catcher(name=__name__)
    def getIdentifierNames(self, entity):
        names = []
        idfs = self.getIdentifiersByType(entity)
        for mtype in idfs:
            for idf in idfs[mtype]:
                names.append(idf["displayName"])

        return names

    @err_catcher(name=__name__)
    def getIdentifierPathFromEntity(self, entity):
        key = "3drenders"
        context = entity.copy()
        template = self.core.projects.getResolvedProjectStructurePath(
            key, context=context
        )
        path = os.path.dirname(template)
        return path

    @err_catcher(name=__name__)
    def getVersionPathFromIdentifier(self, entity):
        key = "renderVersions"
        context = entity.copy()
        template = self.core.projects.getResolvedProjectStructurePath(
            key, context=context
        )
        path = os.path.dirname(template)
        return path

    @err_catcher(name=__name__)
    def getVersionsFromIdentifier(self, identifier, locations=None):
        if not identifier:
            return

        locationData = self.core.paths.getRenderProductBasePaths()
        searchLocations = []
        for locData in locationData:
            if not locations or locData in locations or "all" in locations:
                searchLocations.append(locData)

        versions = []
        for loc in searchLocations:
            context = identifier.copy()
            if "version" in context:
                del context["version"]

            if "paths" in context:
                del context["paths"]

            context["project_path"] = locationData[loc]
            locVersions = self.getVersionsFromContext(context)
            for locVersion in locVersions:
                locVersion["paths"] = [locVersion.get("path")]
                for version in versions:
                    if version.get("version") == locVersion.get("version"):
                        version["paths"].append(locVersion.get("path"))
                        break
                else:
                    versions.append(locVersion)
                    continue

        return versions

    @err_catcher(name=__name__)
    def getVersionStackContextFromPath(self, filepath, mediaType=None):
        context = self.core.paths.getRenderProductData(filepath, mediaType=mediaType)

        if mediaType:
            context["mediaType"] = mediaType

        if "asset" in context:
            context["asset"] = os.path.basename(context["asset_path"])

        if "version" in context:
            del context["version"]
        if "comment" in context:
            del context["comment"]
        if "user" in context:
            del context["user"]

        return context

    @err_catcher(name=__name__)
    def getVersionsFromSameVersionStack(self, path, mediaType=None):
        context = self.getVersionStackContextFromPath(path, mediaType=mediaType)
        if not context:
            return []

        versionData = self.getVersionsFromContext(context)
        return versionData

    @err_catcher(name=__name__)
    def getVersion(self, entity, identifier, mediaType=None, version=None):
        mediaType = mediaType or "3drenders"
        version = version or "latest"
        idf = entity.copy()
        idf["identifier"] = identifier
        idf["mediaType"] = mediaType
        if version == "latest":
            versionData = self.getLatestVersionFromIdentifier(idf)
        else:
            versions = self.getVersionsFromIdentifier(idf)
            versionData = None
            for ver in versions:
                if ver["version"] == version:
                    versionData = ver

        return versionData

    @err_catcher(name=__name__)
    def getFileFromVersion(self, version, aov=None, findExisting=False):
        if aov:
            version["aov"] = aov

        file = self.getFilePatternFromVersion(version)
        if findExisting:
            filepaths = self.core.media.getFilesFromSequence(file)
            if not filepaths:
                sources = self.core.media.getImgSources(os.path.dirname(file))
                if sources:
                    file = sources[0]
                else:
                    return

        return file        

    @err_catcher(name=__name__)
    def getVersionsFromContext(self, context, keys=None, locations=None):
        locationData = self.core.paths.getRenderProductBasePaths()
        searchLocations = []
        for locData in locationData:
            if not locations or locData in locations or "all" in locations:
                searchLocations.append(locData)

        if context.get("mediaType") == "playblasts":
            key = "playblastVersions"
        else:
            key = "renderVersions"

        versions = []
        if self.core.paths.isSimplifiedArtistWorkflowEnabled() and context.get("identifier"):
            for loc in searchLocations:
                ctx = context.copy()
                ctx["project_path"] = locationData[loc]
                basePath = self.getSimplifiedMediaBasePath(
                    ctx, ctx["project_path"], ctx.get("mediaType") or "3drenders",
                    location=loc,
                )
                versionBase = basePath
                if not os.path.isdir(versionBase):
                    continue

                for versionName in os.listdir(versionBase):
                    versionPath = os.path.join(versionBase, versionName)
                    if not os.path.isdir(versionPath):
                        continue

                    c = self.getDeepCopy(context)
                    c["project_path"] = ctx["project_path"]
                    c["version"] = versionName
                    c["path"] = versionPath
                    c["paths"] = [versionPath]
                    c["locations"] = {loc: versionPath}
                    if "_" in versionName and versionName.count("_") == 1:
                        c["version"], c["wedge"] = versionName.split("_")

                    if self.core.products.getIntVersionFromVersionName(c["version"]) is None and c["version"] != "master" and os.getenv("PRISM_SHOW_INVALID_VERSION_NAMES", "0") == "0":
                        continue

                    for version in versions:
                        if version.get("version") == c.get("version"):
                            version["paths"].append(c.get("path"))
                            version["locations"].update(c.get("locations"))
                            break
                    else:
                        versions.append(c)

            # ------------------------------------------------------------------
            # Legacy shim: surface pre-migration versions stored at
            # <entity>/Renders/3dRender/<identifier>/v0001/ (capital letters).
            # Fires only when context["legacy"] is True, which is set by the
            # legacy shim in getIdentifiersByType when the identifier was
            # discovered under the old capital-letter hierarchy.
            # ------------------------------------------------------------------
            if context.get("legacy"):
                idfPath = context.get("path", "")
                if idfPath and os.path.isdir(idfPath):
                    for versionName in sorted(os.listdir(idfPath)):
                        versionPath = os.path.join(idfPath, versionName)
                        if not os.path.isdir(versionPath):
                            continue
                        if (
                            self.core.products.getIntVersionFromVersionName(versionName) is None
                            and versionName != "master"
                            and os.getenv("PRISM_SHOW_INVALID_VERSION_NAMES", "0") == "0"
                        ):
                            continue
                        c = self.getDeepCopy(context)
                        c["version"] = versionName
                        c["path"] = versionPath
                        c["paths"] = [versionPath]
                        c["locations"] = {loc: versionPath}
                        c["legacy"] = True
                        for version in versions:
                            if version.get("version") == c.get("version"):
                                version["paths"].append(c.get("path"))
                                version["locations"].update(c.get("locations"))
                                break
                        else:
                            versions.append(c)

            # ------------------------------------------------------------------
            # Legacy shim for pre-flat-migration content in rendering locations.
            # Fires when the identifier was discovered under the old
            # Output/<stage>/<entity> hierarchy inside a flat rendering location.
            # context["path"] already points to the old base folder.
            # ------------------------------------------------------------------
            if context.get("legacy_flat"):
                idfPath = context.get("path", "")
                idfLoc = context.get("location", "global")
                if idfPath and os.path.isdir(idfPath):
                    for versionName in sorted(os.listdir(idfPath)):
                        versionPath = os.path.join(idfPath, versionName)
                        if not os.path.isdir(versionPath):
                            continue
                        if (
                            self.core.products.getIntVersionFromVersionName(versionName) is None
                            and versionName != "master"
                            and os.getenv("PRISM_SHOW_INVALID_VERSION_NAMES", "0") == "0"
                        ):
                            continue
                        c = self.getDeepCopy(context)
                        c["version"] = versionName
                        c["path"] = versionPath
                        c["paths"] = [versionPath]
                        c["locations"] = {idfLoc: versionPath}
                        c["legacy_flat"] = True
                        for version in versions:
                            if version.get("version") == c.get("version"):
                                version["paths"].append(c.get("path"))
                                version["locations"].update(c.get("locations"))
                                break
                        else:
                            versions.append(c)

        if not self.core.paths.isSimplifiedArtistWorkflowEnabled():
            for loc in searchLocations:
                ctx = context.copy()
                ctx["project_path"] = locationData[loc]
                templates = self.core.projects.getResolvedProjectStructurePaths(
                    key, context=ctx
                )
                versionData = []
                for template in templates:
                    versionData += self.core.projects.getMatchingPaths(template)

                for data in versionData:
                    c = self.getDeepCopy(context)
                    c.update(data)
                    if self.core.products.getIntVersionFromVersionName(c["version"]) is None and c["version"] != "master" and os.getenv("PRISM_SHOW_INVALID_VERSION_NAMES", "0") == "0":
                        continue

                    c["paths"] = [data.get("path")]
                    c["locations"] = {loc: data.get("path", "")}

                    for version in versions:
                        if version.get("version") == c.get("version"):
                            version["paths"].append(c.get("path"))
                            version["locations"].update(c.get("locations"))
                            break
                    else:
                        versions.append(c)
                        continue

        return versions

    @err_catcher(name=__name__)
    def isPicklable(self, value):
        import pickle
        try:
            pickle.dumps(value)
            return True
        except (pickle.PicklingError, TypeError):
            return False

    @err_catcher(name=__name__)
    def getDeepCopy(self, context):
        if not isinstance(context, dict):
            return context

        try:
            newDict = copy.deepcopy(context)
        except:
            newDict = {}
            for key, value in context.items():
                if self.isPicklable(value):
                    newDict[key] = self.getDeepCopy(value)
                else:
                    print(f"Warning: Ignoring unpicklable value for key '{key}'")

        return newDict

    @err_catcher(name=__name__)
    def getAovPathFromVersion(self, version):
        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            # In the new structure the version folder IS the AOV parent.
            # The caller appends the specific AOV name on top of this.
            return version.get("path", "")

        key = "aovs"
        context = version.copy()
        template = self.core.projects.getResolvedProjectStructurePath(
            key, context=context
        )
        path = os.path.dirname(template)
        return path

    @err_catcher(name=__name__)
    def getAOVsFromVersion(self, version):
        if version.get("mediaType") in ("playblasts", "externalMedia"):
            return []

        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            # AOVs are direct subdirectories of the version folder:
            #   <entity>/renders/<version>/<aov>/
            # Iterate ALL known locations so network paths (e.g. "Rendering")
            # are also scanned.  Deduplicate AOV names across locations.
            locationPaths = version.get("locations") or {}
            if not locationPaths and version.get("path"):
                locationPaths = {"_single": version["path"]}

            seen = set()
            aovs = []
            for locPath in locationPaths.values():
                if not locPath or not os.path.isdir(locPath):
                    continue
                for entry in sorted(os.listdir(locPath)):
                    aovPath = os.path.join(locPath, entry)
                    if not os.path.isdir(aovPath) or entry in seen:
                        continue
                    seen.add(entry)
                    d = version.copy()
                    d["aov"] = entry
                    d["path"] = aovPath
                    aovs.append(d)
            return aovs

        key = "aovs"

        aovData = []
        if version.get("locations"):
            locations = self.core.paths.getRenderProductBasePaths()
            for loc in version["locations"]:
                ctx = version.copy()
                if loc not in locations:
                    continue

                ctx["project_path"] = locations[loc]
                template = self.core.projects.getResolvedProjectStructurePath(
                    key, context=ctx
                )
                aovData += self.core.projects.getMatchingPaths(template)

        else:
            template = self.core.projects.getResolvedProjectStructurePath(
                key, context=version
            )
            aovData = self.core.projects.getMatchingPaths(template)

        aovs = []
        for data in aovData:
            if not os.path.isdir(data["path"]):
                continue

            if "aov" not in data:
                continue

            d = version.copy()
            d.update(data)
            aovs.append(d)
        return aovs

    @err_catcher(name=__name__)
    def getFilesFromContext(self, context):
        if context.get("mediaType") == "playblasts":
            if context["type"] == "asset":
                key = "playblastFilesAssets"
            elif context["type"] == "shot":
                key = "playblastFilesShots"
        else:
            if context.get("mediaType") == "3drenders" and "aov" not in context:
                return []

            if context.get("type", None) == "asset":
                key = "renderFilesAssets"
            elif context.get("type", None) == "shot":
                key = "renderFilesShots"
            else:
                return []

        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            # Derive the file folder directly from the version path.
            # For 3D renders, files live inside an AOV subfolder.
            # For all other types, files live directly in the version folder.
            mediaType = context.get("mediaType", "3drenders")
            if context.get("locations"):
                versionPaths = list(context["locations"].values())
            elif context.get("path"):
                versionPaths = [context["path"]]
            else:
                return []

            folders = []
            for vp in versionPaths:
                if mediaType == "3drenders":
                    folders.append(os.path.join(vp, context["aov"]))
                else:
                    folders.append(vp)
        else:
            folders = []
            if context.get("locations"):
                locations = self.core.paths.getRenderProductBasePaths()
                for loc in context["locations"]:
                    if loc not in locations:
                        continue

                    ctx = context.copy()
                    ctx["project_path"] = locations[loc]
                    template = self.core.projects.getResolvedProjectStructurePath(
                        key, context=ctx
                    )
                    folders.append(os.path.dirname(template))

            else:
                template = self.core.projects.getResolvedProjectStructurePath(
                    key, context=context
                )
                folders = [os.path.dirname(template)]

        filepaths = []
        for folder in folders:
            if not os.path.isdir(folder):
                logger.warning("folder doesn't exist: %s" % folder)
                continue

            if context.get("redirect"):
                base, ext = os.path.splitext(context["redirect"])
                if ext:
                    globPath = context["redirect"].replace("#", "?")
                    files = glob.glob(globPath)
                else:
                    if context.get("source"):
                        globPath = os.path.join(context["redirect"], context["source"].replace("#", "?"))
                        files = glob.glob(globPath)
                    else:
                        for rdroot, rdfolders, rdfiles in os.walk(context["redirect"]):
                            break

                        files = [os.path.join(rdroot, rdf) for rdf in rdfiles]

            elif context.get("source"):
                globPath = os.path.join(glob.escape(folder), context["source"].replace("#", "?"))
                files = glob.glob(globPath)
            else:
                files = []
                for root, folders, files in os.walk(folder):
                    break

            for file in files:
                filepath = os.path.join(folder, file)
                if file == "REDIRECT.txt":
                    with open(filepath, "r") as rfile:
                        rpath = rfile.read()
                        base, ext = os.path.splitext(rpath)
                        if ext:
                            filepaths.append(rpath)
                        else:
                            rdfiles = []
                            for rdroot, rdfolders, rdfiles in os.walk(rpath):
                                break

                            filepaths += [os.path.join(rdroot, rdf) for rdf in rdfiles]

                    context["redirect"] = rpath
                else:
                    filepaths.append(filepath)

        return filepaths

    @err_catcher(name=__name__)
    def getFilePatternFromVersion(self, version):
        if version.get("mediaType") == "playblasts":
            if version["type"] == "asset":
                key = "playblastFilesAssets"
            elif version["type"] == "shot":
                key = "playblastFilesShots"
        else:
            if version["type"] == "asset":
                key = "renderFilesAssets"
            elif version["type"] == "shot":
                key = "renderFilesShots"

        context = version.copy()
        files = self.getFilesFromContext(version)
        if files:
            template = self.core.projects.getResolvedProjectStructurePath(key)
            data = self.core.projects.extractKeysFromPath(files[0], template, context=context)
            data["extension"] = os.path.splitext(files[0])[1]
            context.update(data)

        context["frame"] = "#" * self.core.framePadding
        pattern = self.core.projects.getResolvedProjectStructurePath(
            key, context=context
        )
        return pattern

    @err_catcher(name=__name__)
    def getMediaVersionInfoPathFromFilepath(self, path, mediaType=None):
        if mediaType == "playblasts":
            return self.getPlayblastVersionInfoPathFromFilepath(path)
        elif mediaType == "2drenders":
            return self.get2dVersionInfoPathFromFilepath(path)

        infoPath = os.path.join(
            os.path.dirname(os.path.dirname(path)),
            "versioninfo" + self.core.configs.getProjectExtension(),
        )
        return infoPath

    @err_catcher(name=__name__)
    def getPlayblastVersionInfoPathFromFilepath(self, path):
        infoPath = os.path.join(
            os.path.dirname(path), "versioninfo" + self.core.configs.getProjectExtension()
        )
        return infoPath

    @err_catcher(name=__name__)
    def get2dVersionInfoPathFromFilepath(self, path):
        infoPath = os.path.join(
            os.path.dirname(path), "versioninfo" + self.core.configs.getProjectExtension()
        )
        return infoPath

    @err_catcher(name=__name__)
    def getVersionInfoPathFromContext(self, context):
        if context.get("mediaType") == "playblasts":
            if context["type"] == "asset":
                key = "playblastFilesAssets"
            elif context["type"] == "shot":
                key = "playblastFilesShots"
        else:
            if context["type"] == "asset":
                key = "renderFilesAssets"
            elif context["type"] == "shot":
                key = "renderFilesShots"

        filepath = self.core.projects.getResolvedProjectStructurePath(
            key, context=context
        )

        if context.get("mediaType") in ["playblasts", "2drenders"]:
            infopath = self.getPlayblastVersionInfoPathFromFilepath(filepath)
        else:
            infopath = self.getMediaVersionInfoPathFromFilepath(filepath)

        return infopath

    @err_catcher(name=__name__)
    def setComment(self, versionPath, comment):
        infoPath = self.getMediaVersionInfoPathFromFilepath(versionPath)
        infoPath = os.path.join(versionPath, os.path.basename(infoPath))
        mediaInfo = {}
        if os.path.exists(infoPath):
            mediaInfo = self.core.getConfig(configPath=infoPath) or {}

        mediaInfo["comment"] = comment
        self.core.setConfig(data=mediaInfo, configPath=infoPath)

    @err_catcher(name=__name__)
    def getLatestVersionFromVersions(self, versions, includeMaster=True):
        if not versions:
            return

        if not self.getUseMaster():
            includeMaster = False

        latestVersion = None
        sortedVersions = sorted(
            versions,
            key=lambda x: x["version"] if x["version"] != "master" else "zzz",
            reverse=True,
        )
        if not includeMaster:
            sortedVersions = [v for v in sortedVersions if v["version"] != "master"]

        if not sortedVersions:
            return

        latestVersion = sortedVersions[0]
        return latestVersion

    @err_catcher(name=__name__)
    def getLatestVersionFromIdentifier(self, identifier, includeMaster=True):
        versions = self.getVersionsFromIdentifier(identifier)
        if not versions:
            return

        version = self.getLatestVersionFromVersions(
            versions, includeMaster=includeMaster
        )
        if not version:
            return

        return version

    @err_catcher(name=__name__)
    def getLatestVersionFromFilepath(self, filepath, includeMaster=True):
        data = self.getDataFromFilepath(filepath)
        if not data or len(data.keys()) <= 1:
            return

        versions = self.getVersionsFromIdentifier(data)
        version = self.getLatestVersionFromVersions(
            versions, includeMaster=includeMaster
        )
        if not version:
            return

        return version

    @err_catcher(name=__name__)
    def generateMediaProductPath(
        self,
        entity,
        task,
        extension,
        framePadding="",
        comment=None,
        version=None,
        location="global",
        aov="beauty",
        returnDetails=False,
        mediaType=None,
        singleFrame=False,
        ignoreEmpty=False,
        ignoreFolder=False,
        user=None,
        additionalContext=None,
        state=None,
        filenameTemplate=None,
    ):
        framePadding = framePadding or ""
        comment = comment or ""
        location = location or "global"

        versionUser = user or self.core.user
        basePath = self.core.paths.getRenderProductBasePaths()[location]
        context = entity.copy()
        if "version" in context:
            del context["version"]

        context.update(
            {
                "project_path": basePath,
                "identifier": task,
                "comment": comment,
                "user": versionUser,
                "extension": extension,
                "aov": aov,
                "frame": framePadding,
            }
        )
        if "layer" not in context:
            context["layer"] = ""

        if additionalContext:
            context.update(additionalContext)

        if mediaType:
            context["mediaType"] = mediaType

        version = version or self.getHighestMediaVersion(
            context, ignoreEmpty=ignoreEmpty, ignoreFolder=ignoreFolder
        )
        context["version"] = version
        if entity.get("type") == "asset":
            key = "renderFilesAssets"
        elif entity.get("type") == "shot":
            key = "renderFilesShots"
        else:
            return

        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            baseRoot = self.getSimplifiedMediaBasePath(
                entity, basePath, context.get("mediaType") or mediaType or "3drenders",
                location=location,
            )
            versionRoot = os.path.join(baseRoot, version)
            if entity.get("type") == "asset":
                entityLabel = os.path.basename(entity["asset_path"])
            else:
                entityLabel = entity.get("shot", "")
                if entity.get("sequence"):
                    entityLabel = "%s_%s" % (
                        entity["sequence"].replace("\\", "/").split("/")[-1],
                        entity["shot"],
                    )

            # Fallback: when task (identifier) is absent, resolve from entity
            # metadata so the filename token is never empty.  The identifier
            # is used for the filename only — it never appears as a folder in
            # flat mode.
            effectiveTask = task or self.core.paths.resolver.resolve_identifier(entity, task)

            if context.get("mediaType") == "2drenders":
                filename = "%s_%s_%s%s%s" % (
                    entityLabel,
                    effectiveTask,
                    version,
                    "." + framePadding if framePadding else "",
                    extension,
                )
                outputPath = os.path.join(versionRoot, filename)
            else:
                layer = context.get("layer", "")
                filename = "%s_%s_%s%s%s%s" % (
                    entityLabel,
                    effectiveTask,
                    version,
                    "_%s" % layer if layer else "",
                    "_%s" % aov if aov else "",
                    (("." + framePadding) if framePadding else "") + extension,
                )
                outputPath = os.path.join(versionRoot, aov or "rgb", filename)
            outputPath = getattr(
                self.core.appPlugin, "sm_render_fixOutputPath", lambda x, y, singleFrame, state: y
            )(self, outputPath, singleFrame=singleFrame, state=state)
            if returnDetails:
                context["path"] = outputPath
                return context
            else:
                logger.debug("Generated simplified media path: %s", outputPath)
                return outputPath

        outputPath = self.core.projects.getResolvedProjectStructurePath(
            key, context=context
        )
        outputPath = getattr(
            self.core.appPlugin, "sm_render_fixOutputPath", lambda x, y, singleFrame, state: y
        )(self, outputPath, singleFrame=singleFrame, state=state)
        if returnDetails:
            context["path"] = outputPath
            return context
        else:
            return outputPath

    @err_catcher(name=__name__)
    def generatePlayblastPath(
        self,
        entity,
        task,
        extension,
        framePadding="",
        comment=None,
        version=None,
        location="global",
        returnDetails=False,
        user=None,
        filenameTemplate=None,
    ):
        versionUser = user or self.core.user
        basePath = self.core.paths.getRenderProductBasePaths()[location]
        context = entity.copy()
        context.update(
            {
                "project_path": basePath,
                "identifier": task,
                "extension": extension,
                "frame": framePadding,
                "mediaType": "playblasts",
            }
        )

        version = version or self.getHighestMediaVersion(context)
        context["version"] = version
        context["comment"] = comment or ""
        context["user"] = versionUser

        if entity["type"] == "asset":
            key = "playblastFilesAssets"
        elif entity["type"] == "shot":
            key = "playblastFilesShots"

        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            baseRoot = self.getSimplifiedMediaBasePath(entity, basePath, "playblasts", location=location)
            versionRoot = os.path.join(baseRoot, version)
            if entity["type"] == "asset":
                entityLabel = os.path.basename(entity["asset_path"])
            else:
                entityLabel = entity.get("shot", "")
                if entity.get("sequence"):
                    entityLabel = "%s_%s" % (
                        entity["sequence"].replace("\\", "/").split("/")[-1],
                        entity["shot"],
                    )

            filename = "%s_%s_%s%s%s" % (
                entityLabel,
                task,
                version,
                "." + framePadding if framePadding else "",
                extension,
            )
            outputPath = os.path.join(versionRoot, filename)
            if returnDetails:
                context["path"] = outputPath
                return context
            else:
                logger.debug("Generated simplified playblast path: %s", outputPath)
                return outputPath

        outputPath = self.core.projects.getResolvedProjectStructurePath(
            key, context=context
        )
        if returnDetails:
            context["path"] = outputPath
            return context
        else:
            return outputPath

    @err_catcher(name=__name__)
    def getHighestMediaVersion(self, context, getExisting=False, ignoreEmpty=False, ignoreFolder=False):
        if not getExisting and not self.core.separateOutputVersionStack:
            fileName = self.core.getCurrentFileName()
            fnameData = self.core.getScenefileData(fileName)
            if fnameData.get("type") in ["asset", "shot"] and "version" in fnameData:
                hVersion = fnameData["version"]
            else:
                hVersion = self.core.versionFormat % self.core.lowestVersion

            return hVersion

        if context.get("mediaType") == "playblasts":
            key = "playblastVersions"
        else:
            key = "renderVersions"

        locations = self.core.paths.getRenderProductBasePaths()
        validData = []
        if "version" in context:
            del context["version"]

        if self.core.paths.isSimplifiedArtistWorkflowEnabled() and context.get("identifier"):
            for loc in locations:
                ctx = context.copy()
                ctx["project_path"] = locations[loc]
                basePath = self.getSimplifiedMediaBasePath(
                    ctx, ctx["project_path"], ctx.get("mediaType") or "3drenders",
                    location=loc,
                )
                versionBase = basePath
                if not os.path.isdir(versionBase):
                    continue

                for versionName in os.listdir(versionBase):
                    versionPath = os.path.join(versionBase, versionName)
                    if not os.path.isdir(versionPath):
                        continue

                    if ignoreEmpty:
                        mediaType = ctx.get("mediaType", "3drenders")
                        if mediaType == "2drenders":
                            entries = [
                                e for e in os.listdir(versionPath)
                                if not e.startswith("versioninfo")
                            ]
                            if not entries:
                                continue
                        else:
                            hasContent = False
                            for aovEntry in os.listdir(versionPath):
                                aovPath = os.path.join(versionPath, aovEntry)
                                if not os.path.isdir(aovPath):
                                    continue
                                aovFiles = [
                                    f for f in os.listdir(aovPath)
                                    if not f.startswith("versioninfo")
                                ]
                                if aovFiles:
                                    hasContent = True
                                    break
                            if not hasContent:
                                continue

                    validData.append({"version": versionName, "path": versionPath})

        else:
            for loc in locations:
                ctx = context.copy()
                ctx["project_path"] = locations[loc]
                template = self.core.projects.getResolvedProjectStructurePath(
                    key, context=ctx
                )

                productData = self.core.projects.getMatchingPaths(template)
                for data in productData:
                    if ignoreEmpty:
                        if ignoreFolder:
                            files = None
                            for root, folders, files in os.walk(data["path"]):
                                break

                            if not files:
                                continue

                        else:
                            if not os.path.isdir(data["path"]):
                                continue

                        if ctx.get("mediaType") == "2drenders":
                            exFiles = os.listdir(data["path"])
                            if len(exFiles) > 1 or (
                                len(exFiles) == 1 and not exFiles[0].startswith("versioninfo")
                            ):
                                validData.append(data)
                        else:
                            for folder in os.listdir(data["path"]):
                                path = os.path.join(data["path"], folder)
                                if not os.path.isdir(path):
                                    continue

                                exFiles = os.listdir(path)
                                if len(exFiles) > 1 or (
                                    len(exFiles) == 1 and not exFiles[0].startswith("versioninfo")
                                ):
                                    validData.append(data)
                    else:
                        validData.append(data)

        highversion = None
        for data in validData:
            try:
                version = int(data.get("version")[1: (1 + self.core.versionPadding)])
            except:
                continue

            if highversion is None or version > highversion:
                highversion = version

        if getExisting and highversion is not None:
            return self.core.versionFormat % (highversion)
        else:
            if highversion is None:
                return self.core.versionFormat % (self.core.lowestVersion)
            else:
                return self.core.versionFormat % (highversion + 1)

    @err_catcher(name=__name__)
    def getVersionFromFilepath(self, path):
        data = self.getDataFromFilepath(path)

        if "version" not in data:
            return

        version = data["version"]
        return version

    # @err_catcher(name=__name__)
    # def getDataFromFilepath(self, path):
    #     path = os.path.normpath(path)
    #     entityType = self.core.paths.getEntityTypeFromPath(path)

    #     if entityType == "asset":
    #         key = "renderFilesAssets"
    #     elif entityType == "shot":
    #         key = "renderFilesShots"
    #     else:
    #         return {}

    #     template = self.core.projects.getResolvedProjectStructurePath(key)
    #     data = self.core.projects.extractKeysFromPath(path, template, context={"entityType": entityType})
    #     if not data:
    #         if entityType == "asset":
    #             key = "playblastFilesAssets"
    #         elif entityType == "shot":
    #             key = "playblastFilesShots"

    #         template = self.core.projects.getResolvedProjectStructurePath(key)
    #         data = self.core.projects.extractKeysFromPath(path, template, context={"entityType": entityType})
    #         if data:
    #             data["mediaType"] = "playblasts"

    #     data["type"] = entityType
    #     if "asset_path" in data:
    #         data["asset"] = os.path.basename(data["asset_path"])

    #     return data

    @err_catcher(name=__name__)
    def getDataFromFilepath(self, path, isVersionFolder=False):
        if not path:
            return {}

        path = os.path.normpath(path)
        entityType = self.core.paths.getEntityTypeFromPath(path)
        entity = self.core.paths.getRenderProductData(path) or {}
        isValid = (entity.get("type") == "asset" and entity.get("asset_path")) or (entity.get("type") == "shot" and entity.get("shot"))
        if not isValid:
            entity = self.core.paths.getRenderProductData(path, mediaType="2drenders")
            isValid = (entity.get("type") == "asset" and entity.get("asset_path")) or (entity.get("type") == "shot" and entity.get("shot"))
            if not isValid:
                entity = self.core.paths.getPlayblastProductData(path)
                isValid = (entity.get("type") == "asset" and entity.get("asset_path")) or (entity.get("type") == "shot" and entity.get("shot"))
                if not isValid:
                    entity = self.core.paths.getRenderProductData(path, mediaType="externalMedia")
                    isValid = (entity.get("type") == "asset" and entity.get("asset_path")) or (entity.get("type") == "shot" and entity.get("shot"))
                    if not isValid:
                        if isVersionFolder:
                            entity = {}
                        else:
                            entity = self.getDataFromFilepath(os.path.dirname(path), isVersionFolder=True)
                            isValid = (entity.get("type") == "asset" and entity.get("asset_path")) or (entity.get("type") == "shot" and entity.get("shot"))
                            if not isValid:
                                entity = {}

        entity["type"] = entityType
        if "asset_path" in entity:
            entity["asset"] = os.path.basename(entity["asset_path"])

        return entity

    @err_catcher(name=__name__)
    def getVersionFromPlayblastFilepath(self, path):
        entityType = self.core.paths.getEntityTypeFromPath(path)

        if entityType == "asset":
            key = "playblastFilesAssets"
        elif entityType == "shot":
            key = "playblastFilesShots"

        template = self.core.projects.getResolvedProjectStructurePath(key)
        data = self.core.projects.extractKeysFromPath(path, template, context={"entityType": entityType})
        if "version" not in data:
            return

        version = data["version"]
        return version

    @err_catcher(name=__name__)
    def getVersionFromVersionFolder(self, versionFolder, context=None):
        path = os.path.normpath(versionFolder)
        key = "renderVersions"
        context = context or {}

        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            compatData = self.getSimplifiedMediaData(path, mediaType=context.get("mediaType"), isVersionFolder=True)
            if compatData.get("version"):
                return compatData["version"]

        location = self.getLocationFromPath(versionFolder)
        if location:
            context["project_path"] = self.core.paths.getRenderProductBasePaths()[location]

        if "type" in context and "entityType" not in context:
            context["entityType"] = context["type"]

        if context and "version" in context:
            del context["version"]

        template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
        data = self.core.projects.extractKeysFromPath(path, template, context=context)

        if not data:
            key = "playblastVersions"
            template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
            data = self.core.projects.extractKeysFromPath(path, template, context=context)

        if not data and "mediaType" not in context:
            key = "renderVersions"
            context["mediaType"] = "2drenders"
            template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
            data = self.core.projects.extractKeysFromPath(path, template, context=context)

        if "version" not in data:
            return

        version = data["version"]
        return version

    @err_catcher(name=__name__)
    def getRenderProductDataFromFilepath(self, filepath, mediaType="3drenders"):
        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            compatData = self.getSimplifiedMediaData(filepath, mediaType=mediaType)
            if compatData:
                return compatData

        entityType = self.core.paths.getEntityTypeFromPath(filepath)
        if entityType == "asset":
            key = "renderFilesAssets"
        elif entityType == "shot":
            key = "renderFilesShots"
        else:
            return {}

        context = {"type": entityType}
        context["mediaType"] = mediaType
        location = self.getLocationFromPath(filepath)
        if location:
            context["project_path"] = self.core.paths.getRenderProductBasePaths()[location]

        template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
        context = {"entityType": entityType, "project_path": context["project_path"]}
        data = self.core.projects.extractKeysFromPath(filepath, template, context=context)

        if not data:
            if entityType == "asset":
                key = "playblastFilesAssets"
            elif entityType == "shot":
                key = "playblastFilesShots"

            context = {"entityType": entityType, "project_path": context["project_path"]}
            template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
            context = {"entityType": entityType, "project_path": context["project_path"]}
            data = self.core.projects.extractKeysFromPath(filepath, template, context=context)
            if data:
                data["mediaType"] = "playblasts"

        data["type"] = entityType
        if "asset_path" in data:
            data["asset"] = os.path.basename(data["asset_path"])

        return data

    @err_catcher(name=__name__)
    def getMediaDataFromVersionFolder(self, path, mediaType="3drenders"):
        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            compatData = self.getSimplifiedMediaData(path, mediaType=mediaType, isVersionFolder=True)
            if compatData:
                return compatData

        entityType = self.core.paths.getEntityTypeFromPath(path)
        key = "renderVersions"
        context = {"type": entityType, "entityType": entityType}
        context["mediaType"] = mediaType
        location = self.getLocationFromPath(path)
        if location:
            context["project_path"] = self.core.paths.getRenderProductBasePaths()[location]

        template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
        context = {"entityType": entityType, "project_path": context["project_path"]}
        data = self.core.projects.extractKeysFromPath(path, template, context=context)
        data["type"] = entityType
        if "asset_path" in data:
            data["asset"] = os.path.basename(data["asset_path"])

        return data

    @err_catcher(name=__name__)
    def getLocationFromPath(self, path):
        locDict = self.core.paths.getRenderProductBasePaths()
        nPath = os.path.normpath(path)
        validLocs = []
        for location in locDict:
            if nPath.startswith(locDict[location]):
                validLocs.append(location)

        if not validLocs:
            return

        validLocs = sorted(validLocs, key=lambda x: len(locDict[x]), reverse=True)
        return validLocs[0]

    @err_catcher(name=__name__)
    def getVersionPathFromMediaFilePath(self, path, mediaType, entityType=None):
        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            compatData = self.getSimplifiedMediaData(path, mediaType=mediaType)
            if compatData:
                basePath = self.getSimplifiedMediaBasePath(
                    compatData, compatData["project_path"], compatData.get("mediaType") or mediaType
                )
                return os.path.join(basePath, compatData["version"])

        if not entityType:
            entityType = self.core.paths.getEntityTypeFromPath(path)
            if not entityType:
                context = self.core.paths.getMediaProductData(path, mediaType=mediaType)
                entityType = context.get("type")

        key = None
        context = {"mediaType": mediaType}
        if mediaType == "playblasts":
            versionKey = "playblastVersions"
            if entityType == "asset":
                key = "playblastFilesAssets"
            elif entityType == "shot":
                key = "playblastFilesShots"
        else:
            versionKey = "renderVersions"
            if entityType == "asset":
                key = "renderFilesAssets"
            elif entityType == "shot":
                key = "renderFilesShots"

        if not key:
            return

        location = self.getLocationFromPath(path)
        context["project_path"] = self.core.paths.getRenderProductBasePaths()[location]
        template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
        data = self.core.projects.extractKeysFromPath(path, template, context={"entityType": entityType})
        data.update(context)

        versionPath = self.core.projects.getResolvedProjectStructurePath(
            versionKey, context=data
        )

        return versionPath

    @err_catcher(name=__name__)
    def updateMasterVersion(self, path=None, context=None, isFilepath=True, add=False, mediaType=None):
        if context:
            path = context["path"]
            files = self.core.getFilesFromFolder(path)
            if files:
                ext = os.path.splitext(files[0])[1]
            else:
                ext = ".exr"

            context["extension"] = ext
            isFilepath = False
        else:
            if mediaType == "playblasts":
                context = self.core.paths.getPlayblastProductData(path, isFilepath=isFilepath)
            elif mediaType == "2drenders":
                context = self.core.paths.getRenderProductData(path, isFilepath=isFilepath, mediaType=mediaType)
            else:
                context = self.core.paths.getRenderProductData(path, isFilepath=isFilepath)

        forcedLoc = os.getenv("PRISM_MEDIA_MASTER_LOC")
        if forcedLoc:
            location = forcedLoc
        else:
            location = self.getLocationFromPath(path)

        if "mediaType" not in context:
            context["mediaType"] = mediaType or self.getMediaTypeFromContext(context)

        if context.get("mediaType") == "playblasts":
            masterPath = self.generatePlayblastPath(
                entity=context,
                task=context["identifier"],
                extension=context["extension"],
                version="master",
                location=location,
                framePadding="",
            )
        else:
            masterPath = self.generateMediaProductPath(
                entity=context,
                task=context["identifier"],
                extension=context.get("extension"),
                version="master",
                location=location,
                framePadding=None,
                mediaType=context.get("mediaType")
            )

        logger.debug("updating master render version: %s from %s" % (masterPath, path))
        if not add:
            result = self.deleteMasterVersion(masterPath, isFilepath=True, mediaType=context.get("mediaType"))
            if not result:
                return

            masterVersions = []
        else:
            masterVersions = self.getVersionPathsFromMaster(masterPath, isFilepath=True)

        masterDrive = os.path.splitdrive(masterPath)[0]
        drive = os.path.splitdrive(path)[0]

        masterBase = self.getVersionPathFromMediaFilePath(masterPath, mediaType=context.get("mediaType"), entityType=context.get("type"))
        if isFilepath:
            originBase = self.getVersionPathFromMediaFilePath(path, mediaType=context.get("mediaType"), entityType=context.get("type"))
        else:
            originBase = path

        files = self.core.getFilesFromFolder(originBase, recursive=True)
        for file in files:
            frameStr = os.path.splitext(file)[0][-self.core.framePadding :]
            if sys.version[0] == "2":
                frameStr = unicode(frameStr)

            masterFilename = self.core.paths.replaceVersionInStr(
                os.path.basename(file), "master"
            )
            masterFile = file.replace(originBase, masterBase)
            masterFile = os.path.join(os.path.dirname(masterFile), masterFilename)

            if not os.path.exists(os.path.dirname(masterFile)):
                try:
                    os.makedirs(os.path.dirname(masterFile))
                except Exception as e:
                    if e.errno != errno.EEXIST:
                        raise

            useHL = os.getenv("PRISM_USE_HARDLINK_MASTER", None)
            if platform.system() == "Windows" and drive == masterDrive and useHL:
                self.core.createSymlink(masterFile, file)
            else:
                shutil.copy2(file, masterFile)

        masterVersions.append(originBase)
        ext = self.core.configs.getProjectExtension()
        masterInfoPath = os.path.join(masterBase, "versioninfo" + ext)
        self.core.setConfig(
            "versionpaths", val=masterVersions, configPath=masterInfoPath
        )
        self.core.media.invalidateOiioCache()
        return masterPath

    @err_catcher(name=__name__)
    def getMasterVersionNumber(self, masterPath, allowCache=True):
        versionData = self.core.paths.getRenderProductData(masterPath, validateModTime=True, allowCache=allowCache)
        if "versionpaths" in versionData:
            context = versionData.copy()
            for path in versionData["versionpaths"]:
                vName = self.core.mediaProducts.getVersionFromVersionFolder(
                    path, context=context
                )
                if vName:
                    return vName
        else:
            if "sourceVersion" in versionData:
                return versionData["sourceVersion"]

            if "version" in versionData:
                return versionData["version"]

    @err_catcher(name=__name__)
    def getMasterVersionLabel(self, path):
        versionName = "master"
        versionData = self.core.paths.getRenderProductData(path, validateModTime=True, isVersionFolder=True)
        if "versionpaths" in versionData:
            versions = []
            context = versionData.copy()
            for path in versionData["versionpaths"]:
                vName = self.core.mediaProducts.getVersionFromVersionFolder(
                    path, context=context
                )
                if vName:
                    versions.append(vName)

            versionStr = ", ".join(versions)
            versionName = "master"
            if versionStr:
                versionName += " (%s)" % versionStr

        return versionName

    @err_catcher(name=__name__)
    def getMediaTypeFromContext(self, context):
        mtype = "3drenders"
        if "displayName" in context:
            ndata = context["displayName"].rsplit(" (", 1)
            if len(ndata) == 2 and ndata[1][-1] == ")":
                mtype = ndata[1][:-1]

                if mtype == "2d":
                    mtype = "2drenders"
                elif mtype == "playblast":
                    mtype = "playblasts"
                elif mtype == "external":
                    mtype = "externalMedia"

        return mtype

    @err_catcher(name=__name__)
    def getMediaTypeFromPath(self, path):
        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            compatData = self.getSimplifiedMediaData(path)
            if compatData.get("mediaType"):
                return compatData["mediaType"]

        base, ext = os.path.splitext(path)
        if ext:
            dirpath = os.path.basename(path)
        else:
            dirpath = path

        infoPath = os.path.join(dirpath, "versioninfo" + self.core.configs.getProjectExtension())
        if not os.path.exists(infoPath):
            infoPath = os.path.join(os.path.dirname(dirpath), "versioninfo" + self.core.configs.getProjectExtension())

        data = self.core.getConfig(configPath=infoPath)
        if data and "mediaType" in data:
            return data["mediaType"]

        entityType = self.core.paths.getEntityTypeFromPath(path)
        if entityType == "asset":
            key = "renderFilesAssets"
        elif entityType == "shot":
            key = "renderFilesShots"
        else:
            return

        mediaType = None
        context = {"type": entityType}
        context["mediaType"] = "3drenders"
        location = self.getLocationFromPath(path)
        if location:
            context["project_path"] = self.core.paths.getRenderProductBasePaths()[location]

        template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
        context = {"entityType": entityType, "project_path": context["project_path"]}
        data = self.core.projects.extractKeysFromPath(path, template, context=context)
        if data:
            mediaType = "3drenders"
        else:
            if entityType == "asset":
                key = "playblastFilesAssets"
            elif entityType == "shot":
                key = "playblastFilesShots"

            context = {"entityType": entityType, "project_path": context["project_path"]}
            template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
            context = {"entityType": entityType, "project_path": context["project_path"]}
            data = self.core.projects.extractKeysFromPath(path, template, context=context)
            if data:
                mediaType = "playblasts"
            else:
                key = "renderVersions"
                context["mediaType"] = "2drenders"
                template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
                data = self.core.projects.extractKeysFromPath(os.path.dirname(path), template, context=context)
                if data:
                    mediaType = "2drenders"
                else:
                    key = "renderVersions"
                    context["mediaType"] = "externalMedia"
                    template = self.core.projects.getResolvedProjectStructurePath(key, context=context)
                    data = self.core.projects.extractKeysFromPath(os.path.dirname(os.path.dirname(path)), template, context=context)
                    if data:
                        mediaType = "externalMedia"

        return mediaType

    @err_catcher(name=__name__)
    def deleteMasterVersion(self, path, isFilepath=False, mediaType=None, allowClear=True, allowRename=True):
        if isFilepath:
            vpath = self.getVersionPathFromMediaFilePath(path, mediaType=mediaType)
        else:
            vpath = path

        logger.debug("removing master render version: %s" % vpath)
        if vpath and os.path.exists(vpath):
            try:
                shutil.rmtree(vpath)
            except Exception as e:
                if self.core.pb and allowClear:
                    self.core.pb.mediaBrowser.lw_version.clearSelection()
                    return self.deleteMasterVersion(path, isFilepath=isFilepath, mediaType=mediaType, allowClear=False, allowRename=allowRename)

                if allowRename:
                    renamed = self.core.products.renameMaster(vpath)
                    if renamed:
                        return True

                logger.warning(e)
                msg = "Couldn't remove the existing master version:\n\n%s" % (str(e))
                result = self.core.popupQuestion(
                    msg,
                    buttons=["Retry", "Don't delete master version"],
                    icon=QMessageBox.Warning,
                )
                if result == "Retry":
                    return self.deleteMasterVersion(path, isFilepath=isFilepath, mediaType=mediaType, allowClear=allowClear, allowRename=allowRename)
                else:
                    return False

        return True

    @err_catcher(name=__name__)
    def addToMasterVersion(self, path=None, context=None, isFilepath=True, mediaType=None):
        self.updateMasterVersion(
            path=path, context=context, isFilepath=isFilepath, add=True, mediaType=mediaType
        )

    @err_catcher(name=__name__)
    def getVersionPathsFromMaster(self, path, isFilepath=True):
        infoPath = self.getMediaVersionInfoPathFromFilepath(path)
        paths = self.core.getConfig("versionpaths", configPath=infoPath) or []
        return paths

    @err_catcher(name=__name__)
    def getUseMaster(self):
        return self.core.getConfig(
            "globals", "useMasterRenderVersion", dft=False, config="project"
        )

    @err_catcher(name=__name__)
    def getLinkedToTasks(self):
        return self.core.getConfig("globals", "productTasks", config="project")

    @err_catcher(name=__name__)
    def createIdentifier(self, entity, identifier, identifierType="3drenders", location="global"):
        context = entity.copy()
        context["identifier"] = identifier
        context["task"] = self.core.paths.normalizeTask(
            context.get("task"), context=context, reason="media identifier creation"
        )

        if "user" not in context:
            context["user"] = self.core.user

        basePath = self.core.paths.getRenderProductBasePaths()[location]
        context["project_path"] = basePath
        path = self.core.projects.getResolvedProjectStructurePath(identifierType, context)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                self.core.popup("The directory %s could not be created" % path)
                return
            else:
                self.core.callback(
                    name="onIdentifierCreated",
                    args=[self, path, context],
                )

            logger.debug("identifier created %s" % path)
        else:
            logger.debug("identifier already exists: %s" % path)

        return path

    @err_catcher(name=__name__)
    def createVersion(self, entity, identifier, version, identifierType="3drenders", location="global"):
        context = entity.copy()
        context["identifier"] = identifier
        context["mediaType"] = identifierType
        context["version"] = version
        context["task"] = self.core.paths.normalizeTask(
            context.get("task"), context=context, reason="media version creation"
        )

        if "user" not in context:
            context["user"] = self.core.user

        basePath = self.core.paths.getRenderProductBasePaths()[location]
        context["project_path"] = basePath
        if context.get("mediaType") == "playblasts":
            key = "playblastVersions"
        else:
            key = "renderVersions"

        path = self.core.projects.getResolvedProjectStructurePath(key, context)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                self.core.popup("The directory %s could not be created" % path)
                return
            else:
                self.core.callback(
                    name="onVersionCreated",
                    args=[self, path, context],
                )

            logger.debug("version created %s" % path)
        else:
            logger.debug("version already exists: %s" % path)

        return path

    @err_catcher(name=__name__)
    def createAov(self, entity, identifier, version, aov, identifierType="3drenders"):
        context = entity.copy()
        context["identifier"] = identifier
        context["mediaType"] = identifierType
        context["version"] = version
        context["aov"] = aov
        context["task"] = self.core.paths.normalizeTask(
            context.get("task"), context=context, reason="media aov creation"
        )

        if "user" not in context:
            context["user"] = self.core.user

        if self.core.paths.isSimplifiedArtistWorkflowEnabled():
            projectPath = (
                entity.get("project_path")
                or self.core.paths.getRenderProductBasePaths().get("global", "")
            )
            aovLocation = self.core.paths.getLocationNameFromBasePath(projectPath) or "global"
            versionBase = self.getSimplifiedMediaBasePath(entity, projectPath, identifierType, location=aovLocation)
            path = os.path.join(versionBase, version, aov)
        else:
            path = self.core.projects.getResolvedProjectStructurePath("aovs", context)

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                self.core.popup("The directory %s could not be created" % path)
                return
            else:
                self.core.callback(
                    name="onAovCreated",
                    args=[self, path, context],
                )

            logger.debug("aov created %s" % path)
        else:
            logger.debug("aov already exists: %s" % path)

        return path

    @err_catcher(name=__name__)
    def ingestMedia(self, files, entity, identifier, version, aov, mediaType="3drenders", filenameTemplate=None, location="global"):
        if not files:
            return

        kwargs = {
            "entity": entity,
            "task": identifier,
            "version": version,
            "aov": aov,
            "user": self.core.user,
            "mediaType": mediaType,
            "filenameTemplate": filenameTemplate,
            "location": location,
        }

        baseTxt = "Copying file - please wait..\n\n"
        updatedText = baseTxt + "%s/%s" % (0, len(files))
        self.copyMsg = self.core.waitPopup(self.core, updatedText, hidden=True)

        self.ingestedFiles = []
        self.ingestCanceled = False
        self.ingestThreads = []
        startFrame = 1
        if entity.get("type") == "shot":
            shotRange = self.core.entities.getShotRange(entity)
            if shotRange:
                startFrame = shotRange[0]
                if startFrame is None:
                    startFrame = 1

        with self.copyMsg as copyMsg:
            for idx, file in enumerate(files):
                if self.ingestCanceled:
                    return

                kwargs["extension"] = os.path.splitext(file)[1]
                if len(files) > 1:
                    kwargs["framePadding"] = ("%%0%sd" % self.core.framePadding) % (idx + startFrame)

                if kwargs.get("mediaType") == "playblasts":
                    pbkwargs = kwargs.copy()
                    del pbkwargs["aov"]
                    del pbkwargs["mediaType"]
                    targetPath = self.generatePlayblastPath(**pbkwargs)
                else:
                    targetPath = self.generateMediaProductPath(**kwargs)

                if idx == 0:
                    if not os.path.exists(os.path.dirname(targetPath)):
                        try:
                            os.makedirs(os.path.dirname(targetPath))
                        except:
                            msg = "The directory could not be created"
                            self.core.popup(msg)
                            return {"result": msg}

                    elif os.listdir(os.path.dirname(targetPath)):
                        msg = "The targetfolder contains files already.\nContinuing may overwrite existing files."
                        result = self.core.popupQuestion(msg, buttons=["Continue", "Add new version", "Cancel"], icon=QMessageBox.Warning)
                        if result == "Cancel":
                            return {"result": "canceled"}
                        elif result == "Add new version":
                            context = kwargs["entity"].copy()
                            context["identifier"] = identifier
                            context["mediaType"] = mediaType
                            version = self.getHighestMediaVersion(context)
                            self.createVersion(
                                entity=kwargs["entity"],
                                identifier=kwargs["task"],
                                identifierType=kwargs["mediaType"],
                                version=version
                            )

                            if kwargs["mediaType"] == "3drenders":
                                self.createAov(entity=kwargs["entity"], identifier=kwargs["task"], version=version, aov="rgb")

                            result = self.ingestMedia(files, entity, identifier, version, aov, mediaType) or {}
                            return {"result": result.get("result"), "versionAdded": True}

                    self.copyMsg.show()
                    if copyMsg.msg:
                        b_cnl = copyMsg.msg.buttons()[0]
                        b_cnl.setVisible(True)
                        b_cnl.clicked.connect(self.onIngestCanceled)

                    QApplication.processEvents()

                targetPath = targetPath.replace("\\", "/")
                copyThread = self.core.copyWithProgress(file, targetPath, popup=False, start=False)
                self.ingestThreads.append(copyThread)
                copyThread.finished.connect(lambda t=copyThread, tp=targetPath: self.onMediaFileIngested(t, tp, len(files)))
                copyThread.start()

            details = entity.copy()
            details["identifier"] = identifier
            details["user"] = kwargs["user"]
            details["version"] = kwargs["version"]
            details["comment"] = kwargs.get("comment", "")
            details["extension"] = kwargs["extension"]
            details["mediaType"] = kwargs["mediaType"]

            infoPath = self.getMediaVersionInfoPathFromFilepath(targetPath, mediaType=mediaType)
            self.core.saveVersionInfo(filepath=os.path.dirname(infoPath), details=details)
            while (len(self.ingestedFiles) != len(files)) and not self.ingestCanceled:
                time.sleep(0.1)
                QApplication.processEvents()

        return {"result": self.ingestedFiles, "versionAdded": False, "versionPath": targetPath}

    @err_catcher(name=__name__)
    def onMediaFileIngested(self, thread, targetPath, numFiles):
        self.ingestedFiles.append(targetPath)
        logger.debug("ingested media: %s" % targetPath)
        baseTxt = "Copying file - please wait..\n\n"
        updatedText = baseTxt + "%s/%s" % (len(self.ingestedFiles), numFiles)
        self.copyMsg.text = updatedText
        if self.copyMsg.msg:
            self.copyMsg.msg.setText(updatedText)
            QApplication.processEvents()

        if len(self.ingestedFiles) == numFiles:
            self.copyMsg.close()

    @err_catcher(name=__name__)
    def onIngestCanceled(self):
        self.ingestCanceled = True
        for thread in self.ingestThreads:
            if thread.isRunning():
                thread.cancel()

    @err_catcher(name=__name__)
    def checkMasterVersions(self, entities, parent=None):
        self.dlg_masterManager = self.core.paths.masterManager(self.core, entities, "media", parent=parent)
        self.dlg_masterManager.refreshData()
        if not self.dlg_masterManager.outdatedVersions:
            msg = "All master versions of the selected entities are up to date."
            self.core.popup(msg, severity="info")
            return

        self.dlg_masterManager.show()

    @err_catcher(name=__name__)
    def getOutdatedMasterVersions(self, entities):
        outdatedVersions = []
        for entity in entities:
            idfs = self.getIdentifiersByType(entity)
            for cat in idfs:
                for idf in idfs[cat]:
                    versions = self.getVersionsFromContext(idf)
                    latestVersion = self.getLatestVersionFromVersions(versions)
                    if not latestVersion:
                        continue

                    if latestVersion["version"] == "master":
                        versionNumber = self.getMasterVersionNumber(latestVersion["path"])
                        masterLoc = self.getLocationFromPath(latestVersion["path"])
                        locVersions = [v for v in versions if self.getLocationFromPath(v["path"]) == masterLoc]
                        latestNumberVersion = self.getLatestVersionFromVersions(locVersions, includeMaster=False)
                        if latestNumberVersion and latestNumberVersion["version"] != versionNumber:
                            outdatedVersions.append({"master": latestVersion, "latest": latestNumberVersion})
                    else:
                        outdatedVersions.append({"master": None, "latest": latestVersion})

        return outdatedVersions

    @err_catcher(name=__name__)
    def getGroupFromIdentifier(self, identifier):
        identifierPath = self.getIdentifierPathFromEntity(identifier)
        cfgPath = os.path.join(identifierPath, "identifiers" + self.core.configs.getProjectExtension())
        group = self.core.getConfig(identifier.get("displayName"), "group", configPath=cfgPath)
        return group

    @err_catcher(name=__name__)
    def setIdentifiersGroup(self, identifiers, group, projectWide=False):
        identifierPath = self.getIdentifierPathFromEntity(identifiers[0])
        cfgPath = os.path.join(identifierPath, "identifiers" + self.core.configs.getProjectExtension())
        data = self.core.getConfig(configPath=cfgPath) or {}
        for identifier in identifiers:
            if identifier.get("displayName") not in data:
                data[identifier.get("displayName")] = {}

            data[identifier.get("displayName")]["group"] = group

        self.core.setConfig(data=data, configPath=cfgPath)
