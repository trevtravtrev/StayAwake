# App: Stay Awake
# Author: Trevor White
# Description: Stay Awake is a simple app that keeps your computer from sleeping. Features a simple GUI and
#              minimize to tray functionality.

from pyautogui import press
from time import sleep
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, qApp
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import images_qr    # workaround to get it to compile to .exe with pyinstaller
import StayAwake

# since window is fixed, prevents it from showing small on high resolution screens
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


# QThread class to enable threading in GUI for "preventing sleep" loop
class PreventSleep(QThread):
    def __init__(self):
        QThread.__init__(self)

    # "Prevent sleep" method presses f24 key every 60 seconds to prevent sleep
    def run(self):
        while True:
            press('f24')  # press f24 key to prevent sleep
            sleep(60)  # wait 1 minute
   
# main GUI class, inherits from QMainWindow
class StayAwakeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(StayAwakeApp, self).__init__()
        self.ui = StayAwake.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.label_2.setPixmap(QtGui.QPixmap(":icons/32x32.png"))    # set logo in app window (workaround for pyinstaller)
        self.ui.toggle.clicked.connect(self.togglePressed)  # listener for when toggle button is pressed

        self.running = False  # flag to check if program is on or off
        self.preventSleep = None  # initializing to hold PreventSleep instance
        self.trayIcon = None  # initializing to hold tray icon instance
        self.status = "off"

        self.setupTray()  # setup tray icon and menu
       
    #handle double click event
    def handleDoubleClick(self,reason):
        if reason == self.trayIcon.DoubleClick:
           self.showNormal()

    # setup tray icon and menu
    def setupTray(self):
        self.trayIcon = QSystemTrayIcon(self)  # instance of QSystemTrayIcon
        self.trayIcon.setIcon(QIcon(":icons/StayAwakeOpaque.ico"))  # set tray icon image
        self.trayIcon.setToolTip("Stay Awake")

        openAction = QAction("Open", self)  # "open" right click option in tray
        quitAction = QAction("Quit", self)  # "quit" right click option in tray
        openAction.triggered.connect(self.showNormal)  # open app trigger
        quitAction.triggered.connect(qApp.quit)  # quit app trigger
        trayMenu = QMenu()  # QMenu class instance
        trayMenu.addAction(openAction)  # add open action
        trayMenu.addAction(quitAction)  # add quit action
        self.trayIcon.setContextMenu(trayMenu)  # sets menu actions
        self.trayIcon.activated.connect(self.handleDoubleClick) # Icon clicked trigger
        self.trayIcon.show()  # makes tray icon visible
       
    

   



    # handle toggle button states and calling prevent sleep
    def togglePressed(self):
        if self.running:
            self.ui.toggle.setText("Start")  # set toggle button text to "Off"
            self.status = "off"
            self.running = False  # update state
            self.preventSleep.terminate()  # terminate prevent sleep thread
        else:
            self.ui.toggle.setText("Stop")  # set toggle button text to "On"
            self.status = "on"
            self.running = True  # update state
            self.preventSleep = PreventSleep()  # create instance of PreventSleep class
            self.preventSleep.start()  # start prevent sleep thread

    # making "minimize" button minimizes to tray instead of taskbar
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:  # if minimize button is pressed
                event.ignore()  # ignore "minimize to taskbar" event
                self.hide()  # hide the window
                self.trayIcon.show()  # show tray icon
                self.trayIcon.showMessage("Stay Awake is currently " + self.status + ".", "Minimized to tray.",
                                          QSystemTrayIcon.Information)  # show tray message popup


# set icon for window
def setAppIcon():
    appIcon = QtGui.QIcon()  # create instance of QIcon class
    appIcon.addFile(':icons/16x16.png', QtCore.QSize(16, 16))    # adding different sized icons
    appIcon.addFile(':icons/32x32.png', QtCore.QSize(32, 32))
    appIcon.addFile(':icons/48x48.png', QtCore.QSize(48, 48))
    appIcon.addFile(':icons/192x192.png', QtCore.QSize(192, 192))
    appIcon.addFile(':icons/512x512.png', QtCore.QSize(512, 512))
    app.setWindowIcon(appIcon)  # set correct window icon


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    setAppIcon()
    application = StayAwakeApp()
    application.show()
    sys.exit(app.exec())
