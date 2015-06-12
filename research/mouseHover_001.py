#!/usr/local/bin/python

import os, sys
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MyView(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.scene = QGraphicsScene(self)
        self.item = GraphicsItem('item', 100, 50)
        self.item.moveBy(50, 50)
        self.scene.addItem(self.item)
        self.widget = GraphicsWidget('widget', 100, 50)
        self.scene.addItem(self.widget)
        self.setScene(self.scene)

class GraphicsItem(QGraphicsItem):
    def __init__(self, name, width, height):
        QGraphicsItem.__init__(self)
        self.setAcceptHoverEvents(True)
        self.name = name
        self.__width = width
        self.__height = height

    def boundingRect(self): 
        return QRectF(0, 0, self.__width, self.__height)

    def hoverEnterEvent(self, event):
        self.__printGeometryDetails()
        
    def hoverLeaveEvent(self, event):
    	print 'left'

    def paint(self, painter, option, widget):
        bgRect = self.boundingRect()
        painter.drawRects(bgRect)
        painter.fillRect(bgRect, QColor('blue'))

    def __printGeometryDetails(self):
        print self.name
        print '  pos (%.0f, %0.0f)' % (self.pos().x(), self.pos().y())
        print '  boundingRect (%.0f, %0.0f, %.0f, %0.0f)' % (self.boundingRect().x(), self.boundingRect().y(), self.boundingRect().width(), self.boundingRect().height())

class GraphicsWidget(QGraphicsWidget):
    def __init__(self, name, width, height):
        QGraphicsWidget.__init__(self)
        self.setAcceptHoverEvents(True)
        self.name = name
        self.__width = width
        self.__height = height

    def boundingRect(self):
        return QRectF(0, 0, self.__width, self.__height)

    def hoverEnterEvent(self, event):
        self.__printGeometryDetails()
        
    def hoverLeaveEvent(self, event):
    	print 'left'

    def paint(self, painter, option, widget):
        bgRect = self.boundingRect()
        painter.drawRects(bgRect)
        painter.fillRect(bgRect, QColor('red'))

    def __printGeometryDetails(self):
        print self.name
        print '  pos (%.0f, %0.0f)' % (self.pos().x(), self.pos().y())
        print '  boundingRect (%.0f, %0.0f, %.0f, %0.0f)' % (self.boundingRect().x(), self.boundingRect().y(), self.boundingRect().width(), self.boundingRect().height())
        print '  geometry (%.0f, %0.0f, %.0f, %0.0f)' % (self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height())
        print '  rect (%.0f, %0.0f, %.0f, %0.0f)' % (self.rect().x(), self.rect().y(), self.rect().width(), self.rect().height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MyView()
    view.setGeometry(600, 100, 400, 370)
    view.show()
    sys.exit(app.exec_())