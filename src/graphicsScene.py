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

import shutil, os, subprocess

# class Signals( QObject ):
#     trigger = pyqtSignal( str )

class SceneView( QGraphicsScene ):
    textMessage = pyqtSignal( str )
    nodeSelect = pyqtSignal( object )
    nodeDeselect = pyqtSignal()
    
    def __init__( self, mainWindow, parent=None ):
        super( SceneView, self ).__init__( parent )

        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.currentPlatform = self.mainWindow.getCurrentPlatform()
        self.projectsRoot = str( self.mainWindow.getProjectsRoot() )

        self.exclusions = self.mainWindow.getExclusions()
        self.imageExtensions = self.mainWindow.getImageExtensions()
        self.movieExtensions = self.mainWindow.getMovieExtensions()
        self.sequenceExec = self.mainWindow.getSequenceExec()

        self.line = None
        rect = self.setSceneRect( QRectF( 0, 0, 0, 0 ) )
        
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

        #icon = QIcon
        
        objectClicked = self.itemAt( pos )
        
        items = []

        #self.menu.addMenu( 'add item' )
        
        self.menu.addAction( 'node', self.newNodeDialog( pos ) )
        self.menu.addAction( 'loader', self.newLoaderDialog( pos ) )
        self.menu.addAction( 'saver', self.newSaverDialog( pos ) )
        
        
        try:
            if isinstance( objectClicked, portInput ):
                #items.append( 'delete this input' )
                self.menu.addAction( 'delete this input', self.removeObjectCallback( objectClicked ) )
                self.menuPathOps = self.menu.addMenu( 'clipboard' )


                inputLabel = objectClicked.getLabel()
                inputDir = objectClicked.getInputDir()

                outputNode = objectClicked.parentItem()
                outputNodeRootDir = outputNode.getNodeRootDir()

                self.menuPathOps.addAction( 'copy input name', self.copyToClipboardCallback( inputLabel ) )
                self.menuPathOps.addAction( 'copy absolute input path',  self.copyToClipboardCallback( os.path.join( inputDir, inputLabel ) ) )
                self.menuPathOps.addAction( 'copy relative input path',  self.copyToClipboardCallback( os.path.relpath( os.path.join( inputDir, inputLabel ), os.path.join( outputNodeRootDir ) ) ) )

        except:
            pass


        #try:
        if isinstance( objectClicked, portOutput ):
            #items.append( 'delete this output' )
            self.menu.addAction( 'delete this output', self.removeObjectCallback( objectClicked ) )




            self.menuVersion = self.menu.addMenu( 'versions' )
            self.menuPathOps = self.menu.addMenu( 'clipboard' )

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


            versions = self.getVersions( outputDir )
            #print outputDir

            self.menuVersion.addAction( 'open output directory', lambda: self.mainWindow.locateContent( outputDir ) )

            #self.menuVersion.addAction( 'cleanup', lambda: self.foo( 'cleanup' ) )

            

            self.menuVersion.addAction( 'create new version', self.createNewVersionCallback( outputDir ) )
            self.menuVersion.addSeparator()

            #self.menuMakeLive = self.menuVersion.addMenu( 'make live' )

            #try:
            #    print os.path.exists( liveDir )
            #except:
            #    raise 'shizzle'

            self.menuPathOps.addAction( 'copy output name', self.copyToClipboardCallback( outputLabel ) )
            self.menuPathOps.addAction( 'copy absolute output path',  self.copyToClipboardCallback( os.path.join( outputDir, 'current', outputLabel ) ) )
            self.menuPathOps.addAction( 'copy relative output path',  self.copyToClipboardCallback( os.path.relpath( os.path.join( outputDir, 'current', outputLabel ), os.path.join( outputNodeRootDir ) ) ) )


            if os.path.exists( liveDir ):

                #liveVersion = os.path.basename( os.readlink( liveDir ) )


                #self.menuPathOps.addAction( 'to clipboard 1234', self.copyToClipboardCallback( '1234' ) )
                #self.menuPathOps.addAction( 'to clipboard 5678', self.copyToClipboardCallback( '5678' ) )
                #self.menuPathOps.addAction( 'copy relative path', self.foo(  ) )
                #self.menuPathOps()

                self.menuVersion.addAction( 'remove pipe', self.unmakeLiveCallback( liveDir ) )
                #print 'added'
                self.menuVersion.addSeparator()

            
            for version in versions:
                if not version == 'current' and not version in self.exclusions:

                    versionPath = os.path.join( outputDir, version )
                    print versionPath

                    outputDirContent = os.listdir( versionPath )
                    outputDirContent.remove( outputLabel )

                    menuMakeLive = self.menuVersion.addMenu( version )

                    if os.path.exists( liveDir ):
                        if os.path.basename( os.readlink( liveDir ) ) == version:
                            menuMakeLive.setIcon( QIcon( 'src/icons/dotActive.png' ) )
                        else:
                            menuMakeLive.setIcon( QIcon( 'src/icons/dotInactive.png' ) )
                    else:
                        menuMakeLive.setIcon( QIcon( 'src/icons/dotInactive.png' ) )

                    #print 'here we are'

                    if outputLabel.startswith( 'SEQ' ) or outputLabel.startswith( 'TEX' ) or outputLabel.startswith( 'PLB' ):
                        for exclusion in self.exclusions:
                            try:
                                outputDirContent.remove( exclusion )
                            except:
                                pass
                        try:
                            menuMakeLive.addAction( 'view', self.viewVersion( os.path.join( versionPath, outputDirContent[ 0 ] ) ) )
                            try:
                                menuMakeLive.addAction( 'compare to live', self.compareVersion( os.path.join( versionPath, outputDirContent[ 0 ] ), os.path.join( liveDir, outputDirContent[ 0 ] ) ) )
                                menuMakeLive.addAction( 'difference to live', self.differenceVersion( os.path.join( versionPath, outputDirContent[ 0 ] ), os.path.join( liveDir, outputDirContent[ 0 ] ) ) )
                            except:
                                print 'compare/difference to live version not possible'
                        except:
                            print 'not possible to view SEQ. emty?'

                        #menuMakeLive.addAction( 'compare to live', self.compareVersion( os.path.join( outputDir, version, outputDirContent[ 0 ] ), os.path.join( liveDir, outputDirContent[ 0 ] ) ) )


                        #self.versionMenu.addAction( 'view live', self.viewLive( os.path.join( liveDir, liveDirContent[ 0 ] ) ) )

                    menuMakeLive.addAction( 'open directory', self.mainWindow.locateContentCallback( versionPath ) )

                    deleteVersionAction = menuMakeLive.addAction( 'delete version', self.deleteContentCallback( versionPath ) )

                    makeCurrentAction = menuMakeLive.addAction( 'make current', self.makeCurrentCallback( versionPath ) )

                    if os.path.join( outputDir, version ) == os.path.join( outputDir, os.readlink( os.path.join( outputDir, 'current' ) ) ):
                        deleteVersionAction.setEnabled( False )
                    else:
                        deleteVersionAction.setEnabled( True )



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

                    if versionPath == os.path.join( outputDir, os.path.basename( os.readlink( os.path.join( outputDir, 'current' ) ) ) ):
                        makeCurrentAction.setEnabled( False )

                
        #except:
        #    print 'not working'
            #pass

        try:
            if isinstance( objectClicked, node ) or isinstance( objectClicked.parentItem(), node ) or isinstance( objectClicked.parentItem().parentItem(), node ):
                if isinstance( objectClicked, node ):
                    if not os.path.exists( os.path.join( objectClicked.getNodeRootDir(), 'locked' ) ):
                        self.menu.addAction( 'delete this node', self.removeObjectCallback( objectClicked ) )
                    self.menu.addAction( 'clone', lambda: self.cloneNodeCallback( objectClicked ) )
                    #self.menu.addAction( 'none', lambda: None )
                    #items.append( 'delete this node' )
                    #print objectClicked.getNodeRootDir()

                    #location = self.mainWindow.locateContent( objectClicked.getNodeRootDir( objectClicked ) )

                    self.menu.addAction( 'open node directory', lambda: self.mainWindow.locateContent( objectClicked.getNodeRootDir() ) )


                elif isinstance( objectClicked.parentItem(), node ):
                    #print os.path.join( objectClicked.parentItem().getNodeRootDir(), 'locked' )
                    if not os.path.exists( os.path.join( objectClicked.parentItem().getNodeRootDir(), 'locked' ) ):
                        self.menu.addAction( 'delete this node', self.removeObjectCallback( objectClicked.parentItem() ) )
                    self.menu.addAction( 'clone', lambda: self.cloneNodeCallback( objectClicked.parentItem() ) )
                    #print objectClicked.parentItem().getNodeRootDir()

                    #location = self.mainWindow.locateContent( objectClicked.parentItem().getNodeRootDir( objectClicked.parentItem() ) )

                    self.menu.addAction( 'open node directory', lambda: self.mainWindow.locateContent( objectClicked.parentItem().getNodeRootDir() ) )

                elif isinstance( objectClicked.parentItem().parentItem(), node ):
                    if not os.path.exists( os.path.join( objectClicked.parentItem().parentItem(), node.getNodeRootDir(), 'locked' ) ):
                        self.menu.addAction( 'delete this node', self.removeObjectCallback( objectClicked.parentItem().parentItem() ) )
                    self.menu.addAction( 'clone', lambda: self.cloneNodeCallback( objectClicked.parentItem().parentItem() ) )
                    #print objectClicked.parentItem().getNodeRootDir()

                    #location = self.mainWindow.locateContent( objectClicked.parentItem().getNodeRootDir( objectClicked.parentItem() ) )

                    self.menu.addAction( 'open node directory', lambda: self.mainWindow.locateContent( objectClicked.parentItem().parentItem().getNodeRootDir() ) )

        except:
            #print 'fuuuuuuuuck'
            pass

        self.menu.move( QCursor.pos() )
        self.menu.show()

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

            os.symlink( os.path.relpath( versionDir, liveDir ), outputDir )

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

            cmdstring = "mklink /D " + os.path.join( os.path.dirname( currentDir ), 'current' ) + " " + currentDir
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
                output = node.newOutput( self, str( text ) )
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

            ok, loaderName, sourceSaverLocation = newLoaderUI.getNewLoaderData( activeItemPath, self.mainWindow )

            if ok:

                #newLoaderName = loaderName

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
                #print toolNode
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

            #print  toolFamily, toolVendor, toolVersion, toolArch, toolTask, toolTemplate, toolDirectories, toolDefaultOutputList
            
            
            
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

        reply = QMessageBox.warning( self.mainWindow, 'about to delete item', str( 'are you sure to delete %s item and its contents?' %( item.data( 0 ).toPyObject() ) ), QMessageBox.Yes | QMessageBox.No, QMessageBox.No )

        #print yes

        if reply == QMessageBox.Yes:

            if isinstance( item, node ) :

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
                self.removeInput( item )

    
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
        
        
        outputLabel = item.getLabel()
        nodeRootDir = item.parentItem().getNodeRootDir()
        outputDir = os.path.join( str( nodeRootDir ), 'output', str( outputLabel ) )
        #print outputDir
        shutil.rmtree( outputDir )
        #item.parentItem().resize()
        #print item.parentItem().boundingRect()
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
            #newNode = node( pos, self )
            #self.nodeClicked.connect( self.test )
            #newNode.nodeClicked.connect( self.test )
            #newNode.connect(  )
            #newNode.setWidgetMenu()
            #newNode.connect( self.nodeWidget )
            #newNode.signals.connect( self.signals.emit )
            #newNode.nodeCreatedInScene.emit()
            #newNode.clickedSignal.connect( self.nodeClicked.emit )
            #newNode.clickedSignal.connect( self.categoryItemClicked.emit )
 
             
        return callback
        
        
    
    def printContextMenuAction( self, item ):
        def callback():
            pass
            # from http://stackoverflow.com/questions/6682688/python-dynamic-function-generation
            #print item
        return callback
        
    

                
        #return callback
    '''
    def mouseDoubleClickEvent( self, event ):
        print 'double click'

    '''

    def mousePressEvent( self, event ):
        
        #print self.sceneRect()
        #rect = self.setSceneRect( self.itemsBoundingRect() )
        #print self.sceneRect()
        
        #self.nodeDeselect.emit()

        
        #print 'mousePressEvent'
        
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
                
            try:
                print "startItems[ 0 ] = %s" %startItems[ 0 ]
            except:
                print "no startItems[ 0 ]"
            
            endItems = self.items( self.line.line().p2() )
             
            if len( endItems ) and endItems[ 0 ] == self.line:
                #print "popping"
                #print "len( endItems ) = %i" %len( endItems )
                

                endItems.pop( 0 )
                #print "endItems popped = %s" %endItems
                
            try:
                print "endItems[ 0 ] = %s" %endItems[ 0 ]
                
            except:
                print "no endItems[ 0 ]"
                
            self.removeItem( self.line )
            
            
            if ( isinstance( endItems[ 0 ], portInput ) ):
                
                parentNode = endItems[ 0 ].parentItem()
                
                #print 'parentNode.childItems() = %s' %parentNode.childItems()
                
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