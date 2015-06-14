import os, sip, sys, subprocess, platform, re, shutil, random, datetime, getpass
from operator import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import *
from PyQt4.QtOpenGL import *

from src.pypelyneConfigurationWindow import *
#from src.node import *
#from src.circlesInOut import *
from src.bezierLine import *
from src.graphicsScene import *
from src.screenCast import *
#from screenCast import *
from src.timeTracker import *

#from src.parseApplications import *

import xml.etree.ElementTree as ET

from src.vlc import *
#let's see





app = None
        
        
class nodeWidgetUi( QWidget ):
    def __init__( self, mainWindow, parent = None ):
        super( nodeWidgetUi, self ).__init__( parent )
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.currentPlatform = self.mainWindow.getCurrentPlatform()
        '''
        if self.currentPlatform == "Windows":
            self.ui = loadUi( r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\nodeWidget.ui', self )
        elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
            self.ui = loadUi( r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/nodeWidget.ui', self )
        '''

        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'nodeWidget.ui' ), self )



class playerWidgetUi( QWidget ):
    def __init__( self, mainWindow, parent = None ):
        super( playerWidgetUi, self ).__init__( parent )
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.currentPlatform = self.mainWindow.getCurrentPlatform()
        '''
        if self.currentPlatform == "Windows":
            self.ui = loadUi( r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\player.ui', self )
        elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
            print self.pypelyneRoot
            self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'player.ui' ), self )
        '''

        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'player.ui' ), self )


class pypelyneMainWindow( QMainWindow ):
    def __init__( self, parent = None ):
        super( pypelyneMainWindow, self ).__init__( parent )
        
        self.exclusions = [ '.DS_Store', 'Thumbs.db' ]
        self.imageExtensions = [ '.jpg', '.exr', '.tga', '.png' ]
        self.movieExtensions = [ '.mov', '.avi' ]
        
        self.currentPlatform = platform.system()

        self.pypelyneRoot = os.getcwd()

        self.user = getpass.getuser()
        #self.projectsRoot = os.path.join( self.pypelyneRoot, 'projects' )


        if self.currentPlatform == "Windows":
            self.projectsRoot = os.path.join( r'C:\pypelyne_projects' )
            self.audioFolder = r'C:\audio'
            self.screenCastExec = r''
        elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
            #self.projectsRoot = os.path.join( r'/Volumes/pili/pypelyne_projects' )
            self.projectsRoot = os.path.join( r'/Volumes/osx_production/pypelyne_projects' )
            self.audioFolder = r'/Volumes/pili/library/audio'
            self.screenCastExec = r'/Applications/VLC.app/Contents/MacOS/VLC'
            self.sequenceExec = r'/Applications/RV64.app/Contents/MacOS/RV'


        
        #self.audioFolder = r'/Volumes/pili/library/audio'
        #print self.projectsRoot
        
        #self.shotsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'shots' )
        #self.assetsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'assets' )
        
        self.nodeWidgets = []
        self.qprocesses = []
        self.openNodes = []
        self.timeTrackers = []
        self.screenCasts = []

            
        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'pypelyneMainWindow.ui' ), self )
        
        self.nodeView.setVisible( False )
        self.assetsShotsTabWidget.setVisible( False )
        self.statusBox.setVisible( False )
        self.nodeOptionsWindow.setVisible( False )
        self.descriptionWindow.setVisible( False )
        self.openPushButton.setVisible( True )
        self.checkBoxDescription.setVisible( False )

        self.openPushButton.setEnabled( False )

        
        
        
        self.computeValueApplications()
        self.computeValueTasks()
        self.computeValueOutputs()

        # Scene view
        self.scene = SceneView( self )
        self.nodeView.setViewport( QGLWidget( QGLFormat( QGL.SampleBuffers ) ) )
        self.nodeView.setScene( self.scene )
        self.nodeView.setHorizontalScrollBarPolicy ( Qt.ScrollBarAlwaysOn )
        self.nodeView.setVerticalScrollBarPolicy ( Qt.ScrollBarAlwaysOn )
        #self.nodeView.setSceneRect(0, 0, 630, 555)
        
        self.scalingFactor = 1
        
        self.currentContent = None
        
        self.mapSize = ( 512, 512 )
        #self.scene = GraphicsScene(self)
        #self.scene.addRect( QRectF( 0, 0, self.mapSize ), Qt.red )
        #self.addRect()
        #self.boundary = self.scene.addRect( QRectF( -1000, -1000, 1000, 1000 ), Qt.red )
        #self.view = QGraphicsView()
        #self.scene.setScene(self.scene)
        #self.scene.resize(self.scene.width(), self.scene.height())
        #self.setCentralWidget(self.view)

        # Graphics View
        self.nodeView.wheelEvent = self.graphicsView_wheelEvent
        #self.nodeView.resizeEvent = self.graphicsView_resizeEvent
        self.nodeView.setBackgroundBrush( QBrush( QColor( 60, 60, 60, 255 ), Qt.SolidPattern ) )

        # Projects
        self.addProjects()
        
        
        #self.addContent()
        
        # Tools
        self.addTools()
        

        if os.path.exists( self.audioFolder ):
            self.addPlayer()
            if len( os.listdir( self.audioFolder ) ) == 0:
                #print 'no audio files found'
                self.playerUi.radioButtonPlay.setEnabled( False )
                self.playerUi.radioButtonStop.setEnabled( False )
                self.playerUi.buttonSkip.setEnabled( False )
        
        
        self.runToolPushButton.clicked.connect( self.runTool )
        
        self.checkBoxConsole.stateChanged.connect( self.toggleConsole )
        self.checkBoxNodeName.stateChanged.connect( self.toggleNodeName )
        self.checkBoxDescription.stateChanged.connect( self.toggleDescription )
        self.checkBoxContentBrowser.stateChanged.connect( self.toggleContentBrowser )
        #self.checkBoxNodesWindow.stateChanged.connect( self.toggleNodesWindow )
        #self.scene.nodeClicked.connect( self.setWidgetMenu )
        
        # configuration window
        self.configPushButton.clicked.connect( self.configurationWindow )
        self.scene.nodeSelect.connect( self.setNodeWidget )
        self.scene.nodeDeselect.connect( self.clearNodeWidget )
        self.openPushButton.clicked.connect( lambda: self.locateContent( os.path.join( self.projectsRoot, str( self.projectComboBox.currentText() ) ) ) )
        
        #self.scene = SceneView()
        self.scene.textMessage.connect( self.sendTextToBox )
        #self.scene.nodeClicked.connect( self.setNodeMenuWidget )
        #self.scene.nodeMenu.connect( self.setWidgetMenu )
        
        #self.scene.nodeMenuArea.connect( self.updateNodeMenu )

    def getUser( self ):
        return self.user

    def closeEvent( self, event ):

        if len( self.timeTrackers ) > 0 or len( self.screenCasts ) > 0 or len( self.qprocesses ) > 0:

            quit_msg = "Too early to leave. There is still something running..."

            reply = QMessageBox.critical( self, 'Message', quit_msg, QMessageBox.Ok )


            #print 'about to close'

        else:
            quit_msg = "Are you sure you want to exit PyPELyNE?"

            reply = QMessageBox.question( self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No )


        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def getExclusions( self ):
        return self.exclusions

    def getImageExtensions( self ):
        return self.imageExtensions

    def getMovieExtensions( self ):
        return self.movieExtensions

    def getSequenceExec( self ):
        return self.sequenceExec

    def addPlayer( self ):

        self.playerUi = playerWidgetUi( self )
        self.horizontalLayout.addWidget( self.playerUi )
        self.playerUi.radioButtonPlay.clicked.connect( self.playAudio )
        self.playerUi.radioButtonStop.clicked.connect( self.stopAudio )
        self.playerUi.buttonSkip.clicked.connect(self.skipAudio)

        self.playerExists = False
        

    def cb( self, event ):
        print 'cb:', event.type, event.u

    def playAudio( self ):

        # https://forum.videolan.org/viewtopic.php?t=107039

        if len( os.listdir( self.audioFolder ) ) == 0:
            print 'no audio files found'
            self.playerUi.radioButtonPlay.setEnabled( False )

        elif self.playerExists == False:





            print 'playing'
            
            self.audioFolderContent = os.listdir( self.audioFolder )
            #print self.audioFolderContent
            random.shuffle( self.audioFolderContent, random.random )
            #print self.audioFolderContent


            self.mlp = MediaListPlayer()
            self.mp = MediaPlayer()
            self.mlp.set_media_player( self.mp )

            '''
            self.mlp_em = self.mlp.event_manager()
            self.mlp_em.event_attach( EventType.MediaListPlayerNextItemSet, self.cb )

            self.mp_em = self.mp.event_manager
            self.mp_em.event_attach( EventType.MediaPlayerEndReached, self.cb )
            self.mp_em.event_attach( EventType.MediaPlayerMediaChanged, self.cb )
            '''

            self.ml = MediaList()

            for track in self.audioFolderContent:
                self.ml.add_media( os.path.join( self.audioFolder, track ) )

            self.mlp.set_media_list( self.ml )

            self.mlp.play()









            '''
            self.vlcInstance = Instance()
            self.player = self.vlcInstance.media_player_new()


            #print self.audioFolderContent
            self.randValue = random.randint( 0, len( self.audioFolderContent ) - 1 )

            print 'max = %s' %len( self.audioFolderContent )
            print self.randValue
            self.track = os.path.join( self.audioFolder, self.audioFolderContent[ self.randValue ] )
            print 'playing: %s' %self.track

            self.media = self.vlcInstance.media_new( self.track )

            self.player.set_media( self.media )
            #self.player.set_media( self.track )
            #print 'playing %s' %( os.path.join( self.audioFolder, self.audioFolderContent[ random.randint( 0, len( self.audioFolderContent ) ) ] ) )
            self.player.play()

            '''

            self.playerExists = True

        else:
            print 'already on air'

    def skipAudio( self ):
        self.mlp.next()


    def stopAudio( self ):
        
        try:
            self.mp.stop()
            self.mp.release()
            self.mlp.release()
            self.playerExists = False
            print 'stopped'
        except:
            print 'error or not playing'

        
    def getCurrentPlatform( self ):
        return self.currentPlatform
        
    def getProjectsRoot( self ):
        return self.projectsRoot
    
    def getCurrentContent( self ):
        return self.currentContent

    def addRectangular( self ):
        #self.scene.addRect( QRectF( 0, 0, self.mapSize ), Qt.red )
        pass

    def computeValueOutputs( self ):
        #print os.path.join( self.pypelyneRoot, 'conf', 'valueOutputs.xml' )
        self.valueOutputs = ET.parse( os.path.join( self.pypelyneRoot, 'conf', 'valueOutputs.xml' ) )
        self.valueOutputsRoot = self.valueOutputs.getroot()

        self._outputs = []
        categoryList = []
        mimeList = []
        itemList = []

        for category in self.valueOutputsRoot:
            itemList.append( category.items() )
            for mime in category:
                itemList.append( mime.items() )
                #category.items().append( mime )
                #self._outputs.append( category.itemssubmissionCmdArgs() )

            self._outputs.append( itemList )
            itemList = []

            #print category.items()
        #print self._outputs
        '''
        for output in self._outputs:
            #abbrev
            print output[ 0 ][ 2 ][ 1 ]
            #full output name
            print output[ 0 ][ 1 ][ 1 ]
            #for output in outputCollection[ 0 ]:
            #    print output
        '''
    
    def computeValueTasks( self ):
        self.valueTasks = ET.parse( os.path.join( self.pypelyneRoot, 'conf', 'valueTasks.xml' ) )
        self.valueTasksRoot = self.valueTasks.getroot()

        self._tasks = []

        for category in self.valueTasksRoot:
            self._tasks.append( category.items() )

        #print self._tasks
            #print category.items()

    def runTask( self, node, executable, newestFile, *args ):

        #print executable

        makingOfDir = os.path.join( self.getCurrentProject(), 'making_of' )

        #now = str( datetime.datetime.now().strftime( '%Y-%m-%d_%H%M-%S' ) )
        now = datetime.datetime.now()

        nowSecs = str( now.strftime( '%Y-%m-%d_%H%M-%S' ) )
        nowMilliSecs = str( now.strftime( '%Y-%m-%d_%H%M-%S_%f' ) )

        #user = self.mainWindow.getUser()


        #if not os.path.exists( makingOfDir ):
        #    os.makedirs( makingOfDir, mode=0777 )

        '''
        timeTrackerDir = os.path.join( self.project, 'timetracker' )
        if not os.path.exists( timeTrackerDir ):
            os.makedirs( timeTrackerDir, mode=0777 )
        timetrackerCsv = os.path.join( timeTrackerDir, 'timetracker.csv' )
        if not os.path.exists( timetrackerCsv ):
            open( timetrackerCsv, 'a' ).close()
        '''

        #trackThis = timeTracker( os.path.basename( self.asset ), os.path.basename( self.location ), self.project )

        #trackThis.start()


        #mp4 = makingOfDir + os.sep + nowSecs + '__' + self.user + '__' + os.path.basename( self.asset ) + '__' + self.label + '.mp4'
        #print self.mp4

        #print os.path.expanduser('~'), str( 'vlc.sock' + '.' + self.now + '__' + self.user + '__' + self.assetName + '__' + self.taskName )

        #vlcExec = r'/Applications/VLC.app/Contents/MacOS/VLC'

        #vlcSocket = os.path.join( os.path.expanduser('~'), str( 'vlc.sock' + '.' + now + '__' + user + '__' + os.path.basename( self.asset ) + '__' + self.label ) )
        #vlcSocket = os.path.join( os.path.expanduser('~'), str( 'vlc.sock' + '.' + nowMilliSecs ) )

        #vlcArgs = [ vlcExec, '-I', 'rc', '--rc-fake-tty', '--rc-unix', vlcSocket, 'screen://', '--screen-fps', '4', '--quiet', '--sout', '"#transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst=' + mp4 + '}"' ]

        #commandStop = "echo stop | nc -U " + self.vlcSocket
        #commandQuit = "echo quit | nc -U " + self.vlcSocket

        #print commandStop
        #print commandQuit

        #time.sleep( 15 )

        #os.system( commandStop )
        #os.system( commandQuit )

        #print ' '.join( vlcArgs )

        #print args[ 0 ]


        #cmdList = []

        #for trackStart in [ "open( timetrackerCsv, 'a' ).write( user + '\t' + self.getLabel() + '\t' + 'START' + str( now.strftime( '%Y-%m-%d_%H%M-%S' ) ) + '\n' ).close()" ]:
        #    cmdList.append( trackStart )

        #for trackStart in [ '/Library/Frameworks/Python.framework/Versions/2.7/bin/python', '-c', '\"import os;os.chdir(\'' + self.pypelyneRoot + '\');timeTrackerFile=open(\'' + timetrackerCsv + '\',\'a\');timeTrackerFile.write(\'' + user + '\t' + os.path.basename( self.asset ) + '__' + self.label + '\t' + nowSecs + '\t' + '\');timeTrackerFile.close()', '\"', '&' ]:
        #    cmdList.append( trackStart )

        #for touchLocked in [ '/usr/bin/touch', os.path.join( self.location, 'locked' ), '&&' ]:
        #    cmdList.append( touchLocked )

        #for vlcStart in [ '/opt/X11/bin/xterm', '-T', 'screenCast_' + self.label, '-e', ' '.join( vlcArgs ), '&' ]:
        #    cmdList.append( vlcStart )

        #if not os.path.exists( self.trackerData ):
        #    open( self.trackerData, 'a' ).close()

        '''
        timeTrackerFile = open( timetrackerCsv, 'a' )
        timeTrackerFile.write( user + '\t')
        timeTrackerFile.write( self.getLabel() + '\t' )
        timeTrackerFile.write( 'START' + '\t' )
        timeTrackerFile.write( nowSecs + '\t' )
        timeTrackerFile.write( '\n' )
        timeTrackerFile.close()
        '''

        #for nodeExe in [ '/opt/X11/bin/xterm', '-T', self.label, '-e', executable, newestFile ]:
        #    cmdList.append( nodeExe )
        #for nodeExeArg in args[ 0 ]:
        #    cmdList.append( nodeExeArg )
        #cmdList.append( '&&' )

        #for vlcStop in [ '/bin/echo', '-n', 'stop', '|', 'nc', '-U', vlcSocket, '&&' ]:
        #    cmdList.append( vlcStop )

        #for vlcQuit in [ '/bin/echo', '-n', 'quit', '|', 'nc', '-U', vlcSocket, '&&' ]:
        #    cmdList.append( vlcQuit )

        #for rmLocked in [ '/bin/rm', os.path.join( self.location, 'locked' ) ]:
        #    cmdList.append( rmLocked )




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

        for i in arguments:
            print i




        #if executable.startswith('"') and executable.endswith('"'):
        #print executable[1:-2], arguments
        executable = executable.replace( '\"', '' )
        executable = executable.replace( '\'', '' )
        if executable.endswith( ' ' ):
            executable = executable[:-1]
        print executable, arguments



        newScreenCast = screenCast( os.path.basename( node.getNodeAsset() ), node.getLabel(), node.getNodeProject() )
        newTimeTracker = timeTracker( os.path.basename( node.getNodeAsset() ), node.getLabel(), node.getNodeProject() )


        process = QProcess( self )
        #process.readyRead.connect( lambda: self.dataReady( process ) )
        process.readyReadStandardOutput.connect( lambda: self.dataReadyStd( process ) )
        process.readyReadStandardError.connect( lambda: self.dataReadyErr( process ) )
        process.started.connect( lambda: self.onStarted( node, process, newScreenCast, newTimeTracker ) )
        #process.started.connect( lambda:  )
        process.finished.connect( lambda: self.onFinished( node, process, newScreenCast, newTimeTracker ) )
        process.start( executable, arguments )





        #old way (subprocess, xterm):
        #subprocess.Popen( str( ' '.join( cmdList ) ), shell=True )



        '''
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
        '''

    def onStarted( self, node, qprocess, screenCast, timeTracker ):

        self.qprocesses.append( qprocess )
        self.openNodes.append( node )
        print self.qprocesses

        print '%s started' %node.getLabel()
        # #self.
        # #asset = os.path.basename( self.asset )
        # #print asset
        #
        # #self.mainWindow.sendTextToBox( "%s: starting %s (PID %s). Enjoy!\n" %( datetime.datetime.now(), self.data( 0 ).toPyObject(), self.pid ) )
        #

        lockFilePath = os.path.join( node.getNodeRootDir(), 'locked' )
        lockFile = open( lockFilePath, 'a' )
        lockFile.write( self.user )
        lockFile.close()
        #

        screenCast.start()
        self.screenCasts.append( screenCast )
        #

        timeTracker.start()
        self.timeTrackers.append( timeTracker )


    def onFinished( self, node, qprocess, screenCast, timeTracker ):
        print '%s finished' %node.getLabel()
        #
        # #pid = self.process.pid()
        #
        # #self.mainWindow.sendTextToBox( "%s: stopped %s (PID %s).\n" %( datetime.datetime.now(), self.data( 0 ).toPyObject(), self.pid ) )
        #
        # #print self.screenCast
        #
        screenCast.stop()
        self.screenCasts.remove( screenCast )
        #
        timeTracker.stop()
        self.timeTrackers.remove( timeTracker )
        #
        os.remove( os.path.join( node.getNodeRootDir(), 'locked' ) )

        self.openNodes.remove( node )
        self.qprocesses.remove( qprocess )
        print self.qprocesses




    def computeValueApplications( self ):
        self.valueApplications = ET.parse( os.path.join( self.pypelyneRoot, 'conf', 'valueApplications.xml' ) )
        self.valueApplicationsRoot = self.valueApplications.getroot()
        
        #print 'hallo'
#         families = self.valueApplications.findall( './family' )
#         for i in families:
#             print i.items()[ 0 ][ 1 ]
        
        self._tools = []
        
        for family in self.valueApplicationsRoot:

            directoryList = []
            defaultOutputList = []

            directories = family.findall( './directory' )
            defaultOutputs = family.findall( './defaultOutput' )

            for defaultOutput in defaultOutputs:
                defaultOutputList.append( defaultOutput.items()[ 0 ][ 1 ] )
                #print defaultOutput.items()[ 0 ][ 1 ]

            #print directories
            for directory in directories:
                #print directory.items()[ 0 ][ 1 ]
                
                directoryList.append( directory.items()[ 0 ][ 1 ] )

                subdirectories = directory.findall( './subdirectory' )
                #print subdirectories

                #subdirectoryList = []

                for subdirectory in subdirectories:
                    #print subdirectory.items()
                    directoryList.append( directory.items()[ 0 ][ 1 ] + os.sep + subdirectory.items()[ 0 ][ 1 ] )

                    subsubdirectories = subdirectory.findall( './subdirectory' )

                    for subsubdirectory in subsubdirectories:

                        #print subsubdirectory
                        directoryList.append( directory.items()[ 0 ][ 1 ] + os.sep + subdirectory.items()[ 0 ][ 1 ] + os.sep + subsubdirectory.items()[ 0 ][ 1 ] )




                

            for vendor in family:
                for version in vendor:
                    for platform in version:
                        for executable in platform:
                            flags = []
                            for flag in executable:
                                flags.append( flag.items()[ 0 ][ 1 ] )
                            if not executable.items()[ 0 ][ 1 ] == 'None' and platform.items()[ 0 ][ 1 ] == self.currentPlatform:
                                
                                #command = [ "\"" + executable.items()[ 0 ][ 1 ] + "\" " + ' '.join( flags ) ]
                                command = [ "\"" + executable.items()[ 0 ][ 1 ] + "\"" ]
                                
                                path = re.findall( r'"([^"]*)"', command[ 0 ] )[ 0 ]
                                if os.path.exists( os.path.normpath( path ) ):

                                    familyValue = family.items()[ 1 ][ 1 ]
                                    familyAbbreviation = family.items()[ 0 ][ 1 ]
                                    vendorValue = vendor.items()[ 0 ][ 1 ]
                                    versionValue = version.items()[ 0 ][ 1 ]
                                    versionTemplate = version.items()[ 1 ][ 1 ]
                                    #print 'versionTemplate = %s' % version.items()[ 1 ][ 1 ]
                                    platformValue = platform.items()[ 0 ][ 1 ]
                                    executableArch = executable.tag

                                    #self._tools.append( ( vendor.items()[ 0 ][ 1 ] + ' ' + family.items()[ 1 ][ 1 ] + ' ' + version.items()[ 0 ][ 1 ] + ' ' + platform.items()[ 0 ][ 1 ] + ' ' + executable.tag, command, familyAbbreviation ) )
                                    #self._tools.append( ( vendorValue + ' ' + familyValue + ' ' + versionValue + ' ' + platformValue + ' ' + executableArch, command, familyAbbreviation, vendorValue, familyValue, versionValue, executableArch ) )
                                    self._tools.append( ( vendorValue + ' ' + familyValue + ' ' + versionValue + ' ' + executableArch, command, familyAbbreviation, vendorValue, familyValue, versionValue, executableArch, versionTemplate, directoryList, defaultOutputList, flags ) )
                                else:
                                    print 'path not found: %s. application not added to tools dropdown' %( path )
                                    self.sendTextToBox( 'path not found: %s. application not added to tools dropdown\n' %( path ) )

        #print self._tools
    
#     @pyqtSlot()
#     def test( self ):
#         print 'test'

    
    def getOutputs( self ):
        return self._outputs

    
    def getTasks( self ):
        return self._tasks
        
    def getTools( self ):
        return self._tools
    
    
    def locateContent( self, contentFiles ):
        if os.path.exists( contentFiles ):
            if self.currentPlatform == 'Windows':
                subprocess.call( 'explorer.exe %s' %contentFiles, shell=False )
            elif self.currentPlatform == 'Darwin':
                subprocess.call( 'open %s' %contentFiles, shell=True )
            else:
                self.sendTextToBox( 'platform %s not supported\n' %self.currentPlatform )
        else:

            print 'project does not exist:', contentFiles
    
    def cloneContent( self, contentFiles ):
        tabIndex = self.assetsShotsTabWidget.currentIndex()
        #print contentFiles
        cloneExtension = '_clone'
        cloneDestination = contentFiles + cloneExtension
        
        shutil.copytree( contentFiles, cloneDestination )
        
        self.sendTextToBox( 'content at %s cloned to %s\n' %( contentFiles, cloneDestination ) )
        
        self.addContent()
        self.assetsShotsTabWidget.setCurrentIndex( tabIndex )
    
    def removeContent( self, contentFiles ):
        tabIndex = self.assetsShotsTabWidget.currentIndex()
        #print contentFiles
        
        shutil.rmtree( contentFiles )
        self.sendTextToBox( 'content removed from filesystem: %s\n' %contentFiles )
        
        self.addContent()
        self.refreshProjects()
        self.assetsShotsTabWidget.setCurrentIndex( tabIndex )
    
    def createNewContent( self ):
        self.items = [ 'asset', 'shot' ]
        tabIndex = self.assetsShotsTabWidget.currentIndex()
        # tabPosition 0 = assets
        # tabPosition 1 = shots

        text, ok = QInputDialog.getText( self, 'create new %s' %self.items[ tabIndex ], 'enter %s name:' %self.items[ tabIndex ] )
        
        
        
        if tabIndex == 0:
            newContentPath = self.assetsRoot
            
        elif tabIndex == 1:
            newContentPath = self.shotsRoot
            
        newContent = os.path.join( newContentPath, str( text ) )
        
        if ok:
            os.makedirs( newContent, mode=0777 )
            self.addContent()
            self.sendTextToBox( 'content created on filesystem: %s\n' %newContent )
            
        else:
            pass
            
        
        #self.createNewContent()
        self.assetsShotsTabWidget.setCurrentIndex( tabIndex )
            
    
#     def mousePressEvent( self, event ):
#         self.menu = QMenu()
#         
#         #objectClicked = self.itemAt( pos )
#         
#         items = []
#         
#         #self.menu.addAction( 'new node', self.newNodeDialog( pos ) )
#         
#         if isinstance( QPushButton ):
#             
#         
#         if isinstance( objectClicked, QPushButton ):
#             items.append( 'delete this asset' )
# 
# 
#                 
#         if isinstance( objectClicked, QPushButton ):
#             items.append( 'delete this shot' )
# 
#                 
#         
# 
#                 
#                 
#         for item in items:
# 
#             self.menu.addAction( item, self.removeObject( objectClicked ) )
#         
# 
#         
#         self.menu.move( QCursor.pos() )
#         self.menu.show()

    def getPypelyneRoot( self ):
        return self.pypelyneRoot

    def setNodeWidget( self, node ):
        self.widgetUi = nodeWidgetUi( self )
            
        self.nodeMenuArea.setWidget( self.widgetUi )

        
        # self.nodeVersion, self.nodeVendor, self.nodeFamily, self.nodeArch
        self.nodeApplicationInfo = node.queryApplicationInfo()


        self.widgetUi.labelNode.setText( node.data( 0 ).toPyObject() )
        self.widgetUi.labelApplication.setText( self.nodeApplicationInfo[ 2 ] + ' ' + self.nodeApplicationInfo[ 0 ] )
        #self.widgetUi.labelVersion.setText( self.nodeApplicationInfo[ 0 ] )
        #self.widgetUi.labelExecutable.setText( node.data( 0 ).toPyObject() )





    def clearNodeWidget( self ):
        #self.nodeWidgets = []
        self.nodeMenuArea.takeWidget()
        
    def configurationWindow( self ):
        self.configWindow = pypelyneConfigurationWindow()
        self.configWindow.show()
        
    def computeConnections( self ):
        print 'computeConnections...'
        nodeList = self.scene.getNodeList()
        #print any( node for node in nodeList if node.data( 0 ).toPyObject() == 'fnuzjr' )
        #for node in nodeList:
        #    if node.data( 0 ).toPyObject() == 'fnuzjr':
        #        print 'node found at index %s' %( nodeList.index( node ) )
        for node in nodeList:
            currentNode = node
            #if node.data( 0 ).toPyObject() == 'fnuzjr':
            #    print 'found it...eeeeeeeeeeeeee'
            print 'processing %s (%s)' %( node.data( 0 ).toPyObject(), node )
            nodeRootDir = node.getNodeRootDir()
            nodeInputDir = os.sep.join( [ str( nodeRootDir ), 'input' ] )
            print 'nodeInputDir = %s' %nodeInputDir
            inputs = os.listdir( nodeInputDir )
            if len( inputs ) > 0:
                for input in inputs:
                	#tempList = []
                    #print input
                    if not input in self.exclusions:
                        string = input.split( '.' )
                        print 'string', string
                        #print string
                        #print 'string = %s' %string
                        
                        for node in nodeList:
                            print 'nodeList:', nodeList
                            #print node.data( 0 ).toPyObject()

                            #if str( node.data( 0 ).toPyObject() ).startswith( 'LDR' ):


                            #print 'hurrrraaaa', node.getLabel()
                            #print node.data( 0 ).toPyObject()
                            #print string
                            if node.data( 0 ).toPyObject() == string[ 2 ] or str( node.data( 0 ).toPyObject() ).startswith( 'LDR' ):
                                #print 'source node %s found at index %s' %( node.data( 0 ).toPyObject(), nodeList.index( node ) )
                                sourceNodeIndex = nodeList.index( node )
                                #print 'node name = %s' %( node.data( 0 ).toPyObject() )
                                sourceNode = node
                                #tempList.append( node )
                                outputList = node.outputList
                                #print 'outputs: %s' %( outputList )
                                for output in outputList:
                                    print 'processing =', output.data( 0 ).toPyObject()
                                    #print output.data( 0 ).toPyObject()
                                    #print 'output.data( 0 ).toPyObject()', output.data( 0 ).toPyObject()
                                    #print 'str( output.data( 0 ).toPyObject() ).split( . )', str( output.data( 0 ).toPyObject() ).split( '.' )

                                    if len( str( output.data( 0 ).toPyObject() ).split( '.' ) ) == 1:

                                        if output.data( 0 ).toPyObject() == string[ 3 ]:
                                            #print 'source output of %s found at index %s' %( output.data( 0 ).toPyObject(), outputList.index( output ) )
                                            #print 'output', output
                                            startItem = output
                                            print 'if: startItem =', startItem

                                    else:
                                        if str( output.data( 0 ).toPyObject() ).split( '.' )[ 3 ] == string[ 3 ]:
                                            startItem = output
                                            #loader
                                            print 'else: startItem =', startItem
                                            #startItem = outputList[ outputList.index( output ) ]
                                            #print 'startItem = %s' %( startItem )
                                            #print 'startItem = %s (%s)' %( startItem, startItem.data( 0 ).toPyObject() )
                                        
                                
                        
                        #print string
                        #newInput = node.newInput( self.scene )
                        #endItem:
                        #print 'bezier needed to: %s ( node.data( 0 ): %s)' %( node, node.data( 0 ).toPyObject() )
                        #print nodeList
                        #print 'tempList = %s' %( tempList )
                        #print 'sourceNodeIndex: %s' %( sourceNodeIndex )
                        #print 'sourceNode: %s' %( sourceNode.data( 0 ).toPyObject() )
                        #endItem = node.inputList[ 0 ]
                        #endItem = nodeList.index( node )
                        
                        #endItem = sourceNode.inputList[ len( node.inputs ) ]
                        #endItem = nodeList[ sourceNodeIndex ].inputList[ len( node.inputs ) ]
                        endItem = currentNode.inputList[ len( currentNode.inputs ) ]
                        #print 'endItem = %s' %( node.inputList[ 0 ] )
                        #print 'endNode = %s' %( node.data( 0 ).toPyObject() )
                        #print 'endItem = %s' %( endItem )
                        #print 'endItemInputDir = %s' %endItem.getInputDir()
                        #endItem = node
                        #print 'need to create input with name: %s on node: %s' %( input, node.data( 0 ).toPyObject() )
                        #newInput.addText( input )

                        print 'new line from to:', startItem, endItem
                        
                        connectionLine = bezierLine( self, self.scene, startItem, endItem )
                        
                        
                        
                        
                        endItem.parentItem().inputs.append( endItem )
                        endItem.connection.append( connectionLine )
                        endItem.output.append( startItem )
                        endItem.parentItem().incoming.append( startItem )
                        startItem.inputs.append( endItem )
                        
                        
                        
                        startItemRootDir = startItem.parentItem().getNodeRootDir()
                        endItemRootDir = endItem.parentItem().getNodeRootDir()
                        
                        startItemOutputLabel = startItem.getLabel()
                        
                        
                        #startItemOutputDir = os.path.join( str( startItemRootDir ), 'output', str( startItemOutputLabel ) )
                        endItemInputDir = os.path.join( str( endItemRootDir ), 'input', str( input ) )
                        
                        endItem.setInputDir( endItemInputDir )
                        
                        
                        
                        
                        self.scene.addItem( connectionLine )
                        
                        

                        endItem.parentItem().newInput( self.scene )
                        #print 'endItemInputDir = %s' %endItem.getInputDir()
                    else:
                        print 'input data is in exclusions list'
                    
            else:
                print 'node %s has no input' %( node.data( 0 ).toPyObject() )

        
    def getPropertyPaths( self ):
        return self.propertyNodePathAssets, self.propertyNodePathShots

    def getShotContent( self, shotButton ):
        
        self.nodeView.setVisible( True )
        
        buttonText = shotButton.text()

        self.scene.clear()
        self.addRectangular()
        self.scene.clearNodeList()
        currentProject = str( self.projectComboBox.currentText() )
        self.shotsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'shots' )
        shotContent = os.listdir( os.path.join( self.shotsRoot, str( buttonText ) ) )
        
        
        #self.shotsGroupBox.setTitle( '%s/shots/%s' %( currentProject, buttonText ) )
        #self.assetsGroupBox.setTitle( '%s/shots/%s' %( currentProject, buttonText ) )
        
        #self.currentContent = '%s/content/shots/%s' %( currentProject, buttonText )
        
        self.shotsGroupBox.setTitle( 'looking at ' + currentProject + os.sep + 'shots' + os.sep + buttonText )
        self.assetsGroupBox.setTitle( 'looking at ' + currentProject + os.sep + 'shots' + os.sep + buttonText )
        
        self.currentContent = currentProject + os.sep + 'content' + os.sep + 'shots' + os.sep + buttonText
        
        
#         try:
        for nodeItem in shotContent:
            if nodeItem in self.exclusions:
                pass
            else:
                self.propertyNodePathShots = os.path.join( self.shotsRoot, str( buttonText ), nodeItem, 'propertyNode.xml' )
                #self.propertyNode = ET.parse( propertyNodePath )

                
                newNode = node( self, self.scene, self.propertyNodePathShots )
                newNode.addText( self.scene, nodeItem )
                self.scene.addToNodeList( newNode )
                
        self.computeConnections()

#         except:
#             print 'shot contains no tasks'
            
        
    def getCurrentProject( self ):
        currentProject = str( self.projectComboBox.currentText() )
        self.assetsRoot = os.path.join( self.projectsRoot, currentProject )
        #print currentProject
        return currentProject
        
            
    
    def getAssetContent( self, assetButton ):
        
        self.nodeView.setVisible( True )
        
        buttonText = assetButton.text()
        
        
        
        self.scene.clear()
        self.addRectangular()
        self.scene.clearNodeList()
        currentProject = str( self.projectComboBox.currentText() )
        self.assetsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'assets' )
        assetContent = os.listdir( os.path.join( str( self.assetsRoot ), str( buttonText ) ) )
        
        #self.assetsGroupBox.setTitle( '%s/assets/%s' %( currentProject, buttonText ) )
        #self.shotsGroupBox.setTitle( '%s/assets/%s' %( currentProject, buttonText ) )
        
        #self.currentContent = '%s/content/assets/%s' %( currentProject, buttonText )
        
        self.shotsGroupBox.setTitle( 'looking at ' + currentProject + os.sep + 'assets' + os.sep + buttonText )
        self.assetsGroupBox.setTitle( 'looking at ' + currentProject + os.sep + 'assets' + os.sep + buttonText )
        
        self.currentContent = currentProject + os.sep + 'content' + os.sep + 'assets' + os.sep + buttonText
        
        #try:
        #positionX = 0
        #positionY = 0
        

        for nodeItem in assetContent:
            if nodeItem in self.exclusions:
                pass
            else:
                self.propertyNodePathAssets = os.path.join( self.assetsRoot, str( buttonText ), nodeItem, 'propertyNode.xml' )
                print 'im here'
                print self.propertyNodePathAssets
                #print propertyNodePath
                
                newNode = node( self, self.scene, self.propertyNodePathAssets )
                newNode.addText( self.scene, nodeItem )
                self.scene.addToNodeList( newNode )
                
        self.computeConnections()
                        
                    
                    
                    
                    
                    
                    #posX = positionX + 100
                    #posY = positionY + 100
#         except:
#             print 'asset contains no tasks'


    def addContent( self ):
        
        assets = []
        shots = []
        
        currentProject = str( self.projectComboBox.currentText() )
        self.assetsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'assets' )
        self.shotsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'shots' )
        try:
            #print os.listdir( self.assetsRoot )
            for i in os.listdir( self.assetsRoot ):
                if not i in self.exclusions:
                    assets.append( i )
                else:
                    pass
                    
                
        except:
            print 'no assetsRoot found'
        try:
            for i in os.listdir( self.shotsRoot ):
                #print i
                if not i in self.exclusions:
                    shots.append( i )
                else:
                    pass
        except:
            print 'no shotsRoot found'  
    
    
        #Assets
        
        #print shots
        #print assets

        self.assetsGroupBox = QGroupBox( currentProject )
        layoutAssets = QHBoxLayout()
        self.createAssetPushButton = QPushButton( 'create new asset' )
        self.createAssetPushButton.clicked.connect( self.createNewContent )
        layoutAssets.addWidget( self.createAssetPushButton )
        
        self.assetButtonGroup = QButtonGroup()
        self.assetButtonGroup.buttonClicked[ QAbstractButton ].connect( self.getAssetContent )
        
        for i in assets:
            assetPushButton = QPushButton( i )
            assetPushButton.setContextMenuPolicy( Qt.CustomContextMenu )
            self.connect( assetPushButton, SIGNAL( 'customContextMenuRequested( const QPoint& )' ), self.contentContextMenu )
            #print os.path.join( self.assetsRoot, i ) 
            #assetPushButton.clicked.connect( lambda: self.scene.clear() )
            layoutAssets.addWidget( assetPushButton )
            self.assetButtonGroup.addButton( assetPushButton )
            
        layoutAssets.addItem( QSpacerItem( 1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum ) )
        
        
        
        
        self.assetsGroupBox.setLayout( layoutAssets )
        scrollAssets = QScrollArea()
        scrollAssets.setWidget( self.assetsGroupBox )
        scrollAssets.setWidgetResizable( True )
        scrollAssets.setFixedHeight( 90 )
        layoutAssetsScroll = QVBoxLayout()
        layoutAssetsScroll.addWidget( scrollAssets )
        
        widgetAssets = QWidget()
        widgetAssets.setLayout( layoutAssetsScroll )
        
        
        
        #Shots
        #self.contentShotUi = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'contentShot.ui' ), self )
        
        self.shotsGroupBox = QGroupBox( currentProject )
        layoutShots = QHBoxLayout()
        
        self.createShotPushButton = QPushButton( 'create new shot' )
        self.createShotPushButton.clicked.connect( self.createNewContent )
        layoutShots.addWidget( self.createShotPushButton )
        
        self.shotButtonGroup = QButtonGroup()
        self.shotButtonGroup.buttonClicked[ QAbstractButton ].connect( self.getShotContent )
        
        for i in shots:
            #shotContent = self.getShotContent( i )
            #print shotContent
            shotPushButton = QPushButton( i )
            shotPushButton.setContextMenuPolicy( Qt.CustomContextMenu )
            self.connect( shotPushButton, SIGNAL( 'customContextMenuRequested( const QPoint& )' ), self.contentContextMenu )
            #print i
            #print 'getShotContent = %s' %self.getShotContent( i )
            #shotLocation = os.path.join( self.shotsRoot, i )
            #print shotLocation
            #print os.path.join( self.shotsRoot, i )
            #shotPushButton.clicked.connect( self.listContent( i ) )
            #shotPushButton.clicked.connect( lambda: self.scene.clear() )
            layoutShots.addWidget( shotPushButton )
            self.shotButtonGroup.addButton( shotPushButton )
        
        layoutShots.addItem( QSpacerItem( 1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum ) )
        
        
        
        
        self.shotsGroupBox.setLayout( layoutShots )
        scrollShots = QScrollArea()
        scrollShots.setWidget( self.shotsGroupBox )
        scrollShots.setWidgetResizable( True )
        scrollShots.setFixedHeight( 90 )
        layoutShotsScroll = QVBoxLayout()
        layoutShotsScroll.addWidget( scrollShots )
        
        widgetShots = QWidget()
        widgetShots.setLayout( layoutShotsScroll )
        
        
        #test
        testGroupBox = QGroupBox()
        layoutTest = QHBoxLayout()
        
        self.testButtonGroup = QButtonGroup()
        self.testButtonGroup.buttonClicked[QAbstractButton].connect( self.printShit )
        #testButtonGroup.buttonClicked[QAbstractButton].connect( self.printShit )
        
        for i in range( 30 ):
            createTestPushButton = QPushButton( '%d' %i )
            #createTestPushButton.clicked.connect( lambda: self.printShit( i ) )
            layoutTest.addWidget( createTestPushButton )
            self.testButtonGroup.addButton( createTestPushButton )
            
        
        layoutTest.addItem( QSpacerItem( 1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum ) )
        
        
        testGroupBox.setLayout( layoutTest )
        scrollTest = QScrollArea()
        scrollTest.setWidget( testGroupBox ) 
        scrollTest.setWidgetResizable( True )
        layoutTestScroll = QVBoxLayout()
        layoutTestScroll.addWidget( scrollTest )
        
        widgetTest = QWidget()
        widgetTest.setLayout( layoutTestScroll )
        
        
        
        self.assetsShotsTabWidget.clear()
        
        self.assetsShotsTabWidget.addTab( widgetAssets, 'assets' )
        self.assetsShotsTabWidget.addTab( widgetShots, 'shots' )
#         self.assetsShotsTabWidget.insertTab( 0, widgetAssets, 'assets' )
#         self.assetsShotsTabWidget.insertTab( 1, widgetShots, 'shots' )
        #self.assetsShotsTabWidget.addTab( widgetTest, 'test' )
        
        #self.assetsTab.addWidget( QPushButton )

    def contentContextMenu( self, point ):
        
        sendingButton = self.sender()
        sendingButtonText = sendingButton.text()
        
        #currentProject = str( self.projectComboBox.currentText() )
        tabIndex = self.assetsShotsTabWidget.currentIndex()
        
        if tabIndex == 0:
            currentTarget = self.assetsRoot
            
        elif tabIndex == 1:
            currentTarget = self.shotsRoot
            
        contentLocation = os.path.join( str( currentTarget ), str( sendingButtonText ) )
        #print contentLocation
        
        
        #print point
        #print sending_button.pos
        popMenu = QMenu( self )
        popMenu.addAction( 'open directory', lambda: self.locateContent( contentLocation ) )
        popMenu.addAction( 'clone', lambda: self.cloneContent( contentLocation ) )
        popMenu.addAction( 'disable', self.foo )
        popMenu.addSeparator()
        #popMenu.addAction( 'delete', self.removeContent( contentLocation, sendingButton ) )
        popMenu.addAction( 'delete', lambda: self.removeContent( contentLocation ) )
        
        #popMenu.exec_( sending_button.pos )
        popMenu.exec_( sendingButton.mapToGlobal( point ) )  
        #popMenu.exec_( self.mapToGlobal( point ) ) 
        

    def foo( self ):
        pass
    
    
    def printShit( self, button ):
        print button.text()
        #return value
    
    
    def addProjects( self ):
        self.projectComboBox.clear()
        
        self.projectComboBox.addItem( 'select project' )
        self.projectComboBox.insertSeparator( 1 )
        try:
            for i in os.listdir( self.projectsRoot ):
                if os.path.isdir( os.path.join( self.projectsRoot, i ) ):
                    self.projectComboBox.addItem( i )
        except:
            pass
        
        
        self.projectComboBox.activated.connect( self.refreshProjects )
        
        
    def refreshProjects( self ):
        
        self.nodeView.setVisible( False )
        
        indexText = self.projectComboBox.currentText()
        
        index = self.projectComboBox.findText( indexText )
        
        self.projectComboBox.setCurrentIndex( index )
        
        if not indexText == 'select project' and not indexText == 'create new project':
            self.assetsShotsTabWidget.clear()
            self.addContent()
            self.assetsShotsTabWidget.setVisible( True )
            #self.nodeView.setVisible( True )
            self.openPushButton.setEnabled( True )

            
            
        else:
            self.assetsShotsTabWidget.setVisible( False )
            self.nodeView.setVisible( False )
            self.assetsShotsTabWidget.clear()
            print 'no project selected'
            self.openPushButton.setEnabled( False )
            
        
        
        
        self.scene.clear()
        
        
    def addTools( self ):
        
        self.toolsComboBox.clear()
        self.toolsComboBox.addItem( 'run tool instance' )
        
        self.toolsComboBox.insertSeparator( 1 )
        
        for i in self._tools:
            
            item = self.toolsComboBox.addItem( i[ 0 ] )
            #item.setFlags( Qt.ItemIsSelectable( False ) )
            
        
        #self.toolsComboBox.activated.connect( self.runTool )



    '''  
    def runTask( self, executable, newestFile, asset, label, project, *args ):

        #self.processNode = node
        #self.processLabel = self.processNode.getLabel()

        #print args[ 0 ]
        #print type( args[ 0 ] )  

        command = [ executable, newestFile, ' '.join( args[ 0 ] ) ]

        newProcess = QProcess( self )

        self.qprocesses.append( newProcess )
        
        newProcess.readyRead.connect( self.dataReady )
        #self.mainWindow.sendTextToBox( "%s: starting %s. Enjoy!\n" %( datetime.datetime.now(), self.data( 0 ).toPyObject() ) )
        
        #newProcess.started.connect( self.onStarted( newProcess, asset, label, project ) )
        #newProcess.finished.connect( self.onFinished( newProcess, asset, label, project ) )
        
        newProcess.started.connect( lambda: self.onStarted( newProcess.pid(), asset, label, project ) )
        newProcess.finished.connect( lambda: self.onFinished( newProcess.pid(), asset, label, project ) )
        

        newProcess.start( ' '.join( command ) )
        #newProcess.pid = newProcess.pid()
        #print self.process
        #print self.process.state()

        #while self.process.state() == '1':
        #      print 'active'

    def onStarted( self, pid, asset, label, project ):
        #print '%s started' %self.label
        #self.
        #asset = os.path.basename( self.asset )
        #print asset

        #self.sendTextToBox( "%s: starting %s (PID %s). Enjoy!\n" %( datetime.datetime.now(), self.data( 0 ).toPyObject(), self.pid ) )
        self.sendTextToBox( "%s: starting PID %s. Enjoy!\n" %( datetime.datetime.now(), pid ) )
        #print os.path.basename( asset )
        #print label
        #print project
        
        self.screenCast = screenCast( os.path.basename( asset ), label, project )
        self.screenCast.startCast()

        self.timeTracker = timeTracker( os.path.basename( asset ), label, project )
        self.timeTracker.trackStart()




    def onFinished( self, pid, asset, label, project ):
        #print '%s finished' %self.label

        #pid = self.process.pid()

        self.sendTextToBox( "%s: stopped PID %s).\n" %( datetime.datetime.now(), pid ) )

        #print self.screenCast

        self.screenCast.stopCast()

        self.timeTracker.trackStop()
    '''

    def runTool( self ):
        # QProcess object for external app
        #self.process = QProcess( self )
        # QProcess emits `readyRead` when there is data to be read
        #self.process.readyRead.connect( self.dataReady )
        index = self.toolsComboBox.currentIndex() - 2
        #print index
        if index < 0:
            self.sendTextToBox( "%s: nothing to run\n" %datetime.datetime.now() )
            #print "nothing to run"
        else:
            #print self._tools[ index ][ 1 ][ 0 ]
            path = re.findall( r'"([^"]*)"', self._tools[ index ][ 1 ][ 0 ] )[ 0 ]
            #print path
            #print
            if os.path.exists( os.path.normpath( path ) ):
                self.sendTextToBox( "%s: starting %s. Enjoy!\n" %( datetime.datetime.now(), self._tools[ index ][ 0 ] ) )
                #self.process.start( self._tools[ index ][ 1 ][ 0 ] )
                #newToolProc = QProcess( self ).start( ' '.join( [ '/opt/X11/bin/xterm', '-e', self._tools[ index ][ 1 ][ 0 ] ] ) )
                #print str( ' '.join( [ '/opt/X11/bin/xterm', '-e', 'touch /Users/michaelmussato/hello', '&&', self._tools[ index ][ 1 ][ 0 ], '&&', 'touch /Users/michaelmussato/bye' ] ) )
                #newToolProc = QProcess( self )
                
                #newToolProc.start( str( ' '.join( [ '/opt/X11/bin/xterm', '-e', 'touch /Users/michaelmussato/hello', '&&', '/opt/X11/bin/xterm', '-e', self._tools[ index ][ 1 ][ 0 ], '&&', 'touch /Users/michaelmussato/bye' ] ) ) )
                #newToolProc.start( str( ' '.join( [ '/opt/X11/bin/xterm', '-e', '/opt/X11/bin/xterm', '-e', self._tools[ index ][ 1 ][ 0 ] ] ) ) )
                #print str( ' '.join( [ '/opt/X11/bin/xterm', '-e', 'touch /Users/michaelmussato/hello', '&&', '/opt/X11/bin/xterm', '-e', self._tools[ index ][ 1 ][ 0 ], '&&', '/opt/X11/bin/xterm', '-e', 'touch /Users/michaelmussato/bye' ] ) )
                #newToolProc.start( str( ' '.join( [ '/opt/X11/bin/xterm', '-e', 'touch /Users/michaelmussato/hello', '&&', '/opt/X11/bin/xterm', '-e', self._tools[ index ][ 1 ][ 0 ], '&&', '/opt/X11/bin/xterm', '-e', 'touch /Users/michaelmussato/bye' ] ) ) )
                
                #os.system( str( ' '.join( [ '/opt/X11/bin/xterm', '-e', 'touch /Users/michaelmussato/hello', '&&', '/opt/X11/bin/xterm', '-e', self._tools[ index ][ 1 ][ 0 ], '&&', '/opt/X11/bin/xterm', '-e', 'touch /Users/michaelmussato/bye' ] ) ) )
                
                #self.process.start( ' '.join( [ '/bin/bash', '-c', self._tools[ index ][ 1 ][ 0 ] ] ) )
                #newToolProc.start( '/bin/bash', [ '-c', '/opt/X11/bin/xterm' , '-e', 'touch', '/Users/michaelmussato/hello', '&&', 'sleep', '5', '&&', 'touch', '/Users/michaelmussato/bye' ] )
                #print self._tools[ index ][ 1 ][ 0 ]
                command = str( self._tools[ index ][ 1 ][ 0 ] )[:-1]
                
                #print command
                #command = re.sub( r'^"|"$', '', command )
                #print command

                #commandList = 


                #proc = subprocess.Popen( [ '/opt/X11/bin/xterm', '-e' ], stdin=subprocess.PIPE, stdout=subprocess.PIPE )
                
                #out, err = proc.communicate
                
                newToolProc = subprocess.Popen( str( ' '.join( [ '/opt/X11/bin/xterm', '-e', self._tools[ index ][ 1 ][ 0 ] ] ) ), shell=True )
                #self.sendTextToBox( newToolProc.communicate()[ 0 ] )

                #newToolProc.start( str( ' '.join( [ '/usr/bin/touch', '/Users/michaelmussato/hello', '&&', command, '&&', '/usr/bin/touch', '/Users/michaelmussato/bye' ] ) ) )
                #newToolProc.readyRead.connect( self.dataReady )
                
                
                #subprocess.Popen( [ '/opt/X11/bin/xterm', '-e', 'touch', '/Users/michaelmussato/hello mike', '&&', '/opt/X11/bin/xterm', '-e', command, '&&', '/opt/X11/bin/xterm', '-e', 'touch', '/Users/michaelmussato/bye' ], shell=False )
                #subprocess.Popen( [ 'touch', '/Users/michaelmussato/hellomike', '&&', command ], shell=True )
                #subprocess.check_call( [ command ], shell=True )
                #print ' '.join( [ 'xterm', '-e', self._tools[ index ][ 1 ][ 0 ] ] )

                #os.system( ' '.join( [ '/opt/X11/bin/xterm', '-e', self._tools[ index ][ 1 ][ 0 ] ] ) )
                
                #s.system( '/opt/X11/bin/xterm -e "/Applications/MAXON/CINEMA 4D R15/CINEMA 4D.app/Contents/MacOS/CINEMA 4D" ' )
                #os.system( str( ' '.join( [ 'xterm', '-e', self._tools[ index ][ 1 ][ 0 ] ] ) ) )
            else:
                self.sendTextToBox( "%s: cannot start %s. is it installed?\n" %( datetime.datetime.now(), self._tools[index][0] ) )

        
        self.toolsComboBox.setCurrentIndex( 0 )
        
#     def updateNodeMenu( self ):
#         self.nodeMenuArea.setWidget( item.getWidgetMenu() )
    
    def sendTextToBox( self, text ):
        cursorBox = self.statusBox.textCursor()
        cursorBox.movePosition(cursorBox.End)
        cursorBox.insertText( str( text ) )
        self.statusBox.ensureCursorVisible()
    
    def dataReadyStd( self, process ):
        #color = QColor( 0, 255, 0 )
        box = self.statusBox
        #box.setTextColor( color )
        cursorBox = box.textCursor()
        cursorBox.movePosition( cursorBox.End )
        cursorBox.insertText( "%s (std):   %s" %( datetime.datetime.now(), str( process.readAllStandardOutput() ) ) )

        self.statusBox.ensureCursorVisible()

    def dataReadyErr( self, process ):
        #color = QColor( 255, 0, 0 )
        box = self.statusBox
        #box.setTextColor( color )
        cursorBox = box.textCursor()
        cursorBox.movePosition( cursorBox.End )
        cursorBox.insertText( "%s (err):   %s" %( datetime.datetime.now(), str( process.readAllStandardError() ) ) )

        self.statusBox.ensureCursorVisible()

    def toggleContentBrowser( self ):
        if self.assetsShotsTabWidget.isVisible() == True:
            self.assetsShotsTabWidget.setVisible( False )
        else:
            self.assetsShotsTabWidget.setVisible( True )
     
    def toggleConsole( self ):
        if self.statusBox.isVisible() == True:
            self.statusBox.setVisible( False )
        else:
            self.statusBox.setVisible( True )
    
    def toggleNodeName( self ):
        if self.nodeOptionsWindow.isVisible() == True:
            self.nodeOptionsWindow.setVisible( False )
        else:
            self.nodeOptionsWindow.setVisible( True )
         
    def toggleDescription( self ):
        if self.descriptionWindow.isVisible() == True:
            self.descriptionWindow.setVisible( False )
        else:
            self.descriptionWindow.setVisible( True )
    
    def toggleNodesWindow( self ):
        if self.nodesWindow.isVisible() == True:
            self.nodesWindow.setVisible( False )
        else:
            self.nodesWindow.setVisible( True )


        

    



    def graphicsView_wheelEvent( self, event ):
        
#         numSteps = event.delta() / 15 / 8
#         
#         if numSteps == 0:
#             event.ignore()
#             
#         sc = 1.25 * numSteps
#         self.zoom( sc, self.mapToScene( event.pos() ) )
#         event.accept()
        
        
         
        factor = 1.15
          
        #self.nodeView.centerOn()
          
        #print 'event.delta() = %s' %event.delta()
          
        if event.delta() > 0:
            self.nodeView.scale( factor, factor )
            self.nodeView.centerOn( event.pos() )
              
        else:
            self.nodeView.scale( 1.0 / factor, 1.0 / factor )
            self.nodeView.centerOn( event.pos() )
        #print 'scaling factor = %f' %self.nodeView.transform().m11()
        
        
#     def zoom( self, factor, centerPoint ):
#         scale( factor, factor )
#         centerOn( centerPoint )

    def graphicsView_resizeEvent( self, event ):

        pass
    
    
    
    def setNodeMenuWidget( self ):
        print "duude"
        #self.nodeMenuArea.takeWidget()
        #self.nodeMenuArea.setWidget(item.getWidgetMenu())
        #self.nodeOptionsWindow.setTitle(item.displayText.toPlainText())
    
        


if __name__ == "__main__":
    
    print "starting PyPELyNE"
    app = QApplication( sys.argv )
    #app.aboutToQuit.connect(deleteGLWidget)
    screenSize = QApplication.desktop().availableGeometry()
    print 'screen resolution is %ix%i' %( int( screenSize.width() ), int( screenSize.height() ) )
    pypelyneWindow = pypelyneMainWindow()
    #screenSize = QApplication.desktop().availableGeometry()
    pypelyneWindow.resize( int( screenSize.width() ), int( screenSize.height() ) )
    pypelyneWindow.show()
    app.exec_()
    


