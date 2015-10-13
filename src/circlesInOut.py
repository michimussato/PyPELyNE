'''
Created on Dec 15, 2014

@author: michaelmussato
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import random, os


    
    

class portOutput(QGraphicsItem):
    def __init__(self, node, name, mainWindow):
        super(portOutput, self).__init__(None)

        self.setFlags(QGraphicsItem.ItemIsSelectable)

        self.mainWindow = mainWindow
        #print mainWindow.exclusions
        #self.exclusions = self.mainWindow.getExclusions()
        self.exclusions = self.mainWindow.exclusions
        #self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.pypelyneRoot = self.mainWindow.pypelyneRoot
        #self.projectsRoot = self.mainWindow.getProjectsRoot()
        self.projectsRoot = self.mainWindow.projectsRoot
        #self.currentPlatform = self.mainWindow.getCurrentPlatform()
        self.currentPlatform = self.mainWindow.currentPlatform

        self.node = node
        self.nodeRoot = self.node.location
        self.nodeProject = self.node.project

        self.setAcceptHoverEvents(True)

        #self._outputs = self.mainWindow.getOutputs()
        self._outputs = self.mainWindow._outputs

        self.portOutputColorItem = QColor(0, 0, 0)
        self.portOutputRingColorItem = QColor(0, 0, 0)

        #self.outputDir = os.path.normpath(os.path.join(node.getNodeRootDir(), 'output', name))
        self.outputDir = os.path.normpath(os.path.join(self.nodeRoot, 'output', name))
        #self.liveDir = os.path.normpath(os.path.join(node.getNodeRootDir(), 'live', name))
        self.liveDir = os.path.normpath(os.path.join(self.nodeRoot, 'live', name))
        #self.nodeRoot = self.node.getNodeRootDir()



        #print self.outputDir
        #print self.liveDir

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
        #returns /path/to/projects/project/content/assets/asset/node

    def getOutputProjectDir(self):
        return self.nodeProject
    #returns /path/to/projects/project

    def getOutputDir(self):
        return self.outputDir
        #returns /path/to/projects/project/content/assets/asset/node/output/outputLabel

    def getLiveDir(self):
        return self.liveDir
        #returns /path/to/projects/project/content/assets/asset/node/live/outputLabel
        
    def arrange(self, node):
        self.setPos(node.boundingRect().width() - self.rect.width(), ((self.boundingRect().height() * (len(node.outputList) + 1))))
        
    def getLabel(self):
        return self.label
    
    def addText(self, node, name):
        
        textPortOutput = QGraphicsTextItem(str(name), parent = self)
        self.label = name

        textPortOutput.setDefaultTextColor(self.portOutputColorItem.darker(250))
        
        textPortOutput.setPos(QPointF(0 - textPortOutput.boundingRect().width(), 0))
        
    def boundingRect(self):
        return self.rect

    def hoverEnterEvent(self, event):
        #print 'enter'
        self.hovered = True
        #print self.inputs
        for input in self.inputs:
            input.hovered = True
            input.connection[0].hovered = True
        #print self.childItems()
        #print self.parentItem()

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
        if len(str(self.data(0).toPyObject()).split('.')) > 1:
            self.nodeOutput = str(self.data(0).toPyObject()).split('.')[3].split('__')[0]

        else:
            self.nodeOutput = str(self.data(0).toPyObject()).split('__')[0]

        index = 0
        found = False
        for i in self._outputs:
            if found == False:
                
                for j in i:
                    if found == False:
                        if [item for item in j if self.nodeOutput in item and not 'mime' in item]:
                            found = True
                            outputIndex = index

                            self.portOutputColor = self._outputs[outputIndex][0][0][1]

                            break
                index += 1
            else:
                break

        if os.path.exists(self.liveDir):
            if self.currentPlatform == 'Darwin' or self.currentPlatform == 'Linux':
                #print 'outputDir:', self.outputDir
                if os.path.exists(os.path.join(self.outputDir, 'current')):
                    if not os.path.basename(os.readlink(self.liveDir)) == os.readlink(os.path.join(self.outputDir, 'current')):
                        path = os.path.join(self.outputDir, 'current')
                        content = os.listdir(path)
                        for exclusion in self.exclusions:
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
                    #print os.path.basename(self.liveDir).split('.')[-1]
                    #print os.readlink(self.liveDir)
                    #print os.path.abspath(os.readlink(self.liveDir))
                    #print os.path.basename(os.path.abspath(os.readlink(self.liveDir)))

                    #print 'liveDir:', self.liveDir
                    try:
                        outputName = os.path.basename(os.path.abspath(os.readlink(self.liveDir)))
                    except:
                        outputName = self.liveDir.split('.')[-1]
                    #outputName = os.path.basename(self.liveDir).split('.')[-1]
                    #print 'outputName:', outputName


                    #print os.path.dirname(os.path.dirname(os.path.abspath(os.readlink(self.liveDir))))
                    try:
                        srcPath = os.path.dirname(os.path.dirname(os.path.abspath(os.readlink(self.liveDir))))[1:]
                        #print 'srcPath:', srcPath


                        #print os.path.basename(os.path.join(srcPath, 'live', outputName))
                        #print self.projectsRoot
                        #print self.projectsRoot
                        #print srcPath
                        #print os.path.join(self.projectsRoot, srcPath, 'output', outputName, 'current')
                        #print os.path.join(self.projectsRoot, srcPath, 'live', outputName)


                        if not os.readlink(os.path.join(self.projectsRoot, srcPath, 'output', outputName, 'current')) == os.path.basename(os.readlink(os.path.join(self.projectsRoot, srcPath, 'live', outputName))):
                            path = os.path.join(self.projectsRoot, srcPath, 'output', outputName, 'current')
                            content = os.listdir(path)
                            for exclusion in self.exclusions:
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
                        #we have a library loader here:
                        self.portOutputRingColorItem.setNamedColor(self.outputColorOnline)

            elif self.currentPlatform == 'Windows':
                if os.path.exists(os.path.join(self.outputDir, 'current')):
                    if not os.path.basename(os.path.realpath(self.liveDir)) == os.path.realpath(os.path.join(self.outputDir, 'current')):
                        path = os.path.join(self.outputDir, 'current')
                        content = os.listdir(path)
                        for exclusion in self.exclusions:
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

                    #print os.path.basename(os.path.join(srcPath, 'live', outputName))
                    #print self.projectsRoot
                    #print self.projectsRoot
                    #print srcPath
                    #print os.path.join(self.projectsRoot, srcPath, 'output', outputName, 'current')
                    #print os.path.join(self.projectsRoot, srcPath, 'live', outputName)


                    if not os.path.realpath(os.path.join(self.projectsRoot, srcPath, 'output', outputName, 'current')) == os.path.basename(os.path.realpath(os.path.join(self.projectsRoot, srcPath, 'live', outputName))):
                        path = os.path.join(self.projectsRoot, srcPath, 'output', outputName, 'current')
                        content = os.listdir(path)
                        for exclusion in self.exclusions:
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
            #output with no live data found
            self.portOutputRingColorItem.setNamedColor(self.outputcolorNoLive)



        if self.hovered:
            self.portOutputColorItem.setNamedColor(self.portOutputColor)
            self.portOutputColorItem = self.portOutputColorItem.lighter(150)
        else:
            self.portOutputColorItem.setNamedColor(self.portOutputColor)



class portInput(QGraphicsItem):
    def __init__(self, node, scene, mainWindow):
        super(portInput, self).__init__(None)
        self.setFlags(QGraphicsItem.ItemIsSelectable)

        self.mainWindow = mainWindow

        self._outputs = self.mainWindow._outputs

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

        #self.setAcceptHoverEvents(True)
        #self.setAcceptTouchEvents(True)

        #self.setActive(True)
        
        self.label = None
        self.setData(2, 'input')
        
        self.inputDir = None

        self.portInputColorItem = QColor(0, 0, 0, 0)
        self.gradient = QLinearGradient(self.rect.topLeft(), self.rect.topRight())
        

    def hoverEnterEvent(self, event):
        #print 'enter'
        #print self.childItems()
        #print self.parentItem()
        try:
            self.hovered = True
            self.connection[0].hovered = True
            self.output[0].hovered = True
        except:
            pass

    def hoverLeaveEvent(self, event):
        #print 'left'
        try:
            self.hovered = False
            self.connection[0].hovered = False
            self.output[0].hovered = False
        except:
            pass


    def getLabel(self):
        return self.label
    
    def setInputDir(self, dir):
        self.inputDir = dir
    
    def getInputDir(self):
        return self.inputDir
        
    
    def addText(self, name):
        textPortInput = QGraphicsTextItem(name, parent = self)
        self.label = name
        textPortInput.setDefaultTextColor(Qt.black)
        
        textPortInput.setPos(QPointF(self.boundingRect().width(), 0))


    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        #print self.zValue()

        #print self.hovered

        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.SolidLine)
        pen.setColor(Qt.black)
        pen.setWidth(3)

        if self.hovered:
            pass
            #pen.setWidth(5)
            #self.setZValue(3)
        else:
            pass
            #pen.setWidth(3)
            #self.setZValue(-1)

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
        #print self.label
        if len(self.label.split('.')) > 1:
            self.nodeInput = self.label.split('.')[3].split('__')[0]

        else:
            self.nodeInput = self.label.split('__')[0]



        #print self.nodeInput
        index = 0
        found = False
        for i in self._outputs:
            if found == False:

                for j in i:
                    #print j
                    if found == False:
                        #print self._outputs[index][0][0][1]
                        if [item for item in j if self.nodeInput in item and not 'mime' in item]:

                            found = True
                            #print 'found = %s' %(found)
                            inputIndex = index

                            self.portInputColor = self._outputs[inputIndex][0][0][1]

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
    def __init__(self, node, name, mainWindow):
        super(portOutputButton, self).__init__(None)

        self.mainWindow = mainWindow
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.rect = QRectF(0, 0, 20, 20)
        self.icon = []
        self.icon.append(QLine(10, 6, 10, 14))
        self.icon.append(QLine(6, 10, 14, 10))


    def addText(self, node, name):
        item = QGraphicsTextItem('port = %s' %name, parent = self)
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


