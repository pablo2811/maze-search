from PyQt5 import QtWidgets,QtCore,QtGui,QtTest
from PyQt5.QtCore import pyqtSlot
import math,sys
import SearchMaze,hackTime
from colour import Color
import webcolors,time


# class Worker(QtCore.QRunnable):
#     '''
#     Worker thread
#     '''
#
#     @pyqtSlot()
#     def run(self):
#         time.sleep(5)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.basics()
        self.scope = 25
        self.prev = 25
        self.side = None
        self.start = None
        self.end = None
        self.black = set()
        self.blue = None
        self.red = None
        self.amount = None
        self.path = None
        self.threadpool = QtCore.QThreadPool()
    def mousePressEvent(self, event):
        X = event.pos().x()
        Y = event.pos().y()
        if 900 >= X >= 0 and 900 >= Y >= 0:
            x_paint = X // self.side
            y_paint = Y // self.side
            remove = False
            for b in self.black:
                if b == (x_paint,y_paint):
                    self.black.remove(b)
                    remove = True
                    break
            if (x_paint,y_paint) == self.red:
                self.red = None
                remove = True
            if (x_paint,y_paint) == self.blue:
                self.blue = None
                remove = True
            if not remove:
                if event.button() == QtCore.Qt.LeftButton:
                    self.black.add((x_paint,y_paint))
                else:
                    if self.blue is None:
                        self.blue = (x_paint,y_paint)
                    else:
                        if self.blue[0]//self.side == x_paint and self.blue[1]//self.side == y_paint:
                            self.blue = None
                        else:
                            if self.red is None:
                                self.red = (x_paint,y_paint)
                            else:
                                if self.red[0] // self.side == x_paint and self.red[1] // self.side == y_paint:
                                    self.red = None
                                else:
                                    self.red = (x_paint,y_paint)
            self.update()


    def mouseMoveEvent(self, event):
        X = event.pos().x()
        Y = event.pos().y()
        if 900 >= X >= 0 and 900 >= Y >= 0:
            self.black.add((X//self.side, Y//self.side))
            self.update()

    def basics(self):
        self.resize(900, 1050)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        scale = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        scale.move(220, 950)
        scale.setParent(self)
        scale.setMinimum(0)
        scale.setMaximum(100)
        scale.resize(600, 62)
        scale.setSliderPosition(25)
        scale.valueChanged.connect(self.zoom)
        start = QtWidgets.QPushButton(self)
        start.move(50,955)
        start.resize(100,50)
        start.setText("RUN")
        start.clicked.connect(self.runAstar)

    def runAstar(self):
        if self.blue is None or self.red is None:
            popup = QtWidgets.QMessageBox(self)
            popup.setText("Start (blue square) or end (red square) not set.")
            popup.show()
        else:
            lookup = SearchMaze.Graph(self.blue,self.red,self.black,self.amount)
            p = lookup.ASTAR()
            if p is None:
                popup = QtWidgets.QMessageBox(self)
                popup.setText("No solution.")
                popup.show()
            else:
                self.path = p
                red = Color("red")
                self.colors = list(red.range_to(Color("green"), len(self.path)))
                self.j = 1
                while self.j <= len(self.path):
                    time.sleep(0.1)
                    QtWidgets.QApplication.processEvents()
                    self.update()
                    self.j += 1

    def paintEvent(self,event):
        if self.prev != self.scope:
            self.black = set()
            self.red = None
            self.blue = None
            self.path = None
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen()
        pen.setWidth((8/15000)*self.scope**2-(360/3000)*self.scope+1034/120)
        pen.setStyle(QtCore.Qt.SolidLine)
        painter.setPen(pen)
        amount = (19/7500)*self.scope**2+(37/60)*self.scope + 3
        self.amount = amount
        self.side = int(900 // amount)
        self.prev = self.scope
        i = 0
        while i < 905-self.side:
            painter.drawRect(i,i,self.side,self.side)
            j = 0
            while j < 905-self.side:
                painter.drawRect(i,j,self.side,self.side)
                j += self.side
            i += self.side
        for p in self.black:
            painter.fillRect(p[0]*self.side,p[1]*self.side,self.side,self.side,QtCore.Qt.black)
        if self.blue is not None:
            painter.fillRect(self.blue[0]*self.side,self.blue[1]*self.side,self.side,self.side,QtCore.Qt.blue)
        if self.red is not None:
            painter.fillRect(self.red[0] * self.side, self.red[1] * self.side, self.side, self.side, QtCore.Qt.red)
        if self.path is not None:
            for i in range(self.j):
                p = self.path[i]
                a = webcolors.hex_to_rgb(self.colors[i].get_hex())
                painter.fillRect(p[0]*self.side,p[1]*self.side,self.side,self.side,QtGui.QColor(a.red,a.green,a.blue))



    def zoom(self,currVal):
        self.scope = currVal
        self.update()
        return currVal
app = QtWidgets.QApplication([])
icon = QtGui.QIcon("logo.png")
app.setWindowIcon(icon)
app.setApplicationName("Maze Solver")
main = MainWindow()
main.show()
app.exec_()






