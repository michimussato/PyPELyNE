#!/usr/bin/env python
# -*- coding: utf-8 -*-


# http://www.freecadweb.org/wiki/index.php?title=PySide_Beginner_Examples


#from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys


    
class newNodeUI( QMainWindow ):
    
    def __init__( self, *args ):
        QMainWindow.__init__( self, *args )
        self.createUI()
        self.createLayout()
        self.addComboBoxItems()
        self.createConnects()
        
        
    def createUI( self ):
        
        self.spacerItem = QSpacerItem( 1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum )
    
        self.labelNodeName = QLabel( 'node name' )
        self.lineEditNodeName = QLineEdit()
        
        self.labelApplication = QLabel( 'application' )
        self.comboBoxApplication = QComboBox()
        self.comboBoxApplication.addItem( 'select' )
        
        self.labelVersion = QLabel( 'version' )
        self.comboBoxVersion = QComboBox()
        self.comboBoxVersion.addItem( 'select' )
        self.comboBoxVersion.setEnabled( False )
        
        self.labelTask = QLabel( 'task' )
        self.comboBoxTask = QComboBox()
        self.comboBoxTask.addItem( 'select' )
        
        self.dialogBox = QDialogButtonBox()
        self.buttonOk = QPushButton( 'ok' )
        self.buttonOk.setEnabled( False )
        self.buttonCancel = QPushButton( 'cancel' )
        #self.dialogBox = QDialogButtonBox( QHorizontal )
        #self.dialogBox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )
        
        #self.dialogBox = QDialogButtonBox( Qt.Horizontal )
        self.dialogBox.addButton( self.buttonOk, QDialogButtonBox.ActionRole )
        self.dialogBox.addButton( self.buttonCancel, QDialogButtonBox.RejectRole )
        #self.dialogBox.addButton( self.buttonOk, QDialogButtonBox. )
        
        self.labelFolder = QLabel( 'folder of node' )
        self.labelFolder.setEnabled( False )
        self.labelStatus = QLabel( '' )
        self.labelStatus.setEnabled( False )
        #self.labelStatus.setVisible( False )
        
        
        
                
    def createLayout( self ):
        
        vBoxLayout = QVBoxLayout()
        
        hBoxLayoutApplication = QHBoxLayout()
        hBoxLayoutApplication.addWidget( self.labelApplication )
        hBoxLayoutApplication.addItem( self.spacerItem )
        hBoxLayoutApplication.addWidget( self.comboBoxApplication )
        
        vBoxLayout.addLayout( hBoxLayoutApplication )
        
        hBoxLayoutVersion = QHBoxLayout()
        hBoxLayoutVersion.addWidget( self.labelVersion )
        hBoxLayoutVersion.addItem( self.spacerItem )
        hBoxLayoutVersion.addWidget( self.comboBoxVersion )
        
        vBoxLayout.addLayout( hBoxLayoutVersion )
         
        hBoxLayoutTask = QHBoxLayout()
        hBoxLayoutTask.addWidget( self.labelTask )
        hBoxLayoutTask.addItem( self.spacerItem )
        hBoxLayoutTask.addWidget( self.comboBoxTask )
        
        vBoxLayout.addLayout( hBoxLayoutTask )
        
        hBoxLayoutNodeName = QHBoxLayout()
        hBoxLayoutNodeName.addWidget( self.labelNodeName )
        hBoxLayoutNodeName.addItem( self.spacerItem )
        hBoxLayoutNodeName.addWidget( self.lineEditNodeName )
        
        vBoxLayout.addLayout( hBoxLayoutNodeName )
        
        hBoxLayoutStatus = QHBoxLayout()
        hBoxLayoutStatus.addWidget( self.labelFolder )
        hBoxLayoutStatus.addItem( self.spacerItem )
        hBoxLayoutStatus.addWidget( self.labelStatus )
        
        vBoxLayout.addLayout( hBoxLayoutStatus )
        
        hBoxLayoutButtons = QHBoxLayout()
        hBoxLayoutButtons.addItem( self.spacerItem )
        hBoxLayoutButtons.addWidget( self.dialogBox )
        
        vBoxLayout.addLayout( hBoxLayoutButtons )
        
        widgetCentral = QWidget()
        widgetCentral.setLayout( vBoxLayout )
        self.setCentralWidget( widgetCentral )
        
    def addComboBoxItems( self ):
        
        self.applicationItems = [ [ 'Maya', 'MAY', [ '2013', '2014', '2015' ] ], [ 'Cinema 4D', 'C4D', [ 'R14', 'R15', 'R16' ] ] ]
        for applicationItem in self.applicationItems:
            self.comboBoxApplication.addItem( applicationItem[ 0 ] )
    
        self.taskItems = [ [ 'Model', 'MDL' ], [ 'Shader', 'SHD' ] ]
        for taskItem in self.taskItems:
            self.comboBoxTask.addItem( taskItem[ 0 ] )
            
        

        
    def createConnects( self ):
        self.buttonOk.clicked.connect( self.onOk )
        self.buttonCancel.clicked.connect( self.onCancel )
        self.lineEditNodeName.textChanged.connect( self.setStatus )
        self.comboBoxApplication.activated.connect( self.setStatus )
        self.comboBoxApplication.activated.connect( self.updateVersions )
        self.comboBoxTask.activated.connect( self.setStatus )
        self.comboBoxVersion.activated.connect( self.setStatus )
        
    def updateVersions( self ):
        print 'updating versions'
        versions = [ '1', '2', '3' ]
        self.comboBoxVersion.clear()
        self.comboBoxVersion.addItem( 'select' )
        if not self.comboBoxApplication.currentIndex() == 0:
            self.comboBoxVersion.setEnabled( True )
            for version in self.applicationItems[ self.comboBoxApplication.currentIndex() - 1 ][ 2 ]:
                self.comboBoxVersion.addItem( version )
        else:
            self.comboBoxVersion.addItem( 'select' )

        
        
    def setStatus( self ):
        usedNames = [ 'SHD_MAY__hallo', 'MDL_C4D__shizzle' ]
        
        if self.comboBoxTask.currentIndex() == 0 \
                or self.comboBoxApplication.currentIndex() == 0 \
                or self.comboBoxVersion.currentIndex() == 0 \
                or self.lineEditNodeName.text() == '':
            self.buttonOk.setEnabled( False )
            self.labelStatus.setText( '' )
            
        elif self.taskItems[ self.comboBoxTask.currentIndex() - 1 ][ 1 ] + '_' + self.applicationItems[ self.comboBoxApplication.currentIndex() - 1 ][ 1 ] + '__' + self.lineEditNodeName.text() in usedNames:
            self.buttonOk.setEnabled( False )
            self.labelStatus.setText( 'already exists' )
            
        else:
            self.buttonOk.setEnabled( True )
            self.labelStatus.setText( self.taskItems[ self.comboBoxTask.currentIndex() - 1 ][ 1 ] + '_' + self.applicationItems[ self.comboBoxApplication.currentIndex() - 1 ][ 1 ] + '__' + self.lineEditNodeName.text() )
            
    
    def onCancel( self ):
        self.close()
        
    def onOk( self ):
        self.nodeName = self.taskItems[ self.comboBoxTask.currentIndex() - 1 ][ 1 ] + '_' + self.applicationItems[ self.comboBoxApplication.currentIndex() - 1 ][ 1 ] + '__' + self.lineEditNodeName.text()
        print self.nodeName
        #self.labelStatus.setText( nodeName )
        
        
    def getText( self ):
        return self.nodeName, True
        self.close()
        
        


        
def main( argv ):
    app = QApplication( argv )
    mainwindow = newNodeUI()
    mainwindow.show()
    sys.exit( app.exec_() )
    
    
if __name__ == "__main__":
    main( sys.argv )
        
