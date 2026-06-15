# Architecture

---

## Overview

```
pipeline.json
└── globals.use_flat_structure = true
        │
        ├── PathManager.isSimplifiedArtistWorkflowEnabled()
        │       └── getSimplifiedOutputRoot(location)
        │               ├── Rendering  →  <root>/<entity>/renders/
        │               └── Global     →  <project>/Output/<stage>/<entity>/renders/
        │
        ├── Projects.validateFolderStructure()
        │       └── strips @identifier@ for flat keys → no invalid-project popup
        │
        ├── ProjectSettings.validateFolderWidget()
        │       └── strips @identifier@ for flat keys → no red border in UI
        │
        ├── ProjectSettings.isValidStructure()
        │       └── delegates to validateFolderStructure() → Save is not blocked
        │
        └── MediaProducts.getSimplifiedMediaBasePath()
                └── routes mediaType to correct subfolder
                        ├── 3drenders / 2drenders  →  renders/
                        ├── playblasts             →  playblasts/
                        └── externalMedia          →  external/
```

---

## MP4 Preview — 3ds Max

```
getVideoReader(filepath)
│
├── getImageIO()  ──► numpy available  →  imageio.get_reader()  [standard path]
│
└── numpy NOT available (3ds Max)
        └── _getImageIOFfmpegReader(filepath)
                └── _IffmpegReader
                        ├── imageio_ffmpeg.read_frames()  [no numpy needed]
                        └── get_data(index) → bytes
                                └── QImage(bytes, w, h, 3*w, Format_RGB888)
```

---

## Path Conversion Between Locations

```
_convertFlatRenderPath(path, target)
│
├── Flat → Global   strips Output/<stage>, probes disk to detect asset vs shot
├── Global → Flat   adds Output/<stage> prefix
└── Flat → Flat     direct base-path replacement
```

---

## Locations

| Name | Base Path | Structure |
|------|-----------|-----------|
| `global` | `<project>/` | Standard — includes `Output/<stage>` |
| `local` | local project copy | Standard — includes `Output/<stage>` |
| `Rendering` | `%RENDER_ROOT%/<project>/` | Flat — no `Output/<stage>` |

`%RENDER_ROOT%` is set once per machine:
```cmd
setx RENDER_ROOT "\\SERVER\Rendering"
```

---

## Config Key

`pipeline.json` → `globals.use_flat_structure` (bool)

| Value | Behaviour |
|-------|-----------|
| `true` | Flat mode — Rendering location uses `<root>/<entity>/renders/` |
| `false` | Standard mode — all locations use `Output/<stage>` |
| missing | Defaults to `true` |

---

## Removed Integrations

The following DCC integrations were removed from this fork:
- Maya
- Nuke
- Cinema 4D
