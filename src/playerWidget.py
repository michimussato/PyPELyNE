__author__ = 'michaelmussato'

import os

from PyQt4.QtGui import *
from PyQt4.uic import *


class PlayerWidgetUi(QWidget):
    def __init__(self, main_window, parent = None):
        super(PlayerWidgetUi, self).__init__(parent)
        self.main_window = main_window
        # self.pypelyne_root = self.main_window.pypelyne_root
        # self.current_platform = self.main_window.current_platform

        self.ui = loadUi(os.path.join(self.main_window.pypelyne_root, 'ui', 'player.ui'), self)


        #self.connect(self.pushButtonPlayStop, SIGNAL('customContextMenuRequested(const QPoint&)'), self.player_context_menu)
        #self.contextMenu =QMenu()
        #self.contextMenu.addSeparator()

    #def player_context_menu(self, point):
        #sendingButton = self.sender()
        #self.contextMenu.exec_(sendingButton.mapToGlobal(point))