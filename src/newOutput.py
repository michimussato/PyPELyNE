'''
Created on May 2, 2015

@author: michaelmussato
'''


from PyQt4.QtGui import *
from PyQt4.uic import *

import os


class newOutputUI( QDialog ):
    def __init__( self, outputDir, outputs, mainWindow, parent = None ):
        super( newOutputUI, self ).__init__( parent )

        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()

        
        self.currentPlatform = self.mainWindow.getCurrentPlatform()
        '''
        if self.currentPlatform == "Windows":
            self.ui = loadUi( r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\newOutput.ui', self )
            
        elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
            self.ui = loadUi( r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/newOutput.ui', self )
        '''

        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'newOutput.ui' ), self )
        self.setModal( True )
        
        self.outputDir = outputDir
        self.outputs = outputs
        
        self.createUI()
        self.addComboBoxItems()
        self.createConnects()
        
    
    def createUI( self ):
        self.comboBoxOutput.addItem( 'select' )
        self.comboBoxMime.addItem( 'arbitrary' )
        
        #self.comboBoxVersion.addItem( 'select' )
        #self.comboBoxVersion.setEnabled( False )
        
        #self.comboBoxTask.addItem( 'select' )
        
        self.comboBoxMime.setEnabled( False )

        self.buttonOk.setEnabled( False )
        
        self.labelFolder.setEnabled( False )
        self.labelStatus.setEnabled( False )
        
    
    def addComboBoxItems( self ):
        
        #self.applicationItems = [ [ 'Maya', 'MAY', [ '2013', '2014', '2015' ] ], [ 'Cinema 4D', 'C4D', [ 'R14', 'R15', 'R16' ] ] ]
        #for applicationItem in self.applicationItems:
        #    self.comboBoxApplication.addItem( applicationItem[ 0 ] )
            
        for output in self.outputs:
            self.comboBoxOutput.addItem( output[ 0 ][ 2 ][ 1 ] )
        '''
        self.tasks = [ [ 'Model', 'MDL' ], [ 'Shader', 'SHD' ] ]
        for task in self.tasks:
            self.comboBoxOutput.addItem( taskOutput[ 0 ] )
        '''
        

    def createConnects( self ):
        self.buttonOk.clicked.connect( self.onOk )
        #self.buttonOk.accepted.connect( self.onOk )
        self.buttonCancel.clicked.connect( self.onCancel )
        self.lineEditOutputName.textChanged.connect( self.setStatus )
        self.comboBoxOutput.activated.connect( self.setStatus )
        #self.comboBoxApplication.activated.connect( self.updateVersions )
        #self.comboBoxTask.activated.connect( self.setStatus )
        #self.comboBoxVersion.activated.connect( self.setStatus )
        
    # def updateVersions( self ):
        # print 'updating versions'
        # versions = [ '1', '2', '3' ]
        # self.comboBoxVersion.clear()
        # self.comboBoxVersion.addItem( 'select' )
        # if not self.comboBoxApplication.currentIndex() == 0:
            # self.comboBoxVersion.setEnabled( True )
            # for version in self.applicationItems[ self.comboBoxApplication.currentIndex() - 1 ][ 2 ]:
                # self.comboBoxVersion.addItem( version )
        # else:
            # self.comboBoxVersion.addItem( 'select' )

        
        
    def setStatus( self ):
        usedNames = os.listdir( self.outputDir )
        #print usedNames

        #task[ 2 ][ 1 ]

        #print self.outputs
        #print self.outputs[ self.comboBoxOutput.currentIndex() - 1 ][ 0 ][ 1 ][ 1 ]
        #print self.tools[ self.comboBoxApplication.currentIndex() - 1 ][ 2 ]
        
        if self.comboBoxOutput.currentIndex() == 0 \
                or self.comboBoxOutput.currentIndex() == 0 \
                or self.lineEditOutputName.text() == '':
            self.buttonOk.setEnabled( False )
            self.labelStatus.setText( '' )
            
        elif self.outputs[ self.comboBoxOutput.currentIndex() - 1 ][ 0 ][ 1 ][ 1 ]  + '__' + self.lineEditOutputName.text() in usedNames:
            self.buttonOk.setEnabled( False )
            self.labelStatus.setText( 'already exists' )

        elif ' ' in self.lineEditOutputName.text() \
                or '-' in self.lineEditOutputName.text() \
                or '__' in self.lineEditOutputName.text():
            self.buttonOk.setEnabled( False )
            self.labelStatus.setText( 'invalid character' )
            
        else:
            self.buttonOk.setEnabled( True )
            self.labelStatus.setText( self.outputs[ self.comboBoxOutput.currentIndex() - 1 ][ 0 ][ 1 ][ 1 ] + '__' + self.lineEditOutputName.text() )
            #self.labelStatus.setText( self.outputDir + os.sep + self.taskItems[ self.comboBoxTask.currentIndex() - 1 ][ 1 ] + '_' + self.applicationItems[ self.comboBoxApplication.currentIndex() - 1 ][ 1 ] + '__' + self.lineEditNodeName.text() )
            
    
    def onCancel( self ):
        self.reject()
        
    def onOk( self ):
        self.outputName = self.outputs[ self.comboBoxOutput.currentIndex() - 1 ][ 0 ][ 1 ][ 1 ] + '__' + self.lineEditOutputName.text()
        self.outputIndex = self.comboBoxOutput.currentIndex() - 1
        #self.taskIndex = self.comboBoxTask.currentIndex() - 1
        #print self.nodeName
        self.accept()
        return self.outputName, self.outputIndex
    
    
    # http://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    @staticmethod
    def getNewOutputData( outputDir, outputs, mainWindow ):
        dialog = newOutputUI( outputDir, outputs, mainWindow )
        result = dialog.exec_()
        outputName, outputIndex = dialog.onOk()
        return outputName, result == QDialog.Accepted, outputIndex
