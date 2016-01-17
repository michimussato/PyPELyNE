import datetime
import os
import glob
import subprocess
import getpass
import logging
import json
import copy
import uuid

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from circlesInOut import *
# from screenCast import *
from timeTracker import *
from PyQt4.uic import *
from jobDeadline import *
# from errorClasses import *

import xml.etree.ElementTree as ET


class Node(QGraphicsItem, QObject):
    nodeClicked = pyqtSignal()

    def __init__(self, main_window=None, node_root=None):
        super(Node, self).__init__(None, main_window.scene)

        self.main_window = main_window
        self.location = node_root
        self.meta_task = None
        self.meta_tool = None

        try:
            try:
                meta_task_file = open(os.path.join(self.location, 'meta_task.json'))
                self.meta_task = json.load(meta_task_file)
                meta_task_file.close()
            except AttributeError, e:
                print 'self.meta_task', e

            try:
                meta_tool_file = open(os.path.join(self.location, 'meta_tool.json'))
                self.meta_tool = json.load(meta_tool_file)
                meta_tool_file.close()
            except AttributeError, e:
                print 'self.meta_tool', e

        except IOError, e:
            print 'xml loading:', e
            self.propertyNodePath = os.path.join(self.location, 'propertyNode.xml')

        try:
            # print self.meta_task
            self.node_uuid = self.meta_task['uuid']
        except KeyError, e:
            print 'this node has no uuid yet. giving it one.'
            self.node_uuid = uuid.uuid4().hex
            # print self.node_uuid
            self.meta_task['uuid'] = self.node_uuid
            # print self.meta_task
            with open(os.path.join(self.location, 'meta_task.json'), 'w') as outfile:
                json.dump(self.meta_task, outfile)
                outfile.close()

        # print self.meta_task
        # print self.meta_tool

        self.loaderSaver = os.path.basename(self.location)[:7]
        self.asset = os.path.dirname(self.location)
        self.project = os.path.dirname(os.path.dirname(os.path.dirname(self.asset)))

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
        # self.setToolTip('haha')
        self.set_node_position()

        self.main_window.scene.clearSelection()
        self.labelBoundingRect = 0.0
        
        if not self.loaderSaver.startswith('LDR'):
            self.inputPort = self.new_input(self.main_window.scene)
        
        self.label = None
        
        # use this to add outputs from filesystem:
        self.add_outputs()
        self.add_inputs()

        self.gradient = QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())
        self.taskColorItem = QColor(0, 0, 0)
        self.applicationColorItem = QColor(0, 0, 0)

        if not self.loaderSaver.startswith('SVR') and not self.loaderSaver.startswith('LDR'):
            self.new_output_button()

        self.widgetMenu = None
        self.task_color = SETTINGS.DEFAULT_TASK_COLOR
        self.setTaskColor()
        self.setApplicationColor()

    def getNodeAsset(self):
        return self.asset

    def getNodeProject(self):
        return self.project

    def getInputPort(self):
        return self.inputPort
        
    def getNodeRootDir(self):
        return self.location

    def getApplicationInfo(self):
        try:
            # print self.meta_tool
            # print self.meta_task
            self.nodeVersion = self.meta_tool['release_number']
            self.nodeVendor = self.meta_tool['vendor']
            self.nodeFamily = self.meta_tool['family']
            self.nodeArch = self.meta_tool['architecture']
            # self.node_uuid = self.meta_tool['node_uuid']
            # print self.meta_tool
            # print self.meta_task['task']
            self.nodeTask = self.meta_task['task']
            self.node_creator = self.meta_task['creator']
            self.node_operating_system = self.meta_task['operating_system']
        except Exception, e:
            print 'loader or saver? (%s)' % e

    def queryApplicationInfo(self):
        try:
            return self.nodeVersion, self.nodeVendor, self.nodeFamily, self.nodeArch, self.nodeTask

        except TypeError, e:
            logging.warning('queryApplicationInfo for not yet available for saver and loader nodes (%s)' % e)

    def set_node_position(self):
        try:
            pos_x = self.meta_task['pos_x']
            pos_y = self.meta_task['pos_y']
            print 'json reading'

        except TypeError, e:
            print e
            try:
                # print self.propertyNodePath
                self.property_node = ET.parse(self.propertyNodePath)
                logging.info('new style reading xml')
                node_position = self.property_node.findall('./node')

                pos_x = node_position[0].items()[0][1]
                pos_y = node_position[0].items()[1][1]

            except Exception, e:
                logging.info('old style reading xml: %s' % e)
                pos_x = self.property_node.findall('./positionX')
                pos_y = self.property_node.findall('./positionY')

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
        self.main_window.scene.nodeSelect.emit(self)

    def mouseDoubleClickEvent(self, event=None):
        _tools = copy.deepcopy(self.main_window._tools)
        # run_task = None

        # print run_task
        # print self.main_window._tools

        # tools_copy = self.main_window._tools.copy

        if self.label.startswith('LDR'):
            self.main_window.get_content(node_label=self.label)

        else:
            run_task = {}

            run_task['family'] = None
            run_task['release_number'] = None
            run_task['project_template'] = None
            run_task['executable'] = None
            run_task['project_workspace_flag'] = None
            run_task['project_workspace_parent_directory_level'] = None
            run_task['project_file_flag'] = None
            # run_task['architecture_fallback'] = False
            run_task['flags'] = None
            run_task['label'] = None

            if os.path.exists(os.path.join(self.location, 'locked')):
                QMessageBox.critical(self.main_window,
                                     'node warning',
                                     str('%s is currently in use.' % self.label),
                                     QMessageBox.Abort,
                                     QMessageBox.Abort)
                return

            if os.path.exists(os.path.join(self.location, 'checkedOut')):
                QMessageBox.critical(self.main_window,
                                     'node warning',
                                     str('%s is currently checked out.' % self.label),
                                     QMessageBox.Abort,
                                     QMessageBox.Abort)
                return

            for tool in _tools:
                if self.meta_tool['family'] == tool['family']:
                    run_task['family'] = tool['family']
                    if self.meta_tool['release_number'] == tool['release_number']:
                        run_task['release_number'] = tool['release_number']
                        run_task['release_extension'] = tool['release_extension']
                        run_task['project_template'] = tool['project_template']
                        run_task['project_workspace_flag'] = tool['project_workspace_flag']
                        run_task['project_workspace_parent_directory_level'] = tool['project_workspace_parent_directory_level']
                        run_task['project_file_flag'] = tool['project_file_flag']

                        if self.meta_tool['architecture'] == 'x64':
                            if self.meta_tool['architecture_fallback']:
                                logging.info('this is a %s %s %s task, but can fallback to x32' % (tool['family'], tool['release_number'], self.meta_tool['architecture']))
                                if bool(tool['executable_x64']):
                                    if os.path.exists(tool['executable_x64']):
                                        logging.info('x64 found.')
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
                                            logging.warning('x64 not found. using x32.')
                                            run_task['executable'] = tool['executable_x32']
                                            # run_task['architecture_fallback'] = True
                                            run_task['label'] = tool['label_x32']
                                            run_task['flags'] = tool['flags_x32']

                                        else:
                                            logging.warning('dont use x32 instead of x64.')
                                            return

                                    else:
                                        logging.error('x32 and x64 not found.')

                            else:
                                print 'this is a %s %s %s task (cannot fallback)' % (tool['family'], tool['release_number'], self.meta_tool['architecture'])
                                if bool(tool['executable_x64']):
                                    if os.path.exists(tool['executable_x64']):
                                        logging.info('x64 found')
                                        run_task['executable'] = tool['executable_x64']
                                        run_task['flags'] = tool['flags_x64']
                                        run_task['label'] = tool['label_x64']

                                    else:
                                        logging.warning('x64 not found')

                        elif self.meta_tool['architecture'] == 'x32':
                            if self.meta_tool['architecture_fallback']:
                                print 'this is a %s %s %s task, but can fallback to x64.' % (tool['family'], tool['release_number'], self.meta_tool['architecture'])
                                if bool(tool['executable_x32']):
                                    if os.path.exists(tool['executable_x32']):
                                        logging.info('x32 found.')
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
                                                logging.warning('x32 not found. using x64.')
                                                run_task['executable'] = tool['executable_x64']
                                                # run_task['architecture_fallback'] = True
                                                run_task['label'] = tool['label_x64']
                                                run_task['flags'] = tool['flags_x64']

                                            else:
                                                logging.warning('dont use x32 instead of x64.')

                                    else:
                                        logging.error('x32 and x64 not found.')

                            else:
                                print 'this is a %s %s %s task (cannot fallback)' % (tool['family'], tool['release_number'], self.meta_tool['architecture'])
                                if bool(tool['executable_x32']):
                                    if os.path.exists(tool['executable_x32']):
                                        logging.info('x32 found')
                                        run_task['executable'] = tool['executable_x32']
                                        run_task['flags'] = tool['flags_x32']
                                        run_task['label'] = tool['label_x32']

                                    else:
                                        logging.error('x32 not found')

            if run_task['executable'] is None:
                QMessageBox.critical(self.main_window,
                                     'node warning',
                                     str('no suitable tool found to launch task %s.' % self.label),
                                     QMessageBox.Abort,
                                     QMessageBox.Abort)
                return

            project_root_task = os.path.join(self.location, 'project')

            if run_task['project_workspace_flag'] is not None:
                run_task['flags'].append(run_task['project_workspace_flag'])
                workspace_directory = project_root_task
                for parent_directory in range(run_task['project_workspace_parent_directory_level']):
                    workspace_directory = os.path.dirname(workspace_directory)
                run_task['flags'].append(workspace_directory)

            if run_task['project_file_flag'] is not None:
                    run_task['flags'].append(run_task['project_file_flag'])

            extension = run_task['release_extension']

            files = glob.glob1(project_root_task, str('*' + extension))

            abs_files = []

            for rel_file in files:
                if rel_file not in SETTINGS.EXCLUSIONS:
                    abs_files.append(os.path.join(project_root_task, rel_file))

            if 'DDL' not in self.label:
                # TODO: if none is a tools template: this will produce an error
                newest_file = max(abs_files, key=os.path.getctime)
                run_task['flags'].append(newest_file)
                # print run_task
                # print run_task['executable'], run_task['flags']
                self.main_window.run_task(node_object=self, executable=run_task['executable'], args=run_task['flags'])

                # run_task['flags'].remove(newest_file)

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
        cursor_box.insertText("%s (%s): %s" % (datetime.datetime.now(), self.pid, str(self.process.readAll())))
        self.main_window.statusBox.ensureCursorVisible()
    '''
    def hoverEnterEvent(self, event):
        pass
    
    def hoverLeaveEvent(self, event):
        pass
    '''

    def resize_width(self):
        output_list_text_width = [0]
        input_list_text_width = [0]

        for i in self.inputList:
            input_list_text_width.append(int(i.childrenBoundingRect().width()))

        for i in self.outputList:
            output_list_text_width.append(int(i.childrenBoundingRect().width()))

        self.rect.setWidth(max((self.labelBoundingRect + 40 + 20),
                               (max(output_list_text_width) + 80) + (max(input_list_text_width))))
                
    def resize_height(self):
        self.rect.setHeight(max(len(self.inputs) + 1, len(self.outputs) + 1) * 20)
        self.gradient = QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())

    def resize(self):
        self.resize_height()
        self.resize_width()

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
        self.arrange_outputs()
        self.arrange_inputs()
        self.resize()
        # except:
        #     logging.warning('paint error for node %s (corrupt property_node.xml?)' %(self.label))
        
    def arrange_outputs(self):
        for output in self.outputs:
            position = QPointF(self.boundingRect().width() - output.rect.width(), ((output.boundingRect().height() * (self.outputs.index(output) + 1))))
            output.setPos(position)

    def arrange_inputs(self):
        for input in self.inputs:
            position = QPointF(0, ((self.inputs.index(input) + 1) * input.boundingRect().height()))
            input.setPos(position)
        
    # add existing outputs from file system
    def add_outputs(self):
        
        self.output_root_dir = os.path.join(str(self.location), 'output')
        
        all_outputs = os.listdir(self.output_root_dir)
        
        for i in all_outputs:
            if i not in SETTINGS.EXCLUSIONS:
                self.new_output(self, i)

    # add existing inputs from file system
    def add_inputs(self):
        self.input_root_dir = os.path.join(str(self.location), 'input')
        all_inputs = os.listdir(self.input_root_dir)
        for i in all_inputs:
            if i not in SETTINGS.EXCLUSIONS:
                input = self.new_input(self.main_window.scene)
                try:
                    lookup_dir = os.path.dirname(os.path.join(self.input_root_dir,
                                                              os.readlink(os.path.join(self.input_root_dir, i))))
                except:
                    lookup_dir = os.path.dirname(os.path.join(self.input_root_dir,
                                                              os.path.join(self.input_root_dir, i)))

                try:
                    if i not in os.listdir(lookup_dir) \
                            and os.path.basename(os.path.dirname(lookup_dir)).startswith('LDR') == True:
                        os.remove(os.path.join(self.input_root_dir, i))
                        logging.warning('orphaned input found on node %s: %s removed' %(self.label, i))

                    else:

                        logging.info('input is still valid. %s kept' % i)
                except OSError, e:
                    print e

    # add new dynamic input
    def new_input(self, scene):
        input = portInput(self, scene, self.main_window)
        input.setParentItem(self)

        self.inputList.append(input)
        
        self.inputMaxWidth.append(input.childrenBoundingRect().width())
        
        self.resize_height()

    def update_meta_task(self):
        pos = self.scenePos()
        # meta_task = self.meta_task

        self.meta_task['pos_x'] = pos.x()
        self.meta_task['pos_y'] = pos.y()
        # self.meta_task['node_uuid'] = self.node_uuid

        with open(os.path.join(self.location, 'meta_task.json'), 'w') as outfile:
            json.dump(self.meta_task, outfile)
            outfile.close()
        
    def update_property_node_xml(self):
        pos = self.scenePos()
        property_node = ET.parse(self.propertyNodePath)
        property_node_root = property_node.getroot()
        
        try:
            # new style positioning...
            node_position = property_node_root.find('node')

            node_position.set('positionX', '%s' % pos.x())
            node_position.set('positionY', '%s' % pos.y())

        except Exception, e:
            # old style positioning...
            position_x = property_node_root.find('positionX')
            position_y = property_node_root.find('positionY')

            position_x.set('value', '%s' % pos.x())
            position_y.set('value', '%s' % pos.y())
        
        xml_doc = open(self.propertyNodePath, 'w')
        
        xml_doc.write('<?xml version="1.0"?>')
        xml_doc.write(ET.tostring(property_node_root))
        xml_doc.close()

    # add new dynamic output:
    def new_output(self, node, name):
        output = portOutput(self, name, self.main_window)

        if len(name.split('.')) > 1:

            output.add_text(node, name.split('.')[3])

        else:
            output.add_text(node, name)
        
        self.outputs.append(output)

        output.setParentItem(self)
        self.outputList.append(output)
        
        self.rect.setWidth(self.rect.width())
        
        self.outputMaxWidth.append(output.childrenBoundingRect().width())
        
        self.resize_height()

    def new_output_button(self):
        output_button = portOutputButton(self.main_window)
        
        output_button.setParentItem(self)
    
    def send_from_node_to_box(self, text):
        self.main_window.scene.textMessage.emit(text)
        
    def get_label(self):
        return self.label

    @property
    def _label(self):
        return self.label

    def add_text(self, text):
        self.setData(0, text)
        node_label = QGraphicsTextItem(text)
        self.label = text
        node_label_color = (QColor(255, 255, 255))
        node_label_color.setNamedColor('#080808')
        node_label.setDefaultTextColor(node_label_color)
        node_label.setPos(QPointF(25, 0))
        node_label.setParentItem(self)
        self.labelBoundingRect = node_label.boundingRect().width()

        self.resize_width()

    def setApplicationColor(self):
        self.applicationColorItem.setNamedColor(self.task_color)

    def setTaskColor(self):


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

                # print self.nodeTask
                # print task[u'abbreviation']
                # print self.nodeTask
                if self.nodeTask == task[u'task']:
                    # print 'task =', task
                    logging.info('task color description for task %s found' % task[u'abbreviation'])
                    # print 'task color description for task %s found' % task[u'abbreviation']
                    self.task_color = task[u'color']
                    break

        self.taskColorItem.setNamedColor(self.task_color)




