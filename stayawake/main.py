import sys
from time import sleep

import interface
from pyautogui import press
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, Qt, QThread
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon, qApp


class PreventSleep(QThread):
    def run(self):
        while True:
            press("f24")
            sleep(60)


class StayAwakeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = interface.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label_2.setPixmap(QtGui.QPixmap("icons/32x32.png"))

        self.running = False
        self.prevent_sleep = None
        self.tray_icon = None
        self.status = "off"

        self.setup_tray()
        self.setup_window()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icons/StayAwakeOpaque.ico"))
        self.tray_icon.setToolTip("Stay Awake")
        self.tray_icon.activated.connect(self.tray_icon_single_click)

        open_action = QAction("Open", self)
        quit_action = QAction("Quit", self)
        open_action.triggered.connect(self.showNormal)
        quit_action.triggered.connect(qApp.quit)
        tray_menu = QMenu()
        tray_menu.addAction(open_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def setup_window(self):
        self.ui.toggle.clicked.connect(self.toggle_pressed)
        self.setWindowIcon(QtGui.QIcon("icons/stayawake.ico"))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Stay Awake")

    def tray_icon_single_click(self, reason):
        if reason == self.tray_icon.Trigger:
            self.showNormal()
            self.activateWindow()

    def toggle_pressed(self):
        if self.running:
            self.ui.toggle.setText("Start")
            self.status = "off"
            self.running = False
            self.prevent_sleep.terminate()
        else:
            self.ui.toggle.setText("Stop")
            self.status = "on"
            self.running = True
            self.prevent_sleep = PreventSleep()
            self.prevent_sleep.start()

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                event.ignore()
                self.hide()
                self.tray_icon.show()
                self.tray_icon.showMessage(
                    "Stay Awake is currently " + self.status + ".",
                    "Minimized to tray.",
                    QSystemTrayIcon.Information,
                )


def set_app_icon():
    app_icon = QtGui.QIcon()
    app_icon.addFile(":icons/16x16.png", QtCore.QSize(16, 16))
    app_icon.addFile(":icons/32x32.png", QtCore.QSize(32, 32))
    app_icon.addFile(":icons/48x48.png", QtCore.QSize(48, 48))
    app_icon.addFile(":icons/192x192.png", QtCore.QSize(192, 192))
    app_icon.addFile(":icons/512x512.png", QtCore.QSize(512, 512))
    app.setWindowIcon(app_icon)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    set_app_icon()
    application = StayAwakeApp()
    application.show()
    sys.exit(app.exec_())
