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

        gv = QGraphicsView(self.gs, self)

        for i in range(32):
            for j in range(32):
                rect = self.gs.addRect(i*20, j*20, 20, 20, self.pen, self.brush1)
                rect.setAcceptHoverEvents(True)
        # rect1 = self.gs.addRect(10,10,20,20, self.pen, self.brush1)
        # rect2 = self.gs.addRect(30,10,20,20, self.pen, self.brush1)
        # rect3 = self.gs.addRect(50,10,20,20, self.pen, self.brush1)
        # rect1.setFlag(QGraphicsItem.ItemIsMovable, QGraphicsItem.ItemIsSelectable)

        self.setCentralWidget(gv)

       