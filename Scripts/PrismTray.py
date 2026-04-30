# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


import os
import sys
import subprocess
import platform
import logging
import traceback
import time

if sys.version[0] == "3":
    sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    import PrismCore

import psutil
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


logger = logging.getLogger(__name__)


class PrismTray:
    def __init__(self, core: object) -> None:
        """
        Initialize the PrismTray.

        Args:
            core (object): The core Prism object.
        """
        self.core = core

        try:
            self.launching = False
            self.browserStarted = False
            self.createTrayIcon()
            self.trayIcon.show()
            self.startListener()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            QMessageBox.critical(
                self.core.messageParent,
                "Unknown Error",
                "initTray - %s - %s - %s" % (str(e), exc_type, exc_tb.tb_lineno),
            )

    def startListener(self) -> None:
        """
        Start the listener thread for tray events.
        """
        self.listenerThread = ListenerThread()
        self.listenerThread.dataReceived.connect(self.onDataReceived)
        self.listenerThread.errored.connect(self.core.writeErrorLog)
        self.listenerThread.start()

    def onDataReceived(self, data: object) -> None:
        """
        Handle data received from the listener thread.

        Args:
            data (object): The received data.
        """
        logger.warning("received data: %s" % data)
        if data == "openProjectBrowser":
            self.startBrowser()
        elif data.startswith("protocolHandler:"):
            url = data[len("protocolHandler:"):]
            self.core.protocolHandler(url)
        elif data == "close":
            self.exitTray()

    def createTrayIcon(self) -> None:
        """
        Create and configure the system tray icon and its menu.
        """
        try:
            self.trayIconMenu = QMenu(self.core.messageParent)
            self.browserAction = QAction(
                "Project Browser...",
                self.core.messageParent,
                triggered=self.startBrowser,
            )
            self.trayIconMenu.addAction(self.browserAction)

            self.settingsAction = QAction(
                "Settings...",
                self.core.messageParent,
                triggered=lambda: self.core.prismSettings(),
            )
            self.trayIconMenu.addAction(self.settingsAction)
            self.trayIconMenu.addSeparator()

            self.pDirAction = QAction(
                "Open Prism directory",
                self.core.messageParent,
                triggered=lambda: self.openFolder(location="Prism"),
            )
            self.trayIconMenu.addAction(self.pDirAction)
            self.prjDirAction = QAction(
                "Open project directory",
                self.core.messageParent,
                triggered=lambda: self.openFolder(location="Project"),
            )
            self.trayIconMenu.addAction(self.prjDirAction)
            self.trayIconMenu.addSeparator()
            self.restartAction = QAction(
                "Restart", self.core.messageParent, triggered=self.restartTray
            )
            self.trayIconMenu.addAction(self.restartAction)
            self.exitAction = QAction(
                "Exit", self.core.messageParent, triggered=self.exitTray
            )
            self.trayIconMenu.addAction(self.exitAction)

            self.core.callback(
                name="trayContextMenuRequested",
                args=[self, self.trayIconMenu],
            )

            self.trayIcon = QSystemTrayIcon()
            self.trayIcon.setContextMenu(self.trayIconMenu)
            self.trayIcon.setToolTip("Prism Tools")

            self.icon = QIcon(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "UserInterfacesPrism",
                    "p_tray.png",
                )
            )

            self.trayIcon.setIcon(self.icon)

            self.trayIcon.activated.connect(self.iconActivated)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            QMessageBox.critical(
                self.core.messageParent,
                "Unknown Error",
                "createTray - %s - %s - %s" % (str(e), exc_type, exc_tb.tb_lineno),
            )

    def iconActivated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """
        Handle tray icon activation events.

        Args:
            reason (QSystemTrayIcon.ActivationReason): The reason for activation.
        """
        try:
            if reason == QSystemTrayIcon.Trigger:
                self.browserStarted = False
                if (
                    platform.system() == "Darwin"
                    and reason != QSystemTrayIcon.DoubleClick
                ):
                    return

                if (
                    platform.system() == "Windows"
                    and reason == QSystemTrayIcon.DoubleClick
                ):
                    return

                results = self.core.callback(name="trayIconClicked", args=[self, reason])
                if not [r for r in results if r == "handled"]:
                    self.browserStarted = True
                    self.startBrowser()

            elif reason == QSystemTrayIcon.DoubleClick:
                if not self.browserStarted:
                    self.startBrowser()

            elif reason == QSystemTrayIcon.Context:
                self.core.callback(
                    name="openTrayContextMenu",
                    args=[self, self.trayIconMenu],
                )

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
        #   QMessageBox.critical(self.core.messageParent, "Unknown Error", "iconActivated - %s - %s - %s" % (str(e), exc_type, exc_tb.tb_lineno))

    def startBrowser(self) -> None:
        """
        Start the project browser window.
        """
        if self.launching:
            logger.debug("Launching in progress. Skipped opening Project Browser")
            return

        self.launching = True
        self.core.projectBrowser()
        self.launching = False
        return

    def openFolder(self, path: str = "", location: str = None) -> None:
        """
        Open a folder in the file explorer.

        Args:
            path (str): The path to open.
            location (str, optional): The location type ('Prism' or 'Project').
        """
        if location == "Prism":
            path = self.core.prismRoot
        elif location == "Project":
            curProject = self.core.getConfig("globals", "current project")
            if curProject is None:
                QMessageBox.warning(
                    self.core.messageParent,
                    "Open directory",
                    "No active project is set.",
                )
                return
            else:
                path = os.path.dirname(os.path.dirname(curProject))

        self.core.openFolder(path)

    def openSettings(self) -> None:
        """
        Open the Prism settings window.
        """
        self.core.prismSettings()

    def restartTray(self) -> None:
        """
        Restart the Prism tray application.
        """
        self.listenerThread.shutDown()

        pythonPath = self.core.getPythonPath(executable="Prism")
        filepath = os.path.join(self.core.prismRoot, "Scripts", "PrismTray.py")
        cmd = """start "" "%s" "%s" showSplash ignore_pid=%s""" % (pythonPath, filepath, os.getpid())
        subprocess.Popen(cmd, cwd=self.core.prismRoot, shell=True, env=self.core.startEnv)
        sys.exit(0)

    def exitTray(self) -> None:
        """
        Exit the Prism tray application.
        """
        if hasattr(self, "listenerThread"):
            self.listenerThread.shutDown()

        QApplication.instance().quit()


class ListenerThread(QThread):
    """
    Thread for listening to inter-process communication events.
    """

    dataReceived = Signal(object)
    errored = Signal(object)

    def __init__(self, function: object = None) -> None:
        """
        Initialize the ListenerThread.

        Args:
            function (object, optional): Optional function to run.
        """
        super(ListenerThread, self).__init__()

    def run(self) -> None:
        """
        Run the listener thread.
        """
        try:
            from multiprocessing.connection import Listener

            port = 7571
            address = ('localhost', port)
            try:
                self.listener = Listener(address)
            except Exception as e:
                if platform.system() == "Windows":
                    errid = 10048
                else:
                    errid = 98

                if e.errno == errid:
                    logging.warning("Port %s is already in use. Please contact the support." % port)
                    return
                else:
                    raise

            while True:
                self.conn = self.listener.accept()
                while True:
                    try:
                        data = self.conn.recv()
                    except Exception as e:
                        break

                    self.dataReceived.emit(data)

            self.listener.close()
            self.quit()
        except Exception as e:
            self.errored.emit(traceback.format_exc())

    def shutDown(self) -> None:
        """
        Shut down the listener thread.
        """
        if hasattr(self, "listener"):
            self.listener.close()

        self.quit()


class SenderThread(QThread):
    """
    Thread for sending inter-process communication events.
    """
    def __init__(self, function: object = None) -> None:
        """
        Initialize the SenderThread.

        Args:
            function (object, optional): Optional function to run.
        """
        super(SenderThread, self).__init__()
        self.canceled = False

    def run(self) -> None:
        """
        Run the sender thread.
        """
        from multiprocessing.connection import Client
        port = 7571
        address = ('localhost', port)
        self.conn = Client(address)

    def shutDown(self) -> None:
        """
        Shut down the sender thread.
        """
        self.conn.close()
        self.quit()

    def send(self, data: object) -> None:
        """
        Send data to the listener.

        Args:
            data (object): The data to send.
        """
        self.conn.send(data)


def isAlreadyRunning() -> bool:
    """
    Check if Prism is already running.

    Returns:
        bool: True if running, False otherwise.
    """
    if platform.system() == "Windows":
        coreProc = []
        ignoredPids = [os.getpid()]
        for arg in sys.argv:
            if arg.startswith("ignore_pid="):
                pid = int(arg.split("=")[-1])
                ignoredPids.append(pid)

        for proc in psutil.process_iter():
            try:
                if (
                    proc.pid not in ignoredPids
                    and os.path.basename(proc.exe()) == "Prism.exe"
                    and proc.username() == psutil.Process(os.getpid()).username()
                ):
                    coreProc.append(proc.pid)
                    return True
            except:
                pass

    return False


def findPrismProcesses() -> list[str]:
    """
    Find running Prism processes.

    Returns:
        list[str]: List of process descriptions.
    """
    procs = []
    exes = [
        "Prism.exe",
    ]
    try:
        import psutil
    except Exception as e:
        pass
    else:
        ignoredPids = [os.getpid()]
        for arg in sys.argv:
            if arg.startswith("ignore_pid="):
                pid = int(arg.split("=")[-1])
                ignoredPids.append(pid)

        for proc in psutil.process_iter():
            try:
                if proc.pid in ignoredPids:
                    continue

                try:
                    if os.path.basename(proc.exe()) in exes:
                        procs.append("%s (%s)" % (proc.exe(), proc.pid))
                except:
                    continue
            except:
                pass

    return procs


def showDetailPopup(msgTxt: str, parent: QMessageBox) -> str:
    """
    Show a popup with details about running Prism processes.

    Args:
        msgTxt (str): The message text.
        parent (QMessageBox): The parent widget.

    Returns:
        str: The result of the popup.
    """
    procUserTxt = findPrismProcesses()
    if procUserTxt:
        msgTxt += "\n\nThe following Prism processes are already running:\n\n"
        msgTxt += "\n".join(procUserTxt)

    title = "Details"
    icon = QMessageBox.Information
    buttons = ["Stop processes", "Close"]
    default = buttons[0]
    escapeButton = "Close"

    msg = QMessageBox(
        icon,
        title,
        msgTxt,
        parent=parent,
    )

    for button in buttons:
        if button in ["Close", "Cancel", "Ignore"]:
            role = QMessageBox.RejectRole
        else:
            role = QMessageBox.YesRole

        b = msg.addButton(button, role)
        if default == button:
            msg.setDefaultButton(b)

        if escapeButton == button:
            msg.setEscapeButton(b)

    msg.exec_()
    result = msg.clickedButton().text()
    if result == "Stop processes":
        closePrismProcesses()
        parent._result = "Stop running process"
        parent.close()
    elif result == "Close":
        pass

    return result


def popupQuestion(text: str, buttons: list[str]) -> str:
    """
    Show a question popup with custom buttons.

    Args:
        text (str): The question text.
        buttons (list[str]): List of button labels.

    Returns:
        str: The result of the popup.
    """
    text = str(text)
    title = "Prism"
    icon = QMessageBox.Warning
    default = buttons[0]
    escapeButton = "Close"

    msg = QMessageBox(
        icon,
        title,
        text,
    )
    for button in buttons:
        if button in ["Close", "Cancel", "Ignore"]:
            role = QMessageBox.RejectRole
        else:
            role = QMessageBox.YesRole

        b = msg.addButton(button, role)
        if default == button:
            msg.setDefaultButton(b)

        if button == "Details...":
            b.clicked.disconnect()
            b.clicked.connect(lambda: showDetailPopup(text, msg))

        if escapeButton == button:
            msg.setEscapeButton(b)

    msg.exec_()
    result = msg.clickedButton().text()
    if hasattr(msg, "_result"):
        result = msg._result

    return result


def closePrismProcesses() -> None:
    """
    Close all running Prism processes except the current one.
    """
    try:
        import psutil
    except Exception as e:
        pass
    else:
        PROCNAMES = ["Prism.exe"]
        for proc in psutil.process_iter():
            if proc.name() in PROCNAMES:
                p = psutil.Process(proc.pid)
                if proc.pid == os.getpid():
                    continue

                try:
                    if "SYSTEM" not in p.username():
                        try:
                            proc.kill()
                        except Exception as e:
                            logger.warning("error while killing process: %s" % str(e))
                except Exception as e:
                    logger.warning("failed to kill process: %s" % str(e))


def sendCommandToPrismProcess(command):
    senderThread = SenderThread()
    senderThread.start()
    idx = 0
    while True:
        if hasattr(senderThread, "conn"):
            break

        time.sleep(1)
        idx += 1
        if idx > 3:
            break

    if hasattr(senderThread, "conn"):
        senderThread.send(command)
        senderThread.shutDown()
        return True
    else:
        senderThread.quit()
        return False


def launch() -> None:
    """
    Launch the Prism tray application.
    """
    if isAlreadyRunning():
        qApp = QApplication.instance()
        if not qApp:
            qApp = QApplication(sys.argv)

        result = sendCommandToPrismProcess("openProjectBrowser")
        if not result:
            qApp = QApplication.instance()
            wIcon = QIcon(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "UserInterfacesPrism",
                    "p_tray.png",
                )
            )
            qApp.setWindowIcon(wIcon)

            from UserInterfacesPrism.stylesheets import blue_moon
            qApp.setStyleSheet(blue_moon.load_stylesheet(pyside=True))

            result = popupQuestion("Prism is already running.", buttons=["Stop running process", "Details...", "Close"])
            if result == "Stop running process":
                closePrismProcesses()
                return launch()
            elif result == "Close":
                pass
            elif result == "Ignore":
                return

        sys.exit()
    else:
        args = ["loadProject", "tray"]
        if "projectBrowser" not in sys.argv:
            args.append("noProjectBrowser")
            if "showSplash" not in sys.argv:
                args.append("noSplash")

        pc = PrismCore.create(prismArgs=args)
        qApp = QApplication.instance()
        qApp.setQuitOnLastWindowClosed(False)
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(
                None,
                "PrismTray",
                "Could not launch PrismTray. Tray icons are not supported on this OS.",
            )
            sys.exit(1)

        pc.startTray()
        sys.exit(qApp.exec_())


if __name__ == "__main__":
    launch()
