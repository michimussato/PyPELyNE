'''
Created on Dec 15, 2014

@author: michaelmussato
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import random, os


    
    

class portOutput( QGraphicsItem ):
    def __init__( self, node, name, mainWindow ):
        super( portOutput, self ).__init__( None )

        self.setFlags( QGraphicsItem.ItemIsSelectable )

        self.mainWindow = mainWindow
        #print mainWindow.exclusions
        self.exclusions = self.mainWindow.getExclusions()
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.projectsRoot = self.mainWindow.getProjectsRoot()

        self.node = node

        self._outputs = self.mainWindow.getOutputs()

        self.portOutputColorItem = QColor( 0, 0, 0 )
        self.portOutputRingColorItem = QColor( 0, 0, 0 )

        self.outputDir = os.path.normpath( os.path.join( node.getNodeRootDir(), 'output', name ) )
        self.liveDir = os.path.normpath( os.path.join( node.getNodeRootDir(), 'live', name ) )
        self.nodeRoot = self.node.getNodeRootDir()
        self.nodeProject = self.node.getNodeProject()

        #print self.outputDir
        #print self.liveDir

        self.outputColorOnline = '#00FF00'
        self.outputColorNearline = '#FFFF00'
        self.outputColorEmpty = '#FF0000'
        self.outputcolorNoLive = '#FFFFFF'
        
        self.connectedTo = []
        
        self.inputs = []
        
        self.rect = QRectF( 0, 0, 20, 20 )
        
        self.setData( 0, name )
        self.setData( 2, 'output' )

        self.label = None

        self.gradient = QLinearGradient( self.rect.topLeft(), self.rect.topRight() )

    def getOutputRootDir( self ):
        return self.nodeRoot

    def getOutputProjectDir( self ):
        return self.nodeProject

    def getOutputDir( self ):
        return self.outputDir

    def getLiveDir( self ):
        return self.liveDir
        
    def arrange( self, node ):
        self.setPos( node.boundingRect().width() - self.rect.width(), ( ( self.boundingRect().height() * ( len( node.outputList ) + 1 ) ) ) )
        
    def getLabel( self ):
        return self.label
    
    def addText( self, node, name ):
        
        textPortOutput = QGraphicsTextItem( str( name ), parent = self )
        self.label = name

        textPortOutput.setDefaultTextColor( self.portOutputColorItem.darker( 250 ) )
        
        textPortOutput.setPos( QPointF( 0 - textPortOutput.boundingRect().width(), 0 ) )
        
    def boundingRect( self ):
        return self.rect

    def paint( self, painter, option, widget ):
        self.setPortOutputColor()
        painter.setRenderHint( QPainter.Antialiasing )
        pen = QPen( Qt.SolidLine )
        pen.setColor( Qt.black )
        pen.setWidth( 3 )

        self.gradient.setColorAt( 0, self.portOutputRingColorItem )
        self.gradient.setColorAt( 0.3, self.portOutputRingColorItem )
        self.gradient.setColorAt( 0.4, self.portOutputColorItem )
        self.gradient.setColorAt( 1, self.portOutputColorItem )

        painter.setPen( pen )

        painter.setBrush( self.gradient )

        painter.drawEllipse( self.rect )

    def setPortOutputColor( self ):



        if len( str( self.data( 0 ).toPyObject() ).split( '.' ) ) > 1:
            self.nodeOutput = str( self.data( 0 ).toPyObject() ).split( '.' )[ 3 ].split( '__' )[ 0 ]

        else:
            self.nodeOutput = str( self.data( 0 ).toPyObject() ).split( '__' )[ 0 ]

        index = 0
        found = False
        for i in self._outputs:
            if found == False:
                
                for j in i:
                    if found == False:
                        if [ item for item in j if self.nodeOutput in item and not 'mime' in item ]:
                            found = True
                            outputIndex = index

                            self.portOutputColor = self._outputs[ outputIndex ][ 0 ][ 0 ][ 1 ]

                            break
                index += 1
            else:
                break

        if os.path.exists( self.liveDir ):

            if os.path.exists( os.path.join( self.outputDir, 'current' ) ):
                #
                if not os.path.basename( os.readlink( self.liveDir ) ) == os.readlink( os.path.join( self.outputDir, 'current' ) ):
                    path = os.path.join( self.outputDir, 'current' )
                    content = os.listdir( path )
                    for exclusion in self.exclusions:
                        if exclusion in content:
                            content.remove( exclusion )
                            try:
                                os.remove( os.path.join( path, exclusion ) )
                                print 'exclusion removed: %s' %( os.path.join( path, exclusion ) )
                            except:
                                print 'could not remove: %s' %( os.path.join( path, exclusion ) )
                    if len( content ) <= 1:
                        self.portOutputRingColorItem.setNamedColor( self.outputColorEmpty )
                    else:
                        self.portOutputRingColorItem.setNamedColor( self.outputColorNearline )
                else:
                    self.portOutputRingColorItem.setNamedColor( self.outputColorOnline )

            else:
                outputName = os.path.basename( os.path.abspath( os.readlink( self.liveDir ) ) )
                srcPath = os.path.dirname( os.path.dirname( os.path.abspath( os.readlink( self.liveDir ) ) ) )[ 1: ]

                #print os.path.basename( os.path.join( srcPath, 'live', outputName ) )
                #print self.projectsRoot
                #print os.path.join( self.projectsRoot, srcPath, 'output', outputName, 'current' )

                if not os.readlink( os.path.join( self.projectsRoot, srcPath, 'output', outputName, 'current' ) ) == os.path.basename( os.readlink( os.path.join( self.projectsRoot, srcPath, 'live', outputName ) ) ):
                    path = os.path.join( self.projectsRoot, srcPath, 'output', outputName, 'current' )
                    content = os.listdir( path )
                    for exclusion in self.exclusions:
                        if exclusion in content:
                            content.remove( exclusion )
                            try:
                                os.remove( os.path.join( path, exclusion ) )
                                print 'exclusion removed: %s' %( os.path.join( path, exclusion ) )
                            except:
                                print 'could not remove: %s' %( os.path.join( path, exclusion ) )

                    if len( content ) <= 1:
                        self.portOutputRingColorItem.setNamedColor( self.outputColorEmpty )
                    else:
                        self.portOutputRingColorItem.setNamedColor( self.outputColorNearline )

                else:
                    self.portOutputRingColorItem.setNamedColor( self.outputColorOnline )
        else:
            #output with no live data found
            self.portOutputRingColorItem.setNamedColor( self.outputcolorNoLive )

        self.portOutputColorItem.setNamedColor( self.portOutputColor )



class portInput( QGraphicsItem ):
    def __init__( self, node, scene, mainWindow ):
        super( portInput, self ).__init__( None )
        self.setFlags( QGraphicsItem.ItemIsSelectable )

        self.mainWindow = mainWindow
        
        self.scene = scene
        self.node = node

        self.rect = QRectF( 0, 0, 20, 20 )
        
        self.connection = []
        self.output = []
        
        self.setPos( 0, 0 )
        

        self.icon = []
        self.icon.append( QLine( 10, 14, 6, 10 ) )
        self.icon.append( QLine( 10, 14, 14, 10 ) )
        
        self.label = None
        self.setData( 2, 'input' )
        
        self.inputDir = None

        self.portInputColorItem = QColor( 0, 0, 0, 0 )
        self.gradient = QLinearGradient( self.rect.topLeft(), self.rect.topRight() )
        
        

    def getLabel( self ):
        return self.label
    
    def setInputDir( self, dir ):
        self.inputDir = dir
    
    def getInputDir( self ):
        return self.inputDir
        
    
    def addText( self, name ):
        textPortInput = QGraphicsTextItem( name, parent = self )
        self.label = name
        textPortInput.setDefaultTextColor( Qt.black )
        
        textPortInput.setPos( QPointF( self.boundingRect().width(), 0 ) )


    def boundingRect( self ):
        return self.rect

    def paint( self, painter, option, widget ):
        painter.setRenderHint( QPainter.Antialiasing )
        pen = QPen( Qt.SolidLine )
        pen.setColor( Qt.black )
        pen.setWidth( 3 )
        
        painter.setPen( pen )
        if len( self.connection ) == 0:
            painter.setBrush( QColor( 0, 0, 0, 0 ) )
            for i in self.icon:
                painter.drawLine( i )
        elif len( self.connection ) == 1:
            painter.setBrush( self.portInputColorItem )
        painter.drawEllipse( self.rect )


class portOutputButton( QGraphicsItem ):
    def __init__( self, node, name, mainWindow ):
        super( portOutputButton, self ).__init__( None )

        self.mainWindow = mainWindow
        self.setFlags( QGraphicsItem.ItemIsSelectable )
        self.rect = QRectF( 0, 0, 20, 20 )
        self.icon = []
        self.icon.append( QLine( 10, 6, 10, 14 ) )
        self.icon.append( QLine( 6, 10, 14, 10 ) )


    def addText( self, node, name ):
        item = QGraphicsTextItem( 'port = %s' %name, parent = self )
        item.setDefaultTextColor( Qt.black )
        item.setPos( QPointF( ( ( node.childrenBoundingRect().width() ) - item.boundingRect().width() ) - 30, 30 ) )

        
    def boundingRect( self ):
        return self.rect

    def paint( self, painter, option, widget ):
        painter.setRenderHint( QPainter.Antialiasing )
        pen = QPen( Qt.SolidLine )
        pen.setColor( Qt.black )
        pen.setWidth( 3 )

        painter.setPen( pen )
        painter.setBrush( QColor( 0, 0, 0, 0 ) )
        painter.drawEllipse( self.rect )
        for i in self.icon:
            painter.drawLine( i )
        
        self.setPos( self.parentItem().boundingRect().width() - self.boundingRect().width(), self.boundingRect().height() * 0 )


