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
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsItem, QMenuBar, QMenu, QAction, QLabel, QWidget,QGraphicsPixmapItem


class Pixel(QGraphicsRectItem):
    def __init__(self, x,y,h,w, parent=None):
        super().__init__(x,y,h,w, parent=None)
        self.default_color = QBrush(Qt.white)
        self.setAcceptHoverEvents(True)
        self.setBrush(self.default_color)

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(Qt.black))
    
    def hoverLeaveEvent(self, event):
        self.setBrush(self.default_color)

    def mousePressEvent(self, event):
        self.setBrush(QBrush(Qt.red))
        self.default_color = QBrush(Qt.red)

class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = pyqtSignal(QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
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

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())
        self.fitInView()

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

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Pyxel")
        self.setGeometry(200,200,400,400)

        self._zoom = 0

        self.gs = QGraphicsScene()
        self.gs.setBackgroundBrush(QBrush(Qt.blue))

        self.brush1 = QBrush(Qt.white)
        self.brush2 = QBrush(Qt.black)

        self.pen = QPen(Qt.red)

        self.gv = QGraphicsView(self.gs)
        for i in range(20):
            for j in range(20):
                self.gs.addItem(Pixel(i*20, j*20,20,20))
        self.setCentralWidget(self.gv)