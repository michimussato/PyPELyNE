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

        #self.

        self.mainWindow = mainWindow
        self.exclusions = self.mainWindow.getExclusions()

        #self.scene = scene
        #self.mainwindow = self.scene.getMainWindow()
        self._outputs = self.mainWindow.getOutputs()

        
        self.portOutputColorItem = QColor( 0, 0, 0 )
        self.portOutputRingColorItem = QColor( 0, 0, 0 )

        #print node.getNodeRootDir()
        #print name
        #print os.path.join( node.getNodeRootDir(), 'output' )
        #self.outputDir = os.path.join( node.getNodeRootDir(), 'output', name )
        #print type( node.getNodeRootDir() )
        #print type( 'current' )
        #print type( name )
        #self.outputDir = os.path.normpath( os.path.join( node.getNodeRootDir(), 'output', str( os.sep + name ) ) )
        self.outputDir = os.path.normpath( os.path.join( node.getNodeRootDir(), 'output', name ) )
        self.liveDir = os.path.normpath( os.path.join( node.getNodeRootDir(), 'live', name ) )

        print self.outputDir
        print self.liveDir
        #print 'liveDir', self.liveDir
        #print 'outputDir', self.outputDir
        #print self.outputDir
        
        self.connectedTo = []
        
        self.inputs = []
        
#         print 'dir( node ) = %s' %dir( node )
        
#         if ( node.childrenBoundingRect().width() + 40 ) >= node.boundingRect().width():
#             #self.rect = QRectF( ( node.childrenBoundingRect().width() -40 ), -20, 20, 20 )
#             self.rect = QRectF( ( node.childrenBoundingRect().width() -30 ), ( ( 20 * ( increment + 1 ) ) + 10 ), 20, 20 )
#         else:
#             self.rect = QRectF( 50, ( ( 20 * ( increment + 1 ) ) + 10 ) , 20, 20 )
        
        #self.rect = QRectF( ( node.boundingRect().width() - 10 ), ( ( 20 * ( increment + 1 ) ) + 30 ), 20, 20 )
        
        #self.rect = QRectF( ( node.boundingRect().width() ), 10, 20, 20 )
        
        #self.connectedInput = []
        
        self.rect = QRectF( 0, 0, 20, 20 )
        
        self.setData( 0, name )
        
        
        
        
        #self.label = self.addText( node, self.data( 0 ).toPyObject() )
        self.label = None

        self.gradient = QLinearGradient( self.rect.topLeft(), self.rect.topRight() )

        #self.setPortOutputColor()
        
#         print 'node.boundingRect = %s' %node.boundingRect()
#         print 'node.childrenBoundingRect = %s' %node.childrenBoundingRect()
        
        #self.arrange( increment, node )


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
#         textPortOutput = QGraphicsTextItem( 'output id = %s' %random.randrange( 100000000000000 ), parent=self )
        textPortOutput.setDefaultTextColor( self.portOutputColorItem.darker( 250 ) )
        
        textPortOutput.setPos( QPointF( 0 - textPortOutput.boundingRect().width(), 0 ) )
        
    def boundingRect( self ):
        return self.rect

    def paint( self, painter, option, widget ):
        self.setPortOutputColor()
        #self.setZValue( 3 )
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
        
        #print 'portOutput.inputs = %s' %self.inputs
        
        #self.arrange( len( self.parentItem().outputList ), self.parentItem() )

    def setPortOutputColor( self ):
        
        #pass
        #self.gradient.setColorAt( 0, Qt.blue )
        #self.gradient.setColorAt( 1, Qt.green )

        #self.palette = QPalette
        

        if len( str( self.data( 0 ).toPyObject() ).split( '.' ) ) > 1:

            #print 'portOutput.label (split) = %s' %str( self.data( 0 ).toPyObject() ).split( '.' )[ 3 ].split( '__' )[ 0 ]

            self.nodeOutput = str( self.data( 0 ).toPyObject() ).split( '.' )[ 3 ].split( '__' )[ 0 ]

        else:

            #print 'portOutput.label = %s' %str( self.data( 0 ).toPyObject() ).split( '__' )

            self.nodeOutput = str( self.data( 0 ).toPyObject() ).split( '__' )[ 0 ]
        #print self.nodeOutput
        #print self._outputs

        
        #print self._tasks[ 0 ].index( ('value', 'modelling') )
        index = 0
        found = False
        for i in self._outputs:
            if found == False:
                
                for j in i:
                    if found == False:
                        #print j
                        #print i.index( filter( lambda n: n.get( 'value' ) == 'modelling', i )[ 0 ] )
                    #    if self.nodeTask in i:
                    #        print i
                        if [ item for item in j if self.nodeOutput in item and not 'mime' in item ]:
                            #print 'found'
                            found = True
                            outputIndex = index
                            #print item
                            #print index
                            #print self._outputs[ outputIndex ]
                            #print self._outputs[ outputIndex ][ 0 ][ 0 ][ 1 ]
                            self.portOutputColor = self._outputs[ outputIndex ][ 0 ][ 0 ][ 1 ]
                            #outputIndex = index
                            #print self._outputs[  ]
                            #self.taskColor = self._outputs[ index ][ 0 ][ 1 ]
                            break
                        #else:
                            #index += 1
                index += 1
            else:
                break

        #print index
        #self.pathColor = 
        #print self._outputs[ outputIndex ][ 0 ][ 0 ][ 1 ]

        #if not os.path.exists( self.liveDir ):
        #    self.portOutputRingColorItem.setNamedColor( '#FF0000' )
        if os.path.exists( self.liveDir ):

            if os.path.exists( os.path.join( self.outputDir, 'current' ) ):
                #
                if not os.path.basename( os.readlink( self.liveDir ) ) == os.readlink( os.path.join( self.outputDir, 'current' ) ):
                    if len( os.listdir( os.path.join( self.outputDir, 'current' ) ) ) <= 1:
                        #print 'empty output version found'
                        self.portOutputRingColorItem.setNamedColor( '#FF0000' )
                    else:
                        #print 'latest output version not published yet'
                        #print 'liveDir', os.path.basename( os.readlink( self.liveDir ) )
                        #print 'ourputDir', os.readlink( os.path.join( self.outputDir, 'current' ) )
                        self.portOutputRingColorItem.setNamedColor( '#FFFF00' )
                else:
                    #print 'latest output version is live'
                    self.portOutputRingColorItem.setNamedColor( '#00FF00' )

            else:
                #special case for loader/saver
                #print os.readlink(self.outputDir)
                #print os.readlink(self.liveDir)

                if not os.readlink( self.liveDir ) == os.readlink( self.outputDir ):
                    #right now, this case doesn't occur because if not is 
                    #always false: os.readlink( self.liveDir ) is always == os.readlink( self.outputDir )
                    if len( os.listdir( self.outputDir ) ) <= 1:
                        #print 'empty output version found'
                        self.portOutputRingColorItem.setNamedColor( '#FF0000' )
                    else:
                        #print 'latest output version not published yet'
                        #print 'liveDir', os.path.basename( os.readlink( self.liveDir ) )
                        #print 'ourputDir', os.readlink( os.path.join( self.outputDir, 'current' ) )
                        self.portOutputRingColorItem.setNamedColor( '#FF6000' )

                else:
                    #right now, this is the only case that occurs (if node is a loader)
                    #print 'latest output version is live'
                    self.portOutputRingColorItem.setNamedColor( '#00FF00' )
        else:
            #print 'output with no live data found'
            self.portOutputRingColorItem.setNamedColor( '#FFFFFF' )


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
        
        self.inputDir = None

        self.portInputColorItem = QColor( 0, 0, 0, 0 )
        self.gradient = QLinearGradient( self.rect.topLeft(), self.rect.topRight() )
        
        

    def getLabel( self ):
        return self.label
    
    def setInputDir( self, dir ):
#         nodeRootDir = self.node.getNodeRootDir()
#         print 'dir = %s' %dir
#         self.inputDir = os.sep.join( [ nodeRootDir, 'input', dir  ] )
        self.inputDir = dir
    
    def getInputDir( self ):
        #nodeRootDir = self.node.getNodeRootDir()
        #print self.inputDir
        return self.inputDir
        
    
    def addText( self, name ):
        textPortInput = QGraphicsTextItem( name, parent = self )
        self.label = name
        #nodeRootDir = self.parentItem().getNodeRootDir()
        #inputRootDir = os.path.join( nodeRootDir, 'input' )
        #self.inputDir = os.path.join( inputRootDir, self.label )
        textPortInput.setDefaultTextColor( Qt.black )
        
        textPortInput.setPos( QPointF( self.boundingRect().width(), 0 ) )
        
        #self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )
        
        
    def boundingRect( self ):
        return self.rect

    def paint( self, painter, option, widget ):
        painter.setRenderHint( QPainter.Antialiasing )
        pen = QPen( Qt.SolidLine )
        pen.setColor( Qt.black )
        pen.setWidth( 3 )

        
        
        #print 'portInput.connection = %s' %self.connection
        
        painter.setPen( pen )
        if len( self.connection ) == 0:
            painter.setBrush( QColor( 0, 0, 0, 0 ) )
            for i in self.icon:
                painter.drawLine( i )
        elif len( self.connection ) == 1:
            painter.setBrush( self.portInputColorItem )
        painter.drawEllipse( self.rect )
        
        #painter.drawLine( self.line1 )
        
        
        
#         self.opacity = 1.01 - ( ( 1.0 - ( self.currentPos.x() - self.initialPos.x() ) ) / 100 )
#         
#         self.setOpacity( self.opacity )
#         
#         #print self.opacity
#         
#         self.setOpacity( self.opacity )
#         
#         #print self
#         
#         print 'self.parentItem().inputs = %s' %self.parentItem().inputs
#         
#         print 'len( self.parentItem().inputList ) = %s' %len( self.parentItem().inputList )
#         print 'self.parentItem().inputList = %s' %self.parentItem().inputList
#         
#         if self.opacity <= 0:
#             
#             #print 'hallo'
#             self.parentItem().inputs = self.parentItem().inputs - 1
#             self.parentItem().inputList.remove( self )
#             self.scene.removeItem( self )
#             #print 'self.parentItem().inputs = %s' %self.parentItem().inputs
#         
#         #self.setPos( self.initialPos )


class portOutputButton( QGraphicsItem ):
    def __init__( self, node, name, mainWindow ):
        super( portOutputButton, self ).__init__( None )
        #node.resizeWidth()

        self.mainWindow = mainWindow
        self.setFlags( QGraphicsItem.ItemIsSelectable )
#         if ( node.childrenBoundingRect().width() + 40 ) >= node.boundingRect().width():
#             self.rect = QRectF( ( node.childrenBoundingRect().width() + 20 ), 10, 20, 20 )
#         else:
#             self.rect = QRectF( 140, 10, 20, 20 )
#         print 'node.boundingRect before = %s' %node.boundingRect()
#         print 'node.childrenBoundingRect before = %s' %node.childrenBoundingRect()
        self.rect = QRectF( 0, 0, 20, 20 )
        #self.label = self.addText( node, scene, name )
        
#         print 'node.boundingRect after = %s' %node.boundingRect()
#         print 'node.childrenBoundingRect after = %s' %node.childrenBoundingRect()
        
        #self.line1 = QLineF( node.boundingRect().width() - ( self.boundingRect().width() / 2 ), self.boundingRect().height() * 0, self.boundingRect().width(), self.boundingRect().height() * 0 )
        self.icon = []
        self.icon.append( QLine( 10, 6, 10, 14 ) )
        self.icon.append( QLine( 6, 10, 14, 10 ) )
        #self.line1.setParentItem( self )
        
        
        #self.setPos( node.boundingRect().width() - self.boundingRect().width(), self.boundingRect().height() * 0 )
        
        
    def addText( self, node, name ):
        item = QGraphicsTextItem( 'port = %s' %name, parent = self )
        item.setDefaultTextColor( Qt.black )
        item.setPos( QPointF( ( ( node.childrenBoundingRect().width() ) - item.boundingRect().width() ) - 30, 30 ) )
#         item.setPos( QPointF( node.boundingRect().width() - ( textPortOutput.boundingRect().width() ) - 10, ( ( 20 * ( node.outputs + 1 ) ) + 10 ) ) )
        
        #scene.addItem( item )
        
        

        
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


        
    

        
        
        