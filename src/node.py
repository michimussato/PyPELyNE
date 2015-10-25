import datetime
import os
import glob
import subprocess
import getpass
import logging
import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from circlesInOut import *
# from screenCast import *
from timeTracker import *
from PyQt4.uic import *
from jobDeadline import *
# from errorClasses import *

import xml.etree.ElementTree as ET


class node(QGraphicsItem, QObject):
    nodeClicked = pyqtSignal()

    def __init__(self, main_window=None, scene=None, property_node_path=None, meta_task_path=None, meta_tool_path=None):
        super(node, self).__init__(None, scene)

        try:
            self.meta_task_path = meta_task_path
            self.meta_tool_path = meta_tool_path

            try:
                # print self.meta_task_path
                meta_task_file = open(self.meta_task_path)
                self.meta_task = json.load(meta_task_file)
                # print self.meta_task
                meta_task_file.close()
            except AttributeError, e:
                print 'self.meta_task', e

            try:
                # print self.meta_tool_path
                meta_tool_file = open(self.meta_tool_path)
                self.meta_tool = json.load(meta_tool_file)
                # print self.meta_tool
                meta_tool_file.close()

            except AttributeError, e:
                print 'self.meta_tool', e

        except IOError, e:
            print 'xml loading:', e
            self.propertyNodePath = property_node_path
            # print self.propertyNodePath



        self.main_window = main_window
        # self.pypelyne_root = self.main_window.pypelyne_root
        self.user = self.main_window.user
        self.location = self.getNodeRootDir()
        self.loaderSaver = os.path.basename(self.location)[:7]
        self.asset = os.path.dirname(self.location)
        self.project = os.path.dirname(os.path.dirname (os.path.dirname(self.asset)))
        self.scene = scene
        # self._tools = self.main_window.get_tools()
        self.tasks = self.main_window.getTasks()
        # self.exclusions = self.main_window._exclusions
        self.now = datetime.datetime.now()
        self.nowStr = str(self.now)
        self.rect = QRectF(0, 0, 200, 40)
        self.outputMaxWidth = []
        self.inputMaxWidth = []
        self.setAcceptHoverEvents(True)
        self.outputList = []
        self.inputList = []
        self.inputs = []
        self.incoming = []
        self.outputs = []
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.hovered = False
        self.setData(1, self.now)
        self.setData(2, 'node')
        #self.setToolTip('haha')
        self.setNodePosition()
        #print '===> fix corrupt %s' %(self.propertyNodePath)

        self.scene.clearSelection()
        self.labelBoundingRect = 0.0
        
        if not self.loaderSaver.startswith('LDR'):
            self.inputPort = self.newInput(scene)
        
        self.label = None
        
        #use this to add outputs from filesystem:
        self.addOutputs()
        self.addInputs()

        self.gradient = QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())
        self.taskColorItem = QColor(0, 0, 0)
        self.applicationColorItem = QColor(0, 0, 0)

        if not self.loaderSaver.startswith('SVR') and not self.loaderSaver.startswith('LDR'):
            self.newOutputButton()

        self.widgetMenu = None
        self.setTaskColor()
        self.setApplicationColor()

    def convert_xml_to_json(self):
        pass

    def getNodeAsset(self):
        return self.asset

    def getNodeProject(self):
        return self.project

    def getInputPort(self):
        return self.inputPort
        
    def getNodeRootDir(self):
        # print self.meta_task_path
        # print os.path.dirname(self.meta_task_path)
        # print os.path.dirname(os.path.realpath(self.meta_task_path))
        return os.path.dirname(self.meta_task_path)

    def getApplicationInfo(self):
        try:
            self.nodeVersion = self.meta_tool['release_number']
            self.nodeVendor = self.meta_tool['vendor']
            self.nodeFamily = self.meta_tool['family']
            self.nodeArch = self.meta_tool['architecture']
            # print self.meta_tool
            self.nodeTask = self.meta_task['task']
            self.node_creator = self.meta_task['creator']
            self.node_operating_system = self.meta_task['operating_system']
        except TypeError, e:
            print 'loader or saver? (%s)' % e

    def queryApplicationInfo(self):

        try:
            return self.nodeVersion, self.nodeVendor, self.nodeFamily, self.nodeArch, self.nodeTask
            #       [1][1]          [3][1]      [4][1]      [0][1]      [2][1]
            #       ('modelling',   'R 15',       'CINEMA 4D',  'x64',      'MAXON')
            #       [2][1]      [3][1]     [4][1]   [0][1]  [2][1]

        except TypeError, e:
            logging.warning('queryApplicationInfo for not yet available for saver and loader nodes (%s)' % e)

    def setNodePosition(self):
        try:
            pos_x = self.meta_task['pos_x']
            pos_y = self.meta_task['pos_y']
            print 'json reading'

        except TypeError, e:
            print e
            try:
                print self.propertyNodePath
                self.propertyNode = ET.parse(self.propertyNodePath)
                logging.info('new style reading xml')
                nodePosition = self.propertyNode.findall('./node')

                pos_x = nodePosition[0].items()[0][1]
                pos_y = nodePosition[0].items()[1][1]

            except:
                logging.info('old style reading xml')
                pos_x = self.propertyNode.findall('./positionX')
                pos_y = self.propertyNode.findall('./positionY')

                pos_x = pos_x[0].items()[0][1]
                pos_y = pos_y[0].items()[0][1]

        self.setPos(QPointF(float(pos_x), float(pos_y)))

        # TODO: switch to json reading
        self.getApplicationInfo()
    

    def hoverEnterEvent(self, event):
        self.hovered = True

    def hoverLeaveEvent(self, event):
        self.hovered = False

    def mousePressEvent(self, event):
        self.scene.nodeSelect.emit(self)

    def mouseDoubleClickEvent(self, event):
        if self.label.startswith('LDR'):
            self.main_window.get_content(node_label=self.label)

        else:
            search_string = self.nodeVendor + ' ' + self.nodeFamily + ' ' + self.nodeVersion + ' ' + self.nodeArch
            search_index = self.main_window.toolsComboBox.findText(search_string, Qt.MatchContains)

            if search_index < 3:
                if not str(self.nodeFamily + ' ' + self.nodeVersion) in [self.main_window.toolsComboBox.itemText(i) for i in range(self.main_window.toolsComboBox.count())]:
                    logging.warning('application family not available')
                    QMessageBox.critical(self.main_window, 'application warning', str('%s not available.' % str(self.nodeFamily + ' ' + self.nodeVersion)), QMessageBox.Abort, QMessageBox.Abort)
                    return

                elif self.nodeArch == 'x64':
                    reply = QMessageBox.warning(self.main_window, 'architecture warning', str('x64 version of %s not available. continue using x32?' %self.nodeFamily), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                    if reply == QMessageBox.Yes:
                        search_string = str(self.nodeVendor + ' ' + self.nodeFamily + ' ' + self.nodeVersion + ' ' + 'x32')
                        search_index = self.main_window.toolsComboBox.findText(QString(search_string), Qt.MatchContains) - 2
                        logging.warning('x64 not available. using x32 version.')
                    else:
                        return
                elif self.nodeArch == 'x32':
                    reply = QMessageBox.warning(self.main_window,
                                                'architecture warning',
                                                str('x32 version of %s not available. continue using x64?' % self.nodeFamily),
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.No)

                    if reply == QMessageBox.Yes:
                        search_string = str(self.nodeVendor + ' ' + self.nodeFamily + ' ' + self.nodeVersion + ' ' + 'x64')
                        search_index = self.main_window.toolsComboBox.findText(QString(search_string), Qt.MatchContains) - 2
                        logging.warning('x32 not available. using x64 version.')
                    else:
                        return
                else:
                    logging.warning('some weird shit')

            elif os.path.exists(os.path.join(self.location, 'locked')):
                QMessageBox.critical(self.main_window, 'node warning', str('%s is currently in use.' %str(self.label)), QMessageBox.Abort, QMessageBox.Abort)
                return

            elif os.path.exists(os.path.join(self.location, 'checkedOut')):
                QMessageBox.critical(self.main_window, 'node warning', str('%s is currently checked out.' %str(self.label)), QMessageBox.Abort, QMessageBox.Abort)
                return

            args = []

            for arg in self._tools[search_index][10]:
                args.append(arg)

            if self.nodeFamily == 'Maya':
                for arg in ['-proj', self.location, '-file']:
                    args.append(arg)

            projectRoot = os.path.join(self.location, 'project')

            extension = os.path.splitext(self._tools[search_index][7])[1]

            files = glob.glob1(projectRoot, str('*' + extension))

            absFiles = []

            for relFile in files:
                if relFile not in SETTINGS.EXCLUSIONS:
                    absFiles.append(os.path.join(projectRoot, relFile))

            if not 'DDL' in self.label:
                newestFile = max(absFiles, key=os.path.getctime)
                self.main_window.runTask(self, self._tools[search_index][1][0], newestFile, args)
            else:
                ok, jobDeadline = jobDeadlineUi.getDeadlineJobData(self.location, self.main_window)

                if ok:
                    txtFile = os.path.join(self.location, 'project', 'deadlineJob.txt')
                    jobFile = open(txtFile, 'w')

                    for element in jobDeadline:
                        jobFile.write(element)
                        jobFile.write(' ')

                    jobFile.close()

                    self.main_window.submitDeadlineJob(txtFile)

    def data_ready(self):
        cursor_box = self.main_window.statusBox.textCursor()
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText("%s (%s): %s" %(datetime.datetime.now(), self.pid, str(self.process.readAll())))
        self.main_window.statusBox.ensureCursorVisible()
    '''
    def hoverEnterEvent(self, event):
        pass
    
    def hoverLeaveEvent(self, event):
        pass
    '''

    def resizeWidth(self):
        outputListTextWidth = [0]
        inputListTextWidth = [0]

        for i in self.inputList:
            inputListTextWidth.append(int(i.childrenBoundingRect().width()))

        for i in self.outputList:
            outputListTextWidth.append(int(i.childrenBoundingRect().width()))

        self.rect.setWidth(max((self.labelBoundingRect + 40 + 20), (max(outputListTextWidth) + 80) + (max(inputListTextWidth))))
                
    def resizeHeight(self):
        self.rect.setHeight(((max(len(self.inputs) + 1, len(self.outputs) + 1) * 20)))
        self.gradient = QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())

    def resize(self):
        self.resizeHeight()
        self.resizeWidth()

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.SolidLine)
        pen.setColor(Qt.black)
        pen.setWidth(0)

        # try:

        if option.state & QStyle.State_Selected:
            self.update_meta_task()
            self.setZValue(1)
            pen.setWidth(1)
            pen.setColor(Qt.green)
            self.gradient.setColorAt(0, self.taskColorItem)
            self.gradient.setColorAt(1, self.applicationColorItem.darker(160))

            if os.path.exists(os.path.join(self.location, 'locked')):
                self.gradient.setColorAt(0, self.taskColorItem)
                self.gradient.setColorAt(1, Qt.red)

            elif os.path.exists(os.path.join(self.location, 'checkedOut')):
                self.gradient.setColorAt(0, self.taskColorItem)
                self.gradient.setColorAt(1, Qt.white)

        elif option.state & QStyle.State_MouseOver or self.hovered:
            pen.setWidth(1)
            pen.setColor(Qt.yellow)
            self.gradient.setColorAt(0, self.taskColorItem)
            self.gradient.setColorAt(1, self.applicationColorItem.darker(160))

            if os.path.exists(os.path.join(self.location, 'locked')):
                self.gradient.setColorAt(0, self.taskColorItem)
                self.gradient.setColorAt(1, Qt.red)

            elif os.path.exists(os.path.join(self.location, 'checkedOut')):
                self.gradient.setColorAt(0, self.taskColorItem)
                self.gradient.setColorAt(1, Qt.white)

        elif os.path.exists(os.path.join(self.location, 'locked')):
            self.gradient.setColorAt(0, self.taskColorItem)
            self.gradient.setColorAt(1, Qt.red)

        elif os.path.exists(os.path.join(self.location, 'checkedOut')):
            self.gradient.setColorAt(0, self.taskColorItem)
            self.gradient.setColorAt(1, Qt.white)

        else:
            pen.setWidth(0)
            self.setZValue(0)
            self.gradient.setColorAt(0, self.taskColorItem)
            self.gradient.setColorAt(1, self.applicationColorItem.darker(160))


        painter.setBrush(self.gradient)

        painter.setPen(pen)

        painter.drawRoundedRect(self.rect, 10.0, 10.0)

        for i in self.outputList:
            i.setPos(self.boundingRect().width() - i.rect.width(), i.pos().y())

        self.rect.setWidth(self.rect.width())
        self.arrangeOutputs()
        self.arrangeInputs()
        self.resize()
        # except:
        #     logging.warning('paint error for node %s (corrupt propertyNode.xml?)' %(self.label))
        
    def arrangeOutputs(self):
        for output in self.outputs:
            position = QPointF(self.boundingRect().width() - output.rect.width(), ((output.boundingRect().height() * (self.outputs.index(output) + 1))))
            output.setPos(position)

    def arrangeInputs(self):
        for input in self.inputs:
            position = QPointF(0, ((self.inputs.index(input) + 1) * input.boundingRect().height()))
            input.setPos(position)
        
    #add existing outputs from file system
    def addOutputs(self):
        
        self.outputRootDir = os.path.join(str(self.location), 'output')
        
        allOutputs = os.listdir(self.outputRootDir)
        
        for i in allOutputs:
            if i not in SETTINGS.EXCLUSIONS:
                self.newOutput(self, i)

    #add existing inputs from file system
    def addInputs(self):
        self.inputRootDir = os.path.join(str(self.location), 'input')
        allInputs = os.listdir(self.inputRootDir)
        for i in allInputs:
            if i not in SETTINGS.EXCLUSIONS:
                input = self.newInput(self.scene)
                try:
                    lookupDir = os.path.dirname(os.path.join(self.inputRootDir, os.readlink(os.path.join(self.inputRootDir, i))))
                except:
                    lookupDir = os.path.dirname(os.path.join(self.inputRootDir, os.path.join(self.inputRootDir, i)))

                try:
                    if not i in os.listdir(lookupDir) and os.path.basename(os.path.dirname(lookupDir)).startswith('LDR') == True:
                        os.remove(os.path.join(self.inputRootDir, i))
                        logging.warning('orphaned input found on node %s: %s removed' %(self.label, i))

                    else:

                        logging.info('input is still valid. %s kept' % i)
                except OSError, e:
                    print e

    #add new dynamic input
    def newInput(self, scene):
        input = portInput(self, scene, self.main_window)
        input.setParentItem(self)

        self.inputList.append(input)
        
        self.inputMaxWidth.append(input.childrenBoundingRect().width())
        
        self.resizeHeight()

    def update_meta_task(self):
        pos = self.scenePos()
        meta_task = self.meta_task

        meta_task['pos_x'] = pos.x()
        meta_task['pos_y'] = pos.y()

        with open(self.meta_task_path, 'w') as outfile:
            json.dump(meta_task, outfile)
            outfile.close()
        
    def updatePropertyNodeXML(self):
        pos = self.scenePos()
        propertyNode = ET.parse(self.propertyNodePath)
        propertyNodeRoot = propertyNode.getroot()
        
        try:
            #new style positioning...
            nodePosition = propertyNodeRoot.find('node')

            nodePosition.set('positionX', '%s' %pos.x())
            nodePosition.set('positionY', '%s' %pos.y())


        except:
            #old style positioning...
            positionX = propertyNodeRoot.find('positionX')
            positionY = propertyNodeRoot.find('positionY')

            positionX.set('value', '%s' %pos.x())
            positionY.set('value', '%s' %pos.y())
        
        xmlDoc = open(self.propertyNodePath, 'w')
        
        xmlDoc.write('<?xml version="1.0"?>')
        xmlDoc.write(ET.tostring(propertyNodeRoot))
        xmlDoc.close()

    #add new dynamic output:
    def newOutput(self, node, name):
        output = portOutput(self, name, self.main_window)

        if len(name.split('.')) > 1:

            output.addText(node, name.split('.')[3])

        else:
            output.addText(node, name)
        
        self.outputs.append(output)

        output.setParentItem(self)
        self.outputList.append(output)
        
        self.rect.setWidth(self.rect.width())
        
        self.outputMaxWidth.append(output.childrenBoundingRect().width())
        
        self.resizeHeight()

    def newOutputButton(self):
        outputButton = portOutputButton(self.main_window)
        
        outputButton.setParentItem(self)
    
    def sendFromNodeToBox(self, text):
        self.scene.textMessage.emit(text)
        
    def getLabel(self):
        return self.label

    @property
    def _label(self):
        return self.label

    def addText(self, text):
        self.setData(0, text)
        nodeLabel = QGraphicsTextItem(text)
        self.label = text
        nodeLabelColor = (QColor(255, 255, 255))
        nodeLabelColor.setNamedColor('#080808')
        nodeLabel.setDefaultTextColor(nodeLabelColor)
        nodeLabel.setPos(QPointF(25, 0))
        nodeLabel.setParentItem(self)
        self.labelBoundingRect = nodeLabel.boundingRect().width()

        self.resizeWidth()

    def setApplicationColor(self):
        self.applicationColorItem.setNamedColor(self.taskColor)

    def setTaskColor(self):
        index = 0

        # print self.location
        # print self.location[:7]

        if os.path.basename(self.location)[:7].startswith('LDR'):
            if os.path.basename(self.location)[:7].endswith('LIB'):
                self.taskColor = '#00FF00'
            else:
                for tab in self.main_window.content_tabs:
                    if os.path.basename(self.location)[:7].endswith(tab['abbreviation']):
                        self.taskColor = tab['loader_color']
                        break

        elif os.path.basename(self.location)[:7].startswith('SVR'):
            for tab in self.main_window.content_tabs:
                if os.path.basename(self.location)[:7].endswith(tab['abbreviation']):
                    self.taskColor = tab['saver_color']
            # if os.path.basename(self.location)[:7].endswith('AST'):
            #     self.taskColor = '#FFFF33'
            # elif os.path.basename(self.location)[:7].endswith('SHT'):
            #     self.taskColor = '#3333FF'

        else:

            for i in self.tasks:
                # print i
                # print self.nodeTask
                if [item for item in i if self.nodeTask in item]:
                    # print self.tasks[index][0][1]
                    logging.info('task color description found')
                    self.taskColor = self.tasks[index][0][1]
                    break
                else:
                    index += 1

        self.taskColorItem.setNamedColor(self.taskColor)


