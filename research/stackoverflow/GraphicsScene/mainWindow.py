import os, sip, sys, subprocess, platform

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import *
from PyQt4.QtOpenGL import *

from src.node import *

app = None



class mainWindow( QMainWindow ):
    def __init__( self, parent = None ):
        super( mainWindow, self ).__init__( parent )
        
        
        self.currentPlatform = platform.system()
        
        if self.currentPlatform == "Windows":
            self.ui = loadUi( r'ui\mainWindow.ui', self )
        
        elif self.currentPlatform == "Darwin":
            self.ui = loadUi( r'ui/mainWindow.ui', self )
            
        else:
        	print 'platform not supported'
        	quit()
            
        # Scene view
        self.scene = SceneView()
        self.nodeDropGraphicsView.setViewport( QGLWidget( QGLFormat( QGL.SampleBuffers ) ) )
        self.nodeDropGraphicsView.setScene( self.scene )
        
        self.sendTextToBox( 'this text comes from mainWindow class, line 37 and 38.\n' )
        self.sendTextToBox( 'press right mouse button.\n' )
        
    
    def sendTextToBox( self, text ):
        cursorBox = self.statusBox.textCursor()
        cursorBox.movePosition(cursorBox.End)
        cursorBox.insertText( str( text ) )
        self.statusBox.ensureCursorVisible()


class SceneView( QGraphicsScene ):
    def __init__( self, parent=None ):
        super( SceneView, self ).__init__( parent )
        
        text = self.addText( 'title' )
        
    def mousePressEvent( self, event ):
        pos = event.scenePos()
        if event.button() == Qt.MidButton:
            pass
          
        elif event.button() == Qt.RightButton:
        	newNode = node( pos, self )
        	
        super( SceneView, self ).mousePressEvent( event )
        
    def mouseReleaseEvent( self, event ):
        print 'mouseReleaseEvent'
        
        self.line = None

        super( SceneView, self ).mouseReleaseEvent( event )
        
if __name__ == "__main__":
    
    app = QApplication( sys.argv )
    screenSize = QApplication.desktop().availableGeometry()
    window = mainWindow()
    window.resize( int( screenSize.width() ), int( screenSize.height() ) )
    window.show()
    app.exec_()
    


