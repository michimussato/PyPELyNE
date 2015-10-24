import platform
import os
import re

from PyQt4.QtGui import *
from PyQt4.uic import *
from newOutput import *


# class configureRenderJobWidgetUi(QWidget):
#     def __init__(self, parent = None):
#         super(configureRenderJobWidgetUi, self).__init__(parent)
#         self.pypelyneRoot = os.getcwd()
#         self.currentPlatform = platform.system()
#         if self.currentPlatform == "Windows":
#             self.ui = loadUi(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\configureRenderJobWidget.ui', self)
#         elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
#             self.ui = loadUi(r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/configureRenderJobWidget.ui', self)
#
#     def getDeadlineItems(self):
#
#
#
#         #self.deadlineGroupsString = os.popen('/Applications/Deadline/Resources/bin/deadlinecommand Groups').read()
#
#         self.deadlinePlugins = os.popen('/Applications/Deadline/Resources/bin/deadlinecommand Plugins').read().replace('\n',' ').split()
#         self.deadlineGroups = os.popen('/Applications/Deadline/Resources/bin/deadlinecommand Groups').read().replace('\n',' ').split()
#         self.deadlinePools = os.popen('/Applications/Deadline/Resources/bin/deadlinecommand Pools').read().replace('\n',' ').split()
#
#         return self.deadlinePlugins, self.deadlineGroups, self.deadlinePools
#
#
#         #print self.deadlineGroups
#         '''
#         for group in self.deadlineGroups:
#             self.comboBoxDeadlineGroup.addItem(group)
#
#         for pool in self.deadlinePools:
#             self.comboBoxDeadlinePool.addItem(pool)
#         '''


class NewNodeUI(QDialog):
    def __init__(self, node_dir=None, tasks=None, main_window=None, parent=None):
        super(NewNodeUI, self).__init__(parent)
        
        self.main_window = main_window
        self.pypelyne_root = self.main_window._pypelyne_root
        self.current_platform = self.main_window._current_platform

        self.tool_data = None

        self.ui = loadUi(os.path.join(self.pypelyne_root, 'ui', 'newNode.ui'), self)
        self.setModal(True)
        
        self.node_dir = node_dir
        # self.tools = tools
        self.tasks = tasks
        
        self.create_ui()
        self.add_combo_box_items()
        self.create_connects()

    # def set_configure_render_job_widget_ui(self):
    #     pass

        '''deadline queries
        self.configureRenderJobWidget = configureRenderJobWidgetUi()
            
        self.configureRenderJobScrollArea.setWidget(self.configureRenderJobWidget)

        self.deadlinePlugins, self.deadlineGroups, self.deadlinePools = self.configureRenderJobWidget.getDeadlineItems()

        for deadlinePlugin in self.deadlinePlugins:
            self.configureRenderJobWidget.comboBoxDeadlinePlugin.addItem(deadlinePlugin)
        for deadlineGroup in self.deadlineGroups:
            self.configureRenderJobWidget.comboBoxDeadlineGroup.addItem(deadlineGroup)
        for deadlinePool in self.deadlinePools:
            self.configureRenderJobWidget.comboBoxDeadlinePool.addItem(deadlinePool)
        '''

    def clear_configure_render_job_widget_ui(self):
        # self.nodeWidgets = []
        self.configureRenderJobArea.takeWidget()
        
    def create_ui(self):
        self.comboBoxApplication.addItem('select')
        
        # self.comboBoxVersion.addItem('select')
        # self.comboBoxVersion.setEnabled(False)
        
        self.comboBoxTask.addItem('select')

        # self.setConfigureRenderJobWidgetUi()
        
        self.buttonOk.setEnabled(False)
        
        self.labelFolder.setEnabled(False)
        self.labelStatus.setEnabled(False)

        # self.labelRenderManager.setVisible(False)
        # self.comboBoxRenderManager.setVisible(False)
        # self.configureRenderJobScrollArea.setVisible(False)

    def add_combo_box_items(self):
        # executable = []
            
        for tool_item in self.main_window._tool_items:
            self.comboBoxApplication.addItem(tool_item[u'label'], tool_item)

        for task in self.tasks:
            self.comboBoxTask.addItem(task[2][1])

    def create_connects(self):
        self.buttonOk.clicked.connect(self.onOk)
        # self.buttonOk.accepted.connect(self.onOk)
        self.buttonCancel.clicked.connect(self.onCancel)
        self.lineEditNodeName.textChanged.connect(self.set_status)
        self.comboBoxApplication.activated.connect(self.set_status)
        # self.comboBoxApplication.activated.connect(self.updateVersions)
        self.comboBoxTask.activated.connect(self.set_status)
        # self.comboBoxVersion.activated.connect(self.set_status)
        
    def set_status(self):
        # print self.nodeDir

        nodes_dir = os.listdir(os.path.join(self.main_window._projects_root, self.main_window._current_project, 'content', self.main_window._current_content['content'], self.main_window._current_content_item))

        used_names = nodes_dir

        self.comboBoxTask.setVisible(True)
        self.labelTask.setVisible(True)

        index_combobox = self.comboBoxApplication.currentIndex()

        self.tool_data = self.comboBoxApplication.itemData(index_combobox)

        try:
            valid_string = bool(re.match(r'[\w-]*$', self.lineEditNodeName.text()))

        except UnicodeEncodeError, e:
            print 'error captured:', e
            valid_string = False

        finally:
            try:
                if any(invalid_char in str(self.lineEditNodeName.text()) for invalid_char in ['__', '-']):
                    valid_string = False

            except UnicodeEncodeError, e:
                print 'error captured:', e
                valid_string = False

        if not valid_string:
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('invalid character')

        elif self.comboBoxTask.currentIndex() == 0 \
                or self.comboBoxApplication.currentIndex() == 0 \
                or self.lineEditNodeName.text() == '':
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('')

        elif self.tasks[self.comboBoxTask.currentIndex() - 1][1][1] + '_' + self.tool_data['abbreviation'] + '__' + self.lineEditNodeName.text() in used_names:
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('already exists')

        else:
            self.buttonOk.setEnabled(True)
            self.labelStatus.setText(self.tasks[self.comboBoxTask.currentIndex() - 1][1][1] + '_' + self.tool_data['abbreviation'] + '__' + self.lineEditNodeName.text())

    def onCancel(self):
        self.reject()
        
    def onOk(self):
        self.node_name = self.tasks[self.comboBoxTask.currentIndex() - 1][1][1] + '_' + self.tool_data['abbreviation'] + '__' + self.lineEditNodeName.text()
        self.task_index = self.comboBoxTask.currentIndex() - 1
        self.accept()
        return self.node_name, self.tool_data, self.task_index

    @staticmethod
    def get_new_node_data(node_dir, tasks, main_window):
        # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
        dialog = NewNodeUI(node_dir, tasks, main_window)
        result = dialog.exec_()
        node_name, tool_data, task_index = dialog.onOk()
        return node_name, result == QDialog.Accepted, tool_data, task_index
