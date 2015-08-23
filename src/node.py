'''
Created on Dec 15, 2014

@author: michaelmussato
'''

import datetime, os, glob, subprocess, getpass

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from circlesInOut import *
#from screenCast import *
from timeTracker import *
from PyQt4.uic import *
from jobDeadline import *
#from errorClasses import *

import xml.etree.ElementTree as ET


class node( QGraphicsItem, QObject ):
    nodeClicked = pyqtSignal()

    def __init__( self, mainWindow, scene, propertyNodePath ):
        super( node, self ).__init__( None, scene )
        
        self.propertyNodePath = propertyNodePath
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.pypelyneRoot
        self.user = self.mainWindow.getUser()
        self.location = self.getNodeRootDir()
        self.loaderSaver = os.path.basename( self.location )[ :7 ]
        self.asset = os.path.dirname( self.location )
        self.project = os.path.dirname( os.path.dirname ( os.path.dirname( self.asset ) ) )
        self.scene = scene
        self._tools = self.mainWindow.getTools()
        self._tasks = self.mainWindow.getTasks()
        self.exclusions = self.mainWindow.getExclusions()
        self.now = datetime.datetime.now()
        self.nowStr = str( self.now )
        self.rect = QRectF( 0, 0, 200, 40 )
        self.outputMaxWidth = []
        self.inputMaxWidth = []
        self.setAcceptHoverEvents( True )
        self.outputList = []
        self.inputList = []
        self.inputs = []
        self.incoming = []
        self.outputs = []
        self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )
        self.setData( 1, self.now )
        self.setData( 2, 'node' )
        #self.setToolTip( 'haha' )
        try:
            self.setNodePosition()
        except:
            print '===> fix corrupt %s' %( self.propertyNodePath )

        self.scene.clearSelection()
        self.labelBoundingRect = 0.0
        
        if not self.loaderSaver.startswith( 'LDR' ):
            self.inputPort = self.newInput( scene )
        
        self.label = None
        
        #use this to add outputs from filesystem:
        self.addOutputs()
        self.addInputs()

        self.gradient = QLinearGradient( self.rect.topLeft(), self.rect.bottomLeft() )
        self.taskColorItem = QColor( 0, 0, 0 )
        self.applicationColorItem = QColor( 0, 0, 0 )

        if not self.loaderSaver.startswith( 'SVR' ) and not self.loaderSaver.startswith( 'LDR' ):
            self.newOutputButton()

        self.widgetMenu = None
        self.setTaskColor()
        self.setApplicationColor()

    def getNodeAsset( self ):
        return self.asset

    def getNodeProject( self ):
        return self.project

    def getInputPort( self ):
        return self.inputPort
        
    def getNodeRootDir( self ):
        return os.path.dirname( os.path.realpath( self.propertyNodePath ) )

    def getApplicationInfo( self, propertyNode ):

        try:

            nodeApplicationInfo = propertyNode.findall( './task' )

            self.nodeVersion = nodeApplicationInfo[ 0 ].items()[ 3 ][ 1 ]
            self.nodeVendor = nodeApplicationInfo[ 0 ].items()[ 2 ][ 1 ]
            self.nodeFamily = nodeApplicationInfo[ 0 ].items()[ 4 ][ 1 ]
            self.nodeArch = nodeApplicationInfo[ 0 ].items()[ 0 ][ 1 ]
            self.nodeTask = nodeApplicationInfo[ 0 ].items()[ 1 ][ 1 ]

        except:
            self.nodeVersion = 'undefined'
            self.nodeVendor = 'undefined'
            self.nodeFamily = 'undefined'
            self.nodeArch = 'undefined'
            self.nodeTask = 'undefined'


        

    def queryApplicationInfo( self ):

        return self.nodeVersion, self.nodeVendor, self.nodeFamily, self.nodeArch, self.nodeTask
        #       [ 1 ][ 1 ]          [ 3 ][ 1 ]      [ 4 ][ 1 ]      [ 0 ][ 1 ]      [ 2 ][ 1 ]
        #       ('modelling',   'R 15',       'CINEMA 4D',  'x64',      'MAXON')
        #       [ 2 ][ 1 ]      [ 3 ][ 1 ]     [ 4 ][ 1 ]   [ 0 ][ 1 ]  [ 2 ][ 1 ]

    def setNodePosition( self ):
        self.propertyNode = ET.parse( self.propertyNodePath )

        try:
            print 'new style reading'
            nodePosition = self.propertyNode.findall( './node' )

            positionX = nodePosition[ 0 ].items()[ 0 ][ 1 ]
            positionY = nodePosition[ 0 ].items()[ 1 ][ 1 ]

        except:
            print 'old style reading'
            positionX = self.propertyNode.findall( './positionX' )
            positionY = self.propertyNode.findall( './positionY' )

            positionX = positionX[ 0 ].items()[ 0 ][ 1 ]
            positionY = positionY[ 0 ].items()[ 0 ][ 1 ]

        self.setPos( QPointF( float( positionX ), float( positionY ) ) )

        self.getApplicationInfo( self.propertyNode )
    
    
    def mousePressEvent( self, event ):
        self.scene.nodeSelect.emit( self )

    def mouseDoubleClickEvent( self, event ):
        if self.label.startswith( 'LDR_AST' ):
            self.mainWindow.getAssetContent( None, self.label )
        elif self.label.startswith( 'LDR_SHT' ):
            self.mainWindow.getShotContent( None, self.label )

        else:
            searchString = self.nodeVendor + ' ' + self.nodeFamily + ' ' + self.nodeVersion + ' ' + self.nodeArch
            searchIndex = self.mainWindow.toolsComboBox.findText( QString( searchString ), Qt.MatchContains ) - 2

            if searchIndex < 0:
                if not str( self.nodeFamily + ' ' + self.nodeVersion ) in [ self.mainWindow.toolsComboBox.itemText( i ) for i in range( self.mainWindow.toolsComboBox.count() ) ]:
                    print 'application family not available'
                    QMessageBox.critical( self.mainWindow, 'application warning', str( '%s not available.' %str( self.nodeFamily + ' ' + self.nodeVersion ) ), QMessageBox.Abort, QMessageBox.Abort )
                    return

                elif self.nodeArch == 'x64':
                    reply = QMessageBox.warning( self.mainWindow, 'architecture warning', str( 'x64 version of %s not available. continue using x32?' %self.nodeFamily ), QMessageBox.Yes | QMessageBox.No, QMessageBox.No )

                    if reply == QMessageBox.Yes:
                        searchString = str( self.nodeVendor + ' ' + self.nodeFamily + ' ' + self.nodeVersion + ' ' + 'x32' )
                        searchIndex = self.mainWindow.toolsComboBox.findText( QString( searchString ), Qt.MatchContains ) - 2
                        print 'x64 not available. using x32 version.'
                    else:
                        return
                elif self.nodeArch == 'x32':
                    reply = QMessageBox.warning( self.mainWindow, 'architecture warning', str( 'x32 version of %s not available. continue using x64?' %self.nodeFamily ), QMessageBox.Yes | QMessageBox.No, QMessageBox.No )

                    if reply == QMessageBox.Yes:
                        searchString = str( self.nodeVendor + ' ' + self.nodeFamily + ' ' + self.nodeVersion + ' ' + 'x64' )
                        searchIndex = self.mainWindow.toolsComboBox.findText( QString( searchString ), Qt.MatchContains ) - 2
                        print 'x32 not available. using x64 version.'
                    else:
                        return
                else:
                    print 'some weird shit'

            elif os.path.exists( os.path.join( self.location, 'locked' ) ):
                QMessageBox.critical( self.mainWindow, 'node warning', str( '%s is currently in use.' %str( self.label ) ), QMessageBox.Abort, QMessageBox.Abort )
                return

            elif os.path.exists( os.path.join( self.location, 'checkedOut' ) ):
                QMessageBox.critical( self.mainWindow, 'node warning', str( '%s is currently checked out.' %str( self.label ) ), QMessageBox.Abort, QMessageBox.Abort )
                return


            args = []

            for arg in self._tools[ searchIndex ][ 10 ]:
                args.append( arg )

            if self.nodeFamily == 'Maya':
                for arg in [ '-proj', self.location, '-file' ]:
                    print self.location
                    args.append( arg )

            projectRoot = os.path.join( self.location, 'project' )

            #print self._tools[ searchIndex ][ 7 ]
            extension = os.path.splitext( self._tools[ searchIndex ][ 7 ] )[ 1 ]


            files = glob.glob1( projectRoot, str( '*' + extension ) )

            absFiles = []

            for relFile in files:
                if not relFile in self.exclusions:
                    absFiles.append( os.path.join( projectRoot, relFile ) )


            if not 'DDL' in self.label:
                newestFile = max( absFiles, key=os.path.getctime )
                self.mainWindow.runTask( self, self._tools[ searchIndex ][ 1 ][ 0 ], newestFile, args )
            else:
                ok, jobDeadline = jobDeadlineUi.getDeadlineJobData( self.location, self.mainWindow )

                if ok:
                    txtFile = os.path.join( self.location, 'project', 'deadlineJob.txt' )
                    jobFile = open( txtFile, 'w' )

                    for element in jobDeadline:
                        jobFile.write( element )
                        jobFile.write( ' ' )

                    jobFile.close()

                    self.mainWindow.submitDeadlineJob( txtFile )

                    #os.system( 'bash ' + txtFile )


    def dataReady( self ):
        cursorBox = self.mainWindow.statusBox.textCursor()
        cursorBox.movePosition( cursorBox.End )
        cursorBox.insertText( "%s (%s): %s" %( datetime.datetime.now(), self.pid, str( self.process.readAll() ) ) )
        self.mainWindow.statusBox.ensureCursorVisible()

    def hoverEnterEvent( self, event ):
        pass
    
    def hoverLeaveEvent( self, event ):
        pass

    def resizeWidth( self ):
        outputListTextWidth = [ 0 ]
        inputListTextWidth = [ 0 ]

        for i in self.inputList:
            inputListTextWidth.append( int( i.childrenBoundingRect().width() ) )

        for i in self.outputList:
            outputListTextWidth.append( int( i.childrenBoundingRect().width() ) )

        self.rect.setWidth( max( ( self.labelBoundingRect + 40 + 20 ), ( max( outputListTextWidth ) + 80 ) + ( max( inputListTextWidth ) ) ) )
                
    def resizeHeight( self ):
        self.rect.setHeight( ( ( max( len( self.inputs ) + 1, len( self.outputs ) + 1 ) * 20 ) ) )
        self.gradient = QLinearGradient( self.rect.topLeft(), self.rect.bottomLeft() )

    def resize( self ):
        self.resizeHeight()
        self.resizeWidth()

    def boundingRect( self ):
        return self.rect

    def paint( self, painter, option, widget ):
        painter.setRenderHint( QPainter.Antialiasing )

        if os.path.exists( os.path.join( self.location, 'locked' ) ):
            self.gradient.setColorAt( 0, self.taskColorItem )
            self.gradient.setColorAt( 1, Qt.red )
        elif os.path.exists( os.path.join( self.location, 'checkedOut' ) ):
            self.gradient.setColorAt( 0, self.taskColorItem )
            self.gradient.setColorAt( 1, Qt.white )
        else:
            self.gradient.setColorAt( 0, self.taskColorItem )
            self.gradient.setColorAt( 1, self.applicationColorItem.darker( 160 ) )
        pen = QPen( Qt.SolidLine )
        pen.setColor( Qt.black )
        pen.setWidth( 0 )
        painter.setBrush( self.gradient )
        
        if option.state & QStyle.State_Selected:
            self.updatePropertyNodeXML()
            self.setZValue( 1 )
            pen.setWidth( 1 )
            pen.setColor( Qt.green )

        elif option.state & QStyle.State_MouseOver:
            pen.setWidth( 1 )
            pen.setColor( Qt.yellow )

        else:
            
            pen.setWidth( 0 )
            self.setZValue( 0 )

        painter.setPen( pen )

        painter.drawRoundedRect( self.rect, 10.0, 10.0 )
        
        for i in self.outputList:
            i.setPos( self.boundingRect().width() - i.rect.width(), i.pos().y() )
            
        self.rect.setWidth( self.rect.width() )
        self.arrangeOutputs()
        self.arrangeInputs()
        self.resize()
        
    def arrangeOutputs( self ):
        for output in self.outputs:
            position = QPointF( self.boundingRect().width() - output.rect.width(), ( ( output.boundingRect().height() * ( self.outputs.index( output ) + 1 ) ) ) )
            output.setPos( position )

    def arrangeInputs( self ):
        for input in self.inputs:
            position = QPointF( 0, ( ( self.inputs.index( input ) + 1 ) * input.boundingRect().height() ) )
            input.setPos( position )
        
    #add existing outputs from file system
    def addOutputs( self ):
        
        self.outputRootDir = os.path.join( str( self.location ), 'output' )
        
        allOutputs = os.listdir( self.outputRootDir )
        
        for i in allOutputs:
            if not i in self.exclusions:
                self.newOutput( self, i )

    #add existing inputs from file system
    def addInputs( self ):
        self.inputRootDir = os.path.join( str( self.location ), 'input' )
        allInputs = os.listdir( self.inputRootDir )
        for i in allInputs:
            if not i in self.exclusions:
                input = self.newInput( self.scene )

                lookupDir = os.path.dirname( os.path.join( self.inputRootDir, os.readlink( os.path.join( self.inputRootDir, i ) ) ) )

                if not i in os.listdir( lookupDir ) and os.path.basename( os.path.dirname( lookupDir ) ).startswith( 'LDR' ) == True:
                    os.remove( os.path.join( self.inputRootDir, i ) )
                    print 'removed', i

                else:
                    
                    print 'keep', i

    #add new dynamic input
    def newInput( self, scene ):
        input = portInput( self, scene, self.mainWindow )
        input.setParentItem( self )

        self.inputList.append( input )
        
        self.inputMaxWidth.append( input.childrenBoundingRect().width() )
        
        self.resizeHeight()
        
    def updatePropertyNodeXML( self ):
        pos = self.scenePos()
        propertyNode = ET.parse( self.propertyNodePath )
        propertyNodeRoot = propertyNode.getroot()
        
        try:
            #new style positioning...
            nodePosition = propertyNodeRoot.find( 'node' )

            nodePosition.set( 'positionX', '%s' %pos.x() )
            nodePosition.set( 'positionY', '%s' %pos.y() )


        except:
            #old style positioning...
            positionX = propertyNodeRoot.find( 'positionX' )
            positionY = propertyNodeRoot.find( 'positionY' )

            positionX.set( 'value', '%s' %pos.x() )
            positionY.set( 'value', '%s' %pos.y() )
        
        xmlDoc = open( self.propertyNodePath, 'w' )
        
        xmlDoc.write( '<?xml version="1.0"?>' )
        xmlDoc.write( ET.tostring( propertyNodeRoot ) )
        xmlDoc.close()

    #add new dynamic output:
    def newOutput( self, node, name ):
        output = portOutput( self, name, self.mainWindow )

        if len( name.split( '.' ) ) > 1:

            output.addText( node, name.split( '.' )[ 3 ] )

        else:
            output.addText( node, name )
        
        self.outputs.append( output )

        output.setParentItem( self )
        self.outputList.append( output )
        
        self.rect.setWidth( self.rect.width() )
        
        self.outputMaxWidth.append( output.childrenBoundingRect().width() )
        
        self.resizeHeight()

    def newOutputButton( self ):
        outputButton = portOutputButton( self, 'create new output', self.mainWindow )
        
        outputButton.setParentItem( self )
    
    def sendFromNodeToBox( self, text ):
        self.scene.textMessage.emit( text )
        
    def getLabel( self ):
        return self.label

    def addText( self, scene, text ):
        self.setData( 0, text )
        nodeLabel = QGraphicsTextItem( text )
        self.label = text
        nodeLabelColor = ( QColor( 255, 255, 255 ) )
        nodeLabelColor.setNamedColor( '#080808' )
        nodeLabel.setDefaultTextColor( nodeLabelColor )
        nodeLabel.setPos( QPointF( 25, 0 ) )
        nodeLabel.setParentItem( self )
        self.labelBoundingRect = nodeLabel.boundingRect().width()

        self.resizeWidth()

    def setApplicationColor( self ):
        self.applicationColorItem.setNamedColor( self.taskColor )

    def setTaskColor( self ):
        index = 0

        if os.path.basename( self.location )[ :7 ].startswith( 'LDR' ):
            if os.path.basename( self.location )[ :7 ].endswith( 'AST' ):
                self.taskColor = '#FFFF00'
            elif os.path.basename( self.location )[ :7 ].endswith( 'SHT' ):
                self.taskColor = '#0000FF'
        elif os.path.basename( self.location )[ :7 ].startswith( 'SVR' ):
            if os.path.basename( self.location )[ :7 ].endswith( 'AST' ):
                self.taskColor = '#FFFF33'
            elif os.path.basename( self.location )[ :7 ].endswith( 'SHT' ):
                self.taskColor = '#3333FF'

        else:

            for i in self._tasks:
                if [ item for item in i if self.nodeTask in item ]:
                    print 'found'
                    self.taskColor = self._tasks[ index ][ 0 ][ 1 ]
                    break
                else:
                    index += 1

        self.taskColorItem.setNamedColor( self.taskColor )


