'''
Created on May 2, 2015

@author: michaelmussato
'''


from PyQt4.QtGui import *
from PyQt4.uic import *

import os


class newOutputUI(QDialog):
    def __init__(self, output_dir, outputs, main_window, node, parent = None):
        super(newOutputUI, self).__init__(parent)

        self.mainWindow = main_window
        self.pypelyneRoot = self.mainWindow._pypelyne_root

        self.node = node
        
        self.currentPlatform = self.mainWindow._current_platform

        self.ui = loadUi(os.path.join(self.pypelyneRoot, 'ui', 'newOutput.ui'), self)
        self.setModal(True)
        
        self.outputDir = output_dir
        self.outputs = outputs
        
        self.createUI()
        self.addComboBoxItems()
        self.createConnects()

    def createUI(self):
        mimeTypes = [ ('arbitrary', None), ('.ass', 'ASS'), ('.exr', 'EXR'), ('.tga', 'TGA')]

        self.comboBoxOutput.addItem('select')

        for mime in mimeTypes:
            self.comboBoxMime.addItem(mime[ 0])
        
        #self.comboBoxVersion.addItem('select')
        #self.comboBoxVersion.setEnabled(False)
        
        #self.comboBoxTask.addItem('select')
        
        self.comboBoxMime.setEnabled(False)

        self.buttonOk.setEnabled(False)
        
        self.labelFolder.setEnabled(False)
        self.labelStatus.setEnabled(False)
    
    def addComboBoxItems(self):
        for output in self.outputs:
            self.comboBoxOutput.addItem(output[0][2][1])

    def createConnects(self):
        self.buttonOk.clicked.connect(self.onOk)
        #self.buttonOk.accepted.connect(self.on_ok)
        self.buttonCancel.clicked.connect(self.onCancel)
        self.lineEditOutputName.textChanged.connect(self.setStatus)
        self.comboBoxOutput.activated.connect(self.setStatus)
        #self.comboBoxApplication.activated.connect(self.updateVersions)
        #self.comboBoxTask.activated.connect(self.set_status)
        #self.comboBoxVersion.activated.connect(self.set_status)
        
    # def updateVersions(self):
        # print 'updating versions'
        # versions = [ '1', '2', '3']
        # self.comboBoxVersion.clear()
        # self.comboBoxVersion.addItem('select')
        # if not self.comboBoxApplication.currentIndex() == 0:
            # self.comboBoxVersion.setEnabled(True)
            # for version in self.applicationItems[ self.comboBoxApplication.currentIndex() - 1][ 2]:
                # self.comboBoxVersion.addItem(version)
        # else:
            # self.comboBoxVersion.addItem('select')
        
    def setStatus(self):
        # usedNames = os.listdir(self.outputDir)
        print self.node._label
        usedNames = os.listdir(os.path.join(self.mainWindow._projects_root, self.mainWindow._current_project, 'content', self.mainWindow._current_content['content'], self.mainWindow._current_content_item, self.node._label, 'output'))
        #print usedNames

        #task[2][ 1]

        #print self.outputs
        #print self.outputs[ self.comboBoxOutput.currentIndex() - 1][ 0][ 1][ 1]
        #print self.tools[ self.comboBoxApplication.currentIndex() - 1][ 2]
        
        if self.comboBoxOutput.currentIndex() == 0 \
                or self.comboBoxOutput.currentIndex() == 0 \
                or self.lineEditOutputName.text() == '':
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('')
            
        elif self.outputs[ self.comboBoxOutput.currentIndex() - 1][ 0][ 1][ 1]  + '__' + self.lineEditOutputName.text() in usedNames:
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('already exists')

        elif ' ' in self.lineEditOutputName.text() \
                or '-' in self.lineEditOutputName.text() \
                or '__' in self.lineEditOutputName.text():
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('invalid character')
            
        else:
            self.buttonOk.setEnabled(True)
            self.labelStatus.setText(self.outputs[ self.comboBoxOutput.currentIndex() - 1][ 0][ 1][ 1] + '__' + self.lineEditOutputName.text())
            #self.labelStatus.setText(self.outputDir + os.sep + self.taskItems[ self.comboBoxTask.currentIndex() - 1][ 1] + '_' + self.applicationItems[ self.comboBoxApplication.currentIndex() - 1][ 1] + '__' + self.lineEditNodeName.text())

    def onCancel(self):
        self.reject()
        
    def onOk(self):
        self.outputName = self.outputs[ self.comboBoxOutput.currentIndex() - 1][ 0][ 1][ 1] + '__' + self.lineEditOutputName.text()
        self.outputIndex = self.comboBoxOutput.currentIndex() - 1
        self.mimeIndex = self.comboBoxMime.currentIndex()
        self.accept()
        return self.outputName, self.outputIndex
    
    # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    @staticmethod
    def getNewOutputData(output_dir, outputs, main_window, node):
        dialog = newOutputUI(output_dir, outputs, main_window, node)
        result = dialog.exec_()
        output_name, output_index = dialog.onOk()
        return output_name, result == QDialog.Accepted, output_index
