from PyQt4 import QtCore
from PyQt4 import QtGui

class RenamingDialog(QtGui.QDialog):

	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		
		self.setWindowTitle("Renaming Dialog")
		self.setFixedSize(250, 200)
		
if __name__ == "__main__":
	dialog = RenamingDialog()
	
	dialog.show()