import os
import sip
import sys
import subprocess
import platform
import re
import shutil
import random
import datetime
import getpass
import threading
import socket
import json
import logging
from operator import *

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import *
from PyQt4.QtOpenGL import *
from random import *

from src.pypelyneConfigurationWindow import *
from src.bezierLine import *
from src.graphicsScene import *
from src.screenCast import *
from src.timeTracker import *
from src.listScreenCasts import *
from src.nodeWidget import *
from src.playerWidget import *

# from conf.valuePyPELyNE import *

from settings import EXCLUSIONS, AUDIO_EXTENSIONS, IMAGE_EXTENSIONS, MOVIE_EXTENSIONS, ARCHIVE_SEPARATOR
from settings import USE_SERVER, USE_SCREEN_CAST, SERVER_IP, SERVER_PORT, SERVER_PORT_RANGE, PROJECT_ROOT_SERVER
from settings import LIBRARY_ROOT_SERVER, PROJECTS_ROOT_SERVER_DARWIN, ASSETS_ROOT_SERVER_DARWIN
from settings import ASSETS_ROOT_SERVER_WIN, PROJECTS_ROOT_SERVER_LINUX, ASSETS_ROOT_SERVER_LINUX
from settings import FILE_EXPLORER_DARWIN, PROJECTS_ROOT_DARWIN, PROJECTS_ROOT_DARWIN_ALT, LIBRARY_ROOT_DARWIN
from settings import AUDIO_FOLDER_DARWIN, SCREEN_CAST_EXEC_DARWIN, SEQUENCE_EXEC_DARWIN, SEQUENCE_EXEC_RV_DARWIN
from settings import TAR_EXEC_DARWIN, FILE_EXPLORER_WIN, PROJECTS_ROOT_WIN, LIBRARY_ROOT_WIN, AUDIO_FOLDER_WIN
from settings import SCREEN_CAST_EXEC_WIN, SEQUENCE_EXEC_WIN, SEQUENCE_EXEC_RV_WIN, TAR_EXEC_WIN
from settings import FILE_EXPLORER_LINUX_GNOME, FILE_EXPLORER_LINUX_KDE, PROJECTS_ROOT_LINUX, LIBRARY_ROOT_LINUX
from settings import AUDIO_FOLDER_LINUX, SCREEN_CAST_EXEC_LINUX, SEQUENCE_EXEC_LINUX, SEQUENCE_EXEC_RV_LINUX
from settings import TAR_EXEC_LINUX, PROJECTS_ROOT_SERVER_WIN

import xml.etree.ElementTree as ET

try:
    from src.vlc import *
except:
    print 'failed to import vlc'
    # raise ImportError('failed to import vlc')

app = None

# TODO: jumping from shots to asset loader does not update tab widget title correctly


# noinspection PyInterpreter,PyInterpreter
class PypelyneMainWindow(QMainWindow):
    addNewScreenCast = pyqtSignal()

    def __init__(self, parent=None):
        super(PypelyneMainWindow, self).__init__(parent)

        # logging.basicConfig(level = logging.INFO)

        self.serverHost = SERVER_IP
        self.serverPort = int(SERVER_PORT)
        self.portRange = int(SERVER_PORT_RANGE)

        # self.serverPort = 50002
        self.serverAlive = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.content_tabs = [{'content': 'assets', 'abbreviation': 'AST', 'loader_color': '#FFFF00', 'saver_color': '#FFFF33'},
                             {'content': 'shots', 'abbreviation': 'SHT', 'loader_color': '#0000FF', 'saver_color': '#3333FF'},
                             {'content': 'sequences', 'abbreviation': 'SEQ', 'loader_color': '#00FFFF', 'saver_color': '#33FFFF'}]

        # self.connectServer()

        if USE_SERVER:
            logging.info('connecting to server')
            logging.info('server ip is %s' % self.serverHost)
            counter = 1
            while True:
                try:
                    logging.info('trying to connect to %s:%s' % (self.serverHost, self.serverPort))
                    self.socket.connect((self.serverHost, self.serverPort))
                    logging.info('connection to server successful')
                    self.serverAlive = True
                    break
                except:
                    logging.info('connection failed')
                    logging.info('trying next port')
                    if counter < self.portRange:
                        #warning('port %s in use' %(self.port))
                        counter += 1
                        self.serverPort += 1
                    else:
                        logging.warning('tried %s port(s) without success. no server found. continuing as workstation version.' % counter)
                        self.serverAlive = False
                        break

        else:
            self.serverAlive = False

        self.pypelyneRoot = os.getcwd()
        self.currentPlatform = platform.system()
        self.operating_system = self.currentPlatform.lower()

        self.architectures = ['x32', 'x64']

        self.tool_items = []

        if sys.maxsize <= 2**32:
            self.architecture = self.architectures[0]
        elif sys.maxsize > 2**32:
            self.architecture = self.architectures[1]

        self.user = getpass.getuser()

        print self.operating_system, self.architecture, self.user

        self.current_content_item = None
        
        self.exclusions = EXCLUSIONS
        self.audioExtensions = AUDIO_EXTENSIONS
        self.imageExtensions = IMAGE_EXTENSIONS
        self.movieExtensions = MOVIE_EXTENSIONS
        self.tarSep = ARCHIVE_SEPARATOR
        self.screenCastActive = USE_SCREEN_CAST

        self.setProjectsRoot()

        if self.currentPlatform == "Windows":
            # print 'platform not fully supported'
            logging.info('Windows not fully supported')
            self.fileExplorer = FILE_EXPLORER_WIN
            self.tarExec = TAR_EXEC_WIN
            # self.projectsRoot = projectsRootWin
            self.libraryRoot = LIBRARY_ROOT_WIN
            self.audioFolder = AUDIO_FOLDER_WIN
            if SCREEN_CAST_EXEC_WIN[1:].startswith(':' + os.sep):
                self.screenCastExec = SCREEN_CAST_EXEC_WIN
            else:
                self.screenCastExec = os.path.join(self.pypelyneRoot, SCREEN_CAST_EXEC_WIN)
            if len(SEQUENCE_EXEC_RV_WIN) <= 0 or not os.path.exists(SEQUENCE_EXEC_RV_WIN):
                self.sequenceExec = SEQUENCE_EXEC_WIN
                self.rv = False
            else:
                self.sequenceExec = SEQUENCE_EXEC_RV_WIN
                self.rv = True
        elif self.currentPlatform == "Darwin":
            logging.info('welcome to pypelyne for darwin')
            self.fileExplorer = FILE_EXPLORER_DARWIN
            self.tarExec = TAR_EXEC_DARWIN
            # self.projectsRoot = projectsRootDarwin
            self.libraryRoot = LIBRARY_ROOT_DARWIN
            self.audioFolder = AUDIO_FOLDER_DARWIN
            if SCREEN_CAST_EXEC_DARWIN.startswith(os.sep):
                self.screenCastExec = SCREEN_CAST_EXEC_DARWIN
            else:
                self.screenCastExec = os.path.join(self.pypelyneRoot, SCREEN_CAST_EXEC_DARWIN)
            if len(SEQUENCE_EXEC_RV_DARWIN) <= 0 or not os.path.exists(SEQUENCE_EXEC_RV_DARWIN):
                self.sequenceExec = SEQUENCE_EXEC_DARWIN
                self.rv = False
            else:
                self.sequenceExec = SEQUENCE_EXEC_RV_DARWIN
                self.rv = True
        elif self.currentPlatform == "Linux":
            logging.info('linux not fully supported')
            if os.path.exists(FILE_EXPLORER_LINUX_GNOME):
                self.fileExplorer = FILE_EXPLORER_LINUX_GNOME
            elif os.path.exists(FILE_EXPLORER_LINUX_KDE):
                self.fileExplorer = FILE_EXPLORER_LINUX_KDE
            else:
                logging.warning('no valid file explorer found for linux')
            # quit()
            self.tarExec = TAR_EXEC_LINUX
            # self.projectsRoot = projectsRootLinux
            self.libraryRoot = LIBRARY_ROOT_LINUX
            self.audioFolder = AUDIO_FOLDER_LINUX
            if SCREEN_CAST_EXEC_LINUX.startswith(os.sep):
                self.screenCastExec = SCREEN_CAST_EXEC_LINUX
            else:
                self.screenCastExec = os.path.join(self.pypelyneRoot, SCREEN_CAST_EXEC_LINUX)
            if len(SEQUENCE_EXEC_RV_LINUX) <= 0 or not os.path.exists(SEQUENCE_EXEC_RV_LINUX):
                self.sequenceExec = SEQUENCE_EXEC_LINUX
                self.rv = False
            else:
                self.sequenceExec = SEQUENCE_EXEC_RV_LINUX
                self.rv = True
        else:
            print 'platform unknown. not supported. bye.'
            quit()

        # print self.libraryRoot
        if not os.path.exists(self.libraryRoot) and not self.libraryRoot == None and not self.libraryRoot == '':
            os.makedirs(self.libraryRoot, mode=0777)
            logging.info('library root directory created')

        self.nodeWidgets = []
        self.qprocesses = []
        self.openNodes = []
        self.timeTrackers = []
        self.screenCasts = []
        self.screenCastsWindowOpen = None

        self.ui = loadUi(os.path.join(self.pypelyneRoot, 'ui', 'pypelyneMainWindow.ui'), self)
        self.valueApplicationsXML = os.path.join(self.pypelyneRoot, 'conf', 'valueApplications.xml')
        
        self.nodeView.setVisible(False)
        self.assetsShotsTabWidget.setVisible(False)
        self.statusBox.setVisible(False)
        self.nodeOptionsWindow.setVisible(False)
        self.descriptionWindow.setVisible(False)
        self.openPushButton.setVisible(True)
        self.checkBoxDescription.setVisible(False)
        self.configPushButton.setVisible(False)
        if not self.screenCastActive:
            self.screenCastsPushButton.setVisible(False)

        self.openPushButton.setEnabled(False)

        # self.compute_value_applications()
        self.computeValueTasks()
        self.computeValueOutputs()

        # Scene view
        self.scene = SceneView(self)
        self.nodeView.setViewport(QGLWidget(QGLFormat(QGL.SampleBuffers)))
        self.nodeView.setScene(self.scene)
        self.nodeView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.nodeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.nodeView.setSceneRect(0, 0, 630, 555)
        
        self.scalingFactor = 1
        
        self.currentContent = None
        
        self.mapSize = (512, 512)
        # self.scene = GraphicsScene(self)
        # self.scene.addRect(QRectF(0, 0, self.mapSize), Qt.red)
        # self.addRect()
        # self.boundary = self.scene.addRect(QRectF(-1000, -1000, 1000, 1000), Qt.red)
        # self.view = QGraphicsView()
        # self.scene.setScene(self.scene)
        # self.scene.resize(self.scene.width(), self.scene.height())
        # self.setCentralWidget(self.view)

        # Graphics View
        self.nodeView.wheelEvent = self.graphicsView_wheelEvent
        # self.nodeView.resizeEvent = self.graphicsView_resizeEvent
        self.nodeView.setBackgroundBrush(QBrush(QColor(60, 60, 60, 255), Qt.SolidPattern))

        self.tools = None

        # Projects
        self.addProjects()
        
        # Tools
        # self.tools_dict = {}
        self.add_tools()

        self.audioFolderContent = []

        if os.path.exists(self.audioFolder):
            logging.info('audioFolder found at %s' % self.audioFolder)
            self.addPlayer()

        self.runToolPushButton.clicked.connect(self.run_tool)
        
        self.checkBoxConsole.stateChanged.connect(self.toggleConsole)
        self.checkBoxNodeName.stateChanged.connect(self.toggleNodeName)
        self.checkBoxDescription.stateChanged.connect(self.toggleDescription)
        self.checkBoxContentBrowser.stateChanged.connect(self.toggleContentBrowser)
        # self.checkBoxNodesWindow.stateChanged.connect(self.toggleNodesWindow)
        # self.scene.nodeClicked.connect(self.setWidgetMenu)
        
        # configuration window
        self.configPushButton.clicked.connect(self.configurationWindow)
        self.screenCastsPushButton.clicked.connect(self.screenCastsWindow)
        self.scene.nodeSelect.connect(self.setNodeWidget)
        self.scene.nodeDeselect.connect(self.clearNodeWidget)
        self.openPushButton.clicked.connect(lambda: self.locateContent(os.path.join(self.projectsRoot, str(self.projectComboBox.currentText()))))

        self.clipBoard = QApplication.clipboard()
        
        # self.scene = SceneView()
        self.scene.textMessage.connect(self.sendTextToBox)
        # self.scene.nodeClicked.connect(self.setNodeMenuWidget)
        # self.scene.nodeMenu.connect(self.setWidgetMenu)
        
        # self.scene.nodeMenuArea.connect(self.updateNodeMenu)

        # print self._tools
        # print self._tool_items

    # def connectServer(self):

    @property
    def _user(self):
        return self.user

    @property
    def _exclusions(self):
        return self.exclusions

    @property
    def _image_extensions(self):
        return self.imageExtensions

    @property
    def _movie_extensions(self):
        return self.movieExtensions

    @property
    def _sequence_exec(self):
        return self.sequenceExec

    @property
    def _current_platform(self):
        return self.currentPlatform

    @property
    def _pypelyne_root(self):
        return self.pypelyneRoot

    @property
    def _projects_root(self):
        return self.projectsRoot

    @property
    def _current_content(self):
        current_content_index = self.assetsShotsTabWidget.currentIndex()
        return self.content_tabs[current_content_index]

    @property
    def _tools(self):
        if self.tools is None:
            print 'def _tools(self):'

            logging.info('parsing tools')

            app_conf_root = os.path.join(os.path.abspath(r'conf'), r'tools', r'applications')
            # app_conf_files = [os.path.join(app_conf_root, f) for f in os.listdir(app_conf_root) if not f.startswith('_') and f not in self.exclusions and f.split('.')[-1].endswith('json')]

            self.tools = []

            app_conf_files = []
            app_conf_files.append(os.path.join(app_conf_root, '_blender_.json'))
            app_conf_files.append(os.path.join(app_conf_root, '_maya_.json'))
            app_conf_files.append(os.path.join(app_conf_root, '_uvlayout_.json'))

            for app_conf_file in app_conf_files:
                source_file = os.path.join(app_conf_root, app_conf_file)
                tool = {}

                json_file = open(app_conf_file)
                app_conf = json.load(json_file)
                json_file.close()

                logging.info('processing source file: %s' % source_file)

                # print app_conf

                if app_conf['family_enable']:
                    logging.info('checking system for family: %s' % app_conf['family'])

                    # all the family related stuff
                    # source_file = source_file
                    family = app_conf[u'family']
                    vendor = app_conf[u'vendor']
                    abbreviation = app_conf[u'abbreviation']

                    for release in app_conf[u'releases']:
                        # type(release) = dict
                        logging.info('checking system for release: %s' % release[u'release_number'])

                        # and all the version/release related stuff
                        release_number = release[u'release_number']
                        project_template = release[u'project_template']
                        project_workspace = release[u'project_workspace']
                        project_directories = release[u'project_directories']
                        default_outputs = release[u'default_outputs']
                        architecture_fallback = release[u'architecture_fallback']

                        if self.architecture == 'x64' and architecture_fallback:
                            architecture_fallback = True
                        elif self.architecture == 'x32':
                            architecture_fallback = False

                        label_x32 = vendor + ' ' + family + ' ' + release_number + ' (%s)' % self.architectures[0]
                        label_x64 = vendor + ' ' + family + ' ' + release_number + ' (%s)' % self.architectures[1]

                        project_directories_list = []
                        # default_outputs_list = []

                        for project_directory in project_directories:
                            project_directory = project_directory.replace('%', os.sep)
                            project_directories_list.append(project_directory)

                        # for default_output in default_outputs:
                        #     default_outputs_list.append(default_output)

                        for platform in release['platforms']:
                            if platform.has_key(self.operating_system):
                                # general information:

                                executable_x32 = platform[self.operating_system][u'executable_x32']
                                executable_x64 = platform[self.operating_system][u'executable_x64']

                                flags_x32 = platform[self.operating_system][u'flags_x32']
                                flags_x64 = platform[self.operating_system][u'flags_x64']

                                executables = []

                                for executable in [executable_x32, executable_x64]:
                                    if executable is None:
                                        logging.warning('executable is %s' % executable)
                                    elif os.path.exists(executable):
                                        # print executables
                                        executables.append(executable)
                                        logging.info('executable %s found on this machine.' % executable)
                                    else:
                                        logging.warning('executable %s not found on this machine.' % executable)

                                tool[u'family'] = family
                                tool[u'vendor'] = vendor
                                tool[u'abbreviation'] = abbreviation
                                tool[u'release_number'] = release_number
                                tool[u'project_template'] = project_template
                                tool[u'project_workspace'] = project_workspace
                                tool[u'project_directories'] = project_directories_list
                                tool[u'default_outputs'] = default_outputs
                                tool[u'architecture_fallback'] = architecture_fallback
                                tool[u'label_x32'] = label_x32
                                tool[u'label_x64'] = label_x64
                                tool[u'project_directories'] = project_directories
                                tool[u'flags_x32'] = flags_x32
                                tool[u'flags_x64'] = flags_x64

                                if executable_x32 in executables:
                                    tool[u'executable_x32'] = executable_x32
                                else:
                                    tool[u'executable_x32'] = None
                                if executable_x64 in executables:
                                    tool[u'executable_x64'] = executable_x64
                                else:
                                    tool[u'executable_x64'] = None

                                self.tools.append(tool.copy())

                                # print 'tool', tool

                else:
                    logging.info('source file skipped (reason: disabled): %s' % source_file)

        # print self.tools
        return self.tools

    @property
    def _outputs(self):
        return self.outputs

    @property
    def _tasks(self):
        return self.tasks

    @property
    def _tool_items(self):
        if not self.tool_items:
            # print 'def _tool_items(self):'

            for tool in self._tools:
                # self.tool_items = []
                # for tool in self._tools:
                # print tool
                index = self._tools.index(tool)

                executable = []
                # self.run_items = []

                if tool[u'executable_x32'] is not None:
                    executable.append(self._tools[index][u'executable_x32'])
                    for flag_x32 in self._tools[index][u'flags_x32']:
                        executable.append(flag_x32)

                    run_item = self.get_dict_x32(tool)

                    self.tool_items.append(run_item.copy())

                    # print run_item

                    # self.toolsComboBox.addItem(tool[u'label_x32'], run_item.copy())

                executable[:] = []

                if tool[u'executable_x64'] is not None:
                    executable.append(self._tools[index][u'executable_x64'])
                    for flag_x64 in self._tools[index][u'flags_x64']:
                        executable.append(flag_x64)

                    run_item = self.get_dict_x64(tool)

                    self.tool_items.append(run_item.copy())

                    # print 'run_item', run_item

                    # self.toolsComboBox.addItem(tool[u'label_x64'], run_item.copy())

                executable[:] = []

        # print 'self.tool_items', self.tool_items
        return self.tool_items

    def receiveSerialized(self, sock):
        # read the length of the data, letter by letter until we reach EOL
        length_str = ''
        char = sock.recv(1)

        # print char

        while char != '\n':
            length_str += char
            # logging.warning('till here')
            char = sock.recv(1)

        total = int(length_str)
        # use a memoryview to receive the data chunk by chunk efficiently
        view = memoryview(bytearray(total))
        next_offset = 0

        while total - next_offset > 0:
            recv_size = sock.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
        try:

            deserialized = json.loads(view.tobytes())
        # except (TypeError, ValueError), e:
        except:
            raise Exception('Data received was not in JSON format')
        return deserialized

    def setProjectsRoot(self):
        logging.info('getting projectsRoot')
        if self.currentPlatform == 'Windows':
            self.setProjectsRootWin()
        elif self.currentPlatform == 'Darwin':
            self.setProjectsRootDarwin()
        elif self.currentPlatform == 'Linux':
            self.setProjectsRootLinux()
        else:
            print 'platform not supported'
            sys.exit()

    def setProjectsRootWin(self):
        try:
            # self.socket.connect((self.serverHost, self.serverPort))
            # print 'here'
            self.socket.sendall('getProjectsRootServerWin')
            self.projectsRoot = self.receiveSerialized(self.socket)
            logging.info('projectsRootServerWin server successfully queried')
            self.serverAlive = True
            # self.socket.close()
        except socket.error:
            self.projectsRoot = PROJECTS_ROOT_WIN
            self.serverAlive = False

    def setProjectsRootLinux(self):
        try:
            # self.socket.connect((self.serverHost, self.serverPort))
            # print 'here'
            self.socket.sendall('getProjectsRootServerLinux')
            self.projectsRoot = self.receiveSerialized(self.socket)
            logging.info('projectsRootServerLinux server successfully queried')
            self.serverAlive = True
            # self.socket.close()
        except socket.error:
            self.projectsRoot = PROJECTS_ROOT_LINUX
            self.serverAlive = False

    def setProjectsRootDarwin(self):
        if self.serverAlive == True:
            try:
                logging.info('sending getProjectsRootServerDarwin to server')
                # self.socket.connect((self.serverHost, self.serverPort))
                # print 'here'
                self.socket.sendall('getProjectsRootServerDarwin')
                self.projectsRoot = self.receiveSerialized(self.socket)
                logging.info('projectsRootServerDarwin server successfully queried')
                # self.serverAlive = True
                # self.socket.close()
            except socket.error:
                logging.warning('looks like server connection died')
                self.projectsRoot = PROJECTS_ROOT_DARWIN
                self.serverAlive = False

        else:
            if os.path.exists(PROJECTS_ROOT_DARWIN):
                self.projectsRoot = PROJECTS_ROOT_DARWIN
            elif os.path.exists(PROJECTS_ROOT_DARWIN_ALT):
                self.projectsRoot = PROJECTS_ROOT_DARWIN_ALT
            else:
                logging.warning('no predefinded projectsRoot found')

    def exportToLibraryCallback(self, node):
        def callback():
            self.exportToLibrary(node)
        return callback

    def exportToLibrary(self, node):
        print 'exportToLibrary', node
        date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
        current_dir = os.getcwd()
        export_src_node_dir = node.location
        export_src_node_dir_inputs = os.path.join(export_src_node_dir, 'input')
        # exportSrcNodeDirOutputs = os.path.join(exportSrcNodeDir, 'output')
        exportDstDirRoot = self.libraryRoot
        exportDstName = self.getCurrentProject() + self.tarSep + os.path.basename(os.path.dirname(node.getNodeAsset())) + self.tarSep + os.path.basename(node.getNodeAsset()) + self.tarSep + node.label + self.tarSep + date_time
        exportDstDir = os.path.join(exportDstDirRoot, exportDstName)
        exportDstNameInput = os.path.join(exportDstDir, 'input')
        exportDstNameOutput = os.path.join(exportDstDir, 'output')

        # print 'export from:', exportSrcNodeDirInputs
        # print 'export to:', exportDstNameInput
        # print 'export name:', exportDstName

        os.makedirs(os.path.join(self.libraryRoot, exportDstName), mode=0777)
        os.makedirs(os.path.join(self.libraryRoot, exportDstNameInput), mode=0777)
        # os.makedirs(os.path.join(self.libraryRoot, exportDstNameOutput), mode = 0777)

        # shutil.copytree('/Volumes/pili/pypelyne_projects/0000-00-00___test___test/content/assets/test/SVR_AST__test/input', '/Volumes/pili/pypelyne_assets/0000-00-00___test___test_____assets_____test_____SVR_AST__test_____2015-09-04_1311-41/output', symlinks = False)
        #                   /Volumes/pili/pypelyne_projects/0000-00-00___test___test/content/assets/test/SVR_AST__test/input

        shutil.copytree(export_src_node_dir_inputs, exportDstNameOutput, symlinks=False)

        os.chdir(exportDstDir)
        os.symlink(os.path.relpath(exportDstNameOutput, exportDstDir), 'live')
        os.path.relpath(exportDstNameOutput, exportDstDir)
        os.chdir(current_dir)
        # shutil.copytree(exportSrcNodeDirOutputs, exportDstNameInput, symlinks = False)

    def screenCastsWindow(self):
        if self.screenCastsWindowOpen == None:
            self.screenCastsUI = listScreenCastsUI(self, self)
            self.screenCastsUI.show()
            self.screenCastsWindowOpen = self.screenCastsUI
            self.screenCastsUI.listScreenCastsUIClosed.connect(self.resetScreenCastsWindowOpen)

        else:
            self.screenCastsUI.activateWindow()
            self.screenCastsUI.raise_()
        # print 'hallo'

    def resetScreenCastsWindowOpen(self):
        # print 'emitted'
        self.screenCastsWindowOpen = None

    # def getUser(self):
    #     return self.user

    def _closeEvent(self, event):
        if len(self.timeTrackers) > 0 or len(self.screenCasts) > 0 or len(self.qprocesses) > 0:

            if len(self.qprocesses) > 0:
                qprocesses = []
                for qprocess in self.qprocesses:
                    qprocesses.append(qprocess.pid())

            pids = ', '.join([str(qprocess)[:-1] for qprocess in qprocesses])

            quit_msg = "Too early to leave. There is still something running...\n\nPID(s): %s" % pids

            reply = QMessageBox.critical(self, 'Message', quit_msg, QMessageBox.Ok)

            # print 'about to close'

        else:
            quit_msg = "Are you sure you want to exit PyPELyNE?"

            reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.serverAlive == True:
                logging.info('sending bye')
                self.socket.sendall('bye')
                # byeMsg = self.receiveSerialized(self.socket)[1]
                # print byeMsg
                logging.info('closing socket')
                self.socket.close()
                logging.info('socket closed')
                self.serverAlive = False
            event.accept()
        else:
            event.ignore()

    # def getExclusions(self):
    #     return self.exclusions

    # def getImageExtensions(self):
    #     return self.imageExtensions

    # def getMovieExtensions(self):
    #     return self.movieExtensions

    # def getSequenceExec(self):
    #     return self.sequenceExec

    def addPlayer(self):
        self.playerUi = playerWidgetUi(self)
        self.horizontalLayout.addWidget(self.playerUi)
        # self.playerUi.radioButtonPlay.clicked.connect(self.playAudio)
        self.playerUi.pushButtonPlayStop.clicked.connect(self.playAudio)

        self.playerUi.pushButtonPlayStop.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self.playerUi.pushButtonPlayStop, SIGNAL('customContextMenuRequested(const QPoint&)'), self.playerContextMenu)

        self.playerContextMenu = QMenu()
        qMenuTitles = []

        for dir, subdirs, files in os.walk(self.audioFolder, topdown=False):
            for file in files:
                if file in self.exclusions:
                    os.remove(os.path.join(dir, file))
                    logging.warning('file %s deleted from %s' % (file, dir))

                elif os.path.splitext(file)[1] not in self.audioExtensions:
                    logging.warning('non audio file %s found in %s' % (file, dir))

                else:
                    if not os.path.relpath(dir, self.audioFolder) == '.':
                        qMenuName = os.path.relpath(dir, self.audioFolder)
                        # if len(qMenuName.split(os.sep)) > 1:
                        if not qMenuName in qMenuTitles:
                            self.menuAlbum = self.playerContextMenu.addMenu(qMenuName.replace(os.sep, ' - '))
                            qMenuTitles.append(qMenuName)

                            self.menuAlbum.addAction(file, self.playAudioCallback(os.path.join(dir, file)))
                            self.audioFolderContent.append(os.path.join(dir, file))
                        else:
                            self.menuAlbum.addAction(file, self.playAudioCallback(os.path.join(dir, file)))
                            self.audioFolderContent.append(os.path.join(dir, file))

                    else:
                        self.playerContextMenu.addAction(file, self.playAudioCallback(os.path.join(dir, file)))
                        self.audioFolderContent.append(os.path.join(dir, file))

        self.playerUi.pushButtonPlayStop.setText('play')
        self.playerExists = False

    def playerContextMenu(self, point):
        self.playerContextMenu.exec_(self.playerUi.pushButtonPlayStop.mapToGlobal(point))

    # def cb(self, event):
    #     print 'cb:', event.type, event.u

    def playAudioCallback(self, track = None):
        def callback():
            self.playAudio(track)
        return callback

    def playAudio(self, track = None):
        # https://forum.videolan.org/viewtopic.php?t=107039

        if len(os.listdir(self.audioFolder)) == 0:
            logging.warning('no audio files found')
            self.playerUi.radioButtonPlay.setEnabled(False)

        elif self.playerExists == False:
            random.shuffle(self.audioFolderContent, random.random)

            if not track == False:
                trackID = self.audioFolderContent.index(track)

            #print 'playing'

            self.mlp = MediaListPlayer()
            self.mp = MediaPlayer()
            self.mlp.set_media_player(self.mp)


            self.ml = MediaList()

            for file in self.audioFolderContent:
                self.ml.add_media(os.path.join(self.audioFolder, file))

            self.mlp.set_media_list(self.ml)

            if not track == False:
                #print trackID
                self.mlp.play_item_at_index(trackID)
                logging.info('playing %s' %(trackID))

            else:
                self.mlp.play()
                logging.info('playing randomly')


            #self.playerUi.pushButtonPlayStop.setText('skip')

            self.playerExists = True

            self.playerUi.pushButtonPlayStop.clicked.disconnect(self.playAudio)
            self.playerUi.pushButtonPlayStop.clicked.connect(self.stopAudio)
            self.playerUi.pushButtonPlayStop.setText('stop')
            logging.info('setting pushButtonPlayStop function to stop')
            #self.playerUi.pushButtonPlayStop.clicked.disconnect(self.playAudio)
            #self.playerUi.pushButtonPlayStop.clicked.connect(self.skipAudio)
            #print 'timer start'
            threading.Timer(0.5, self.fromStopToSkip).start()


        elif self.playerExists == True and not track == False:

            logging.info('playing %s' %(track))

            #random.shuffle(self.audioFolderContent, random.random)
            trackID = self.audioFolderContent.index(track)


            #self.audioFolderContent.remove(track)
            #self.audioFolderContent.insert(0, track)
            self.skipAudio(trackID)




        else:
            logging.info('already on air')

    def fromStopToSkip(self):
        if self.playerExists == True:
            self.playerUi.pushButtonPlayStop.clicked.disconnect(self.stopAudio)
            self.playerUi.pushButtonPlayStop.clicked.connect(self.skipAudio)
            self.playerUi.pushButtonPlayStop.setText('skip')
            logging.info('setting pushButtonPlayStop function to skip')

    def fromSkipToStop(self):
        if self.playerExists == True:
            self.playerUi.pushButtonPlayStop.clicked.disconnect(self.skipAudio)
            self.playerUi.pushButtonPlayStop.clicked.connect(self.stopAudio)
            self.playerUi.pushButtonPlayStop.setText('stop')
            logging.info('setting pushButtonPlayStop function to stop')

    def stopAudio(self):
        if self.playerExists == True:
            try:
                self.playerUi.pushButtonPlayStop.clicked.disconnect(self.stopAudio)
                self.playerUi.pushButtonPlayStop.clicked.connect(self.playAudio)
                self.mp.stop()
                self.mp.release()
                self.mlp.release()
                self.playerExists = False
                self.playerUi.pushButtonPlayStop.setText('play')
                logging.info('setting pushButtonPlayStop function to play')
                #logging.info('audio stopped')
            except:
                logging.warning('error or not playing')

    def skipAudio(self, trackID = None):
        if self.playerExists == True:
            if not trackID == False:
                self.mlp.play_item_at_index(trackID)

            else:
                self.mlp.next()

            self.playerUi.pushButtonPlayStop.clicked.disconnect(self.skipAudio)
            self.playerUi.pushButtonPlayStop.clicked.connect(self.stopAudio)
            self.playerUi.pushButtonPlayStop.setText('stop')
            threading.Timer(0.5, self.fromStopToSkip).start()
            #threading.Timer(1, self.fromStopToSkipChangeUi).start()

    # def getCurrentPlatform(self):
    #     return self.currentPlatform
        
    # def getProjectsRoot(self):
    #     return self.projectsRoot

    # def getCurrentContent(self):
    #     return self.currentContent

    # def addRectangular(self):
    #     self.scene.addRect(QRectF(0, 0, self.mapSize), Qt.red)
    #     pass

    def computeValueOutputs(self):
        #print os.path.join(self.pypelyneRoot, 'conf', 'valueOutputs.xml')
        self.valueOutputs = ET.parse(os.path.join(self.pypelyneRoot, 'conf', 'valueOutputs.xml'))
        self.valueOutputsRoot = self.valueOutputs.getroot()

        self.outputs = []
        categoryList = []
        mimeList = []
        itemList = []

        for category in self.valueOutputsRoot:
            itemList.append(category.items())
            for mime in category:
                itemList.append(mime.items())
                # category.items().append(mime)
                # self._outputs.append(category.itemssubmissionCmdArgs())

            self.outputs.append(itemList)
            itemList = []

            #print category.items()
        #print self._outputs
        '''
        for output in self._outputs:
            #abbrev
            print output[0][2][1]
            #full output name
            print output[0][1][1]
            #for output in outputCollection[0]:
            #    print output
        '''
    
    def computeValueTasks(self):
        self.valueTasks = ET.parse(os.path.join(self.pypelyneRoot, 'conf', 'valueTasks.xml'))
        self.valueTasksRoot = self.valueTasks.getroot()

        self.tasks = []

        for category in self.valueTasksRoot:
            self.tasks.append(category.items())

        #print self._tasks
            #print category.items()

    def new_process_color(self):
        pColorR = random.randint(20, 235)
        pColorG = random.randint(20, 235)
        pColorB = random.randint(20, 235)

        pColor = (QColor(pColorR, pColorG, pColorB))

        return pColor

    # TODO: refactor
    def runTask(self, node, executable, newestFile, *args):
        #print executable

        makingOfDir = os.path.join(self.getCurrentProject(), 'making_of')

        #now = str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S'))
        now = datetime.datetime.now()

        nowSecs = str(now.strftime('%Y-%m-%d_%H%M-%S'))
        nowMilliSecs = str(now.strftime('%Y-%m-%d_%H%M-%S_%f'))

        arguments = QStringList()
        #arguments = []

        for nodeExeArg in args[0]:
            arguments.append(nodeExeArg)

        arguments.append(newestFile)
        #print newestFile
        #print args[0]
        #print str(arguments)

        #for i in arguments:
        #    print i

        #if executable.startswith('"') and executable.endswith('"'):
        #print executable[1:-2], arguments
        executable = executable.replace('\"', '')
        executable = executable.replace('\'', '')
        if executable.endswith(' '):
            executable = executable[:-1]
        #print executable, arguments

        newScreenCast = screenCast(self, os.path.basename(node.getNodeAsset()), node.getLabel(), node.getNodeProject())
        newTimeTracker = timeTracker(os.path.basename(node.getNodeAsset()), node.getLabel(), node.getNodeProject())

        process = QProcess(self)

        pColor = self.new_process_color()

        #process.readyRead.connect(lambda: self.dataReady(process))
        process.readyReadStandardOutput.connect(lambda: self.data_ready_std(process, pColor))
        process.readyReadStandardError.connect(lambda: self.dataReadyErr(process, pColor))
        process.started.connect(lambda: self.taskOnStarted(node, process, newScreenCast, newTimeTracker))
        #process.started.connect(lambda: )
        process.finished.connect(lambda: self.task_on_finished(node, process, newScreenCast, newTimeTracker))
        currentDir = os.getcwd()
        os.chdir(node.getNodeRootDir())
        #print node.getNodeRootDir()
        process.start(executable, arguments)
        os.chdir(currentDir)
        #print os.getcwd()

    def checkOutCallback(self, node):
        def callback():
            self.checkOut(node)
        return callback

    def checkOut(self, node):
        # self.tarSep = '_____'
        dateTime = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
        # executable = self.tarExec
        pigz = os.path.join(self.pypelyneRoot, 'payload', 'pigz', 'darwin', 'pigz')
        tarDirRoot = os.path.join(self.projectsRoot, self.getCurrentProject(), 'check_out')
        # print self._current_content
        tarName = dateTime + self.tarSep + self.getCurrentProject() + self.tarSep + os.path.basename(os.path.dirname(node.getNodeAsset())) + self.tarSep + os.path.basename(node.getNodeAsset()) + self.tarSep + node.label + '.tar.gz'

        if not os.path.exists(tarDirRoot):
            os.makedirs(tarDirRoot, mode=0777)

        # print tarDirRoot
        # print os.getcwd()

        arguments = []
        arguments.append('cvL')
        arguments.append('--exclude')
        arguments.append('checkedOut')
        #exclude all non-current folders
        arguments.append('--exclude')
        arguments.append('output/*/2*')
        arguments.append('--exclude')
        arguments.append('output/*.*')
        arguments.append('--exclude')
        arguments.append('live')
        #arguments.append('--exclude')
        #arguments.append('propertyNode.xml')
        arguments.append('--use-compress-program')
        arguments.append(pigz)
        arguments.append('-f')
        arguments.append(os.path.join(tarDirRoot, tarName))
        arguments.append('--directory')
        arguments.append(node.getNodeRootDir())
        arguments.append('.')

        pColor = self.new_process_color()

        process = QProcess(self)
        process.readyReadStandardOutput.connect(lambda: self.data_ready_std(process, pColor))
        process.readyReadStandardError.connect(lambda: self.dataReadyErr(process, pColor))
        process.started.connect(lambda: self.checkOutOnStarted(process))
        process.finished.connect(lambda: self.checkoutOnFinished(process, node, tarName))

        process.start(self.tarExec, arguments)

        '''
        checkOutFilePath = os.path.join(node.getNodeRootDir(), 'checkedOut')
        checkOutFile = open(checkOutFilePath, 'a')
        checkOutFile.write(self.user)
        checkOutFile.close()
        '''

    def checkInCallback(self, node):
        def callback():
            self.checkIn(node)
        return callback

    def checkIn(self, node):
        try:
            checkOutFilePath = os.path.join(node.getNodeRootDir(), 'checkedOut')
            os.remove(checkOutFilePath)
        except:
            #print 'check in failed'
            logging.warning('check in failed')

    def taskOnStarted(self, node, qprocess, screenCast, timeTracker):

        self.qprocesses.append(qprocess)
        self.openNodes.append(node)
        #print self.qprocesses

        logging.info('task %s started' %node.getLabel())
        # #self.
        # #asset = os.path.basename(self.asset)
        # #print asset
        #
        # #self.mainWindow.sendTextToBox("%s: starting %s (PID %s). Enjoy!\n" %(datetime.datetime.now(), self.data(0).toPyObject(), self.pid))
        #

        lockFilePath = os.path.join(node.getNodeRootDir(), 'locked')
        lockFile = open(lockFilePath, 'a')
        lockFile.write(self.user)
        lockFile.close()
        #
        if self.screenCastActive:
            screenCast.start()
            self.screenCasts.append(screenCast)
            self.addNewScreenCast.emit()

        timeTracker.start()
        self.timeTrackers.append(timeTracker)

    def task_on_finished(self, node, qprocess, screenCast, timeTracker):
        logging.info('task %s finished' %node.getLabel())

        if self.screenCastActive and screenCast in self.screenCasts:
            screenCast.stop()
            self.screenCasts.remove(screenCast)
            self.addNewScreenCast.emit()

        timeTracker.stop()
        self.timeTrackers.remove(timeTracker)

        os.remove(os.path.join(node.getNodeRootDir(), 'locked'))

        self.openNodes.remove(node)
        self.qprocesses.remove(qprocess)

    # def compute_value_applications_(self):
    #     return self._tools

    # def getOutputs(self):
    #     return self.outputs

    def getTasks(self):
        return self.tasks
        
    def getTools(self):
        return self._tools

    def locateContentCallback(self, contentFiles):
        def callback():
            self.locateContent(contentFiles)
        return callback

    def locateContent(self, contentFiles):
        #print contentFiles
        if os.path.exists(contentFiles):
            if self.currentPlatform == 'Windows':
                subprocess.call(self.fileExplorer + ' ' + contentFiles, shell = False)
            elif self.currentPlatform == 'Darwin':
                subprocess.Popen([self.fileExplorer, contentFiles], shell = False)
            elif self.currentPlatform == 'Linux':
                subprocess.Popen([self.fileExplorer, contentFiles], shell = False)
            else:
                self.sendTextToBox('platform %s not supported\n' %(self.currentPlatform))
        else:

            logging.warning('project does not exist:', contentFiles)
    
    def cloneContent(self, contentFiles):
        tabIndex = self.assetsShotsTabWidget.currentIndex()
        #print contentFiles
        cloneExtension = '_clone'
        cloneDestination = contentFiles + cloneExtension
        
        shutil.copytree(contentFiles, cloneDestination)
        
        self.sendTextToBox('content at %s cloned to %s\n' %(contentFiles, cloneDestination))
        
        self.add_content()
        self.assetsShotsTabWidget.setCurrentIndex(tabIndex)
    
    def removeContent(self, contentFiles):
        tabIndex = self.assetsShotsTabWidget.currentIndex()
        #print contentFiles
        
        shutil.rmtree(contentFiles)
        logging.info('content removed from filesystem: %s' %(contentFiles))
        self.sendTextToBox('content removed from filesystem: %s\n' %(contentFiles))
        
        self.add_content()
        self.refreshProjects()
        self.assetsShotsTabWidget.setCurrentIndex(tabIndex)


    
    def create_new_content(self):
        tab_index = self.assetsShotsTabWidget.currentIndex()



        # print tab_index
        # print self.content_tabs[tab_index]
        # print self.content_tabs[tab_index]['content']

        text, ok = QInputDialog.getText(self, 'create new %s' %(self.content_tabs[tab_index]['content']), 'enter %s name:' %(self.content_tabs[tab_index]['content']))

        current_target = os.path.join(self.projectsRoot, self._current_project, 'content', self.content_tabs[tab_index]['content'])
            
        new_content = os.path.join(current_target, str(text))

        # TODO: capture invalid characters. see newNode.setStatus()

        if ok:
            if not os.path.exists(new_content):
                os.makedirs(new_content, mode = 0777)
                self.add_content()
                self.sendTextToBox('content created on filesystem: %s\n' % new_content)
                logging.info('content created on filesystem: %s' % new_content)

            else:
                self.sendTextToBox('content not created because it already exists (%s)\n' % new_content)
                self.sendTextToBox('choose different name.\n')
                logging.warning('content not created because it already exists (%s)' % new_content)

    # def getPypelyneRoot(self):
    #     return self.pypelyneRoot

    def setNodeWidget(self, node):
        self.widgetUi = NodeWidgetUi(self)

        # print node.data(0)
            
        self.nodeMenuArea.setWidget(self.widgetUi)

        # self.nodeVersion, self.nodeVendor, self.nodeFamily, self.nodeArch
        self.nodeApplicationInfo = node.queryApplicationInfo()

        self.widgetUi.labelNode.setText(node.data(0))
        self.widgetUi.labelApplication.setText(self.nodeApplicationInfo[2] + ' ' + self.nodeApplicationInfo[0])
        #self.widgetUi.labelVersion.setText(self.nodeApplicationInfo[0])

    def clearNodeWidget(self):
        #self.nodeWidgets = []
        self.nodeMenuArea.takeWidget()
        
    def configurationWindow(self):
        self.configWindow = pypelyneConfigurationWindow()
        self.configWindow.show()

    def computeConnections(self):
        logging.info('computeConnections...')
        # get all nodes
        nodeList = self.scene._node_list
        # for each node
        for nodeDst in nodeList:
            logging.info('%s:' %(nodeDst.data(0)))
            # get node inputs
            nodeRootDir = nodeDst.getNodeRootDir()
            nodeInputDir = os.sep.join([str(nodeRootDir), 'input'])
            #endItems =
            inputs = os.listdir(nodeInputDir)
            #print inputs
            # for each input

            for input in  inputs:
                if len(inputs) > 0 and not input in self.exclusions:
                    logging.info('\tprocessing input %s' %(input))
                    # input circle = endItem
                    endItem = nodeDst.inputList[len(nodeDst.inputs)]
                    # find connected node (string[2])
                    inputString = input.split('.')
                    #print inputString
                    inputContent = inputString[0]
                    inputAsset = inputString[1]
                    inputNode = inputString[2]
                    inputOutput = inputString[3]

                    nodeDstAssetDir = nodeDst.getNodeAsset()
                    #print nodeDst.getNodeAsset()
                    for nodeSrc in nodeList:
                        #print input.getInputDir()
                        #print nodeSrc.getNodeRootDir()
                        nodeSrcRootDir = nodeSrc.getNodeRootDir()
                        nodeSrcRootDirBasename = os.path.basename(nodeSrcRootDir)

                        #print nodeSrcRootDir
                        #print os.path.join(nodeDstAssetDir, inputNode)



                        # if inputContent == 'assets':
                        #     content = 'AST'
                        # elif inputContent == 'shots':
                        #     content = 'SHT'

                        outputItems = nodeSrc.outputList

                        #print 'nodeSrcRootDir:', nodeSrcRootDir
                        #print 'os.path.join:', os.path.join(nodeDstAssetDir, 'LDR_LIB__' + inputAsset)


                        if nodeSrcRootDir == os.path.join(nodeDstAssetDir, inputNode):
                            logging.info('\t\tnodeSrc is a task')
                            logging.info('\t\tnodeSrc is %s' %(nodeSrc.data(0)))
                            logging.info('\t\tlooking for output called %s' %(inputOutput))
                            for outputItem in outputItems:
                                logging.info('\t\t\tprocessing output %s' %(outputItem.data(0)))
                                if outputItem.data(0) == inputOutput:
                                    logging.info('\t\t\t\t found output %s' %(outputItem.data(0)))
                                    startItem = outputItem
                                    #startItem =
                                    #break
                                #else:
                                #    print '\t\t\t\tnot found'



                        #special case for library loader
                        elif nodeSrc.label.startswith('LDR_LIB__'):
                            logging.info('\t\tnodeSrc is a library loader')
                            logging.info('\t\tnodeSrc is %s' %(nodeSrc.data(0)))
                            logging.info('\t\tlooking for output called %s' %(inputOutput))
                            for outputItem in outputItems:
                                logging.info('\t\t\tprocessing output %s' %(outputItem.data(0).split('.')[3]))
                                #print nodeSrc.data(0).toPyObject()
                                logging.info('\t\tlooking for output called %s' %(inputOutput))
                                searchString = outputItem.data(0).split('.')[3]
                                if searchString == inputOutput:
                                    logging.info('\t\t\t\t found output %s' %(outputItem.data(0).split('.')[3]))
                                    startItem = outputItem

                        else:
                            for tab in self.content_tabs:
                                if nodeSrcRootDir == os.path.join(nodeDstAssetDir, 'LDR_' + tab['abbreviation'] + '__' + inputAsset):
                                    logging.info('\t\tnodeSrc is a loader')
                                    logging.info('\t\tnodeSrc is %s' %(nodeSrc.data(0)))
                                    logging.info('\t\tlooking for output called %s' %(inputOutput))
                                    for outputItem in outputItems:
                                        logging.info('\t\t\tprocessing output %s' %(outputItem.data(0).split('.')[3]))
                                        #print nodeSrc.data(0).toPyObject()
                                        logging.info('\t\tlooking for output called %s' %(inputOutput))
                                        searchString = outputItem.data(0).split('.')[3]
                                        if searchString == inputOutput:
                                            logging.info('\t\t\t\t found output %s' %(outputItem.data(0).split('.')[3]))
                                            startItem = outputItem
                                            #endItem = nodeDst.inputList[len(nodeDst.inputs)]
                                            #connectionLine = bezierLine(self, self.scene, startItem, endItem)
                                            #break
                                        #else:
                                        #    print '\t\t\t\tnot found'



                    endItem = nodeDst.inputList[len(nodeDst.inputs)]

                    connectionLine = bezierLine(self, self.scene, startItem, endItem)

                    endItem.parentItem().inputs.append(endItem)
                    endItem.connection.append(connectionLine)
                    endItem.output.append(startItem)
                    endItem.parentItem().incoming.append(startItem)
                    startItem.inputs.append(endItem)

                    startItemRootDir = startItem.parentItem().getNodeRootDir()
                    endItemRootDir = endItem.parentItem().getNodeRootDir()

                    startItemOutputLabel = startItem.getLabel()

                    endItemInputDir = os.path.join(str(endItemRootDir), 'input', str(input))

                    endItem.setInputDir(endItemInputDir)

                    self.scene.addItem(connectionLine)

                    endItem.parentItem().newInput(self.scene)


                elif input in self.exclusions:
                    logging.info('input data is in exclusions list')

                else:
                    logging.info('node %s has no input' %(node.data(0)))


        #except:
        #    logging.warning('computeConnections error. aborted.')



        
    def computeConnectionsOld(self):
        '''
        - get all nodes
        - for each node
            - get node inputs
            - for each input
                - input circle = endItem
                - find connected node (string[2])
                    - find corresponding output circle (string[3])
                        - output circle = startItem
        :return:
        '''
        '''
        :return:
        '''
        print 'computeConnections...'
        nodeList = self.scene._node_list
        # for node in nodeList:
        #     print node.data(0).toPyObject()
        #print any(node for node in nodeList if node.data(0).toPyObject() == 'fnuzjr')
        #for node in nodeList:
        #    if node.data(0).toPyObject() == 'fnuzjr':
        #        print 'node found at index %s' %(nodeList.index(node))
        for node in nodeList:
            currentNode = node
            print 'processing %s (%s)' %(node.data(0), node)
            nodeRootDir = node.getNodeRootDir()
            nodeInputDir = os.sep.join([str(nodeRootDir), 'input'])
            print 'nodeInputDir = %s' %nodeInputDir
            inputs = os.listdir(nodeInputDir)
            if len(inputs) > 0:
                for input in inputs:
                    if not input in self.exclusions:
                        string = input.split('.')
                        x = 0
                        for node in nodeList:
                            # print x, node.data(0).toPyObject()
                            x += 1
                            # print 'nodeList 123:', nodeList
                            # print string[2]
                            if node.data(0) == string[2] or str(node.data(0)).startswith('LDR'):

                                sourceNodeIndex = nodeList.index(node)

                                sourceNode = node

                                outputList = node.outputList

                                for output in outputList:
                                    print 'processing =', output.data(0)
                                    if len(str(output.data(0)).split('.')) == 1:
                                        if output.data(0) == string[3]:
                                            startItem = output
                                            print 'if: startItem =', startItem

                                    else:
                                        # print 'hallo'
                                        if str(output.data(0)).split('.')[3] == string[3]:
                                            # print 'velo'
                                            startItem = output

                        endItem = currentNode.inputList[len(currentNode.inputs)]

                        print 'new line from %s to %s' %(startItem.data(0), endItem)



                        connectionLine = bezierLine(self, self.scene, startItem, endItem)

                        '''

                        endItem.parentItem().inputs.append(endItem)
                        #endItem.connection.append(connectionLine)
                        endItem.output.append(startItem)
                        endItem.parentItem().incoming.append(startItem)
                        startItem.inputs.append(endItem)

                        startItemRootDir = startItem.parentItem().getNodeRootDir()
                        endItemRootDir = endItem.parentItem().getNodeRootDir()

                        startItemOutputLabel = startItem.getLabel()

                        endItemInputDir = os.path.join(str(endItemRootDir), 'input', str(input))

                        endItem.setInputDir(endItemInputDir)

                        self.scene.addItem(connectionLine)

                        endItem.parentItem().newInput(self.scene)

                        '''

                    else:
                        print 'input data is in exclusions list'
                    
            else:
                print 'node %s has no input' %(node.data(0))

    def getPropertyPaths(self):
        return self.propertyNodePathAssets, self.propertyNodePathShots

    @property
    def _current_content_item(self):
        return str(self.current_content_item)

    def get_content(self, button = None, node_label = None):


        if button is not None:
            button_text = button.text()
            content = self._current_content['content']
        elif node_label is not None:
            button_text = node_label.split('__')[1]
            for tab in self.content_tabs:
                if tab['abbreviation'] == node_label.split('__')[0].split('_')[1]:
                    content = tab['content']
                    break

        ######

        for tab in self.content_tabs:
            self.group_boxes[self.content_tabs.index(tab)].setTitle('looking at ' + self._current_project + os.sep + self._current_content['content'] + os.sep + button_text)

        self.current_content_item = button_text

        # self.group_boxes[self.content_tabs.index(self._current_content)].setTitle('looking at ' + self._current_project + os.sep + self._current_content + os.sep + button_text)

        self.nodeView.setVisible(True)

        self.scene.clear()
        # self.addRectangular()
        self.scene.clearNodeList()

        content_root = os.path.join(self.projectsRoot, self._current_project, 'content', content)
        content_items = os.listdir(os.path.join(content_root, str(button_text)))

        for node_item in content_items:
            if node_item not in self.exclusions:
                if os.path.isdir(os.path.join(content_root, str(button_text), node_item)):
                    node_path = os.path.join(content_root, str(button_text), node_item)
                    # convert xml to json if propertyNode.xml is found
                    property_node_path = os.path.join(node_path, 'propertyNode.xml')
                    if os.path.exists(property_node_path):
                        new_name = os.path.join(node_path, 'converted_propertyNode.xml')

                        property_node = ET.parse(property_node_path)
                        logging.info('new style reading xml')
                        node_position = property_node.findall('./node')

                        pos_x = node_position[0].items()[0][1]
                        pos_y = node_position[0].items()[1][1]

                        # print pos_x
                        # print pos_y

                        node_task = property_node.findall('./task')

                        # for i in node_task[0].items():
                        #     print i

                        try:
                            arch = node_task[0].items()[0][1]
                            # print arch
                            family = node_task[0].items()[4][1]
                            # print family
                            for tool in self._tools:
                                # print tool
                                if tool['family'] == family:
                                    abbreviation = tool['abbreviation']
                            # abbreviation = 'UVLayout'
                            task = node_task[0].items()[1][1]
                            vendor = node_task[0].items()[2][1]
                            version = node_task[0].items()[3][1]

                            meta_task = {}
                            meta_tool = {}

                            meta_task['pos_x'] = pos_x
                            meta_task['pos_y'] = pos_y
                            meta_task['creator'] = 'nobody'
                            meta_task['operating_system'] = self.operating_system
                            meta_task['task'] = task

                            meta_tool['family'] = family
                            meta_tool['architecture_fallback'] = False
                            meta_tool['abbreviation'] = abbreviation
                            meta_tool['architecture'] = arch
                            meta_tool['vendor'] = vendor
                            meta_tool['release_number'] = version

                            meta_task_path = os.path.join(node_path, 'meta_task.json')
                            meta_tool_path = os.path.join(node_path, 'meta_tool.json')

                            with open(meta_task_path, 'w') as outfile:
                                json.dump(meta_task, outfile)
                                outfile.close()

                            with open(meta_tool_path, 'w') as outfile:
                                json.dump(meta_tool, outfile)
                                outfile.close()

                            os.rename(property_node_path, new_name)

                        except IndexError, e:
                            # TODO: special treatment for loaders and savers needed
                            print e

                    meta_task_path = os.path.join(content_root, str(button_text), node_item, 'meta_task.json')
                    meta_tool_path = os.path.join(content_root, str(button_text), node_item, 'meta_tool.json')

                    new_node = node(main_window=self, scene=self.scene, property_node_path=None, meta_task_path=meta_task_path, meta_tool_path=meta_tool_path)
                    new_node.addText(self.scene, node_item)
                    self.scene.addToNodeList(new_node)
                else:
                    logging.warning('shots: nodeItem %s is not a directory' % node_item)
            else:
                os.remove(os.path.join(content_root, str(button_text), node_item))
                logging.info('exclusion %s found and cleaned' % node_item)

        self.computeConnections()

    # def getShotContent(self, shotButton = None, nodeShtLabel = None):
    #     #print shotButton
    #     #print nodeShtLabel
    #
    #     if not shotButton == None:
    #         #print shotButton.text()
    #         buttonText = shotButton.text()
    #     elif not nodeShtLabel == None:
    #         buttonText = nodeShtLabel.split('__')[1]
    #         #print buttonText
    #
    #
    #
    #
    #     self.nodeView.setVisible(True)
    #
    #
    #
    #
    #     self.scene.clear()
    #     self.addRectangular()
    #     self.scene.clearNodeList()
    #     currentProject = str(self.projectComboBox.currentText())
    #     self.shotsRoot = os.path.join(self.projectsRoot, currentProject, 'content', 'shots')
    #     shotContent = os.listdir(os.path.join(self.shotsRoot, str(buttonText)))
    #
    #     for tab in self.content_tabs:
    #         self.group_boxes[self.content_tabs.index(tab)].setTitle('looking at ' + self._current_project + os.sep + self._current_content['content'] + os.sep + button_text)
    #
    #     self.currentContent = currentProject + os.sep + 'content' + os.sep + 'shots' + os.sep + buttonText
    #
    #     for nodeItem in shotContent:
    #         if not nodeItem in self.exclusions:
    #             if os.path.isdir(os.path.join(self.shotsRoot, str(buttonText), nodeItem)):
    #
    #                 self.propertyNodePathShots = os.path.join(self.shotsRoot, str(buttonText), nodeItem, 'propertyNode.xml')
    #
    #                 newNode = node(self, self.scene, self.propertyNodePathShots)
    #                 newNode.addText(self.scene, nodeItem)
    #                 self.scene.addToNodeList(newNode)
    #             else:
    #                 logging.warning('shots: nodeItem %s is not a directory' %(nodeItem))
    #
    #         else:
    #             os.remove(os.path.join(self.shotsRoot, str(buttonText), nodeItem))
    #             logging.info('exclusion %s found and cleaned' %(nodeItem))
    #
    #
    #     self.computeConnections()
            
        
    def getCurrentProject(self):
        currentProject = str(self.projectComboBox.currentText())
        self.assetsRoot = os.path.join(self.projectsRoot, currentProject)
        return currentProject
        
    @property
    def _current_project(self):
        return str(self.projectComboBox.currentText())
    
    # def getAssetContent(self, assetButton = None, nodeAstLabel = None):
    #
    #
    #     if not assetButton == None:
    #         buttonText = assetButton.text()
    #     elif not nodeAstLabel == None:
    #         buttonText = nodeAstLabel.split('__')[1]
    #
    #     self.nodeView.setVisible(True)
    #
    #
    #     self.scene.clear()
    #     self.addRectangular()
    #     self.scene.clearNodeList()
    #     currentProject = str(self.projectComboBox.currentText())
    #     self.assetsRoot = os.path.join(self.projectsRoot, currentProject, 'content', 'assets')
    #     assetContent = os.listdir(os.path.normpath(os.path.join(str(self.assetsRoot), str(buttonText))))
    #
    #     for tab in self.content_tabs:
    #         self.group_boxes[self.content_tabs.index(tab)].setTitle('looking at ' + self._current_project + os.sep + self._current_content['content'] + os.sep + button_text)
    #
    #     self.currentContent = currentProject + os.sep + 'content' + os.sep + 'assets' + os.sep + buttonText
    #
    #     for nodeItem in assetContent:
    #
    #         if not nodeItem in self.exclusions:
    #             if os.path.isdir(os.path.join(self.assetsRoot, str(buttonText), nodeItem)):
    #                 self.propertyNodePathAssets = os.path.join(self.assetsRoot, str(buttonText), nodeItem, 'propertyNode.xml')
    #
    #                 newNode = node(self, self.scene, self.propertyNodePathAssets)
    #                 newNode.addText(self.scene, nodeItem)
    #                 self.scene.addToNodeList(newNode)
    #
    #             else:
    #                 logging.warning('assets: nodeItem %s is not a directory' %(nodeItem))
    #         else:
    #             os.remove(os.path.join(self.assetsRoot, str(buttonText), nodeItem))
    #             logging.info('exclusion %s found and cleaned' % nodeItem)
    #
    #     self.computeConnections()

    def print_sth(self):
        print 'hallo'

    def add_content(self):
        current_index = self.assetsShotsTabWidget.currentIndex()

        self.assetsShotsTabWidget.clear()

        self.buttons = {}
        self.group_boxes = {}
        # for i in range(1,10,1)
        #     buttons[i] = 100 / i
        #     print x[i]

        for tab in self.content_tabs:
            content = []

            # currentProject = str(self.projectComboBox.currentText())

            # print 'self.content_tabs[self.content_tabs.index(tab)]', self.content_tabs[self.content_tabs.index(tab)]['content']

            content_root = os.path.join(self.projectsRoot, self._current_project, 'content', self.content_tabs[self.content_tabs.index(tab)]['content'])

            try:
                for i in os.listdir(content_root):
                    if i not in self.exclusions:
                        content.append(i)
            except WindowsError, e:
                logging.warning('no %s root found: %s' % (self.content_tabs[self.content_tabs.index(tab)]['content'], e))

            self.group_boxes[self.content_tabs.index(tab)] = QGroupBox(self._current_project)
            layout_content = QHBoxLayout()
            create_content_push_button = QPushButton('create new %s' % self.content_tabs[self.content_tabs.index(tab)]['content'])
            create_content_push_button.clicked.connect(self.create_new_content)
            layout_content.addWidget(create_content_push_button)


            self.buttons[self.content_tabs.index(tab)] = QButtonGroup()
            # content_button_group.buttonClicked[QAbstractButton].connect(self.getContent)
            # self.buttons[self.content_tabs.index(tab)].buttonClicked[QAbstractButton].connect(self.print_sth)
            self.buttons[self.content_tabs.index(tab)].buttonClicked[QAbstractButton].connect(self.get_content)

            for i in content:
                content_push_button = QPushButton(i)
                content_push_button.setContextMenuPolicy(Qt.CustomContextMenu)
                self.connect(content_push_button, SIGNAL('customContextMenuRequested(const QPoint&)'), self.content_context_menu)
                layout_content.addWidget(content_push_button)
                self.buttons[self.content_tabs.index(tab)].addButton(content_push_button)
                logging.info('%s %s found' % (self.content_tabs[self.content_tabs.index(tab)]['content'], i))

            layout_content.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

            self.group_boxes[self.content_tabs.index(tab)].setLayout(layout_content)
            scroll_content = QScrollArea()
            scroll_content.setWidget(self.group_boxes[self.content_tabs.index(tab)])
            scroll_content.setWidgetResizable(True)
            scroll_content.setFixedHeight(90)
            layout_content_scroll = QVBoxLayout()
            layout_content_scroll.addWidget(scroll_content)

            widget_content = QWidget()
            widget_content.setLayout(layout_content_scroll)

            # TODO: refactor assetsShotTabWidget name
            self.assetsShotsTabWidget.addTab(widget_content, tab['content'])

        # print self.buttons
        self.assetsShotsTabWidget.setCurrentIndex(current_index)

        '''

        assets = []
        shots = []

        currentProject = str(self.projectComboBox.currentText())
        self.assetsRoot = os.path.join(self.projectsRoot, currentProject, 'content', 'assets')
        self.shotsRoot = os.path.join(self.projectsRoot, currentProject, 'content', 'shots')
        try:
            for i in os.listdir(self.assetsRoot):
                if not i in self.exclusions:
                    assets.append(i)
        except:
            logging.warning('no assetsRoot found')

        try:
            for i in os.listdir(self.shotsRoot):
                if not i in self.exclusions:
                    shots.append(i)
        except:
            logging.warning('no shotsRoot found')

        #Assets

        self.assetsGroupBox = QGroupBox(currentProject)
        layoutAssets = QHBoxLayout()
        self.createAssetPushButton = QPushButton('create new asset')
        self.createAssetPushButton.clicked.connect(self.create_new_content)
        layoutAssets.addWidget(self.createAssetPushButton)

        self.assetButtonGroup = QButtonGroup()
        self.assetButtonGroup.buttonClicked[QAbstractButton].connect(self.getAssetContent)

        for i in assets:
            assetPushButton = QPushButton(i)
            assetPushButton.setContextMenuPolicy(Qt.CustomContextMenu)
            self.connect(assetPushButton, SIGNAL('customContextMenuRequested(const QPoint&)'), self.content_context_menu)
            layoutAssets.addWidget(assetPushButton)
            self.assetButtonGroup.addButton(assetPushButton)
            logging.info('asset %s found' %(i))

        layoutAssets.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.assetsGroupBox.setLayout(layoutAssets)
        scrollAssets = QScrollArea()
        scrollAssets.setWidget(self.assetsGroupBox)
        scrollAssets.setWidgetResizable(True)
        scrollAssets.setFixedHeight(90)
        layoutAssetsScroll = QVBoxLayout()
        layoutAssetsScroll.addWidget(scrollAssets)

        widgetAssets = QWidget()
        widgetAssets.setLayout(layoutAssetsScroll)
        
        #Shots
        
        self.shotsGroupBox = QGroupBox(currentProject)
        layoutShots = QHBoxLayout()
        
        self.createShotPushButton = QPushButton('create new shot')
        self.createShotPushButton.clicked.connect(self.create_new_content)
        layoutShots.addWidget(self.createShotPushButton)
        
        self.shotButtonGroup = QButtonGroup()
        self.shotButtonGroup.buttonClicked[QAbstractButton].connect(self.getShotContent)
        
        for i in shots:
            shotPushButton = QPushButton(i)
            shotPushButton.setContextMenuPolicy(Qt.CustomContextMenu)
            self.connect(shotPushButton, SIGNAL('customContextMenuRequested(const QPoint&)'), self.content_context_menu)
            layoutShots.addWidget(shotPushButton)
            self.shotButtonGroup.addButton(shotPushButton)
            logging.info('shot %s found' %(i))
        
        layoutShots.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.shotsGroupBox.setLayout(layoutShots)
        scrollShots = QScrollArea()
        scrollShots.setWidget(self.shotsGroupBox)
        scrollShots.setWidgetResizable(True)
        scrollShots.setFixedHeight(90)
        layoutShotsScroll = QVBoxLayout()
        layoutShotsScroll.addWidget(scrollShots)
        
        widgetShots = QWidget()
        widgetShots.setLayout(layoutShotsScroll)

        self.assetsShotsTabWidget.clear()

        self.assetsShotsTabWidget.addTab(widgetAssets, 'assets')
        self.assetsShotsTabWidget.addTab(widgetShots, 'shots')
    '''

    def content_context_menu(self, point):
        
        sendingButton = self.sender()
        sendingButtonText = sendingButton.text()

        tab_index = self.assetsShotsTabWidget.currentIndex()

        # print tab_index
        # print self.content_tabs[tab_index]
        # print self.content_tabs[tab_index]['content']
        # print self.content_tabs

        current_target = os.path.join(self.projectsRoot, self._current_project, 'content', self.content_tabs[tab_index]['content'])

        # if tab_index == 0:
        #     current_target = self.assetsRoot
        #
        # elif tab_index == 1:
        #     current_target = self.shotsRoot
            
        contentLocation = os.path.join(str(current_target), str(sendingButtonText))

        popMenu = QMenu(self)
        popMenu.addAction('open directory', lambda: self.locateContent(contentLocation))
        popMenu.addAction('clone', lambda: self.cloneContent(contentLocation))
        popMenu.addAction('disable', self.foo)
        popMenu.addSeparator()
        popMenu.addAction('delete', lambda: self.removeContent(contentLocation))

        popMenu.exec_(sendingButton.mapToGlobal(point))
        

    def fooCallback(self, arg = None):
        def callback():
            self.foo(arg)
        return callback


    def foo(self, arg = None):
        try:
            print arg
        except:
            pass
    
    
    def printShit(self, button):
        print button.text()
    
    
    def addProjects(self):
        self.projectComboBox.clear()
        self.projectComboBox.addItem('select project')
        self.projectComboBox.insertSeparator(1)

        if self.serverAlive == True:
            try:
                self.socket.sendall('addProjectsServer')
                projects = self.receiveSerialized(self.socket)[2]
            except:
                logging.warning('could not get projects from server')
                projects = []
            #print projects

            #try:
            #    for i in projects:
            #        if os.path.isdir(os.path.join(self.projectsRoot, i)):

        else:
            #self.sendTextToBox('looking for projects in %s:\n' %(self.projectsRoot))
            #self.projectComboBox.clear()
            try:
                projects = os.listdir(self.projectsRoot)
            except:
                logging.warning('could not find projects')
                projects = []


        logging.info('using projects root: %s' %(self.projectsRoot))

        for exclusion in self.exclusions:
            try:
                projects.remove(exclusion)
                os.remove(os.path.join(self.projectsRoot, exclusion))
                logging.info('exclusion in projectsRoot removed')
            except:
                pass


        for i in projects:
            #print i
            #if os.path.isdir(os.path.join(self.projectsRoot, i)):
            self.projectComboBox.addItem(i)
            self.sendTextToBox('\tproject %s found\n' %(i))
            logging.info('project %s found' %(i))

        self.sendTextToBox('all projects added.\n\n')
        self.projectComboBox.activated.connect(self.refreshProjects)
        
        
    def refreshProjects(self):
        
        self.nodeView.setVisible(False)
        
        indexText = self.projectComboBox.currentText()
        
        index = self.projectComboBox.findText(indexText)
        
        self.projectComboBox.setCurrentIndex(index)
        
        if not indexText == 'select project' and not indexText == 'create new project':
            self.assetsShotsTabWidget.clear()
            self.add_content()
            self.assetsShotsTabWidget.setVisible(True)
            #self.nodeView.setVisible(True)
            self.openPushButton.setEnabled(True)

            
            
        else:
            self.assetsShotsTabWidget.setVisible(False)
            self.nodeView.setVisible(False)
            self.assetsShotsTabWidget.clear()
            #print 'no project selected'
            self.openPushButton.setEnabled(False)
        
        self.scene.clear()

    # TODO: create method that returns the dicts for x_32 and x_64 (to shorten run_item = {})
    # newNode.py:137 ff
    # here:
        
    def add_tools(self):
        self.toolsComboBox.clear()
        self.toolsComboBox.addItem('run tool instance')
        
        self.toolsComboBox.insertSeparator(1)
        
        for tool_item in self._tool_items:
            print tool_item
            self.toolsComboBox.addItem(tool_item[u'label'], tool_item)

    def get_dict_x32(self, tool):
        dict_x32 = {
                    u'project_template': tool[u'project_template'],
                    u'abbreviation': tool[u'abbreviation'],
                    u'vendor': tool[u'vendor'],
                    u'family': tool[u'family'],
                    u'architecture_fallback': tool[u'architecture_fallback'],
                    u'flags': tool[u'flags_x32'],
                    u'release_number': tool[u'release_number'],
                    u'project_directories': tool[u'project_directories'],
                    u'default_outputs': tool[u'default_outputs'],
                    u'executable': tool[u'executable_x32'],
                    u'project_workspace': tool[u'project_workspace'],
                    u'label': tool[u'label_x32'],
                    u'architecture': u'x32'
                    }

        return dict_x32

    def get_dict_x64(self, tool):
        dict_x64 = {
                    u'project_template': tool[u'project_template'],
                    u'abbreviation': tool[u'abbreviation'],
                    u'vendor': tool[u'vendor'],
                    u'family': tool[u'family'],
                    u'label': tool[u'label_x64'],
                    u'executable': tool[u'executable_x64'],
                    u'architecture_fallback': tool[u'architecture_fallback'],
                    u'release_number': tool[u'release_number'],
                    u'project_directories': tool[u'project_directories'],
                    u'default_outputs': tool[u'default_outputs'],
                    u'project_workspace': tool[u'project_workspace'],
                    u'flags': tool[u'flags_x64'],
                    u'architecture': u'x64'
                    }

        return dict_x64

    def submitDeadlineJob(self, jobFile):

        executable = '/bin/bash'

        executable = executable.replace('\"', '')
        executable = executable.replace('\'', '')
        if executable.endswith(' '):
            executable = executable[:-1]

        #now = datetime.datetime.now()

        arguments = QStringList()

        arguments.append(jobFile)

        process = QProcess(self)

        pColor = self.new_process_color()

        process.readyReadStandardOutput.connect(lambda: self.data_ready_std(process, pColor))
        process.readyReadStandardError.connect(lambda: self.dataReadyErr(process, pColor))
        process.started.connect(lambda: self.toolOnStarted(process))
        process.finished.connect(lambda: self.toolOnFinished(process))

        process.start(executable, arguments)

    def run_tool(self):
        index_combobox = self.toolsComboBox.currentIndex()
        dict_combobox = self.toolsComboBox.itemData(index_combobox)

        # pydict = eval( str( self.toolsComboBox.itemData(index_combobox).toString() ) )
        #
        # print pydict

        # print self.toolsComboBox.itemData(index_combobox)
        # print self.toolsComboBox.itemData(index_combobox)['executable']
        # print index_tools

        if index_combobox < 2:
            self.sendTextToBox("%s: nothing to run\n" % datetime.datetime.now())

        else:
            # if not self._tools[index_tools]['executable_x64'] is None:
            #     if os.path.exists(os.path.normpath(self._tools[index_tools]['executable_x64'])):
            logging.info('%s: starting %s' % (datetime.datetime.now(), dict_combobox['executable']))
            self.sendTextToBox('%s: starting %s. Enjoy!\n' % (datetime.datetime.now(), dict_combobox['executable']))

            process = QProcess(self)

            process_color = self.new_process_color()

            process.readyReadStandardOutput.connect(lambda: self.data_ready_std(process, process_color))
            process.readyReadStandardError.connect(lambda: self.dataReadyErr(process, process_color))
            process.started.connect(lambda: self.toolOnStarted(process))
            process.finished.connect(lambda: self.toolOnFinished(process))

            temp_pypelyne_dir = os.path.join(os.path.expanduser('~'), 'pypelyne_temp')
            current_dir = os.getcwd()
            date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')

            if not os.path.exists(temp_pypelyne_dir):
                os.makedirs(temp_pypelyne_dir, mode=0777)

            if dict_combobox['project_template'] is not None:
                name, extension = os.path.splitext(dict_combobox['project_template'])
                temp_project = str(name + '.' + date_time + extension)
                temp_project_dir = str(name + '.' + date_time)
                src = os.path.join('src', 'template_documents', dict_combobox['project_template'])
                dst = os.path.join(temp_pypelyne_dir, temp_project_dir, temp_project)

                os.makedirs(os.path.join(temp_pypelyne_dir, temp_project_dir), mode=0777)

                shutil.copyfile(src, dst)

                os.chdir(os.path.join(temp_pypelyne_dir, temp_project_dir))

                # arguments = QStringList()
                arguments = []

                for flag in dict_combobox['flags']:
                    arguments.append(flag)

                arguments.append(dst)

                process.start(dict_combobox['executable'], arguments)
                os.chdir(current_dir)

            elif dict_combobox['family'].lower() == 'deadline':
                os.chdir(temp_pypelyne_dir)
                process.start(dict_combobox['executable'])
                os.chdir(current_dir)
            else:
                temp_project_dir = 'no_template_' + dict_combobox['vendor'] + '_' + dict_combobox['family'] + '_' + dict_combobox['release_number'] + '.' +  date_time
                temp_project_dir_full = os.path.join(temp_pypelyne_dir, temp_project_dir)
                os.makedirs(temp_project_dir_full, mode=0777)

                os.chdir(temp_project_dir_full)

                process.start(dict_combobox['executable'])
                os.chdir(current_dir)
                # else:
                #     self.sendTextToBox("%s: cannot start %s. is it installed?\n" % (datetime.datetime.now(), self._tools[index_tools]['executable']))

        self.toolsComboBox.setCurrentIndex(0)

    def checkOutOnStarted(self, qprocess):
        self.qprocesses.append(qprocess)

    def checkoutOnFinished(self, qprocess, node, tarName):
        tarNameSplit = tarName.split(self.tarSep)
        #        0                1        2          3           4
        #2015-08-27_1134-42_____test_____assets_____asdf_____SVR_AST__asdf.tar.gz
        #projectName = os.path.basename(os.path.dirname(node.getNodeAsset()))
        projectName = tarNameSplit[1]
        contentFamily = tarNameSplit[2][:-1]
        #contentName = os.path.basename(node.getNodeAsset())
        contentName = tarNameSplit[3]
        nodeName = tarNameSplit[4].split('.')[0]
        #nodeName = node.label
        self.qprocesses.remove(qprocess)
        QMessageBox.information(self, 'check out finished', str('node %s successfully checked out\nproject:\t%s\n%s:\t%s\n\narchive file: %s' %(nodeName, projectName, contentFamily, contentName, tarName)), QMessageBox.Ok, QMessageBox.Ok)
        return

    def toolOnStarted(self, qprocess):
        self.qprocesses.append(qprocess)

    def toolOnFinished(self, qprocess):
        self.qprocesses.remove(qprocess)
    
    def sendTextToBox(self, text):
        cursorBox = self.statusBox.textCursor()
        cursorBox.movePosition(cursorBox.End)
        cursorBox.insertText(str(text))
        self.statusBox.ensureCursorVisible()
    
    def data_ready_std(self, process, process_color):
        box = self.statusBox
        cursor_box = box.textCursor()
        cursor_box.movePosition(cursor_box.End)

        std_format = cursor_box.charFormat()
        new_format = cursor_box.charFormat()

        std_format.setBackground(Qt.white)
        std_format.setForeground(Qt.black)

        # modify it
        new_format.setBackground(process_color)
        new_format.setForeground(process_color.lighter(160))
        # apply it
        cursor_box.setCharFormat(new_format)

        cursor_box.insertText('%s (std):   %s' % (datetime.datetime.now(), str(process.readAllStandardOutput())))
        logging.info( '%s (std):   %s' % (datetime.datetime.now(), str(process.readAllStandardOutput())))

        cursor_box.movePosition(cursor_box.End)
        char_format = cursor_box.charFormat()
        char_format.setBackground(Qt.white)
        char_format.setForeground(Qt.black)
        cursor_box.setCharFormat(std_format)

        cursor_box.insertText('\n')

        self.statusBox.ensureCursorVisible()

    def dataReadyErr(self, process, pColor):
        #color = QColor(255, 0, 0)
        box = self.statusBox
        #box.setTextColor(color)
        cursorBox = box.textCursor()
        cursorBox.movePosition(cursorBox.End)

        # get the current format
        stdFormat = cursorBox.charFormat()
        newFormat = cursorBox.charFormat()

        stdFormat.setBackground(Qt.white)
        stdFormat.setForeground(Qt.black)

        # modify it
        newFormat.setBackground(pColor)
        newFormat.setForeground(pColor.darker(160))
        # apply it
        cursorBox.setCharFormat(newFormat)

        cursorBox.insertText('%s (err):   %s' %(datetime.datetime.now(), str(process.readAllStandardError())))
        logging.warning('%s (err):   %s' %(datetime.datetime.now(), str(process.readAllStandardError())))

        cursorBox.movePosition(cursorBox.End)
        format = cursorBox.charFormat()
        format.setBackground(Qt.white)
        format.setForeground(Qt.black)
        cursorBox.setCharFormat(stdFormat)

        cursorBox.insertText('\n')

        self.statusBox.ensureCursorVisible()

    def toggleContentBrowser(self):
        if self.assetsShotsTabWidget.isVisible() == True:
            self.assetsShotsTabWidget.setVisible(False)
        else:
            self.assetsShotsTabWidget.setVisible(True)
     
    def toggleConsole(self):
        if self.statusBox.isVisible() == True:
            self.statusBox.setVisible(False)
        else:
            self.statusBox.setVisible(True)
    
    def toggleNodeName(self):
        if self.nodeOptionsWindow.isVisible() == True:
            self.nodeOptionsWindow.setVisible(False)
        else:
            self.nodeOptionsWindow.setVisible(True)
         
    def toggleDescription(self):
        if self.descriptionWindow.isVisible() == True:
            self.descriptionWindow.setVisible(False)
        else:
            self.descriptionWindow.setVisible(True)
    
    def toggleNodesWindow(self):
        if self.nodesWindow.isVisible() == True:
            self.nodesWindow.setVisible(False)
        else:
            self.nodesWindow.setVisible(True)

    def graphicsView_wheelEvent(self, event):
        
#         numSteps = event.delta() / 15 / 8
#         
#         if numSteps == 0:
#             event.ignore()
#             
#         sc = 1.25 * numSteps
#         self.zoom(sc, self.mapToScene(event.pos()))
#         event.accept()
         
        factor = 1.15
          
        #self.nodeView.centerOn()
          
        #print 'event.delta() = %s' %event.delta()
          
        if event.delta() > 0:
            self.nodeView.scale(factor, factor)
            self.nodeView.centerOn(event.pos())
              
        else:
            self.nodeView.scale(1.0 / factor, 1.0 / factor)
            self.nodeView.centerOn(event.pos())
        # print 'scaling factor = %f' %self.nodeView.transform().m11()

#     def zoom(self, factor, centerPoint):
#         scale(factor, factor)
#         centerOn(centerPoint)

    def graphicsView_resizeEvent(self, event):
        pass

    def setNodeMenuWidget(self):
        print "duude"
        #self.nodeMenuArea.takeWidget()
        #self.nodeMenuArea.setWidget(item.getWidgetMenu())
        #self.nodeOptionsWindow.setTitle(item.displayText.toPlainText())


if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)
    logging.info('launching PyPELyNE')
    app = QApplication(sys.argv)
    # app.aboutToQuit.connect(deleteGLWidget)
    screenSize = QApplication.desktop().availableGeometry()
    logging.info('screen resolution is %ix%i' %(int(screenSize.width()), int(screenSize.height())))
    pypelyneWindow = PypelyneMainWindow()
    # screenSize = QApplication.desktop().availableGeometry()
    pypelyneWindow.resize(int(screenSize.width()), int(screenSize.height()))
    pypelyneWindow.show()
    app.exec_()