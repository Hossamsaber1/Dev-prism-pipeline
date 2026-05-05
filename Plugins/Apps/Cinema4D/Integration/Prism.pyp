import os
import sys

import c4d


def fixPythonDlls():
    base = os.path.dirname(sys.executable)
    if sys.version_info[1] == 10:
        dllDir = base + "/resource/modules/python/libs/python310.win64.framework/dlls"
        os.add_dll_directory(dllDir)
    elif sys.version_info[1] == 11:
        dllDir = base + "/resource/modules/python/libs/win64/dlls"
        os.add_dll_directory(dllDir)


def prismInit():
    prismRoot = os.getenv("PRISM_ROOT")
    if not prismRoot:
        prismRoot = PRISMROOT

    scriptDir = os.path.join(prismRoot, "Scripts")

    if scriptDir not in sys.path:
        sys.path.append(scriptDir)

    import PrismCore
    from qtpy.QtWidgets import QApplication

    qapp = QApplication.instance()
    if qapp is None:
        qapp = QApplication(sys.argv)

    prismArgs = []
    if os.path.basename(sys.executable) == "Commandline.exe":
        prismArgs.append("noUI")

    pcore = PrismCore.PrismCore(app="Cinema4D", prismArgs=prismArgs)
    return pcore


fixPythonDlls()
pcore = prismInit()


def PluginMessage(id, data):
    pcore.appPlugin.pluginMessage(id, data)


class PrismSaveScene(c4d.plugins.CommandData):
    def Execute(self, doc):
        pcore.saveScene()
        return True

class PrismSaveComment(c4d.plugins.CommandData):
    def Execute(self, doc):
        pcore.saveWithComment()
        return True

class PrismProjectBrowser(c4d.plugins.CommandData):
    def Execute(self, doc):
        pcore.projectBrowser()
        return True

class PrismStateManager(c4d.plugins.CommandData):
    def Execute(self, doc):
        pcore.stateManager()
        return True

class PrismSettings(c4d.plugins.CommandData):
    def Execute(self, doc):
        pcore.prismSettings()
        return True


c4d.plugins.RegisterCommandPlugin(1063247, "Save Version", 0, None, "Save the current scene as a new version", PrismSaveScene())
c4d.plugins.RegisterCommandPlugin(1063248, "Save Comment", 0, None, "Save the current scene as a new version with a comment", PrismSaveComment())
c4d.plugins.RegisterCommandPlugin(1063249, "Project Browser", 0, None, "Open the Prism Project Browser", PrismProjectBrowser())
c4d.plugins.RegisterCommandPlugin(1063250, "State Manager", 0, None, "Open the Prism State Manager", PrismStateManager())
c4d.plugins.RegisterCommandPlugin(1063251, "Settings", 0, None, "Open the Prism Settings", PrismSettings())
