#!/usr/bin/python

# dragbutton.py

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

class Button(QtGui.QPushButton):
    def __init__(self, title, parent):
        QtGui.QPushButton.__init__(self, title, parent)

    def mouseMoveEvent(self, event):

        if event.buttons() != QtCore.Qt.RightButton:
            return

        mimeData = QtCore.QMimeData()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        dropAction = drag.start(QtCore.Qt.MoveAction)

        if dropAction == QtCore.Qt.MoveAction:
            self.close()


    def mousePressEvent(self, event):
        QtGui.QPushButton.mousePressEvent(self, event)
        if event.button() == QtCore.Qt.LeftButton:
            print 'press'



class DragButton(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.resize(280, 150)
        self.setWindowTitle('Click or Move')
        self.setAcceptDrops(True)

        self.button = Button('Button', self)
        self.button.move(100, 65)


        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)


    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):

        position = event.pos()
        button = Button('Button', self)
        
        button.move(position)
        button.show()

        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()


app = QtGui.QApplication(sys.argv)
db = DragButton()
db.show()
app.exec_()