import sys, os, platform, re


import xml.etree.ElementTree as ET
from PyQt4.QtGui import *
from PyQt4.uic import *

import settings as SETTINGS


class jobAddArgUi(QWidget):
    def __init__(self, main_window, argValue = None, parent = None):
        super(jobAddArgUi, self).__init__(parent)

        self.main_window = main_window
        # self.pypelyne_root = self.main_window.pypelyne_root
        self.main_window.current_platform = self.main_window.current_platform
        self.ui = loadUi(os.path.join(self.main_window.pypelyne_root, 'ui', 'jobAddArg.ui'), self)
        self.pushButtonDelete.setVisible(False)

        if not bool(argValue) == False:
            self.lineEditArg.setText(argValue)

    def returnLineEditValue(self):
        return self.lineEditArg.text()

    def createConnects(self):
        self.pushButtonDelete.clicked.connect(self.delete)

    def delete(self):
        self.deleteLater()


class jobAddPropUi(QWidget):
    def __init__(self, main_window, propValue = None, parent = None):
        super(jobAddPropUi, self).__init__(parent)

        self.main_window = main_window
        # self.pypelyne_root = self.main_window.pypelyne_root
        # self.current_platform = self.main_window.current_platform
        self.ui = loadUi(os.path.join(self.main_window.pypelyne_root, 'ui', 'jobAddProp.ui'), self)
        self.pushButtonDelete.setVisible(False)

        if not bool(propValue) == False:
            self.lineEditProp.setText(propValue)

    def returnLineEditValue(self):
        return self.lineEditProp.text()

    def createConnects(self):
        self.pushButtonDelete.clicked.connect(self.delete)

    def delete(self):
        self.deleteLater()


class jobDeadlineUi(QDialog):
    def __init__(self, taskRoot, main_window = None, parent = None):
        super(jobDeadlineUi, self).__init__(parent)

        self.main_window = main_window
        # self.pypelyne_root = self.main_window.pypelyne_root
        # self.current_platform = self.main_window.current_platform
        # self.exclusions = SETTINGS.EXCLUSIONS
        self.taskRoot = taskRoot
        self.projectName = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(self.taskRoot)))))
        self.assetName = os.path.basename(os.path.dirname(self.taskRoot))
        self.taskName = os.path.basename(self.taskRoot)

        inputContent = os.listdir(os.path.join(self.taskRoot, 'input'))

        self.input = []

        for directory in inputContent:
            if directory not in SETTINGS.EXCLUSIONS:
                self.input.append(os.path.join(self.taskRoot, 'input', directory))

        self.input = self.input[0]
        self.inputPrefix = os.path.splitext(self.input)[1][1:]

        self.inputContent = os.listdir(self.input)

        if self.inputPrefix in self.inputContent:
            self.inputContent.remove(self.inputPrefix)

        for exclusion in SETTINGS.EXCLUSIONS:
            if exclusion in self.inputContent:
                print 'exclusion found'
                self.inputContent.remove(exclusion)

        if len(self.inputContent) > 0:
            self.jobExtension = os.path.splitext(self.inputContent[0])[1]
            self.range = self.getRange(self.inputContent)

        self.inputLink = os.path.realpath(self.input)
        self.inputName = getattr(os.path.basename(self.input).split('.'), '__getitem__')(-1)
        outputContent = os.listdir(os.path.join(self.taskRoot, 'output'))

        self.output = []

        for directory in outputContent:
            if directory not in SETTINGS.EXCLUSIONS:
                self.output.append(os.path.join(self.taskRoot, 'output', directory))

        self.output = self.output[0]
        self.outputName = os.path.basename(self.output)
        self.outputVersion = os.readlink(os.path.join(self.output, 'current'))

        self.ui = loadUi(os.path.join(self.main_window.pypelyne_root, 'ui', 'jobDeadline.ui'), self)

        self.propWidgets = []
        self.argWidgets = []
        self.props = []
        self.args = []

        self.initialStates = ['Suspended', 'Active']

        self.submissionCmdArgs = []

        self.submissionCmd = r'/Applications/Deadline/Resources/bin/deadlinecommand'


        if self.jobExtension == '.ass':
            self.setArnoldProps()
        elif self.jobExtension == '.ifd':
            self.setMantraProps()
        else:
            print self.jobExtension

        self.createConnects()

        self.setValues()

    def setArnoldProps(self):
        self.startupDirectory = r'/Applications/MtoA/bin'
        self.plugin = r'kick'
        self.helpCommand = os.path.join(self.startupDirectory, self.plugin) + ' --help'
        self.getAASamples(self.inputContent[0])
        self.props = [\
                        ('Comment', 'Arnold'), \
                        ('Interruptible', 'true'), \
                        ('ForceReloadPlugin', 'false'), \
                        ('OutputDirectory0', self.output + os.sep + self.outputVersion), \
                        ('OutputFilename0', self.outputName + '.####.exr'), \
                        ('Name', self.projectName + '  |  ' + self.assetName + '  |  ' + self.taskName + '  |  ' + self.outputName + '  |  ' + self.outputVersion) \
                       ]
        self.args = [\
                        ('-v', '2'), \
                        ('-as', self.aaSamples), \
                        ('-dw', ''), \
                        ('-nstdin', ''), \
                        ('-bs', '64'), \
                        ('-i', '<QUOTE>' + self.inputLink + os.sep + self.inputName + '.' + '<STARTFRAME%4>' + '.ass' + '<QUOTE>'), \
                        ('-o', '<QUOTE>' + self.output + os.sep + self.outputVersion + os.sep + self.outputName + '.' + '<STARTFRAME%4>' + '.exr' + '<QUOTE>') \
                       ]



    def setMantraProps(self):
        self.startupDirectory = r'/Library/Frameworks/Houdini.framework/Versions/Current/Resources/bin'
        self.plugin = r'mantra'
        self.helpCommand = os.path.join(self.startupDirectory, self.plugin) + ' -h'
        self.props = [\
                        ('Comment', 'Mantra'), \
                        ('Interruptible', 'true'), \
                        ('ForceReloadPlugin', 'false'), \
                        ('OutputDirectory0', self.output + os.sep + self.outputVersion), \
                        ('OutputFilename0', self.outputName + '.####.exr'), \
                        ('Name', self.projectName + '  |  ' + self.assetName + '  |  ' + self.taskName + '  |  ' + self.outputName + '  |  ' + self.outputVersion) \
                       ]
        self.args = [\
                        ('-V', '4a'), \
                        ('-j', '0'), \
                        ('-F', '<QUOTE>' + self.inputLink + os.sep + self.inputName + '.' + '<STARTFRAME%4>' + '.ifd' + '<QUOTE>'), \
                        ('', '<QUOTE>' + self.output + os.sep + self.outputVersion + os.sep + self.outputName + '.' + '<STARTFRAME%4>' + '.exr' + '<QUOTE>') \
                       ]
        # ('-V', '4a'), \

    def getRange(self, fileList):
        arrayLength = len(fileList[0].split('.'))

        if arrayLength == 2:
            firstFrame = 1
            lastFrame = 1

        elif arrayLength == 3:
            firstFrame = fileList[0].split('.')[1]
            lastFrame = fileList[-1].split('.')[1]

        return firstFrame, lastFrame

    def getAASamples(self, file):
        try:
            #print os.path.join(self.input, file)
            assFile = open(os.path.join(self.input, file), 'r')

            for line in assFile:
                if re.match('(.*)(A|a)(A|a)_samples(.*)', line):
                    lineSplit = line.split(' ')
                    self.aaSamples = lineSplit[2].replace('\n', '')
                    assFile.close()
                    break
        except:
            self.aaSamples = 3



    def setValues(self):

        self.labelExecutable.setText(self.plugin)
        self.lineEditHelp.setText(self.helpCommand)
        self.lineEditFrames.setText(self.range[0] + '-' + self.range[1])
        self.labelStartupDirectory.setText(os.path.realpath(self.startupDirectory))
        self.labelJobName.setText(self.taskName)
        self.labelInput.setText(os.path.basename(self.input) + ' (' + os.path.basename(self.inputLink) + ')')
        self.labelOutput.setText(self.outputName + ' (' + self.outputVersion + ')')
        for initialStatus in self.initialStates:
            self.comboBoxInitialStatus.addItem(initialStatus)

        for arg in self.args:
            argValue = str(arg[0] + ' ' + arg[1])
            newArg = self.addArg(argValue)

        for prop in self.props:
            propValue = str(prop[0] + '=' + prop[1])
            newProp = self.addProp(propValue)





    def createConnects(self):
        self.pushButtonAddProp.clicked.connect(self.addProp)
        self.pushButtonAddArg.clicked.connect(self.addArg)
        self.pushButtonOk.clicked.connect(self.onOk)
        self.pushButtonCancel.clicked.connect(self.onCancel)

    def addArg(self, argValue=None):

        #print 'addArg'
        newArg = jobAddArgUi(self.main_window, argValue)

        self.vLayoutProps.addWidget(newArg)
        self.argWidgets.append(newArg)

    def addProp(self, propValue=None):
        newProp = jobAddPropUi(self.main_window, propValue)
        self.vLayoutProps.addWidget(newProp)
        self.propWidgets.append(newProp)

    def delProp(self, propUi):
        print 'delProp'
        pass

    def onOk(self):
        self.submissionCmdArgs.append(self.submissionCmd)
        self.submissionCmdArgs.append('-SubmitCommandLineJob')

        args = []
        props = []

        for argWidget in self.argWidgets:
            if not str(argWidget.returnLineEditValue()) == '' or str(argWidget.returnLineEditValue()) == ' ':
                args.append(str(argWidget.returnLineEditValue()))

        for propWidget in self.propWidgets:
            if not str(propWidget.returnLineEditValue()) == '' or str(propWidget.returnLineEditValue()) == ' ':
                props.append(str(propWidget.returnLineEditValue()))

        startupDirectory = str(self.labelStartupDirectory.text())
        chunkSize = str(self.spinBoxChunkSize.value())
        frames = str(self.lineEditFrames.text())
        initialStatus = str(self.comboBoxInitialStatus.currentText())
        concurrentTasks = str(self.spinBoxConcurrentTasks.value())

        argsString = ' '.join(args)

        priority = str(self.spinBoxPropPriority.value())
        props.append('Priority=' + priority)

        props.append('ConcurrentTasks=' + concurrentTasks)

        self.submissionCmdArgs.append('-executable ' + '"' + os.path.join(self.startupDirectory, self.plugin) + '"')
        self.submissionCmdArgs.append('-startupdirectory ' + '"' + startupDirectory + '"')
        #self.submissionCmdArgs.append('-chunksize ' + '"' + chunkSize + '"')
        self.submissionCmdArgs.append('-arguments ' + '"' + argsString + '"')
        self.submissionCmdArgs.append('-frames ' + '"' + frames + '"')
        self.submissionCmdArgs.append('-initialstatus ' + '"' + initialStatus + '"')

        for prop in props:
            self.submissionCmdArgs.append('-prop ' + '"' + prop + '"')

        self.accept()

    def submitData(self):
        return self.submissionCmdArgs

    def onCancel(self):
        pass
        self.reject()

    @staticmethod
    def getDeadlineJobData(nodeDir, main_window):
        dialog = jobDeadlineUi(nodeDir, main_window)
        result = dialog.exec_()
        submissionCmdArgs = dialog.submitData()
        return result == dialog.Accepted, submissionCmdArgs







def main():
    app = QApplication(sys.argv)

    taskFolder = r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/projects/proj1/content/assets/asset_01/RND_DDL__vvasdfa'

    ok, jobArnold = jobDeadlineUi.getDeadlineJobData(taskFolder)

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
    #jobArnoldWidget.show()
    #app.exec_()



if __name__ == "__main__":
    main()