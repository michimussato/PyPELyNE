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
        self.exclusions = self.mainWindow._exclusions
        self.pypelyneRoot = self.mainWindow._pypelyne_root
        
        self.currentPlatform = self.mainWindow._current_platform
        self.activeItemPath = activeItemPath
        self.contentDirectory = os.path.dirname(os.path.dirname(activeItemPath))

        self.ui = loadUi(os.path.join(self.pypelyneRoot, 'ui', 'newLoader.ui'), self)

        self.setModal(True)

        self.createUI()
        self.addComboBoxCategoryItems()
        self.createConnects()

    def createUI(self):
        self.comboBoxCategory.addItem('select')
        self.comboBoxItem.addItem('select')
        
        self.comboBoxItem.setEnabled(False)

        self.buttonOk.setEnabled(False)
        
        self.labelFolder.setEnabled(False)
        self.labelStatus.setEnabled(False)

    def addComboBoxCategoryItems(self):
        directoryContent = os.listdir(self.contentDirectory)

        for directory in directoryContent:
            if not directory in self.exclusions:
                self.comboBoxCategory.addItem(directory)

    def createConnects(self):
        self.buttonOk.clicked.connect(self.onOk)
        self.buttonCancel.clicked.connect(self.onCancel)
        self.comboBoxCategory.activated.connect(self.setStatus)
        self.comboBoxItem.activated.connect(self.setComboBoxItem)

    def setComboBoxItem(self):
        if str(self.comboBoxItem.currentText()) == 'select':
            self.buttonOk.setEnabled(False)
            self.labelStatus.setText('')

        else:
            subcontentLocation = os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText()), str(self.comboBoxItem.currentText()))
            subcontent = os.listdir(subcontentLocation)

            if any('SVR' in s for s in subcontent):
                if self.activeItemPath == os.path.join(self.contentDirectory, str(self.comboBoxCategory.currentText()), str(self.comboBoxItem.currentText())):
                    self.buttonOk.setEnabled(False)
                    self.labelStatus.setText('dont\'t create its own loader')

                else:
                    self.buttonOk.setEnabled(True)
                    self.labelStatus.setText('item has saver')
                    self.sourceSaverLocation = subcontentLocation

            else:
                self.buttonOk.setEnabled(False)
                self.labelStatus.setText('item has no saver')

    def setStatus(self):
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

            if self.comboBoxItem.currentIndex() == 0:

                for directory in content:
                    if directory not in self.exclusions:
                        self.comboBoxItem.addItem(directory)

    def onCancel(self):
        self.reject()
        
    def onOk(self):
        saverFolder = [folder for folder in os.listdir(self.sourceSaverLocation) if folder.startswith('SVR_')][0]

        for tab in self.mainWindow.content_tabs:
            if str(self.comboBoxCategory.currentText()) == tab['content']:
                self.loaderName = 'LDR_' + tab['abbreviation'] + '__' + str(self.comboBoxItem.currentText())
                break

        self.accept()
        return self.loaderName, os.path.join(self.sourceSaverLocation, saverFolder)  #, tabIndex

    # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    @staticmethod
    def getNewLoaderData(contentDirectory, exclusions):
        dialog = newLoaderUI(contentDirectory, exclusions)
        result = dialog.exec_()
        loaderName, sourceSaverLocation = dialog.onOk()
        return result == QDialog.Accepted, loaderName, sourceSaverLocation
