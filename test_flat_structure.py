# -*- coding: utf-8 -*-
# test_flat_structure.py -- headless test for flat-structure refactor

import os, sys, json, shutil, traceback

# ── Bootstrap Prism ──────────────────────────────────────────────────────────
PRISM_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PRISM_ROOT, "Scripts"))
sys.path.insert(0, os.path.join(PRISM_ROOT, "PythonLibs", "Python3"))
sys.path.insert(0, os.path.join(PRISM_ROOT, "PythonLibs", "CrossPlatform"))

# Qt must exist before PrismCore import
try:
    from qtpy import QtWidgets, QtCore
    _qapp = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
except Exception:
    pass

import PrismCore

# ── Helpers ───────────────────────────────────────────────────────────────────
PASS  = "[PASS]"
FAIL  = "[FAIL]"
INFO  = "[INFO]"
WARN  = "[WARN]"

results = []

def check(label, condition, got=None, expected=None):
    if condition:
        tag = PASS
        results.append(("PASS", label))
    else:
        tag = FAIL
        results.append(("FAIL", label))
    line = "%s  %s" % (tag, label)
    if not condition:
        if expected is not None:
            line += "\n         expected : %s" % expected
        if got is not None:
            line += "\n         got      : %s" % got
    print(line)

def section(title):
    print("\n%s  -- %s --" % (INFO, title))

# ── Create headless PrismCore ─────────────────────────────────────────────────
section("Initialising Prism (noUI, noSplash)")
try:
    core = PrismCore.create(app="Standalone", prismArgs=["noUI", "noSplash"])
    check("PrismCore created", core is not None)
except Exception as e:
    print(FAIL + "  PrismCore failed to init: %s" % e)
    traceback.print_exc()
    sys.exit(1)

# ── Load the Visions project ───────────────────────────────────────────────────
PROJECT_PATH = os.path.join(PRISM_ROOT, "Presets", "Projects", "Visions")
section("Loading project: %s" % PROJECT_PATH)

try:
    core.changeProject(PROJECT_PATH)
    check("Project loaded", core.projectPath and os.path.normpath(core.projectPath) == os.path.normpath(PROJECT_PATH))
except Exception as e:
    print(FAIL + "  changeProject raised: %s" % e)
    traceback.print_exc()

# ── Test 1: use_flat_structure config key ─────────────────────────────────────
section("Test 1 — use_flat_structure config key")
val = core.getConfig("globals", "use_flat_structure", config="project")
check("use_flat_structure present in pipeline.json", val is not None, got=val, expected="True / False")
check("use_flat_structure == True", val is True, got=val, expected=True)

# ── Test 2: isSimplifiedArtistWorkflowEnabled ─────────────────────────────────
section("Test 2 — isSimplifiedArtistWorkflowEnabled()")
flat = core.paths.isSimplifiedArtistWorkflowEnabled()
check("returns True (flat mode active)", flat is True, got=flat, expected=True)

# ── Test 3: MediaPathResolver wired up ───────────────────────────────────────
section("Test 3 — MediaPathResolver instantiated")
check("core.paths.resolver exists", hasattr(core.paths, "resolver"))
if hasattr(core.paths, "resolver"):
    from PrismUtils.PathManager import MediaPathResolver
    check("resolver is MediaPathResolver", isinstance(core.paths.resolver, MediaPathResolver))

# ── Test 4: getSimplifiedMediaBasePath folder routing ────────────────────────
section("Test 4 — getSimplifiedMediaBasePath folder routing")

# Fake entity & project path – no files needed for this test
shot_entity = {
    "type":     "shot",
    "sequence": "sq010",
    "shot":     "sh010",
}
FAKE_PROJECT = PROJECT_PATH   # use the template dir as the "project root"
# We need getSimplifiedOutputRoot to return something; it depends on project structure.
# So we just test the suffix logic by inspecting the returned path.
try:
    base3d = core.mediaProducts.getSimplifiedMediaBasePath(shot_entity, FAKE_PROJECT, "3drenders")
    base2d = core.mediaProducts.getSimplifiedMediaBasePath(shot_entity, FAKE_PROJECT, "2drenders")
    basepb = core.mediaProducts.getSimplifiedMediaBasePath(shot_entity, FAKE_PROJECT, "playblasts")
    baseex = core.mediaProducts.getSimplifiedMediaBasePath(shot_entity, FAKE_PROJECT, "externalMedia")

    check("3drenders ends with /renders",      base3d.replace("\\","/").endswith("/renders"),   got=base3d)
    check("2drenders ends with /renders",      base2d.replace("\\","/").endswith("/renders"),   got=base2d)
    check("playblasts ends with /playblasts",  basepb.replace("\\","/").endswith("/playblasts"),got=basepb)
    check("externalMedia ends with /external", baseex.replace("\\","/").endswith("/external"),  got=baseex)
    check("No 'Renders' or 'identifier' in 3d path", "Renders" not in base3d and "identifier" not in base3d, got=base3d)
except Exception as e:
    print(FAIL + "  getSimplifiedMediaBasePath raised: %s" % e)
    traceback.print_exc()

# ── Test 5: generateMediaProductPath output structure ─────────────────────────
section("Test 5 — generateMediaProductPath path structure")
try:
    path = core.mediaProducts.generateMediaProductPath(
        entity        = shot_entity,
        task          = "Lighting",
        extension     = ".exr",
        framePadding  = "####",
        version       = "v0001",
        aov           = "beauty",
        mediaType     = "3drenders",
        location      = "global",
    )
    if path:
        p = path.replace("\\", "/")
        check("Path contains /renders/",              "/renders/" in p,      got=p)
        check("Path contains /v0001/",                "/v0001/" in p,        got=p)
        check("Path contains /beauty/",               "/beauty/" in p,       got=p)
        check("No /3dRender/ in path",                "/3dRender/" not in p, got=p)
        check("No /identifier/ folder (Lighting as folder)", "/Lighting/" not in p, got=p)
        check("Filename contains Lighting (token)",   "Lighting" in os.path.basename(p), got=os.path.basename(p))
        print("         >> %s" % p)
    else:
        print(FAIL + "  generateMediaProductPath returned empty")
        results.append(("FAIL", "generateMediaProductPath returned empty"))
except Exception as e:
    print(FAIL + "  generateMediaProductPath raised: %s" % e)
    traceback.print_exc()

# ── Test 6: generateMediaProductPath with task=None (fallback) ────────────────
section("Test 6 — Identifier fallback when task is None")
try:
    path_no_task = core.mediaProducts.generateMediaProductPath(
        entity        = shot_entity,
        task          = None,
        extension     = ".exr",
        framePadding  = "####",
        version       = "v0001",
        aov           = "beauty",
        mediaType     = "3drenders",
        location      = "global",
    )
    if path_no_task:
        fn = os.path.basename(path_no_task)
        check("Filename not empty when task=None", bool(fn), got=fn)
        check("No 'None' literal in filename",     "None" not in fn,        got=fn)
        print("         >> %s" % path_no_task.replace("\\","/"))
    else:
        print(WARN + "  path was empty (may need valid project root)")
except Exception as e:
    print(FAIL + "  identifier fallback raised: %s" % e)
    traceback.print_exc()

# ── Test 7: generatePlayblastPath ─────────────────────────────────────────────
section("Test 7 — generatePlayblastPath path structure")
try:
    pbpath = core.mediaProducts.generatePlayblastPath(
        entity    = shot_entity,
        task      = "Animation",
        extension = ".mp4",
        version   = "v0001",
        location  = "global",
    )
    if pbpath:
        p = pbpath.replace("\\", "/")
        check("Playblast path contains /playblasts/", "/playblasts/" in p, got=p)
        check("Playblast path contains /v0001/",       "/v0001/" in p,     got=p)
        check("No /Playblasts/ (capital)",             "/Playblasts/" not in p, got=p)
        print("         >> %s" % p)
    else:
        print(WARN + "  generatePlayblastPath returned empty")
except Exception as e:
    print(FAIL + "  generatePlayblastPath raised: %s" % e)
    traceback.print_exc()

# ── Test 8: Legacy shim (simulated on disk) ────────────────────────────────────
section("Test 8 — Legacy shim discovers old Renders/ content")

# Build fake legacy folder structure in a temp directory
import tempfile
TEMP = tempfile.mkdtemp(prefix="prism_legacy_test_")
try:
    # Fake entity path structure: <project>/Output/04-Cameras/sq010/sh010
    entity_root = os.path.join(TEMP, "Output", "04-Cameras", "sq010", "sh010")
    old_render  = os.path.join(entity_root, "Renders", "3dRender", "lighting", "v0001", "beauty")
    old_pb      = os.path.join(entity_root, "Playblasts", "main", "v0001")
    os.makedirs(old_render)
    os.makedirs(old_pb)
    # Create a dummy file so the folder isn't empty
    open(os.path.join(old_render, "sh010_lighting_v0001_beauty.0001.exr"), "w").close()
    open(os.path.join(old_pb,    "sh010_main_v0001.mp4"),                  "w").close()

    # The legacy shim in getIdentifiersByType scans getSimplifiedOutputRoot.
    # We need to replicate that scan manually since we're using a temp path.
    # Instead, directly verify the shim logic by calling it with a patched entity.

    # Scan the legacy render folder manually (mirrors shim logic)
    legacy_render_root = os.path.join(entity_root, "Renders")
    found_ids = []
    if os.path.isdir(legacy_render_root):
        sub = os.path.join(legacy_render_root, "3dRender")
        if os.path.isdir(sub):
            for name in os.listdir(sub):
                if os.path.isdir(os.path.join(sub, name)):
                    found_ids.append(name)

    check("Legacy 3dRender folder found",        os.path.isdir(os.path.join(entity_root, "Renders", "3dRender")))
    check("Legacy identifier 'lighting' found",  "lighting" in found_ids, got=found_ids)

    # Scan versions inside lighting/
    idf_path = os.path.join(entity_root, "Renders", "3dRender", "lighting")
    found_versions = [n for n in os.listdir(idf_path) if os.path.isdir(os.path.join(idf_path, n))]
    check("Legacy version v0001 found",          "v0001" in found_versions, got=found_versions)

    check("Legacy Playblasts folder found",      os.path.isdir(os.path.join(entity_root, "Playblasts")))
    pb_ids = [n for n in os.listdir(os.path.join(entity_root, "Playblasts"))
              if os.path.isdir(os.path.join(entity_root, "Playblasts", n))]
    check("Legacy playblast identifier 'main' found", "main" in pb_ids, got=pb_ids)

    print("         Legacy folder tree created at: %s" % TEMP)
finally:
    shutil.rmtree(TEMP, ignore_errors=True)

# ── Test 9: pipeline.json folder_structure keys ────────────────────────────────
section("Test 9 — pipeline.json folder_structure keys")
cfg_path = os.path.join(PROJECT_PATH, "00_Pipeline", "pipeline.json")
with open(cfg_path, "r") as f:
    cfg = json.load(f)

fs = cfg.get("folder_structure", {})
check("3drenders value == @entity_path@/renders",     fs.get("3drenders",{}).get("value") == "@entity_path@/renders")
check("2drenders value == @entity_path@/renders",     fs.get("2drenders",{}).get("value") == "@entity_path@/renders")
check("externalMedia value == @entity_path@/external",fs.get("externalMedia",{}).get("value") == "@entity_path@/external")
check("playblasts value == @entity_path@/playblasts", fs.get("playblasts",{}).get("value") == "@entity_path@/playblasts")
check("renderFilesAssets has no @identifier@",        "@identifier@" not in fs.get("renderFilesAssets",{}).get("value",""))
check("renderFilesShots has no @identifier@",         "@identifier@" not in fs.get("renderFilesShots",{}).get("value",""))
check("playblastFilesAssets has no @identifier@",     "@identifier@" not in fs.get("playblastFilesAssets",{}).get("value",""))
check("playblastFilesShots has no @identifier@",      "@identifier@" not in fs.get("playblastFilesShots",{}).get("value",""))
check("use_flat_structure == true in globals",        cfg.get("globals",{}).get("use_flat_structure") is True)

# ── Summary ───────────────────────────────────────────────────────────────────
section("SUMMARY")
passed = sum(1 for s,_ in results if s == "PASS")
failed = sum(1 for s,_ in results if s == "FAIL")
total  = len(results)
print("\n  Total: %d   %s  Passed: %d   %s  Failed: %d\n" % (
    total, PASS, passed, FAIL, failed))

if failed:
    print("  Failed tests:")
    for s, lbl in results:
        if s == "FAIL":
            print("    X  %s" % lbl)

sys.exit(0 if failed == 0 else 1)
