# Prism Pipeline - onProjectCreated Hook
# ──────────────────────────────────────────────────────────────────────────────
# INSTALL:
#   Project Tab → Hooks → onProjectCreated → paste this code
#   OR save as:  {ProjectRoot}\00_Pipeline\Hooks\onProjectCreated.py
#
# HOW PRISM CALLS HOOKS:
#   - The function MUST be named  main(*args, **kwargs)
#   - kwargs["core"]              → Prism core object
#   - kwargs["core"].projectName  → new project name  (e.g. "Example_Project")
#   - kwargs["core"].projectPath  → full path to new project root
# ──────────────────────────────────────────────────────────────────────────────

import os
import logging

logger = logging.getLogger(__name__)

# ── Network shares – a sub-folder named after the project will be created here ─
NETWORK_BASE_PATHS = [
    r"\\172.18.20.12\Project Run",
    r"\\172.18.20.12\Rendering",
    r"\\172.18.20.12\M&P",
]

# ── Entry point ────────────────────────────────────────────────────────────────

def main(*args, **kwargs):
    """
    Prism executes this function when a new project is created.
    kwargs["core"].projectName  holds the new project's name.
    """

    core = kwargs.get("core")

    # ── 1. Get the new project name ────────────────────────────────────────────
    project_name = _get_project_name(core, kwargs)

    if not project_name:
        msg = (
            "onProjectCreated hook:\n"
            "Could not read the new project name.\n"
            "Network folders were NOT created.\n\n"
            f"kwargs keys: {list(kwargs.keys())}"
        )
        logger.warning(msg)
        _popup(core, msg, title="Create Folders - Error", severity="warning")
        return

    logger.info("onProjectCreated -- creating folders for: %s", project_name)

    # ── 2. Create the 3 network folders ───────────────────────────────────────
    created, failed = [], []

    for base in NETWORK_BASE_PATHS:
        target = os.path.join(base, project_name)
        try:
            if os.path.isdir(target):
                created.append(target + "  (already existed)")
            else:
                os.makedirs(target)
                created.append(target)
                logger.info("Created: %s", target)
        except OSError as exc:
            failed.append((target, str(exc)))
            logger.error("Failed: %s -- %s", target, exc)

    # ── 3. Show result popup ───────────────────────────────────────────────────
    lines = [f"Project:  {project_name}", ""]

    if created:
        lines.append("Network folders created:")
        lines += [f"  OK   {p}" for p in created]

    if failed:
        lines.append("")
        lines.append("FAILED to create:")
        lines += [f"  XX   {p}\n       Error: {e}" for p, e in failed]

    msg = "\n".join(lines)
    logger.info(msg)
    _popup(
        core, msg,
        title="Network Folders - " + ("FAILED" if failed else "Done"),
        severity="warning" if failed else "info",
    )


# ── Helpers ────────────────────────────────────────────────────────────────────

def _get_project_name(core, kwargs):
    """
    Try every known location where Prism stores the new project name.
    """

    # 1. Direct kwarg  (some Prism versions pass it explicitly)
    for key in ("projectName", "project_name", "name"):
        val = kwargs.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()

    # 2. projectPath kwarg  →  extract last folder component
    for key in ("projectPath", "project_path", "path"):
        val = kwargs.get(key)
        if isinstance(val, str) and val.strip():
            name = _folder_name(val)
            if name:
                return name

    # 3. core.projectName  (standard Prism 2.x attribute)
    if core is not None:
        val = getattr(core, "projectName", None)
        if isinstance(val, str) and val.strip():
            return val.strip()

    # 4. core.projectPath  →  extract last folder component
    if core is not None:
        val = getattr(core, "projectPath", None)
        if isinstance(val, str) and val.strip():
            name = _folder_name(val)
            if name:
                return name

    # 5. core.getProjectName() / core.getProjectPath()
    if core is not None:
        for method in ("getProjectName", "getProjectPath", "getCurrentProject"):
            fn = getattr(core, method, None)
            if callable(fn):
                try:
                    val = fn()
                    if isinstance(val, str) and val.strip():
                        name = _folder_name(val) or val.strip()
                        if name:
                            return name
                except Exception:
                    pass

    return None


def _folder_name(path):
    """Return the last meaningful folder name from a path string."""
    SKIP = {
        "00_Pipeline", "01_Assets", "02_Shots",
        "03_Dailies", "04_Renders", "05_Deliverables", "06_Archive",
    }
    path = path.strip().rstrip("/\\")
    parts = path.replace("\\", "/").split("/")
    parts = [p for p in parts if p]
    for part in reversed(parts):
        if part not in SKIP:
            return part
    return None


def _popup(core, message, title="Prism Hook", severity="info"):
    if core is None:
        return
    try:
        core.popup(message, title=title, severity=severity)
    except Exception:
        try:
            core.popup(message, title=title)
        except Exception:
            pass
