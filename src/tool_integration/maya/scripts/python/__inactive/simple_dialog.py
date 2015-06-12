from PyQt4 import QtCore
from PyQt4 import QtGui
import maya.cmds


class RenamingDialog(QtGui.QWidget):

	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		
		self.setWindowTitle("Create Geo")
		self.setWindowFlags(QtCore.Qt.Tool)
		#self.setFixedSize(200, 50)
		
		self.button01 = QtGui.QPushButton('Sphere', self)
		self.button01.clicked.connect(self.handleButton01)
		
		self.button02 = QtGui.QPushButton('Cube', self)
		self.button02.clicked.connect(self.handleButton02)
		
		self.button03 = QtGui.QPushButton('List objects', self)
		self.button03.clicked.connect(self.handleButton03)
		
		self.buttonQuit = QtGui.QPushButton('Quit Maya', self)
		self.buttonQuit.setGeometry(10,10,60,35)
		self.connect(self.buttonQuit, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
				
		layout = QtGui.QVBoxLayout(self)
		layout.addWidget(self.button01)
		layout.addWidget(self.button02)
		layout.addWidget(self.button03)
		layout.addWidget(self.buttonQuit)
		
	def handleButton01(self):
	    maya.cmds.polySphere()
	    
	def handleButton02(self):
		maya.cmds.polyCube()
		
	def handleButton03(self):
		print(maya.cmds.ls(geometry=True))
	
		
if __name__ == "__main__":
	dialog = RenamingDialog()
	
	dialog.show()