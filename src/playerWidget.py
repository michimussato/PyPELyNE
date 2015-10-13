__author__ = 'michaelmussato'

import os

from PyQt4.QtGui import *
from PyQt4.uic import *


class playerWidgetUi(QWidget):
    def __init__(self, mainWindow, parent = None):
        super(playerWidgetUi, self).__init__(parent)
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
        self.currentPlatform = self.mainWindow.getCurrentPlatform()

        self.ui = loadUi(os.path.join(self.pypelyneRoot, 'ui', 'player.ui'), self)


        #self.connect(self.pushButtonPlayStop, SIGNAL('customContextMenuRequested(const QPoint&)'), self.playerContextMenu)
        #self.contextMenu =QMenu()
        #self.contextMenu.addSeparator()

    #def playerContextMenu(self, point):
        #sendingButton = self.sender()
        #self.contextMenu.exec_(sendingButton.mapToGlobal(point))