#!/usr/bin/env python
#from: http://stackoverflow.com/questions/19121309/pyqt-qgraphicsitem-added-at-a-wrong-position

import sys, datetime
#from PyQt4.QtCore import (QPointF, QRectF, Qt, )
#from PyQt4.QtGui import (QApplication, QMainWindow, QGraphicsItem, 
#                         QGraphicsScene, QGraphicsView, QPen, QStyle)
from PyQt4 import QtGui, QtCore

MapSize = (512, 512)




class DraggableMark(QtGui.QGraphicsItem):
    def __init__(self, position, scene):
        super(DraggableMark, self).__init__(None, scene)
        #self.setObjectName( 'fuck' )
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable)
        #now = datetime.datetime.now()
        #self.setData( 0, 'Das ist mein Name' )
        #self.setData( 1, 'fuck' )
        #self.rect = QtCore.QRectF(position.x(), position.y(), 15, 15)
        self.rect = QtCore.QRectF(-30, -30, 120, 60)
        self.setPos(position)
        scene.clearSelection()
        
        #print dir( item )
        #print 'init'
        
        #painter = QtGui.QPainter()
        

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(3)
        
        if option.state & QtGui.QStyle.State_Selected:
            pen.setColor(QtCore.Qt.green)
            print 'hallo'
            #print dir( self.data( 0 ) )
            #print self.data( 0 )..toString
            #print self.data( 0 ).type
        painter.setPen(pen)
        #brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        #painter.setBrush(brush)
        painter.setBrush(QtGui.QColor(200, 0, 0))
        #painter.drawEllipse(self.rect)
        painter.drawRoundedRect(self.rect, 10.0, 10.0)
        #painter.drawLine(20, 160, 250, 160)



class GraphicsScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.setSceneRect(0, 0, *MapSize)
        #DraggableMark(QtCore.QPointF(92.0, 90.0), self)

    def mousePressEvent(self, event):
        super(GraphicsScene, self).mousePressEvent(event)
        if event.button() != QtCore.Qt.LeftButton:
            print "Left mouse click"
            #return

        modifiers = QtGui.QApplication.keyboardModifiers()
        pos = event.scenePos()
        if modifiers == QtCore.Qt.ControlModifier:
            print("Control + Click: (%d, %d)" % (pos.x(), pos.y()))
            DraggableMark(pos, self)
            #self.addEllipse(QtCore.QRectF(pos.x(), pos.y(), 10, 10))
        else:
            print("Click: (%d, %d)" % (pos.x(), pos.y()))
            
#             start = QtCore.QPointF(self.mapToScene(self._start))
#             end = QtCore.QPointF(self.mapToScene(event.pos()))
#             self.scene().addItem(QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))          


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.scene = GraphicsScene(self)
        self.scene.addRect(QtCore.QRectF(0, 0, *MapSize), QtCore.Qt.red)
        self.view = QtGui.QGraphicsView()
        self.view.setScene(self.scene)
        self.view.resize(self.scene.width(), self.scene.height())
        self.setCentralWidget(self.view)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    rect = QtGui.QApplication.desktop().availableGeometry()
    window.resize(int(rect.width()), int(rect.height()))
    window.show()
    app.exec_()