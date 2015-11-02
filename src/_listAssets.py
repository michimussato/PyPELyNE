__author__ = 'michaelmussato'


from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import *

import os

class listAssetsUI( QWidget ):
    def __init__( self, main_window = None, position = None, parent = None ):
        super( listAssetsUI, self ).__init__( parent )

        self.main_window = main_window
        # self.pypelyne_root = self.main_window.pypelyne_root
        self.libraryRoot = self.main_window.libraryRoot

        self.position = position

        self.assets = []
        self.getAssets( self.libraryRoot )

        self.createUI()

        self.addAssetToUI()

    def createUI( self ):
        self.ui = loadUi( os.path.join( self.main_window.pypelyne_root, 'ui', 'assetsLibrary.ui' ), self )


    def getAssets( self, libraryRoot ):
        self.assets = os.listdir( libraryRoot )

    def addAssetToUI( self ):
        for asset in self.assets:
            self.vLayoutAssets.addWidget( QPushButton( asset ) )

    def createLoader( self ):
        pass
