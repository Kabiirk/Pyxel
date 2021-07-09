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
        self.setAcceptHoverEvents(True)
        self.setBrush(QBrush(Qt.white))

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(Qt.black))
        print('hello')
    
    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(Qt.white))

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

        self.gv = QGraphicsView(self.gs)
        a = Pixel(10,10,120,120)
        #a.setBrush(self.brush1)
        # a.setAcceptHoverEvents(True)
        self.gs.addItem(a)

        self.setCentralWidget(self.gv)

    
    def hoverEnterEvent(self, event):
        print('hello')

