# This script holds the Main UI building class
# It is instantiated as 'Window' in main.py
# Any changes in the UI to be implemented by
# editing this script

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QMenuBar, QToolBar, QAction

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Pyxel")
        self.resize(400, 200)
        self.centralWidget = QLabel("Hello, World")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

        # 1. Menubar
        #   1.A. Creating Menubar & Menu Items
        self.menubar = QMenuBar(self)
        #   File
        filemenu = QMenu('&File', self.menubar)
        #   Edit
        editmenu = QMenu('&Edit', self.menubar)
        #   Help
        helpmenu = QMenu('&Help', self.menubar)

        #    1.B. Adding Menu Items to Menubar
        self.menubar.addMenu(filemenu)
        self.menubar.addMenu(editmenu)
        self.menubar.addMenu(helpmenu)

        # Setting menubar as Menubar for Window
        self.setMenuBar(self.menubar)


        # 2. Toolbars
        fileToolBar = self.addToolBar("File")
        new = QAction("New",self)
        fileToolBar.addAction(new)
        # Using a QToolBar object
        editToolBar = QToolBar("Edit", self)
        # Using a QToolBar object and a toolbar area
        helpToolBar = QToolBar("Help", self)
        self.addToolBar(editToolBar)
        self.addToolBar(Qt.LeftToolBarArea, helpToolBar)