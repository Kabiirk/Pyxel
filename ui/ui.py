# This script holds the Main UI building class
# It is instantiated as 'Window' in main.py
# Any changes in the UI to be implemented by
# editing this script

import sys

from PyQt5.QtGui import QIcon, QKeySequence, QImage
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QMenuBar, QToolBar, QAction, QSpinBox

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Pyxel")
        self.setGeometry(200,200,400,400)
        self.centralWidget = QLabel("Hello, World")
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        # variables
        # drawing flag
        self.drawing = False
        # default brush size
        self.brushSize = 2
        # default color
        self.brushColor = Qt.black
        # QPoint object to tract the point
        self.lastPoint = QPoint()
  


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
        file_toolbar = QToolBar("File", self)
        file_toolbar.setMovable(False)
        tools_toolbar = QToolBar("Tools", self)
        palette_toolbar = QToolBar("Palette", self)
        
        #    2.A. Creating Actions for File Toolbar
        new_project = QAction("New",self)
        file_toolbar.addAction(new_project)
        open_project = QAction("Open",self)
        file_toolbar.addAction(open_project)
        save_project = QAction("Save",self)
        file_toolbar.addAction(save_project)
        
        #   2.B. Creating Actions for tools Toolbar
        shape = QAction("Shape",self)
        tools_toolbar.addAction(shape)
        paint = QAction("Paint",self)
        tools_toolbar.addAction(paint)
        
        #   2.C. Creating Actions for Palette Toolbar
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setFocusPolicy(Qt.NoFocus)
        palette_toolbar.addWidget(self.fontSizeSpinBox)
        palette = QAction("Palette",self)
        palette_toolbar.addAction(palette)
        layers = QAction("Layers",self)
        palette_toolbar.addAction(layers)

        # Adding toolbars to Window
        self.addToolBar(file_toolbar)
        self.addToolBar(Qt.LeftToolBarArea , tools_toolbar)
        self.addToolBar(Qt.RightToolBarArea, palette_toolbar)

        # contextMenuPolicy for centralwidget
        # Setting contextMenuPolicy
        self.centralWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        # Populating the widget with actions
        self.centralWidget.addAction(self.newAction)
        self.centralWidget.addAction(self.openAction)
        self.centralWidget.addAction(self.saveAction)
        self.centralWidget.addAction(self.copyAction)
        self.centralWidget.addAction(self.pasteAction)
        self.centralWidget.addAction(self.cutAction)

        
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
        # Snip...
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

    def newFile(self):
        # Logic for creating a new file goes here...
        self.centralWidget.setText("<b>File > New</b> clicked")

    def openFile(self):
        # Logic for opening an existing file goes here...
        self.centralWidget.setText("<b>File > Open...</b> clicked")

    def saveFile(self):
        # Logic for saving a file goes here...
        self.centralWidget.setText("<b>File > Save</b> clicked")

    def copyContent(self):
        # Logic for copying content goes here...
        self.centralWidget.setText("<b>Edit > Copy</b> clicked")

    def pasteContent(self):
        # Logic for pasting content goes here...
        self.centralWidget.setText("<b>Edit > Paste</b> clicked")

    def cutContent(self):
        # Logic for cutting content goes here...
        self.centralWidget.setText("<b>Edit > Cut</b> clicked")

    def helpContent(self):
        # Logic for launching help goes here...
        self.centralWidget.setText("<b>Help > Help Content...</b> clicked")

    def about(self):
        # Logic for showing an about dialog content goes here...
        self.centralWidget.setText("<b>Help > About...</b> clicked")
