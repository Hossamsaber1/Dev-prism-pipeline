# -*- coding: utf-8 -*-
"""
test_media_player_locations.py
==============================
Verifies that the Media Player and Preview pipeline work correctly for
BOTH Global and Rendering locations (flat structure).

Covers every function in the read path:
  - getSimplifiedEntityDataFromPath
  - getSimplifiedMediaData
  - getSimplifiedMediaBasePath / getSimplifiedOutputRoot
  - getIdentifiersByType
  - getVersionsFromContext
  - getFilesFromContext  (file discovery used by Media Browser)
  - getRenderProductDataFromFilepath  (used by preview)
  - getMediaDataFromVersionFolder     (used by preview)
  - convertPath  (bidirectional)

All tests are project-agnostic: they create a temporary project tree on disk
so the same suite runs correctly for EVERY future project.
"""

import os
import sys
import shutil
import tempfile
import traceback
import unittest.mock as mock

# ── Bootstrap ────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "Scripts"))
sys.path.insert(0, os.path.join(ROOT, "PythonLibs", "Python3"))
sys.path.insert(0, os.path.join(ROOT, "PythonLibs", "CrossPlatform"))

try:
    from qtpy import QtWidgets
    _app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
except Exception:
    pass

import PrismCore

# ── Result tracking ──────────────────────────────────────────────────────────
_results = []

def _ok(label, cond, got=None, expected=None):
    tag = "[PASS]" if cond else "[FAIL]"
    _results.append(("PASS" if cond else "FAIL", label))
    msg = "%s  %s" % (tag, label)
    if not cond:
        if expected is not None:
            msg += "\n         expected : %s" % expected
        if got is not None:
            msg += "\n         got      : %s" % got
    print(msg)

def _section(title):
    print("\n[INFO]  -- %s --" % title)

def _skip(label, reason):
    print("[SKIP]  %s  (%s)" % (label, reason))

# ── Fixtures ─────────────────────────────────────────────────────────────────
SHOT_STAGE  = "04-Cameras"
ASSET_STAGE = "01-Modeling"
SEQ         = "still"
SHOT        = "cam-02"
ASSET_CAT   = "Characters"
ASSET_NAME  = "Hero"
VERSION     = "v0001"
AOV         = "beauty"
MEDIATYPE   = "3drenders"

SHOT_ENTITY = {
    "type": "shot", "entityType": "shot",
    "sequence": SEQ, "shot": SHOT,
}
ASSET_ENTITY = {
    "type": "asset", "entityType": "asset",
    "asset_path": "%s/%s" % (ASSET_CAT, ASSET_NAME),
    "asset": ASSET_NAME,
}


def _make_render_file(path):
    """Create a dummy EXR-like file so disk probes succeed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(b"\x76\x2f\x31\x01" + b"\x00" * 100)  # fake EXR magic


def _build_project_tree(base):
    """
    Create:
      <base>/
        Output/04-Cameras/still/cam-02/   (global shot entity dir)
        Output/01-Modeling/Characters/Hero/  (global asset entity dir)

    Returns (prj_path, rend_path) where both are inside <base>.
    """
    prj  = os.path.join(base, "project")
    rend = os.path.join(base, "rendering")

    # ---- Global shot renders (Output/<stage>/<seq>/<shot>/renders/<ver>/<aov>/)
    g_shot_render = os.path.join(
        prj, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION, AOV
    )
    _make_render_file(os.path.join(g_shot_render, "frame.0001.exr"))

    # ---- Global shot playblast (Output/<stage>/<seq>/<shot>/playblasts/<ver>/)
    g_shot_pb = os.path.join(
        prj, "Output", SHOT_STAGE, SEQ, SHOT, "playblasts", VERSION
    )
    _make_render_file(os.path.join(g_shot_pb, "shot.mp4"))

    # ---- Global asset renders
    g_asset_render = os.path.join(
        prj, "Output", ASSET_STAGE, ASSET_CAT, ASSET_NAME, "renders", VERSION, AOV
    )
    _make_render_file(os.path.join(g_asset_render, "frame.0001.exr"))

    # ---- Flat rendering shot renders (<rend>/<seq>/<shot>/renders/<ver>/<aov>/)
    r_shot_render = os.path.join(
        rend, SEQ, SHOT, "renders", VERSION, AOV
    )
    _make_render_file(os.path.join(r_shot_render, "frame.0001.exr"))

    # ---- Flat rendering shot playblasts
    r_shot_pb = os.path.join(
        rend, SEQ, SHOT, "playblasts", VERSION
    )
    _make_render_file(os.path.join(r_shot_pb, "shot.mp4"))

    # ---- Flat rendering asset renders
    r_asset_render = os.path.join(
        rend, ASSET_CAT, ASSET_NAME, "renders", VERSION, AOV
    )
    _make_render_file(os.path.join(r_asset_render, "frame.0001.exr"))

    return prj, rend


def _build_legacy_rendering_tree(base):
    """
    Create old Output/<stage> structure INSIDE the rendering location.
    Used for backward-compat tests.
    """
    rend = os.path.join(base, "rendering_legacy")
    old_path = os.path.join(
        rend, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION, AOV
    )
    _make_render_file(os.path.join(old_path, "frame.0001.exr"))
    return rend


# ── Core setup ───────────────────────────────────────────────────────────────
_section("Initialising Prism")
try:
    core = PrismCore.create(app="Standalone", prismArgs=["noUI", "noSplash"])
    _ok("PrismCore created", core is not None)
except Exception as exc:
    print("[FAIL]  PrismCore init: %s" % exc)
    traceback.print_exc()
    sys.exit(1)

VISIONS = os.path.join(ROOT, "Presets", "Projects", "Visions")
try:
    core.changeProject(VISIONS)
    _ok("Project loaded", bool(core.projectPath))
except Exception as exc:
    print("[FAIL]  changeProject: %s" % exc)
    traceback.print_exc()


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURE BUILD
# ─────────────────────────────────────────────────────────────────────────────
TMP   = tempfile.mkdtemp(prefix="prism_media_test_")
PRJ, REND = _build_project_tree(TMP)
REND_LEGACY = _build_legacy_rendering_tree(TMP)

FAKE_PATHS = {"global": PRJ, "rendering": REND}

# Helpers that run every test inside the patched environment
def _with_fake(fn):
    with mock.patch.object(core.paths, "getRenderProductBasePaths", return_value=FAKE_PATHS):
        with mock.patch.object(core, "projectPath", PRJ):
            return fn()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — getSimplifiedOutputRoot
# ─────────────────────────────────────────────────────────────────────────────
_section("1 — getSimplifiedOutputRoot")

def _test_output_root():
    # Global
    g_shot  = core.paths.getSimplifiedOutputRoot(SHOT_ENTITY,  projectPath=PRJ,  location=None)
    g_asset = core.paths.getSimplifiedOutputRoot(ASSET_ENTITY, projectPath=PRJ,  location=None)
    # Flat rendering
    r_shot  = core.paths.getSimplifiedOutputRoot(SHOT_ENTITY,  projectPath=REND, location="rendering")
    r_asset = core.paths.getSimplifiedOutputRoot(ASSET_ENTITY, projectPath=REND, location="rendering")

    _ok("Global  shot  has Output/%s" % SHOT_STAGE,
        ("Output" in g_shot and SHOT_STAGE in g_shot), got=g_shot)
    _ok("Global  asset has Output/%s" % ASSET_STAGE,
        ("Output" in g_asset and ASSET_STAGE in g_asset), got=g_asset)
    _ok("Flat    shot  has NO Output",
        ("Output" not in r_shot), got=r_shot)
    _ok("Flat    asset has NO Output",
        ("Output" not in r_asset), got=r_asset)
    _ok("Flat    shot  ends with cam-02",
        r_shot.replace("\\", "/").endswith("still/cam-02"), got=r_shot)
    _ok("Flat    asset ends with Characters/Hero",
        r_asset.replace("\\", "/").endswith("Characters/Hero"), got=r_asset)

_with_fake(_test_output_root)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — getSimplifiedMediaBasePath
# ─────────────────────────────────────────────────────────────────────────────
_section("2 — getSimplifiedMediaBasePath")

def _test_media_base():
    g_base = core.mediaProducts.getSimplifiedMediaBasePath(
        SHOT_ENTITY, PRJ, "3drenders", location=None)
    r_base = core.mediaProducts.getSimplifiedMediaBasePath(
        SHOT_ENTITY, REND, "3drenders", location="rendering")
    pb_g   = core.mediaProducts.getSimplifiedMediaBasePath(
        SHOT_ENTITY, PRJ, "playblasts", location=None)
    pb_r   = core.mediaProducts.getSimplifiedMediaBasePath(
        SHOT_ENTITY, REND, "playblasts", location="rendering")

    _ok("Global  3drenders ends with /renders",
        g_base.replace("\\","/").endswith("/renders"), got=g_base)
    _ok("Flat    3drenders ends with /renders",
        r_base.replace("\\","/").endswith("/renders"), got=r_base)
    _ok("Global  3drenders has Output",
        "Output" in g_base, got=g_base)
    _ok("Flat    3drenders has NO Output",
        "Output" not in r_base, got=r_base)
    _ok("Global  playblasts ends with /playblasts",
        pb_g.replace("\\","/").endswith("/playblasts"), got=pb_g)
    _ok("Flat    playblasts has NO Output",
        "Output" not in pb_r, got=pb_r)

_with_fake(_test_media_base)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — getSimplifiedEntityDataFromPath
# ─────────────────────────────────────────────────────────────────────────────
_section("3 — getSimplifiedEntityDataFromPath")

def _test_entity_from_path():
    # Global paths
    g_shot_file = os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION, AOV, "frame.0001.exr")
    g_asset_file = os.path.join(PRJ, "Output", ASSET_STAGE, ASSET_CAT, ASSET_NAME, "renders", VERSION, AOV, "frame.0001.exr")
    # Flat rendering paths
    r_shot_file  = os.path.join(REND, SEQ, SHOT, "renders", VERSION, AOV, "frame.0001.exr")
    r_asset_file = os.path.join(REND, ASSET_CAT, ASSET_NAME, "renders", VERSION, AOV, "frame.0001.exr")

    eg = core.paths.getSimplifiedEntityDataFromPath(g_shot_file)
    ea = core.paths.getSimplifiedEntityDataFromPath(g_asset_file)
    er = core.paths.getSimplifiedEntityDataFromPath(r_shot_file)
    era= core.paths.getSimplifiedEntityDataFromPath(r_asset_file)

    _ok("Global  shot  entity type == shot",   eg.get("type") == "shot",  got=eg)
    _ok("Global  shot  sequence correct",      eg.get("sequence") == SEQ, got=eg)
    _ok("Global  shot  shot correct",          eg.get("shot") == SHOT,    got=eg)
    _ok("Global  asset entity type == asset",  ea.get("type") == "asset", got=ea)
    _ok("Global  asset asset_path correct",    ea.get("asset") == ASSET_NAME, got=ea)

    _ok("Flat    shot  entity type == shot",   er.get("type") == "shot",  got=er)
    _ok("Flat    shot  sequence correct",      er.get("sequence") == SEQ, got=er)
    _ok("Flat    shot  shot correct",          er.get("shot") == SHOT,    got=er)
    _ok("Flat    asset entity type == asset",  era.get("type") == "asset", got=era)
    _ok("Flat    asset asset correct",         era.get("asset") == ASSET_NAME, got=era)

_with_fake(_test_entity_from_path)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — getSimplifiedMediaData  (media classification)
# ─────────────────────────────────────────────────────────────────────────────
_section("4 — getSimplifiedMediaData  (media classification for preview)")

def _test_media_data():
    g_file = os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION, AOV, "frame.0001.exr")
    r_file = os.path.join(REND, SEQ, SHOT, "renders", VERSION, AOV, "frame.0001.exr")

    dg = core.mediaProducts.getSimplifiedMediaData(g_file)
    dr = core.mediaProducts.getSimplifiedMediaData(r_file)

    _ok("Global  shot  mediaData not empty", bool(dg), got=dg)
    _ok("Global  shot  version == v0001",    dg.get("version") == VERSION, got=dg)
    _ok("Global  shot  type == shot",        dg.get("type") == "shot", got=dg)
    _ok("Global  shot  mediaType == 3drenders", dg.get("mediaType") in ("3drenders","2drenders"), got=dg)

    _ok("Flat    shot  mediaData not empty", bool(dr), got=dr)
    _ok("Flat    shot  version == v0001",    dr.get("version") == VERSION, got=dr)
    _ok("Flat    shot  type == shot",        dr.get("type") == "shot", got=dr)
    _ok("Flat    shot  mediaType == 3drenders", dr.get("mediaType") in ("3drenders","2drenders"), got=dr)

    # Playblast
    g_pb = os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "playblasts", VERSION, "shot.mp4")
    r_pb = os.path.join(REND, SEQ, SHOT, "playblasts", VERSION, "shot.mp4")
    dg_pb = core.mediaProducts.getSimplifiedMediaData(g_pb, mediaType="playblasts")
    dr_pb = core.mediaProducts.getSimplifiedMediaData(r_pb, mediaType="playblasts")

    _ok("Global  playblast mediaData not empty",       bool(dg_pb), got=dg_pb)
    _ok("Global  playblast mediaType == playblasts",   dg_pb.get("mediaType") == "playblasts", got=dg_pb)
    _ok("Flat    playblast mediaData not empty",       bool(dr_pb), got=dr_pb)
    _ok("Flat    playblast mediaType == playblasts",   dr_pb.get("mediaType") == "playblasts", got=dr_pb)

_with_fake(_test_media_data)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — getRenderProductDataFromFilepath  (used by preview classification)
# ─────────────────────────────────────────────────────────────────────────────
_section("5 — getRenderProductDataFromFilepath")

def _test_render_product_data():
    g_file = os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION, AOV, "frame.0001.exr")
    r_file = os.path.join(REND, SEQ, SHOT, "renders", VERSION, AOV, "frame.0001.exr")

    dg = core.mediaProducts.getRenderProductDataFromFilepath(g_file)
    dr = core.mediaProducts.getRenderProductDataFromFilepath(r_file)

    _ok("Global  shot  product data not empty", bool(dg), got=dg)
    _ok("Global  shot  version correct",        dg.get("version") == VERSION, got=dg)
    _ok("Global  shot  type == shot",           dg.get("type") == "shot", got=dg)

    _ok("Flat    shot  product data not empty", bool(dr), got=dr)
    _ok("Flat    shot  version correct",        dr.get("version") == VERSION, got=dr)
    _ok("Flat    shot  type == shot",           dr.get("type") == "shot", got=dr)

_with_fake(_test_render_product_data)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — getMediaDataFromVersionFolder  (used by preview info panel)
# ─────────────────────────────────────────────────────────────────────────────
_section("6 — getMediaDataFromVersionFolder")

def _test_version_folder_data():
    g_ver = os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION)
    r_ver = os.path.join(REND, SEQ, SHOT, "renders", VERSION)

    dg = core.mediaProducts.getMediaDataFromVersionFolder(g_ver)
    dr = core.mediaProducts.getMediaDataFromVersionFolder(r_ver)

    _ok("Global  version folder data not empty", bool(dg), got=dg)
    _ok("Global  version == v0001",              dg.get("version") == VERSION, got=dg)
    _ok("Global  type == shot",                  dg.get("type") == "shot", got=dg)

    _ok("Flat    version folder data not empty", bool(dr), got=dr)
    _ok("Flat    version == v0001",              dr.get("version") == VERSION, got=dr)
    _ok("Flat    type == shot",                  dr.get("type") == "shot", got=dr)

_with_fake(_test_version_folder_data)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — getIdentifiersByType  (Media Browser left panel)
# ─────────────────────────────────────────────────────────────────────────────
_section("7 — getIdentifiersByType  (Media Browser identifier panel)")

def _test_identifiers():
    # Global
    idfs_g = core.mediaProducts.getIdentifiersByType(
        dict(SHOT_ENTITY, project_path=PRJ)
    )
    all_g = [d["identifier"] for cat in idfs_g.values() for d in cat]

    # Flat rendering only
    idfs_r = core.mediaProducts.getIdentifiersByType(
        dict(SHOT_ENTITY, project_path=REND),
        locations=["rendering"]
    )
    all_r = [d["identifier"] for cat in idfs_r.values() for d in cat]

    _ok("Global  'renders' identifier found",    "renders"    in all_g, got=all_g)
    _ok("Global  'playblasts' identifier found", "playblasts" in all_g, got=all_g)
    _ok("Flat    'renders' identifier found",    "renders"    in all_r, got=all_r)
    _ok("Flat    'playblasts' identifier found", "playblasts" in all_r, got=all_r)

    # Check flat renders path has no Output
    flat_renders = [d for cat in idfs_r.values() for d in cat if d["identifier"] == "renders"]
    if flat_renders:
        _ok("Flat    renders path has no Output",
            "Output" not in flat_renders[0]["path"],
            got=flat_renders[0]["path"])
    else:
        _ok("Flat    renders entry found (path check)", False, got=all_r)

_with_fake(_test_identifiers)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — getVersionsFromContext  (Media Browser version list)
# ─────────────────────────────────────────────────────────────────────────────
_section("8 — getVersionsFromContext  (Media Browser version list)")

def _test_versions():
    # Build contexts as getIdentifiersByType would produce them
    g_ctx = dict(SHOT_ENTITY,
                 project_path=PRJ, identifier="renders",
                 mediaType="3drenders", location="global")
    r_ctx = dict(SHOT_ENTITY,
                 project_path=REND, identifier="renders",
                 mediaType="3drenders", location="rendering")

    vers_g = core.mediaProducts.getVersionsFromContext(g_ctx, locations=["global"])
    vers_r = core.mediaProducts.getVersionsFromContext(r_ctx, locations=["rendering"])

    vnames_g = [v.get("version") for v in vers_g]
    vnames_r = [v.get("version") for v in vers_r]

    _ok("Global  v0001 found in versions",  VERSION in vnames_g, got=vnames_g)
    _ok("Flat    v0001 found in versions",  VERSION in vnames_r, got=vnames_r)

    # Confirm flat version path has no Output
    if vers_r:
        vpath = vers_r[0].get("path", "")
        _ok("Flat    version path has no Output", "Output" not in vpath, got=vpath)
    else:
        _ok("Flat    at least one version returned", False, got=vers_r)

    # Playblast versions
    g_pb_ctx = dict(SHOT_ENTITY,
                    project_path=PRJ, identifier="playblasts",
                    mediaType="playblasts", location="global")
    r_pb_ctx = dict(SHOT_ENTITY,
                    project_path=REND, identifier="playblasts",
                    mediaType="playblasts", location="rendering")
    vers_g_pb = core.mediaProducts.getVersionsFromContext(g_pb_ctx, locations=["global"])
    vers_r_pb = core.mediaProducts.getVersionsFromContext(r_pb_ctx, locations=["rendering"])

    _ok("Global  playblast v0001 found",  VERSION in [v.get("version") for v in vers_g_pb], got=vers_g_pb)
    _ok("Flat    playblast v0001 found",  VERSION in [v.get("version") for v in vers_r_pb], got=vers_r_pb)

_with_fake(_test_versions)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9 — getFilesFromContext  (Media Player file discovery)
# ─────────────────────────────────────────────────────────────────────────────
_section("9 — getFilesFromContext  (Media Player file discovery)")

def _test_files_from_context():
    g_ver_path = os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION)
    r_ver_path = os.path.join(REND, SEQ, SHOT, "renders", VERSION)

    g_ctx = dict(SHOT_ENTITY,
                 project_path=PRJ, identifier="renders",
                 mediaType="3drenders", version=VERSION,
                 aov=AOV,
                 path=g_ver_path,
                 locations={"global": g_ver_path})
    r_ctx = dict(SHOT_ENTITY,
                 project_path=REND, identifier="renders",
                 mediaType="3drenders", version=VERSION,
                 aov=AOV,
                 path=r_ver_path,
                 locations={"rendering": r_ver_path})

    files_g = core.mediaProducts.getFilesFromContext(g_ctx)
    files_r = core.mediaProducts.getFilesFromContext(r_ctx)

    _ok("Global  getFilesFromContext returns files",     len(files_g) > 0, got=files_g)
    _ok("Global  file is frame.0001.exr",               any("frame.0001.exr" in f for f in files_g), got=files_g)
    _ok("Flat    getFilesFromContext returns files",     len(files_r) > 0, got=files_r)
    _ok("Flat    file is frame.0001.exr",               any("frame.0001.exr" in f for f in files_r), got=files_r)

    # Playblast file discovery
    g_pb_path = os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "playblasts", VERSION)
    r_pb_path = os.path.join(REND, SEQ, SHOT, "playblasts", VERSION)

    g_pb_ctx = dict(SHOT_ENTITY,
                    project_path=PRJ, identifier="playblasts",
                    mediaType="playblasts", version=VERSION,
                    path=g_pb_path,
                    locations={"global": g_pb_path})
    r_pb_ctx = dict(SHOT_ENTITY,
                    project_path=REND, identifier="playblasts",
                    mediaType="playblasts", version=VERSION,
                    path=r_pb_path,
                    locations={"rendering": r_pb_path})

    files_g_pb = core.mediaProducts.getFilesFromContext(g_pb_ctx)
    files_r_pb = core.mediaProducts.getFilesFromContext(r_pb_ctx)

    _ok("Global  playblast file found",  any("shot.mp4" in f for f in files_g_pb), got=files_g_pb)
    _ok("Flat    playblast file found",  any("shot.mp4" in f for f in files_r_pb), got=files_r_pb)

_with_fake(_test_files_from_context)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10 — convertPath  (bidirectional)
# ─────────────────────────────────────────────────────────────────────────────
_section("10 — convertPath  (bidirectional)")

def _test_convert_path():
    # --- Global -> Rendering ---
    g_shot_path = os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION)
    r_shot_path = core.convertPath(g_shot_path, "rendering")
    exp_r_shot  = os.path.normpath(os.path.join(REND, SEQ, SHOT, "renders", VERSION))

    _ok("convertPath global->rendering shot",
        os.path.normpath(r_shot_path) == exp_r_shot,
        got=r_shot_path, expected=exp_r_shot)
    _ok("convertPath global->rendering shot has NO Output",
        "Output" not in r_shot_path, got=r_shot_path)

    # --- Rendering -> Global (disk probe) ---
    r_in  = os.path.join(REND, SEQ, SHOT, "renders", VERSION)
    g_out = core.convertPath(r_in, "global")
    exp_g = os.path.normpath(os.path.join(PRJ, "Output", SHOT_STAGE, SEQ, SHOT, "renders", VERSION))

    _ok("convertPath rendering->global shot (disk probe)",
        os.path.normpath(g_out) == exp_g,
        got=g_out, expected=exp_g)
    _ok("convertPath rendering->global result has Output/%s" % SHOT_STAGE,
        SHOT_STAGE in g_out, got=g_out)

    # --- Asset: global -> rendering ---
    g_asset_path = os.path.join(PRJ, "Output", ASSET_STAGE, ASSET_CAT, ASSET_NAME, "renders", VERSION)
    r_asset_path = core.convertPath(g_asset_path, "rendering")
    exp_r_asset  = os.path.normpath(os.path.join(REND, ASSET_CAT, ASSET_NAME, "renders", VERSION))

    _ok("convertPath global->rendering asset",
        os.path.normpath(r_asset_path) == exp_r_asset,
        got=r_asset_path, expected=exp_r_asset)

    # --- Asset: rendering -> global (disk probe) ---
    r_asset_in = os.path.join(REND, ASSET_CAT, ASSET_NAME, "renders", VERSION)
    g_asset_out = core.convertPath(r_asset_in, "global")
    exp_g_asset = os.path.normpath(os.path.join(PRJ, "Output", ASSET_STAGE, ASSET_CAT, ASSET_NAME, "renders", VERSION))

    _ok("convertPath rendering->global asset (disk probe)",
        os.path.normpath(g_asset_out) == exp_g_asset,
        got=g_asset_out, expected=exp_g_asset)

    # --- Global stays unchanged when already global ---
    same = core.convertPath(g_shot_path, "global")
    _ok("convertPath global->global returns same path",
        os.path.normpath(same) == os.path.normpath(g_shot_path),
        got=same)

_with_fake(_test_convert_path)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 11 — Asset entity full round-trip
# ─────────────────────────────────────────────────────────────────────────────
_section("11 — Asset full round-trip (identifiers + versions + files)")

def _test_asset_round_trip():
    asset_entity_with_prj = dict(ASSET_ENTITY, project_path=REND)

    idfs_r = core.mediaProducts.getIdentifiersByType(
        asset_entity_with_prj, locations=["rendering"]
    )
    all_r = [d for cat in idfs_r.values() for d in cat if d["identifier"] == "renders"]
    _ok("Asset flat  renders identifier found", len(all_r) > 0, got=[d["identifier"] for cat in idfs_r.values() for d in cat])

    if all_r:
        idf_ctx = all_r[0]
        vers = core.mediaProducts.getVersionsFromContext(idf_ctx, locations=["rendering"])
        vnames = [v.get("version") for v in vers]
        _ok("Asset flat  version v0001 found", VERSION in vnames, got=vnames)

        if vers:
            v_ctx = dict(vers[0], aov=AOV)
            files = core.mediaProducts.getFilesFromContext(v_ctx)
            _ok("Asset flat  files found in version", len(files) > 0, got=files)
            _ok("Asset flat  frame.0001.exr present",
                any("frame.0001.exr" in f for f in files), got=files)

_with_fake(_test_asset_round_trip)


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 12 — Backward compat: old Output/<stage> content in Rendering
# ─────────────────────────────────────────────────────────────────────────────
_section("12 — Backward compat: old Output/<stage> in Rendering location")

def _test_legacy_flat():
    fake_paths_legacy = {"global": PRJ, "rendering": REND_LEGACY}
    with mock.patch.object(core.paths, "getRenderProductBasePaths", return_value=fake_paths_legacy):
        with mock.patch.object(core, "projectPath", PRJ):
            # getIdentifiersByType should surface the old content via legacy_flat shim
            idfs = core.mediaProducts.getIdentifiersByType(
                dict(SHOT_ENTITY, project_path=REND_LEGACY),
                locations=["rendering"]
            )
            legacy_entries = [d for cat in idfs.values() for d in cat if d.get("legacy_flat")]
            all_idfs = [d["identifier"] for cat in idfs.values() for d in cat]

            _ok("Legacy flat  renders identifier surfaced",
                any(d["identifier"] == "renders" for d in legacy_entries),
                got=all_idfs)

            if legacy_entries:
                lctx = next(d for d in legacy_entries if d["identifier"] == "renders")
                vers = core.mediaProducts.getVersionsFromContext(lctx, locations=["rendering"])
                vnames = [v.get("version") for v in vers]
                _ok("Legacy flat  version v0001 discovered", VERSION in vnames, got=vnames)

                if vers:
                    v_ctx = dict(vers[0], aov=AOV)
                    files = core.mediaProducts.getFilesFromContext(v_ctx)
                    _ok("Legacy flat  frame.0001.exr found",
                        any("frame.0001.exr" in f for f in files), got=files)

_test_legacy_flat()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 13 — Global unchanged (regression)
# ─────────────────────────────────────────────────────────────────────────────
_section("13 — Global paths completely unchanged (regression guard)")

def _test_global_regression():
    PRJ_REAL = os.path.normpath(core.projectPath)
    # These tests use the real Visions project — no mocking
    shot_entity_real = {
        "type": "shot", "entityType": "shot",
        "sequence": "sq010", "shot": "sh010",
    }
    root = core.paths.getSimplifiedOutputRoot(shot_entity_real, projectPath=PRJ_REAL, location=None)
    _ok("Real project  Output/%s present" % SHOT_STAGE,
        "Output" in root and SHOT_STAGE in root, got=root)
    _ok("Real project  location=None does NOT change root",
        "Output" in root, got=root)

    path_g = os.path.join(PRJ_REAL, "Output", SHOT_STAGE, "sq010", "sh010", "renders", "v0001")
    same = core.convertPath(path_g, "global")
    _ok("Global convertPath to global returns identical path",
        os.path.normpath(same) == os.path.normpath(path_g), got=same)

_test_global_regression()


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 14 — _isFlatRenderLocation helper
# ─────────────────────────────────────────────────────────────────────────────
_section("14 — _isFlatRenderLocation helper")

_ok("global   is NOT flat",    not core.paths._isFlatRenderLocation("global"))
_ok("local    is NOT flat",    not core.paths._isFlatRenderLocation("local"))
_ok("None     is NOT flat",    not core.paths._isFlatRenderLocation(None))
_ok("rendering IS  flat",       core.paths._isFlatRenderLocation("rendering"))
_ok("farm     IS  flat",        core.paths._isFlatRenderLocation("farm"))
_ok("custom   IS  flat",        core.paths._isFlatRenderLocation("my_custom_loc"))


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 15 — generateMediaProductPath writes to correct location
# ─────────────────────────────────────────────────────────────────────────────
_section("15 — generateMediaProductPath path correctness per location")

def _test_generate_path():
    # Global
    p_g = core.mediaProducts.generateMediaProductPath(
        entity=dict(SHOT_ENTITY, project_path=PRJ),
        task="Lighting", extension=".exr",
        version=VERSION, aov=AOV, mediaType="3drenders", location="global",
    )
    # Flat rendering
    p_r = core.mediaProducts.generateMediaProductPath(
        entity=dict(SHOT_ENTITY, project_path=REND),
        task="Lighting", extension=".exr",
        version=VERSION, aov=AOV, mediaType="3drenders", location="rendering",
    )

    _ok("Global  path has Output/%s" % SHOT_STAGE, SHOT_STAGE in (p_g or ""), got=p_g)
    _ok("Global  path under PRJ",   (p_g or "").startswith(PRJ), got=p_g)
    _ok("Flat    path has NO Output", "Output" not in (p_r or ""), got=p_r)
    _ok("Flat    path under REND",  (p_r or "").startswith(REND), got=p_r)
    _ok("Flat    path has /renders/", "/renders/" in (p_r or "").replace("\\","/"), got=p_r)
    _ok("Flat    path has /v0001/",   "/v0001/" in (p_r or "").replace("\\","/"), got=p_r)

_with_fake(_test_generate_path)


# ─────────────────────────────────────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────────────────────────────────────
shutil.rmtree(TMP, ignore_errors=True)


# ─────────────────────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
_section("SUMMARY")
passed = sum(1 for s, _ in _results if s == "PASS")
failed = sum(1 for s, _ in _results if s == "FAIL")
total  = len(_results)

print("\n  Total: %d    Passed: %d    Failed: %d\n" % (total, passed, failed))

if failed:
    print("  Failed tests:")
    for s, lbl in _results:
        if s == "FAIL":
            print("    X  %s" % lbl)

sys.exit(0 if failed == 0 else 1)
