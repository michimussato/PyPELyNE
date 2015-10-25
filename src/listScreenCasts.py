__author__ = 'michaelmussato'

import os, sys, threading

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import *

class addScreenCastUI(QWidget):
    def __init__(self, main_window = None, castProcess = None, parent = None):
        super(addScreenCastUI, self).__init__(parent)
        self.main_window = main_window
        self.castProcess = castProcess
        # self.pypelyne_root = self.main_window.pypelyne_root

        self.createUI()

        self.createConnects()

    def createUI(self):
        self.ui = loadUi(os.path.join(self.main_window.pypelyne_root, 'ui', 'addScreenCast.ui'), self)
        self.labelProcess.setText(self.castProcess.taskName)
        self.pushButtonScreenCastAction.setText('stop')

    def createConnects(self):
        self.pushButtonScreenCastAction.clicked.connect(self.stopCast)

    def stopCast(self):
        self.castProcess.stop()
        self.main_window.screenCasts.remove(self.castProcess)
        self.close()
        #self.setParen(None)






class listScreenCastsUI(QDialog):
    listScreenCastsUIClosed = pyqtSignal()
    #newScreenCast = pyqtSignal()



    def __init__(self, main_window = None, parent = None):
        super (listScreenCastsUI, self).__init__(parent)

        self.main_window = main_window
        # self.pypelyne_root = self.main_window.pypelyne_root
        self.processes = self.main_window.qprocesses
        self.screenCasts = None
        #self.ui = loadUi(r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/screenCasts.ui')
        #self.vLayoutScreenCast(addScreenCastUI(self.main_window))
        #for i in self.processes:



        self.createUI()
        self.createConnects()
        self.addScreenCastsUI()

        #self.timer = threading.Timer(1, self.refresh).start()

    def createUI(self):
        self.ui = loadUi(os.path.join(self.main_window.pypelyne_root, 'ui', 'screenCasts.ui'), self)
        self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.refreshPushButton.setVisible(False)
        #self.spacer.expandingDirections(Qt.Vertical)

    def createConnects(self):
        self.refreshPushButton.clicked.connect(self.refresh)
        self.main_window.addNewScreenCast.connect(self.refresh)



    def refresh(self):
        #self.main_window.addNewScreenCast.connect(self.refresh)
        #self.timer = threading.Timer(1, self.refresh).start()
        print 'refresh'
        for item in reversed(range(self.vLayoutScreenCasts.count())):

            #self.vLayoutScreenCasts.itemAt(item).widget().setParent(None)
            self.vLayoutScreenCasts.itemAt(item).widget().close()

        #for i in range(self.vLayoutScreenCasts.count()):
        #    print i

        #self.screenCasts = self.main_window.screenCasts
        self.addScreenCastsUI()
        #time.sleep(2)


    def addScreenCastsUI(self):
        self.screenCasts = self.main_window.screenCasts
        for castProcess in self.screenCasts:
            newCast = addScreenCastUI(self.main_window, castProcess)
            #newCast = addScreenCastUI()
            #button = QPushButton()
            self.vLayoutScreenCasts.addWidget(newCast)

        #self.vLayoutScreenCasts.addSpacerItem(self.spacer)



    def closeEvent(self, event):
        self.listScreenCastsUIClosed.emit()
        #self.main_window.screenCastsWindow = None

    '''
    @staticmethod
    def displayCasts(main_window = None):
        dialog = listScreenCastsUI(main_window)
        result = dialog.exec_()
        submissionCmdArgs = dialog.submitData()
        #return result == dialog.Accepted, submissionCmdArgs
    '''

def main():
    app = QApplication(sys.argv)

    #taskFolder = r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/projects/proj1/content/assets/asset_01/RND_DDL__vvasdfa'

    window = listScreenCastsUI()

    #print jobArnold
    #if ok:
        #print jobArnold
    #screenCastInstance = screenCast('asset01', 'task_01')
    #screenCastInstance.startCast()

    #screenCastInstance.stopCast()
    #print 'fuck it'
    #time.sleep(15)
    #screenCastInstance.stopCast()
    #screenCastInstance.quit()
    window.show()
    app.exec_()



if __name__ == "__main__":
    main()