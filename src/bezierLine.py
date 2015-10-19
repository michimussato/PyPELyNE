'''
Created on Dec 15, 2014

@author: michaelmussato
'''

import os, logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class bezierLine(QGraphicsPathItem):
    def __init__(self, mainwindow, scene, startItem, endItem, *args, **kwargs):
        super(bezierLine, self).__init__(*args, **kwargs)
        self.mainwindow = mainwindow
        self.outputs = self.mainwindow._outputs
        self.startItemOutputDir = startItem.outputDir
        self.startItemLiveDir = startItem.liveDir
        self.scene = scene
        self.pathItem = None
        self.myStartItem = startItem
        self.myEndItem = endItem
        self.myColor = Qt.black
        self.setZValue(-1.0)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)

        self.setActive(True)

        self.hovered = False

        self.qp = QPainterPathStroker()
        self.qp.setWidth(10)
        self.qp.setCapStyle(Qt.SquareCap)
        self.shape = self.qp.createStroke(self.getLine())

        self.setPen(QPen(self.myColor, 2))
        self.getEndItem()

        self.label = str(startItem.label)
        self.myEndItem.addText(self.label)

        self.pathColorItem = QColor(0, 0, 0)
        self.setPathColor()
        #self.setBoundingRegionGranularity(0.1)
        
    def hoverEnterEvent(self, event):
        self.hovered = True
        self.myStartItem.hovered = True
        self.myEndItem.hovered = True
        
    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.myStartItem.hovered = False
        self.myEndItem.hovered = False

    def mouseMoveEvent(self, event):
        pass

    def shape(self):
        return self.shape

    def paint(self, painter, option, widget):
        line = self.getLine()

        pen = self.pen()
        pen.setWidth(2)
        painter.setRenderHint(QPainter.Antialiasing)

        if not os.path.isdir(self.startItemLiveDir):
            pen.setStyle(Qt.CustomDashLine)
            pen.setDashPattern([1, 4])

        else:
            pen.setStyle(Qt.SolidLine)

        if self.hovered:
            pen.setWidth(3)
            self.setZValue(-1)
            pen.setColor(self.pathColorItem.lighter(150))

        else:
            self.setZValue(-2)
            pen.setColor(self.pathColorItem)

        painter.setPen(pen)

        self.setPath(line)

        painter.drawPath(line)

    def getEndItem(self):
        return self.myEndItem

    def getStartItem(self):
        return self.myStartItem
    
    def getLine(self):
        p1 = QPointF(self.myStartItem.sceneBoundingRect().center().x() + 10, self.myStartItem.sceneBoundingRect().center().y())
        p4 = QPointF(self.myEndItem.sceneBoundingRect().center().x() - 10, self.myEndItem.sceneBoundingRect().center().y())
        if (p1.x() + 40) < p4.x():
            p2 = QPointF((p4.x() - p1.x()) / 2 + p1.x() + 40, p1.y())
            p3 = QPointF((p4.x() - p1.x()) / 2 + p1.x() - 40, p4.y())

        elif (p1.x() + 40) >= p4.x():
            p2 = QPointF((p4.x() - p1.x()) / 2 + p1.x() + 40 + (((p1.x() + 40) - p4.x())), p1.y())
            p3 = QPointF((p4.x() - p1.x()) / 2 + p1.x() - 40 - (((p1.x() + 40) - p4.x())), p4.y())

        path = QPainterPath(p1)

        path.cubicTo(p2, p3, p4)

        self.shape = self.qp.createStroke(path)

        return path

    def setPathColor(self):
        self.nodeOutput = self.label.split('__')[0]

        index = 0
        found = False
        for i in self.outputs:
            if found == False:
                for j in i:
                    if found == False:
                        if [item for item in j if self.nodeOutput in item and not 'mime' in item]:
                            found = True
                            outputIndex = index
                            self.pathColor = self.outputs[outputIndex][0][0][1]
                            break

                index += 1
            else:
                break

        self.pathColorItem.setNamedColor(self.pathColor)