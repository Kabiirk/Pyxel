# This script holds the Main UI building class
# It is instantiated as 'Window' in main.py
# Any changes in the UI to be implemented by
# editing this script

import sys
from PyQt5 import QtWidgets

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMenuBar, QMenu, QAction, QLabel, QWidget

NUM_BLOCKS_X = 10
NUM_BLOCKS_Y = 10
WIDTH = 20
HEIGHT = 20


class QS(QGraphicsScene):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lines = []

        self.draw_grid()
        self.set_opacity(0.3)
        #self.set_visible(False)
        #self.delete_grid()

    def draw_grid(self):
        width = NUM_BLOCKS_X * WIDTH
        height = NUM_BLOCKS_Y * HEIGHT
        self.setSceneRect(0, 0, width, height)
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        pen = QPen(QColor(255,0,100), 1, Qt.SolidLine)

        for x in range(0,NUM_BLOCKS_X+1):
            xc = x * WIDTH
            self.lines.append(self.addLine(xc,0,xc,height,pen))

        for y in range(0,NUM_BLOCKS_Y+1):
            yc = y * HEIGHT
            self.lines.append(self.addLine(0,yc,width,yc,pen))

    def set_visible(self,visible=True):
        for line in self.lines:
            line.setVisible(visible)

    def delete_grid(self):
        for line in self.lines:
            self.removeItem(line)
        del self.lines[:]

    def set_opacity(self,opacity):
        for line in self.lines:
            line.setOpacity(opacity)

class MainWindow(QtWidgets.QMainWindow):
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


        # self.label = QLabel()
        # self.label.setStyleSheet("background-color: lightgreen")
        # self.label.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # self.label.setAlignment(Qt.AlignCenter)
        # self.setMinimumSize(10,10)
        # w = self.label.width()
        # h = self.label.height()
        # self.canvas = QPixmap(w, h)
        # self.canvas.fill(QColor("white")) # Ref.: https://stackoverflow.com/questions/63269098/qpixmap-qpainter-showing-black-window-background
        # self.label.setPixmap(self.canvas.scaled(w,h ))
        # self.setCentralWidget(self.label)
        # self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        # #self.draw_something()
        # self.last_x, self.last_y = None, None
        # print(self.label.size(), w, h)
        gv = QGraphicsView()
        gs = QS()
        gv.setScene(gs)
        self.setCentralWidget(gv)



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
