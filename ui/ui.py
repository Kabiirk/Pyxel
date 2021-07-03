# This script holds the Main UI building class
# It is instantiated as 'Window' in main.py
# Any changes in the UI to be implemented by
# editing this script

import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Pyxel")
        self.setGeometry(200,200,400,400)

        # 1. Menubar
        #   1.A. Creating Menubar & Menu Items
        self.menubar = QMenuBar(self)
        #   File
        filemenu = QMenu('&File', self.menubar)
        self.newAction = QAction("New", self)
        self.openAction = QAction("Open", self)
        self.saveAction = QAction("Save", self)
        self.exitAction = QAction("Exit", self)
        filemenu.addAction(self.newAction)
        filemenu.addAction(self.openAction)
        filemenu.addAction(self.saveAction)
        filemenu.addAction(self.exitAction)

        #   Edit
        editmenu = QMenu('&Edit', self.menubar)
        self.copyAction = QAction("Copy", self)
        self.pasteAction = QAction("Paste", self)
        self.cutAction = QAction("Cut", self)
        editmenu.addAction(self.copyAction)
        editmenu.addAction(self.pasteAction)
        editmenu.addAction(self.cutAction)
        #   Help
        helpmenu = QMenu('&Help', self.menubar)
        self.helpAction = QAction("Help", self)
        self.aboutAction = QAction("About", self)
        helpmenu.addAction(self.helpAction)
        helpmenu.addAction(self.aboutAction)

        #    1.B. Adding Menu Items to Menubar
        self.menubar.addMenu(filemenu)
        self.menubar.addMenu(editmenu)
        self.menubar.addMenu(helpmenu)

        # Setting menubar as Menubar for Window
        self.setMenuBar(self.menubar)


        # 2. Toolbars
        tools_toolbar = QToolBar("Tools", self)
        
        #   2.B. Creating Actions for tools Toolbar
        shape = QAction("Shape",self)
        tools_toolbar.addAction(shape)
        paint = QAction("Paint",self)
        tools_toolbar.addAction(paint)

        # Adding toolbars to Window
        self.addToolBar(Qt.LeftToolBarArea , tools_toolbar)

        
        # Binding Actions in Menubar + Toolbars to Functions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        # Connect Edit actions
        self.copyAction.triggered.connect(self.copyContent)
        self.pasteAction.triggered.connect(self.pasteContent)
        self.cutAction.triggered.connect(self.cutContent)
        # Connect Help actions
        self.helpAction.triggered.connect(self.helpContent)
        self.aboutAction.triggered.connect(self.about)

        # Assigning Keyboard Shortcuts to Actions
        self.newAction.setShortcut("Ctrl+N")
        self.openAction.setShortcut("Ctrl+O")
        self.saveAction.setShortcut("Ctrl+S")
        # Edit actions
        # Using standard keys
        self.copyAction.setShortcut(QKeySequence.Copy)
        self.pasteAction.setShortcut(QKeySequence.Paste)
        self.cutAction.setShortcut(QKeySequence.Cut)

        # Status Bar
        self.statusbar = self.statusBar()
        # Adding a temporary message
        self.statusbar.showMessage("Ready", 3000)
        newTip = "Create a new file"
        self.newAction.setStatusTip(newTip)
        self.newAction.setToolTip(newTip)

        self.label = QLabel()
        self.label.setStyleSheet("background-color: lightgreen")
        w = self.label.width()
        h = self.label.height()
        canvas = QPixmap(w, h)
        canvas.fill(QColor("white")) # Ref.: https://stackoverflow.com/questions/63269098/qpixmap-qpainter-showing-black-window-background
        self.label.setPixmap(canvas.scaled(w,h ))
        self.setCentralWidget(self.label)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        #self.draw_something()
        self.last_x, self.last_y = None, None
        print(self.label.size())

    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        painter = QPainter(self.label.pixmap())
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None



    def newFile(self):
        # Logic for creating a new file goes here...
        print("Pressed !")
        # self.centralWidget.setText("<b>File > New</b> clicked")

    def openFile(self):
        # Logic for opening an existing file goes here...
        print("Pressed !")
        # self.centralWidget.setText("<b>File > Open...</b> clicked")

    def saveFile(self):
        # Logic for saving a file goes here...
        print("Pressed !")
        # self.centralWidget.setText("<b>File > Save</b> clicked")

    def copyContent(self):
        # Logic for copying content goes here...
        print("Pressed !")
        # self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        # Logic for pasting content goes here...
        print("Pressed !")
        # self.centralWidget.setText("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        # Logic for cutting content goes here...
        print("Pressed !")
        # self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def helpContent(self):
        # Logic for launching help goes here...
        print("Pressed !")
        # self.centralWidget.setText("<b>Help > Help Content...</b> clicked")

    def about(self):
        # Logic for showing an about dialog content goes here...
        print("Pressed !")
        # self.centralWidget.setText("<b>Help > About...</b> clicked")
