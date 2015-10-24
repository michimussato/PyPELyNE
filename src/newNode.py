'''
Created on Apr 27, 2015

@author: michaelmussato
'''

from PyQt4.QtGui import *
from PyQt4.uic import *
from newOutput import *
import re

import platform, os



# class configureRenderJobWidgetUi(QWidget):
#     def __init__(self, parent = None):
#         super(configureRenderJobWidgetUi, self).__init__(parent)
#         self.pypelyneRoot = os.getcwd()
#         self.currentPlatform = platform.system()
#         if self.currentPlatform == "Windows":
#             self.ui = loadUi(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\configureRenderJobWidget.ui', self)
#         elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
#             self.ui = loadUi(r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/configureRenderJobWidget.ui', self)

#     def getDeadlineItems(self):



#         #self.deadlineGroupsString = os.popen('/Applications/Deadline/Resources/bin/deadlinecommand Groups').read()

#         self.deadlinePlugins = os.popen('/Applications/Deadline/Resources/bin/deadlinecommand Plugins').read().replace('\n',' ').split()
#         self.deadlineGroups = os.popen('/Applications/Deadline/Resources/bin/deadlinecommand Groups').read().replace('\n',' ').split()
#         self.deadlinePools = os.popen('/Applications/Deadline/Resources/bin/deadlinecommand Pools').read().replace('\n',' ').split()

#         return self.deadlinePlugins, self.deadlineGroups, self.deadlinePools


#         #print self.deadlineGroups
#         '''
#         for group in self.deadlineGroups:
#             self.comboBoxDeadlineGroup.addItem(group)

#         for pool in self.deadlinePools:
#             self.comboBoxDeadlinePool.addItem(pool)
#         '''


class newNodeUI(QDialog):
    def __init__(self, nodeDir, tasks, mainWindow, parent = None):
        super(newNodeUI, self).__init__(parent)
        
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow._pypelyne_root
        self.currentPlatform = self.mainWindow._current_platform

        self.tool_data = None

        self.ui = loadUi(os.path.join(self.pypelyneRoot, 'ui', 'newNode.ui'), self)
        self.setModal(True)
        
        self.nodeDir = nodeDir
        # self.tools = tools
        self.tasks = tasks
        
        self.createUI()
        self.add_combo_box_items()
        self.createConnects()

        #self.deadlinePlugins, self.deadlineGroups, self.deadlinePools = self.configureRenderJobWidget.getDeadlineItems()

    def setConfigureRenderJobWidgetUi(self):
        pass

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

        
        # self.nodeVersion, self.nodeVendor, self.nodeFamily, self.nodeArch
        #self.nodeApplicationInfo = node.queryApplicationInfo()


        #self.widgetUi.labelNode.setText(node.data(0).toPyObject())
        #self.widgetUi.labelApplication.setText(self.nodeApplicationInfo[2] + ' ' + self.nodeApplicationInfo[0])
        #self.widgetUi.labelVersion.setText(self.nodeApplicationInfo[0])
        #self.widgetUi.labelExecutable.setText(node.data(0).toPyObject())





    def clearConfigureRenderJobWidgetUi(self):
        #self.nodeWidgets = []
        self.configureRenderJobArea.takeWidget()
        
    
    def createUI(self):
        self.comboBoxApplication.addItem('select')
        
        #self.comboBoxVersion.addItem('select')
        #self.comboBoxVersion.setEnabled(False)
        
        self.comboBoxTask.addItem('select')

        #self.setConfigureRenderJobWidgetUi()
        
        self.buttonOk.setEnabled(False)
        
        self.labelFolder.setEnabled(False)
        self.labelStatus.setEnabled(False)

        #self.labelRenderManager.setVisible(False)
        #self.comboBoxRenderManager.setVisible(False)
        #self.configureRenderJobScrollArea.setVisible(False)

    def add_combo_box_items(self):
        executable = []
            
        for tool in self.mainWindow._tools:

            if tool[u'executable_x32'] is not None:
                executable.append(tool[u'executable_x32'])
                for flag_x32 in tool[u'flags_x32']:
                    executable.append(flag_x32)

                run_item = self.mainWindow.get_dict_x32(tool)

                self.comboBoxApplication.addItem(tool[u'label_x32'], run_item.copy())

                executable[:] = []

            if tool[u'executable_x64'] is not None:
                executable.append(tool[u'executable_x64'])
                for flag_x64 in tool[u'flags_x64']:
                    executable.append(flag_x64)

                run_item = self.mainWindow.get_dict_x64(tool)

                self.comboBoxApplication.addItem(tool[u'label_x64'], run_item.copy())

                executable[:] = []

            # print tool

            # if tool['executable_x32'] is not None:
            #     self.comboBoxApplication.addItem(tool['label_x32'], self.mainWindow._tools.index(tool))
            # if tool['executable_x64'] is not None:
            #     self.comboBoxApplication.addItem(tool['label_x64'], self.mainWindow._tools.index(tool))

        for task in self.tasks:
            self.comboBoxTask.addItem(task[2][1])

    def createConnects(self):
        self.buttonOk.clicked.connect(self.onOk)
        #self.buttonOk.accepted.connect(self.onOk)
        self.buttonCancel.clicked.connect(self.onCancel)
        self.lineEditNodeName.textChanged.connect(self.setStatus)
        self.comboBoxApplication.activated.connect(self.setStatus)
        #self.comboBoxApplication.activated.connect(self.updateVersions)
        self.comboBoxTask.activated.connect(self.setStatus)
        #self.comboBoxVersion.activated.connect(self.setStatus)
        
    def setStatus(self):
        print self.nodeDir

        nodes_dir = os.listdir(os.path.join(self.mainWindow._projects_root, self.mainWindow._current_project, 'content', self.mainWindow._current_content['content'], self.mainWindow._current_content_item))

        usedNames = nodes_dir

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

        elif self.tasks[self.comboBoxTask.currentIndex() - 1][1][1] + '_' + self.tool_data['abbreviation'] + '__' + self.lineEditNodeName.text() in usedNames:
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('already exists')

        else:
            self.buttonOk.setEnabled(True)
            self.labelStatus.setText(self.tasks[self.comboBoxTask.currentIndex() - 1][1][1] + '_' + self.tool_data['abbreviation'] + '__' + self.lineEditNodeName.text())

    def onCancel(self):
        self.reject()
        
    def onOk(self):
        index_combobox = self.comboBoxApplication.currentIndex()
        # tool_data = self.comboBoxApplication.itemData(index_combobox)
        # print 'onOk'
        # try:
        self.nodeName = self.tasks[self.comboBoxTask.currentIndex() - 1][1][1] + '_' + self.tool_data['abbreviation'] + '__' + self.lineEditNodeName.text()
        # except:
        #     self.nodeName = self.tasks[self.comboBoxTask.currentIndex() - 1][1][1] + '_' + 'DDL' + '__' + self.lineEditNodeName.text()
        # self.toolIndex = self.comboBoxApplication.currentIndex() - 1
        self.taskIndex = self.comboBoxTask.currentIndex() - 1
        # self.toolTemplate = self.tools[self.comboBoxApplication.currentIndex() - 1]
        # print self.nodeName
        self.accept()
        return self.nodeName, self.tool_data, self.taskIndex

    @staticmethod
    def getNewNodeData(nodeDir, tasks, mainWindow):
        # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
        dialog = newNodeUI(nodeDir, tasks, mainWindow)
        result = dialog.exec_()
        nodeName, tool_data, taskIndex = dialog.onOk()
        return nodeName, result == QDialog.Accepted, tool_data, taskIndex
