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
                meta_task_file = open(self.meta_task_path)
                self.meta_task = json.load(meta_task_file)
                meta_task_file.close()
            except AttributeError, e:
                print 'self.meta_task', e

            try:
                meta_tool_file = open(self.meta_tool_path)
                self.meta_tool = json.load(meta_tool_file)
                meta_tool_file.close()
            except AttributeError, e:
                print 'self.meta_tool', e

        except IOError, e:
            print 'xml loading:', e
            self.propertyNodePath = property_node_path

        self.main_window = main_window
        self.user = self.main_window.user
        self.location = self.getNodeRootDir()
        self.loaderSaver = os.path.basename(self.location)[:7]
        self.asset = os.path.dirname(self.location)
        self.project = os.path.dirname(os.path.dirname (os.path.dirname(self.asset)))
        self.scene = scene
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

    def getNodeAsset(self):
        return self.asset

    def getNodeProject(self):
        return self.project

    def getInputPort(self):
        return self.inputPort
        
    def getNodeRootDir(self):
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

    def mouseDoubleClickEvent(self, event=None):
        if self.label.startswith('LDR'):
            self.main_window.get_content(node_label=self.label)

        else:
            run_task = {}

            run_task['family'] = None
            run_task['release_number'] = None
            run_task['project_template'] = None
            run_task['executable'] = None
            # run_task['architecture_fallback'] = False
            run_task['flags'] = None
            run_task['label'] = None

            if os.path.exists(os.path.join(self.location, 'locked')):
                QMessageBox.critical(self.main_window, 'node warning', str('%s is currently in use.' % self.label), QMessageBox.Abort, QMessageBox.Abort)
                return

            if os.path.exists(os.path.join(self.location, 'checkedOut')):
                QMessageBox.critical(self.main_window, 'node warning', str('%s is currently checked out.' % self.label), QMessageBox.Abort, QMessageBox.Abort)
                return

            for tool in self.main_window._tools:
                # print tool
                if self.meta_tool['family'] == tool['family']:
                    run_task['family'] = tool['family']
                    if self.meta_tool['release_number'] == tool['release_number']:
                        run_task['release_number'] = tool['release_number']
                        run_task['project_template'] = tool['project_template']
                        # run_task['project_workspace'] = tool['project_workspace']
                        # print tool
                        if self.meta_tool['architecture'] == 'x64':
                            if self.meta_tool['architecture_fallback']:
                                print 'this is a %s %s %s task, but can fallback to x32' % (tool['family'], tool['release_number'], self.meta_tool['architecture'])
                                if bool(tool['executable_x64']):
                                    if os.path.exists(tool['executable_x64']):
                                        print 'x64 found.'
                                        run_task['executable'] = tool['executable_x64']
                                        # run_task['architecture_fallback'] = False
                                        run_task['flags'] = tool['flags_x64']
                                        run_task['label'] = tool['label_x64']

                                if bool(tool['executable_x32']) and run_task['executable'] is None:
                                    if os.path.exists(tool['executable_x32']):
                                        reply = QMessageBox.warning(self.main_window,
                                                    'architecture warning',
                                                    'x64 version of %s %s not available. use x32?' % (run_task['family'], run_task['release_number']),
                                                    QMessageBox.Yes | QMessageBox.No,
                                                    QMessageBox.No)
                                        if reply == QMessageBox.Yes:
                                            print 'x64 not found. using x32.'
                                            run_task['executable'] = tool['executable_x32']
                                            # run_task['architecture_fallback'] = True
                                            run_task['label'] = tool['label_x32']
                                            run_task['flags'] = tool['flags_x32']

                                        else:
                                            print 'dont use x32 instead of x64.'

                                    else:
                                        print 'x32 and x64 not found.'

                            else:
                                print 'this is a %s %s %s task (cannot fallback)' % (tool['family'], tool['release_number'], self.meta_tool['architecture'])
                                if bool(tool['executable_x64']):
                                    if os.path.exists(tool['executable_x64']):
                                        print 'x64 found'
                                        run_task['executable'] = tool['executable_x64']
                                        run_task['flags'] = tool['flags_x64']
                                        run_task['label'] = tool['label_x64']

                                    else:
                                        print 'x64 not found'

                        elif self.meta_tool['architecture'] == 'x32':
                            if self.meta_tool['architecture_fallback']:
                                print 'this is a %s %s %s task, but can fallback to x64.' % (tool['family'], tool['release_number'], self.meta_tool['architecture'])
                                if bool(tool['executable_x32']):
                                    if os.path.exists(tool['executable_x32']):
                                        print 'x32 found.'
                                        run_task['executable'] = tool['executable_x32']
                                        # run_task['architecture_fallback'] = False
                                        run_task['flags'] = tool['flags_x32']
                                        run_task['label'] = tool['label_x32']

                                    if bool(tool['executable_x64']) and run_task['executable'] is None:
                                        if os.path.exists(tool['executable_x64']):
                                            reply = QMessageBox.warning(self.main_window,
                                                        'architecture warning',
                                                        'x32 version of %s %s not available. use x64?' % (run_task['family'], run_task['release_number']),
                                                        QMessageBox.Yes | QMessageBox.No,
                                                        QMessageBox.No)
                                            if reply == QMessageBox.Yes:
                                                print 'x32 not found. using x64.'
                                                run_task['executable'] = tool['executable_x64']
                                                # run_task['architecture_fallback'] = True
                                                run_task['label'] = tool['label_x64']
                                                run_task['flags'] = tool['flags_x64']

                                            else:
                                                print 'dont use x32 instead of x64.'

                                    else:
                                        print 'x32 and x64 not found.'

                            else:
                                print 'this is a %s %s %s task (cannot fallback)' % (tool['family'], tool['release_number'], self.meta_tool['architecture'])
                                if bool(tool['executable_x32']):
                                    if os.path.exists(tool['executable_x32']):
                                        print 'x32 found'
                                        run_task['executable'] = tool['executable_x32']
                                        run_task['flags'] = tool['flags_x32']
                                        run_task['label'] = tool['label_x32']

                                    else:
                                        print 'x32 not found'

            if run_task['executable'] is None:
                QMessageBox.critical(self.main_window, 'node warning', str('no suitable tool found to launch task %s.' % self.label), QMessageBox.Abort, QMessageBox.Abort)
                return

            if self.nodeFamily == 'Maya':
                for arg in ['-proj', self.location, '-file']:
                    run_task['flags'].append(arg)

            project_root_task = os.path.join(self.location, 'project')

            extension = os.path.splitext(run_task['project_template'])[1]

            files = glob.glob1(project_root_task, str('*' + extension))

            abs_files = []

            for rel_file in files:
                if rel_file not in SETTINGS.EXCLUSIONS:
                    abs_files.append(os.path.join(project_root_task, rel_file))

            if 'DDL' not in self.label:
                newest_file = max(abs_files, key=os.path.getctime)
                run_task['flags'].append(newest_file)
                self.main_window.run_task(node_object=self, executable=run_task['executable'], args=run_task['flags'])
            else:
                ok, job_deadline = jobDeadlineUi.getDeadlineJobData(self.location, self.main_window)

                if ok:
                    txt_file = os.path.join(self.location, 'project', 'deadlineJob.txt')
                    job_file = open(txt_file, 'w')

                    for element in job_deadline:
                        job_file.write(element)
                        job_file.write(' ')

                    job_file.close()

                    self.main_window.submitDeadlineJob(txt_file)

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
        self.applicationColorItem.setNamedColor(self.task_color)

    def setTaskColor(self):
        self.task_color = SETTINGS.DEFAULT_TASK_COLOR

        if os.path.basename(self.location)[:7].startswith('LDR'):
            if os.path.basename(self.location)[:7].endswith('LIB'):
                self.task_color = '#00FF00'
            else:
                for tab in self.main_window.content_tabs:
                    if os.path.basename(self.location)[:7].endswith(tab['abbreviation']):
                        self.task_color = tab['loader_color']
                        break

        elif os.path.basename(self.location)[:7].startswith('SVR'):
            for tab in self.main_window.content_tabs:
                if os.path.basename(self.location)[:7].endswith(tab['abbreviation']):
                    self.task_color = tab['saver_color']

        else:
            for task in self.main_window._tasks:
                print task[u'abbreviation']
                print self.nodeTask
                if self.nodeTask == task[u'task']:
                    logging.info('task color description for task %s found' % task[u'abbreviation'])
                    self.task_color = task[u'color']
                    break

        self.taskColorItem.setNamedColor(self.task_color)




