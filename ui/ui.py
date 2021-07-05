# This script holds the Main UI building class
# It is instantiated as 'Window' in main.py
# Any changes in the UI to be implemented by
# editing this script

import sys
from PyQt5 import QtWidgets

from PyQt5.QtGui import QBrush, QPainter, QPen
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QMenuBar, QMenu, QAction, QLabel, QWidget


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

        for i in range(32):
            for j in range(32):
                rect = self.gs.addRect(i*20, j*20, 20, 20, self.pen, self.brush1)
                rect.setAcceptHoverEvents(True)
        # rect1 = self.gs.addRect(10,10,20,20, self.pen, self.brush1)
        # rect2 = self.gs.addRect(30,10,20,20, self.pen, self.brush1)
        # rect3 = self.gs.addRect(50,10,20,20, self.pen, self.brush1)
        # rect1.setFlag(QGraphicsItem.ItemIsMovable, QGraphicsItem.ItemIsSelectable)

        self.setCentralWidget(self.gv)

    
    def wheelEvent(self, event):
        if True:
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.gv.scale(factor, factor)
            elif self._zoom == 0:
                self.gv.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.gv.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

