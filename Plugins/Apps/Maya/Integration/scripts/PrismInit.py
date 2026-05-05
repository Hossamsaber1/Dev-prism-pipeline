import os
import sys


def prismInit(prismArgs=[]):
    prismRoot = os.getenv("PRISM_ROOT")
    if not prismRoot:
        raise Exception("PRISM_ROOT env var is not defined. Please reinstall the Prism integration")

    import maya.cmds as cmds
    if cmds.about(batch=True):
        try:
            from PySide6 import QtWidgets
        except:
            from PySide2 import QtWidgets

        qapp = QtWidgets.QApplication.instance()
        if not isinstance(qapp, QtWidgets.QApplication):
            print("Cannot create Prism instance because no QApplication exists. To load Prism you can create a QApplication before initilizing mayapy like this: import sys;from PySide2 import QtWidgets;QtWidgets.QApplication(sys.argv)")
            return

        if not qapp:
            QtWidgets.QApplication(sys.argv)

        prismArgs.append("noUI")

    scriptDir = os.path.join(prismRoot, "Scripts")

    if scriptDir not in sys.path:
        sys.path.append(scriptDir)

    import PrismCore
    global pcore
    pcore = PrismCore.PrismCore(app="Maya", prismArgs=prismArgs)
    return pcore
