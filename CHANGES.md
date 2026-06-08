# Dev-Prism-Pipeline — سجل التعديلات

> **الإصدار:** feature/flat-render-structure  
> **تاريخ آخر تحديث:** يونيو 2026

---

## الفكرة العامة

المشروع ده نسخة مخصصة من [Prism Pipeline](https://prism-pipeline.com/) مصممة لاستوديو 3ds Max + Vray.
الهدف الأساسي: جعل مسار الـ **Rendering** يخزن الملفات بـ **flat structure**:

```
\\SERVER\Rendering\<project>\<entity>\renders\v0001\
```

بدل البنية الافتراضية:
```
<project>\Output\04-Cameras\<entity>\Renders\3dRender\<identifier>\v0001\
```

---

## الملفات المعدّلة

### 1. `Scripts/PrismUtils/Projects.py`

#### `validateFolderStructure()` — سطر 1548

**المشكلة:** الـ validator الأصلي كان يطلب `@identifier@` في مسارات الـ renders — لكن في الـ flat mode مفيش `@identifier@` في المسار.

**التعديل:** قبل الـ validation، لو `use_flat_structure = true` في الـ project config، بيشيل `identifier` من قائمة `requires` للـ keys دي:
- `3drenders`
- `2drenders`
- `externalMedia`
- `playblasts`

```python
_flatMode = bool(self.core.getConfig("globals", "use_flat_structure", config="project"))
_flatKeys = {"3drenders", "2drenders", "externalMedia", "playblasts"}
# strips "identifier" from requires before validation
```

---

### 2. `Scripts/ProjectSettings.py`

#### `validateFolderWidget()` — سطر 2024

**المشكلة:** الـ UI كان يعرض **red border** على fields الـ 3D Renders / 2D Renders / External Media / Playblasts لأنه كان بيستدعي `validateFolderKey()` مباشرة بدون الـ flat-mode fix.

**التعديل:** نفس منطق `validateFolderStructure` — بيشيل `identifier` من `requires` قبل validation الـ UI.

#### `isValidStructure()` — سطر 1025

**المشكلة:** كانت بتمنع الـ **Save** لو في validation errors على الـ flat fields.

**التعديل:** دلوقتي بتفوّض لـ `validateFolderStructure()` اللي فيها الـ flat fix، بدل ما تستدعي `validateFolderKey()` مباشرة.

---

### 3. `Scripts/PrismUtils/MediaManager.py`

#### `getVideoReader()` — سطر 281

**المشكلة:** داخل 3ds Max مفيش `numpy` في الـ Python environment، فـ `imageio` كان بيفشل تحميله بصمت، وبيرجع صورة checkerboard بدل الـ MP4 preview.

**التعديل:**
```python
imageio = self.getImageIO()
if imageio is not None:
    return imageio.get_reader(filepath, "ffmpeg")   # الطريق الأصلي (numpy متاح)

# Fallback: numpy-free reader
return self._getImageIOFfmpegReader(filepath)
```

#### `_getImageIOFfmpegReader()` — سطر 302 (جديد بالكامل)

قارئ فيديو خفيف بيستخدم `imageio_ffmpeg.read_frames()` مباشرة — لا يحتاج `numpy`.

| API | الوصف |
|-----|-------|
| `reader.get_data(index)` | يرجع raw RGB bytes للـ frame |
| `reader.count_frames()` | يرجع عدد الـ frames |
| `reader._meta["size"]` | `(width, height)` |
| `reader._meta["fps"]` | معدل الإطارات |

**تفاصيل تقنية:**
- يستخدم `IMAGEIO_FFMPEG_EXE` env var بدل `ffmpeg_exe` parameter (مش موجود في v0.4.9)
- `count_frames()`: يستخدم `re.findall` على stderr بدل `re.search` (يأخذ آخر قيمة لـ `frame=`)
- `count_frames()`: يستخدم `"nul"` بدل `os.devnull` على Windows

#### `playMediaInExternalPlayer()` — سطر 1397

**المشكلة:** لما مفيش external media player configured، كان بيظهر popup error.

**التعديل:** يفتح الملف بالـ default application:
- **Windows:** `os.startfile()`
- **macOS:** `subprocess.Popen(["open", path])`
- **Linux:** `subprocess.Popen(["xdg-open", path])`

---

### 4. `Scripts/PrismUtils/PathManager.py`

#### `isSimplifiedArtistWorkflowEnabled()` — سطر 64

بيقرأ `use_flat_structure` من الـ project config بدل hardcoded value.
- لو الـ key مش موجود → يرجع `True` (flat mode as default)

#### `getSimplifiedOutputRoot()` — سطر 132

**الجديد:** بيفرق بين الـ locations:

| Location | المسار المُنشأ |
|----------|--------------|
| `global` أو `local` | `<project>/Output/<stage>/<entity>` |
| `Rendering` (flat) | `<RenderingRoot>/<entity>` مباشرة |

```python
if self._isFlatRenderLocation(location):
    # flat: بدون Output/<stage>
    return os.path.join(projectPath, sequence, shot)
else:
    # standard
    return os.path.join(projectPath, "Output", self.simplifiedShotStage, sequence, shot)
```

#### `getRenderProductBasePaths()` — سطر 812

**الجديد:** `os.path.expandvars()` على كل الـ render paths — بيحل `%RENDER_ROOT%` و أي env vars تانية.

```python
render_paths[path] = os.path.normpath(os.path.expandvars(render_paths[path]))
```

---

### 5. `Scripts/PrismUtils/MediaProducts.py`

#### `getSimplifiedMediaBasePath()` — سطر 75

بيبني المسار الكامل للـ media حسب الـ location:

| `mediaType` | المسار |
|-------------|--------|
| `3drenders` أو `2drenders` | `<root>/renders/` |
| `externalMedia` | `<root>/external/` |
| `playblasts` | `<root>/playblasts/` |

ملاحظة: `3drenders` و `2drenders` بيشتركوا في نفس folder الـ `renders/` — الفرق بينهم في وجود AOV subfolders (3D) أو ملفات مباشرة في الـ version folder (2D).

#### `getIdentifiersByType()` — سطر 236

في الـ flat mode:
- `"renders"` → يظهر دايماً (3D + 2D)
- `"playblasts"` → يظهر دايماً
- `"external"` → يظهر لو فيه محتوى

---

### 6. `Scripts/PrismCore.py`

#### `_convertFlatRenderPath()` — جديد

يحوّل بين الـ locations لما البنية مختلفة:

| من | إلى | العملية |
|----|-----|---------|
| Flat Rendering | Global | يضيف `Output/<stage>` — يتحقق من disk لتحديد asset أو shot |
| Global | Flat Rendering | يشيل `Output/<stage>` |
| Flat ← Flat | أي location | استبدال مباشر للـ base path |

---

### 7. `Presets/Projects/Visions/00_Pipeline/pipeline.json`

#### globals

أُضيف:
```json
"use_flat_structure": true
```

يفعّل الـ flat structure mode للـ Visions project template.

#### render_paths

```json
"render_paths": {
    "Rendering": "\\\\172.18.20.12\\Rendering\\@project_name@"
}
```

> **ملاحظة للـ multi-machine setup:** استبدل الـ IP بـ `%RENDER_ROOT%\\@project_name@` وحدد `RENDER_ROOT` كـ environment variable على كل جهاز:
> ```cmd
> setx RENDER_ROOT "\\172.18.20.12\Rendering"
> ```

---

## Architecture — كيف تعمل الأجزاء مع بعض

```
pipeline.json
  └─ globals.use_flat_structure = true
       │
       ├─► PathManager.isSimplifiedArtistWorkflowEnabled()
       │       └─► getSimplifiedOutputRoot(location="Rendering")
       │               └─► يبني flat path: <root>/<entity>/renders
       │
       ├─► Projects.validateFolderStructure()
       │       └─► يتجاهل @identifier@ لـ {3drenders, 2drenders, externalMedia, playblasts}
       │
       ├─► ProjectSettings.validateFolderWidget()  [UI red borders]
       │       └─► نفس منطق validateFolderStructure
       │
       └─► ProjectSettings.isValidStructure()  [حماية الـ Save]
               └─► يفوّض لـ validateFolderStructure()
```

```
3ds Max بدون numpy
  └─► MediaManager.getImageIO() = None
          └─► getVideoReader()
                  └─► _getImageIOFfmpegReader()  [numpy-free]
                          └─► imageio_ffmpeg.read_frames()
                                  └─► _IffmpegReader.get_data(0)
                                          └─► bytes → QImage(bytes, w, h, 3*w, Format_RGB888)
```

---

## Tests

| الملف | عدد الاختبارات | ما يغطيه |
|-------|----------------|----------|
| `test_mp4_media_player.py` | 47 | MP4 pipeline كامل |
| `test_flat_structure.py` | — | flat path resolution |
| `test_media_player_locations.py` | — | location-aware media paths |

**تشغيل الاختبارات:**
```cmd
cd C:\Users\Hossam.Saber\Desktop\DEV-Prism\v2\Dev-prism-pipeline
Python313\python.exe test_mp4_media_player.py
```

---

## مشكلات تم حلها

| المشكلة | السبب | الحل |
|---------|-------|------|
| "The project structure is invalid" | `validateFolderKey` يطلب `@identifier@` | `validateFolderStructure` تتجاهله في flat mode |
| Red borders في Project Settings | `validateFolderWidget` يستدعي `validateFolderKey` مباشرة | نفس الـ flat-mode fix في `validateFolderWidget` |
| Media Browser فارغ | EntityWidget كان يحدد Rendering كـ default location | تم الـ revert |
| MP4 مش شغال في 3ds Max | `imageio` يحتاج `numpy` — مش موجود في 3ds Max | `_IffmpegReader` fallback بدون numpy |
| فتح MP4 بدون media player | كان يظهر error popup | `os.startfile()` fallback |
| `ffmpeg_exe` parameter error | `imageio_ffmpeg` v0.4.9 مش بيقبل الـ parameter | استخدام `IMAGEIO_FFMPEG_EXE` env var |
| `count_frames()` يرجع 0 | `re.search` يأخذ أول match (`frame= 0`) | `re.findall` يأخذ آخر match |

---

## ملاحظات مهمة للمطور

1. **`use_flat_structure`** لازم يكون موجود في `globals` في الـ `pipeline.json` الخاص بالـ project (مش الـ preset).

2. **`_flatKeys`** محددة في **3 أماكن** — لو احتجت تضيف key جديد لازم تحدثهم كلهم:
   - `Projects.validateFolderStructure()` (line 1556)
   - `ProjectSettings.validateFolderWidget()` (line 2030)
   - `MediaProducts.getSimplifiedMediaBasePath()` (logic)

3. **Rendering location** = أي location مش `"global"` أو `"local"`. الـ check في `_isFlatRenderLocation()`.

4. **`imageio_ffmpeg` version = 0.4.9** — لا تستخدم `ffmpeg_exe` parameter (مش موجود).

5. الـ **3D Renders و 2D Renders** بيتشاركوا نفس folder الـ `renders/` — الفرق في وجود AOV subdirectories.
