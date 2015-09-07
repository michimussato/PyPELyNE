'''
Created on Feb 4, 2015

@author: michaelmussato
'''

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import xml.etree.ElementTree as ET

from src.circlesInOut import *
from src.node import *
from src.bezierLine import *

from src.newNode import *
from src.newOutput import *
from src.newLoader import *
#from src.listAssets import *

import shutil, os, subprocess, logging

# class Signals( QObject ):
#     trigger = pyqtSignal( str )

class SceneView( QGraphicsScene ):
    textMessage = pyqtSignal( str )
    nodeSelect = pyqtSignal( object )
    nodeDeselect = pyqtSignal()
    
    def __init__( self, mainWindow, parent=None ):
        super( SceneView, self ).__init__( parent )

        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.pypelyneRoot
        self.currentPlatform = self.mainWindow.currentPlatform
        self.projectsRoot = str( self.mainWindow.projectsRoot )

        self.exclusions = self.mainWindow.exclusions
        self.imageExtensions = self.mainWindow.imageExtensions
        self.movieExtensions = self.mainWindow.movieExtensions
        self.sequenceExec = self.mainWindow.sequenceExec

        self.line = None

        self.nodeList = []

    def addToNodeList( self, node ):
        self.nodeList.append( node )

    def getNodeList( self ):
        return self.nodeList
        
    def clearNodeList( self ):
        self.nodeList = []

    def keyPressEvent( self, event ):
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                if item.inputs > 1:
                    item.sendFromNodeToBox( 'item has inputs. cannot delete.\n' )
                elif item.inputs == 1:
                    self.removeItem(item)

        super( SceneView, self ).keyPressEvent( event )

    def unmakeLive( self, path ):
        os.unlink( path )

    def unmakeLiveCallback( self, path ):
        def callback():
            self.unmakeLive( path )
        return callback

    def viewVersion( self, imgFile ):
        def callback():
            subprocess.Popen( [ self.sequenceExec, imgFile ], shell=False )
        return callback

    def compareVersion( self, imgFile, liveImgFile ):
        def callback():
            subprocess.Popen( [ self.sequenceExec, imgFile, '-wipe', liveImgFile ], shell=False )
        return callback

    def differenceVersion( self, imgFile, liveImgFile ):
        def callback():
            subprocess.Popen( [ self.sequenceExec, imgFile, '-diff', liveImgFile ], shell=False )
        return callback

    def deleteContentCallback( self, path ):
        def callback():
            self.deleteContent( path )
        return callback

    def deleteContent( self, path ):
        #print path
        shutil.rmtree( path )

    def copyToClipboard( self, text ):
        self.mainWindow.clipBoard.setText( text )
        print '%s copied to clipboard' %( text )

    def copyToClipboardCallback( self, text ):
        def callback():
            self.copyToClipboard( text )
        return callback

        
    def contextMenu( self, pos ):
        
        self.menu = QMenu()

        #currentProject = self.mainWindow.getCurrentProject()
        #currentContent = self.mainWindow.getCurrentContent()

        objectClicked = self.itemAt( pos )

        #items = []

        contentDirs = os.listdir( os.path.join( str( self.mainWindow.getProjectsRoot() ), str( self.mainWindow.getCurrentContent() ) ) )
        
        self.menu.addAction( 'new node', self.newNodeDialog( pos ) )
        self.menu.addSeparator()
        self.menu.addAction( 'new loader', self.newLoaderDialog( pos ) )
        #for dir in contentDirs:
        if not any( dir.startswith( 'SVR' ) for dir in contentDirs ):
            self.menu.addAction( 'new saver', self.newSaverDialog( pos ) )
        else:
            print 'content already has a saver'
        self.menu.addSeparator()

        #self.menu.addAction( 'new library loader', self.newLibraryLoaderCallback( pos ) )
        #self.menu.addAction( 'new library saver', self.newLibrarySaverCallback() )
        #self.menu.addSeparator()
        
        try:

            #node specific context menu items
            if isinstance( objectClicked, node ) \
                    or isinstance( objectClicked.parentItem(), node ) \
                    or isinstance( objectClicked.parentItem().parentItem(), node ) \
                    or isinstance( objectClicked.parentItem().parentItem().parentItem(), node ):

                if isinstance( objectClicked, node ):
                    nodeClicked = objectClicked
                elif isinstance( objectClicked.parentItem(), node ):
                    nodeClicked = objectClicked.parentItem()
                elif isinstance( objectClicked.parentItem().parentItem(), node ):
                    nodeClicked = objectClicked.parentItem().parentItem()
                elif isinstance( objectClicked.parentItem().parentItem().parentItem(), node ):
                    nodeClicked = objectClicked.parentItem().parentItem().parentItem()

                if nodeClicked.label.startswith( 'SVR' ):
                    self.menu.addAction( 'export to library', self.mainWindow.exportToLibraryCallback( nodeClicked ) )
                self.menu.addSeparator()



                self.menuNode = self.menu.addMenu( 'node' )

                if not nodeClicked.label.startswith( 'LDR' ) and not nodeClicked.label.startswith( 'SVR' ):
                    self.menuNode.addAction( 'open node directory', lambda: self.mainWindow.locateContent( nodeClicked.getNodeRootDir() ) )

                    if not os.path.exists( os.path.join( nodeClicked.getNodeRootDir(), 'locked' ) ):
                        self.menuNode.addSeparator()
                        self.menuNode.addAction( 'cleanup node', self.cleanUpNodeCallback( nodeClicked ) )
                        self.menuNode.addAction( 'delete node', self.removeObjectCallback( nodeClicked ) )

                        if os.path.exists( os.path.join( nodeClicked.getNodeRootDir(), 'checkedOut' ) ):
                            self.menuNode.addSeparator()
                            self.menuNode.addAction( 'check in node', self.mainWindow.checkInCallback( nodeClicked ) )

                        else:
                            self.menuNode.addSeparator()
                            self.menuNode.addAction( 'check out node', self.mainWindow.checkOutCallback( nodeClicked ) )

                elif nodeClicked.label.startswith( 'LDR_AST' ):

                    self.menuNode.addAction( 'open asset tree', lambda: self.mainWindow.getAssetContent( None, nodeClicked.getLabel() ) )
                    self.menuNode.addSeparator()
                    self.menuNode.addAction( 'delete asset loader', self.removeObjectCallback( nodeClicked ) )

                elif nodeClicked.label.startswith( 'LDR_SHT' ):
                    #self.menuNode.addAction( 'open shot', lambda: self.foo( nodeClicked.getNodeRootDir() ) )
                    self.menuNode.addAction( 'open shot tree', lambda: self.mainWindow.getShotContent( None, nodeClicked.getLabel() ) )
                    self.menuNode.addSeparator()
                    self.menuNode.addAction( 'delete shot loader', self.removeObjectCallback( nodeClicked ) )

                elif nodeClicked.label.startswith( 'LDR_LIB' ):
                    self.menuNode.addAction( 'delete library loader', self.removeObjectCallback( nodeClicked ) )

                elif nodeClicked.label.startswith( 'SVR_AST' ):
                    self.menuNode.addAction( 'delete asset saver', self.removeObjectCallback( nodeClicked ) )
                    self.menuNode.addSeparator()
                    self.menuNode.addAction( 'check out asset', self.mainWindow.checkOutCallback( nodeClicked ) )

                elif nodeClicked.label.startswith( 'SVR_SHT' ):
                    self.menuNode.addAction( 'delete shot saver', self.removeObjectCallback( nodeClicked ) )
                    self.menuNode.addSeparator()
                    self.menuNode.addAction( 'check out shot', self.mainWindow.checkOutCallback( nodeClicked ) )

                #elif nodeClicked.label.startswith

                    #self.mainWindow.getShotContent( None, nodeClicked.getLabel() )

                self.menuNode.addSeparator()
                #self.menu.addAction( 'cleanup node', self.fooCallback( 'cleanup node' ) )




                #self.menu.addSeparator()


                #self.menu.addAction( 'clone', lambda: self.cloneNodeCallback( objectClicked ) ).setActive ( 'False' )


                #self.menu.addAction( 'none', lambda: None )
                #items.append( 'delete this node' )
                #print objectClicked.getNodeRootDir()

                #location = self.mainWindow.locateContent( objectClicked.getNodeRootDir( objectClicked ) )






            #input specific context menu items
            if isinstance( objectClicked, portInput ) and not objectClicked.label == None:
                self.menuInput = self.menu.addMenu( 'input' )



                #items.append( 'delete this input' )

                self.menuPathOps = self.menuInput.addMenu( 'clipboard' )
                self.menuInput.addSeparator()
                self.menuInput.addAction( 'delete input', self.removeObjectCallback( objectClicked ) )


                inputLabel = objectClicked.getLabel()
                inputDir = objectClicked.getInputDir()

                outputNode = objectClicked.parentItem()
                outputNodeRootDir = outputNode.getNodeRootDir()

                self.menuPathOps.addAction( 'copy input label', self.copyToClipboardCallback( inputLabel ) )
                self.menuPathOps.addAction( 'copy absolute input path',  self.copyToClipboardCallback( os.path.join( inputDir, inputLabel ) ) )
                self.menuPathOps.addAction( 'copy relative input path',  self.copyToClipboardCallback( os.path.relpath( os.path.join( inputDir, inputLabel ), os.path.join( outputNodeRootDir ) ) ) )





            #output specific context menu items
            #if isinstance( objectClicked, portOutput ) and not objectClicked.parentItem().label.startswith( 'LDR' ):
            if isinstance( objectClicked, portOutput ):
                #items.append( 'delete this output' )

                #self.menu.addSeparator()



                #self.menu.addSeparator()




                self.menuOutput = self.menu.addMenu( 'output' )

                self.menuPathOps = self.menuOutput.addMenu( 'clipboard' )
                self.menuOutput.addSeparator()

                #print objectClicked.getOutputDir()

                outputDir = objectClicked.getOutputDir()
                #print outputDir
                outputLabel = objectClicked.getLabel()
                #print outputLabel
                liveDir = objectClicked.getLiveDir()
                #print liveDir
                outputNodeRootDir = objectClicked.getOutputRootDir()










                #RV viewer here...

                #print 'liveDir = %s' %liveDir


                #versions = self.getVersions( outputDir )
                #try:
                #    versions.remove( 'current' )
                #except:
                #    pass

                #print outputDir
                #print os.path.basename( outputDir )

                #print outputDir

                self.menuOutput.addAction( 'open output directory', lambda: self.mainWindow.locateContent( outputDir ) )

                #self.menuVersion.addAction( 'cleanup', lambda: self.foo( 'cleanup' ) )





                self.menuOutput.addSeparator()

                #self.menuMakeLive = self.menuVersion.addMenu( 'make live' )

                #try:
                #    print os.path.exists( liveDir )
                #except:
                #    raise 'shizzle'

                self.menuPathOps.addAction( 'copy output label', self.copyToClipboardCallback( outputLabel ) )
                self.menuPathOps.addAction( 'copy absolute output path',  self.copyToClipboardCallback( os.path.join( outputDir, 'current', outputLabel ) ) )
                self.menuPathOps.addAction( 'copy relative output path',  self.copyToClipboardCallback( os.path.relpath( os.path.join( outputDir, 'current', outputLabel ), os.path.join( outputNodeRootDir ) ) ) )


                versions = self.getVersions( outputDir )
                #print 'outputDir', outputDir
                try:
                    versions.remove( 'current' )
                except:
                    pass
                try:
                    versions.remove( os.path.basename( outputDir ).split( '.' )[ -1 ] )
                except:
                    pass
                #print 'outputDir', outputDir

                if not objectClicked.parentItem().label.startswith( 'LDR' ):

                    self.menuOutput.addAction( 'cleanup output', self.cleanUpOutputCallback( objectClicked ) )

                    if os.path.exists( liveDir ):

                        #liveVersion = os.path.basename( os.readlink( liveDir ) )


                        #self.menuPathOps.addAction( 'to clipboard 1234', self.copyToClipboardCallback( '1234' ) )
                        #self.menuPathOps.addAction( 'to clipboard 5678', self.copyToClipboardCallback( '5678' ) )
                        #self.menuPathOps.addAction( 'copy relative path', self.foo(  ) )
                        #self.menuPathOps()

                        self.menuOutput.addAction( 'remove pipe (live)', self.unmakeLiveCallback( liveDir ) )

                #if not objectClicked.parentItem().label.startswith( 'LDR' ):
                    self.menuOutput.addAction( 'delete output', self.removeObjectCallback( objectClicked ) )
                    self.menuOutput.addSeparator()

                    self.menuOutput.addAction( 'create new version', self.createNewVersionCallback( outputDir ) )

                    #print 'added'
                #else:


                self.menuOutput.addSeparator()
                #print versions
                for version in versions:
                    '''
                    if version in self.exclusions:
                        try:
                            os.remove( os.path.join( outputDir, version ) )
                            logging.info( 'exclusion found in versions of output %s. %s removed.' %( objectClicked.label, os.path.join( outputDir, version ) ) )
                        except:
                            logging.warning( 'exclusion found but not removed: %s' %( os.path.join( outputDir, version ) ) )
                    '''
                    if not version == 'current':

                        if not objectClicked.parentItem().label.startswith( 'LDR' ):
                            versionPath = os.path.join( outputDir, version )
                        else:
                            versionPath = outputDir
                        print 'versionPath', versionPath






                        outputDirContent = os.listdir( versionPath )

                        #print 'outputDirContent', outputDirContent
                        for item in outputDirContent:
                            if item in self.exclusions:
                                try:
                                    os.remove( os.path.join( versionPath, item ) )
                                    outputDirContent.remove( item )
                                    logging.info( 'exclusion found and removed: %s' %( os.path.join( versionPath, item ) ) )
                                except:
                                    outputDirContent.remove( item )
                                    logging.warning( 'exclusion found but not removed: %s' %( os.path.join( versionPath, item ) ) )
                        outputDirContent.remove( outputLabel )

                        menuMakeLive = self.menuOutput.addMenu( version )


                        if self.currentPlatform == 'Darwin' or self.currentPlatform == 'Linux':
                            if os.path.exists( liveDir ):
                                if not objectClicked.parentItem().label.startswith( 'LDR' ):
                                    if os.path.basename( os.readlink( liveDir ) ) == version:
                                        menuMakeLive.setIcon( QIcon( 'src/icons/dotActive.png' ) )
                                    else:
                                        menuMakeLive.setIcon( QIcon( 'src/icons/dotInactive.png' ) )
                                else:
                                    menuMakeLive.setIcon( QIcon( 'src/icons/dotActive.png' ) )
                            else:
                                menuMakeLive.setIcon( QIcon( 'src/icons/dotInactive.png' ) )
                        elif self.currentPlatform == 'Windows':
                            if os.path.exists( liveDir ):
                                #print liveDir
                                #print os.path.abspath( liveDir )
                                #print os.path.realpath( liveDir )
                                #print version
                                if os.path.basename( os.path.realpath( liveDir ) ) == version:
                                    menuMakeLive.setIcon( QIcon( 'src/icons/dotActive.png' ) )
                                else:
                                    menuMakeLive.setIcon( QIcon( 'src/icons/dotInactive.png' ) )
                            else:
                                menuMakeLive.setIcon( QIcon( 'src/icons/dotInactive.png' ) )

                        #print 'here we are'

                        #if outputLabel.startswith( 'SEQ' ) or outputLabel.startswith( 'TEX' ) or outputLabel.startswith( 'PLB' ):
                        #print os.path.splitext( outputDirContent[ 0 ] )[ 1 ]
                        if len( outputDirContent ) > 0:
                            if os.path.splitext( outputDirContent[ 0 ] )[ 1 ] in self.imageExtensions or os.path.splitext( outputDirContent[ 0 ] )[ 1 ] in self.movieExtensions:
                                '''
                                for exclusion in self.exclusions:
                                    try:
                                        #if os.path.exists( os.path.join( outputDirContent, exclusion ) ):
                                        logging.info( 'exclusion removed from list: %s' %( os.path.join( outputDirContent, exclusion ) ) )
                                        #os.remove( os.path.join( outputDirContent, exclusion ) )
                                        outputDirContent.remove( exclusion )
                                    except:
                                        logging.warning( 'exclusion found but not removed from list: %s' %( os.path.join( outputDirContent, exclusion ) ) )
                                '''

                                try:
                                    menuMakeLive.addAction( 'view', self.viewVersion( os.path.join( versionPath, outputDirContent[ 0 ] ) ) )
                                    if not objectClicked.parentItem().label.startswith( 'LDR' ):
                                        try:
                                            if self.mainWindow.rv == True:
                                                menuMakeLive.addAction( 'compare to live', self.compareVersion( os.path.join( versionPath, outputDirContent[ 0 ] ), os.path.join( liveDir, outputDirContent[ 0 ] ) ) )
                                                menuMakeLive.addAction( 'difference to live', self.differenceVersion( os.path.join( versionPath, outputDirContent[ 0 ] ), os.path.join( liveDir, outputDirContent[ 0 ] ) ) )

                                        except:
                                            print 'compare/difference to live version not possible'
                                except:
                                    print 'not possible to view SEQ. emty?'

                                #menuMakeLive.addAction( 'compare to live', self.compareVersion( os.path.join( outputDir, version, outputDirContent[ 0 ] ), os.path.join( liveDir, outputDirContent[ 0 ] ) ) )


                                #self.versionMenu.addAction( 'view live', self.viewLive( os.path.join( liveDir, liveDirContent[ 0 ] ) ) )



                        if not objectClicked.parentItem().label.startswith( 'LDR' ):
                            menuMakeLive.addAction( 'open directory', self.mainWindow.locateContentCallback( versionPath ) )
                            deleteVersionAction = menuMakeLive.addAction( 'delete version', self.deleteContentCallback( versionPath ) )

                            makeCurrentAction = menuMakeLive.addAction( 'make current', self.makeCurrentCallback( versionPath ) )


                        if self.currentPlatform == 'Darwin' or self.currentPlatform == 'Linux':
                            if not objectClicked.parentItem().label.startswith( 'LDR' ):
                                if os.path.join( outputDir, version ) == os.path.join( outputDir, os.readlink( os.path.join( outputDir, 'current' ) ) ):
                                    deleteVersionAction.setEnabled( False )
                                else:
                                    deleteVersionAction.setEnabled( True )

                        elif self.currentPlatform == 'Windows':


                            print os.path.join( outputDir, version )
                            print os.path.join( outputDir, 'current' )
                            print os.path.join( outputDir, os.path.realpath( os.path.join( outputDir, 'current' ) ) )


                        if not objectClicked.parentItem().label.startswith( 'LDR' ):
                            makeLiveAction = menuMakeLive.addAction( 'make live', self.makeLiveCallback( versionPath ) )


                            #print liveDir
                            #print outputLabel
                            #print 'test', os.path.join( os.path.dirname( os.path.dirname( liveDir ) ), 'output', outputLabel, version )
                            #print os.path.basename( os.readlink( liveDir ) )
                            #print 'livedir   =', os.path.join( outputDir, os.path.basename( os.readlink( liveDir ) ) )
                            #print 'outputdir =', os.path.join( outputDir, version )



                            if len( outputDirContent ) > 0:
                                makeLiveAction.setEnabled( True )


                                #outputDir = objectClicked.getOutputDir()

                                #outputLabel = objectClicked.getLabel()

                                #liveDir = objectClicked.getLiveDir()
                            else:
                                makeLiveAction.setEnabled( False )
                                makeLiveAction.setText( makeLiveAction.text() + ' (no content)' )

                            try:

                                if os.path.join( outputDir, os.path.basename( os.readlink( liveDir ) ) ) == os.path.join( outputDir, version ):
                                    makeLiveAction.setEnabled( False )
                                    makeLiveAction.setText( makeLiveAction.text() + ' (already live)' )
                                    deleteVersionAction.setEnabled( False )

                            except:
                                print 'no live version found'
                                #makeLiveAction.setEnabled( True )


                        if self.currentPlatform == 'Darwin' or self.currentPlatform == 'Linux':
                            if not objectClicked.parentItem().label.startswith( 'LDR' ):
                                if versionPath == os.path.join( outputDir, os.path.basename( os.readlink( os.path.join( outputDir, 'current' ) ) ) ):
                                    makeCurrentAction.setEnabled( False )

                        elif self.currentPlatform == 'Windows':
                            if versionPath == os.path.join( outputDir, os.path.basename( os.path.realpath( os.path.join( outputDir, 'current' ) ) ) ):
                                makeCurrentAction.setEnabled( False )




        #except:
            #print 'not working'
            #pass





        except:
            logging.warning( 'context menu fuck up or objectClicked == None (QGraphicsScene)' )

        self.menu.move( QCursor.pos() )
        self.menu.show()

    def cleanUpOutputProc( self, portOutput ):
        outputDir = portOutput.getOutputDir()
        outputVersions = self.getVersions( outputDir )
        #print outputVersions
        outputVersions.remove( 'current' )
        for exclusion in self.exclusions:
            try:
                outputVersions.remove( exclusion )
            except:
                pass
        #print outputVersions
        currentVersion = os.path.realpath( os.path.join( outputDir, 'current' ) )
        outputVersions.remove( os.path.basename( currentVersion ) )
        #print outputVersions
        #print currentVersion
        liveDir = portOutput.getLiveDir()
        #print liveDir

        if os.path.exists( liveDir ):
            liveDirDest = os.path.realpath( liveDir )
            liveVersion = os.path.basename( liveDirDest )
            #print liveDirDest
            #print liveVersion
            try:
                outputVersions.remove( liveVersion )
            except:
                print 'outputCurrent = live'

        else:
            print 'no liveDir'

        for outputVersion in outputVersions:
            #print 'need to delete %s' %( os.path.join( outputDir, outputVersion ) )
            self.deleteContent( os.path.join( outputDir, outputVersion ) )
            print '%s removed' %( os.path.join( outputDir, outputVersion ) )
        print 'output %s cleaned up' %( portOutput.getLabel() )

    def cleanUpNodeCallback( self, node ):
        def callback():
            self.cleanUpNode( node )
        return callback

    def cleanUpNode( self, node ):
        reply = QMessageBox.warning( self.mainWindow, str( 'about to cleanup item' ), str( 'are you sure to \ncleanup all outputs of %s?' %( node.getLabel() ) ), QMessageBox.Yes | QMessageBox.No, QMessageBox.No )

        if reply == QMessageBox.Yes:
            for output in node.outputList:
                self.cleanUpOutputProc( output )
            #print node.outputs
            #print node.outputList

    def cleanUpOutputCallback( self, portOutput ):
        def callback():
            self.cleanUpOutput( portOutput )
        return callback

    def cleanUpOutput( self, portOutput ):

        #print portOutput.getLabel()

        reply = QMessageBox.warning( self.mainWindow, str( 'about to cleanup item' ), str( 'are you sure to \ncleanup %s?' %( portOutput.getLabel() ) ), QMessageBox.Yes | QMessageBox.No, QMessageBox.No )

        #print yes


        if reply == QMessageBox.Yes:
            self.cleanUpOutputProc( portOutput )

    def cloneNodeCallback( self, node ):
        def callback():
            self.cloneNode( node )

        return callback()

    def cloneNode( self, node ):
        print 'clone node not yet working'

    def makeLiveCallback( self, versionDir ):
        def callback():
            #print versionDir
            cwd = os.getcwd()

            outputDir = os.path.basename( os.path.dirname( versionDir ) )
            #print outputDir

            liveDir = os.path.join( os.path.dirname( os.path.dirname( os.path.dirname( versionDir ) ) ), 'live' )
            #print liveDir

            os.chdir( liveDir )

            if os.path.islink( outputDir ):
                os.unlink( outputDir )


            if self.currentPlatform == "Darwin" or self.currentPlatform == "Linux":
                os.symlink( os.path.relpath( versionDir, liveDir ), outputDir )
            elif self.currentPlatform == "Windows":
                cmdstring = str( "mklink /D " + outputDir + " " + os.path.relpath( versionDir, liveDir ) )
                #print 'Win cmdstring = %s' %( cmdstring )
                #os.chdir( os.path.dirname( endItemInputDir ) )
                os.system( cmdstring )


            os.chdir( cwd )

        return callback

    def makeCurrentCallback( self, currentDir ):
        def callback():
            self.makeCurrent( currentDir )
        return callback

    def makeCurrent( self, currentDir ):
        fullOutputDir = os.path.dirname( currentDir )
        #print currentDir
        #print fullOutputDir

        try:
            if self.currentPlatform == "Darwin":
                os.unlink( os.path.join( fullOutputDir, 'current' ) )
            elif self.currentPlatform == "Windows":
                os.rmdir( os.path.join( fullOutputDir, 'current' ) )
        except:
            print 'cannot remove symlink or not available'

        cwd = os.getcwd()
        os.chdir( os.path.join( os.path.dirname( currentDir ) ) )

        if self.currentPlatform == "Darwin":

            # TODO: need to create relative links
            #print os.path.relpath( newVersionDir, os.path.dirname( newVersionDir ) )

            os.symlink( os.path.basename( currentDir ), 'current' )

        elif self.currentPlatform == "Windows":
            logging.info( 'creating windows symlink to %s' %( os.path.join( os.path.dirname( currentDir ) ) ) )

            cmdstring = str( "mklink /D " + os.path.join( os.path.dirname( currentDir ), 'current' ) + " " + currentDir )
            #print 'Win cmdstring = %s' %( cmdstring )
            #os.chdir( os.path.dirname( endItemInputDir ) )
            os.system( cmdstring )
            #os.chdir( cwd )

            #endItems[ 0 ].setInputDir( inputLink )
            #print 'Windows: endItems[ 0 ].getInputDir() = %s' %endItems[ 0 ].getInputDir()

        os.chdir( cwd )

    def createNewVersion( self, fullOutputDir ):

        #print 'testing'
        newVersion = datetime.datetime.now().strftime( '%Y-%m-%d_%H%M-%S' )
        #print os.path.join( fullOutputDir, newVersion )

        #versions = self.getVersions( fullOutputDir )
        newVersionDir = os.path.join( fullOutputDir, newVersion )
        os.makedirs( newVersionDir, mode=0777 )
        open( os.path.join( fullOutputDir, newVersion, os.path.basename( fullOutputDir ) ), 'a' ).close()

        self.makeCurrent( newVersionDir )

    def createNewVersionCallback( self, fullOutputDir ):
        #print 'test'
        def callback():
            self.createNewVersion( fullOutputDir )
        return callback

    def getVersions( self, fullOutputDir ):
        versions = os.listdir( fullOutputDir )
        for version in versions:
            if version in self.exclusions:
                try:
                    os.remove( os.path.join( fullOutputDir, version ) )
                    versions.remove( version )
                    logging.info( 'exclusion found and removed: %s' %( os.path.join( fullOutputDir, version ) ) )
                except:
                    versions.remove( version )
                    logging.warning( 'exclusion found but not removed: %s' %( os.path.join( fullOutputDir, version ) ) )
        return versions

    def foo( self, arg ):
        print arg

    def fooCallback( self, arg ):
        def callback():


            print arg
        return callback

    def newOutputAuto( self, node, defaultOutput ):

        #print node.data( 0 ).toPyObject(), defaultOutput

        #projectsRoot = str( self.mainWindow.getProjectsRoot() )
        currentContent = str( self.mainWindow.getCurrentContent() )
        currentProject = str( self.mainWindow.projectComboBox.currentText() )

        outputDir = os.path.join( self.projectsRoot, currentContent, str( node.data( 0 ).toPyObject() ), 'output' )

        nodeRootDir = node.getNodeRootDir()

        newOutputDir = os.path.join( str( nodeRootDir ), 'output', str( defaultOutput ) )
        #print newOutputDir
        os.makedirs( newOutputDir, mode=0777 )

        #output = node.newOutput( self, str( defaultOutput ) )
        #print output

        

        #os.makedirs( newOutputDir, mode=0777 )

        #while not os.path.isdir( newOutputDir ):
        #    print 'not created yet'

        self.createNewVersion( newOutputDir )


    def newOutputDialog( self, node ):
        #def callback():
        #projectsRoot = str( self.mainWindow.getProjectsRoot() )
        currentContent = str( self.mainWindow.getCurrentContent() )
        currentProject = str( self.mainWindow.projectComboBox.currentText() )
        outputs = self.mainWindow.getOutputs()

        outputDir = os.path.join( self.projectsRoot, currentContent, str( node.data( 0 ).toPyObject() ), 'output' )

        #text, ok, outputIndex, mimeIndex = newOutputUI.getNewOutputData( outputDir, outputs )
        text, ok, outputIndex = newOutputUI.getNewOutputData( outputDir, outputs, self.mainWindow )

        if ok:
            #print text, ok, outputIndex

            nodeRootDir = node.getNodeRootDir()

            newOutputDir = os.path.join( str( nodeRootDir ), 'output', str( text ) )

            if os.path.exists( newOutputDir ):
                node.sendFromNodeToBox( '--- output already exists' + '\n' )
                
            else:
                #print self
                #print text
                #print type( str( text ) )
                #output = node.newOutput( node, text )
                node.newOutput( self, str( text ) )
                os.makedirs( newOutputDir, mode=0777 )

                #while not os.path.isdir( newOutputDir ):
                #    print 'not created yet'

                self.createNewVersion( newOutputDir )

                #print newOutputDir
                
                #print output
                #print 'item.parentItem().outputs = %s' %node.outputs
                #node.resize()
                node.sendFromNodeToBox( str( datetime.datetime.now() ) )
                node.sendFromNodeToBox( ':' + '\n' )
                node.sendFromNodeToBox( '--- new output created' + '\n' )
                


        #return callback

    def newOutputDialogOld( self, node ):


        nodeLabel = node.getLabel()
        #print nodeLabel
        text, ok = QInputDialog.getText( self.mainWindow, 'create new output in %s' %nodeLabel, 'enter output name:' )
        # text is a fucking QString object
        
        
        
        if ok:
            nodeRootDir = node.getNodeRootDir()
            
            
            newNodeDir = os.path.join( str( nodeRootDir ), 'output', str( text ) )
            
            if os.path.exists( newNodeDir ):
                node.sendFromNodeToBox( '--- output already exists' + '\n' )
                
            else:
                #print self
                #print text
                #print type( str( text ) )
                #output = node.newOutput( node, text )
                output = node.newOutput( self, str( text ) )
                os.makedirs( newNodeDir, mode=0777 )
                #print output
                #print 'item.parentItem().outputs = %s' %node.outputs
                #node.resize()
                node.sendFromNodeToBox( str( datetime.datetime.now() ) )
                node.sendFromNodeToBox( ':' + '\n' )
                node.sendFromNodeToBox( '--- new output created' + '\n' )
    '''
    def newLibraryLoaderDialogCallback( self, pos ):
        def callback():
            self.newLibraryLoaderDialog( pos )
        return callback

    def newLibraryLoaderDialog( self, pos ):
        print 'newLibraryLoaderDialog', pos
        libraryContent = os.listdir( self.mainWindow.libraryRoot )
    '''


    def newLoaderDialog( self, pos ):
        def callback():
            #projectsRoot = str( self.mainWindow.getProjectsRoot() )
            currentProject = str( self.mainWindow.projectComboBox.currentText() )

            currentContent = str( self.mainWindow.getCurrentContent() )
            #print currentContent
            #print os.path.basename( currentContent )

            activeItemPath = os.path.join( self.projectsRoot, currentProject, 'content', os.path.basename( os.path.dirname( currentContent ) ), os.path.basename( currentContent ) )

            #print activeItemPath

            #directoryContent = 

            ok, loaderName, sourceSaverLocation, tabIndex = newLoaderUI.getNewLoaderData( activeItemPath, self.mainWindow )

            if ok:

                print tabIndex

                #newLoaderName = loaderName

                #print tabItem

                newLoaderPath = os.path.join( activeItemPath, loaderName )

                #print newLoaderPath, sourceSaverLocation

                srcParentDirs = os.sep.join( [ str( os.path.relpath( self.projectsRoot, sourceSaverLocation ) ) ] ) + os.sep
                #print srcParentDirs

                src = os.sep.join( [ str( os.path.relpath( sourceSaverLocation, self.projectsRoot ) ) ] )
                #print src

                relPath = os.sep.join( [ str( srcParentDirs + src ) ] )
                #print relPath

                inputLinkOutput = os.path.join( newLoaderPath, 'output' )
                inputLinkLive = os.path.join( newLoaderPath, 'live' )
                #print inputLinkOutput
                #print inputLinkLive


                '''
                srcParentDirs = os.sep.join( [ str( os.path.relpath( self.projectsRoot, os.path.dirname( dst ) ) ) ] ) + os.sep
                print srcParentDirs


                src = os.sep.join( [ str( os.path.relpath( startItemOutputDir, self.projectsRoot ) ) ] )
                print src


                #relPath = os.sep.join( [ str( src + os.sep + os.sep.join( [ str( os.path.relpath( dst, self.projectsRoot ) ) ] ) ) ] )
                
                relPath = os.sep.join( [ str( srcParentDirs + src ) ] )
                #print relPath

                #src + os.sep + os.sep.join( [ str( os.path.relpath( dst, self.projectsRoot ) ) ] )


                
                inputLink = os.path.dirname( dst ) + os.sep + os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) ) + '.' + os.path.basename( os.path.dirname( startItemRootDir ) ) + '.' + os.path.basename( startItemRootDir ) + '.' + os.path.basename( dst )
                '''



                if not os.path.exists( newLoaderPath ):

                                #print newNodePath
                    propertyNode = ET.Element( 'propertyNode' )
                    
                    #print pos.x()
                    #print pos.y()
                    
                    posX = str( int( float( round( pos.x() ) ) ) )
                    posY = str( int( float( round( pos.y() ) ) ) )

                    ET.SubElement( propertyNode, 'node', { 'positionX':posX, 'positionY':posY } )
                    #ET.SubElement( propertyNode, 'positionX', { 'value':posX } )
                    #ET.SubElement( propertyNode, 'positionY', { 'value':posY } )

                    #print  toolFamily, toolVendor, toolVersion, toolArch

                    #ET.SubElement( propertyNode, 'task', { 'family':toolFamily, 'vendor':toolVendor, 'version':toolVersion, 'arch':toolArch, 'nodetask':toolTask } )




                    

                    
                    
                    
                    tree = ET.ElementTree( propertyNode )
                    
                    propertyNodePath = os.path.join( newLoaderPath, 'propertyNode.xml' )
                    #print propertyNodePath
                    

                    os.makedirs( newLoaderPath, mode=0777 )
                    #os.makedirs( os.path.join( newNodePath, 'project' ), mode=0777 )
                    os.makedirs( os.path.join( newLoaderPath, 'input' ), mode=0777 )
                    #os.makedirs( os.path.join( newLoaderPath, 'live' ), mode=0777 )
                    #os.symlink( relPath, inputLink )
                    os.symlink( os.path.join( relPath, 'input' ), inputLinkOutput )
                    os.symlink( os.path.join( relPath, 'input' ), inputLinkLive )
                    #os.makedirs( os.path.join( newLoaderPath, 'input' ), mode=0777 )
                    #print os.path.exists( newNodePath )

                    #for toolDirectory in toolDirectories:
                    #    os.makedirs( os.path.join( newNodePath, 'project', toolDirectory ), mode=0777 )

                    

                    #if not toolTemplate == 'None':

                    #    shutil.copyfile( os.path.join( 'src', 'template_documents', toolTemplate ), os.path.join( newNodePath, 'project', str( text + '.' + '0000' + os.path.splitext( toolTemplate )[ 1 ] ) ) )


                    
                    
                    #print ET.tostring( propertyNode ) 
                    #if not os.path.exists( propertyNodePath ): 
                    xmlDoc = open( propertyNodePath, 'w' )
                     
                    #print ET.tostring( propertyNode )
                    
                    xmlDoc.write( '<?xml version="1.0"?>' )
                    xmlDoc.write( ET.tostring( propertyNode ) )
                    #ET.ElementTree( propertyNode ).write( xmlDoc )
                    #tree.write( xmlDoc )
                    
                    
                    xmlDoc.close()
                    
                    newNode = node( self.mainWindow, self, propertyNodePath )
                    newNode.addText( self, loaderName )

                else:
                    print 'asset loader already exists'
        return callback

    def newLibraryLoaderCallback( self, pos ):
        def callback():
            self.newLibraryLoader( pos )
        return callback

    def newLibraryLoader( self, pos ):
        print 'newLibraryLoader', pos
        assetsInLibrary = os.listdir( self.mainWindow.libraryRoot )
        for exclusion in self.exclusions:
            if exclusion in assetsInLibrary:
                try:
                    os.remove( os.path.join( self.mainWindow.libraryRoot, exclusion ) )
                    assetsInLibrary.remove( exclusion )
                    logging.info( 'exclusion in libraryRoot removed' )
                except:
                    logging.info( 'exclusion in libraryRoot could not be removed' )
        assetsUI = listAssetsUI( self.mainWindow, pos )
        assetsUI.show()







    def newSaverDialog( self, pos ):
        def callback():

            #currentContent = str( self.mainWindow.getCurrentContent() )
            #currentProject = str( self.mainWindow.projectComboBox.currentText() )

            
            #nodeDir = os.path.join( self.projectsRoot, currentContent )

            #print nodeDir

            #projectsRoot = str( self.mainWindow.getProjectsRoot() )
            #currentTarget = str( self.mainWindow.getCurrentContent() )
            currentContent = str( self.mainWindow.getCurrentContent() )
            #print currentContent.split( os.sep )[ 2 ]
            currentProject = str( self.mainWindow.projectComboBox.currentText() )

            if currentContent.split( os.sep )[ 2 ] == 'assets':

                newSaverName = 'SVR_AST__' + os.path.basename( currentContent )

            elif currentContent.split( os.sep )[ 2 ] == 'shots':

                newSaverName = 'SVR_SHT__' + os.path.basename( currentContent )

            newSaverPath = os.path.join( self.projectsRoot, currentContent, newSaverName )

            if not os.path.exists( newSaverPath ):

                            #print newNodePath
                propertyNode = ET.Element( 'propertyNode' )
                
                #print pos.x()
                #print pos.y()
                
                posX = str( int( float( round( pos.x() ) ) ) )
                posY = str( int( float( round( pos.y() ) ) ) )

                ET.SubElement( propertyNode, 'node', { 'positionX':posX, 'positionY':posY } )
                #ET.SubElement( propertyNode, 'positionX', { 'value':posX } )
                #ET.SubElement( propertyNode, 'positionY', { 'value':posY } )

                #print  toolFamily, toolVendor, toolVersion, toolArch

                #ET.SubElement( propertyNode, 'task', { 'family':toolFamily, 'vendor':toolVendor, 'version':toolVersion, 'arch':toolArch, 'nodetask':toolTask } )




                

                
                
                
                tree = ET.ElementTree( propertyNode )
                
                propertyNodePath = os.path.join( newSaverPath, 'propertyNode.xml' )
                #print propertyNodePath
                

                os.makedirs( newSaverPath, mode=0777 )
                #os.makedirs( os.path.join( newNodePath, 'project' ), mode=0777 )
                os.makedirs( os.path.join( newSaverPath, 'output' ), mode=0777 )
                #os.makedirs( os.path.join( newNodePath, 'live' ), mode=0777 )
                os.makedirs( os.path.join( newSaverPath, 'input' ), mode=0777 )
                #print os.path.exists( newNodePath )

                #for toolDirectory in toolDirectories:
                #    os.makedirs( os.path.join( newNodePath, 'project', toolDirectory ), mode=0777 )

                

                #if not toolTemplate == 'None':

                #    shutil.copyfile( os.path.join( 'src', 'template_documents', toolTemplate ), os.path.join( newNodePath, 'project', str( text + '.' + '0000' + os.path.splitext( toolTemplate )[ 1 ] ) ) )


                
                
                #print ET.tostring( propertyNode ) 
                #if not os.path.exists( propertyNodePath ): 
                xmlDoc = open( propertyNodePath, 'w' )
                 
                #print ET.tostring( propertyNode )
                
                xmlDoc.write( '<?xml version="1.0"?>' )
                xmlDoc.write( ET.tostring( propertyNode ) )
                #ET.ElementTree( propertyNode ).write( xmlDoc )
                #tree.write( xmlDoc )
                
                
                xmlDoc.close()
                
                newNode = node( self.mainWindow, self, propertyNodePath )
                newNode.addText( self, newSaverName )

            else:
                print 'asset saver already exists'

        return callback



        '''
        #newNodePath = os.path.join( str( projectsRoot ), str( currentContent ), str( text ) )
                
                
                
#                 if tabIndex == 0:
#                     newNodePath = os.path.join( str( currentContent ), str( text ) )
#             
#                 elif tabIndex == 1:
#                     newNodePath = os.path.join( str( currentContent ), str( text ) )
                
                #print newNodePath
                propertyNode = ET.Element( 'propertyNode' )
                
                #print pos.x()
                #print pos.y()
                
                posX = str( int( float( round( pos.x() ) ) ) )
                posY = str( int( float( round( pos.y() ) ) ) )

                ET.SubElement( propertyNode, 'node', { 'positionX':posX, 'positionY':posY } )
                #ET.SubElement( propertyNode, 'positionX', { 'value':posX } )
                #ET.SubElement( propertyNode, 'positionY', { 'value':posY } )

                #print  toolFamily, toolVendor, toolVersion, toolArch

                ET.SubElement( propertyNode, 'task', { 'family':toolFamily, 'vendor':toolVendor, 'version':toolVersion, 'arch':toolArch, 'nodetask':toolTask } )




                

                
                
                
                tree = ET.ElementTree( propertyNode )
                
                propertyNodePath = os.path.join( newNodePath, 'propertyNode.xml' )
                #print propertyNodePath
                

                os.makedirs( newNodePath, mode=0777 )
                os.makedirs( os.path.join( newNodePath, 'project' ), mode=0777 )
                os.makedirs( os.path.join( newNodePath, 'output' ), mode=0777 )
                os.makedirs( os.path.join( newNodePath, 'live' ), mode=0777 )
                os.makedirs( os.path.join( newNodePath, 'input' ), mode=0777 )
                print os.path.exists( newNodePath )

                for toolDirectory in toolDirectories:
                    os.makedirs( os.path.join( newNodePath, 'project', toolDirectory ), mode=0777 )

                

                if not toolTemplate == 'None':

                    shutil.copyfile( os.path.join( 'src', 'template_documents', toolTemplate ), os.path.join( newNodePath, 'project', str( text + '.' + '0000' + os.path.splitext( toolTemplate )[ 1 ] ) ) )


                
                
                #print ET.tostring( propertyNode ) 
                #if not os.path.exists( propertyNodePath ): 
                xmlDoc = open( propertyNodePath, 'w' )
                 
                #print ET.tostring( propertyNode )
                
                xmlDoc.write( '<?xml version="1.0"?>' )
                xmlDoc.write( ET.tostring( propertyNode ) )
                #ET.ElementTree( propertyNode ).write( xmlDoc )
                #tree.write( xmlDoc )
                
                
                xmlDoc.close()
                
                newNode = node( self, propertyNodePath )
                newNode.addText( self, str( text ) )

                print toolDefaultOutputList

                for toolDefaultOutput in toolDefaultOutputList:
                    print toolDefaultOutput
                    self.newOutputAuto( newNode, toolDefaultOutput )
        '''



        pass

        
    def newNodeDialog( self, pos ):
        def callback():
            
            #projectsRoot = str( self.mainWindow.getProjectsRoot() )
            currentContent = str( self.mainWindow.getCurrentContent() )
            currentProject = str( self.mainWindow.projectComboBox.currentText() )
            tools = self.mainWindow.getTools()
            tasks = self.mainWindow.getTasks()
            #tabIndex = self.mainWindow.assetsShotsTabWidget.currentIndex()
            #index = self.projectComboBox.findText( indexText )
            
            #self.ui = loadUi( os.path.join( self.mainWindow.getPypelyneRoot(), 'ui', 'newNode.ui' ), self )

            #text, ok = QInputDialog.getText( self.mainWindow, 'create new node in %s' %currentProject, 'enter node name:' )
            #print os.getcwd()
            
            nodeDir = os.path.join( self.projectsRoot, currentContent )
            
            #print 'root: %s' %projectsRoot
            #print 'content: %s' %currentContent
            #print 'nodes: %s' %currentNodes
            #print nodeDir
            
            #print tools
            text, ok, toolIndex, taskIndex = newNodeUI.getNewNodeData( nodeDir, tools, tasks, self.mainWindow )

            try:
                toolNode = tools[ toolIndex ]
                print toolNode
            except:
                #print 'deadline job'
                toolNode = ('Thinkbox Software Deadline 5.2 x64', ['"deadlinecommand" -SubmitCommandLineJob'], 'DDL', 'Thinkbox Software', 'Deadline', '5.2', 'x64', 'None', [], [])
            taskNode = tasks[ taskIndex ]
            
            #print text, ok, toolIndex, taskIndex
            #print tools[ toolIndex ]

            #print taskNode

            toolTask = taskNode[ 2 ][ 1 ]

            toolVendor = toolNode[ 3 ]
            toolFamily = toolNode[ 4 ]
            toolVersion = toolNode[ 5 ]
            toolArch = toolNode[ 6 ]
            toolTemplate = toolNode[ 7 ]
            toolDirectories = toolNode[ 8 ]
            toolDefaultOutputList = toolNode[ 9 ]
            toolFlags = toolNode[ 10 ]
            workspaceTemplate = toolNode[ 11 ]

            #print  toolFamily, toolVendor, toolVersion, toolArch, toolTask, toolTemplates, toolDirectories, toolDefaultOutputList
            
            
            
            #print text, ok
 
            if ok:
                
#                 #os.makedirs( newContent, mode=0777 )
                newNodePath = os.path.join( str( self.projectsRoot ), str( currentContent ), str( text ) )
                
                
                
#                 if tabIndex == 0:
#                     newNodePath = os.path.join( str( currentContent ), str( text ) )
#             
#                 elif tabIndex == 1:
#                     newNodePath = os.path.join( str( currentContent ), str( text ) )
                
                #print newNodePath
                propertyNode = ET.Element( 'propertyNode' )
                
                #print pos.x()
                #print pos.y()
                
                posX = str( int( float( round( pos.x() ) ) ) )
                posY = str( int( float( round( pos.y() ) ) ) )

                ET.SubElement( propertyNode, 'node', { 'positionX':posX, 'positionY':posY } )
                #ET.SubElement( propertyNode, 'positionX', { 'value':posX } )
                #ET.SubElement( propertyNode, 'positionY', { 'value':posY } )

                #print  toolFamily, toolVendor, toolVersion, toolArch

                ET.SubElement( propertyNode, 'task', { 'family':toolFamily, 'vendor':toolVendor, 'version':toolVersion, 'arch':toolArch, 'nodetask':toolTask } )




                

                
                
                
                tree = ET.ElementTree( propertyNode )
                
                propertyNodePath = os.path.join( newNodePath, 'propertyNode.xml' )
                #print propertyNodePath
                

                os.makedirs( newNodePath, mode=0777 )
                os.makedirs( os.path.join( newNodePath, 'project' ), mode=0777 )
                os.makedirs( os.path.join( newNodePath, 'output' ), mode=0777 )
                os.makedirs( os.path.join( newNodePath, 'live' ), mode=0777 )
                os.makedirs( os.path.join( newNodePath, 'input' ), mode=0777 )
                #print os.path.exists( newNodePath )

                for toolDirectory in toolDirectories:
                    os.makedirs( os.path.join( newNodePath, 'project', toolDirectory ), mode=0777 )

                

                if not toolTemplate == 'None':
                    #print toolTemplates

                    shutil.copyfile( os.path.join( 'src', 'template_documents', toolTemplate ), os.path.join( newNodePath, 'project', str( text + '.' + '0000' + os.path.splitext( toolTemplate )[ 1 ] ) ) )
                    #toolTemplates.remove( toolTemplates[ 0 ] )

                    if not workspaceTemplate == 'None':
                        print str( workspaceTemplate )
                        print str( workspaceTemplate ).split( '_' )
                        shutil.copyfile( os.path.join( 'src', 'template_documents', workspaceTemplate ), os.path.join( newNodePath, str( workspaceTemplate ).split( '_' )[ -1 ] ) )


                
                
                #print ET.tostring( propertyNode ) 
                #if not os.path.exists( propertyNodePath ): 
                xmlDoc = open( propertyNodePath, 'w' )
                 
                #print ET.tostring( propertyNode )
                
                xmlDoc.write( '<?xml version="1.0"?>' )
                xmlDoc.write( ET.tostring( propertyNode ) )
                #ET.ElementTree( propertyNode ).write( xmlDoc )
                #tree.write( xmlDoc )
                
                
                xmlDoc.close()
                
                newNode = node( self.mainWindow, self, propertyNodePath )
                newNode.addText( self, str( text ) )

                #print toolDefaultOutputList

                for toolDefaultOutput in toolDefaultOutputList:
                    #print toolDefaultOutput
                    self.newOutputAuto( newNode, toolDefaultOutput )
                    #self.newOutputDialog( newNode )
                
                

                #self.sendTextToBox( 'content created on filesystem: %s\n' %newContent )
                
                #self.mainWindow.getAssetContent()
                #self.mainWindow.getShotContent()
                
                

        return callback





    def removeObject( self, item ):
        reply = QMessageBox.warning( self.mainWindow, str( 'about to delete item' ), str( 'are you sure to \ndelete %s %s \nand its contents?' %( item.data( 2 ).toPyObject(), item.label ) ), QMessageBox.Yes | QMessageBox.No, QMessageBox.No )

        #print yes

        if reply == QMessageBox.Yes:

            if isinstance( item, node ):
                #print 'self.children() = %s' %self.children()
                #node.outputList
                tempOutputList = item.outputList
                #node.inputList
                tempInputList = item.inputList


                for output in tempOutputList:
                    try:
                        self.removeOutput( output )
                    except:
                        pass

                for input in tempInputList:
                    self.removeInput( input )


                del tempOutputList
                del tempInputList


                nodeRootDir = item.getNodeRootDir()


                if item.label.startswith( 'LDR' ):
                    #print 'deleting loader'
                    #print nodeRootDir
                    nodeRootDirContent = os.listdir( nodeRootDir )

                    #print nodeRootDirContent

                    for dir in nodeRootDirContent:
                        if os.path.islink( os.path.join( nodeRootDir, dir ) ):
                            os.remove( os.path.join( nodeRootDir, dir ) )
                            print os.path.join( nodeRootDir, dir ), 'removed'
                    shutil.rmtree( nodeRootDir )
                    self.removeItem( item )

                else:


                    #print 'nodeRootDir = %s' %nodeRootDir
                    shutil.rmtree( nodeRootDir )
                    self.removeItem( item )

                    #print 'self.children() = %s' %self.children()




            elif isinstance( item, portOutput ):
                self.removeOutput( item )




            elif isinstance( item, portInput ):
                ###
                #print 'shit'
                #print item.getInputDir()
                #print 'another shit'
                inputDir = item.getInputDir()

                #shutil.rmtree( inputDir ) #removes link and contents
                #os.unlink( inputDir ) #access denied error
                #os.remove( inputDir ) #access denied error
                try:
                    if self.currentPlatform == "Darwin":
                        os.unlink( inputDir )
                    elif self.currentPlatform == "Windows":
                        os.rmdir( inputDir )
                        #windows removes the contents of the connected output folder as well using shutil.rmtree :(((
                        #and if inputDir is not empty, it cannot remove the link/directory because it's not empty :(((
                        #shutil.rmtree( inputDir )
                except:
                    print 'cannot remove symlink 1234'

                #os.rmdir( inputDir )
                print 'here'
                self.removeInput( item )

                print 'and here'

    
    def removeObjectCallback( self, item ):
        def callback():
            self.removeObject( item )

        return callback
    
    def removeOutput( self, item ):
        #print item.parentItem().boundingRect()
        #need a copy of the actual list for the item count to stay consistent over the loop
        tempInputsList = list( item.inputs )
        for port in tempInputsList:
            #remove connection from objects and scene
            connectionLine = port.connection[ 0 ]
            self.removeItem( connectionLine )
            port.connection.remove( connectionLine )
             
            #remove input from output list in upstream node
            output = port.output[ 0 ]
            output.inputs.remove( port )
             
            #remove input in parentNode.inputs[]
            port.parentItem().inputs.remove( port )
            port.parentItem().incoming.remove( output )
            inputDir = port.getInputDir()
                
            #os.unlink( inputDir )
            try:
                if self.currentPlatform == "Darwin":
                    os.unlink( inputDir )
                elif self.currentPlatform == "Windows":
                    os.rmdir( inputDir )
            except:
                print 'cannot remove symlink 2345'
            self.removeItem( port )
            
                 
        
         
        del tempInputsList
        
        item.parentItem().outputs.remove( item )

        #if os.path.exists( os.path.join( item.getLiveDir, outputLabel ) )
        
        
        #outputLabel = item.getLabel()
        #nodeRootDir = item.parentItem().getNodeRootDir()
        #outputDir = os.path.join( str( nodeRootDir ), 'output', str( outputLabel ) )
        outputDir = item.getOutputDir()
        #print outputDir
        liveDir = item.getLiveDir()
        #print liveDir
        if not item.parentItem().label.startswith( 'LDR' ):
            if os.path.exists( liveDir ):
                #########
                os.unlink( liveDir )
            #print outputDir
            shutil.rmtree( outputDir )

            self.removeItem( item )
        
    def removeInput( self, item ):
        try:
            
            #remove connection from objects and scene
            self.removeItem( item.connection[ 0 ] )
            item.connection.remove( item.connection[ 0 ] )
            
            #remove input from output list in upstream node
            output = item.output[ 0 ]
            output.inputs.remove( item )
            
            #remove input in parentNode.inputs[]
            item.parentItem().inputs.remove( item )
            item.parentItem().incoming.remove( output )
            #item.parentItem().resize()
            self.removeItem( item )
        
        except:
            print 'port is input portal! mustn\'t delete!'
        
        
    def newNode( self, pos ):

        
        def callback():
            node( self.mainWindow, pos, self )
        return callback

    def printContextMenuAction( self, item ):
        def callback():
            pass
            # from http://stackoverflow.com/questions/6682688/python-dynamic-function-generation
            #print item
        return callback

    def mousePressEvent( self, event ):
        pos = event.scenePos()

        print 'pos = %s' %pos
        
        if event.button() == Qt.MidButton:
            print 'MidButton'
          
        elif event.button() == Qt.LeftButton:
            print 'LeftButton'
            item = self.itemAt( event.scenePos() )
            #print "item = %s" %item
            if event.button() == Qt.LeftButton and ( isinstance( item, portOutput ) ):
                self.line = QGraphicsLineItem( QLineF( event.scenePos(), event.scenePos() ) )
                self.addItem( self.line )
            elif event.button() == Qt.LeftButton and ( isinstance( item, portOutputButton ) ):
                #print 'is portOutputButton'
                #print item.parentItem()
                self.newOutputDialog( item.parentItem() )
                
            elif event.button() == Qt.LeftButton and ( isinstance( item, node ) ):
                pass
                #self.nodeSelect.emit( item )
                #print item
                #print item.getWidgetMenu()
                #print self.parentItem()
                #self.scene.nodeMenuArea.setWidget( self.widget )
            else:
                self.nodeDeselect.emit()
                #print 'deselect'
                
                

            modifiers = QApplication.keyboardModifiers()
            pos = event.scenePos()
            if modifiers == Qt.ControlModifier:
                print "Control + Click: (%d, %d)" % ( pos.x(), pos.y() ) 


            else:
                pass
                #print "Click: (%d, %d)" % (pos.x(), pos.y())

        elif event.button() == Qt.RightButton:
            print 'RightButton'

            self.contextMenu( pos )

        else:
            print 'def mousePressEvent problem'

        super( SceneView, self ).mousePressEvent( event )

        
    def mouseMoveEvent( self, event ):

        if self.line:

            newLine = QLineF( self.line.line().p1(), event.scenePos() )
            self.line.setLine( newLine )
        super( SceneView, self ).mouseMoveEvent(event)
        self.update()
        

    def mouseReleaseEvent( self, event ):
        #print 'mouseReleaseEvent'
        
        if self.line:
            try:
                startItems = self.items( self.line.line().p1() )
                parentNodeStartItem = startItems[ 0 ].parentItem()
            except:
                return

            if len( startItems ) and startItems[ 0 ] == self.line:
                #print "popping"
                #print "len( startItems ) = %i" %len( startItems )

                startItems.pop( 0 )
                #print "startItems popped = %s" %startItems
            
            endItems = self.items( self.line.line().p2() )
             
            if len( endItems ) and endItems[ 0 ] == self.line:
                #print "popping"
                #print "len( endItems ) = %i" %len( endItems )
                

                endItems.pop( 0 )
                #print "endItems popped = %s" %endItems
                
            self.removeItem( self.line )
            
            
            if ( isinstance( endItems[ 0 ], portInput ) ):
                
                parentNode = endItems[ 0 ].parentItem()
                
                if startItems[ 0 ] in endItems[ 0 ].parentItem().incoming:
                    
                    parentNode.sendFromNodeToBox( str( datetime.datetime.now() ) )
                    parentNode.sendFromNodeToBox( ':' + '\n' )
                    parentNode.sendFromNodeToBox( '--- this connection already exists, you dumbass' + '\n' )

                    
                elif startItems[ 0 ].parentItem() == endItems[ 0 ].parentItem():
                    parentNode.sendFromNodeToBox( str( datetime.datetime.now() ) )
                    parentNode.sendFromNodeToBox( ':' + '\n' )
                    parentNode.sendFromNodeToBox( '--- don\'t connect to itself, you moron' + '\n' )
                    
                elif len( endItems[ 0 ].connection ) == 0:
                    if os.path.basename( startItems[ 0 ].parentItem().getNodeRootDir() ).startswith( 'LDR' ) \
                                    and os.path.basename( endItems[ 0 ].parentItem().getNodeRootDir() ).startswith( 'SVR' ):
                        parentNode.sendFromNodeToBox( '--- don\'t connect loader to saver' + '\n' )
                        logging.info( 'tried to connect loader to saver, which is not possible' )
                    else:

                        #print "is an input :)"
                        connectionLine = bezierLine( self.mainWindow, self, startItems[ 0 ], endItems[ 0 ], QPainterPath( startItems[ 0 ].scenePos() ) )
                        #print "connectionLine = %s" %connectionLine
                        
                        endItems[ 0 ].parentItem().inputs.append( endItems[ 0 ] )
                        endItems[ 0 ].connection.append( connectionLine )
                        endItems[ 0 ].output.append( startItems[ 0 ] )
                        endItems[ 0 ].parentItem().incoming.append( startItems[ 0 ] )
                        startItems[ 0 ].inputs.append( endItems[ 0 ] )
                        
                        
                        
                        startItemRootDir = startItems[ 0 ].parentItem().getNodeRootDir()
                        endItemRootDir = endItems[ 0 ].parentItem().getNodeRootDir()
                        
                        #startItemOutputLabel = startItems[ 0 ].getLabel()
                        startItemOutputLabel = os.path.basename( startItems[ 0 ].getOutputDir() )
                        #print 'startItemOutputLabel', startItemOutputLabel
                        
                        #
                        #startItemOutputDir = os.path.join( str( startItemRootDir ), 'output', str( startItemOutputLabel ) )
                        startItemOutputDir = os.path.join( str( startItemRootDir ), 'live', str( startItemOutputLabel ) )
                        endItemInputDir = os.path.join( str( endItemRootDir ), 'input', str( startItemOutputLabel ) )
                        
                        #print 'startItemRootDir = %s' %startItemRootDir
                        #print 'startItemOutputLabel = %s' %startItemOutputLabel
                        #print 'endItemRootDir = %s' %endItemRootDir
                        
    #                     Return a relative filepath to path either from the current directory or from an optional start point.
    #                     >>> from os.path import relpath
    #                     >>> relpath('/usr/var/log/', '/usr/var')
    #                     'log'
    #                     >>> relpath('/usr/var/log/', '/usr/var/sad/')
    #                     '../log'
                        
                        #os.makedirs( endItemOutputDir, mode=0777 )


                        #projectsRoot = str( self.mainWindow.getProjectsRoot() )
                        currentContent = str( self.mainWindow.getCurrentContent() )
                        #currentProject = str( self.mainWindow.projectComboBox.currentText() )

                        #currentProjectRoot = os.path.join( projectsRoot, currentContent )
                        

    #                     #darwin:
    #                     os.unlink(currentDir)
    #                     os.symlink(self.newFolderFull, os.path.relpath(currentDir))  
                        cwd = os.getcwd()
                        dst = endItemInputDir
                        #src = os.sep.join( [ str( os.path.relpath( startItemOutputDir, os.path.dirname( dst ) ) ), 'current' ] )
                        #src = os.sep.join( [ str( os.path.relpath( startItemOutputDir, os.path.dirname( dst ) ) ) ] )
                        #print str( os.path.relpath( os.path.join( self.projectsRoot, currentContent ), os.path.dirname( dst ) ) )
                        
                        srcParentDirs = os.sep.join( [ str( os.path.relpath( self.projectsRoot, os.path.dirname( dst ) ) ) ] ) + os.sep
                        #print srcParentDirs


                        src = os.sep.join( [ str( os.path.relpath( startItemOutputDir, self.projectsRoot ) ) ] )
                        


                        #relPath = os.sep.join( [ str( src + os.sep + os.sep.join( [ str( os.path.relpath( dst, self.projectsRoot ) ) ] ) ) ] )
                        
                        relPath = os.sep.join( [ str( srcParentDirs + src ) ] )
                        #print relPath

                        #src + os.sep + os.sep.join( [ str( os.path.relpath( dst, self.projectsRoot ) ) ] )

                        #print str( os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) ) ).split( '.' )

                        #if len( str( os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) ) ).split( '.' ) ) == 4:

                        #print os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) )
                        #print os.path.dirname( os.path.dirname( startItemRootDir ) )

                        #if not len( startItemOutputLabel.split( '.' ) ) == 1:
                        #    startItemOutputLabel = startItemOutputLabel.split( '.' )[ 3 ]

                        if len( os.path.basename( dst ).split( '.' ) ) > 1:

                            #inputLink = os.path.dirname( dst ) + os.sep + os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) ) + '.' + os.path.basename( os.path.dirname( startItemRootDir ) ) + '.' + os.path.basename( startItemRootDir ) + '.' + os.path.basename( dst ).split( '.' )[ 3 ]
                            inputLink = os.path.dirname( dst ) + os.sep + os.path.basename( relPath )
                            
                        else:
                            inputLink = os.path.dirname( dst ) + os.sep + os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) ) + '.' + os.path.basename( os.path.dirname( startItemRootDir ) ) + '.' + os.path.basename( startItemRootDir ) + '.' + os.path.basename( dst )
                        #print inputLink
                        #print src
                        #print os.path.basename( dst )
                        #elif len( str( os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) ) ).split( '.' ) ) == 7:
                        #    inputLink = os.path.dirname( dst ) + os.sep + os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) )
                        #print 'inputLink = %s' %( inputLink )
                        #print 'inputLink = %s' %( inputLink )
                        if self.currentPlatform == "Darwin":
                            #cwd = os.getcwd()
                            #src = startItemOutputDir
                            #dst = endItemInputDir
                            #print 'asset = %s' %os.path.dirname( startItemRootDir )
                            #print 'node = %s' %startItemRootDir
                            #src = str(  ) + '.' + str( os.path.relpath( startItemOutputDir, os.path.dirname( dst ) ) )
                            #print str( os.path.dirname( dst ) )
                            #src = os.sep.join( [ str( os.path.relpath( startItemOutputDir, os.path.dirname( dst ) ) ), 'current' ] )
                            #src = os.path.basename( os.path.normpath( startItemOutputDir ) )
                            #dst = endItemOutputDir
                            #print cwd
                            #print src
                            #print os.path.dirname( dst ) + os.sep + os.path.basename( os.path.dirname( startItemRootDir ) ) + '.' + os.path.basename( startItemRootDir ) + '.' + os.path.basename( dst )
                            #'.'join( [ os.path.basename( startItemRootDir ), os.path.basename( dst ) ] )
                            #print os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) )
                            #inputLink = os.path.dirname( dst ) + os.sep + os.path.basename( os.path.dirname( os.path.dirname( startItemRootDir ) ) ) + '.' + os.path.basename( os.path.dirname( startItemRootDir ) ) + '.' + os.path.basename( startItemRootDir ) + '.' + os.path.basename( dst )
                            #print 'inputLink = %s' %inputLink
                            try:
                                #print src
                                #print inputLink

                                #print self.projectsRoot, relPath, inputLink, 

                                os.symlink( relPath, inputLink )
                            except:
                                pass
                            endItems[ 0 ].setInputDir( inputLink )
                            #print 'Darwin: endItems[ 0 ].getInputDir() = %s' %endItems[ 0 ].getInputDir()
                            
                            
    #                     #win:
    #                     os.removedirs(currentDir)
    #                     cmdstring = "mklink /D " + os.path.relpath(currentDir) + " " + self.newFolderFull
    #                     os.system(cmdstring)
                        elif self.currentPlatform == "Windows":
                            #dst = endItemInputDir
                            #src = os.sep.join( [ str( os.path.relpath( startItemOutputDir, os.path.dirname( dst ) ) ), 'current' ] )
                            cmdstring = "mklink /D " + inputLink + " " + src
                            #print 'Win cmdstring = %s' %( cmdstring )
                            os.chdir( os.path.dirname( endItemInputDir ) )
                            os.system( cmdstring )
                            os.chdir( cwd )
                            
                            endItems[ 0 ].setInputDir( inputLink )
                            #print 'Windows: endItems[ 0 ].getInputDir() = %s' %endItems[ 0 ].getInputDir()
                        

                        
                        
                        
                        self.addItem( connectionLine )
                        
                        

                        endItems[ 0 ].parentItem().newInput( self )

                else:
                                       
                    
                    parentNode.sendFromNodeToBox( str( datetime.datetime.now() ) )
                    parentNode.sendFromNodeToBox( ':' + '\n' )
                    parentNode.sendFromNodeToBox( '--- this input port is already in use. obviously.' + '\n' )
                    parentNode.sendFromNodeToBox( '--- your iq is dropping...' + '\n' )
                    
                    

                
            else:


                parentNodeStartItem = startItems[ 0 ].parentItem()
                

                parentNodeStartItem.sendFromNodeToBox( str( datetime.datetime.now() ) )
                parentNodeStartItem.sendFromNodeToBox( ':' + '\n' )
                parentNodeStartItem.sendFromNodeToBox( '--- endItem is not an input :(' + '\n' )
                parentNodeStartItem.sendFromNodeToBox( '--- no endItem chosen' + '\n' )

        
        
        self.line = None

        super( SceneView, self ).mouseReleaseEvent( event )