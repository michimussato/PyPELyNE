import os, sip, sys, subprocess, platform, re, shutil, random, datetime, getpass, threading
from operator import *

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import *
from PyQt4.QtOpenGL import *
from random import *

from src.pypelyneConfigurationWindow import *
from src.bezierLine import *
from src.graphicsScene import *
from src.screenCast import *
from src.timeTracker import *
from src.listScreenCasts import *

import xml.etree.ElementTree as ET

try:
    from src.vlc import *
except:
    raise ImportError( 'failed to import vlc' )





app = None
        
        
class nodeWidgetUi( QWidget ):
    def __init__( self, mainWindow, parent = None ):
        super( nodeWidgetUi, self ).__init__( parent )
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.currentPlatform = self.mainWindow.getCurrentPlatform()

        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'nodeWidget.ui' ), self )



class playerWidgetUi( QWidget ):
    def __init__( self, mainWindow, parent = None ):
        super( playerWidgetUi, self ).__init__( parent )
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.currentPlatform = self.mainWindow.getCurrentPlatform()

        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'player.ui' ), self )


        #self.connect( self.pushButtonPlayStop, SIGNAL( 'customContextMenuRequested( const QPoint& )' ), self.playerContextMenu )
        #self.contextMenu =QMenu()
        #self.contextMenu.addSeparator()

    #def playerContextMenu( self, point ):
        #sendingButton = self.sender()
        #self.contextMenu.exec_( sendingButton.mapToGlobal( point ) )




class pypelyneMainWindow( QMainWindow ):
    def __init__( self, parent = None ):
        super( pypelyneMainWindow, self ).__init__( parent )
        
        self.exclusions = [ '.DS_Store', 'Thumbs.db', '.com.apple.timemachine.supported', 'desktop.ini' ]

        self.imageExtensions = [ '.jpg', '.exr', '.tga', '.png' ]
        self.movieExtensions = [ '.mov', '.avi' ]
        
        self.currentPlatform = platform.system()

        self.pypelyneRoot = os.getcwd()

        self.user = getpass.getuser()

        if self.currentPlatform == "Windows":
            if os.path.exists( os.path.join( r'\\192.168.0.12\pypelyne_projects' ) ):
                self.projectsRoot = os.path.join( r'\\192.168.0.12\pypelyne_projects' )
            else:
                self.projectsRoot = r'C:\pypelyne_projects'
            self.audioFolder = r'C:\audio'
            self.screenCastExec = r''
            self.sequenceExec = os.path.join( self.pypelyneRoot, r'payload/vlc/win64/vlc.exe' )
        elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
            if os.path.exists( os.path.join( r'/Volumes/pili/pypelyne_projects' ) ):
                self.projectsRoot = os.path.join( r'/Volumes/pili/pypelyne_projects' )
            else:
                self.projectsRoot = os.path.join( r'/Volumes/osx_production/pypelyne_projects' )
            self.audioFolder = r'/Volumes/pili/library/audio'
            self.screenCastExec = os.path.join( self.pypelyneRoot, r'payload/vlc/darwin/VLC' )
            self.sequenceExec = r'/Applications/RV64.app/Contents/MacOS/RV'

        self.nodeWidgets = []
        self.qprocesses = []
        self.openNodes = []
        self.timeTrackers = []
        self.screenCasts = []
        self.screenCastsWindowOpen = None

        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'pypelyneMainWindow.ui' ), self )
        self.valueApplicationsXML = os.path.join( self.pypelyneRoot, 'conf', 'valueApplications.xml' )
        
        self.nodeView.setVisible( False )
        self.assetsShotsTabWidget.setVisible( False )
        self.statusBox.setVisible( False )
        self.nodeOptionsWindow.setVisible( False )
        self.descriptionWindow.setVisible( False )
        self.openPushButton.setVisible( True )
        self.checkBoxDescription.setVisible( False )
        self.configPushButton.setVisible( False )

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
        
        # Tools
        self.addTools()

        if os.path.exists( self.audioFolder ):
            self.audioFolderContent = os.listdir( self.audioFolder )


            for exclusion in self.exclusions:
                try:
                    self.audioFolderContent.remove( exclusion )
                    print 'exclusion %s removed from audioFolderContent' %( exclusion )
                except:
                    pass

            self.addPlayer()

            if len( os.listdir( self.audioFolder ) ) == 0:
                #print 'no audio files found'
                self.playerUi.pushButtonPlayStop.setEnabled( False )

                #self.playerUi.radioButtonStop.setEnabled( False )
                #self.playerUi.buttonSkip.setEnabled( False )
        
        
        self.runToolPushButton.clicked.connect( self.runTool )
        
        self.checkBoxConsole.stateChanged.connect( self.toggleConsole )
        self.checkBoxNodeName.stateChanged.connect( self.toggleNodeName )
        self.checkBoxDescription.stateChanged.connect( self.toggleDescription )
        self.checkBoxContentBrowser.stateChanged.connect( self.toggleContentBrowser )
        #self.checkBoxNodesWindow.stateChanged.connect( self.toggleNodesWindow )
        #self.scene.nodeClicked.connect( self.setWidgetMenu )
        
        # configuration window
        self.configPushButton.clicked.connect( self.configurationWindow )
        self.screenCastsPushButton.clicked.connect( self.screenCastsWindow )
        self.scene.nodeSelect.connect( self.setNodeWidget )
        self.scene.nodeDeselect.connect( self.clearNodeWidget )
        self.openPushButton.clicked.connect( lambda: self.locateContent( os.path.join( self.projectsRoot, str( self.projectComboBox.currentText() ) ) ) )

        self.clipBoard = QApplication.clipboard()
        
        #self.scene = SceneView()
        self.scene.textMessage.connect( self.sendTextToBox )
        #self.scene.nodeClicked.connect( self.setNodeMenuWidget )
        #self.scene.nodeMenu.connect( self.setWidgetMenu )
        
        #self.scene.nodeMenuArea.connect( self.updateNodeMenu )


    def screenCastsWindow( self ):

        if self.screenCastsWindowOpen == None:
            self.screenCastsUI = listScreenCastsUI( self, self )
            self.screenCastsUI.show()
            self.screenCastsWindowOpen = self.screenCastsUI
            self.screenCastsUI.listScreenCastsUIClosed.connect( self.resetScreenCastsWindowOpen )

        else:
            self.screenCastsUI.activateWindow()
            self.screenCastsUI.raise_()
        print 'hallo'

    def resetScreenCastsWindowOpen( self ):
        #print 'emitted'
        self.screenCastsWindowOpen = None

    def getUser( self ):
        return self.user

    def closeEvent( self, event ):

        if len( self.timeTrackers ) > 0 or len( self.screenCasts ) > 0 or len( self.qprocesses ) > 0:

            if len( self.qprocesses ) > 0:
                qprocesses = []
                for qprocess in self.qprocesses:
                    qprocesses.append( qprocess.pid() )

            pids = ', '.join( [ str( qprocess )[ :-1 ] for qprocess in qprocesses ] )

            quit_msg = "Too early to leave. There is still something running...\n\nPID(s): %s" %( pids )

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
        #self.playerUi.radioButtonPlay.clicked.connect( self.playAudio )
        self.playerUi.pushButtonPlayStop.clicked.connect( self.playAudio )

        self.playerUi.pushButtonPlayStop.setContextMenuPolicy( Qt.CustomContextMenu )
        self.connect( self.playerUi.pushButtonPlayStop, SIGNAL( 'customContextMenuRequested( const QPoint& )' ), self.playerContextMenu )

        self.playerContextMenu = QMenu()
        #self.audioFolderContent = os.listdir( self.audioFolder )

        #if any( self.exclusions for track in self.audioFolderContent ):
        #    print 'exclusion found'

        for track in self.audioFolderContent:
            self.playerContextMenu.addAction( track, self.playAudioCallback( track ) )
        self.playerContextMenu.addSeparator()



        #self.playerUi.radioButtonStop.clicked.connect( self.stopAudio )
        #self.playerUi.buttonSkip.clicked.connect( self.skipAudio )

        self.playerUi.pushButtonPlayStop.setText( 'play' )
        self.playerExists = False

    def playerContextMenu( self, point ):
        self.playerContextMenu.exec_( self.playerUi.pushButtonPlayStop.mapToGlobal( point ) )

    def cb( self, event ):
        print 'cb:', event.type, event.u

    def playAudioCallback( self, track = None ):
        def callback():
            self.playAudio( track )
        return callback

    def playAudio( self, track = None ):
        print track

        # https://forum.videolan.org/viewtopic.php?t=107039

        if len( os.listdir( self.audioFolder ) ) == 0:
            print 'no audio files found'
            self.playerUi.radioButtonPlay.setEnabled( False )

        elif self.playerExists == False:
            random.shuffle( self.audioFolderContent, random.random )

            if not track == False:
                trackID = self.audioFolderContent.index( track )

            print 'playing'

            self.mlp = MediaListPlayer()
            self.mp = MediaPlayer()
            self.mlp.set_media_player( self.mp )


            self.ml = MediaList()

            for track in self.audioFolderContent:
                self.ml.add_media( os.path.join( self.audioFolder, track ) )

            self.mlp.set_media_list( self.ml )

            if not track == False:
                self.mlp.play_item_at_index( trackID )

            else:
                self.mlp.play()


            #self.playerUi.pushButtonPlayStop.setText( 'skip' )

            self.playerExists = True

            self.playerUi.pushButtonPlayStop.clicked.disconnect( self.playAudio )
            self.playerUi.pushButtonPlayStop.clicked.connect( self.stopAudio )
            self.playerUi.pushButtonPlayStop.setText( 'stop' )
            #self.playerUi.pushButtonPlayStop.clicked.disconnect( self.playAudio )
            #self.playerUi.pushButtonPlayStop.clicked.connect( self.skipAudio )
            print 'timer start'
            threading.Timer( 0.5, self.fromStopToSkip ).start()


        elif self.playerExists == True and not track == False:

            print 'playing %s' %( track )

            #random.shuffle( self.audioFolderContent, random.random )
            trackID = self.audioFolderContent.index( track )


            #self.audioFolderContent.remove( track )
            #self.audioFolderContent.insert( 0, track )
            self.skipAudio( trackID )




        else:
            print 'already on air'



    def fromStopToSkip( self ):
        if self.playerExists == True:
            self.playerUi.pushButtonPlayStop.clicked.disconnect( self.stopAudio )
            self.playerUi.pushButtonPlayStop.clicked.connect( self.skipAudio )
            self.playerUi.pushButtonPlayStop.setText( 'skip' )


    def fromSkipToStop( self ):
        if self.playerExists == True:
            self.playerUi.pushButtonPlayStop.clicked.disconnect( self.skipAudio )
            self.playerUi.pushButtonPlayStop.clicked.connect( self.stopAudio )
            self.playerUi.pushButtonPlayStop.setText( 'stop' )





    def stopAudio( self ):
        if self.playerExists == True:
            try:
                self.playerUi.pushButtonPlayStop.clicked.disconnect( self.stopAudio )
                self.playerUi.pushButtonPlayStop.clicked.connect( self.playAudio )
                self.mp.stop()
                self.mp.release()
                self.mlp.release()
                self.playerExists = False
                self.playerUi.pushButtonPlayStop.setText( 'play' )
                print 'stopped'
            except:
                print 'error or not playing'



    def skipAudio( self, trackID = None ):
        if self.playerExists == True:
            if not trackID == False:
                self.mlp.play_item_at_index( trackID )

            else:
                self.mlp.next()

            self.playerUi.pushButtonPlayStop.clicked.disconnect( self.skipAudio )
            self.playerUi.pushButtonPlayStop.clicked.connect( self.stopAudio )
            self.playerUi.pushButtonPlayStop.setText( 'stop' )
            threading.Timer( 0.5, self.fromStopToSkip ).start()
            #threading.Timer( 1, self.fromStopToSkipChangeUi ).start()






        
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

    def newProcessColor( self ):
        pColorR = random.randint( 20, 235 )
        pColorG = random.randint( 20, 235 )
        pColorB = random.randint( 20, 235 )

        pColor = ( QColor( pColorR, pColorG, pColorB ) )

        return pColor

    def runTask( self, node, executable, newestFile, *args ):

        #print executable

        makingOfDir = os.path.join( self.getCurrentProject(), 'making_of' )

        #now = str( datetime.datetime.now().strftime( '%Y-%m-%d_%H%M-%S' ) )
        now = datetime.datetime.now()

        nowSecs = str( now.strftime( '%Y-%m-%d_%H%M-%S' ) )
        nowMilliSecs = str( now.strftime( '%Y-%m-%d_%H%M-%S_%f' ) )

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
        #print executable, arguments



        newScreenCast = screenCast( self, os.path.basename( node.getNodeAsset() ), node.getLabel(), node.getNodeProject() )
        newTimeTracker = timeTracker( os.path.basename( node.getNodeAsset() ), node.getLabel(), node.getNodeProject() )


        process = QProcess( self )

        pColor = self.newProcessColor()

        #process.readyRead.connect( lambda: self.dataReady( process ) )
        process.readyReadStandardOutput.connect( lambda: self.dataReadyStd( process, pColor ) )
        process.readyReadStandardError.connect( lambda: self.dataReadyErr( process, pColor ) )
        process.started.connect( lambda: self.taskOnStarted( node, process, newScreenCast, newTimeTracker ) )
        #process.started.connect( lambda:  )
        process.finished.connect( lambda: self.taskOnFinished( node, process, newScreenCast, newTimeTracker ) )
        currentDir = os.getcwd()
        os.chdir( node.getNodeRootDir() )
        print node.getNodeRootDir()
        process.start( executable, arguments )
        os.chdir( currentDir )
        #print os.getcwd()

    def taskOnStarted( self, node, qprocess, screenCast, timeTracker ):

        self.qprocesses.append( qprocess )
        self.openNodes.append( node )
        #print self.qprocesses

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


    def taskOnFinished( self, node, qprocess, screenCast, timeTracker ):
        print '%s finished' %node.getLabel()
        #
        # #pid = self.process.pid()
        #
        # #self.mainWindow.sendTextToBox( "%s: stopped %s (PID %s).\n" %( datetime.datetime.now(), self.data( 0 ).toPyObject(), self.pid ) )
        #
        # #print self.screenCast
        #
        if screenCast in self.screenCasts:
            screenCast.stop()
            self.screenCasts.remove( screenCast )
        #
        timeTracker.stop()
        self.timeTrackers.remove( timeTracker )
        #
        os.remove( os.path.join( node.getNodeRootDir(), 'locked' ) )

        self.openNodes.remove( node )
        self.qprocesses.remove( qprocess )
        #print self.qprocesses




    def computeValueApplications( self ):

        self.sendTextToBox( 'registering applications for current platform (%s) found at %s:\n' %( self.currentPlatform, self.valueApplicationsXML ) )

        self.valueApplications = ET.parse( self.valueApplicationsXML )
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

                                familyValue = family.items()[ 1 ][ 1 ]
                                familyAbbreviation = family.items()[ 0 ][ 1 ]
                                vendorValue = vendor.items()[ 0 ][ 1 ]
                                versionValue = version.items()[ 0 ][ 1 ]
                                versionTemplate = version.items()[ 1 ][ 1 ]
                                #print 'versionTemplate = %s' % version.items()[ 1 ][ 1 ]
                                platformValue = platform.items()[ 0 ][ 1 ]
                                executableArch = executable.tag

                                if os.path.exists( os.path.normpath( path ) ):

                                    #self._tools.append( ( vendor.items()[ 0 ][ 1 ] + ' ' + family.items()[ 1 ][ 1 ] + ' ' + version.items()[ 0 ][ 1 ] + ' ' + platform.items()[ 0 ][ 1 ] + ' ' + executable.tag, command, familyAbbreviation ) )
                                    #self._tools.append( ( vendorValue + ' ' + familyValue + ' ' + versionValue + ' ' + platformValue + ' ' + executableArch, command, familyAbbreviation, vendorValue, familyValue, versionValue, executableArch ) )
                                    self._tools.append( ( vendorValue + ' ' + familyValue + ' ' + versionValue + ' ' + executableArch, command, familyAbbreviation, vendorValue, familyValue, versionValue, executableArch, versionTemplate, directoryList, defaultOutputList, flags ) )
                                    self.sendTextToBox( '\t' + vendorValue + ' ' + familyValue + ' ' + versionValue + ' ' + executableArch + ' found.\n' )

                                else:
                                    print 'path not found: %s. application not added to tools dropdown' %( path )
                                    self.sendTextToBox( '\t' + vendorValue + ' ' + familyValue + ' ' + versionValue + ' ' + executableArch + ' not found.\n' )

        self.sendTextToBox( 'initialization done.\n\n' )

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

    def locateContentCallback( self, contentFiles ):
        def callback():
            self.locateContent( contentFiles )
        return callback
    
    
    def locateContent( self, contentFiles ):
        #print contentFiles
        if os.path.exists( contentFiles ):
            if self.currentPlatform == 'Windows':
                subprocess.call( 'explorer.exe %s' %contentFiles, shell=False )
            elif self.currentPlatform == 'Darwin':
                subprocess.Popen( [ '/usr/bin/open', contentFiles ], shell=False )
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


        #for char in list( text ):
        #    if not char in [ r'.', r' ', r',', r'/', r'\\' ]:

        if ok:
            if not os.path.exists( newContent ):
                os.makedirs( newContent, mode=0777 )
                self.addContent()
                self.sendTextToBox( 'content created on filesystem: %s\n' %newContent )
            else:
                self.sendTextToBox( 'content not created because it already exists (%s)\n' %newContent )
                self.sendTextToBox( 'choose different name.\n' %newContent )

        #    else:
        #        self.sendTextToBox( 'invalid characters: %s\n' %text )
            
        
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
        print '\ncomputeConnections...'
        # get all nodes
        nodeList = self.scene.getNodeList()
        # for each node
        for nodeDst in nodeList:
            print '\nnodeDst = %s' %( nodeDst.data( 0 ).toPyObject() )
            # get node inputs
            nodeRootDir = nodeDst.getNodeRootDir()
            nodeInputDir = os.sep.join( [ str( nodeRootDir ), 'input' ] )
            #endItems =
            inputs = os.listdir( nodeInputDir )
            #print inputs
            # for each input

            for input in  inputs:



                if len( inputs ) > 0 and not input in self.exclusions:
                    print '\tprocessing input %s' %( input )
                    # input circle = endItem
                    endItem = nodeDst.inputList[ len( nodeDst.inputs ) ]
                    # find connected node (string[ 2 ])
                    inputString = input.split( '.' )
                    #print inputString
                    inputContent = inputString[ 0 ]
                    inputAsset = inputString[ 1 ]
                    inputNode = inputString[ 2 ]
                    inputOutput = inputString[ 3 ]

                    nodeDstAssetDir = nodeDst.getNodeAsset()
                    #print nodeDst.getNodeAsset()
                    for nodeSrc in nodeList:
                        #print input.getInputDir()
                        #print nodeSrc.getNodeRootDir()
                        nodeSrcRootDir = nodeSrc.getNodeRootDir()
                        nodeSrcRootDirBasename = os.path.basename( nodeSrcRootDir )

                        #print nodeSrcRootDir
                        #print os.path.join( nodeDstAssetDir, inputNode )

                        if inputContent == 'assets':
                            content = 'AST'
                        elif inputContent == 'shots':
                            content = 'SHT'

                        outputItems = nodeSrc.outputList


                        if nodeSrcRootDir == os.path.join( nodeDstAssetDir, inputNode ):
                            print '\t\tnodeSrc is a task'
                            print '\t\tnodeSrc is %s' %( nodeSrc.data( 0 ).toPyObject() )
                            print '\t\tlooking for output called %s' %( inputOutput )
                            for outputItem in outputItems:
                                print '\t\t\tprocessing output %s' %( outputItem.data( 0 ).toPyObject() )
                                if outputItem.data( 0 ).toPyObject() == inputOutput:
                                    print '\t\t\t\t found output %s' %( outputItem.data( 0 ).toPyObject() )
                                    startItem = outputItem
                                    #startItem =
                                    #break
                                #else:
                                #    print '\t\t\t\tnot found'

                        elif nodeSrcRootDir == os.path.join( nodeDstAssetDir, 'LDR_' + content + '__' + inputAsset ):
                            print '\t\tnodeSrc is a loader'
                            print '\t\tnodeSrc is %s' %( nodeSrc.data( 0 ).toPyObject() )
                            print '\t\tlooking for output called %s' %( inputOutput )
                            for outputItem in outputItems:
                                print '\t\t\tprocessing output %s' %( outputItem.data( 0 ).toPyObject().split( '.' )[ 3 ] )
                                #print nodeSrc.data( 0 ).toPyObject()
                                print '\t\tlooking for output called %s' %( inputOutput )
                                searchString = outputItem.data( 0 ).toPyObject().split( '.' )[ 3 ]
                                if searchString == inputOutput:
                                    print '\t\t\t\t found output %s' %( outputItem.data( 0 ).toPyObject().split( '.' )[ 3 ] )
                                    startItem = outputItem
                                    #endItem = nodeDst.inputList[ len( nodeDst.inputs ) ]
                                    #connectionLine = bezierLine( self, self.scene, startItem, endItem )
                                    #break
                                #else:
                                #    print '\t\t\t\tnot found'

                    endItem = nodeDst.inputList[ len( nodeDst.inputs ) ]

                    connectionLine = bezierLine( self, self.scene, startItem, endItem )

                    endItem.parentItem().inputs.append( endItem )
                    endItem.connection.append( connectionLine )
                    endItem.output.append( startItem )
                    endItem.parentItem().incoming.append( startItem )
                    startItem.inputs.append( endItem )

                    startItemRootDir = startItem.parentItem().getNodeRootDir()
                    endItemRootDir = endItem.parentItem().getNodeRootDir()

                    startItemOutputLabel = startItem.getLabel()

                    endItemInputDir = os.path.join( str( endItemRootDir ), 'input', str( input ) )

                    endItem.setInputDir( endItemInputDir )

                    self.scene.addItem( connectionLine )

                    endItem.parentItem().newInput( self.scene )


                elif input in self.exclusions:
                    print 'input data is in exclusions list'

                else:
                    print 'node %s has no input' %( node.data( 0 ).toPyObject() )





        
    def computeConnectionsOld( self ):
        '''
        - get all nodes
        - for each node
            - get node inputs
            - for each input
                - input circle = endItem
                - find connected node (string[ 2 ])
                    - find corresponding output circle (string[ 3 ])
                        - output circle = startItem
        :return:
        '''
        '''
        :return:
        '''
        print 'computeConnections...'
        nodeList = self.scene.getNodeList()
        for node in nodeList:
            print node.data( 0 ).toPyObject()
        #print any( node for node in nodeList if node.data( 0 ).toPyObject() == 'fnuzjr' )
        #for node in nodeList:
        #    if node.data( 0 ).toPyObject() == 'fnuzjr':
        #        print 'node found at index %s' %( nodeList.index( node ) )
        for node in nodeList:
            currentNode = node
            print 'processing %s (%s)' %( node.data( 0 ).toPyObject(), node )
            nodeRootDir = node.getNodeRootDir()
            nodeInputDir = os.sep.join( [ str( nodeRootDir ), 'input' ] )
            print 'nodeInputDir = %s' %nodeInputDir
            inputs = os.listdir( nodeInputDir )
            if len( inputs ) > 0:
                for input in inputs:
                    if not input in self.exclusions:
                        string = input.split( '.' )
                        x = 0
                        for node in nodeList:
                            print x, node.data( 0 ).toPyObject()
                            x += 1
                            print 'nodeList 123:', nodeList
                            print string[ 2 ]
                            if node.data( 0 ).toPyObject() == string[ 2 ] or str( node.data( 0 ).toPyObject() ).startswith( 'LDR' ):

                                sourceNodeIndex = nodeList.index( node )

                                sourceNode = node

                                outputList = node.outputList

                                for output in outputList:
                                    print 'processing =', output.data( 0 ).toPyObject()
                                    if len( str( output.data( 0 ).toPyObject() ).split( '.' ) ) == 1:
                                        if output.data( 0 ).toPyObject() == string[ 3 ]:
                                            startItem = output
                                            print 'if: startItem =', startItem

                                    else:
                                        print 'hallo'
                                        if str( output.data( 0 ).toPyObject() ).split( '.' )[ 3 ] == string[ 3 ]:
                                            print 'velo'
                                            startItem = output

                        endItem = currentNode.inputList[ len( currentNode.inputs ) ]

                        print 'new line from %s to %s' %( startItem.data( 0 ).toPyObject(), endItem )



                        connectionLine = bezierLine( self, self.scene, startItem, endItem )

                        '''

                        endItem.parentItem().inputs.append( endItem )
                        #endItem.connection.append( connectionLine )
                        endItem.output.append( startItem )
                        endItem.parentItem().incoming.append( startItem )
                        startItem.inputs.append( endItem )

                        startItemRootDir = startItem.parentItem().getNodeRootDir()
                        endItemRootDir = endItem.parentItem().getNodeRootDir()

                        startItemOutputLabel = startItem.getLabel()

                        endItemInputDir = os.path.join( str( endItemRootDir ), 'input', str( input ) )

                        endItem.setInputDir( endItemInputDir )

                        self.scene.addItem( connectionLine )

                        endItem.parentItem().newInput( self.scene )

                        '''

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
        
        self.shotsGroupBox.setTitle( 'looking at ' + currentProject + os.sep + 'shots' + os.sep + buttonText )
        self.assetsGroupBox.setTitle( 'looking at ' + currentProject + os.sep + 'shots' + os.sep + buttonText )
        
        self.currentContent = currentProject + os.sep + 'content' + os.sep + 'shots' + os.sep + buttonText

        for nodeItem in shotContent:
            if nodeItem in self.exclusions:
                pass
            else:
                self.propertyNodePathShots = os.path.join( self.shotsRoot, str( buttonText ), nodeItem, 'propertyNode.xml' )
                
                newNode = node( self, self.scene, self.propertyNodePathShots )
                newNode.addText( self.scene, nodeItem )
                self.scene.addToNodeList( newNode )
                
        self.computeConnections()
            
        
    def getCurrentProject( self ):
        currentProject = str( self.projectComboBox.currentText() )
        self.assetsRoot = os.path.join( self.projectsRoot, currentProject )
        return currentProject
        
            
    
    def getAssetContent( self, assetButton ):
        
        self.nodeView.setVisible( True )
        
        buttonText = assetButton.text()

        self.scene.clear()
        self.addRectangular()
        self.scene.clearNodeList()
        currentProject = str( self.projectComboBox.currentText() )
        self.assetsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'assets' )
        assetContent = os.listdir( os.path.normpath( os.path.join( str( self.assetsRoot ), str( buttonText ) ) ) )

        self.shotsGroupBox.setTitle( 'looking at ' + currentProject + os.sep + 'assets' + os.sep + buttonText )
        self.assetsGroupBox.setTitle( 'looking at ' + currentProject + os.sep + 'assets' + os.sep + buttonText )
        
        self.currentContent = currentProject + os.sep + 'content' + os.sep + 'assets' + os.sep + buttonText

        for nodeItem in assetContent:
            if nodeItem in self.exclusions:
                pass
            else:
                self.propertyNodePathAssets = os.path.join( self.assetsRoot, str( buttonText ), nodeItem, 'propertyNode.xml' )
                
                newNode = node( self, self.scene, self.propertyNodePathAssets )
                newNode.addText( self.scene, nodeItem )
                self.scene.addToNodeList( newNode )
                
        self.computeConnections()


    def addContent( self ):
        
        assets = []
        shots = []
        
        currentProject = str( self.projectComboBox.currentText() )
        self.assetsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'assets' )
        self.shotsRoot = os.path.join( self.projectsRoot, currentProject, 'content', 'shots' )
        try:
            for i in os.listdir( self.assetsRoot ):
                if not i in self.exclusions:
                    assets.append( i )
                else:
                    pass
                    
                
        except:
            print 'no assetsRoot found'
        try:
            for i in os.listdir( self.shotsRoot ):
                if not i in self.exclusions:
                    shots.append( i )
                else:
                    pass
        except:
            print 'no shotsRoot found'  
    
    
        #Assets

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
        
        self.shotsGroupBox = QGroupBox( currentProject )
        layoutShots = QHBoxLayout()
        
        self.createShotPushButton = QPushButton( 'create new shot' )
        self.createShotPushButton.clicked.connect( self.createNewContent )
        layoutShots.addWidget( self.createShotPushButton )
        
        self.shotButtonGroup = QButtonGroup()
        self.shotButtonGroup.buttonClicked[ QAbstractButton ].connect( self.getShotContent )
        
        for i in shots:
            shotPushButton = QPushButton( i )
            shotPushButton.setContextMenuPolicy( Qt.CustomContextMenu )
            self.connect( shotPushButton, SIGNAL( 'customContextMenuRequested( const QPoint& )' ), self.contentContextMenu )
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

    def contentContextMenu( self, point ):
        
        sendingButton = self.sender()
        sendingButtonText = sendingButton.text()

        tabIndex = self.assetsShotsTabWidget.currentIndex()
        
        if tabIndex == 0:
            currentTarget = self.assetsRoot
            
        elif tabIndex == 1:
            currentTarget = self.shotsRoot
            
        contentLocation = os.path.join( str( currentTarget ), str( sendingButtonText ) )

        popMenu = QMenu( self )
        popMenu.addAction( 'open directory', lambda: self.locateContent( contentLocation ) )
        popMenu.addAction( 'clone', lambda: self.cloneContent( contentLocation ) )
        popMenu.addAction( 'disable', self.foo )
        popMenu.addSeparator()
        popMenu.addAction( 'delete', lambda: self.removeContent( contentLocation ) )

        popMenu.exec_( sendingButton.mapToGlobal( point ) )
        

    def fooCallback( self, arg = None ):
        def callback():
            self.foo( arg )
        return callback


    def foo( self, arg = None ):
        try:
            print arg
        except:
            pass
    
    
    def printShit( self, button ):
        print button.text()
    
    
    def addProjects( self ):
        self.sendTextToBox( 'looking for projects in %s:\n' %( self.projectsRoot ) )
        self.projectComboBox.clear()
        
        self.projectComboBox.addItem( 'select project' )
        self.projectComboBox.insertSeparator( 1 )
        try:
            for i in os.listdir( self.projectsRoot ):
                if os.path.isdir( os.path.join( self.projectsRoot, i ) ):
                    self.projectComboBox.addItem( i )
                    self.sendTextToBox( '\tproject found: %s\n' %( i ) )
        except:
            self.sendTextToBox( 'no project found.\n' )
        
        self.sendTextToBox( 'all projects added.\n\n' )
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

    def submitDeadlineJob( self, jobFile ):

        executable = '/bin/bash'

        executable = executable.replace( '\"', '' )
        executable = executable.replace( '\'', '' )
        if executable.endswith( ' ' ):
            executable = executable[:-1]

        #now = datetime.datetime.now()

        arguments = QStringList()

        arguments.append( jobFile )

        process = QProcess( self )

        pColor = self.newProcessColor()

        process.readyReadStandardOutput.connect( lambda: self.dataReadyStd( process, pColor ) )
        process.readyReadStandardError.connect( lambda: self.dataReadyErr( process, pColor ) )
        process.started.connect( lambda: self.toolOnStarted( process ) )
        process.finished.connect( lambda: self.toolOnFinished( process ) )

        process.start( executable, arguments )



    def runTool( self ):

        index = self.toolsComboBox.currentIndex() - 2

        if index < 0:
            self.sendTextToBox( "%s: nothing to run\n" %datetime.datetime.now() )

        else:

            path = re.findall( r'"([^"]*)"', self._tools[ index ][ 1 ][ 0 ] )[ 0 ]

            if os.path.exists( os.path.normpath( path ) ):
                self.sendTextToBox( "%s: starting %s. Enjoy!\n" %( datetime.datetime.now(), self._tools[ index ][ 0 ] ) )

                process = QProcess( self )

                pColor = self.newProcessColor()

                process.readyReadStandardOutput.connect( lambda: self.dataReadyStd( process, pColor ) )
                process.readyReadStandardError.connect( lambda: self.dataReadyErr( process, pColor ) )
                process.started.connect( lambda: self.toolOnStarted( process ) )
                process.finished.connect( lambda: self.toolOnFinished( process ) )

                try:
                    toolTemplate = self._tools[ index ][ 7 ]
                except:
                    toolTemplate = 'None'

                tempDir = os.path.join( os.path.expanduser( '~' ), 'pypelyne_temp' )
                currentDir = os.getcwd()

                if not os.path.exists( tempDir ):
                    os.makedirs( tempDir, mode=0777 )

                if not toolTemplate == 'None':
                    dateTime = datetime.datetime.now().strftime( '%Y-%m-%d_%H%M-%S' )
                    src = os.path.join( 'src', 'template_documents', toolTemplate )
                    dst = os.path.join( tempDir, str( os.path.splitext( toolTemplate )[ 0 ] + '.' + dateTime + os.path.splitext( toolTemplate )[ 1 ] ) )
                    shutil.copyfile( src, dst )

                    os.chdir( tempDir )

                    executable = self._tools[ index ][ 1 ][ 0 ]

                    executable = executable.replace( '\"', '' )
                    executable = executable.replace( '\'', '' )
                    if executable.endswith( ' ' ):
                        executable = executable[ :-1 ]

                    arguments = QStringList()
                    arguments.append( dst )

                    process.start( executable, arguments )
                    os.chdir( currentDir )
                else:
                    os.chdir( tempDir )
                    executable = self._tools[ index ][ 1 ][ 0 ]
                    process.start( executable )
                    os.chdir( currentDir )

            else:
                self.sendTextToBox( "%s: cannot start %s. is it installed?\n" %( datetime.datetime.now(), self._tools[index][0] ) )


        self.toolsComboBox.setCurrentIndex( 0 )

    def toolOnStarted( self, qprocess ):
        self.qprocesses.append( qprocess )

    def toolOnFinished( self, qprocess ):
        self.qprocesses.remove( qprocess )
    
    def sendTextToBox( self, text ):
        cursorBox = self.statusBox.textCursor()
        cursorBox.movePosition(cursorBox.End)
        cursorBox.insertText( str( text ) )
        self.statusBox.ensureCursorVisible()
    
    def dataReadyStd( self, process, pColor ):
        #palette = QPalette()
        #color = QColor( 0, 255, 0 )
        box = self.statusBox
        #palette.setColor( QPalette.Foreground, Qt.red )
        #box.setPalette( palette )
        #box.setTextColor( color )
        cursorBox = box.textCursor()
        cursorBox.movePosition( cursorBox.End )

        # get the current format
        stdFormat = cursorBox.charFormat()
        newFormat = cursorBox.charFormat()

        stdFormat.setBackground( Qt.white )
        stdFormat.setForeground( Qt.black )

        # modify it
        newFormat.setBackground( pColor )
        newFormat.setForeground( pColor.lighter( 160 ) )
        # apply it
        cursorBox.setCharFormat( newFormat )

        cursorBox.insertText( '%s (std):   %s' %( datetime.datetime.now(), str( process.readAllStandardOutput() ) ) )

        cursorBox.movePosition( cursorBox.End )
        format = cursorBox.charFormat()
        format.setBackground( Qt.white )
        format.setForeground( Qt.black )
        cursorBox.setCharFormat( stdFormat )

        cursorBox.insertText( '\n' )

        self.statusBox.ensureCursorVisible()

    def dataReadyErr( self, process, pColor ):
        #color = QColor( 255, 0, 0 )
        box = self.statusBox
        #box.setTextColor( color )
        cursorBox = box.textCursor()
        cursorBox.movePosition( cursorBox.End )

        # get the current format
        stdFormat = cursorBox.charFormat()
        newFormat = cursorBox.charFormat()

        stdFormat.setBackground( Qt.white )
        stdFormat.setForeground( Qt.black )

        # modify it
        newFormat.setBackground( pColor )
        newFormat.setForeground( pColor.darker( 160 ) )
        # apply it
        cursorBox.setCharFormat( newFormat )

        cursorBox.insertText( "%s (err):   %s" %( datetime.datetime.now(), str( process.readAllStandardError() ) ) )

        cursorBox.movePosition( cursorBox.End )
        format = cursorBox.charFormat()
        format.setBackground( Qt.white )
        format.setForeground( Qt.black )
        cursorBox.setCharFormat( stdFormat )

        cursorBox.insertText( '\n' )

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