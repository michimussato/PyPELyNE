import PyQt4.QtGui as gui, PyQt4.QtCore as core

app = gui.QApplication([])

cb = gui.QComboBox()

cb.addItem('int 1',100)
cb.addItem('int 2',200)
cb.addItem('int 3',300)
cb.addItem('int 4',400)

print cb.itemData(0).toInt()[0]

core.pyqtSlot('int')
def f(index):
    data, can_convert = cb.itemData(index).toInt()
    if can_convert:
        print 'integer:',data

cb.currentIndexChanged.connect(f)

cb.show()

app.exec_()