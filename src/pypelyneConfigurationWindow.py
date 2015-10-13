'''
Created on Dec 7, 2014

@author: michaelmussato
'''

from PyQt4.QtGui import *
from PyQt4.uic import *

import platform


class pypelyneConfigurationWindow(QDialog):
    def __init__(self, parent = None):
        super(pypelyneConfigurationWindow, self).__init__(parent)
        
        self.currentPlatform = platform.system()
        
        if self.currentPlatform == "Windows":
            self.ui = loadUi(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\pypelyneConfigurationWindow.ui', self)
            
        elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
            self.ui = loadUi(r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/pypelyneConfigurationWindow.ui', self)
        self.setModal(True)