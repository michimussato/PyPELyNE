'''
Created on Apr 29, 2015

@author: michaelmussato
'''

import os
from PyQt4.QtGui import *
from PyQt4.uic import *
from vlc import *


class playerUi(QWidget):
    def __init__(self, parent = None):
        super(playerUi, self).__init__(parent)
        self.pypelyne_root = os.getcwd()

        self.ui = loadUi(os.path.join(os.path.dirname(self.main_window.pypelyne_root), 'ui', 'player.ui'), self)
        #self.ui = loadUi(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\player.ui')

        self.player = None

        #self.create_connects()


    def createConnects(self):
        self.radioButtonPlay.toggled.connect(self.play)
        self.radioButtonStop.toggled.connect(self.stop)

    def play(self):
        self.player = MediaPlayer(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\src\audio\cairnomount.mp3')
        self.player.play()

    def stop(self):
        try:
            self.player.stop()
        except:
            pass


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    playerWindow = playerUi()
    #screenSize = QApplication.desktop().availableGeometry()

    playerUi.show()
    app.exec_()