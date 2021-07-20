# This script holds the Main UI building class
# It is instantiated as 'Window' in main.py
# Any changes in the UI to be implemented by
# editing this script

# Ref : 
# Hover events = https://stackoverflow.com/questions/37090727/hover-event-for-a-qgraphicsitem-pyqt4

import sys
from PyQt5 import QtWidgets

from PyQt5.QtGui import QBrush, QImage, QPainter, QPen, QPixmap, QColor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsItem, QMenuBar, QMenu, QAction, QLabel, QStatusBar, QToolBar, QWidget,QGraphicsPixmapItem


class Pixel(QGraphicsRectItem):
    def __init__(self, x,y,h,w, *args, parent=None):
        super().__init__(x,y,h,w, parent=None)
        self.default_color = QBrush(Qt.white)
        self.hover_color = args[0]
        self.setAcceptHoverEvents(True)
        self.setBrush(self.default_color)

    def hoverEnterEvent(self, event):
        self.setBrush(self.hover_color)
    
    def hoverLeaveEvent(self, event):
        self.setBrush(self.default_color)

    def mousePressEvent(self, event):
        #self.setBrush(self.hover_color)
        self.default_color = self.hover_color

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = pyqtSignal(QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__( parent)
        self._zoom = 0
        self._empty = False
        self._scene = QtWidgets.QGraphicsScene(self)
        self.pen_color = Qt.red
        self._photo = QtWidgets.QGraphicsPixmapItem()
        canvas = QPixmap(200, 200)
        canvas.fill(QColor("white")) # ref. : https://stackoverflow.com/questions/63269098/qpixmap-qpainter-showing-black-window-background
        self._photo.setPixmap(canvas)
        self._scene.addItem(self._photo)
        # for i in range(20):
        #     for j in range(20):
        #         self._scene.addItem(Pixel(i*20, j*20,20,20, self.brush3))
        self.setScene(self._scene)
        #self.draw_something()
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0
    
    def draw_something(self):
        #painter = QPainter(self._photo.pixmap())
        pixmap = self._photo.pixmap()
        painter = QPainter()
        painter.begin(pixmap)
        painter.drawLine(10, 10, 50, 50)
        self._photo.setPixmap(pixmap)
        painter.end()

    def mouseMoveEvent(self, e):
        # ref https://stackoverflow.com/questions/39866813/qt5-scribble-with-layers-qpaintdevice-cannot-destroy-device-that-is-being-pai
        pixmap = self._photo.pixmap()
        painter = QPainter()
        painter.begin(pixmap)
        p = painter.pen()
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawPoint(e.x(), e.y())
        self._photo.setPixmap(pixmap)
        painter.end()
        #self.update()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Pyxel")
        self.setGeometry(200,200,400,400)

        self._zoom = 0

        self.gs = QGraphicsScene()

        self.gv = PhotoViewer(self)
        # for i in range(20):
        #     for j in range(20):
        #         self.gs.addItem(Pixel(i*20, j*20,20,20))

        # Menubar
        menuBar = self.menuBar()

        fileMenu = QMenu("&File", self)
        self.newAction = QAction("&New", self)
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        editMenu = QMenu("&Edit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        
        helpMenu = QMenu("&Help", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)

        menuBar.addMenu(fileMenu)
        menuBar.addMenu(editMenu)
        menuBar.addMenu(helpMenu)

        # Toolbar
        self.ColorAction = QAction("&Color", self)

        editToolBar = QToolBar("Edit", self)
        self.addToolBar(Qt.LeftToolBarArea, editToolBar)
        helpToolBar = QToolBar("Help", self)
        helpToolBar.addAction(self.ColorAction)
        self.addToolBar(Qt.RightToolBarArea, helpToolBar)

        # Binding all the Actions to options
        # Menubar Actions
        self.exitAction.triggered.connect(self.close)

        # Toolbar actions
        self.ColorAction.triggered.connect(self.changeBrushColor)

        self.setCentralWidget(self.gv)

    def changeBrushColor(self):
        self.gv.pen_color = Qt.blue
        print("I was pressed !")