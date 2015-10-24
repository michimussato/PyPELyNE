__author__ = 'michaelmussato'

import os

from PyQt4.QtGui import *
from PyQt4.uic import *


class NodeWidgetUi(QWidget):
    def __init__(self, mainWindow, parent = None):
        super(NodeWidgetUi, self).__init__(parent)
        self.mainWindow = mainWindow
        self.pypelyneRoot = self.mainWindow._pypelyne_root
        self.currentPlatform = self.mainWindow._current_platform

        self.ui = loadUi(os.path.join(self.pypelyneRoot, 'ui', 'nodeWidget.ui'), self)