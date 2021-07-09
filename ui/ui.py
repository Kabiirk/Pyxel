# This script holds the Main UI building class
# It is instantiated as 'Window' in main.py
# Any changes in the UI to be implemented by
# editing this script

# Ref : 
# Hover events = https://stackoverflow.com/questions/37090727/hover-event-for-a-qgraphicsitem-pyqt4

import sys
from PyQt5 import QtWidgets

from PyQt5.QtGui import QBrush, QPainter, QPen, QPixmap, QColor
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

    
    def hoverEnterEvent(self, event):
        print('hello')

