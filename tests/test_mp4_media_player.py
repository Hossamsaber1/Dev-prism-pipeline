# -*- coding: utf-8 -*-
# test_mp4_media_player.py
# Verifies that MP4 files are correctly discovered, routed, and renderable
# through the Prism media-player pipeline for both Global and Rendering locations.
# Project-agnostic: builds a full temp project tree; works for any future project.

import os, sys, shutil, tempfile, traceback

PRISM_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PRISM_ROOT, "Scripts"))
sys.path.insert(0, os.path.join(PRISM_ROOT, "PythonLibs", "Python3"))
sys.path.insert(0, os.path.join(PRISM_ROOT, "PythonLibs", "CrossPlatform"))

try:
    from qtpy import QtWidgets
    _qapp = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
except Exception:
    pass

import PrismCore

# ── helpers ──────────────────────────────────────────────────────────────────
PASS = "[PASS]"
FAIL = "[FAIL]"
INFO = "[INFO]"
results = []

def check(label, condition, got=None, expected=None):
    tag = PASS if condition else FAIL
    results.append(("PASS" if condition else "FAIL", label))
    line = "%s  %s" % (tag, label)
    if not condition:
        if expected is not None:
            line += "\n         expected : %s" % expected
        if got is not None:
            line += "\n         got      : %s" % got
    print(line)

def section(title):
    print("\n%s  -- %s --" % (INFO, title))

# ── bootstrap core ───────────────────────────────────────────────────────────
section("Init Prism (noUI)")
try:
    core = PrismCore.create(app="Standalone", prismArgs=["noUI", "noSplash"])
    check("PrismCore created", core is not None)
except Exception as e:
    print(FAIL + "  PrismCore init: %s" % e)
    traceback.print_exc()
    sys.exit(1)

PROJECT_PATH = os.path.join(PRISM_ROOT, "Presets", "Projects", "Visions")
try:
    core.changeProject(PROJECT_PATH)
    check("Visions project loaded", bool(core.projectPath))
except Exception as e:
    print(FAIL + "  changeProject: %s" % e)
    traceback.print_exc()

# ── build temp directory tree ────────────────────────────────────────────────
TEMP = tempfile.mkdtemp(prefix="prism_mp4_test_")

try:
    # ── Shared entity definition ─────────────────────────────────────────────
    entity = {
        "type": "shot",
        "entityType": "shot",
        "sequence": "sq010",
        "shot": "sh010",
        "project_path": TEMP,
    }

    SHOT_STAGE = core.paths.simplifiedShotStage       # e.g. "04-Cameras"
    SHOT_ROOT  = os.path.join(TEMP, "Output", SHOT_STAGE, "sq010", "sh010")

    # ── Global location: flat structure ──────────────────────────────────────
    # <project>/Output/<stage>/sq010/sh010/playblasts/v0001/sh010_Animation_v0001.mp4
    GLOBAL_PB_VERSION = os.path.join(SHOT_ROOT, "playblasts", "v0001")
    GLOBAL_MP4        = os.path.join(GLOBAL_PB_VERSION, "sh010_Animation_v0001.mp4")
    os.makedirs(GLOBAL_PB_VERSION, exist_ok=True)
    with open(GLOBAL_MP4, "wb") as f:
        # Minimal valid MP4 magic bytes (ftyp box) – enough for extension checks
        f.write(b"\x00\x00\x00\x18ftypisom\x00\x00\x00\x00isomiso2mp41")

    # ── Rendering location: flat structure (no Output/<stage>) ───────────────
    RENDERING_ROOT    = os.path.join(TEMP, "Rendering", "project-test-mp4")
    REND_SHOT_ROOT    = os.path.join(RENDERING_ROOT, "sq010", "sh010")
    REND_PB_VERSION   = os.path.join(REND_SHOT_ROOT, "playblasts", "v0001")
    REND_MP4          = os.path.join(REND_PB_VERSION, "sh010_Animation_v0001.mp4")
    os.makedirs(REND_PB_VERSION, exist_ok=True)
    with open(REND_MP4, "wb") as f:
        f.write(b"\x00\x00\x00\x18ftypisom\x00\x00\x00\x00isomiso2mp41")

    # ── Also create a 3D render EXR for comparison ────────────────────────────
    GLOBAL_EXR_VERSION = os.path.join(SHOT_ROOT, "renders", "v0001", "beauty")
    os.makedirs(GLOBAL_EXR_VERSION, exist_ok=True)
    with open(os.path.join(GLOBAL_EXR_VERSION, "sh010_v0001.0001.exr"), "wb") as f:
        f.write(b"\x76\x2f\x31\x01")  # EXR magic

    # =========================================================================
    # SECTION 1: videoFormats list contains .mp4
    # =========================================================================
    section("1 — MediaManager videoFormats contains .mp4")
    check(".mp4 in videoFormats",  ".mp4"  in core.media.videoFormats,  got=core.media.videoFormats)
    check(".mov in videoFormats",  ".mov"  in core.media.videoFormats,  got=core.media.videoFormats)
    check(".mp4 in supportedFormats", ".mp4" in core.media.supportedFormats, got=core.media.supportedFormats)

    # =========================================================================
    # SECTION 2: filterValidMediaFiles accepts MP4
    # =========================================================================
    section("2 — filterValidMediaFiles accepts .mp4")
    filtered = core.media.filterValidMediaFiles([GLOBAL_MP4, "/fake/file.xyz"])
    check("MP4 passes filterValidMediaFiles", GLOBAL_MP4 in filtered, got=filtered)
    check(".xyz rejected by filterValidMediaFiles", "/fake/file.xyz" not in filtered, got=filtered)

    # =========================================================================
    # SECTION 3: detectSequences treats single MP4 as non-sequence
    # =========================================================================
    section("3 — detectSequences: single MP4 is NOT an image sequence")
    seqs = core.media.detectSequences([GLOBAL_MP4])
    check("detectSequences returns entry for MP4", bool(seqs), got=seqs)
    if seqs:
        mp4_seq = list(seqs.values())[0]
        check("MP4 sequence has exactly 1 file", len(mp4_seq) == 1, got=mp4_seq)
        check("MP4 file retained in sequence", GLOBAL_MP4 in mp4_seq, got=mp4_seq)

    # =========================================================================
    # SECTION 4: getSimplifiedMediaBasePath — playblasts (global)
    # =========================================================================
    section("4 — getSimplifiedMediaBasePath playblasts (global)")
    pb_base_global = core.mediaProducts.getSimplifiedMediaBasePath(entity, TEMP, "playblasts", location="global")
    pb_base_global_n = pb_base_global.replace("\\", "/")
    check("Global playblast base ends with /playblasts", pb_base_global_n.endswith("/playblasts"), got=pb_base_global)
    check("Global playblast base contains Output/<stage>",
          "/Output/%s/" % SHOT_STAGE in pb_base_global_n, got=pb_base_global)

    # =========================================================================
    # SECTION 5: getSimplifiedMediaBasePath — playblasts (flat rendering)
    # =========================================================================
    section("5 — getSimplifiedMediaBasePath playblasts (Rendering / flat)")
    entity_rend = dict(entity, project_path=RENDERING_ROOT)
    pb_base_rend = core.mediaProducts.getSimplifiedMediaBasePath(entity_rend, RENDERING_ROOT, "playblasts", location="Rendering")
    pb_base_rend_n = pb_base_rend.replace("\\", "/")
    check("Flat playblast base ends with /playblasts", pb_base_rend_n.endswith("/playblasts"), got=pb_base_rend)
    check("Flat playblast base does NOT contain /Output/", "/Output/" not in pb_base_rend_n, got=pb_base_rend)

    # =========================================================================
    # SECTION 6: getFilesFromContext — global location returns MP4
    # =========================================================================
    section("6 — getFilesFromContext global playblast returns MP4 path")
    ctx_global = {
        "type": "shot",
        "sequence": "sq010",
        "shot": "sh010",
        "mediaType": "playblasts",
        "identifier": "playblasts",
        "version": "v0001",
        "path": GLOBAL_PB_VERSION,
        "paths": [GLOBAL_PB_VERSION],
        "locations": {"global": GLOBAL_PB_VERSION},
        "project_path": TEMP,
    }
    files_global = core.mediaProducts.getFilesFromContext(ctx_global)
    check("getFilesFromContext returns files (global)", bool(files_global), got=files_global)
    if files_global:
        mp4_found = any(f.lower().endswith(".mp4") for f in files_global)
        check("At least one .mp4 file in results (global)", mp4_found, got=files_global)
        check("Correct MP4 path returned (global)",
              any(os.path.normpath(GLOBAL_MP4) == os.path.normpath(f) for f in files_global),
              got=files_global, expected=GLOBAL_MP4)

    # =========================================================================
    # SECTION 7: getFilesFromContext — flat Rendering location returns MP4
    # =========================================================================
    section("7 — getFilesFromContext flat Rendering playblast returns MP4 path")
    ctx_rend = {
        "type": "shot",
        "sequence": "sq010",
        "shot": "sh010",
        "mediaType": "playblasts",
        "identifier": "playblasts",
        "version": "v0001",
        "path": REND_PB_VERSION,
        "paths": [REND_PB_VERSION],
        "locations": {"Rendering": REND_PB_VERSION},
        "project_path": RENDERING_ROOT,
    }
    files_rend = core.mediaProducts.getFilesFromContext(ctx_rend)
    check("getFilesFromContext returns files (Rendering)", bool(files_rend), got=files_rend)
    if files_rend:
        mp4_found_rend = any(f.lower().endswith(".mp4") for f in files_rend)
        check("At least one .mp4 file in results (Rendering)", mp4_found_rend, got=files_rend)
        check("Correct MP4 path returned (Rendering)",
              any(os.path.normpath(REND_MP4) == os.path.normpath(f) for f in files_rend),
              got=files_rend, expected=REND_MP4)

    # =========================================================================
    # SECTION 8: getAOVsFromVersion — playblasts return empty (no AOVs)
    # =========================================================================
    section("8 — getAOVsFromVersion: playblasts have no AOVs")
    aovs = core.mediaProducts.getAOVsFromVersion(ctx_global)
    check("AOVs for playblast = [] (correct)", aovs == [], got=aovs, expected=[])

    # Patch render paths so both locations resolve to our temp tree.
    # getVersionsFromContext uses locationData = getRenderProductBasePaths()
    # and ignores context["project_path"], so we must inject the correct roots.
    orig_render_paths = core.paths.getRenderProductBasePaths

    def patched_render_paths_both():
        paths = orig_render_paths()
        paths["global"]     = TEMP           # redirect global → our temp project
        paths["Rendering"]  = RENDERING_ROOT  # redirect Rendering → our flat tree
        return paths

    core.paths.getRenderProductBasePaths = patched_render_paths_both

    # =========================================================================
    # SECTION 9: getVersionsFromContext — finds v0001 (global)
    # =========================================================================
    section("9 — getVersionsFromContext finds v0001 playblast (global)")
    versions_ctx = {
        "type": "shot",
        "sequence": "sq010",
        "shot": "sh010",
        "mediaType": "playblasts",
        "identifier": "playblasts",
        "project_path": TEMP,
        "path": pb_base_global,
        "location": "global",
        "locations": {"global": pb_base_global},
    }
    try:
        versions = core.mediaProducts.getVersionsFromContext(versions_ctx)
        check("getVersionsFromContext returns versions (global)", bool(versions), got=versions)
        if versions:
            ver_names = [v.get("version") for v in versions]
            check("v0001 found in versions (global)", "v0001" in ver_names, got=ver_names)
    except Exception as e:
        print(FAIL + "  getVersionsFromContext (global) raised: %s" % e)
        traceback.print_exc()
        results.append(("FAIL", "getVersionsFromContext global"))

    # =========================================================================
    # SECTION 10: getVersionsFromContext — finds v0001 (Rendering / flat)
    # =========================================================================
    section("10 — getVersionsFromContext finds v0001 playblast (Rendering)")
    versions_ctx_rend = {
        "type": "shot",
        "sequence": "sq010",
        "shot": "sh010",
        "mediaType": "playblasts",
        "identifier": "playblasts",
        "project_path": RENDERING_ROOT,
        "path": pb_base_rend,
        "location": "Rendering",
        "locations": {"Rendering": pb_base_rend},
    }
    try:
        versions_rend = core.mediaProducts.getVersionsFromContext(versions_ctx_rend)
        check("getVersionsFromContext returns versions (Rendering)", bool(versions_rend), got=versions_rend)
        if versions_rend:
            ver_names_rend = [v.get("version") for v in versions_rend]
            check("v0001 found in versions (Rendering)", "v0001" in ver_names_rend, got=ver_names_rend)
    except Exception as e:
        print(FAIL + "  getVersionsFromContext (Rendering) raised: %s" % e)
        traceback.print_exc()
        results.append(("FAIL", "getVersionsFromContext Rendering"))

    # Restore after sections 9 & 10
    core.paths.getRenderProductBasePaths = orig_render_paths

    # =========================================================================
    # SECTION 11: EXR renders also work (regression guard)
    # =========================================================================
    section("11 — EXR 3D render regression guard (global)")
    ctx_exr = {
        "type": "shot",
        "sequence": "sq010",
        "shot": "sh010",
        "mediaType": "3drenders",
        "identifier": "renders",
        "aov": "beauty",
        "version": "v0001",
        "path": GLOBAL_EXR_VERSION,
        "paths": [GLOBAL_EXR_VERSION],
        "locations": {"global": os.path.join(SHOT_ROOT, "renders", "v0001")},
        "project_path": TEMP,
    }
    files_exr = core.mediaProducts.getFilesFromContext(ctx_exr)
    check("EXR getFilesFromContext returns files", bool(files_exr), got=files_exr)
    if files_exr:
        exr_found = any(f.lower().endswith(".exr") for f in files_exr)
        check("At least one .exr file returned", exr_found, got=files_exr)

    # =========================================================================
    # SECTION 12: MP4 file magic-bytes / extension recognised by MediaManager
    # =========================================================================
    section("12 — MediaManager extension check for player routing")
    ext_mp4 = os.path.splitext(GLOBAL_MP4)[1].lower()
    check("MP4 extension is video format",   ext_mp4 in core.media.videoFormats, got=ext_mp4)
    check("MP4 extension is supported format", ext_mp4 in core.media.supportedFormats, got=ext_mp4)

    ext_exr = ".exr"
    check("EXR is NOT a video format",  ext_exr not in core.media.videoFormats, got=ext_exr)
    check("EXR IS a supported format",  ext_exr in core.media.supportedFormats, got=ext_exr)

    # =========================================================================
    # SECTION 13: generatePlayblastPath produces valid .mp4 path
    # =========================================================================
    section("13 — generatePlayblastPath produces .mp4 path")
    try:
        pb_path = core.mediaProducts.generatePlayblastPath(
            entity=entity,
            task="Animation",
            extension=".mp4",
            version="v0001",
            location="global",
        )
        if pb_path:
            p = pb_path.replace("\\", "/")
            check("Playblast path ends with .mp4",    p.endswith(".mp4"),           got=p)
            check("Playblast path contains /playblasts/", "/playblasts/" in p,     got=p)
            check("Playblast path contains /v0001/",  "/v0001/" in p,              got=p)
            print("         >> %s" % p)
        else:
            print(FAIL + "  generatePlayblastPath returned empty")
            results.append(("FAIL", "generatePlayblastPath"))
    except Exception as e:
        print(FAIL + "  generatePlayblastPath raised: %s" % e)
        traceback.print_exc()
        results.append(("FAIL", "generatePlayblastPath exception"))

    # =========================================================================
    # SECTION 14: generatePlayblastPath — flat Rendering location
    # =========================================================================
    section("14 — generatePlayblastPath flat Rendering location produces .mp4")
    try:
        pb_path_rend = core.mediaProducts.generatePlayblastPath(
            entity=entity,
            task="Animation",
            extension=".mp4",
            version="v0001",
            location="Rendering",
        )
        if pb_path_rend:
            p = pb_path_rend.replace("\\", "/")
            check("Flat playblast path ends with .mp4",    p.endswith(".mp4"), got=p)
            check("Flat playblast path has /playblasts/",  "/playblasts/" in p, got=p)
            check("Flat playblast path has NO /Output/",   "/Output/" not in p, got=p)
            print("         >> %s" % p)
        else:
            print(FAIL + "  generatePlayblastPath (Rendering) returned empty")
            results.append(("FAIL", "generatePlayblastPath Rendering"))
    except Exception as e:
        print(FAIL + "  generatePlayblastPath (Rendering) raised: %s" % e)
        traceback.print_exc()
        results.append(("FAIL", "generatePlayblastPath Rendering exception"))

    # =========================================================================
    # SECTION 15: Full chain — identifiers → versions → files (global)
    # =========================================================================
    section("15 — Full chain: identifiers -> versions -> files (global MP4)")
    try:
        # Patch so getVersionsFromContext finds our temp tree as "global"
        _orig15 = core.paths.getRenderProductBasePaths
        def _patched15():
            p = _orig15(); p["global"] = TEMP; return p
        core.paths.getRenderProductBasePaths = _patched15

        identifiers = core.mediaProducts.getIdentifiersByType(entity=entity, locations=["global"])
        pb_ids = identifiers.get("playblast", [])
        check("playblast identifiers returned", bool(pb_ids), got=list(identifiers.keys()))

        if pb_ids:
            idf = pb_ids[0]
            idf["project_path"] = TEMP
            idf["path"] = pb_base_global
            idf["locations"] = {"global": pb_base_global}
            versions2 = core.mediaProducts.getVersionsFromContext(idf)
            check("versions from identifier (global)", bool(versions2), got=versions2)

            if versions2:
                v = versions2[0]
                files2 = core.mediaProducts.getFilesFromContext(v)
                check("files from version (global)", bool(files2), got=files2)
                if files2:
                    check("MP4 in final file list (global)",
                          any(f.lower().endswith(".mp4") for f in files2), got=files2)

        core.paths.getRenderProductBasePaths = _orig15
    except Exception as e:
        print(FAIL + "  Full chain (global) raised: %s" % e)
        traceback.print_exc()
        results.append(("FAIL", "Full chain global"))
        try: core.paths.getRenderProductBasePaths = _orig15
        except Exception: pass

    # =========================================================================
    # SECTION 16: Full chain — identifiers → versions → files (Rendering flat)
    # =========================================================================
    section("16 — Full chain: identifiers -> versions -> files (Rendering flat MP4)")
    try:
        # Patch getRenderProductBasePaths to include our temp Rendering location
        orig_render_paths = core.paths.getRenderProductBasePaths

        def patched_render_paths():
            paths = orig_render_paths()
            paths["Rendering"] = RENDERING_ROOT
            return paths

        core.paths.getRenderProductBasePaths = patched_render_paths

        identifiers_rend = core.mediaProducts.getIdentifiersByType(entity=entity, locations=["Rendering"])
        pb_ids_rend = identifiers_rend.get("playblast", [])
        check("playblast identifiers returned (Rendering)", bool(pb_ids_rend), got=list(identifiers_rend.keys()))

        if pb_ids_rend:
            idf_r = pb_ids_rend[0]
            idf_r["project_path"] = RENDERING_ROOT
            idf_r["path"] = pb_base_rend
            idf_r["locations"] = {"Rendering": pb_base_rend}
            versions_r2 = core.mediaProducts.getVersionsFromContext(idf_r)
            check("versions from identifier (Rendering)", bool(versions_r2), got=versions_r2)

            if versions_r2:
                v_r = versions_r2[0]
                files_r2 = core.mediaProducts.getFilesFromContext(v_r)
                check("files from version (Rendering)", bool(files_r2), got=files_r2)
                if files_r2:
                    check("MP4 in final file list (Rendering)",
                          any(f.lower().endswith(".mp4") for f in files_r2), got=files_r2)

        # Restore
        core.paths.getRenderProductBasePaths = orig_render_paths

    except Exception as e:
        print(FAIL + "  Full chain (Rendering) raised: %s" % e)
        traceback.print_exc()
        results.append(("FAIL", "Full chain Rendering"))
        try:
            core.paths.getRenderProductBasePaths = orig_render_paths
        except Exception:
            pass

finally:
    shutil.rmtree(TEMP, ignore_errors=True)

# =========================================================================
# SECTION 17: playMediaInExternalPlayer OS-default fallback (no player configured)
# =========================================================================
section("17 — playMediaInExternalPlayer fallback when no player configured")

import tempfile as _tf, platform as _platform

_tmp2 = _tf.mkdtemp(prefix="prism_play_test_")
try:
    _mp4 = os.path.join(_tmp2, "test_fallback.mp4")
    with open(_mp4, "wb") as f:
        f.write(b"\x00\x00\x00\x18ftypisom\x00\x00\x00\x00isomiso2mp41")

    # Patch getExternalMediaPlayer to return None (simulating unconfigured state)
    _orig_get_player = core.media.getExternalMediaPlayer
    core.media.getExternalMediaPlayer = lambda name=None: None

    # Patch os.startfile to capture the call without actually launching anything
    import builtins as _builtins
    _startfile_calls = []
    _orig_startfile = getattr(os, "startfile", None)
    if _platform.system() == "Windows":
        os.startfile = lambda p: _startfile_calls.append(p)

    # Patch subprocess.Popen for non-Windows platforms
    _popen_calls = []
    import subprocess as _subprocess
    _orig_popen = _subprocess.Popen
    class _FakePopen:
        def __init__(self, args, **kwargs): _popen_calls.append(args)
    _subprocess.Popen = _FakePopen

    try:
        core.media.playMediaInExternalPlayer(_mp4)
    except Exception as e:
        print(FAIL + "  playMediaInExternalPlayer raised: %s" % e)
        traceback.print_exc()
        results.append(("FAIL", "playMediaInExternalPlayer fallback raised"))
    finally:
        # Restore
        core.media.getExternalMediaPlayer = _orig_get_player
        _subprocess.Popen = _orig_popen
        if _platform.system() == "Windows" and _orig_startfile:
            os.startfile = _orig_startfile
        elif _platform.system() == "Windows":
            del os.startfile

    if _platform.system() == "Windows":
        check("os.startfile called with MP4 path (fallback)",
              bool(_startfile_calls) and any(_mp4 in str(p) for p in _startfile_calls),
              got=_startfile_calls, expected=_mp4)
    else:
        check("subprocess.Popen called with open/xdg-open (fallback)",
              bool(_popen_calls),
              got=_popen_calls)

    # Also verify: when player IS configured, it uses the configured path
    _prog = r"C:\fake\player.exe"
    _orig_get_player2 = core.media.getExternalMediaPlayer
    core.media.getExternalMediaPlayer = lambda name=None: {"path": _prog, "framePattern": False}
    _popen_calls2 = []
    _subprocess.Popen = lambda args, **kw: _popen_calls2.append(args)
    try:
        core.media.playMediaInExternalPlayer(_mp4)
    except Exception:
        pass
    finally:
        core.media.getExternalMediaPlayer = _orig_get_player2
        _subprocess.Popen = _orig_popen

    check("configured player path used when set",
          bool(_popen_calls2) and any(
              isinstance(a, (list, tuple)) and any(
                  os.path.normpath(_prog) == os.path.normpath(p) for p in a if isinstance(p, str)
              )
              for a in _popen_calls2
          ),
          got=_popen_calls2)

finally:
    shutil.rmtree(_tmp2, ignore_errors=True)

# ── Summary ───────────────────────────────────────────────────────────────────
section("SUMMARY")
passed = sum(1 for s, _ in results if s == "PASS")
failed = sum(1 for s, _ in results if s == "FAIL")
total  = len(results)

print("\n  Total: %d   %s Passed: %d   %s Failed: %d\n" % (total, PASS, passed, FAIL, failed))

if failed:
    print("  Failed tests:")
    for s, lbl in results:
        if s == "FAIL":
            print("    X  %s" % lbl)

sys.exit(0 if failed == 0 else 1)
