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
        
        self.current_platform = platform.system()
        
        if self.current_platform == "Windows":
            self.ui = loadUi(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\pypelyneConfigurationWindow.ui', self)
            
        elif self.current_platform == "Linux" or self.current_platform == "Darwin":
            self.ui = loadUi(r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/pypelyneConfigurationWindow.ui', self)
        self.setModal(True)