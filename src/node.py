'''
Created on Dec 15, 2014

@author: michaelmussato
'''

import datetime, os, glob, subprocess, getpass

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from circlesInOut import *
from screenCast import *
from timeTracker import *
from PyQt4.uic import *
from jobDeadline import *

import xml.etree.ElementTree as ET


# class Signals( QObject ):
#     trigger = pyqtSignal( str )


class node( QGraphicsItem, QObject ):
    
    #clickedSignal = pyqtSignal( QObject )
    nodeClicked = pyqtSignal()
    #textMessage = pyqtSignal( str )

    def __init__( self, mainWindow, scene, propertyNodePath ):
        super( node, self ).__init__( None, scene )

        #self.loaderSaver = loaderSaver
        
        #self.exclusions = [ '.DS_Store', 'Thumbs.db' ]
        
        self.propertyNodePath = propertyNodePath
        #print self.propertyNodePath
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.user = self.mainWindow.getUser()


        
        self.location = self.getNodeRootDir()
        self.loaderSaver = os.path.basename( self.location )[ :7 ]

        self.asset = os.path.dirname( self.location )
        self.project = os.path.dirname( os.path.dirname ( os.path.dirname( self.asset ) ) )

        
        self.scene = scene

        #self.mainWindow = self.scene.getMainWindow()
        self._tools = self.mainWindow.getTools()
        self._tasks = self.mainWindow.getTasks()
        self.exclusions = self.mainWindow.getExclusions()
        #self.projectsRoot
        #self.project = self.mainWindow.getCurrentProject()
        #self.nodeMenu = loadUi( r'ui/nodeWidget.ui' )
        
        self.now = datetime.datetime.now()
        self.nowStr = str( self.now )
        
        self.rect = QRectF( 0, 0, 200, 40 )
        self.outputMaxWidth = []
        self.inputMaxWidth = []
        #self.resizeWidth()
        self.setAcceptHoverEvents( True )
        self.outputList = []
        self.inputList = []
        
        self.inputs = []
        self.incoming = []
        self.outputs = []

        
        self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )
        #self.sendFromNodeToBox( propertyNodePath )
        self.setData( 1, self.now )
        
        #print 'created:'
        #print self.data( 0 ).toPyObject()
        
        self.setNodePosition()
        #self.setPos( position )
        #print position
        self.scene.clearSelection()
        
        self.labelBoundingRect = 0.0
        #self.label = self.addText( scene, str( self.data( 0 ).toPyObject() )[-6:] )

        #self.label = self.addText( scene, '1rt' )
        
        if not self.loaderSaver.startswith( 'LDR' ):

            self.inputPort = self.newInput( scene )
        
        self.label = None
        
        #use this to add outputs from filesystem:
        self.addOutputs()
        self.addInputs()
        
        #print self.rect.topLeft()
        #print self.rect()

        self.gradient = QLinearGradient( self.rect.topLeft(), self.rect.bottomLeft() )
        self.taskColorItem = QColor( 0, 0, 0 )
        self.applicationColorItem = QColor( 0, 0, 0 )
        if not self.loaderSaver.startswith( 'SVR' ) and not self.loaderSaver.startswith( 'LDR' ):
            #pass
            self.newOutputButton()
        self.widgetMenu = None
        self.setTaskColor()
        self.setApplicationColor()

    def getNodeAsset( self ):
        return self.asset

    def getNodeProject( self ):
        return self.project

        
    def getInputPort( self ):
        #print 'aaaaaaaaaaaaa %s' %self.inputPort
        return self.inputPort
        
    def getNodeRootDir( self ):
        return os.path.dirname( os.path.realpath( self.propertyNodePath ) )

    def getApplicationInfo( self, propertyNode ):

        try:

            nodeApplicationInfo = propertyNode.findall( './task' )

            #print nodeApplicationInfo[ 0 ].items()

            self.nodeVersion = nodeApplicationInfo[ 0 ].items()[ 3 ][ 1 ]
            self.nodeVendor = nodeApplicationInfo[ 0 ].items()[ 2 ][ 1 ]
            self.nodeFamily = nodeApplicationInfo[ 0 ].items()[ 4 ][ 1 ]
            self.nodeArch = nodeApplicationInfo[ 0 ].items()[ 0 ][ 1 ]
            self.nodeTask = nodeApplicationInfo[ 0 ].items()[ 1 ][ 1 ]

            #print nodeApplicationInfo[ 0 ].items()
            #[('arch', 'x64'), ('task', 'modelling'), ('vendor', 'MAXON'), ('version', 'R 15'), ('family', 'CINEMA 4D')]

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
        #self.propertyNode = ET.parse( os.path.join( self.propertyNodePath, 'propertyNode.xml' ) )
        self.propertyNode = ET.parse( self.propertyNodePath )
        
        try:
            print 'new style reading'
            #nodePosition = propertyNodeRoot.find( 'node' )

            #nodePosition.set( 'positionX', '%s' %pos.x() )
            #nodePosition.set( 'positionY', '%s' %pos.y() )
            #positionX = self.propertyNode.findall('./positionX' )
            #positionY = self.propertyNode.findall('./positionY' )
            nodePosition = self.propertyNode.findall( './node' )

            
            #print nodePosition[ 0 ].items()

            positionX = nodePosition[ 0 ].items()[ 0 ][ 1 ]
            positionY = nodePosition[ 0 ].items()[ 1 ][ 1 ]

            #print positionX
            #print positionY

        except:
            print 'old style reading'
            positionX = self.propertyNode.findall( './positionX' )
            positionY = self.propertyNode.findall( './positionY' )

            positionX = positionX[ 0 ].items()[ 0 ][ 1 ]
            positionY = positionY[ 0 ].items()[ 0 ][ 1 ]
        
        self.setPos( QPointF( float( positionX ), float( positionY ) ) )

        self.getApplicationInfo( self.propertyNode )
    
    
    def mousePressEvent( self, event ):
        #print 'fuck it'
        self.scene.nodeSelect.emit( self )

    def mouseDoubleClickEvent( self, event ):
        #propertyNode = ET.parse( self.propertyNodePath )
        #propertyNodeRoot = propertyNode.getroot()
        #nodeApplicationInfo = propertyNode.findall( './task' )
        #nodeApplicationInfo = self.queryApplicationInfo()
        #print nodeApplicationInfo
        #('R 15', 'MAXON', 'CINEMA 4D', 'x64', 'modelling')
        # self.nodeVersion, self.nodeVendor, self.nodeFamily, self.nodeArch, self.nodeTask

        #print 'need to start %s %s %s' %( nodeApplicationInfo[ 2 ], nodeApplicationInfo[ 0 ], nodeApplicationInfo[ 3 ] )

        searchString = self.nodeVendor + ' ' + self.nodeFamily + ' ' + self.nodeVersion + ' ' + self.nodeArch
        searchIndex = self.mainWindow.toolsComboBox.findText( QString( searchString ), Qt.MatchContains ) - 2

        #print searchIndex
        #print searchString

        #print self.nodeFamily + ' ' + self.nodeVersion

        if searchIndex < 0:
            #print self.nodeFamily + ' ' + self.nodeVersion
            #print 'range %s' %[ self.mainWindow.toolsComboBox.itemText( i ) for i in range( self.mainWindow.toolsComboBox.count() ) ]
            if not str( self.nodeFamily + ' ' + self.nodeVersion ) in [ self.mainWindow.toolsComboBox.itemText( i ) for i in range( self.mainWindow.toolsComboBox.count() ) ]:
                print 'application family not available'
                QMessageBox.critical( self.mainWindow, 'application warning', str( '%s not available.' %str( self.nodeFamily + ' ' + self.nodeVersion ) ), QMessageBox.Abort, QMessageBox.Abort )
                return
            elif self.nodeArch == 'x64':
                reply = QMessageBox.warning( self.mainWindow, 'architecture warning', str( 'x64 version of %s not available. continue using x32?' %self.nodeFamily ), QMessageBox.Yes | QMessageBox.No, QMessageBox.No )
                #msgBox.setWindowTitle( QString( 'architecture warning' ) )
                #msgBox.setText( QString( 'x64 version of %s not found. continue using x32?' %self.nodeFamily )
                #msgBox.setStandardButtons( QMessageBox.Yes )
                #msgBox.setDefaultButton( QMessageBox.No )

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
        #elif self.label.startswith( '' ):
        elif os.path.exists( os.path.join( self.location, 'locked' ) ):
            QMessageBox.critical( self.mainWindow, 'node warning', str( '%s is currently in use.' %str( self.label ) ), QMessageBox.Abort, QMessageBox.Abort )
            return


            #else:
            #   print 'using x64 version.'

        #print QString( self.nodeFamily )
        

        #print self.mainWindow.toolsComboBox.

        
        #print searchString
        #print searchIndex

        #print self._tools[ searchIndex ][ 1 ][ 0 ]

        #print self._tools[ searchIndex ]
        args = []

        for arg in self._tools[ searchIndex ][ 10 ]:
            args.append( arg )

        if self.nodeFamily == 'Maya':
            for arg in [ '-proj', self.location, '-file' ]:
                args.append( arg )

        projectRoot = os.path.join( self.location, 'project' )

        #print os.listdir( projectRoot )

        extension = os.path.splitext( self._tools[ searchIndex ][ 7 ] )[ 1 ]
        #print extension

        files = glob.glob1( projectRoot, str( '*' + extension ) )

        absFiles = []

        for relFile in files:
            if not relFile in self.exclusions:
                absFiles.append( os.path.join( projectRoot, relFile ) )

        #print absFiles

        #print len(absFiles)

        if not 'DDL' in self.label:
            newestFile = max( absFiles, key=os.path.getctime )
            self.mainWindow.runTask( self, self._tools[ searchIndex ][ 1 ][ 0 ], newestFile, args )
        else:
            ok, jobDeadline = jobDeadlineUi.getDeadlineJobData( self.location, self.mainWindow )
            #print self.location

            if ok:
                txtFile = os.path.join( self.location, 'project', 'deadlineJob.txt' )
                jobFile = open( txtFile, 'w' )

                for element in jobDeadline:
                    jobFile.write( element )
                    jobFile.write( ' ' )
                    #jobFile.write( ' \\\n' )

                jobFile.close()

                os.system( 'bash ' + txtFile )



            #print 'this is a deadline job'

        #print newestFile

        #fullFilePath

        #self.mainWindow.runTask( self._tools[ searchIndex ][ 1 ][ 0 ], self, newestFile )
            
        #self.mainWindow.runTask( self._tools[ searchIndex ][ 1 ][ 0 ], newestFile, self.asset, self.data( 0 ).toPyObject(), self.project, args )
        

        print 'double clicke node'
    


    def dataReady( self ):
        cursorBox = self.mainWindow.statusBox.textCursor()
        cursorBox.movePosition( cursorBox.End )
        cursorBox.insertText( "%s (%s): %s" %( datetime.datetime.now(), self.pid, str( self.process.readAll() ) ) )
        self.mainWindow.statusBox.ensureCursorVisible()

    '''
    def runTask( self, executable, newestFile, *args ):

        #print executable

        makingOfDir = os.path.join( self.project, 'making_of' )

        #now = str( datetime.datetime.now().strftime( '%Y-%m-%d_%H%M-%S' ) )
        now = datetime.datetime.now()

        nowSecs = str( now.strftime( '%Y-%m-%d_%H%M-%S' ) )
        nowMilliSecs = str( now.strftime( '%Y-%m-%d_%H%M-%S_%f' ) )
        
        user = self.mainWindow.getUser()


        if not os.path.exists( makingOfDir ):
            os.makedirs( makingOfDir, mode=0777 )


        timeTrackerDir = os.path.join( self.project, 'timetracker' )
        if not os.path.exists( timeTrackerDir ):
            os.makedirs( timeTrackerDir, mode=0777 )
        timetrackerCsv = os.path.join( timeTrackerDir, 'timetracker.csv' )
        if not os.path.exists( timetrackerCsv ):
            open( timetrackerCsv, 'a' ).close()


        #trackThis = timeTracker( os.path.basename( self.asset ), os.path.basename( self.location ), self.project )

        #trackThis.start()


        mp4 = makingOfDir + os.sep + nowSecs + '__' + user + '__' + os.path.basename( self.asset ) + '__' + self.label + '.mp4'
        #print self.mp4

        #print os.path.expanduser('~'), str( 'vlc.sock' + '.' + self.now + '__' + self.user + '__' + self.assetName + '__' + self.taskName )

        vlcExec = r'/Applications/VLC.app/Contents/MacOS/VLC'

        #vlcSocket = os.path.join( os.path.expanduser('~'), str( 'vlc.sock' + '.' + now + '__' + user + '__' + os.path.basename( self.asset ) + '__' + self.label ) )
        vlcSocket = os.path.join( os.path.expanduser('~'), str( 'vlc.sock' + '.' + nowMilliSecs ) )

        vlcArgs = [ vlcExec, '-I', 'rc', '--rc-fake-tty', '--rc-unix', vlcSocket, 'screen://', '--screen-fps', '4', '--quiet', '--sout', '"#transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst=' + mp4 + '}"' ]

        #commandStop = "echo stop | nc -U " + self.vlcSocket
        #commandQuit = "echo quit | nc -U " + self.vlcSocket

        #print commandStop
        #print commandQuit

        #time.sleep( 15 )

        #os.system( commandStop )
        #os.system( commandQuit )

        #print ' '.join( vlcArgs )

        #print args[ 0 ]


        cmdList = []

        #for trackStart in [ "open( timetrackerCsv, 'a' ).write( user + '\t' + self.getLabel() + '\t' + 'START' + str( now.strftime( '%Y-%m-%d_%H%M-%S' ) ) + '\n' ).close()" ]:
        #    cmdList.append( trackStart )

        #for trackStart in [ '/Library/Frameworks/Python.framework/Versions/2.7/bin/python', '-c', '\"import os;os.chdir(\'' + self.pypelyneRoot + '\');timeTrackerFile=open(\'' + timetrackerCsv + '\',\'a\');timeTrackerFile.write(\'' + user + '\t' + os.path.basename( self.asset ) + '__' + self.label + '\t' + nowSecs + '\t' + '\');timeTrackerFile.close()', '\"', '&' ]:
        #    cmdList.append( trackStart )

        for touchLocked in [ '/usr/bin/touch', os.path.join( self.location, 'locked' ), '&&' ]:
            cmdList.append( touchLocked )

        for vlcStart in [ '/opt/X11/bin/xterm', '-T', 'screenCast_' + self.label, '-e', ' '.join( vlcArgs ), '&' ]:
            cmdList.append( vlcStart )

        #if not os.path.exists( self.trackerData ):
        #    open( self.trackerData, 'a' ).close()


        timeTrackerFile = open( timetrackerCsv, 'a' )
        timeTrackerFile.write( user + '\t')
        timeTrackerFile.write( self.getLabel() + '\t' )
        timeTrackerFile.write( 'START' + '\t' )
        timeTrackerFile.write( nowSecs + '\t' )
        timeTrackerFile.write( '\n' )
        timeTrackerFile.close()


        for nodeExe in [ '/opt/X11/bin/xterm', '-T', self.label, '-e', executable, newestFile ]:
            cmdList.append( nodeExe )
        for nodeExeArg in args[ 0 ]:
            cmdList.append( nodeExeArg )
        cmdList.append( '&&' )

        for vlcStop in [ '/bin/echo', '-n', 'stop', '|', 'nc', '-U', vlcSocket, '&&' ]:
            cmdList.append( vlcStop )

        for vlcQuit in [ '/bin/echo', '-n', 'quit', '|', 'nc', '-U', vlcSocket, '&&' ]:
            cmdList.append( vlcQuit )

        for rmLocked in [ '/bin/rm', os.path.join( self.location, 'locked' ) ]:
            cmdList.append( rmLocked )




        #cmdList.append( '&&', '/opt/X11/bin/xterm', '-e', ' '.join( vlcArgs ) )
        #print cmdList

        #newTaskProc = subprocess.Popen( str( ' '.join( [ '/usr/bin/touch', os.path.join( self.location, 'locked' ), '&&', '/opt/X11/bin/xterm', '-e', ' '.join( vlcArgs ), '&', '/opt/X11/bin/xterm', '-e', executable, '&&', '/bin/rm', os.path.join( self.location, 'locked' ) ] ) ), shell=True )

        #print str( ' '.join( cmdList ) )

        arguments = QStringList()
        #arguments = [  ]

        for nodeExeArg in args[ 0 ]:
            arguments.append( nodeExeArg )
            
        

        arguments.append( newestFile )
        #print newestFile
        #print args[ 0 ]
        #print str( arguments )
        
        #for i in arguments:
        #    print i
        
        


        #if executable.startswith('"') and executable.endswith('"'):
        #print executable[1:-2], arguments
        executable = executable.replace( '\"', '' )
        executable = executable.replace( '\'', '' )
        if executable.endswith( ' ' ):
            executable = executable[:-1]
        print executable, arguments


        self.process = QProcess( self.mainWindow )
        self.process.started.connect( self.onStarted )
        self.process.finished.connect( self.onFinished )
        self.process.start( executable, arguments )


        #old way (subprocess, xterm):
        #subprocess.Popen( str( ' '.join( cmdList ) ), shell=True )



        #self.processNode = node
        #self.processLabel = self.processNode.getLabel()

        #print args[ 0 ]
        #print type( args[ 0 ] )  

        command = [ executable, newestFile, ' '.join( args[ 0 ] ) ]

        self.process = QProcess( self.mainWindow )
        
        self.process.readyRead.connect( self.dataReady )
        #self.mainWindow.sendTextToBox( "%s: starting %s. Enjoy!\n" %( datetime.datetime.now(), self.data( 0 ).toPyObject() ) )
        self.process.started.connect( self.onStarted )
        self.process.finished.connect( self.onFinished )
        self.process.start( ' '.join( command ) )
        self.pid = self.process.pid()
        #print self.process
        #print self.process.state()

        #while self.process.state() == '1':
        #      print 'active'


    def onStarted( self ):
        print '%s started' %self.label
        #self.
        #asset = os.path.basename( self.asset )
        #print asset

        #self.mainWindow.sendTextToBox( "%s: starting %s (PID %s). Enjoy!\n" %( datetime.datetime.now(), self.data( 0 ).toPyObject(), self.pid ) )

        self.lockFilePath = os.path.join( self.location, 'locked' )
        self.lockFile = open( self.lockFilePath, 'a' )
        self.lockFile.write( self.user )
        self.lockFile.close()

        self.screenCast = screenCast( os.path.basename( self.asset ), self.label, self.project )
        self.screenCast.start()

        self.timeTracker = timeTracker( os.path.basename( self.asset ), self.label, self.project )
        self.timeTracker.start()


    def onFinished( self ):
        print '%s finished' %self.label

        #pid = self.process.pid()

        #self.mainWindow.sendTextToBox( "%s: stopped %s (PID %s).\n" %( datetime.datetime.now(), self.data( 0 ).toPyObject(), self.pid ) )

        #print self.screenCast

        self.screenCast.stop()

        self.timeTracker.stop()

        os.remove( self.lockFilePath )
    '''


    
    

        
    def hoverEnterEvent( self, event ):
        print 'node.hoverEnterEvent'
#         if self.isSelected():
        #self.scene.nodeSelect.emit( self )
#         else:
#             pass
    
    def hoverLeaveEvent( self, event ):
#         if self.isSelected():
        #self.scene.nodeDeselect.emit()
#         else:
#             pass
        print 'node.hoverLeaveEvent'

    def resizeWidth( self ):
        #pass
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
        #self.rect = QRectF( 0, 0, 250, 90 )
        self.resizeHeight()
        self.resizeWidth()
        #self.gradient = QLinearGradient( self.rect.topLeft(), self.rect.bottomLeft() )
        

    def boundingRect( self ):
        return self.rect

    def paint( self, painter, option, widget ):
        painter.setRenderHint( QPainter.Antialiasing )
        
        #self.gradient.setColorAt( 0.5, Qt.grey )
        if os.path.exists( os.path.join( self.location, 'locked' ) ):
            self.gradient.setColorAt( 0, self.taskColorItem )
            self.gradient.setColorAt( 1, Qt.red )
        else:
            self.gradient.setColorAt( 0, self.taskColorItem )
            self.gradient.setColorAt( 1, self.applicationColorItem.darker( 160 ) )
        pen = QPen( Qt.SolidLine )
        pen.setColor( Qt.black )
        pen.setWidth( 0 )
        painter.setBrush( self.gradient )
        #painter.setBrush( self.color )
        #self.palette.setBrush( QBrush( self.gradient ) )
        #self.setPalette( self.palette )
        
        if option.state & QStyle.State_Selected:
            self.updatePropertyNodeXML()
            #self.scene.nodeClicked.emit()
            self.setZValue( 1 )
            pen.setWidth( 1 )
            pen.setColor( Qt.green )
            #self.scene.nodeSelect.emit( self )
        #elif not QStyle.State_Selected:
        #    self.scene.nodeDeselect.emit()
        elif option.state & QStyle.State_MouseOver:
            pen.setWidth( 1 )
            pen.setColor( Qt.yellow )
            #pen.setWidth( 1 )
        else:
            
            pen.setWidth( 0 )
            self.setZValue( 0 )

    
        painter.setPen( pen )

        
        #self.setNodePosition()
        
        '''
        if self.now:
            if int( self.nowStr[ -6: ] ) < 500000:
                painter.setBrush( QColor( 200, 0, 0 ) )
            elif int( self.nowStr[ -6: ] ) >= 500000:
                painter.setBrush( QColor( 100, 0, 0 ) )
        else:
            print 'now not available'
        '''

        painter.drawRoundedRect( self.rect, 10.0, 10.0 )
        
        for i in self.outputList:
            i.setPos( self.boundingRect().width() - i.rect.width(), i.pos().y() )
            
        self.rect.setWidth( self.rect.width() )
        self.arrangeOutputs()
        self.arrangeInputs()
        self.resize()
#         self.rect.setHeight( ( ( max( self.inputs + 1, len( self.outputList ) + 1 ) * 20 ) ) )
        
    def arrangeOutputs( self ):
        #sort list in place according to attribute "label"
        #self.outputs.sort( key=lambda x: x.label, reverse=True )
        for output in self.outputs:
            position = QPointF( self.boundingRect().width() - output.rect.width(), ( ( output.boundingRect().height() * ( self.outputs.index( output ) + 1 ) ) ) )
        
            
            #for inputs:
            #position = QPointF( 0, ( ( self.inputList.index( input ) + 1 ) * input.boundingRect().height() ) )
            
            #position = QPointF( 0, ( ( len( self.outputList ) + 1 ) * output.boundingRect().height() ) )
            output.setPos( position )
            #output.setPos( QPointF( 0, ( ( self.outputList.index[ output ] + 1 ) * output.boundingRect().height() ) ) )
    def arrangeInputs( self ):
        #print 'len( self.inputs ) = %s' %len( self.inputs )
        for input in self.inputs:
            position = QPointF( 0, ( ( self.inputs.index( input ) + 1 ) * input.boundingRect().height() ) )
            input.setPos( position )
        
    #add existing outputs from file system
    def addOutputs( self ):
        
        self.outputRootDir = os.path.join( str( self.location ), 'output' )
        
        allOutputs = os.listdir( self.outputRootDir )
        
        for i in allOutputs:
            if not i in self.exclusions:
                #print 'hoooooooooooooi output = %s' %i
                self.newOutput( self, i )
            
        
        #self.outputs = self.outputs + 1
        #print 'self.outputs = %s' %self.outputs
        #output = portOutput()
        #output.setParentItem( self )
        #self.outputList.append( output )
        
        
        #print 'len( self.outputList ) = %s' %len( self.outputList )
        #print 'self.outputList[ len( self.outputList ) ] = %s' %dir( self.outputList[ len( self.outputList ) ] )


    
    #add existing inputs from file system
    def addInputs( self ):
        self.inputRootDir = os.path.join( str( self.location ), 'input' )
        allInputs = os.listdir( self.inputRootDir )
        for i in allInputs:
            if not i in self.exclusions:
                #print 'input: %s' %i
                input = self.newInput( self.scene )
                #print 'i', i

                #print 'linkpath', os.path.join( self.inputRootDir, i )

                #print 'abspath', os.path.abspath( os.path.join( self.inputRootDir, i ) )

                #print 'readlink', os.readlink( os.path.join( self.inputRootDir, i ) )

                #print 'realpath', os.path.realpath( os.path.join( self.inputRootDir, i ) )

                #print 'basename', os.path.basename( os.path.realpath( os.path.join( self.inputRootDir, i ) ) )

                #print 'lookupdir', os.path.dirname( os.path.realpath( os.path.join( self.inputRootDir, i ) ) )

                lookupDir = os.path.dirname( os.path.join( self.inputRootDir, os.readlink( os.path.join( self.inputRootDir, i ) ) ) )

                #print 'lookupDir', lookupDir
                #print 'lookupDir', os.listdir( lookupDir )

                #if input in 

                #print os.path.basename( os.path.dirname( lookupDir ) ).startswith( 'LDR' )

                #if i in os.listdir( lookupDir ) and os.path.basename( os.path.dirname( lookupDir ) ).startswith( 'LDR' ) == False:
                if not i in os.listdir( lookupDir ) and os.path.basename( os.path.dirname( lookupDir ) ).startswith( 'LDR' ) == True:
                    os.remove( os.path.join( self.inputRootDir, i ) )
                    print 'removed', i

                #if not i in os.listdir( os.path.realpath( os.path.join( self.inputRootDir, i ) ) ):

                #if os.path.isfile( os.path.realpath( os.path.join( self.inputRootDir, i ) ) ) \
                #        or os.path.isdir( os.path.realpath( os.path.join( self.inputRootDir, i ) ) ) \
                #        or os.path.islink( os.path.realpath( os.path.join( self.inputRootDir, i ) ) ):
                    
                    
                else:
                    
                    print 'keep', i
                #input.addText( i )
        
        
        
    
    #add new dynamic input
    def newInput( self, scene ):
        
        #allInputs = []
        input = portInput( self, scene, self.mainWindow )
        input.setParentItem( self )
        
        #self.inputs = self.inputs + 1
        self.inputList.append( input )
        
        #print 'node.inputList = %s' %self.inputList
        
        #for i in self.inputList:
        #    print 'input.childItems() = %s' %i.childItems()
        
        self.inputMaxWidth.append( input.childrenBoundingRect().width() )
        
        self.resizeHeight()
        
    def updatePropertyNodeXML( self ):
        pos = self.scenePos()
        #print pos.x()
        #print pos.y()
        propertyNode = ET.parse( self.propertyNodePath )
        propertyNodeRoot = propertyNode.getroot()
        #positionX = self.valueApplications.findall( './positionX' )
        #positionY = self.valueApplications.findall( './positionY' )
        
        try:
            #print 'new style positioning...'
            nodePosition = propertyNodeRoot.find( 'node' )

            nodePosition.set( 'positionX', '%s' %pos.x() )
            nodePosition.set( 'positionY', '%s' %pos.y() )


        except:
            #print 'old style positioning...'
            positionX = propertyNodeRoot.find( 'positionX' )
            positionY = propertyNodeRoot.find( 'positionY' )

            positionX.set( 'value', '%s' %pos.x() )
            positionY.set( 'value', '%s' %pos.y() )
        
        
        #ET.tostring( propertyNode )
        #print positionX.attrib
        #print positionY.attrib
        
        
        #print ET.tostring( propertyNodeRoot )
        #ET.tostring( propertyNode )
        
        xmlDoc = open( self.propertyNodePath, 'w' )
        
        xmlDoc.write( '<?xml version="1.0"?>' )
        xmlDoc.write( ET.tostring( propertyNodeRoot ) )
        xmlDoc.close()
        #print 'hallo'
#         families = self.valueApplications.findall( './family' )
    
    
    #add new dynamic output:
    def newOutput( self, node, name ):

        #self.outputDir = os.path.join( self.outputRootDir, name )

        #print '____________outputDir = &s' self.outputDir

        #allOutputs = []
        #print name



        output = portOutput( self, name, self.mainWindow )

        if len( name.split( '.' ) ) > 1:


            #print i.split( '.' )
            #self.newOutput( self, i.split( '.' )[ 3 ] )
            output.addText( node, name.split( '.' )[ 3 ] )

        else:

            

            #print 'outputDir = %s' %output.getOutputDir()
            
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


        #self.setTaskColor()
        self.resizeWidth()

    def setApplicationColor( self ):
        self.applicationColorItem.setNamedColor( self.taskColor )
        #self.applicationColorItem.darker( factor=200 )


    def setTaskColor( self ):
        
        #pass
        #self.gradient.setColorAt( 0, Qt.blue )
        #self.gradient.setColorAt( 1, Qt.green )

        #self.palette = QPalette
        

        #print self._tasks

        
        #print self._tasks[ 0 ].index( ('value', 'modelling') )
        index = 0

        #print os.path.basename( self.location )[ :7 ]
        #self.taskColor = '#444444'


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
                #print i.index( filter( lambda n: n.get( 'value' ) == 'modelling', i )[ 0 ] )
            #    if self.nodeTask in i:
            #        print i
                if [item for item in i if self.nodeTask in item]:
                    print 'found'
                    self.taskColor = self._tasks[ index ][ 0 ][ 1 ]
                    break
                    '''
                elif str( self.data( 0 ).toPyObject() ) [ :3 ] == 'SVR':
                    print 'SVR found'
                    self.taskColor = '#333333'
                    break
                    '''
                else:
                    index += 1

        #self.taskColorItem = QColor( 0, 0, 0 )
        #self.taskColorItem = color.setNamedColor( self.taskColor )

        #print self.taskColor

        self.taskColorItem.setNamedColor( self.taskColor )

        #print index
        #print self._tasks[ index ]
        #print self.taskColor
        #print [item for item in self._tasks if self.nodeTask in item[ 1 ]]
        #nodeTaskInfo = self._tasks.findall( './MDL' )
        #print nodeTaskInfo
        #print self._tasks
        #print self.data( 0 ).toPyObject()


        #self.color = QColor( 200, 0, 0 )
        #self.color.setNamedColor( self.taskColor )

        #return self.taskColor
        
                
                
                
