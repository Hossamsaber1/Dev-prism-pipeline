# Dev-prism-pipeline

A customized [Prism Pipeline](https://prism-pipeline.com/) (v2.1) tailored for a 3ds Max + Vray studio workflow.

---

## Features

- **Flat render structure**: Rendering location stores files at `<RenderingRoot>/<entity>/renders/v0001` (no `Output/<stage>` prefix), keeping the network server clean.
- **MP4 playblast preview**: Works inside 3ds Max without requiring `numpy` (uses `imageio_ffmpeg` fallback).
- **OS-default media player fallback**: Opens media with the system default if no external player is configured.
- **Project structure validation**: Correctly handles flat-mode templates without false "invalid project" popups.

---

## Setup on a new machine

### 1. Clone the repository

```cmd
git clone https://github.com/Hossamsaber1/Dev-prism-pipeline.git
cd Dev-prism-pipeline
```

### 2. Download and install the runtime (gitignored binaries)

Download the latest `runtime-vX.X.zip` from the [GitHub Releases](https://github.com/Hossamsaber1/Dev-prism-pipeline/releases) page and extract it into the repo root. It contains:

| Folder | Contents |
|--------|----------|
| `Python313/` | Embedded Python 3.13 runtime |
| `PythonLibs/` | All Python dependencies (PySide2, imageio, imageio_ffmpeg, …) |
| `Tools/FFmpeg/` | FFmpeg binary used for video preview |

### 3. Set the render path environment variable (once per machine)

The path to the shared rendering server is **not** stored in the repo. Set it once as a Windows environment variable:

```cmd
setx RENDER_ROOT "\\172.18.20.12\Rendering"
```

> On a different network or local test machine, point it to any accessible folder:
> ```cmd
> setx RENDER_ROOT "D:\LocalRendering"
> ```

After setting the variable, **restart any open terminals or applications** for it to take effect.

### 4. Run Prism

```cmd
Tools\prism_gui_with_console.bat
```

---

## Running tests

```cmd
cd tests
python test_mp4_media_player.py    # 47 tests — full MP4 pipeline
python test_flat_structure.py      # flat path resolution
python test_media_player_locations.py  # location-aware media paths
```

> Tests use Prism's bundled Python at `Python313/python.exe`.

---

## Branch strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable — never commit directly, always via PR |
| `feature/*` | New features |
| `fix/*` | Bug fixes |

---

## Key config files

| File | Purpose |
|------|---------|
| `Presets/Projects/Visions/00_Pipeline/pipeline.json` | Project settings, folder structure, render paths |
| `Scripts/PrismUtils/PathManager.py` | Path resolution logic (flat vs standard) |
| `Scripts/PrismUtils/MediaManager.py` | Video reader, external player |
| `Scripts/PrismUtils/MediaProducts.py` | Media discovery, identifiers, versions |
