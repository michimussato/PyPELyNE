'''
Created on May 2, 2015

@author: michaelmussato
'''


from PyQt4.QtGui import *
from PyQt4.uic import *

import os




'''
#library loader procedure:
cd /Volumes/pili/pypelyne_projects/0000-00-00___test___test/content/assets/libraryTest ;

mkdir LDR_LIB__mazda;

cd LDR_LIB__mazda/;

#create the xml file:
touch propertyNode.xml;

ln -s ../../../../../../pypelyne_library/2015-05-20___myself___edelviz_____assets_____edelVizModel_____SVR_AST__edelVizModel_____2015-09-04_1632-53/output output;

ln -s ../../../../../../pypelyne_library/2015-05-20___myself___edelviz_____assets_____edelVizModel_____SVR_AST__edelVizModel_____2015-09-04_1632-53/input input;

ln -s ../../../../../../pypelyne_library/2015-05-20___myself___edelviz_____assets_____edelVizModel_____SVR_AST__edelVizModel_____2015-09-04_1632-53/live live;

'''








class newLoaderUI(QDialog):
    def __init__(self, activeItemPath, mainWindow, parent = None):
        super(newLoaderUI, self).__init__(parent)

        self.mainWindow = mainWindow
        self.exclusions = self.mainWindow.getExclusions()
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        
        self.currentPlatform = self.mainWindow.getCurrentPlatform()
        self.activeItemPath = activeItemPath
        self.contentDirectory = os.path.dirname(os.path.dirname(activeItemPath))
        #contentDirectory 
        #self.exclusions = exclusions
        '''
        if self.currentPlatform == "Windows":
            self.ui = loadUi(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\newLoader.ui', self)
            
        elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
            self.ui = loadUi(r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/newLoader.ui', self)
        '''

        self.ui = loadUi(os.path.join(self.pypelyneRoot, 'ui', 'newLoader.ui'), self)

        self.setModal(True)


        
        #self.outputDir = outputDir
        #self.outputs = outputs
        
        self.createUI()
        self.addComboBoxCategoryItems()
        self.createConnects()
        
    
    def createUI(self):
        self.comboBoxCategory.addItem('select')
        self.comboBoxItem.addItem('select')
        
        #self.comboBoxVersion.addItem('select')
        #self.comboBoxVersion.setEnabled(False)
        
        #self.comboBoxTask.addItem('select')
        
        self.comboBoxItem.setEnabled(False)

        self.buttonOk.setEnabled(False)
        
        self.labelFolder.setEnabled(False)
        self.labelStatus.setEnabled(False)
        
    
    def addComboBoxCategoryItems(self):
        
        #self.applicationItems = [['Maya', 'MAY', ['2013', '2014', '2015']], ['Cinema 4D', 'C4D', ['R14', 'R15', 'R16']]]
        #for applicationItem in self.applicationItems:
        #    self.comboBoxApplication.addItem(applicationItem[0])

        directoryContent = os.listdir(self.contentDirectory)
        

        for directory in directoryContent:
            if not directory in self.exclusions:
                self.comboBoxCategory.addItem(directory)
        '''
        self.tasks = [['Model', 'MDL'], ['Shader', 'SHD']]
        for task in self.tasks:
            self.comboBoxOutput.addItem(taskOutput[0])
        '''
        

    def createConnects(self):
        self.buttonOk.clicked.connect(self.onOk)
        #self.buttonOk.accepted.connect(self.onOk)
        self.buttonCancel.clicked.connect(self.onCancel)
        #self.lineEditOutputName.textChanged.connect(self.setStatus)
        self.comboBoxCategory.activated.connect(self.setStatus)
        #self.comboBoxApplication.activated.connect(self.updateVersions)
        self.comboBoxItem.activated.connect(self.setComboBoxItem)
        #self.comboBoxVersion.activated.connect(self.setStatus)
        
    # def updateVersions(self):
        # print 'updating versions'
        # versions = ['1', '2', '3']
        # self.comboBoxVersion.clear()
        # self.comboBoxVersion.addItem('select')
        # if not self.comboBoxApplication.currentIndex() == 0:
            # self.comboBoxVersion.setEnabled(True)
            # for version in self.applicationItems[self.comboBoxApplication.currentIndex() - 1][2]:
                # self.comboBoxVersion.addItem(version)
        # else:
            # self.comboBoxVersion.addItem('select')

    def setComboBoxItem(self):
        #self.activeItemPath
        if str(self.comboBoxItem.currentText()) == 'select':
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('')
        else:
            subcontentLocation = os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText()), str(self.comboBoxItem.currentText()))
            subcontent = os.listdir(subcontentLocation)

            #print subcontent

            if any('SVR' in s for s in subcontent):
                if self.activeItemPath == os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText()), str(self.comboBoxItem.currentText())):
                    self.buttonOk.setEnabled(False)
                    self.labelStatus.setText('dont\'t create its own loader')
                else:
                    #print 'yes'

                    #if 'SVR' in subcontent:
                    
                    self.buttonOk.setEnabled(True)
                    self.labelStatus.setText('item has saver')
                    self.sourceSaverLocation = subcontentLocation
            else:
                self.buttonOk.setEnabled(False)
                self.labelStatus.setText('item has no saver')
                #print 'no'
        
        
    def setStatus(self):

        print 'tabIndex:', self.tabAsset.currentIndex()


        #print type(self.comboBoxCategory.currentText())
        #print self.comboBoxCategory.currentText()

        
        #print content

        #usedNames = os.listdir(self.outputDir)
        #print usedNames

        #task[2][1]

        #print self.outputs
        #print self.outputs[self.comboBoxOutput.currentIndex() - 1][0][1][1]
        #print self.tools[self.comboBoxApplication.currentIndex() - 1][2]


        if self.comboBoxCategory.currentIndex() == 0:
            self.comboBoxItem.clear()
            self.labelStatus.setText('')
            self.comboBoxItem.addItem('select')
            self.comboBoxItem.setEnabled(False)
            self.buttonOk.setEnabled(False)


        else:

            content = os.listdir(os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText())))
            self.comboBoxItem.clear()
            self.comboBoxItem.addItem('select')
            self.labelStatus.setText('')
            self.comboBoxItem.setEnabled(True)

            #print content
            
            if self.comboBoxItem.currentIndex() == 0:

                for directory in content:
                    if directory not in self.exclusions:
                        self.comboBoxItem.addItem(directory)


            #else:
                
            #print self.comboBoxCategory.text()
            

        '''
        if self.comboBoxOutput.currentIndex() == 0 \
                or self.comboBoxOutput.currentIndex() == 0 \
                or self.lineEditOutputName.text() == '':
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('')
            
        elif self.outputs[self.comboBoxOutput.currentIndex() - 1][0][1][1]  + '__' + self.lineEditOutputName.text() in usedNames:
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('already exists')

        elif ' ' in self.lineEditOutputName.text() \
                or '-' in self.lineEditOutputName.text() \
                or '__' in self.lineEditOutputName.text():
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('invalid character')
            
        else:
            self.buttonOk.setEnabled(True)
            self.labelStatus.setText(self.outputs[self.comboBoxOutput.currentIndex() - 1][0][1][1] + '__' + self.lineEditOutputName.text())
            #self.labelStatus.setText(self.outputDir + os.sep + self.taskItems[self.comboBoxTask.currentIndex() - 1][1] + '_' + self.applicationItems[self.comboBoxApplication.currentIndex() - 1][1] + '__' + self.lineEditNodeName.text())
            
        '''
    
    def onCancel(self):
        self.reject()
        
    def onOk(self):

        tabIndex = self.tabAsset.currentIndex()

        #tabItem = self.tabAsset.currentItem()

        saverFolder = [folder for folder in os.listdir(self.sourceSaverLocation) if folder.startswith('SVR_')][0]
        #print saverFolder

        #print os.path.basename(os.path.dirname(self.activeItemPath))
        #print os.path.basename(self.activeItemPath)

        #self.loaderRoot = os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText()), str(self.comboBoxItem.currentText()))
        #print 'self.loaderRoot :', self.loaderRoot
        if str(self.comboBoxCategory.currentText()) == 'assets':
            self.loaderName = 'LDR_AST__' + str(self.comboBoxItem.currentText())
        elif str(self.comboBoxCategory.currentText()) == 'shots':
            self.loaderName = 'LDR_SHT__' + str(self.comboBoxItem.currentText())
        #self.outputName = self.outputs[self.comboBoxOutput.currentIndex() - 1][0][1][1] + '__' + self.lineEditOutputName.text()
        #self.outputIndex = self.comboBoxOutput.currentIndex() - 1
        #self.taskIndex = self.comboBoxTask.currentIndex() - 1
        #print self.nodeName
        self.accept()
        return self.loaderName, os.path.join(self.sourceSaverLocation, saverFolder), tabIndex
    
    
    # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    @staticmethod
    def getNewLoaderData(contentDirectory, exclusions):
        dialog = newLoaderUI(contentDirectory, exclusions)
        result = dialog.exec_()
        loaderName, sourceSaverLocation, tabIndex = dialog.onOk()
        return result == QDialog.Accepted, loaderName, sourceSaverLocation, tabIndex
