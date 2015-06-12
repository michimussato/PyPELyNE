import sys
from PyQt4 import QtCore, QtGui
app = QtGui.QApplication(sys.argv)
sb = QtGui.QScrollBar()
sb.setMinimum(0)
sb.setMaximum(100)
def on_slider_moved(value): print "new slider position: %i" % (value, )
sb.connect(sb, QtCore.SIGNAL("sliderMoved(int)"), on_slider_moved)
sb.show()
app.exec_()