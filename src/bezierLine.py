'''
Created on Dec 15, 2014

@author: michaelmussato
'''

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

#class bezierLineGraphicsItem(  ):

#from circlesInOut import *

class bezierLine( QGraphicsPathItem ):
    def __init__( self, mainwindow, scene, startItem, endItem, *args, **kwargs ):
        super( bezierLine, self ).__init__( *args, **kwargs )
        
        #self.setFlags( QGraphicsItem.ItemIsSelectable )
        self.mainwindow = mainwindow
        self._outputs = self.mainwindow.getOutputs()
        self.startItemOutputDir = startItem.getOutputDir()
        self.startItemLiveDir = startItem.getLiveDir()
        #print self.outputs
        self.scene = scene
        self.pathItem = None
        self.myStartItem = startItem
        self.myEndItem = endItem
        self.myColor = Qt.black
        self.setZValue( -1.0 )

        #self.bezierGraphicsItem = QGraphicsPathItem()
        #self.bezierGraphicsItem.setAcceptHoverEvents( True )
        #self.bezierGraphicsItem.setAcceptTouchEvents( True )
        #self.scene.addItem( self.bezierGraphicsItem )

        self.setAcceptHoverEvents( True )
        self.setAcceptTouchEvents( True )

        #self.scene.addItem( self )

        #self.setCursor( Qt.OpenHandCursor )
        #self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )
        #self.
        #self
        self.setActive( True )
        #self.setBoundingRegionGranularity( 0.5 )
        self.setPen( QPen( self.myColor, 2 ) )
        self.getEndItem()
        #self.myEndItem.addText( str( startItem.parentItem().data( 0 ).toPyObject() )[-6:] + '.' + str( startItem.parentItem().outputList[ startItem.data( 0 ).toPyObject() ].data( 0 ).toPyObject() ) )
        #text = str( startItem.parentItem().getLabel() ) + '.' + str( startItem.getLabel() )
        self.label = str( startItem.getLabel() )
        self.myEndItem.addText( self.label )

        #self.dashPattern = QVector( []] )

        self.pathColorItem = QColor( 0, 0, 0 )
        self.setPathColor()
        #self.myEndItem.setInputDir( text )
        #self.myEndItem.getInputDir()
        
        #self.rect = QRectF( 0, 0, 500, 500 )
        #self.acceptHoverEvents()
        
        #print 'bezierLine.parentItem() = %s' %self.parentItem()
        #print 'bezierLine.parentObject() = %s' %self.parentObject()
        #print 'bezierLine.parentWidget() = %s' %self.parentWidget()
        
    def hoverEnterEvent( self, event ):
        print 'bezierLine.hoverEnterEvent'
        
    def hoverLeaveEvent( self, event ):
        print 'bezierLine.hoverLeaveEvent'
        
    def mouseMoveEvent( self, event ):
        print 'mouseMove'
    '''
    def paintOld( self, painter, option, widget ):
        line = self.getLine()
        #painter.setBrush( self.myColor )
        pen = self.pen()
        pen.setWidth( 2 )
        #pen.setColor( Qt.black )
        painter.setRenderHint( QPainter.Antialiasing )
        
        #if option.state and QStyle.State_Selected:
        if self.isSelected():
            pen.setWidth( 4 )
            #self.setZValue( 10.0 )
            pen.setColor( Qt.green )
            #print 'selection: %s' %self.data( 0 ).toPyObject()
        else:
            pen.setWidth( 2 )
        
        painter.setPen( pen )
        
        painter.drawPath( line )
        
        #print 'endItem = %s' %endItem
        #print 'dir( endItem ) = %s' %dir( endItem )
        #print 'endItems.parentWidget() = %s' %endItem.parentWidget()

    '''

    #def paint( path ):
        
    def paint( self, painter, option, widget ):
        
        #painter.setPen( ( QPen( QColor( 79, 106, 255, 255 ), 2, Qt.DotLine, Qt.FlatCap, Qt.MiterJoin ) ) )
        #painter.setBrush( QColor( 122, 163, 39, 0 ) )




        line = self.getLine()

        pen = self.pen()
        pen.setWidth( 2 )
        #self.setZValue( 2 )
        #pen.setColor( Qt.black )
        painter.setRenderHint( QPainter.Antialiasing )

        if not os.path.isdir( self.startItemLiveDir ):


            #print 'fuck yaaa'
            #pen.setStyle( Qt.DashDotLine )
            pen.setStyle( Qt.CustomDashLine )
            pen.setDashPattern( [ 1, 4 ] )
        else:
            pen.setStyle( Qt.SolidLine )


        if option.state & QStyle.State_MouseOver:
            pen.setColor( self.pathColorItem.lighter( 150 ) )
            self.setZValue( 2 )
        else:
            pen.setColor( self.pathColorItem )
            self.setZValue( -1 )

        painter.setPen( pen )

        self.setPath( line )

        #self.scene.addItem( self.pathItem )



        #painter.setBrush( self.myColor )
        #pen = self.pen()
        #pen.setWidth( 2 )
        #self.setZValue( 2 )
        #pen.setColor( Qt.black )
        
        #pen.setColor( Qt.green )
        
        '''
        if option.state & QStyle.State_Selected:
        #if self.isSelected():
            pen.setWidth( 4 )
            #self.setZValue( 10.0 )
            pen.setColor( Qt.blue )
            #print 'selection: %s' %self.data( 0 ).toPyObject()
        elif option.state & QStyle.State_MouseOver:
            pen.setColor( Qt.yellow )
        else:
            pen.setWidth( 2 )
        '''
        #self.scene.removeItem( self.pathItem )
        #painter.setPen( pen )
        
        painter.drawPath( line )


        
        #print 'endItem = %s' %endItem
        #print 'dir( endItem ) = %s' %dir( endItem )
        #print 'endItems.parentWidget() = %s' %endItem.parentWidget()
        

        
        
        

      
    def getEndItem( self ):
#         print "SceneView.getEndItem(): self.myEndItem = %s" %self.myEndItem
#         print "SceneView.getEndItem(): self.myEndItem.parentItem() = %s" %self.myEndItem.parentItem()
        return self.myEndItem

    def getStartItem( self ):
#         print "SceneView.getEndItem(): self.myStartItem = %s" %self.myStartItem
#         print "SceneView.getEndItem(): self.myStartItem.parentItem() = %s" %self.myStartItem.parentItem()
        return self.myStartItem

    def addItem( self ):
        self.bezierItem = QGraphicsPathItem()
    
    def getLine( self ):
        p1 = QPointF( self.myStartItem.sceneBoundingRect().center().x() + 10, self.myStartItem.sceneBoundingRect().center().y() )
        #print 'p1 = %s' %p1.x()
        p4 = QPointF( self.myEndItem.sceneBoundingRect().center().x() - 10, self.myEndItem.sceneBoundingRect().center().y() )
        #print 'p4 = %s' %p4
        #print dir( p4 )
        if ( p1.x() + 40 ) < p4.x():
            p2 = QPointF( ( p4.x() - p1.x() ) / 2 + p1.x() + 40, p1.y() )
            p3 = QPointF( ( p4.x() - p1.x() ) / 2 + p1.x() - 40, p4.y() )
        elif ( p1.x() + 40 ) >= p4.x():
            
            p2 = QPointF( ( p4.x() - p1.x() ) / 2 + p1.x() + 40 + ( ( ( p1.x() + 40 ) - p4.x() ) ), p1.y() )
            p3 = QPointF( ( p4.x() - p1.x() ) / 2 + p1.x() - 40 - ( ( ( p1.x() + 40 ) - p4.x() ) ), p4.y() )
            
        
        path = QPainterPath( p1 )
        #path.setAcceptHoverEvents( True )
        #path.setAcceptTouchEvents( True )
        #transition = QMouseEventTransition()

        path.cubicTo( p2, p3, p4 )
        #transition.setHitTestPath( path )
        
        #print 'path.elementAt( 3 ) = %s' %path.elementAt( 3 )
        #print 'path.childItems() = %s' %path.childItems()
        #print 'path.parentItem() = %s' %path.parentItem()

        #self.addItem()



        return path


    def setPathColor( self ):
        
        #pass
        #self.gradient.setColorAt( 0, Qt.blue )
        #self.gradient.setColorAt( 1, Qt.green )

        #self.palette = QPalette
        


        print 'bezierLine.label = %s' %self.label.split( '__' )

        self.nodeOutput = self.label.split( '__' )[ 0 ]
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
                            print 'found'
                            found = True
                            outputIndex = index
                            #print item
                            #print index
                            #print self._outputs[ outputIndex ]
                            #print self._outputs[ outputIndex ][ 0 ][ 0 ][ 1 ]
                            self.pathColor = self._outputs[ outputIndex ][ 0 ][ 0 ][ 1 ]
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

        self.pathColorItem.setNamedColor( self.pathColor )
        
        



