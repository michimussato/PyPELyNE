from PyQt4 import QtCore, QtGui
import maya.cmds as mc
import maya.mel as mel

# def main(argv):
# 	app = QtGui.QApplication(argv)
# 	mainwindow = MainWindow()
# 	mainwindow.show()
# 	sys.exit(app.exec_())
	
class objBatchExport( QtGui.QMainWindow ):
	
	def __init__( self, *args ):
		QtGui.QMainWindow.__init__( self, *args )
		self.createUI()
		self.createLayout()
		self.createConnects()
		self.checkPlugin()
		self.errors = 0

			
	def checkPlugin( self ):
		pluginLoaded = mc.pluginInfo( 'objExport', query=True, loaded=True )
		
		if pluginLoaded == False:
			try:
				mc.loadPlugin( 'objExport' )
				self.statusBar.showMessage( 'objExport plugin loaded successfully' )
				print 'objExport plugin loaded successfully'
			except:
				self.statusBar.showMessage( 'could not load objExport plugin. load manually.' )
				print 'could not load objExport plugin. load manually.'
		elif pluginLoaded == True:
			self.statusBar.showMessage( 'objExport plugin already loaded' )
			print 'objExport plugin already loaded'
			
		
	def createUI( self ):
		self.setWindowTitle( 'obj batch export' )
		self.setWindowFlags( QtCore.Qt.Tool )
		
		#self.fileDialog = QtGui.QFileDialog()
		#self.fileDialog.setOption(QtGui.QFileDialog.ShowDirsOnly)
		#self.fileDialog.setViewMode(0)
		self.pushButtonBrowse = QtGui.QPushButton( 'set target directory' )
		self.lineEditBrowse = QtGui.QLineEdit()
		self.lineEditBrowse.setVisible( False )
		self.editTextLabel = QtGui.QLabel( 'select set:' )
		#self.editText = QtGui.QLineEdit()
		
		self.setsDropDown = QtGui.QComboBox()
		mayaSets = mc.ls( sets=True )
		self.setsDropDown.addItem( '' )
		for element in mayaSets:
			self.setsDropDown.addItem( element )
			
		self.spacerItem = QtGui.QSpacerItem( 40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum )
		self.pushButtonCancel = QtGui.QPushButton( 'cancel' )
		self.pushButtonStart = QtGui.QPushButton( 'start' )
		self.statusBar = QtGui.QStatusBar()
		#self.statusBar.setVisible(True)
		
	def createLayout( self ):
		vBoxLayout = QtGui.QVBoxLayout()
		
		hBoxLayoutFileDialog = QtGui.QHBoxLayout()
		hBoxLayoutFileDialog.addWidget( self.pushButtonBrowse )
		hBoxLayoutFileDialog.addWidget( self.lineEditBrowse )
		
		vBoxLayout.addLayout( hBoxLayoutFileDialog )
		
		#vBoxLayout.addWidget(self.fileDialog)
		
		hBoxLayoutPrefix = QtGui.QHBoxLayout()
		hBoxLayoutPrefix.addWidget( self.editTextLabel )
		#hBoxLayoutPrefix.addWidget(self.editText)
		hBoxLayoutPrefix.addWidget( self.setsDropDown )
		
		vBoxLayout.addLayout( hBoxLayoutPrefix )
		
		hBoxLayoutStart = QtGui.QHBoxLayout()
		hBoxLayoutStart.addItem( self.spacerItem )
		hBoxLayoutStart.addWidget( self.pushButtonCancel )
		hBoxLayoutStart.addWidget( self.pushButtonStart )
		
		vBoxLayout.addLayout( hBoxLayoutStart )
		
		vBoxLayout.addWidget( self.statusBar )
		
		#vBoxLayout.addWidget(self.pushButtonStart)
		
		widgetCentral = QtGui.QWidget()
		widgetCentral.setLayout( vBoxLayout )
		self.setCentralWidget( widgetCentral )
		
		
	def createConnects( self ):
		self.pushButtonCancel.clicked.connect( self.close )
		self.pushButtonBrowse.clicked.connect( self.selectFile )
		self.pushButtonStart.clicked.connect( self.runExport )
		
	def selectFile( self ):
		#either maya cmds fileDialog2
		outputDir = mc.fileDialog2( fileMode=3, dialogStyle=2, startingDirectory=mc.workspace( q=True, directory=True ), caption='choose directory', okCaption='use this directory', cancelCaption='cancel' )
		self.lineEditBrowse.setText( str( outputDir[ 0 ] ) )
		self.lineEditBrowse.setVisible( True )
		#or this way using QtGui.QFileDialog
		#outputDir = self.fileDialog.getExistingDirectory()
		#self.lineEditBrowse.setText(outputDir)
		
	def runExport( self ):
		#self.statusBar.showMessage( 'exporting...' )
		currentSet = str( self.setsDropDown.currentText() )
		#print currentSet
		currentSetMembers = cmds.select( currentSet )
		currentSelection = cmds.ls( sl=1,fl=1 )
		exportDirectory = str( self.lineEditBrowse.text() )
		
		#print cmds.ls(currentSetMembers)
		#print exportDirectory
		
		for item in currentSelection:
			fullExportDirectory = '%s/%s__%s.obj' %( exportDirectory, currentSet, item )
			try:
				cmds.select( item )
				mel.eval( 'file -force -options "groups=0;ptgroups=0;materials=0;smoothing=1;normals=1" -typ "OBJexport" -pr -es "%s";' %( fullExportDirectory ) )
			except:
				self.errors = self.errors + 1
				self.statusBar.showMessage( 'Ignoring object named: %s. Export failed, probably not a polygonal object. ' %(item) )
				print 'Ignoring object named: %s. Export failed, probably not a polygonal object. ' %( item )

		#self.statusBar.setVisible(True)
		self.statusBar.showMessage( 'export completed with %d errors' %self.errors )


objBatchExportClass = objBatchExport()
		
if __name__ == "__main__":
	mainwindow = objBatchExport()
	mainwindow.show()