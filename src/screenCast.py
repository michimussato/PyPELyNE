
import os, sys, time, subprocess, getpass, datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *

# xterm -T "ScreenCapture" -e /Applications/VLC.app/Contents/MacOS/VLC -I rc --rc-fake-tty --rc-unix=vlc.sock screen:// screen:// --screen-fps=4 --quiet --sout "#transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst=test.mp4}"
# /Applications/VLC.app/Contents/MacOS/VLC -I rc --rc-fake-tty --rc-unix=vlc.sock screen:// --screen-fps=4 --quiet --sout "#transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst=test.mp4}"


class screenCast( QProcess ):
	def __init__( self, assetName, taskName, projectPath ):
		super( screenCast, self ).__init__( None )

		self.vlcExec = r'/Applications/VLC.app/Contents/MacOS/VLC'

		self.now = datetime.datetime.now().strftime( '%Y-%m-%d_%H%M-%S-%f' )

		self.projectPath = projectPath
		self.assetName = assetName
		self.taskName = taskName
		self.makingOfDir = os.path.join( self.projectPath, 'making_of' )
		
		self.user = getpass.getuser()

		if not os.path.exists( self.makingOfDir ):
			os.makedirs( self.makingOfDir, mode=0777 )

		#self.mp4 = r'/Users/michaelmussato/' + self.now + '__' + self.user + '__' + self.assetName + '__' + self.taskName + '.mp4'
		self.mp4 = self.makingOfDir + os.sep + self.now + '__' + self.user + '__' + self.assetName + '__' + self.taskName + '.mp4'
		#print self.mp4

		#print os.path.expanduser('~'), str( 'vlc.sock' + '.' + self.now + '__' + self.user + '__' + self.assetName + '__' + self.taskName )

		#self.vlcSocket = os.path.join( os.path.expanduser('~'), str( 'vlc.sock' + '.' + self.now + '__' + self.user + '__' + self.assetName + '__' + self.taskName ) )
		self.vlcSocket = os.path.join( os.path.expanduser('~'), str( 'vlc.sock' + '.' + self.now ) )

		self.vlcArgs = [ r'/Applications/VLC.app/Contents/MacOS/VLC', '-I', 'rc', '--rc-fake-tty', '--rc-unix', self.vlcSocket, 'screen://', '--screen-fps', '4', '--quiet', '--sout', '#transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst=' + self.mp4 + '}' ]

		#self.vlcArgs = [ r'screen://', '--screen-fps','4', '--quiet', '--sout', str( '#transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst="/Users/michaelmussato/test.mp4"}' ) ]
		
		#self.vlcArgs = r'-I rc --rc-fake-tty --rc-unix="/Users/michaelmussato/vlc.sock" screen:// --screen-fps=4 --quiet --sout #transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst=/Users/michaelmussato/test.mp4}'

		#print self.vlcSocket
		#print self.vlcArgs




	def start( self ):
		'''
		self.process = QProcess()
		self.process.start( self.vlcExec, self.vlcArgs )
		'''

		#print ' '.join( self.vlcArgs )
		
		#os.system( ' '.join( self.vlcArgs ) )
		
		#http://stackoverflow.com/questions/3516007/run-process-and-dont-wait
		#subprocess.call( [ r'/Applications/VLC.app/Contents/MacOS/VLC', '-I', 'rc', '--rc-fake-tty', '--rc-unix', self.vlcSocket, 'screen://', '--screen-fps', '4', '--quiet', '--sout', '#transcode{vcodec=h264,vb=512,scale=0.5}:standard{access=file,mux=mp4,dst=/Users/michaelmussato/test.mp4}' ] )
		try:
			subprocess.Popen( self.vlcArgs, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
			print 'screencast for %s started' %( self.taskName )
		except:
			print 'startCast failed'

		#subprocess.call( self.vlcArgs )

		#print output

		#quit()




		#time.sleep( 10 )
		#self.stopCast()
		#self.stopCast( self.process )
		#self.process.start( self.vlcExec )

	def stop( self ):

		#commandStop = [ 'echo', 'stop', '|', 'nc', '-U', '/Users/michaelmussato/vlc.sock' ]
		#commandQuit = [ 'echo', 'quit', '|', 'nc', '-U', '/Users/michaelmussato/vlc.sock' ]


		#try:
		commandStop = "echo stop | nc -U " + self.vlcSocket
		commandQuit = "echo quit | nc -U " + self.vlcSocket

		#print commandStop
		#print commandQuit

		#time.sleep( 15 )

		os.system( commandStop )
		os.system( commandQuit )
		#self.quit()
		#except:
		print 'screenCast on %s finished' %( self.taskName )
		print 'video created at %s' %( self.mp4 )


	def quit( self ):
		print 'exitting'
		quit()





def main():
	app = QApplication( sys.argv )
	screenCastInstance = screenCast( 'asset01', 'task_01')
	screenCastInstance.start()
	
	#screenCastInstance.stopCast()
	#print 'fuck it'
	time.sleep( 15 )
	screenCastInstance.stop()
	screenCastInstance.quit()

	return app.exec_()



if __name__ == "__main__":
	main()

	
	#print "starting PyPELyNE"
	
	#app.aboutToQuit.connect(deleteGLWidget)
	#screenSize = QApplication.desktop().availableGeometry()
	#print 'screen resolution is %ix%i' %( int( screenSize.width() ), int( screenSize.height() ) )
	
	#screenSize = QApplication.desktop().availableGeometry()
	#pypelyneWindow.resize( int( screenSize.width() ), int( screenSize.height() ) )
	#pypelyneWindow.show()
	#app.exec_()