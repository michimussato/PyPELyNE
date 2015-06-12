# coding: utf-8

from PyQt4 import QtCore, QtGui

app = QtGui.QApplication([])
window = QtGui.QWidget()
grid = QtGui.QGridLayout()

def callback(button):
   print button

for x in range(10):
   b = QtGui.QPushButton()
   b.setText(unicode(x))
   grid.addWidget(b, 0, x)
   window.connect(b, QtCore.SIGNAL("clicked()"), (lambda: callback(x))
   b.show()

window.setLayout(grid)
window.show()
app.exec_()