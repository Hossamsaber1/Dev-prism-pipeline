import os
import sys


def prismInit(prismArgs=[]):
    if "hython" in os.path.basename(sys.executable).lower():
        if "noUI" not in prismArgs:
            prismArgs.append("noUI")

        from PySide2.QtWidgets import QApplication
        import hou
        QApplication.addLibraryPath(
            os.path.join(hou.text.expandString("$HFS"), "bin", "Qt_plugins")
        )
        if not QApplication.instance():
            QApplication(sys.argv)

    root = os.getenv("PRISM_ROOT", "")
    if not root:
        if not os.getenv("PRISM_STANDALONE_KARMA", ""):
            from PySide2 import QtWidgets
            QtWidgets.QMessageBox.warning(None, "Prism", "The environment variable \"PRISM_ROOT\" is not defined. Try to setup the Prism Houdini integration again from the DCC apps tab in the Prism User Settings.")

        return

    scriptPath = os.path.join(root, "Scripts")
    if scriptPath not in sys.path:
        sys.path.append(scriptPath)

    import PrismCore
    pcore = PrismCore.PrismCore(app="Houdini", prismArgs=prismArgs)
    return pcore


def createPrismCore():
    if os.getenv("PRISM_ENABLED") == "0":
        return
    
    try:
        import PySide2
    except:
        return

    global pcore
    pcore = prismInit()
