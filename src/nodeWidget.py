__author__ = 'michaelmussato'

import os

from PyQt4.QtGui import *
from PyQt4.uic import *


class nodeWidgetUi( QWidget ):
    def __init__( self, mainWindow, parent = None ):
        super( nodeWidgetUi, self ).__init__( parent )
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.currentPlatform = self.mainWindow.getCurrentPlatform()

        self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'nodeWidget.ui' ), self )