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

import settings as SETTINGS

# class Signals(QObject):
#     trigger = pyqtSignal(str)


class SceneView(QGraphicsScene):
    textMessage = pyqtSignal(str)
    nodeSelect = pyqtSignal(object)
    nodeDeselect = pyqtSignal()
    
    def __init__(self, main_window, parent=None):
        super(SceneView, self).__init__(parent)

        self.main_window = main_window
        self.line = None
        self.node_list = []

        self.menu = None

    def addToNodeList(self, node):
        self.node_list.append(node)

    # @property
    # def _node_list(self):
    #     return self.node_list

    # def getNodeList(self):
    #     return self.node_list
        
    def clearNodeList(self):
        self.node_list = []

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
            subprocess.Popen([self.main_window.sequence_exec, imgFile], shell=False)
        return callback

    def compareVersion(self, imgFile, liveImgFile):
        def callback():
            subprocess.Popen([self.main_window.sequence_exec, imgFile, '-wipe', liveImgFile], shell=False)
        return callback

    def differenceVersion(self, imgFile, liveImgFile):
        def callback():
            subprocess.Popen([self.main_window.sequence_exec, imgFile, '-diff', liveImgFile], shell=False)
        return callback

    def deleteContentCallback(self, path):
        def callback():
            self.deleteContent(path)
        return callback

    def deleteContent(self, path):
        shutil.rmtree(path)

    def copyToClipboard(self, text):
        self.main_window.clipBoard.setText(text)
        print '%s copied to clipboard' %(text)

    def copyToClipboardCallback(self, text):
        def callback():
            self.copyToClipboard(text)
        return callback

    # @property
    # def _item_clicked(self, event):
    #     pos = event.scenePos()
    #     return self.itemAt(pos)
    #
    # @property
    # def _node_clicked(self, event):
    #     pos = event.scenePos()
    #     object_clicked = self.itemAt(pos)
    #     # try:
    #     # node specific context menu items
    #     if isinstance(object_clicked, node) \
    #             or isinstance(object_clicked.parentItem(), node) \
    #             or isinstance(object_clicked.parentItem().parentItem(), node) \
    #             or isinstance(object_clicked.parentItem().parentItem().parentItem(), node):
    #
    #         if isinstance(object_clicked, node):
    #             object_clicked = object_clicked
    #         elif isinstance(object_clicked.parentItem(), node):
    #             object_clicked = object_clicked.parentItem()
    #         elif isinstance(object_clicked.parentItem().parentItem(), node):
    #             object_clicked = object_clicked.parentItem().parentItem()
    #         elif isinstance(object_clicked.parentItem().parentItem().parentItem(), node):
    #             object_clicked = object_clicked.parentItem().parentItem().parentItem()
    #
    #     return object_clicked

    def contextMenu(self, pos):
        self.menu = QMenu()

        object_clicked = self.itemAt(pos)

        # items = []

        contentDirs = os.listdir(os.path.join(self.main_window.projects_root, self.main_window._current_project, 'content', self.main_window._current_content['content']))

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
            if isinstance(object_clicked, node) \
                    or isinstance(object_clicked.parentItem(), node) \
                    or isinstance(object_clicked.parentItem().parentItem(), node) \
                    or isinstance(object_clicked.parentItem().parentItem().parentItem(), node):

                if isinstance(object_clicked, node):
                    node_clicked = object_clicked
                elif isinstance(object_clicked.parentItem(), node):
                    node_clicked = object_clicked.parentItem()
                elif isinstance(object_clicked.parentItem().parentItem(), node):
                    node_clicked = object_clicked.parentItem().parentItem()
                elif isinstance(object_clicked.parentItem().parentItem().parentItem(), node):
                    node_clicked = object_clicked.parentItem().parentItem().parentItem()

                self.menu_node = self.menu.addMenu('node')

                if not node_clicked.label.startswith('LDR') and not node_clicked.label.startswith('SVR'):
                    self.menu_node.addAction('open node directory', lambda: self.main_window.locate_content(node_clicked.getNodeRootDir()))

                    if not os.path.exists(os.path.join(node_clicked.getNodeRootDir(), 'locked')):
                        self.menu_node.addSeparator()
                        self.menu_node.addAction('run', lambda: node_clicked.mouseDoubleClickEvent())
                        self.menu_node.addSeparator()
                        self.menu_node.addAction('cleanup node', self.cleanUpNodeCallback(node_clicked))
                        self.menu_node.addAction('delete node', self.removeObjectCallback(node_clicked))

                        if os.path.exists(os.path.join(node_clicked.getNodeRootDir(), 'checkedOut')):
                            self.menu_node.addSeparator()
                            self.menu_node.addAction('check in node', self.main_window.check_in_callback(node_clicked))

                        else:
                            self.menu_node.addSeparator()
                            self.menu_node.addAction('check out node', self.main_window.check_out_callback(node_clicked))

                elif node_clicked.label.startswith('LDR'):

                    self.menu_node.addAction('open source tree', lambda: self.main_window.get_content(None, node_label=node_clicked.getLabel()))
                    self.menu_node.addSeparator()
                    self.menu_node.addAction('delete loader', self.removeObjectCallback(node_clicked))

                # elif node_clicked.label.startswith('LDR_SHT'):
                #     #self.menu_node.addAction('open shot', lambda: self.foo(node_clicked.getNodeRootDir()))
                #     self.menu_node.addAction('open shot tree', lambda: self.main_window.get_content(None, node_label=node_clicked.getLabel()))
                #     self.menu_node.addSeparator()
                #     self.menu_node.addAction('delete shot loader', self.removeObjectCallback(node_clicked))

                elif node_clicked.label.startswith('SVR'):
                    self.menu_node.addAction('delete saver', self.removeObjectCallback(node_clicked))
                    self.menu_node.addSeparator()
                    self.menu_node.addAction('check out tree', self.main_window.check_out_callback(node_clicked))

                # elif node_clicked.label.startswith('SVR_SHT'):
                #     self.menu_node.addAction('delete shot saver', self.removeObjectCallback(node_clicked))
                #     self.menu_node.addSeparator()
                #     self.menu_node.addAction('check out shot', self.main_window.check_out_callback(node_clicked))

                self.menu_node.addSeparator()

            if isinstance(object_clicked, portInput) and not object_clicked.label == None:
                self.menu_input = self.menu.addMenu('input')

                self.menu_path_ops = self.menu_input.addMenu('clipboard')
                self.menu_input.addSeparator()
                self.menu_input.addAction('delete input', self.removeObjectCallback(object_clicked))

                input_label = object_clicked.getLabel()
                input_dir = object_clicked.getInputDir()

                output_node = object_clicked.parentItem()
                output_node_root_dir = output_node.getNodeRootDir()

                self.menu_path_ops.addAction('copy input label', self.copyToClipboardCallback(input_label))
                self.menu_path_ops.addAction('copy absolute input path',  self.copyToClipboardCallback(os.path.join(input_dir, input_label)))
                self.menu_path_ops.addAction('copy relative input path',  self.copyToClipboardCallback(os.path.relpath(os.path.join(input_dir, input_label), os.path.join(output_node_root_dir))))

            if isinstance(object_clicked, portOutput) and not object_clicked.parentItem().label.startswith('LDR'):
                self.menu_output = self.menu.addMenu('output')

                self.menu_path_ops = self.menu_output.addMenu('clipboard')
                self.menu_output.addSeparator()

                output_dir = object_clicked.getOutputDir()
                output_label = object_clicked.getLabel()
                live_dir = object_clicked.getLiveDir()
                output_node_root_dir = object_clicked.getOutputRootDir()

                versions = self.getVersions(output_dir)

                self.menu_output.addAction('open output directory', lambda: self.main_window.locate_content(output_dir))

                self.menu_output.addSeparator()

                self.menu_path_ops.addAction('copy output label', self.copyToClipboardCallback(output_label))
                self.menu_path_ops.addAction('copy absolute output path',  self.copyToClipboardCallback(os.path.join(output_dir, 'current', output_label)))
                self.menu_path_ops.addAction('copy relative output path',  self.copyToClipboardCallback(os.path.relpath(os.path.join(output_dir, 'current', output_label), os.path.join(output_node_root_dir))))

                self.menu_output.addAction('cleanup output', self.cleanUpOutputCallback(object_clicked))

                if os.path.exists(live_dir):
                    self.menu_output.addAction('remove pipe (live)', self.unmakeLiveCallback(live_dir))

                self.menu_output.addAction('delete output', self.removeObjectCallback(object_clicked))
                self.menu_output.addSeparator()

                self.menu_output.addAction('create new version', self.createNewVersionCallback(output_dir))

                self.menu_output.addSeparator()

                for version in versions:
                    if not version == 'current':

                        version_path = os.path.join(output_dir, version)

                        output_dir_content = os.listdir(version_path)

                        for item in output_dir_content:
                            if item in SETTINGS.EXCLUSIONS:
                                # try:
                                os.remove(os.path.join(version_path, item))
                                output_dir_content.remove(item)
                                logging.info('exclusion found and removed: %s' %(os.path.join(version_path, item)))

                            try:
                                output_dir_content.remove('approved')
                            except ValueError, e:
                                print 'error captured:', e
                            try:
                                output_dir_content.remove('requestApproval')
                            except ValueError, e:
                                print 'error captured:', e
                            try:
                                output_dir_content.remove('denied')
                            except ValueError, e:
                                print 'error captured:', e
                        output_dir_content.remove(output_label)

                        menu_make_live = self.menu_output.addMenu(version)

                        if self.main_window.current_platform == 'Darwin' or self.main_window.current_platform == 'Linux':
                            if os.path.exists(live_dir):
                                if not object_clicked.parentItem().label.startswith('LDR'):
                                    if os.path.exists(os.path.join(output_dir, version, 'approved')):
                                        if os.path.basename(os.readlink(live_dir)) == version:
                                            menu_make_live.setIcon(QIcon('src/icons/dotActiveApproved.png'))
                                        elif not os.path.basename(os.readlink(live_dir)) == version:
                                            menu_make_live.setIcon(QIcon('src/icons/dotInactiveApproved.png'))

                                    elif os.path.exists(os.path.join(output_dir, version, 'waiting')):
                                        if os.path.basename(os.readlink(live_dir)) == version:
                                            menu_make_live.setIcon(QIcon('src/icons/dotActiveRequested.png'))
                                        elif not os.path.basename(os.readlink(live_dir)) == version:
                                            menu_make_live.setIcon(QIcon('src/icons/dotInactiveRequested.png'))

                                    elif os.path.exists(os.path.join(output_dir, version, 'denied')):
                                        if os.path.basename(os.readlink(live_dir)) == version:
                                            menu_make_live.setIcon(QIcon('src/icons/dotActiveDenied.png'))
                                        elif not os.path.basename(os.readlink(live_dir)) == version:
                                            menu_make_live.setIcon(QIcon('src/icons/dotInactiveDenied.png'))

                                    else:
                                        if os.path.basename(os.readlink(live_dir)) == version:
                                            menu_make_live.setIcon(QIcon('src/icons/dotActive.png'))
                                        elif not os.path.basename(os.readlink(live_dir)) == version:
                                            menu_make_live.setIcon(QIcon('src/icons/dotInactive.png'))

                                else:
                                    menu_make_live.setIcon(QIcon('src/icons/dotActive.png'))
                            else:
                                    menu_make_live.setIcon(QIcon('src/icons/dotInactive.png'))

                        if os.path.exists(os.path.join(version_path, 'approved')):
                            menu_make_live.addAction('remove approval', self.removeApproveVersionCallback(version_path))
                            menu_make_live.addSeparator()
                        else:
                            if not os.path.exists(os.path.join(version_path, 'denied')):
                                menu_make_live.addAction('approve', self.approveVersionCallback(version_path))
                                menu_make_live.addAction('deny', self.denyVersionCallback(version_path))

                            if os.path.exists(os.path.join(version_path, 'waiting')):
                                menu_make_live.addAction('cancel approval request', self.removeApproveRequestVersionCallback(version_path))
                            else:
                                menu_make_live.addAction('request approval', self.approveRequestCallback(version_path))

                            menu_make_live.addSeparator()

                        # if output_label.startswith('SEQ') or output_label.startswith('TEX') or output_label.startswith('PLB'):
                        # print os.path.splitext(output_dir_content[0])[1]
                        # TODO: error here
                        try:
                            if os.path.splitext(output_dir_content[0])[1] in SETTINGS.IMAGE_EXTENSIONS or os.path.splitext(output_dir_content[0])[1] in SETTINGS.MOVIE_EXTENSIONS:
                                try:
                                    menu_make_live.addAction('view', self.viewVersion(os.path.join(version_path, output_dir_content[0])))
                                    try:
                                        if self.main_window.rv == True:
                                            menu_make_live.addAction('compare to live', self.compareVersion(os.path.join(version_path, output_dir_content[0]), os.path.join(live_dir, output_dir_content[0])))
                                            menu_make_live.addAction('difference to live', self.differenceVersion(os.path.join(version_path, output_dir_content[0]), os.path.join(live_dir, output_dir_content[0])))

                                    except:
                                        print 'compare/difference to live version not possible'
                                except:
                                    print 'not possible to view SEQ. emty?'
                        except IndexError, e:
                            print 'error captured', e

                        menu_make_live.addAction('open directory', self.main_window.locate_content_callback(version_path))

                        delete_version_action = menu_make_live.addAction('delete version', self.deleteContentCallback(version_path))

                        make_current_action = menu_make_live.addAction('make current', self.makeCurrentCallback(version_path))

                        if self.main_window.current_platform == 'Darwin' or self.main_window.current_platform == 'Linux':
                            if os.path.join(output_dir, version) == os.path.join(output_dir, os.readlink(os.path.join(output_dir, 'current'))):
                                delete_version_action.setEnabled(False)
                            else:
                                delete_version_action.setEnabled(True)
                        elif self.main_window.current_platform == 'Windows':

                            print os.path.join(output_dir, version)
                            print os.path.join(output_dir, 'current')
                            print os.path.join(output_dir, os.path.realpath(os.path.join(output_dir, 'current')))

                        make_live_action = menu_make_live.addAction('make live', self.makeLiveCallback(version_path))

                        if len(output_dir_content) > 0:
                            make_live_action.setEnabled(True)

                        else:
                            make_live_action.setEnabled(False)
                            make_live_action.setText(make_live_action.text() + ' (no content)')

                        try:
                            if os.path.join(output_dir, os.path.basename(os.readlink(live_dir))) == os.path.join(output_dir, version):
                                make_live_action.setEnabled(False)
                                make_live_action.setText(make_live_action.text() + ' (already live)')
                                delete_version_action.setEnabled(False)

                        except OSError, e:
                            print 'no live version found:', e
                            make_live_action.setEnabled(True)

                        if self.main_window.current_platform == 'Darwin' or self.main_window.current_platform == 'Linux':
                            if version_path == os.path.join(output_dir, os.path.basename(os.readlink(os.path.join(output_dir, 'current')))):
                                make_current_action.setEnabled(False)
                        elif self.main_window.current_platform == 'Windows':
                            if version_path == os.path.join(output_dir, os.path.basename(os.path.realpath(os.path.join(output_dir, 'current')))):
                                make_current_action.setEnabled(False)

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
        denyVersionFile.write(self.main_window.user)
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
        approveRequestFile.write(self.main_window.user)
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
        approve_file_path = os.path.join(versionPath, 'approved')
        os.remove(approve_file_path)

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

        approve_file_path = os.path.join(versionPath, 'approved')
        approve_file = open(approve_file_path, 'a')
        approve_file.write(self.main_window.user)
        approve_file.close()

    def cleanUpOutputProc(self, portOutput):
        output_dir = portOutput.getOutputDir()
        output_versions = self.getVersions(output_dir)
        output_versions.remove('current')
        for exclusion in SETTINGS.EXCLUSIONS:
            try:
                output_versions.remove(exclusion)
            except:
                pass

        current_version = os.path.realpath(os.path.join(output_dir, 'current'))
        output_versions.remove(os.path.basename(current_version))
        live_dir = portOutput.getLiveDir()

        if os.path.exists(live_dir):
            live_dir_dest = os.path.realpath(live_dir)
            live_version = os.path.basename(live_dir_dest)
            try:
                output_versions.remove(live_version)
            except:
                print 'outputCurrent = live'

        else:
            print 'no live_dir'

        for output_version in output_versions:
            self.deleteContent(os.path.join(output_dir, output_version))
            print '%s removed' %(os.path.join(output_dir, output_version))
        print 'output %s cleaned up' %(portOutput.getLabel())

    def cleanUpNodeCallback(self, node):
        def callback():
            self.cleanUpNode(node)
        return callback

    def cleanUpNode(self, node):
        reply = QMessageBox.warning(self.main_window, str('about to cleanup item'), str('are you sure to \ncleanup all outputs of %s?' %(node.getLabel())), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for output in node.outputList:
                self.cleanUpOutputProc(output)

    def cleanUpOutputCallback(self, portOutput):
        def callback():
            self.cleanUpOutput(portOutput)
        return callback

    def cleanUpOutput(self, portOutput):
        reply = QMessageBox.warning(self.main_window, str('about to cleanup item'), str('are you sure to \ncleanup %s?' %(portOutput.getLabel())), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

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
            cwd = os.getcwd()

            output_dir = os.path.basename(os.path.dirname(versionDir))

            live_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(versionDir))), 'live')            #print live_dir

            os.chdir(live_dir)

            if os.path.islink(output_dir):
                os.unlink(output_dir)

            if self.main_window.current_platform == "Darwin" or self.main_window.current_platform == "Linux":
                os.symlink(os.path.relpath(versionDir, live_dir), output_dir)
            elif self.main_window.current_platform == "Windows":
                cmdstring = str("mklink /D " + output_dir + " " + os.path.relpath(versionDir, live_dir))
                os.system(cmdstring)

            os.chdir(cwd)

        return callback

    def makeCurrentCallback(self, currentDir):
        def callback():
            self.makeCurrent(currentDir)
        return callback

    def makeCurrent(self, currentDir):
        full_output_dir = os.path.dirname(currentDir)

        try:
            if self.main_window.current_platform == "Darwin":
                os.unlink(os.path.join(full_output_dir, 'current'))
            elif self.main_window.current_platform == "Windows":
                os.rmdir(os.path.join(full_output_dir, 'current'))
        except:
            print 'cannot remove symlink or not available'

        cwd = os.getcwd()
        os.chdir(os.path.join(os.path.dirname(currentDir)))

        if self.main_window.current_platform == "Darwin":
            # TODO: need to create relative links

            os.symlink(os.path.basename(currentDir), 'current')

        elif self.main_window.current_platform == "Windows":
            logging.info('creating windows symlink to %s' %(os.path.join(os.path.dirname(currentDir))))

            cmdstring = str("mklink /D " + os.path.join(os.path.dirname(currentDir), 'current') + " " + currentDir)

            os.system(cmdstring)

        os.chdir(cwd)

    def createNewVersion(self, full_output_dir):
        new_version = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
        new_version_dir = os.path.join(full_output_dir, new_version)
        os.makedirs(new_version_dir, mode=0777)
        open(os.path.join(full_output_dir, new_version, os.path.basename(full_output_dir)), 'a').close()

        self.makeCurrent(new_version_dir)

    def createNewVersionCallback(self, full_output_dir):
        def callback():
            self.createNewVersion(full_output_dir)
        return callback

    def getVersions(self, full_output_dir):
        versions = os.listdir(full_output_dir)
        for version in versions:
            if version in SETTINGS.EXCLUSIONS:
                try:
                    os.remove(os.path.join(full_output_dir, version))
                    versions.remove(version)
                    logging.info('exclusion found and removed: %s' %(os.path.join(full_output_dir, version)))
                except:
                    versions.remove(version)
                    logging.warning('exclusion found but not removed: %s' %(os.path.join(full_output_dir, version)))
        return versions

    def foo(self, arg):
        print arg

    def fooCallback(self, arg):
        def callback():
            print arg
        return callback

    def newOutputAuto(self, node, defaultOutput):
        node_root_dir = node.getNodeRootDir()

        new_output_dir = os.path.join(str(node_root_dir), 'output', str(defaultOutput))

        os.makedirs(new_output_dir, mode=0777)

        self.createNewVersion(new_output_dir)

    def newOutputDialog(self, node):

        # current_content = str(self.main_window._current_content)
        # currentProject = str(self.main_window.projectComboBox.currentText())
        # outputs = self.main_window.outputs

        # print self.main_window._current_content
        #
        # output_dir = os.path.join(self.main_window.projects_root, 'content', self.main_window._current_content['content'], node.data(0), 'output')
        # print output_dir

        # print node._label

        text, ok = NewOutputUI.get_new_output_data(self.main_window, node)

        if ok:

            node_root_dir = node.getNodeRootDir()

            new_output_dir = os.path.join(str(node_root_dir), 'output', str(text))

            if os.path.exists(new_output_dir):
                node.sendFromNodeToBox('--- output already exists' + '\n')
                
            else:
                node.newOutput(self, str(text))
                os.makedirs(new_output_dir, mode=0777)

                self.createNewVersion(new_output_dir)

                node.sendFromNodeToBox(str(datetime.datetime.now()))
                node.sendFromNodeToBox(':' + '\n')
                node.sendFromNodeToBox('--- new output created' + '\n')

    def newOutputDialogOld(self, node):
        # node_label = node.getLabel()

        text, ok = QInputDialog.getText(self.main_window, 'create new output in %s' % node.label, 'enter output name:')

        if ok:
            node_root_dir = node.getNodeRootDir()

            new_node_dir = os.path.join(str(node_root_dir), 'output', str(text))
            
            if os.path.exists(new_node_dir):
                node.sendFromNodeToBox('--- output already exists' + '\n')
                
            else:
                # output = node.newOutput(self, str(text))
                os.makedirs(new_node_dir, mode=0777)
                node.sendFromNodeToBox(str(datetime.datetime.now()))
                node.sendFromNodeToBox(':' + '\n')
                node.sendFromNodeToBox('--- new output created' + '\n')

    def newLoaderDialog(self, pos):
        def callback():
            active_item_path = os.path.join(self.main_window.projects_root, self.main_window._current_project, 'content', self.main_window._current_content['content'], self.main_window._current_content_item)

            ok, loaderName, sourceSaverLocation = NewLoaderUI.get_new_loader_data(active_item_path, self.main_window)

            if ok:
                newLoaderPath = os.path.join(active_item_path, loaderName)

                srcParentDirs = os.sep.join([str(os.path.relpath(self.main_window.projects_root, sourceSaverLocation))]) + os.sep

                src = os.sep.join([str(os.path.relpath(sourceSaverLocation, self.main_window.projects_root))])

                relPath = os.sep.join([str(srcParentDirs + src)])

                inputLinkOutput = os.path.join(newLoaderPath, 'output')
                inputLinkLive = os.path.join(newLoaderPath, 'live')

                if not os.path.exists(newLoaderPath):
                    os.makedirs(newLoaderPath, mode=0777)
                    os.makedirs(os.path.join(newLoaderPath, 'input'), mode=0777)

                    os.symlink(os.path.join(relPath, 'input'), inputLinkOutput)
                    os.symlink(os.path.join(relPath, 'input'), inputLinkLive)

                    meta_task_path = os.path.join(newLoaderPath, 'meta_task.json')

                    meta_task = {}

                    meta_task['pos_x'] = pos.x()
                    meta_task['pos_y'] = pos.y()
                    meta_task['task'] = 'LDR'
                    meta_task['operating_system'] = self.main_window.operating_system
                    meta_task['creator'] = self.main_window.user

                    with open(meta_task_path, 'w') as outfile:
                        json.dump(meta_task, outfile)
                        outfile.close()
                    
                    new_node = node(self.main_window, self, newLoaderPath)
                    new_node.addText(loaderName)

                else:
                    print 'asset loader already exists'
        return callback

    def newSaverDialog(self, pos):
        def callback():
            newSaverName = 'SVR_' + self.main_window._current_content['abbreviation'] + '__' + self.main_window._current_content_item

            newSaverPath = os.path.join(self.main_window.projects_root, self.main_window._current_project, 'content', self.main_window._current_content['content'], self.main_window._current_content_item, newSaverName)

            if not os.path.exists(newSaverPath):
                os.makedirs(newSaverPath, mode=0777)
                os.makedirs(os.path.join(newSaverPath, 'output'), mode=0777)
                os.makedirs(os.path.join(newSaverPath, 'input'), mode=0777)

                meta_task_path = os.path.join(newSaverPath, 'meta_task.json')

                meta_task = {}

                meta_task['pos_x'] = pos.x()
                meta_task['pos_y'] = pos.y()
                meta_task['task'] = 'SVR'
                meta_task['operating_system'] = self.main_window.operating_system
                meta_task['creator'] = self.main_window.user

                with open(meta_task_path, 'w') as outfile:
                    json.dump(meta_task, outfile)
                    outfile.close()
                
                new_node = node(main_window=self.main_window, scene=self, meta_task_path=meta_task_path)
                new_node.addText(newSaverName)

            else:
                print 'asset saver already exists'

        return callback

    def new_node_dialog(self, pos):
        def callback():
            tasks = self.main_window.getTasks()

            meta_tool = {}
            meta_task = {}
            
            node_dir = os.path.join(self.main_window.projects_root,
                                    self.main_window._current_project,
                                    'content',
                                    self.main_window._current_content['content'],
                                    self.main_window._current_content_item)

            node_name, ok, tool_data, task_index = NewNodeUI.get_new_node_data(node_dir, tasks, self.main_window)

            if ok:
                new_node_path = os.path.join(node_dir, str(node_name))

                pos_x = str(int(float(round(pos.x()))))
                pos_y = str(int(float(round(pos.y()))))

                meta_task['pos_x'] = pos_x
                meta_task['pos_y'] = pos_y

                meta_task['creator'] = self.main_window.user
                meta_task['operating_system'] = self.main_window.operating_system
                meta_task['task'] = self.main_window.tasks[task_index]['task']

                meta_tool['family'] = tool_data['family']
                meta_tool['architecture_fallback'] = tool_data['architecture_fallback']
                meta_tool['abbreviation'] = tool_data['abbreviation']
                meta_tool['architecture'] = tool_data['architecture']
                meta_tool['vendor'] = tool_data['vendor']
                meta_tool['release_number'] = tool_data['release_number']

                meta_task_path = os.path.join(new_node_path, 'meta_task.json')
                meta_tool_path = os.path.join(new_node_path, 'meta_tool.json')

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

                if tool_data['project_workspace_template'] is not None:
                    extension = os.path.splitext(tool_data['project_workspace_template'])[1]
                    # extension = str(tool_data['project_workspace_template']).split('_')[-1]
                    src_path = os.path.join('src', 'template_documents', tool_data['project_workspace_template'])
                    dst_path = os.path.join(new_node_path, extension)
                    shutil.copyfile(src_path, dst_path)

                property_node_path = None

                with open(meta_task_path, 'w') as outfile:
                    json.dump(meta_task, outfile)
                    outfile.close()

                with open(meta_tool_path, 'w') as outfile:
                    json.dump(meta_tool, outfile)
                    outfile.close()
                
                new_node = node(main_window=self.main_window, scene=self, property_node_path=property_node_path, meta_task_path=meta_task_path, meta_tool_path=meta_tool_path)
                new_node.addText(str(node_name))

                for tool_default_output in tool_data['default_outputs']:
                    self.newOutputAuto(new_node, tool_default_output)

        return callback

    def removeObject(self, item):
        reply = QMessageBox.warning(self.main_window, str('about to delete item'), str('are you sure to \ndelete %s %s \nand its contents?' %(item.data(2), item.label)), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:

            if isinstance(item, node) :
                tempOutputList = item.outputList
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
                    if self.main_window.current_platform == "Darwin":
                        os.unlink(inputDir)
                    elif self.main_window.current_platform == "Windows":
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
                if self.main_window.current_platform == "Darwin":
                    os.unlink(inputDir)
                elif self.main_window.current_platform == "Windows":
                    os.rmdir(inputDir)
            except:
                print 'cannot remove symlink 2345'
            self.removeItem(port)

        del tempInputsList
        
        item.parentItem().outputs.remove(item)

        output_dir = item.getOutputDir()
        live_dir = item.getLiveDir()
        if os.path.exists(live_dir):
            os.unlink(live_dir)
        shutil.rmtree(output_dir)

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

    # def new_node(self, pos):
    #     def callback():
    #         node(self.main_window, pos, self)
    #
    #     return callback
    
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
            # pos = event.scenePos()
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
                            connectionLine = bezierLine(self.main_window, self, startItems[0], endItems[0], QPainterPath(startItems[0].scenePos()))

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

                            # current_content = str(self.main_window._current_content)

                            cwd = os.getcwd()
                            dst = endItemInputDir

                            srcParentDirs = os.sep.join([str(os.path.relpath(self.main_window.projects_root, os.path.dirname(dst)))]) + os.sep

                            src = os.sep.join([str(os.path.relpath(startItemOutputDir, self.main_window.projects_root))])

                            relPath = os.sep.join([str(srcParentDirs + src)])

                            if len(os.path.basename(dst).split('.')) > 1:
                                inputLink = os.path.dirname(dst) + os.sep + os.path.basename(relPath)

                            else:
                                inputLink = os.path.dirname(dst) + os.sep + os.path.basename(os.path.dirname(os.path.dirname(startItemRootDir))) + '.' + os.path.basename(os.path.dirname(startItemRootDir)) + '.' + os.path.basename(startItemRootDir) + '.' + os.path.basename(dst)
                            if self.main_window.current_platform == "Darwin":
                                try:
                                    os.symlink(relPath, inputLink)
                                except:
                                    pass
                                endItems[0].setInputDir(inputLink)
                            elif self.main_window.current_platform == "Windows":
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