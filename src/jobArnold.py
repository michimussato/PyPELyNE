import sys, os, platform


import xml.etree.ElementTree as ET
from PyQt4.QtGui import *
from PyQt4.uic import *


class jobAddArgUi( QWidget ):
	def __init__( self, mainWindow, argValue = None, parent = None ):
		super( jobAddArgUi, self ).__init__( parent )

		self.mainWindow = mainWindow
		self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
		#print argValue
		self.currentPlatform = self.mainWindow.getCurrentPlatform()
		'''
		if self.currentPlatform == "Windows":
			self.ui = loadUi( r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\jobAddArg.ui', self )
		elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
			self.ui = loadUi( r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/jobAddArg.ui', self )
		'''

		self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'jobAddArg.ui' ), self )
		#self.createConnects()

		self.pushButtonDelete.setVisible( False )

		if not bool( argValue ) == False:
			self.lineEditArg.setText( argValue )

	def returnLineEditValue( self ):
		return self.lineEditArg.text()

	def createConnects( self ):
		self.pushButtonDelete.clicked.connect( self.delete )

	def delete( self ):
		#print 'hallo'
		self.deleteLater()


class jobAddPropUi( QWidget ):
	def __init__( self, mainWindow, propValue = None, parent = None ):
		super( jobAddPropUi, self ).__init__( parent )

		self.mainWindow = mainWindow
		self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
		#print argValue
		self.currentPlatform = self.mainWindow.getCurrentPlatform()

		#print propValue
		#self.currentPlatform = platform.system()
		'''
		if self.currentPlatform == "Windows":
			self.ui = loadUi( r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\jobAddProp.ui', self )
		elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
			self.ui = loadUi( r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/jobAddProp.ui', self )
		'''

		self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'jobAddProp.ui' ), self )

		#self.createConnects()

		self.pushButtonDelete.setVisible( False )

		if not bool( propValue ) == False:
			self.lineEditProp.setText( propValue )

	def returnLineEditValue( self ):
		return self.lineEditProp.text()

	def createConnects( self ):
		self.pushButtonDelete.clicked.connect( self.delete )

	def delete( self ):
		#print 'hallo'
		self.deleteLater()
		





class jobArnoldUi( QDialog ):
	def __init__( self, taskRoot, mainWindow = None, parent = None ):
		super( jobArnoldUi, self ).__init__( parent )

		#print 'init'

		self.mainWindow = mainWindow
		self.pypelyneRoot = self.mainWindow.getPypelyneRoot()
		self.currentPlatform = self.mainWindow.getCurrentPlatform()
		self.exclusions = mainWindow.getExclusions()

		self.taskRoot = taskRoot
		# /Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/projects/proj1/content/assets/test/RND_CIN__asdfgsd
		self.projectName = os.path.basename( os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname( self.taskRoot ) ) ) ) )
		self.assetName = os.path.basename( os.path.dirname( self.taskRoot ) )
		self.startupDirectory = r'/Applications/MtoA-1.2.2.0-darwin-2014/bin'
		#self.startupDirectory = self.taskRoot
		self.taskName = os.path.basename( self.taskRoot )

		inputContent = os.listdir( os.path.join( self.taskRoot, 'input' ) )

		self.input = []

		for directory in inputContent:
			if not directory in self.exclusions:
				self.input.append( os.path.join( self.taskRoot, 'input', directory ) )

		self.input = self.input[ 0 ]

		self.inputLink = os.path.realpath( self.input )
		#print self.inputLink

		#self.input = os.path.join( self.taskRoot, 'input', directory )

		#self.inputSequence = os.listdir( self.input )
		#self.input = os.path.join( self.taskRoot, 'input', 'ASS_input' )
		#print self.input
		self.inputName = getattr( os.path.basename( self.input ).split( '.' ), '__getitem__' )( -1 )
		#print getattr( os.path.basename( self.input ).split( '.' ), '__getitem__' )( -1)

		outputContent = os.listdir( os.path.join( self.taskRoot, 'output' ) )
		#os.path.join( self.taskRoot, 'output', os.listdir( os.path.join( self.taskRoot, 'output' ) ) )

		#print self.outputContent

		self.output = []

		for directory in outputContent:
			#print type(directory)
			#print self.exclusions
			if not directory in self.exclusions:
				self.output.append( os.path.join( self.taskRoot, 'output', directory ) )

		self.output = self.output[ 0 ]

		#self.output = os.path.join( self.taskRoot, 'output', 'SEQ_output', 'version_0014' )
		self.outputName = os.path.basename( self.output )
		#print self.outputName
		self.outputVersion = os.readlink( os.path.join( self.output, 'current' ) )
		#print self.outputVersion

		#self.pypelyneRoot = os.getcwd()
		#self.currentPlatform = platform.system()
		'''
		if self.currentPlatform == "Windows":
			self.ui = loadUi( r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\jobArnold.ui', self )
		elif self.currentPlatform == "Linux" or self.currentPlatform == "Darwin":
			self.ui = loadUi( r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/ui/jobArnold.ui', self )
		'''

		self.ui = loadUi( os.path.join( self.pypelyneRoot, 'ui', 'jobArnold.ui' ), self )



		self.propWidgets = []
		self.argWidgets = []

		self.initialStates = [ 'Suspended', 'Active' ]

		self.submissionCmdArgs = []

		self.submissionCmd = r'/Applications/Deadline/Resources/bin/deadlinecommand'
		

		self.plugin = r'kick'
		
		self.props = [ ( 'Comment', 'Arnold' ), ( 'Interruptible', 'true' ), ( 'ForceReloadPlugin', 'false' ), ( 'OutputDirectory0', self.output + os.sep + self.outputVersion ), ( 'OutputFilename0', self.outputName + '.####.exr' ), ( 'Name', self.projectName + '  |  ' + self.assetName + '  |  ' + self.taskName + '  |  ' + self.outputName + '  |  ' + self.outputVersion ) ]
		#self.props = [ ( 'Comment', 'Arnold' ) ]
		#self.args = [ ( '-v', '2' ) ]
		self.args = [ \
		 				( '-v', '2' ), \
		 				( '-as', '3' ), \
		 				( '-ds', '2' ), \
		 				( '-gs', '2' ), \
		 				( '-dw', '' ), \
		 				( '-nstdin', '' ), \
		 				( '-bs', '16' ), \
		 				( '-i', '<QUOTE>' + self.inputLink + os.sep + self.inputName + '.' + '<STARTFRAME%4>' + '.ass' + '<QUOTE>' ), \
		 				( '-o', '<QUOTE>' + self.output + os.sep + self.outputVersion + os.sep + self.outputName + '.' + '<STARTFRAME%4>' + '.exr' + '<QUOTE>' ) ]




		#self.valueApplications = ET.parse( os.path.join( self.pypelyneRoot, 'conf', 'valueApplications.xml' ) )
		#self.valueApplicationsRoot = self.valueApplications.getroot()

		self.createConnects()

		self.setValues()

	def setValues( self ):
		#print 'setValues'
		self.labelExecutable.setText( os.path.join( self.startupDirectory, self.plugin ) )
		self.labelStartupDirectory.setText( self.startupDirectory )
		self.labelJobName.setText( self.taskName )
		self.labelInput.setText( os.path.basename( self.input ) + ' (' + os.path.basename( self.inputLink ) + ')' )
		self.labelOutput.setText( self.outputName + ' (' + self.outputVersion + ')' )
		for initialStatus in self.initialStates:
			self.comboBoxInitialStatus.addItem( initialStatus )

		for arg in self.args:
			argValue = str( arg[ 0 ] + ' ' + arg[ 1 ] )
			newArg = self.addArg( argValue )

		for prop in self.props:
			propValue = str( prop[ 0 ] + '=' + prop[ 1 ] )
			newProp = self.addProp( propValue )
			#print str( prop[ 0 ] + '=' + prop[ 1 ] )


			


	def createConnects( self ):
		#print 'createConnects'
		self.pushButtonAddProp.clicked.connect( self.addProp )
		self.pushButtonAddArg.clicked.connect( self.addArg )
		self.pushButtonOk.clicked.connect( self.onOk )
		self.pushButtonCancel.clicked.connect( self.onCancel )

	def addArg( self, argValue=None ):
		#print 'addArg'
		newArg = jobAddArgUi( self.mainWindow, argValue )

		self.vLayoutProps.addWidget( newArg )
		self.argWidgets.append( newArg )

	def addProp( self, propValue=None ):
		#print 'addProp'
		newProp = jobAddPropUi( self.mainWindow, propValue )

		self.vLayoutProps.addWidget( newProp )
		self.propWidgets.append( newProp )
		#newProp.pushButtonDelete.clicked.connect( lambda: self.delProp( newProp ) )

	def delProp( self, propUi ):
		print 'delProp'
		#pass
		#self.deleteLater( propUi )
		#self.vLayoutProps.removeWidget( self )

	def onOk( self ):
		#print 'onOk'
		self.submissionCmdArgs.append( self.submissionCmd )
		self.submissionCmdArgs.append( '-SubmitCommandLineJob' )

		#print '1', self.submissionCmdArgs

		args = []
		props = []

		for argWidget in self.argWidgets:
			if not str( argWidget.returnLineEditValue() ) == '' or str( argWidget.returnLineEditValue() ) == ' ':
				#print str( argWidget.returnLineEditValue() )
				args.append( str( argWidget.returnLineEditValue() ) )

		for propWidget in self.propWidgets:
			if not str( propWidget.returnLineEditValue() ) == '' or str( propWidget.returnLineEditValue() ) == ' ':
				props.append( str( propWidget.returnLineEditValue() ) )


		#print '2', self.submissionCmdArgs

		startupDirectory = str( self.labelStartupDirectory.text() )
		chunkSize = str( self.spinBoxChunkSize.value() )
		frames = str( self.lineEditFrames.text() )
		initialStatus = str( self.comboBoxInitialStatus.currentText() )
		concurrentTasks = str( self.spinBoxConcurrentTasks.value() )

		
		argsString = ' '.join( args )
		#propsString = ' '.join( props )

		

		#arguments = 
		priority = str( self.spinBoxPropPriority.value() )
		props.append( 'Priority=' + priority )

		props.append( 'ConcurrentTasks=' + concurrentTasks )
		
		#initialStatus = 
		#print 'test'
		self.submissionCmdArgs.append( '-executable ' + '"' + self.plugin + '"' )
		self.submissionCmdArgs.append( '-startupdirectory ' + '"' + startupDirectory + '"' )
		#self.submissionCmdArgs.append( '-chunksize ' + '"' + chunkSize + '"' )
		self.submissionCmdArgs.append( '-arguments ' + '"' + argsString + '"' )
		self.submissionCmdArgs.append( '-frames ' + '"' + frames + '"' )
		self.submissionCmdArgs.append( '-initialstatus ' + '"' + initialStatus + '"' )

		for prop in props:
			#print prop, 'appended'
			self.submissionCmdArgs.append( '-prop ' + '"' + prop + '"' )
		#self.submissionCmdArgs.append( [ '', ] )
		#self.submissionCmdArgs.append( [ '', ] )

		#print 'new\n', self.submissionCmdArgs, '\n'
		self.accept()
		#return self.submissionCmdArgs

	def submitData( self ):
		#self.accept()
		return self.submissionCmdArgs

	def onCancel( self ):
		pass
		self.reject()


	@staticmethod
	def getArnoldData( nodeDir, mainWindow ):
		#print 'fuck'
		dialog = jobArnoldUi( nodeDir, mainWindow )
		result = dialog.exec_()
		submissionCmdArgs = dialog.submitData()
		#print result
		#print submissionCmdArgs
		return result == dialog.Accepted, submissionCmdArgs







def main():
	app = QApplication( sys.argv )

	taskFolder = r'/Users/michaelmussato/Dropbox/development/workspace/PyPELyNE/projects/proj1/content/assets/asset_01/RND_DDL__vvasdfa'

	ok, jobArnold = jobArnoldUi.getArnoldData( taskFolder )

	#print jobArnold
	#if ok:
		#print jobArnold
	#screenCastInstance = screenCast( 'asset01', 'task_01')
	#screenCastInstance.startCast()
	
	#screenCastInstance.stopCast()
	#print 'fuck it'
	#time.sleep( 15 )
	#screenCastInstance.stopCast()
	#screenCastInstance.quit()
	#jobArnoldWidget.show()
	#app.exec_()



if __name__ == "__main__":
	main()