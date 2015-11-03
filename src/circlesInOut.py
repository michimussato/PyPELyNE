from PyQt4.QtCore import *
from PyQt4.QtGui import *

import random, os

import settings as SETTINGS


class portOutput(QGraphicsItem):
    def __init__(self, node, name, main_window):
        super(portOutput, self).__init__(None)

        self.setFlags(QGraphicsItem.ItemIsSelectable)

        self.main_window = main_window

        self.node = node
        self.nodeRoot = self.node.location
        self.nodeProject = self.node.project

        self.setAcceptHoverEvents(True)

        self.portOutputColorItem = QColor(0, 0, 0)
        self.portOutputRingColorItem = QColor(0, 0, 0)

        self.outputDir = os.path.normpath(os.path.join(self.nodeRoot, 'output', name))
        self.liveDir = os.path.normpath(os.path.join(self.nodeRoot, 'live', name))

        self.outputColorOnline = '#00FF00'
        self.outputColorNearline = '#FFFF00'
        self.outputColorEmpty = '#FF0000'
        self.outputcolorNoLive = '#FFFFFF'
        
        self.connectedTo = []
        
        self.inputs = []

        self.hovered = False
        
        self.rect = QRectF(0, 0, 20, 20)
        
        self.setData(0, name)
        self.setData(2, 'output')

        self.label = None

        self.gradient = QLinearGradient(self.rect.topLeft(), self.rect.topRight())

    def getOutputRootDir(self):
        return self.nodeRoot
        # returns /path/to/projects/project/content/assets/asset/node

    def getOutputProjectDir(self):
        return self.nodeProject
        # returns /path/to/projects/project

    def getOutputDir(self):
        return self.outputDir
        # returns /path/to/projects/project/content/assets/asset/node/output/outputLabel

    def getLiveDir(self):
        return self.liveDir
        # returns /path/to/projects/project/content/assets/asset/node/live/outputLabel
        
    def arrange(self, node):
        self.setPos(node.boundingRect().width() - self.rect.width(), (self.boundingRect().height() * (len(node.outputList) + 1)))
        
    def get_label(self):
        return self.label
    
    def add_text(self, node, name):
        
        text_port_output = QGraphicsTextItem(str(name), parent=self)
        self.label = name

        text_port_output.setDefaultTextColor(self.portOutputColorItem.darker(250))
        
        text_port_output.setPos(QPointF(0 - text_port_output.boundingRect().width(), 0))
        
    def boundingRect(self):
        return self.rect

    def hoverEnterEvent(self, event):
        self.hovered = True
        for input in self.inputs:
            input.hovered = True
            input.connection[0].hovered = True

    def hoverLeaveEvent(self, event):
        #print 'left'
        self.hovered = False
        for input in self.inputs:
            input.hovered = False
            input.connection[0].hovered = False

    def paint(self, painter, option, widget):
        self.setPortOutputColor()
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.SolidLine)
        pen.setColor(Qt.black)
        pen.setWidth(3)

        self.gradient.setColorAt(0, self.portOutputRingColorItem)
        self.gradient.setColorAt(0.3, self.portOutputRingColorItem)
        self.gradient.setColorAt(0.4, self.portOutputColorItem)
        self.gradient.setColorAt(1, self.portOutputColorItem)

        if self.hovered:
            pass
            #self.setZValue(3)
        else:
            pass
            #self.setZValue(-1)

        painter.setPen(pen)

        painter.setBrush(self.gradient)

        painter.drawEllipse(self.rect)

    def setPortOutputColor(self):
        if len(str(self.data(0)).split('.')) > 1:

            self.nodeOutput = str(self.data(0)).split('.')[3].split('__')[0]

        else:
            self.nodeOutput = str(self.data(0)).split('__')[0]

        index = 0
        found = False
        for i in self.main_window.outputs:
            if found == False:
                
                for j in i:
                    if found == False:
                        if [item for item in j if self.nodeOutput in item and 'mime' not in item]:
                            found = True
                            outputIndex = index

                            self.portOutputColor = self.main_window.outputs[outputIndex][0][0][1]

                            break
                index += 1
            else:
                break

        if os.path.exists(self.liveDir):
            if self.main_window.current_platform == 'Darwin' or self.main_window.current_platform == 'Linux':
                if os.path.exists(os.path.join(self.outputDir, 'current')):
                    if not os.path.basename(os.readlink(self.liveDir)) == os.readlink(os.path.join(self.outputDir, 'current')):
                        path = os.path.join(self.outputDir, 'current')
                        content = os.listdir(path)
                        for exclusion in SETTINGS.EXCLUSIONS:
                            if exclusion in content:
                                content.remove(exclusion)
                                try:
                                    os.remove(os.path.join(path, exclusion))
                                    print 'exclusion removed: %s' %(os.path.join(path, exclusion))
                                except:
                                    print 'could not remove: %s' %(os.path.join(path, exclusion))
                        if len(content) <= 1:
                            self.portOutputRingColorItem.setNamedColor(self.outputColorEmpty)
                        else:
                            self.portOutputRingColorItem.setNamedColor(self.outputColorNearline)
                    else:
                        self.portOutputRingColorItem.setNamedColor(self.outputColorOnline)

                else:
                    try:
                        outputName = os.path.basename(os.path.abspath(os.readlink(self.liveDir)))

                    except:
                        outputName = self.liveDir.split('.')[-1]

                    try:
                        srcPath = os.path.dirname(os.path.dirname(os.path.abspath(os.readlink(self.liveDir))))[1:]
                        if not os.readlink(os.path.join(self.main_window.projects_root, srcPath, 'output', outputName, 'current')) == os.path.basename(os.readlink(os.path.join(self.main_window.projects_root, srcPath, 'live', outputName))):
                            path = os.path.join(self.main_window.projects_root, srcPath, 'output', outputName, 'current')
                            content = os.listdir(path)
                            for exclusion in SETTINGS.EXCLUSIONS:
                                if exclusion in content:
                                    content.remove(exclusion)
                                    try:
                                        os.remove(os.path.join(path, exclusion))
                                        print 'exclusion removed: %s' %(os.path.join(path, exclusion))
                                    except:
                                        print 'could not remove: %s' %(os.path.join(path, exclusion))

                            if len(content) <= 1:
                                self.portOutputRingColorItem.setNamedColor(self.outputColorEmpty)
                            else:
                                self.portOutputRingColorItem.setNamedColor(self.outputColorNearline)

                        else:
                            self.portOutputRingColorItem.setNamedColor(self.outputColorOnline)
                    except:
                        # we have a library loader here:
                        self.portOutputRingColorItem.setNamedColor(self.outputColorOnline)

            elif self.main_window.current_platform == 'Windows':
                if os.path.exists(os.path.join(self.outputDir, 'current')):
                    if not os.path.basename(os.path.realpath(self.liveDir)) == os.path.realpath(os.path.join(self.outputDir, 'current')):
                        path = os.path.join(self.outputDir, 'current')
                        content = os.listdir(path)
                        for exclusion in SETTINGS.EXCLUSIONS:
                            if exclusion in content:
                                content.remove(exclusion)
                                try:
                                    os.remove(os.path.join(path, exclusion))
                                    print 'exclusion removed: %s' %(os.path.join(path, exclusion))
                                except:
                                    print 'could not remove: %s' %(os.path.join(path, exclusion))
                        if len(content) <= 1:
                            self.portOutputRingColorItem.setNamedColor(self.outputColorEmpty)
                        else:
                            self.portOutputRingColorItem.setNamedColor(self.outputColorNearline)
                    else:
                        self.portOutputRingColorItem.setNamedColor(self.outputColorOnline)

                else:
                    outputName = os.path.basename(os.path.abspath(os.path.realpath(self.liveDir)))
                    srcPath = os.path.dirname(os.path.dirname(os.path.abspath(os.path.realpath(self.liveDir))))[1:]

                    if not os.path.realpath(os.path.join(self.main_window.projects_root, srcPath, 'output', outputName, 'current')) == os.path.basename(os.path.realpath(os.path.join(self.main_window.projects_root, srcPath, 'live', outputName))):
                        path = os.path.join(self.main_window.projects_root, srcPath, 'output', outputName, 'current')
                        content = os.listdir(path)
                        for exclusion in SETTINGS.EXCLUSIONS:
                            if exclusion in content:
                                content.remove(exclusion)
                                try:
                                    os.remove(os.path.join(path, exclusion))
                                    print 'exclusion removed: %s' %(os.path.join(path, exclusion))
                                except:
                                    print 'could not remove: %s' %(os.path.join(path, exclusion))

                        if len(content) <= 1:
                            self.portOutputRingColorItem.setNamedColor(self.outputColorEmpty)
                        else:
                            self.portOutputRingColorItem.setNamedColor(self.outputColorNearline)

                    else:
                        self.portOutputRingColorItem.setNamedColor(self.outputColorOnline)

        else:
            # output with no live data found
            self.portOutputRingColorItem.setNamedColor(self.outputcolorNoLive)

        if self.hovered:
            self.portOutputColorItem.setNamedColor(self.portOutputColor)
            self.portOutputColorItem = self.portOutputColorItem.lighter(150)
        else:
            self.portOutputColorItem.setNamedColor(self.portOutputColor)


class portInput(QGraphicsItem):
    def __init__(self, node, scene, main_window):
        super(portInput, self).__init__(None)
        self.setFlags(QGraphicsItem.ItemIsSelectable)

        self.main_window = main_window

        self.portInputColorItem = QColor(0, 0, 0)
        self.portInputRingColorItem = QColor(0, 0, 0)
        
        self.scene = scene
        self.node = node

        self.rect = QRectF(0, 0, 20, 20)
        
        self.connection = []
        self.output = []
        
        self.setPos(0, 0)

        self.hovered = False

        self.setAcceptHoverEvents(True)

        self.icon = []
        self.icon.append(QLine(10, 14, 6, 10))
        self.icon.append(QLine(10, 14, 14, 10))

        self.label = None
        self.setData(2, 'input')
        
        self.inputDir = None

        self.portInputColorItem = QColor(0, 0, 0, 0)
        self.gradient = QLinearGradient(self.rect.topLeft(), self.rect.topRight())
        
    def hoverEnterEvent(self, event):
        try:
            self.hovered = True
            self.connection[0].hovered = True
            self.output[0].hovered = True
        except:
            pass

    def hoverLeaveEvent(self, event):
        try:
            self.hovered = False
            self.connection[0].hovered = False
            self.output[0].hovered = False
        except:
            pass

    def get_label(self):
        return self.label
    
    def setInputDir(self, dir):
        self.inputDir = dir
    
    def getInputDir(self):
        return self.inputDir

    def add_text(self, name):
        text_port_input = QGraphicsTextItem(name, parent=self)
        self.label = name
        text_port_input.setDefaultTextColor(Qt.black)
        
        text_port_input.setPos(QPointF(self.boundingRect().width(), 0))

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.SolidLine)
        pen.setColor(Qt.black)
        pen.setWidth(3)

        if self.hovered:
            pass
            # pen.setWidth(5)
            # self.setZValue(3)
        else:
            pass
            # pen.setWidth(3)
            # self.setZValue(-1)

        painter.setPen(pen)

        if self.label == None:
            if len(self.connection) == 0:
                painter.setBrush(QColor(0, 0, 0, 0))
                for i in self.icon:
                    painter.drawLine(i)
            elif len(self.connection) == 1:
                painter.setBrush(self.portInputColorItem.lighter(150))

        else:
            self.setPortInputColor()
            painter.setBrush(self.portInputColorItem)

        painter.drawEllipse(self.rect)

    def setPortInputColor(self):
        if len(self.label.split('.')) > 1:
            self.nodeInput = self.label.split('.')[3].split('__')[0]

        else:
            self.nodeInput = self.label.split('__')[0]

        index = 0
        found = False
        for i in self.main_window.outputs:
            if found == False:
                for j in i:
                    if found == False:
                        if [item for item in j if self.nodeInput in item and not 'mime' in item]:

                            found = True
                            inputIndex = index

                            self.portInputColor = self.main_window.outputs[inputIndex][0][0][1]

                            break
                index += 1
            else:
                break

        if self.hovered:
            #print 'hover hello'
            self.portInputColorItem.setNamedColor(self.portInputColor)
            self.portInputColorItem = self.portInputColorItem.lighter(150)
        else:
            self.portInputColorItem.setNamedColor(self.portInputColor)


class portOutputButton(QGraphicsItem):
    def __init__(self, main_window):
        super(portOutputButton, self).__init__(None)

        self.main_window = main_window
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.rect = QRectF(0, 0, 20, 20)
        self.icon = []
        self.icon.append(QLine(10, 6, 10, 14))
        self.icon.append(QLine(6, 10, 14, 10))

    def add_text(self, node, name):
        item = QGraphicsTextItem('port = %s' % name, parent=self)
        item.setDefaultTextColor(Qt.black)
        item.setPos(QPointF(((node.childrenBoundingRect().width()) - item.boundingRect().width()) - 30, 30))

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.SolidLine)
        pen.setColor(Qt.black)
        pen.setWidth(3)

        painter.setPen(pen)
        painter.setBrush(QColor(0, 0, 0, 0))
        painter.drawEllipse(self.rect)
        for i in self.icon:
            painter.drawLine(i)
        
        self.setPos(self.parentItem().boundingRect().width() - self.boundingRect().width(), self.boundingRect().height() * 0)


