#!/usr/bin/env python
#from: http://stackoverflow.com/questions/19121309/pyqt-qgraphicsitem-added-at-a-wrong-position

import sys, datetime
#from PyQt4.QtCore import (QPointF, QRectF, Qt, )
#from PyQt4.QtGui import (QApplication, QMainWindow, QGraphicsItem, 
#                         QGraphicsScene, QGraphicsView, QPen, QStyle)
from PyQt4 import QtGui, QtCore

MapSize = (512, 512)

class LineClass( QtGui.QGraphicsLineItem ):
    def __init__(self, startItem, endItem, *args, **kwargs):
        super(LineClass, self).__init__(*args, **kwargs)
        
        self.myStartItem = startItem
        self.myEndItem = endItem
        self.myColor = QtCore.Qt.black
        self.setZValue(-1.0)
        #self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsFocusable)
        self.setPen(QtGui.QPen(QtCore.Qt.black, 10))
        
        
#         try:
#             temp = self.myStartItem
#             self.myStartItem = self.myEndItem
#             self.myEndItem = temp
#         except AttributeError, e:
#             print "Error checking isInputConnection on node %s" %str(e)
        
        
    def paint(self, painter, option, widget=None):
        #arrowSize = 20.0
        line = self.getLine()
        painter.setBrush(self.myColor)
        myPen = self.pen()
        myPen.setColor(self.myColor)
        painter.setPen(myPen)
        
        painter.drawLine(line)
        
    def getEndItem(self):
        print "SceneView.getEndItem(): self.myEndItem = %s" %self.myEndItem
        print "SceneView.getEndItem(): self.myEndItem.parentItem() = %s" %self.myEndItem.parentItem()
        return self.myEndItem.parentItem()

    def getStartItem(self):
        print "SceneView.getEndItem(): self.myStartItem = %s" %self.myStartItem
        print "SceneView.getEndItem(): self.myStartItem.parentItem() = %s" %self.myStartItem.parentItem()
        return self.myStartItem.parentItem()
    
    def getLine(self):
        p1 = self.myStartItem.sceneBoundingRect().center()
        print "p1 = %s" %p1
#        print "LineClass.getLine(): p1 = %s" %p1
        p2 = self.myEndItem.sceneBoundingRect().center()
        print "p1 = %s" %p2
#        print "LineClass.getLine(): p2 = %s" %p2
        return QtCore.QLineF(self.mapFromScene(p1), self.mapFromScene(p2))
    
#     def updatePosition(self):
#         print "SceneView.updatePosition() called"
#         self.setLine(self.getLine())
#         self.myStartItem.connectedLine.append(self)
#         self.myEndItem.connectedLine.append(self)
    
    
#     def boundingRect(self):
#         extra = (self.pen().width() + 100)  / 2.0
#         line = self.getLine()
#         p1 = line.p1()
#         p2 = line.p2()
#         return QtCore.QRectF(p1, QtCore.QSizeF(p2.x() - p1.x(), p2.y() - p1.y())).normalized().adjusted(-extra, -extra, extra, extra)

#     def shape(self):
#         path = super(LineClass, self).shape()
#         return path

    
















class line( QtGui.QGraphicsPathItem ):
    def __init__( self, startItem, endItem, scene ):
        super(line, self).__init__(None, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable)
        #self.rect = QtCore.QRectF(80, -20, 20, 20)
        #self.setPos(position)
        scene.clearSelection()
        
#         self.myStartItem = startItem
#         self.myEndItem = endItem
        
        
#         point1 = QtCore.QPointF( position.x(), position.y() )
#         point2 = QtCore.QPointF( position.x()/2, 0 )
#         point3 = QtCore.QPointF( position.x()/2-40, position.y()-20 )
#         point4 = QtCore.QPointF( position.x()-40, position.y()-20 )
        
        #pos = self.mapToScene(self.startItem.pos())
        
        point1 = QtCore.QPointF( startItem.pos() )
        print "startItem = %s" %startItem
        print "point1 = %s" %point1
        print "endItem = %s" %endItem
        print "startParent = %s" %startItem.parentItem()
        print "endParent = %s" %endItem.parentItem()

#         
#         self.contains( point1, point2, point3, point4 )
        
#         # Startpoint
#         path = QtGui.QPainterPath( point1 )
#         path.lineTo( point4 )
# #         path.cubicTo( point2, point3, point4 )
#         pathItem = QtGui.QGraphicsPathItem( path, self, self.scene() )
#         pen = QtGui.QPen( QtCore.Qt.green )
#         pen.setWidthF( 3 )
#         pathItem.setPen( pen )
    
    
    def getStartItem( self ):
        return self.startItem.parentItem()
    
    def getEndItem( self ):
        return self.endItem.parentItem()
    
#     def updatePosition(self):
#         print "SceneView.updatePosition() called"
#         self.setLine(self.getLine())
#         self.myStartItem.connectedLine.append(self)
#         self.myEndItem.connectedLine.append(self)
        
    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(3)




















class circleOutput( QtGui.QGraphicsItem ):
    def __init__( self, scene ):
        super(circleOutput, self).__init__(None, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
        self.rect = QtCore.QRectF(80, -20, 20, 20)
        #self.setPos(position)
        scene.clearSelection()
        
    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(3)
        
        if option.state & QtGui.QStyle.State_Selected:
            pen.setColor(QtCore.Qt.yellow)
            print 'hallo'
            #print dir( self.data( 0 ) )
            #print self.data( 0 )..toString
            #print self.data( 0 ).type
        painter.setPen(pen)
        #brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        #painter.setBrush(brush)
        painter.setBrush(QtGui.QColor(200, 0, 200))
        #painter.drawEllipse(self.rect)
        painter.drawEllipse(self.rect)
        #painter.drawLine(20, 160, 250, 160)

class circleInput( QtGui.QGraphicsItem ):
    def __init__( self, scene ):
        super(circleInput, self).__init__(None, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable)
        self.rect = QtCore.QRectF(-40, -20, 20, 20)
        #self.setPos(position)
        scene.clearSelection()
        
    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(3)
        
        if option.state & QtGui.QStyle.State_Selected:
            pen.setColor(QtCore.Qt.blue)
            print 'hallo'
            #print dir( self.data( 0 ) )
            #print self.data( 0 )..toString
            #print self.data( 0 ).type
        painter.setPen(pen)
        #brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        #painter.setBrush(brush)
        painter.setBrush(QtGui.QColor(200, 200, 0))
        #painter.drawEllipse(self.rect)
        painter.drawEllipse(self.rect)
        #painter.drawLine(20, 160, 250, 160)

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
    #categoryItemClicked = QtCore.pyqtSignal(QtCore.QObject)
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.setSceneRect(0, 0, *MapSize)
        #DraggableMark(QtCore.QPointF(92.0, 90.0), self)
        self.line = None

    def mousePressEvent(self, event):
        #super(GraphicsScene, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            print "Left mouse click"
            #return
        item = self.itemAt( event.scenePos() )
        print "item = %s" %item
        if event.button() == QtCore.Qt.LeftButton and ( isinstance( item, circleOutput ) ):
            self.line = QtGui.QGraphicsLineItem( QtCore.QLineF( event.scenePos(), event.scenePos() ) )
            self.addItem( self.line )


        modifiers = QtGui.QApplication.keyboardModifiers()
        pos = event.scenePos()
        if modifiers == QtCore.Qt.ControlModifier:
            print "Control + Click: (%d, %d)" % (pos.x(), pos.y()) 
            itemParent = DraggableMark(pos, self)
            circleInput( self ).setParentItem( itemParent )
            circleOutput( self ).setParentItem( itemParent )
            #self.addEllipse(QtCore.QRectF(pos.x(), pos.y(), 10, 10))
            #path1 = line( pos, self )#.setParentItem( itemParent )
        else:
            print "Click: (%d, %d)" % (pos.x(), pos.y())
            
#             start = QtCore.QPointF(self.mapToScene(self._start))
#             end = QtCore.QPointF(self.mapToScene(event.pos()))
#             self.scene().addItem(QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))

        super(GraphicsScene, self).mousePressEvent(event)
    
    def mouseMoveEvent( self, event ):
        if self.line:

            newLine = QtCore.QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(newLine)
        super(GraphicsScene, self).mouseMoveEvent(event)
        self.update()
        
    def mouseReleaseEvent( self, event ):
        
        if self.line:
            startItems = self.items( self.line.line().p1() )
            #print "startItems[0] = %s" %startItems
            if len(startItems) and startItems[0] == self.line:
                print "popping"
                print "len(startItems) = %i" %len(startItems)
                
                #print "SceneView.mouseReleaseEvent(): startItems = %s" %startItems
                startItems.pop(0)
                print "startItems popped = %s" %startItems
                
            
            
            try:
                print "startItems[ 0 ] = %s" %startItems[ 0 ]
            except:
                print "no startItems[ 0 ]"
            
            endItems = self.items( self.line.line().p2() )
             
            if len(endItems) and endItems[0] == self.line:
                print "popping"
                print "len(endItems) = %i" %len(endItems)
                
                #print "SceneView.mouseReleaseEvent(): endItems = %s" %endItems
                endItems.pop(0)
                print "endItems popped = %s" %endItems
                
            try:
                print "endItems[ 0 ] = %s" %endItems[ 0 ]
            except:
                print "no endItems[ 0 ]"
            #itemEnd = self.itemAt( event.scenePos() )
            self.removeItem( self.line )
            #pos = event.scenePos()
            #if event.button() == QtCore.Qt.LeftButton and ( isinstance( itemEnd, circleInput ) ):
            #newLine = line( startItems[ 1 ], endItems[ 1 ], self )
            #newLine.updatePosition()
            try:
                if ( isinstance( endItems[ 0 ], circleInput ) ):
                    print "is an input :)"
                    connectionLine = LineClass( startItems[ 0 ], endItems[ 0 ], QtCore.QLineF(startItems[ 0 ].scenePos(), endItems[ 0 ].scenePos() ) )
                    print "connectionLine = %s" %connectionLine
                    #connectionLine.myEndItem.lineConnected.emit()
                    #self.removeItem( self.line )
                    self.addItem( connectionLine )
                    #connectionLine.updatePosition()
                else:
                    print "is not an input :("
            except:
                print "no endItem chosen"

            
        self.line = None
        super(GraphicsScene, self).mouseReleaseEvent(event)
    
    



class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.scene = GraphicsScene(self)
        #self.scene.addRect(QtCore.QRectF(0, 0, *MapSize), QtCore.Qt.red)
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