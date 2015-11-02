
import os, sys, time, subprocess, getpass, datetime, logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class screenCast(QProcess):
    def __init__(self, main_window, assetName, taskName, projectPath):
        super(screenCast, self).__init__(None)

        self.main_window = main_window

        self.vlcExec = self.main_window.screenCastExec

        self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S-%f')

        self.projectPath = projectPath
        self.assetName = assetName
        self.taskName = taskName
        self.makingOfDir = os.path.join(self.projectPath, 'making_of')

        self.user = self.main_window.user

        if not os.path.exists(self.makingOfDir):
            os.makedirs(self.makingOfDir, mode=0777)

        self.mp4 = self.makingOfDir + os.sep + self.now + '__' + self.user + '__' + self.assetName + '__' + self.taskName + '.mp4'
        self.vlcSocket = os.path.join(os.path.expanduser('~'), str('vlc.sock' + '.' + self.now))

        self.vlcArgs = [self.vlcExec, '-I', 'rc', '--rc-fake-tty', '--rc-unix', self.vlcSocket, 'screen://', '--screen-fps', '4', '--quiet', '--sout', '#transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst=' + self.mp4 + '}']

    def start(self):
        try:
            subprocess.Popen(self.vlcArgs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.main_window.sendTextToBox('%s: screencast for %s started\n' %(datetime.datetime.now(), self.taskName))
            logging.info('screencast for %s started' %(self.taskName))
        except:
            self.main_window.sendTextToBox('%s: startCast failed\n'%(datetime.datetime.now()))
            logging.warning('startCast failed')

    def stop(self):
        commandStop = "echo stop | nc -U " + self.vlcSocket
        commandQuit = "echo quit | nc -U " + self.vlcSocket

        os.system(commandStop)
        os.system(commandQuit)
        self.main_window.sendTextToBox('%s: screenCast on %s finished\n' %(datetime.datetime.now(), self.taskName))
        self.main_window.sendTextToBox('%s: video created at %s\n' %(datetime.datetime.now(), self.mp4))

        logging.info('screenCast on %s finished' %(self.taskName))
        logging.info('video created at %s' %(self.mp4))


    def quit(self):
        print 'exitting'
        quit()





def main():
    app = QApplication(sys.argv)
    screenCastInstance = screenCast('asset01', 'task_01')
    screenCastInstance.start()

    time.sleep(15)
    screenCastInstance.stop()
    screenCastInstance.quit()

    return app.exec_()



if __name__ == "__main__":
    main()


    #print "starting PyPELyNE"

    #app.aboutToQuit.connect(deleteGLWidget)
    #screenSize = QApplication.desktop().availableGeometry()
    #print 'screen resolution is %ix%i' %(int(screenSize.width()), int(screenSize.height()))

    #screenSize = QApplication.desktop().availableGeometry()
    #pypelyneWindow.resize(int(screenSize.width()), int(screenSize.height()))
    #pypelyneWindow.show()
    #app.exec_()