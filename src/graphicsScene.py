from PyQt4.QtGui import *
from PyQt4.QtCore import *
import xml.etree.ElementTree as ET

from src.circlesInOut import *
from src.node import *
from src.bezierLine import *

from src.newNode import *
from src.newOutput import *
from src.newLoader import *

import shutil
import os
import subprocess
import logging
import json

# class Signals(QObject):
#     trigger = pyqtSignal(str)


class SceneView(QGraphicsScene):
    textMessage = pyqtSignal(str)
    nodeSelect = pyqtSignal(object)
    nodeDeselect = pyqtSignal()
    
    def __init__(self, main_window, parent=None):
        super(SceneView, self).__init__(parent)

        self.mainWindow = main_window
        self.pypelyneRoot = self.mainWindow._pypelyne_root
        self.currentPlatform = self.mainWindow._current_platform
        self.projectsRoot = str(self.mainWindow._projects_root)

        self.exclusions = self.mainWindow._exclusions
        self.imageExtensions = self.mainWindow._image_extensions
        self.movieExtensions = self.mainWindow._movie_extensions
        self.sequenceExec = self.mainWindow._sequence_exec

        self.line = None
        # rect = self.setSceneRect(QRectF(0, 0, 0, 0))
        
        self.nodeList = []

    def addToNodeList(self, node):
        self.nodeList.append(node)

    @property
    def _node_list(self):
        return self.nodeList

    # def getNodeList(self):
    #     return self.nodeList
        
    def clearNodeList(self):
        self.nodeList = []

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                if item.inputs > 1:
                    item.sendFromNodeToBox('item has inputs. cannot delete.\n')
                elif item.inputs == 1:
                    self.removeItem(item)

        super(SceneView, self).keyPressEvent(event)

    def unmakeLive(self, path):
        os.unlink(path)

    def unmakeLiveCallback(self, path):
        def callback():
            self.unmakeLive(path)
        return callback

    def viewVersion(self, imgFile):
        def callback():
            subprocess.Popen([self.sequenceExec, imgFile], shell=False)
        return callback

    def compareVersion(self, imgFile, liveImgFile):
        def callback():
            subprocess.Popen([self.sequenceExec, imgFile, '-wipe', liveImgFile], shell=False)
        return callback

    def differenceVersion(self, imgFile, liveImgFile):
        def callback():
            subprocess.Popen([self.sequenceExec, imgFile, '-diff', liveImgFile], shell=False)
        return callback

    def deleteContentCallback(self, path):
        def callback():
            self.deleteContent(path)
        return callback

    def deleteContent(self, path):
        #print path
        shutil.rmtree(path)

    def copyToClipboard(self, text):
        self.mainWindow.clipBoard.setText(text)
        print '%s copied to clipboard' %(text)

    def copyToClipboardCallback(self, text):
        def callback():
            self.copyToClipboard(text)
        return callback

    @property
    def _item_clicked(self, event):
        pos = event.scenePos()
        return self.itemAt(pos)

    @property
    def _node_clicked(self, event):
        pos = event.scenePos()
        object_clicked = self.itemAt(pos)
        # try:
        # node specific context menu items
        if isinstance(object_clicked, node) \
                or isinstance(object_clicked.parentItem(), node) \
                or isinstance(object_clicked.parentItem().parentItem(), node) \
                or isinstance(object_clicked.parentItem().parentItem().parentItem(), node):

            if isinstance(object_clicked, node):
                object_clicked = object_clicked
            elif isinstance(object_clicked.parentItem(), node):
                object_clicked = object_clicked.parentItem()
            elif isinstance(object_clicked.parentItem().parentItem(), node):
                object_clicked = object_clicked.parentItem().parentItem()
            elif isinstance(object_clicked.parentItem().parentItem().parentItem(), node):
                object_clicked = object_clicked.parentItem().parentItem().parentItem()

        return object_clicked

    def contextMenu(self, pos):
        
        self.menu = QMenu()

        # currentProject = self.mainWindow.getCurrentProject()
        # currentContent = self.mainWindow._current_content
        # print self.mainWindow._current_content
        # print self.mainWindow._projects_root
        # print os.path.join(str(self.mainWindow._projects_root), str(self.mainWindow._current_content))

        # icon = QIcon
        
        objectClicked = self.itemAt(pos)

        '''
        try:
            print '1 %s' %(objectClicked)
        except:
            pass
        try:
            print '2 %s' %(objectClicked.parentItem())
        except:
            pass
        try:
            print '3 %s' %(objectClicked.parentItem().parentItem())
        except:
            pass
        try:
            print '4 %s' %(objectClicked.parentItem().parentItem().parentItem())
        except:
            pass
        '''
        
        items = []

        #self.menu.addMenu('add item')

        contentDirs = os.listdir(os.path.join(self.mainWindow._projects_root, self.mainWindow._current_project, 'content', self.mainWindow._current_content['content']))
        print contentDirs
        
        self.menu.addAction('new node', self.new_node_dialog(pos))
        self.menu.addSeparator()
        self.menu.addAction('new loader', self.newLoaderDialog(pos))
        #for dir in contentDirs:
        if not any(dir.startswith('SVR') for dir in contentDirs):
            self.menu.addAction('new saver', self.newSaverDialog(pos))
        else:
            print 'content already has a saver'
        self.menu.addSeparator()

        self.menu.addAction('from library...', self.fooCallback('from library item'))
        
        try:

            #node specific context menu items
            if isinstance(objectClicked, node) \
                    or isinstance(objectClicked.parentItem(), node) \
                    or isinstance(objectClicked.parentItem().parentItem(), node) \
                    or isinstance(objectClicked.parentItem().parentItem().parentItem(), node):

                if isinstance(objectClicked, node):
                    nodeClicked = objectClicked
                elif isinstance(objectClicked.parentItem(), node):
                    nodeClicked = objectClicked.parentItem()
                elif isinstance(objectClicked.parentItem().parentItem(), node):
                    nodeClicked = objectClicked.parentItem().parentItem()
                elif isinstance(objectClicked.parentItem().parentItem().parentItem(), node):
                    nodeClicked = objectClicked.parentItem().parentItem().parentItem()


                self.menuNode = self.menu.addMenu('node')

                if not nodeClicked.label.startswith('LDR') and not nodeClicked.label.startswith('SVR'):
                    self.menuNode.addAction('open node directory', lambda: self.mainWindow.locateContent(nodeClicked.getNodeRootDir()))

                    if not os.path.exists(os.path.join(nodeClicked.getNodeRootDir(), 'locked')):
                        self.menuNode.addSeparator()
                        self.menuNode.addAction('cleanup node', self.cleanUpNodeCallback(nodeClicked))
                        self.menuNode.addAction('delete node', self.removeObjectCallback(nodeClicked))

                        if os.path.exists(os.path.join(nodeClicked.getNodeRootDir(), 'checkedOut')):
                            self.menuNode.addSeparator()
                            self.menuNode.addAction('check in node', self.mainWindow.checkInCallback(nodeClicked))

                        else:
                            self.menuNode.addSeparator()
                            self.menuNode.addAction('check out node', self.mainWindow.checkOutCallback(nodeClicked))

                elif nodeClicked.label.startswith('LDR_AST'):

                    self.menuNode.addAction('open asset tree', lambda: self.mainWindow.getAssetContent(None, nodeClicked.getLabel()))
                    self.menuNode.addSeparator()
                    self.menuNode.addAction('delete asset loader', self.removeObjectCallback(nodeClicked))

                elif nodeClicked.label.startswith('LDR_SHT'):
                    #self.menuNode.addAction('open shot', lambda: self.foo(nodeClicked.getNodeRootDir()))
                    self.menuNode.addAction('open shot tree', lambda: self.mainWindow.getShotContent(None, nodeClicked.getLabel()))
                    self.menuNode.addSeparator()
                    self.menuNode.addAction('delete shot loader', self.removeObjectCallback(nodeClicked))

                elif nodeClicked.label.startswith('SVR_AST'):
                    self.menuNode.addAction('delete asset saver', self.removeObjectCallback(nodeClicked))
                    self.menuNode.addSeparator()
                    self.menuNode.addAction('check out asset', self.mainWindow.checkOutCallback(nodeClicked))

                elif nodeClicked.label.startswith('SVR_SHT'):
                    self.menuNode.addAction('delete shot saver', self.removeObjectCallback(nodeClicked))
                    self.menuNode.addSeparator()
                    self.menuNode.addAction('check out shot', self.mainWindow.checkOutCallback(nodeClicked))

                    #self.mainWindow.getShotContent(None, nodeClicked.getLabel())

                self.menuNode.addSeparator()
                #self.menu.addAction('cleanup node', self.fooCallback('cleanup node'))




                #self.menu.addSeparator()


                #self.menu.addAction('clone', lambda: self.cloneNodeCallback(objectClicked)).setActive ('False')


                #self.menu.addAction('none', lambda: None)
                #items.append('delete this node')
                #print objectClicked.getNodeRootDir()

                #location = self.mainWindow.locateContent(objectClicked.getNodeRootDir(objectClicked))

            #input specific context menu items
            if isinstance(objectClicked, portInput) and not objectClicked.label == None:
                self.menuInput = self.menu.addMenu('input')



                #items.append('delete this input')

                self.menuPathOps = self.menuInput.addMenu('clipboard')
                self.menuInput.addSeparator()
                self.menuInput.addAction('delete input', self.removeObjectCallback(objectClicked))


                inputLabel = objectClicked.getLabel()
                inputDir = objectClicked.getInputDir()

                outputNode = objectClicked.parentItem()
                outputNodeRootDir = outputNode.getNodeRootDir()

                self.menuPathOps.addAction('copy input label', self.copyToClipboardCallback(inputLabel))
                self.menuPathOps.addAction('copy absolute input path',  self.copyToClipboardCallback(os.path.join(inputDir, inputLabel)))
                self.menuPathOps.addAction('copy relative input path',  self.copyToClipboardCallback(os.path.relpath(os.path.join(inputDir, inputLabel), os.path.join(outputNodeRootDir))))





            #output specific context menu items
            if isinstance(objectClicked, portOutput) and not objectClicked.parentItem().label.startswith('LDR'):
                #items.append('delete this output')

                #self.menu.addSeparator()



                #self.menu.addSeparator()




                self.menuOutput = self.menu.addMenu('output')

                self.menuPathOps = self.menuOutput.addMenu('clipboard')
                self.menuOutput.addSeparator()

                #print objectClicked.getOutputDir()

                outputDir = objectClicked.getOutputDir()
                #print outputDir
                outputLabel = objectClicked.getLabel()
                #print outputLabel
                liveDir = objectClicked.getLiveDir()
                #print liveDir
                outputNodeRootDir = objectClicked.getOutputRootDir()

                #RV viewer here...

                #print 'liveDir = %s' %liveDir


                versions = self.getVersions(outputDir)
                #print outputDir

                self.menuOutput.addAction('open output directory', lambda: self.mainWindow.locateContent(outputDir))

                #self.menuVersion.addAction('cleanup', lambda: self.foo('cleanup'))

                self.menuOutput.addSeparator()

                #self.menuMakeLive = self.menuVersion.addMenu('make live')

                #try:
                #    print os.path.exists(liveDir)
                #except:
                #    raise 'shizzle'

                self.menuPathOps.addAction('copy output label', self.copyToClipboardCallback(outputLabel))
                self.menuPathOps.addAction('copy absolute output path',  self.copyToClipboardCallback(os.path.join(outputDir, 'current', outputLabel)))
                self.menuPathOps.addAction('copy relative output path',  self.copyToClipboardCallback(os.path.relpath(os.path.join(outputDir, 'current', outputLabel), os.path.join(outputNodeRootDir))))

                self.menuOutput.addAction('cleanup output', self.cleanUpOutputCallback(objectClicked))

                if os.path.exists(liveDir):

                    #liveVersion = os.path.basename(os.readlink(liveDir))


                    #self.menuPathOps.addAction('to clipboard 1234', self.copyToClipboardCallback('1234'))
                    #self.menuPathOps.addAction('to clipboard 5678', self.copyToClipboardCallback('5678'))
                    #self.menuPathOps.addAction('copy relative path', self.foo())
                    #self.menuPathOps()

                    self.menuOutput.addAction('remove pipe (live)', self.unmakeLiveCallback(liveDir))
                self.menuOutput.addAction('delete output', self.removeObjectCallback(objectClicked))
                self.menuOutput.addSeparator()

                self.menuOutput.addAction('create new version', self.createNewVersionCallback(outputDir))

                    #print 'added'
                self.menuOutput.addSeparator()
                #print versions
                for version in versions:
                    '''
                    if version in self.exclusions:
                        try:
                            os.remove(os.path.join(outputDir, version))
                            logging.info('exclusion found in versions of output %s. %s removed.' %(objectClicked.label, os.path.join(outputDir, version)))
                        except:
                            logging.warning('exclusion found but not removed: %s' %(os.path.join(outputDir, version)))
                    '''
                    if not version == 'current':

                        versionPath = os.path.join(outputDir, version)
                        #print versionPath

                        outputDirContent = os.listdir(versionPath)

                        print outputDirContent

                        for item in outputDirContent:
                            if item in self.exclusions:
                                # try:
                                os.remove(os.path.join(versionPath, item))
                                outputDirContent.remove(item)
                                logging.info('exclusion found and removed: %s' %(os.path.join(versionPath, item)))
                                # except:
                                #     outputDirContent.remove(item)
                                #     logging.warning('exclusion found but not removed: %s' %(os.path.join(versionPath, item)))
                            try:
                                outputDirContent.remove('approved')
                            except ValueError, e:
                                print 'error captured:', e
                            try:
                                outputDirContent.remove('requestApproval')
                            except ValueError, e:
                                print 'error captured:', e
                            try:
                                outputDirContent.remove('denied')
                            except ValueError, e:
                                print 'error captured:', e
                        outputDirContent.remove(outputLabel)

                        menuMakeLive = self.menuOutput.addMenu(version)

                        if self.currentPlatform == 'Darwin' or self.currentPlatform == 'Linux':
                            if os.path.exists(liveDir):
                                if not objectClicked.parentItem().label.startswith('LDR'):
                                    if os.path.exists(os.path.join(outputDir, version, 'approved')):
                                        if os.path.basename(os.readlink(liveDir)) == version:
                                            menuMakeLive.setIcon(QIcon('src/icons/dotActiveApproved.png'))
                                        elif not os.path.basename(os.readlink(liveDir)) == version:
                                            menuMakeLive.setIcon(QIcon('src/icons/dotInactiveApproved.png'))

                                    elif os.path.exists(os.path.join(outputDir, version, 'waiting')):
                                        if os.path.basename(os.readlink(liveDir)) == version:
                                            menuMakeLive.setIcon(QIcon('src/icons/dotActiveRequested.png'))
                                        elif not os.path.basename(os.readlink(liveDir)) == version:
                                            menuMakeLive.setIcon(QIcon('src/icons/dotInactiveRequested.png'))

                                    elif os.path.exists(os.path.join(outputDir, version, 'denied')):
                                        if os.path.basename(os.readlink(liveDir)) == version:
                                            menuMakeLive.setIcon(QIcon('src/icons/dotActiveDenied.png'))
                                        elif not os.path.basename(os.readlink(liveDir)) == version:
                                            menuMakeLive.setIcon(QIcon('src/icons/dotInactiveDenied.png'))

                                    else:
                                        if os.path.basename(os.readlink(liveDir)) == version:
                                            menuMakeLive.setIcon(QIcon('src/icons/dotActive.png'))
                                        elif not os.path.basename(os.readlink(liveDir)) == version:
                                            menuMakeLive.setIcon(QIcon('src/icons/dotInactive.png'))

                                else:
                                    menuMakeLive.setIcon(QIcon('src/icons/dotActive.png'))
                            else:
                                    menuMakeLive.setIcon(QIcon('src/icons/dotInactive.png'))
                        # elif self.currentPlatform == 'Windows':
                        #     if os.path.exists(liveDir):
                        #         print liveDir
                        #         print os.path.abspath(liveDir)
                        #         print os.path.realpath(liveDir)
                        #         print version
                        #         if os.path.basename(os.path.realpath(liveDir)) == version:
                        #             menuMakeLive.setIcon(QIcon('src/icons/dotActive.png'))
                        #         else:
                        #             menuMakeLive.setIcon(QIcon('src/icons/dotInactive.png'))
                        #     else:
                        #         menuMakeLive.setIcon(QIcon('src/icons/dotInactive.png'))

                        if os.path.exists(os.path.join(versionPath, 'approved')):
                            menuMakeLive.addAction('remove approval', self.removeApproveVersionCallback(versionPath))
                            menuMakeLive.addSeparator()
                        else:
                            if not os.path.exists(os.path.join(versionPath, 'denied')):
                                menuMakeLive.addAction('approve', self.approveVersionCallback(versionPath))
                                menuMakeLive.addAction('deny', self.denyVersionCallback(versionPath))

                            if os.path.exists(os.path.join(versionPath, 'waiting')):
                                menuMakeLive.addAction('cancel approval request', self.removeApproveRequestVersionCallback(versionPath))
                            else:
                                menuMakeLive.addAction('request approval', self.approveRequestCallback(versionPath))

                            menuMakeLive.addSeparator()


                        # if outputLabel.startswith('SEQ') or outputLabel.startswith('TEX') or outputLabel.startswith('PLB'):
                        # print os.path.splitext(outputDirContent[0])[1]
                        # TODO: error here
                        try:
                            print 'halo'
                            print '1', os.path.splitext(outputDirContent[0])[1]
                            print '2', os.path.splitext(outputDirContent[0])[1]
                            if os.path.splitext(outputDirContent[0])[1] in self.imageExtensions or os.path.splitext(outputDirContent[0])[1] in self.movieExtensions:
                                '''
                                for exclusion in self.exclusions:
                                    try:
                                        #if os.path.exists(os.path.join(outputDirContent, exclusion)):
                                        logging.info('exclusion removed from list: %s' %(os.path.join(outputDirContent, exclusion)))
                                        #os.remove(os.path.join(outputDirContent, exclusion))
                                        outputDirContent.remove(exclusion)
                                    except:
                                        logging.warning('exclusion found but not removed from list: %s' %(os.path.join(outputDirContent, exclusion)))
                                '''

                                try:
                                    menuMakeLive.addAction('view', self.viewVersion(os.path.join(versionPath, outputDirContent[0])))
                                    try:
                                        if self.mainWindow.rv == True:
                                            menuMakeLive.addAction('compare to live', self.compareVersion(os.path.join(versionPath, outputDirContent[0]), os.path.join(liveDir, outputDirContent[0])))
                                            menuMakeLive.addAction('difference to live', self.differenceVersion(os.path.join(versionPath, outputDirContent[0]), os.path.join(liveDir, outputDirContent[0])))

                                    except:
                                        print 'compare/difference to live version not possible'
                                except:
                                    print 'not possible to view SEQ. emty?'
                        except IndexError, e:
                            print 'error captured', e

                            #menuMakeLive.addAction('compare to live', self.compareVersion(os.path.join(outputDir, version, outputDirContent[0]), os.path.join(liveDir, outputDirContent[0])))

                            #self.versionMenu.addAction('view live', self.viewLive(os.path.join(liveDir, liveDirContent[0])))

                        menuMakeLive.addAction('open directory', self.mainWindow.locateContentCallback(versionPath))

                        deleteVersionAction = menuMakeLive.addAction('delete version', self.deleteContentCallback(versionPath))

                        makeCurrentAction = menuMakeLive.addAction('make current', self.makeCurrentCallback(versionPath))


                        if self.currentPlatform == 'Darwin' or self.currentPlatform == 'Linux':
                            if os.path.join(outputDir, version) == os.path.join(outputDir, os.readlink(os.path.join(outputDir, 'current'))):
                                deleteVersionAction.setEnabled(False)
                            else:
                                deleteVersionAction.setEnabled(True)
                        elif self.currentPlatform == 'Windows':


                            print os.path.join(outputDir, version)
                            print os.path.join(outputDir, 'current')
                            print os.path.join(outputDir, os.path.realpath(os.path.join(outputDir, 'current')))



                        makeLiveAction = menuMakeLive.addAction('make live', self.makeLiveCallback(versionPath))


                        #print liveDir
                        #print outputLabel
                        #print 'test', os.path.join(os.path.dirname(os.path.dirname(liveDir)), 'output', outputLabel, version)
                        #print os.path.basename(os.readlink(liveDir))
                        #print 'livedir   =', os.path.join(outputDir, os.path.basename(os.readlink(liveDir)))
                        #print 'outputdir =', os.path.join(outputDir, version)



                        if len(outputDirContent) > 0:
                            makeLiveAction.setEnabled(True)


                            #outputDir = objectClicked.getOutputDir()

                            #outputLabel = objectClicked.getLabel()

                            #liveDir = objectClicked.getLiveDir()
                        else:
                            makeLiveAction.setEnabled(False)
                            makeLiveAction.setText(makeLiveAction.text() + ' (no content)')

                        try:
                            if os.path.join(outputDir, os.path.basename(os.readlink(liveDir))) == os.path.join(outputDir, version):
                                makeLiveAction.setEnabled(False)
                                makeLiveAction.setText(makeLiveAction.text() + ' (already live)')
                                deleteVersionAction.setEnabled(False)

                        except OSError, e:
                            print 'no live version found:', e
                            makeLiveAction.setEnabled(True)


                        if self.currentPlatform == 'Darwin' or self.currentPlatform == 'Linux':
                            if versionPath == os.path.join(outputDir, os.path.basename(os.readlink(os.path.join(outputDir, 'current')))):
                                makeCurrentAction.setEnabled(False)
                        elif self.currentPlatform == 'Windows':
                            if versionPath == os.path.join(outputDir, os.path.basename(os.path.realpath(os.path.join(outputDir, 'current')))):
                                makeCurrentAction.setEnabled(False)


        except AttributeError, e:
            print 'error captured:', e

        self.menu.move(QCursor.pos())
        self.menu.show()



    def denyVersionCallback(self, versionPath):
        def callback():
            self.denyVersion(versionPath)
        return callback

    def denyVersion(self, versionPath):
        approveRequestFilePath = os.path.join(versionPath, 'waiting')

        try:
            os.remove(approveRequestFilePath)
        except:
            pass

        denyVersionFilePath = os.path.join(versionPath, 'denied')
        denyVersionFile = open(denyVersionFilePath, 'a')
        denyVersionFile.write(self.mainWindow.user)
        # self.menu.show()

    def approveRequestCallback(self, versionPath):
        def callback():
            self.approveRequest(versionPath)
        return callback

    def approveRequest(self, versionPath):
        denyVersionFilePath = os.path.join(versionPath, 'denied')

        try:
            os.remove(denyVersionFilePath)
        except:
            pass

        approveRequestFilePath = os.path.join(versionPath, 'waiting')
        approveRequestFile = open(approveRequestFilePath, 'a')
        approveRequestFile.write(self.mainWindow.user)
        approveRequestFile.close()

    def removeApproveRequestVersionCallback(self, versionPath):
        def callback():
            self.removeApproveRequestVersion(versionPath)
        return callback

    def removeApproveRequestVersion(self, versionPath):
        approveRequestFilePath = os.path.join(versionPath, 'waiting')
        os.remove(approveRequestFilePath)

    def removeApproveVersionCallback(self, versionPath):
        def callback():
            self.removeApproveVersion(versionPath)
        return callback

    def removeApproveVersion(self, versionPath):
        approveFilePath = os.path.join(versionPath, 'approved')
        os.remove(approveFilePath)

    def approveVersionCallback(self, versionPath):
        def callback():
            self.approveVersion(versionPath)
        return callback

    def approveVersion(self, versionPath):
        approveRequestFilePath = os.path.join(versionPath, 'waiting')

        try:
            os.remove(approveRequestFilePath)
        except:
            pass

        approveFilePath = os.path.join(versionPath, 'approved')
        approveFile = open(approveFilePath, 'a')
        approveFile.write(self.mainWindow.user)
        approveFile.close()


    def cleanUpOutputProc(self, portOutput):
        outputDir = portOutput.getOutputDir()
        outputVersions = self.getVersions(outputDir)
        #print outputVersions
        outputVersions.remove('current')
        for exclusion in self.exclusions:
            try:
                outputVersions.remove(exclusion)
            except:
                pass
        #print outputVersions
        currentVersion = os.path.realpath(os.path.join(outputDir, 'current'))
        outputVersions.remove(os.path.basename(currentVersion))
        #print outputVersions
        #print currentVersion
        liveDir = portOutput.getLiveDir()
        #print liveDir

        if os.path.exists(liveDir):
            liveDirDest = os.path.realpath(liveDir)
            liveVersion = os.path.basename(liveDirDest)
            #print liveDirDest
            #print liveVersion
            try:
                outputVersions.remove(liveVersion)
            except:
                print 'outputCurrent = live'

        else:
            print 'no liveDir'

        for outputVersion in outputVersions:
            #print 'need to delete %s' %(os.path.join(outputDir, outputVersion))
            self.deleteContent(os.path.join(outputDir, outputVersion))
            print '%s removed' %(os.path.join(outputDir, outputVersion))
        print 'output %s cleaned up' %(portOutput.getLabel())

    def cleanUpNodeCallback(self, node):
        def callback():
            self.cleanUpNode(node)
        return callback

    def cleanUpNode(self, node):
        reply = QMessageBox.warning(self.mainWindow, str('about to cleanup item'), str('are you sure to \ncleanup all outputs of %s?' %(node.getLabel())), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for output in node.outputList:
                self.cleanUpOutputProc(output)
            #print node.outputs
            #print node.outputList

    def cleanUpOutputCallback(self, portOutput):
        def callback():
            self.cleanUpOutput(portOutput)
        return callback

    def cleanUpOutput(self, portOutput):

        #print portOutput.getLabel()

        reply = QMessageBox.warning(self.mainWindow, str('about to cleanup item'), str('are you sure to \ncleanup %s?' %(portOutput.getLabel())), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        #print yes


        if reply == QMessageBox.Yes:
            self.cleanUpOutputProc(portOutput)

    def cloneNodeCallback(self, node):
        def callback():
            self.cloneNode(node)

        return callback()

    def cloneNode(self, node):
        print 'clone node not yet working'

    def makeLiveCallback(self, versionDir):
        def callback():
            #print versionDir
            cwd = os.getcwd()

            outputDir = os.path.basename(os.path.dirname(versionDir))
            #print outputDir

            liveDir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(versionDir))), 'live')
            #print liveDir

            os.chdir(liveDir)

            if os.path.islink(outputDir):
                os.unlink(outputDir)


            if self.currentPlatform == "Darwin" or self.currentPlatform == "Linux":
                os.symlink(os.path.relpath(versionDir, liveDir), outputDir)
            elif self.currentPlatform == "Windows":
                cmdstring = str("mklink /D " + outputDir + " " + os.path.relpath(versionDir, liveDir))
                #print 'Win cmdstring = %s' %(cmdstring)
                #os.chdir(os.path.dirname(endItemInputDir))
                os.system(cmdstring)


            os.chdir(cwd)

        return callback

    def makeCurrentCallback(self, currentDir):
        def callback():
            self.makeCurrent(currentDir)
        return callback

    def makeCurrent(self, currentDir):
        fullOutputDir = os.path.dirname(currentDir)

        try:
            if self.currentPlatform == "Darwin":
                os.unlink(os.path.join(fullOutputDir, 'current'))
            elif self.currentPlatform == "Windows":
                os.rmdir(os.path.join(fullOutputDir, 'current'))
        except:
            print 'cannot remove symlink or not available'

        cwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(currentDir)))

        if self.currentPlatform == "Darwin":
            # TODO: need to create relative links

            os.symlink(os.path.basename(currentDir), 'current')

        elif self.currentPlatform == "Windows":
            logging.info('creating windows symlink to %s' %(os.path.join(os.path.dirname(currentDir))))

            cmdstring = str("mklink /D " + os.path.join(os.path.dirname(currentDir), 'current') + " " + currentDir)

            os.system(cmdstring)

        os.chdir(cwd)

    def createNewVersion(self, fullOutputDir):
        newVersion = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
        newVersionDir = os.path.join(fullOutputDir, newVersion)
        os.makedirs(newVersionDir, mode=0777)
        open(os.path.join(fullOutputDir, newVersion, os.path.basename(fullOutputDir)), 'a').close()

        self.makeCurrent(newVersionDir)

    def createNewVersionCallback(self, fullOutputDir):
        def callback():
            self.createNewVersion(fullOutputDir)
        return callback

    def getVersions(self, fullOutputDir):
        versions = os.listdir(fullOutputDir)
        for version in versions:
            if version in self.exclusions:
                try:
                    os.remove(os.path.join(fullOutputDir, version))
                    versions.remove(version)
                    logging.info('exclusion found and removed: %s' %(os.path.join(fullOutputDir, version)))
                except:
                    versions.remove(version)
                    logging.warning('exclusion found but not removed: %s' %(os.path.join(fullOutputDir, version)))
        return versions

    def foo(self, arg):
        print arg

    def fooCallback(self, arg):
        def callback():
            print arg
        return callback

    def newOutputAuto(self, node, defaultOutput):
        # currentContent = str(self.mainWindow._current_content)

        nodeRootDir = node.getNodeRootDir()

        newOutputDir = os.path.join(str(nodeRootDir), 'output', str(defaultOutput))

        os.makedirs(newOutputDir, mode=0777)

        self.createNewVersion(newOutputDir)

    def newOutputDialog(self, node):

        currentContent = str(self.mainWindow._current_content)
        # currentProject = str(self.mainWindow.projectComboBox.currentText())
        outputs = self.mainWindow._outputs

        outputDir = os.path.join(self.projectsRoot, currentContent, str(node.data(0)), 'output')

        print node._label

        text, ok, outputIndex = newOutputUI.getNewOutputData(outputDir, outputs, self.mainWindow, node)

        if ok:

            nodeRootDir = node.getNodeRootDir()

            newOutputDir = os.path.join(str(nodeRootDir), 'output', str(text))

            if os.path.exists(newOutputDir):
                node.sendFromNodeToBox('--- output already exists' + '\n')
                
            else:
                node.newOutput(self, str(text))
                os.makedirs(newOutputDir, mode=0777)

                self.createNewVersion(newOutputDir)

                node.sendFromNodeToBox(str(datetime.datetime.now()))
                node.sendFromNodeToBox(':' + '\n')
                node.sendFromNodeToBox('--- new output created' + '\n')

    def newOutputDialogOld(self, node):
        nodeLabel = node.getLabel()

        text, ok = QInputDialog.getText(self.mainWindow, 'create new output in %s' %nodeLabel, 'enter output name:')

        if ok:
            nodeRootDir = node.getNodeRootDir()

            newNodeDir = os.path.join(str(nodeRootDir), 'output', str(text))
            
            if os.path.exists(newNodeDir):
                node.sendFromNodeToBox('--- output already exists' + '\n')
                
            else:
                # output = node.newOutput(self, str(text))
                os.makedirs(newNodeDir, mode=0777)
                node.sendFromNodeToBox(str(datetime.datetime.now()))
                node.sendFromNodeToBox(':' + '\n')
                node.sendFromNodeToBox('--- new output created' + '\n')

    def newLoaderDialog(self, pos):
        def callback():
            currentProject = str(self.mainWindow.projectComboBox.currentText())

            currentContent = str(self.mainWindow._current_content)




            activeItemPath = os.path.join(self.mainWindow._projects_root, self.mainWindow._current_project, 'content', self.mainWindow._current_content['content'], self.mainWindow._current_content_item)

            ok, loaderName, sourceSaverLocation = newLoaderUI.getNewLoaderData(activeItemPath, self.mainWindow)

            if ok:
                newLoaderPath = os.path.join(activeItemPath, loaderName)

                srcParentDirs = os.sep.join([str(os.path.relpath(self.projectsRoot, sourceSaverLocation))]) + os.sep

                src = os.sep.join([str(os.path.relpath(sourceSaverLocation, self.projectsRoot))])

                relPath = os.sep.join([str(srcParentDirs + src)])

                inputLinkOutput = os.path.join(newLoaderPath, 'output')
                inputLinkLive = os.path.join(newLoaderPath, 'live')

                if not os.path.exists(newLoaderPath):
                    propertyNode = ET.Element('propertyNode')

                    posX = str(int(float(round(pos.x()))))
                    posY = str(int(float(round(pos.y()))))

                    ET.SubElement(propertyNode, 'node', { 'positionX':posX, 'positionY':posY })
                    
                    # tree = ET.ElementTree(propertyNode)
                    
                    propertyNodePath = os.path.join(newLoaderPath, 'propertyNode.xml')

                    os.makedirs(newLoaderPath, mode=0777)

                    os.makedirs(os.path.join(newLoaderPath, 'input'), mode=0777)

                    os.symlink(os.path.join(relPath, 'input'), inputLinkOutput)
                    os.symlink(os.path.join(relPath, 'input'), inputLinkLive)

                    xmlDoc = open(propertyNodePath, 'w')

                    xmlDoc.write('<?xml version="1.0"?>')
                    xmlDoc.write(ET.tostring(propertyNode))

                    xmlDoc.close()
                    
                    newNode = node(self.mainWindow, self, propertyNodePath)
                    newNode.addText(self, loaderName)

                else:
                    print 'asset loader already exists'
        return callback

    def newSaverDialog(self, pos):
        def callback():

            # currentContent = str(self.mainWindow._current_content)
            # currentProject = str(self.mainWindow.projectComboBox.currentText())

            
            # nodeDir = os.path.join(self.projectsRoot, currentContent)

            # print nodeDir

            # projectsRoot = str(self.mainWindow._projects_root)
            # currentTarget = str(self.mainWindow._current_content)
            # currentContent = str(self.mainWindow._current_content)
            # print currentContent.split(os.sep)[2]
            # currentProject = str(self.mainWindow.projectComboBox.currentText())

            # print self.mainWindow._current_content['content']
            # self.mainWindow._current_content

            newSaverName = 'SVR_' + self.mainWindow._current_content['abbreviation'] + '__' + self.mainWindow._current_content_item

            # if currentContent.split(os.sep)[2] == 'assets':
            #
            #     newSaverName = 'SVR_AST__' + os.path.basename(currentContent)
            #
            # elif currentContent.split(os.sep)[2] == 'shots':
            #
            #     newSaverName = 'SVR_SHT__' + os.path.basename(currentContent)

            # os.path.join(self.mainWindow._projects_root, self.mainWindow._current_project, 'content', self.mainWindow._current_content['content']

            newSaverPath = os.path.join(self.mainWindow._projects_root, self.mainWindow._current_project, 'content', self.mainWindow._current_content['content'], self.mainWindow._current_content_item, newSaverName)

            print newSaverPath

            if not os.path.exists(newSaverPath):

                #print newNodePath
                propertyNode = ET.Element('propertyNode')
                
                #print pos.x()
                #print pos.y()
                
                posX = str(int(float(round(pos.x()))))
                posY = str(int(float(round(pos.y()))))

                ET.SubElement(propertyNode, 'node', { 'positionX':posX, 'positionY':posY })
                #ET.SubElement(propertyNode, 'positionX', { 'value':posX })
                #ET.SubElement(propertyNode, 'positionY', { 'value':posY })

                #print  toolFamily, toolVendor, toolVersion, toolArch

                #ET.SubElement(propertyNode, 'task', { 'family':toolFamily, 'vendor':toolVendor, 'version':toolVersion, 'arch':toolArch, 'nodetask':toolTask })




                

                
                
                
                tree = ET.ElementTree(propertyNode)
                
                propertyNodePath = os.path.join(newSaverPath, 'propertyNode.xml')
                #print propertyNodePath
                

                os.makedirs(newSaverPath, mode=0777)
                #os.makedirs(os.path.join(newNodePath, 'project'), mode=0777)
                os.makedirs(os.path.join(newSaverPath, 'output'), mode=0777)
                #os.makedirs(os.path.join(newNodePath, 'live'), mode=0777)
                os.makedirs(os.path.join(newSaverPath, 'input'), mode=0777)
                #print os.path.exists(newNodePath)

                #for toolDirectory in toolDirectories:
                #    os.makedirs(os.path.join(newNodePath, 'project', toolDirectory), mode=0777)

                

                #if not toolTemplate == 'None':

                #    shutil.copyfile(os.path.join('src', 'template_documents', toolTemplate), os.path.join(newNodePath, 'project', str(text + '.' + '0000' + os.path.splitext(toolTemplate)[1])))


                
                
                #print ET.tostring(propertyNode) 
                #if not os.path.exists(propertyNodePath): 
                xmlDoc = open(propertyNodePath, 'w')
                 
                #print ET.tostring(propertyNode)
                
                xmlDoc.write('<?xml version="1.0"?>')
                xmlDoc.write(ET.tostring(propertyNode))
                #ET.ElementTree(propertyNode).write(xmlDoc)
                #tree.write(xmlDoc)
                
                
                xmlDoc.close()
                
                newNode = node(self.mainWindow, self, propertyNodePath)
                newNode.addText(self, newSaverName)

            else:
                print 'asset saver already exists'

        return callback

    def new_node_dialog(self, pos):
        def callback():
            tasks = self.mainWindow.getTasks()

            meta_tool = {}
            meta_task = {}
            
            node_dir = os.path.join(self.mainWindow._projects_root,
                                    self.mainWindow._current_project,
                                    'content',
                                    self.mainWindow._current_content['content'],
                                    self.mainWindow._current_content_item)

            node_name, ok, tool_data, task_index = newNodeUI.getNewNodeData(node_dir, tasks, self.mainWindow)

            taskNode = tasks[task_index]
            # toolTask = taskNode[2][1]
 
            if ok:
                new_node_path = os.path.join(node_dir, str(node_name))

                pos_x = str(int(float(round(pos.x()))))
                pos_y = str(int(float(round(pos.y()))))

                meta_task['pos_x'] = pos_x
                meta_task['pos_y'] = pos_y

                meta_task['creator'] = self.mainWindow.user
                meta_task['operating_system'] = self.mainWindow.operating_system

                meta_tool['family'] = tool_data['family']
                meta_tool['architecture_fallback'] = tool_data['architecture_fallback']
                meta_tool['abbreviation'] = tool_data['abbreviation']
                meta_tool['architecture'] = tool_data['architecture']
                meta_tool['vendor'] = tool_data['vendor']
                meta_tool['release_number'] = tool_data['release_number']

                meta_node_path = os.path.join(new_node_path, 'meta_task.json')
                meta_tool_path = os.path.join(new_node_path, 'meta_tool.json')

                # posX = pos_x
                # posY = pox_y
                #
                # property_node = ET.Element('propertyNode')
                #
                # ET.SubElement(property_node, 'node', { 'positionX':posX, 'positionY':posY })
                #
                # ET.SubElement(property_node, 'task', {'family':tool_data['family'],
                #                                       'vendor':tool_data['vendor'],
                #                                       'version':tool_data['release_number'],
                #                                       'arch':tool_data['architecture'],
                #                                       'nodetask':toolTask,
                #                                       })
                #
                # property_node_path = os.path.join(new_node_path, 'propertyNode.xml')

                os.makedirs(new_node_path, mode=0777)
                os.makedirs(os.path.join(new_node_path, 'project'), mode=0777)
                os.makedirs(os.path.join(new_node_path, 'output'), mode=0777)
                os.makedirs(os.path.join(new_node_path, 'live'), mode=0777)
                os.makedirs(os.path.join(new_node_path, 'input'), mode=0777)

                for tool_directory in tool_data['project_directories']:
                    os.makedirs(os.path.join(new_node_path, 'project', tool_directory), mode=0777)

                if tool_data['project_template'] is not None:
                    extension = os.path.splitext(tool_data['project_template'])[1]
                    src_path = os.path.join('src', 'template_documents', tool_data['project_template'])
                    dst_path = os.path.join(new_node_path, 'project', str(node_name + '.' + '0000' + extension))
                    shutil.copyfile(src_path, dst_path)

                if tool_data['project_workspace'] is not None:
                    extension = os.path.splitext(tool_data['project_workspace'])[1]
                    # extension = str(tool_data['project_workspace']).split('_')[-1]
                    src_path = os.path.join('src', 'template_documents', tool_data['project_workspace'])
                    dst_path = os.path.join(new_node_path, extension)
                    shutil.copyfile(src_path, dst_path)

                # xml_doc = open(property_node_path, 'w')
                #
                # xml_doc.write('<?xml version="1.0"?>')
                # xml_doc.write(ET.tostring(property_node))
                #
                # xml_doc.close()

                with open(meta_node_path, 'w') as outfile:
                    json.dump(meta_task, outfile)

                with open(meta_tool_path, 'w') as outfile:
                    json.dump(meta_tool, outfile)
                
                new_node = node(self.mainWindow, self, property_node_path)
                new_node.addText(self, str(node_name))

                for tool_default_output in tool_data['default_outputs']:
                    self.newOutputAuto(new_node, tool_default_output)

        return callback

    def removeObject(self, item):



        reply = QMessageBox.warning(self.mainWindow, str('about to delete item'), str('are you sure to \ndelete %s %s \nand its contents?' %(item.data(2), item.label)), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        #print yes

        if reply == QMessageBox.Yes:

            if isinstance(item, node) :

                #print 'self.children() = %s' %self.children()
                #node.outputList
                tempOutputList = item.outputList
                #node.inputList
                tempInputList = item.inputList


                for output in tempOutputList:
                    try:
                        self.removeOutput(output)
                    except:
                        pass

                for input in tempInputList:
                    self.removeInput(input)


                del tempOutputList
                del tempInputList


                nodeRootDir = item.getNodeRootDir()
                #print 'nodeRootDir = %s' %nodeRootDir
                shutil.rmtree(nodeRootDir)
                self.removeItem(item)

                #print 'self.children() = %s' %self.children()

            elif isinstance(item, portOutput):
                self.removeOutput(item)

            elif isinstance(item, portInput):
                inputDir = item.getInputDir()

                try:
                    if self.currentPlatform == "Darwin":
                        os.unlink(inputDir)
                    elif self.currentPlatform == "Windows":
                        os.rmdir(inputDir)
                        # windows removes the contents of the connected output folder as well using shutil.rmtree :(((
                        # and if inputDir is not empty, it cannot remove the link/directory because it's not empty :(((
                        # shutil.rmtree(inputDir)
                except:
                    print 'cannot remove symlink 1234'

                #os.rmdir(inputDir)
                self.removeInput(item)

    def removeObjectCallback(self, item):
        def callback():
            self.removeObject(item)

        return callback
    
    def removeOutput(self, item):
        tempInputsList = list(item.inputs)
        for port in tempInputsList:
            connectionLine = port.connection[0]
            self.removeItem(connectionLine)
            port.connection.remove(connectionLine)

            output = port.output[0]
            output.inputs.remove(port)

            port.parentItem().inputs.remove(port)
            port.parentItem().incoming.remove(output)
            inputDir = port.getInputDir()

            try:
                if self.currentPlatform == "Darwin":
                    os.unlink(inputDir)
                elif self.currentPlatform == "Windows":
                    os.rmdir(inputDir)
            except:
                print 'cannot remove symlink 2345'
            self.removeItem(port)

        del tempInputsList
        
        item.parentItem().outputs.remove(item)

        outputDir = item.getOutputDir()
        liveDir = item.getLiveDir()
        if os.path.exists(liveDir):
            os.unlink(liveDir)
        shutil.rmtree(outputDir)

        self.removeItem(item)

    def removeInput(self, item):
        try:
            self.removeItem(item.connection[0])
            item.connection.remove(item.connection[0])

            output = item.output[0]
            output.inputs.remove(item)

            item.parentItem().inputs.remove(item)
            item.parentItem().incoming.remove(output)
            self.removeItem(item)
        
        except:
            print 'port is input portal! mustn\'t delete!'

    def newNode(self, pos):
        def callback():
            node(self.mainWindow, pos, self)

        return callback
    
    def printContextMenuAction(self, item):
        def callback():
            pass
            # from http://stackoverflow.com/questions/6682688/python-dynamic-function-generation
            # print item
        return callback

    def mousePressEvent(self, event):
        pos = event.scenePos()

        # print 'pos = %s' %pos
        
        if event.button() == Qt.MidButton:
            # print 'MidButton'
            pass
          
        elif event.button() == Qt.LeftButton:
            # print 'LeftButton'
            item = self.itemAt(event.scenePos())
            if event.button() == Qt.LeftButton and (isinstance(item, portOutput)):
                self.line = QGraphicsLineItem(QLineF(event.scenePos(), event.scenePos()))
                self.addItem(self.line)
            elif event.button() == Qt.LeftButton and (isinstance(item, portOutputButton)):
                self.newOutputDialog(item.parentItem())
                
            elif event.button() == Qt.LeftButton and (isinstance(item, node)):
                pass
            else:
                self.nodeDeselect.emit()

            modifiers = QApplication.keyboardModifiers()
            pos = event.scenePos()
            if modifiers == Qt.ControlModifier:
                # print "Control + Click: (%d, %d)" % (pos.x(), pos.y())
                pass

            else:
                pass
                # print "Click: (%d, %d)" % (pos.x(), pos.y())

        elif event.button() == Qt.RightButton:
            # print 'RightButton'

            self.contextMenu(pos)

        else:
            print 'def mousePressEvent problem'


        super(SceneView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.line:
            newLine = QLineF(self.line.line().p1(), event.scenePos())
            self.line.setLine(newLine)
        super(SceneView, self).mouseMoveEvent(event)
        self.update()

    def mouseReleaseEvent(self, event):
        if self.line:
            try:
                startItems = self.items(self.line.line().p1())
                parentNodeStartItem = startItems[0].parentItem()
            except:
                return

            if len(startItems) and startItems[0] == self.line:
                startItems.pop(0)
            
            endItems = self.items(self.line.line().p2())
             
            if len(endItems) and endItems[0] == self.line:
                endItems.pop(0)

            self.removeItem(self.line)

            try:

                if (isinstance(endItems[0], portInput)):
                    parentNode = endItems[0].parentItem()
                    # print 'parentNode.childItems() = %s' %parentNode.childItems()

                    if startItems[0] in endItems[0].parentItem().incoming:
                        parentNode.sendFromNodeToBox(str(datetime.datetime.now()))
                        parentNode.sendFromNodeToBox(':' + '\n')
                        parentNode.sendFromNodeToBox('--- this connection already exists, you dumbass' + '\n')

                    elif startItems[0].parentItem() == endItems[0].parentItem():
                        parentNode.sendFromNodeToBox(str(datetime.datetime.now()))
                        parentNode.sendFromNodeToBox(':' + '\n')
                        parentNode.sendFromNodeToBox('--- don\'t connect to itself, you moron' + '\n')

                    elif len(endItems[0].connection) == 0:
                        if os.path.basename(startItems[0].parentItem().getNodeRootDir()).startswith('LDR') \
                                        and os.path.basename(endItems[0].parentItem().getNodeRootDir()).startswith('SVR'):
                            parentNode.sendFromNodeToBox('--- don\'t connect loader to saver' + '\n')
                            logging.info('tried to connect loader to saver, which is not possible')
                        else:
                            connectionLine = bezierLine(self.mainWindow, self, startItems[0], endItems[0], QPainterPath(startItems[0].scenePos()))

                            endItems[0].parentItem().inputs.append(endItems[0])
                            endItems[0].connection.append(connectionLine)
                            endItems[0].output.append(startItems[0])
                            endItems[0].parentItem().incoming.append(startItems[0])
                            startItems[0].inputs.append(endItems[0])

                            startItemRootDir = startItems[0].parentItem().getNodeRootDir()

                            endItemRootDir = endItems[0].parentItem().getNodeRootDir()

                            startItemOutputLabel = os.path.basename(startItems[0].getOutputDir())

                            startItemOutputDir = os.path.join(str(startItemRootDir), 'live', str(startItemOutputLabel))
                            endItemInputDir = os.path.join(str(endItemRootDir), 'input', str(startItemOutputLabel))

                            # currentContent = str(self.mainWindow._current_content)

                            cwd = os.getcwd()
                            dst = endItemInputDir

                            srcParentDirs = os.sep.join([str(os.path.relpath(self.projectsRoot, os.path.dirname(dst)))]) + os.sep

                            src = os.sep.join([str(os.path.relpath(startItemOutputDir, self.projectsRoot))])

                            relPath = os.sep.join([str(srcParentDirs + src)])

                            if len(os.path.basename(dst).split('.')) > 1:
                                inputLink = os.path.dirname(dst) + os.sep + os.path.basename(relPath)

                            else:
                                inputLink = os.path.dirname(dst) + os.sep + os.path.basename(os.path.dirname(os.path.dirname(startItemRootDir))) + '.' + os.path.basename(os.path.dirname(startItemRootDir)) + '.' + os.path.basename(startItemRootDir) + '.' + os.path.basename(dst)
                            if self.currentPlatform == "Darwin":
                                try:
                                    os.symlink(relPath, inputLink)
                                except:
                                    pass
                                endItems[0].setInputDir(inputLink)
                            elif self.currentPlatform == "Windows":
                                cmdstring = "mklink /D " + inputLink + " " + src
                                os.chdir(os.path.dirname(endItemInputDir))
                                os.system(cmdstring)
                                os.chdir(cwd)

                                endItems[0].setInputDir(inputLink)

                            self.addItem(connectionLine)

                            endItems[0].parentItem().newInput(self)

                    else:
                        parentNode.sendFromNodeToBox(str(datetime.datetime.now()))
                        parentNode.sendFromNodeToBox(':' + '\n')
                        parentNode.sendFromNodeToBox('--- this input port is already in use. obviously.' + '\n')
                        parentNode.sendFromNodeToBox('--- your iq is dropping...' + '\n')

                else:
                    parentNodeStartItem = startItems[0].parentItem()

                    parentNodeStartItem.sendFromNodeToBox(str(datetime.datetime.now()))
                    parentNodeStartItem.sendFromNodeToBox(':' + '\n')
                    parentNodeStartItem.sendFromNodeToBox('--- endItem is not an input :(' + '\n')
                    parentNodeStartItem.sendFromNodeToBox('--- no endItem chosen' + '\n')

            except IndexError, e:
                print 'error captured:', e
        
        self.line = None

        super(SceneView, self).mouseReleaseEvent(event)