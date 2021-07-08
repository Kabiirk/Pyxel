# This script holds the Main UI building class
# It is instantiated as 'Window' in main.py
# Any changes in the UI to be implemented by
# editing this script

import sys
from PyQt5 import QtWidgets

from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsItem, QMenuBar, QMenu, QAction, QLabel, QWidget,QGraphicsPixmapItem


class graphics_Object(QGraphicsPixmapItem):
    def __init__(self, parent=None):
        super(graphics_Object, self).__init__(parent)
        pixmap = QPixmap("a.png")
        self.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio))
        self.setFlag(QGraphicsPixmapItem.ItemIsSelectable)
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        print('hello')


class graphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(graphicsScene, self).__init__(parent)
        for i in range(2):
            for j in range(2):
                self.graphics_item = graphics_Object()


    # def mousePressEvent(self, event):
    #     self.graphics_item = graphics_Object()
        
    def mouseReleaseEvent(self, event):
        print('adding to scene')
        self.addItem(self.graphics_item)
        self.graphics_item.setPos(event.scenePos())

class customPixel(QGraphicsRectItem):
    def __init__(self, x, y, h, w, pen, brush, parent=None):
        super(customPixel, self).__init__(x, y, h, w, pen, brush, parent)
        self.setBrush = brush
        self.setPen = pen
        self.setPos(x,y)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        print('hello')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Pyxel")
        self.setGeometry(200,200,400,400)

        self._zoom = 0

        self.gs = QGraphicsScene()

        self.brush1 = QBrush(Qt.white)
        self.brush2 = QBrush(Qt.black)

        self.pen = QPen(Qt.red)

        self.gv = QGraphicsView(self.gs, self)

        for i in range(10):
            for j in range(10):
                rect = self.gs.addItem(customPixel(i*20, j*20, 20, 20, self.pen, self.brush1))
        # # rect1 = self.gs.addRect(10,10,20,20, self.pen, self.brush1)
        # # rect2 = self.gs.addRect(30,10,20,20, self.pen, self.brush1)
        # # rect3 = self.gs.addRect(50,10,20,20, self.pen, self.brush1)
        # # rect1.setFlag(QGraphicsItem.ItemIsMovable, QGraphicsItem.ItemIsSelectable)

        self.setCentralWidget(self.gv)

    
    def hoverEnterEvent(self, event):
        print('hello')

