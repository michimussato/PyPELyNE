import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class node( QGraphicsItem ):
    def __init__( self, position, scene ):
        super( node, self ).__init__( None, scene )
        
        self.setFlags( QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable )

        self.rect = QRectF( -30, -30, 120, 60 )
        self.setPos( position )
        scene.clearSelection()
        
    def sendFromNodeToBox( self, text ):
        # how do i send text from here to textBox?
        pass
        
    def boundingRect( self ):
        return self.rect

    def paint( self, painter, option, widget ):
        painter.setRenderHint( QPainter.Antialiasing )
        pen = QPen( Qt.SolidLine )
        pen.setColor( Qt.black )
        pen.setWidth( 3 )
        
        if option.state & QStyle.State_Selected:
            #####################
            self.sendFromNodeToBox( 'node selected' )
            #####################
            self.setZValue( 1 )
            pen.setWidth( 4 )
            pen.setColor( Qt.green )
        else:
            pen.setWidth( 3 )
            self.setZValue( 0 )
        painter.setPen( pen )
        painter.setBrush( QColor( 200, 0, 0 ) )
        painter.drawRoundedRect( self.rect, 10.0, 10.0 )
        
        
    


        