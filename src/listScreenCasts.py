__author__ = 'michaelmussato'

import os, sys, threading

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import *

class addScreenCastUI( QWidget ):
    def __init__( self, mainWindow = None, castProcess = None, parent = None ):
        super( addScreenCastUI, self ).__init__( parent )
        self.mainWindow = mainWindow
        self.castProcess = castProcess
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()

        self.createUI()

        self.createConnects()

    def createUI( self ):
        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'addScreenCast.ui' ), self )
        self.labelProcess.setText( self.castProcess.taskName )
        self.pushButtonScreenCastAction.setText( 'stop' )

    def createConnects( self ):
        self.pushButtonScreenCastAction.clicked.connect( self.stopCast )

    def stopCast( self ):
        self.castProcess.stop()
        self.mainWindow.screenCasts.remove( self.castProcess )
        self.close()
        #self.setParen( None )






class listScreenCastsUI( QDialog ):
    listScreenCastsUIClosed = pyqtSignal()



    def __init__( self, mainWindow = None, parent = None ):
        super ( listScreenCastsUI, self ).__init__( parent )

        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.processes = self.mainWindow.qprocesses
        self.screenCasts = None
        #self.ui = loadUi( r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/screenCasts.ui' )
        #self.vLayoutScreenCast( addScreenCastUI( self.mainWindow ) )
        #for i in self.processes:



        self.createUI()
        self.createConnects()
        self.addScreenCastsUI()

        #self.timer = threading.Timer( 1, self.refresh ).start()

    def createUI( self ):
        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'screenCasts.ui' ), self )
        self.spacer = QSpacerItem( 0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding )
        #self.spacer.expandingDirections( Qt.Vertical )

    def createConnects( self ):
        self.refreshPushButton.clicked.connect( self.refresh )



    def refresh( self ):
        #self.timer = threading.Timer( 1, self.refresh ).start()
        print 'refresh'
        for item in reversed( range( self.vLayoutScreenCasts.count() ) ):

            #self.vLayoutScreenCasts.itemAt( item ).widget().setParent( None )
            self.vLayoutScreenCasts.itemAt( item ).widget().close()

        #for i in range( self.vLayoutScreenCasts.count() ):
        #    print i

        #self.screenCasts = self.mainWindow.screenCasts
        self.addScreenCastsUI()
        #time.sleep( 2 )


    def addScreenCastsUI( self ):
        self.screenCasts = self.mainWindow.screenCasts
        for castProcess in self.screenCasts:
            newCast = addScreenCastUI( self.mainWindow, castProcess )
            #newCast = addScreenCastUI()
            #button = QPushButton()
            self.vLayoutScreenCasts.addWidget( newCast )

        #self.vLayoutScreenCasts.addSpacerItem( self.spacer )



    def closeEvent( self, event ):
        self.listScreenCastsUIClosed.emit()
        #self.mainWindow.screenCastsWindow = None

    '''
    @staticmethod
    def displayCasts( mainWindow = None ):
        dialog = listScreenCastsUI( mainWindow )
        result = dialog.exec_()
        submissionCmdArgs = dialog.submitData()
        #return result == dialog.Accepted, submissionCmdArgs
    '''

def main():
    app = QApplication( sys.argv )

    #taskFolder = r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/projects/proj1/content/assets/asset_01/RND_DDL__vvasdfa'

    window = listScreenCastsUI()

    #print jobArnold
    #if ok:
        #print jobArnold
    #screenCastInstance = screenCast( 'asset01', 'task_01')
    #screenCastInstance.startCast()

    #screenCastInstance.stopCast()
    #print 'fuck it'
    #time.sleep( 15 )
    #screenCastInstance.stopCast()
    #screenCastInstance.quit()
    window.show()
    app.exec_()



if __name__ == "__main__":
    main()