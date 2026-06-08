# Custom Patches

All changes made to the original Prism Pipeline codebase.

---

## Projects.validateFolderStructure()
**File:** `Scripts/PrismUtils/Projects.py`

Strips `@identifier@` requirement from render/playblast keys when
`use_flat_structure = true` in project config, preventing false-positive
"project structure is invalid" popups.

---

## ProjectSettings.validateFolderWidget()
**File:** `Scripts/ProjectSettings.py`

Same flat-mode fix applied to the UI layer so the red border does not
appear on 3D Renders / 2D Renders / External Media / Playblasts fields.

---

## ProjectSettings.isValidStructure()
**File:** `Scripts/ProjectSettings.py`

Delegates to `validateFolderStructure()` instead of calling
`validateFolderKey()` directly, so the Save button is not blocked when
flat-mode templates are in use.

---

## MediaManager.getVideoReader()
**File:** `Scripts/PrismUtils/MediaManager.py`

Falls back to `_getImageIOFfmpegReader()` when `imageio` cannot be
imported (e.g. 3ds Max Python has no `numpy`).

---

## MediaManager._getImageIOFfmpegReader()
**File:** `Scripts/PrismUtils/MediaManager.py`  
**Status:** New function

Numpy-free video reader built on `imageio_ffmpeg.read_frames()`.
Implements the same API used by `getPixmapFromVideoPath()`:
- `reader.get_data(index)` → raw RGB bytes
- `reader.count_frames()` → int
- `reader._meta["size"]` → (width, height)
- `reader._meta["fps"]` → float

Fixes MP4 preview inside 3ds Max.

---

## MediaManager.playMediaInExternalPlayer()
**File:** `Scripts/PrismUtils/MediaManager.py`

When no external player is configured, opens the file with the OS
default application instead of showing an error popup.
- Windows: `os.startfile()`
- macOS: `open`
- Linux: `xdg-open`

---

## PathManager.getSimplifiedOutputRoot()
**File:** `Scripts/PrismUtils/PathManager.py`

Location-aware output root:
- `global` / `local` → `<project>/Output/<stage>/<entity>`
- Rendering (flat) → `<RenderingRoot>/<entity>` (no `Output/<stage>`)

---

## PathManager.getRenderProductBasePaths()
**File:** `Scripts/PrismUtils/PathManager.py`

Calls `os.path.expandvars()` on every render path so environment
variables such as `%RENDER_ROOT%` are resolved at runtime.

---

## PathManager.isSimplifiedArtistWorkflowEnabled()
**File:** `Scripts/PrismUtils/PathManager.py`

Reads `use_flat_structure` from the per-project config instead of a
hardcoded value. Defaults to `True` when the key is absent.

---

## PrismCore._convertFlatRenderPath()
**File:** `Scripts/PrismCore.py`  
**Status:** New function

Converts paths between a flat Rendering location and Global/Local when
the directory structures differ (flat has no `Output/<stage>` prefix).
